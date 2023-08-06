import os, datetime, logging
from struct import unpack
import numpy as np

from . import sfdics, sfhread, sfobj, manage_ed, parse_kwargs, str_byt, libddc

PPGCLOCK = [1e-6, 1e-5, 1e-4, 1e-3]

logger = logging.getLogger('aug_sfutils.sfread')
date_fmt = '%Y-%m-%d'


def read_other_sf(*args, **kwargs):

    return SFREAD(*args, **kwargs)


def parse_url(url, blen=100):
    """
    Read URL content
    """

    try:
        import urllib3
        url_lib = 'urllib3'
    except:
        try:
            import urllib2
            url_lib = 'urllib2'
        except:
            try:
                import urllib
                url_lib = 'urllib'
            except:
                logger.error('No urllib(2, 3) found')
                return None

    url_not_found = 'URLs %s not found' %url
    if url_lib == 'urllib3':
        http = urllib3.PoolManager()
        try:
            tmp = http.request('GET', url)
        except:
            logger.error(url_not_found)
            return None
        bshot = tmp.data
    elif url_lib == 'urllib2':
        try:
            bshot = urllib2.urlopen(url).read(blen)
        except:
            logger.error(url_not_found)
            return None
    elif url_lib == 'urllib':
        try:
            bshot = request.urlopen(url).read()
        except:
            logger.error(url_not_found)
            return None

    return bshot


def getlastshot():
    """
    Gets last shot number from the AUG webpage(s)
    """

    try:
        from . import journal
        return journal.getLastShot()
    except:
        pass
    url1 = 'http://ssr-mir.aug.ipp.mpg.de:9090/Diag/ShotNumber.dta'
    url2 = 'https://www.aug.ipp.mpg.de/aug/local/aug_only/journal_today_2.html'
    bshot = parse_url(url1)
    if bshot is None:
        page = parse_url(url2, blen=5000)
        if page is None:
            return None
        else:
            page = str_byt.to_str(page)
            idx = page.find("Current shot:")
            if idx < 0:
                logger.warning('Missing substring "Current shot:" in %s, exiting' %url2)
                return None
            substr = page[idx:idx+30]
            a = substr.find('>')+1
            b = substr.find('<', a)
            nshot = int(substr[a:b])-1
    else:
        sshot = str_byt.to_str(bshot)
        try:
            nshot = int(sshot)
        except:
            logger.error('ERROR sfread.getlastshot: cannot convert string %s to integer' %sshot)
            nshot = None

    return nshot


def getcti_ts06(nshot):
    """
    Gets the absolute time (ns) of a discharge trigger 
    """
    diag = 'CTI'
    cti = SFREAD(nshot, diag)
    try:
        cdev = cti.getdevice('LAM')
        ts06 = cdev['PhyReset']
        if ts06 == 0:
            ts06 = cdev['TS06']
        if ts06 == 0:
            ts06 = cdev['CT_TS06']
    except: # shot < 35318
        cdev = cti.getdevice('TS6')
        ts06 = cdev['TRIGGER']

    return ts06


def getgc(nshot=30136):
    """
    Returns first wall contours for plotting
    """
    ygc_sf = [1996, 8646, 8650, 9401, 11300, 11301, 11320, 12751, 13231, 14051, 14601, 16310, 16315, 18204, 19551, 21485, 25891, 30136]
    ygc_sf = np.array(ygc_sf)
    nshot = np.max(ygc_sf[ygc_sf <= nshot])
    ygc = SFREAD(nshot, 'YGC')
    if ygc is not None:
        rrgc     = ygc.getobject('RrGC')
        zzgc     = ygc.getobject('zzGC')
        inxlen   = ygc.getobject('inxlen')
        flag_use = ygc.getobject('ixplin')
        gcnames  = ygc.getobject('chGCnm')

    comp_d = {}

    inxbeg = np.cumsum(np.append(0, inxlen))

    if gcnames is None:
        for jcom, leng in enumerate(inxlen):
            comp_d[jcom] = type('', (), {})() # empty object
            comp_d[jcom].r = rrgc[inxbeg[jcom]: inxbeg[jcom+1]]
            comp_d[jcom].z = zzgc[inxbeg[jcom]: inxbeg[jcom+1]]
    else:
        for jcom, lbl in enumerate(gcnames):
            lbl = str_byt.to_str(lbl)
            if flag_use[jcom] > 0:
                comp_d[lbl] = type('', (), {})()
                comp_d[lbl].r = rrgc[inxbeg[jcom]: inxbeg[jcom+1]]
                comp_d[lbl].z = zzgc[inxbeg[jcom]: inxbeg[jcom+1]]
    
    return comp_d


class SFREAD:
    """
    Class for reading ASDEX Upgrade shotfile data
    """

    def __init__(self, *args, **kwargs):
        """
        Opens a shotfile, reads the header
        """

        self.shot = None
        self.diag = None
        self.exp = None
        self.status = False
        self.open(*args, **kwargs)


    def open(self, *args, **kwargs):

        if 'sfh' in kwargs.keys():
            self.sfile = kwargs['sfh']
        if 'sf' in kwargs.keys():
            self.sfile = kwargs['sf']
        if hasattr(self, 'sfile'):
            self.shot = 0
            self.ed = 0
            self.diag = os.path.basename(self.sfile)[:3]

        else:

            n_args = len(args) 
            if n_args == 0:
                logger.warning('No argument given, need at least diag_name')
                return
            if isinstance(args[0], str) and len(args[0].strip()) == 3:
                diag = args[0].strip()
                if n_args > 1: 
                    if isinstance(args[1], (int, np.integer)):
                        nshot = args[1]
            elif isinstance(args[0], (int, np.integer)):
                nshot = args[0]
                if n_args > 1:
                    if isinstance(args[1], str) and len(args[1].strip()) == 3:
                        diag = args[1].strip()
            if 'nshot' not in locals(): 
                logger.warning('No argument is a shot number (int), taking last AUG shot')
                nshot = getlastshot()
            if 'diag' not in locals():
                diag = input('Please enter a diag_name (str(3), no delimiter):\n')

            exp = parse_kwargs.parse_kw( ('exp', 'experiment'), kwargs, default='AUGD')
            ed  = parse_kwargs.parse_kw( ('ed', 'edition'), kwargs, default=0)
            logger.debug('%d %s %s %d', nshot, diag, exp, ed)
            self.sfile, self.ed = manage_ed.sf_path(nshot, diag, exp=exp, ed=ed)
            if self.sfile is None:
                logger.error('Shotfile not found for %s:%s(%d) #%d', exp, diag, ed, nshot)
                return
            else:
                self.shot = nshot
                self.diag = diag.upper()
                self.exp  = exp  # unused herein, but useful docu

        if os.path.isfile(self.sfile):
            self.time = datetime.datetime.fromtimestamp(os.path.getctime(self.sfile))
            with open(self.sfile, 'rb') as f:
                byt_str = f.read(128000)
                if len(byt_str) < 128:
                    logger.error('Error: shotfile %s has < 128 bytes, ignored' %(self.sfile))
                    return
                self.sfh = sfhread.read_sfh(byt_str)
                self.status = True
        else:
            logger.error('Shotfile %s not found' %self.sfile)
            return

        if self.status:
            self.objects = [ lbl for lbl in self.sfh['obj_nam'] if self.sfh[lbl].obj_type in [6, 7, 8, 13] ]
            self.parsets = [ lbl for lbl in self.sfh['obj_nam'] if self.sfh[lbl].obj_type in [3, 4] ]
        self.cache = {}


    def __call__(self, name):

        if not self.status:
            return None
        if name not in self.cache.keys():
            if name in self.objects:
                self.cache[name] = self.getobject(name)
            elif name in self.parsets:
                self.cache[name] = self.getparset(name)
            else:
                logger.error('Signal %s:%s not found for shot #%d', self.diag, name, self.shot)
                return None
        return self.cache[name]


    def getchunk(self, start, length):
        """
        Reads the requested byteblock from the actual file, not the byt_str
        """
        rdata = None
        with open(self.sfile, 'rb') as f:
            f.seek(start)
            rdata = f.read(length)
        return rdata


    def gettimebase(self, obj):
        """
        Reads the timebase of a given SIG, SGR or AB
        """

        obj = str_byt.to_str(obj)
        sfo = self.sfh[obj]
        otyp = sfo.obj_type
        if otyp == 8:
            return self.getobject(obj)
        elif otyp in (6, 7, 13):
            rels = self.getrelnames(obj)
            for rel in rels:
                if self.sfh[rel].obj_type == 8:
                    return self.getobject(rel)
        return None


    def getareabase(self, obj):
        """
        Reads the areabase of a given SIG or SGR
        """

        obj = str_byt.to_str(obj)
        sfo = self.sfh[obj]
        otyp = sfo.obj_type
        if otyp == 13:
            return self.getobject(obj)
        elif otyp in (6, 7):
            rels = self.getrelnames(obj)
            for rel in rels:
                if self.sfh[rel].obj_type == 13:
                    return self.getobject(rel)
        return None


    def getobject(self, obj, cal=False, nbeg=None, nend=None):
        """
        Reads the data of a given TB, AB, SIG or SGR
        """

        obj = str_byt.to_str(obj)
        data = None
        if obj not in self.sfh.keys():
            logger.error('Signal %s:%s not found for #%d', self.diag, obj, self.shot)
            return None
# Don't uncomment the following lines, to allow 1 cal and 1 uncal reading
#        if obj in self.cache.keys(): 
#            return cache[obj]

        sfo = self.sfh[obj]
        if sfo.status != 0:
            logger.error('Status of SF object %s is %d' %(obj, sfo.status))
            return None
        otyp = sfo.obj_type
        if otyp in (6, 7):
            shape_arr = np.array(sfo.index[::-1][:sfo.num_dims])
        elif otyp == 8:
            shape_arr = np.array([sfo.n_steps])
        elif otyp == 13:
            x = np.array([sfo.size_x, sfo.size_y, sfo.size_z, sfo.n_steps])
            shape_arr = x[x != 0]
        else:
            logger.error('Object %s is no signal, signalgroup, timebase nor areabase, skipping')
            return None

        dfmt = sfo.data_format
        if otyp == 8 and sfo.length == 0:
            if sfo.tbase_type == 1: # PPG_prog, e.g. END:T-LM_END
                dout = self.ppg_time(obj)
            else:   # ADC_intern, e.g. DCN:T-ADC-SL
                dout = (np.arange(sfo.n_steps, dtype=np.float32) - sfo.n_pre)/sfo.s_rate
        else:
            if dfmt in sfdics.fmt2len.keys(): # char variable
                dlen = sfdics.fmt2len[dfmt]
                bytlen = np.prod(shape_arr) * dlen
                data = np.chararray(shape_arr, itemsize=dlen, buffer=self.getchunk(sfo.address, bytlen), order='F')
            else: # numerical variable
                sfmt = sfdics.fmt2struc[dfmt]
                type_len = np.dtype(sfmt).itemsize
                addr = sfo.address
                bytlen = np.prod(shape_arr) * type_len
                if otyp in (7, 8) or self.time_last(obj):
                    if nbeg is None:
                        nbeg = 0
                    else:
                        byt_beg = nbeg*np.prod(shape_arr[:-1])
                        addr   += byt_beg*type_len
                        bytlen -= byt_beg*type_len
                        shape_arr[-1] -= nbeg
                    if nend is not None:
                        bytlen = (nend - nbeg)*np.prod(shape_arr[:-1])*type_len
                        shape_arr[-1] = nend - nbeg
                data = np.ndarray(shape_arr, '>%s' %sfmt, self.getchunk(addr, bytlen), order='F')

# LongLong in [ns] and no zero at TS06
            if otyp == 8 and dfmt == 13: # RMC:TIME-AD0
                dout = 1e-9*(data - self.getts06())
            else:
                dout = sfobj.SFOBJ(data, sfho=sfo) # Add metadata

# Calibrated signals and signal groups
            if otyp in (6, 7) and cal:
                pscal = self.lincalib(obj)
                if pscal is not None:
                    for j in range(10):
                        mult = 'MULTIA0%d' %j
                        shif = 'SHIFTB0%d' %j
                        if mult in pscal.keys():
# we need to fix the content of pscal for signagroups
# assuming first entry wins
                            if (pscal[mult].size > 1):
                                pscal[mult] = pscal[mult][0]
                                pscal[shif] = pscal[shif][0]
                            dout = dout * pscal[mult] + pscal[shif]
                        else:
                            break
                    if self.diag in ('DCN', 'DCK', 'DCR'):
                        dout.phys_unit = '1/m^2'
 
        return dout


    def ppg_time(self, tbobj):
        """
        Returns the time-array in [s] for TB of type PPG_prog
        """

        for rel in self.getrelnames(tbobj):
            if self.sfh[rel].obj_type == 3:
                ppg = self.getdevice(rel)
                if 'PRETRIG' in ppg.keys():
                    pretrig = ppg['PRETRIG']
                if self.sfh[tbobj].n_pre > 0:
                    if pretrig > 0:
                        dt = ppg['RESOLUT'][15] * PPGCLOCK[ppg['RESFACT'][15]] + 1e-6
                    else:
                        dt = 0.
                    start_time = -dt*ppg['PULSES'][0]
                else:
                    start_time = 0.
                time_ppg = []
                start_phase = start_time
                for jphase in range(16):
                    if ppg['PULSES'][jphase] > 0:
                        dt = ppg['RESOLUT'][jphase]*PPGCLOCK[ppg['RESFACT'][jphase]]
                        dtyp = sfdics.fmt2np[self.sfh[tbobj].data_format]
                        tb_phase = dt*np.arange(ppg['PULSES'][jphase], dtype=dtyp) + start_phase
                        time_ppg = np.append(time_ppg, tb_phase)
                        start_phase = time_ppg[-1] + dt
                if len(time_ppg) == 0:
                    return None
                else:
                    return time_ppg
        return None


    def lincalib(self, obj):
        """
        Returns coefficients for signal(group) calibration
        """
        obj = str_byt.to_str(obj)
        for rel in self.getrelnames(obj):
            if self.sfh[rel].obj_type == 4:
                caltyp = str_byt.to_str(sfdics.cal_type[self.sfh[rel].cal_type])
                if caltyp == 'LinCalib':
                    logger.info('PSet for calib: %s' %rel)
                    return self.getparset(rel)
                elif caltyp == 'extCalib':
                    diag_ext = self.getparset(rel)['DIAGNAME']
                    diag_ext = ''.join([str_byt.to_str(x) for x in diag_ext])
                    shot_ext = libddc.previousshot(diag_ext)
                    ext = read_other_sf(shot_ext, diag_ext)
                    return ext.getparset(rel) # same name in external shotfile
        return None


    def getparset(self, pset):
        """
        Returns data and metadata of a Parameter Set
        """

        pset = str_byt.to_str(pset)
        sfo = self.sfh[pset]
        otyp = sfo.obj_type
        if otyp not in (3, 4):
            return None

        buf = self.getchunk(sfo.address, sfo.length)

        j0 = 0
        par_d = {}
        
        for j in range(sfo.items):
            pname = str_byt.to_str(buf[j0: j0+8])
            unit, dfmt, n_items = unpack('>3H', buf[j0+8:  j0+14])
            meta = type('', (), {})()
#            meta.phys_unit = sfdics.unit_d[unit]
            meta.data_format = dfmt
            logger.debug(pname, unit, dfmt, n_items)
            status = unpack('>h', buf[j0+14:  j0+16])[0]
            j0 += 16
            if dfmt in sfdics.fmt2len.keys(): # char variable
                dlen = sfdics.fmt2len[dfmt]
                bytlen = n_items * dlen
                data = np.chararray((n_items,), itemsize=dlen, buffer=buf[j0+2: j0+2+bytlen])
                dj0 = 8 * ( (bytlen + 9)//8 )
                j0 += dj0
            else: # number
                sfmt = sfdics.fmt2struc[dfmt]
                val_len = n_items + 2
                bytlen = val_len * np.dtype(sfmt).itemsize
                fmt = '>%d%s' %(val_len, sfmt)
                if dfmt == 7:
                    data = unpack(sfmt, buf[j0+5: j0+6])[0]
                else:
                    data = unpack(fmt, buf[j0: j0+bytlen])
                    data = np.squeeze(data[2:])
                dj0 = 8 * ( (bytlen + 7)//8 )
                j0 += dj0

            logger.debug(pname, data)
            par_d[pname] = sfobj.SFOBJ(data, sfho=meta)

        return par_d


    def getlist(self, obj=None):
        """
        Returns a list of data-objects of a shotfile
        """
        if obj is None:
            obj = 'SIGNALS'
        else:
            obj = str_byt.to_str(obj)
        sfo = self.sfh[obj]
        otyp = sfo.obj_type
        dfmt = sfo.data_format
        if otyp != 2:
            return None
        buf = self.getchunk(sfo.address, sfo.length)
        sfmt = sfdics.fmt2struc[dfmt]
        list_ids = unpack('>%d%s' %(sfo.items, sfmt), buf)

        return [self.getobjname(jid) for jid in list_ids]


    def getlist_by_type(self, obj_type=7):

        return [lbl for lbl in self.sfh['obj_nam'] if self.sfh[lbl].obj_type == obj_type]


    def getobjname(self, jobj):
        """
        Returns the object name for an inpur object ID
        """

        return self.sfh['obj_nam'][jobj]


    def getobjid(self, lbl):
        """
        Returns the object ID for a given objeect
        """

        lbl = str_byt.to_str(lbl)
        return self.sfh['obj_id'][lbl]


    def getrelnames(self, lbl):
        """
        Returns the relation names of a given object
        """

        lbl = str_byt.to_str(lbl)
        rels_id = self.sfh[lbl].rel
        return [self.getobjname(jobj) for jobj in rels_id if jobj < 65535]


    def getdevice(self, lbl):
        """
        Returns a DEVICE object
        """

        return self.getparset(lbl)


    def getts06(self):
        """
        Reads the diagnostic internal TS06 from parameter set
        """
        ts6 = 0
        for obj in self.parsets:
            if self.sfh[obj].obj_type == 3:
                ps = self.getparset(obj)
                if 'TS06' in ps.keys():
                    ts6 = ps['TS06']
                    break

        if ts6 == 0:
            ts6 = getcti_ts06(self.shot)

        return ts6


    def time_first(self, obj):
        """
        Tells whether a SigGroup has time as first coordinate
        by comparing with the size of the related TBase
        """

        obj = str_byt.to_str(obj)
        sfo = self.sfh[obj]
        otyp = sfo.obj_type
        if otyp != 6:
            return False # Objects other than sig, sgr, tbase

        rels = self.getrelnames(obj)
        for rel in rels:
            if self.sfh[rel].obj_type == 8:
                shape_arr = np.array(sfo.index[::-1][:sfo.num_dims])
                nt = self.sfh[rel].n_steps
                if shape_arr[0] != nt:
                    return False
                for jdim in range(1, sfo.num_dims):
                    if shape_arr[jdim] == nt:
                        return False # Two dimension are
                return True # No other dim's size matches by chance


    def time_last(self, obj):
        """
        Tells whether a SigGroup has time as first coordinate
        by comparing with the size of the related TBase
        """

        obj = str_byt.to_str(obj)
        sfo = self.sfh[obj]
        otyp = sfo.obj_type
        if otyp != 6:
            return False # Objects other than sig, sgr, tbase

        rels = self.getrelnames(obj)
        for rel in rels:
            if self.sfh[rel].obj_type == 8:
                shape_arr = np.array(sfo.index[::-1][:sfo.num_dims])
                nt = self.sfh[rel].n_steps
                if shape_arr[-1] != nt:
                    return False
                for jdim in range(sfo.num_dims-1):
                    if shape_arr[jdim] == nt:
                        return False # Two dimension are
                return True # No other dim's size matches by chance
