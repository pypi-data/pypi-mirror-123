import os, datetime, warnings, logging
import ctypes as ct
import numpy as np
from . import sfdics, str_byt

logger = logging.getLogger('aug_sfutils.ww')

wwlib = '/afs/ipp-garching.mpg.de/aug/ads/lib64/@sys/libddww8.so.8.1'
if not os.path.isfile(wwlib):
    wwlib = '/afs/ipp-garching.mpg.de/aug/ads/lib64/amd64_sles11/libddww8.so.8.1'
libddww = ct.cdll.LoadLibrary(wwlib)

def getError(error):

    """ Check if an error/warning occured. """
    try:
        err = ct.c_int32(error)
    except TypeError:
        err = ct.c_int32(error.value)
    isError = libddww.xxsev_(ct.byref(err))==1
    isWarning = libddww.xxwarn_(ct.byref(err))==1
    if isError or isWarning:
        id = ct.c_char_p(b'')
        lid = ct.c_uint64(0)
        text = ct.c_char_p(b' '*255)
        ltext = ct.c_uint64(255)
        unit = ct.byref(ct.c_int32(-1))
        ctrl = ct.byref(ct.c_uint32(3))
        libddww.xxerrprt_(unit, text, ct.byref(err), ctrl, id, ltext, lid);
        if isError:
            raise Exception(text.value.strip())
        else:
            warnings.warn(text.value.strip(), RuntimeWarning)


class WW:


    def Open(self, exp, diag, nshot, edition=-1, mode='new'):

        self.Close()
        if nshot > 0:
            date = datetime.date.strftime(datetime.datetime.today(),'%y.%m.%d;%H:%M:%S')

            exp  = str_byt.to_byt(exp)
            diag = str_byt.to_byt(diag)
            mode = str_byt.to_byt(mode)
            date = str_byt.to_byt(date)

            self.edition = ct.c_int32(edition)
            error        = ct.c_int(0)
            diaref       = ct.c_int32(0)
            shot         = ct.c_uint32(nshot)
            cexp         = ct.c_char_p(exp )
            cdiag        = ct.c_char_p(diag)
            cmode        = ct.c_char_p(mode)
            cdate        = ct.c_char_p(date)
            _error       = ct.byref(error)
            _nshot       = ct.byref(shot)
            _edition     = ct.byref(self.edition)
            self._diaref = ct.byref(diaref)
            lexpr = ct.c_uint64(len(exp ))
            ldiag = ct.c_uint64(len(diag))
            lmode = ct.c_uint64(len(mode))
            ldate = ct.c_uint64(len(date))

            result = libddww.wwopen_(_error, cexp, cdiag, _nshot, cmode, _edition, \
                                     self._diaref, cdate, lexpr, ldiag, lmode, ldate)
            if getError( error ):
                del self._diaref
                del self.edition
                raise Exception('ww: Error Opening Shotfile %(error)s' % {'error':error.value})
        return hasattr(self, '_diaref')


    def Close(self):

        if hasattr(self, '_diaref'):
            error = ct.c_int32(0)
            disp  = b'lock'
            space = b'maxspace'
            ldisp  = ct.c_uint64(len(disp))
            lspace = ct.c_uint64(len(space))
            _error = ct.byref(error)
            _disp  = ct.c_char_p( disp )
            _space = ct.c_char_p( space )

            result = libddww.wwclose_(_error , self._diaref , _disp , _space , ldisp , lspace )
            logger.info('Close: ', result, error.value, ' Edition', self.edition.value)
            if getError( error ):
                raise Exception('ww: Error Closing Shotfile')
            del self._diaref
            del self.edition


    def _wwoinfo(self, signame):
        if hasattr(self, '_diaref'):
            signame = str_byt.to_byt(signame)

            error   = ct.c_int32(0)
            name    = ct.c_char_p(signame)
            lname   = ct.c_uint64(len(signame))
            typ     = ct.c_uint32(0)
            format  = ct.c_uint16(0)
            ntval   = ct.c_uint32(0)
            items   = ct.c_uint32(0)
            _items  = ct.byref(items)
            c_indices = (ct.c_uint32 * 4)()
            _error   = ct.byref(error)
            _typ     = ct.byref(typ)
            _ntval   = ct.byref(ntval)
            _format  = ct.byref(format)
            _indices = ct.byref(c_indices)

            result = libddww.wwoinfo_(_error, self._diaref, name, _typ, \
                     _format, _ntval, _items, _indices, lname)

            if getError(error):
                lbl = sfdics.obj_name[typ.value]
                raise Exception('ww: Error wwoinfo %s' %(lbl, signame) )

            return {'otype': typ.value, 'format': format.value, 'leng': ntval.value, \
                    'items': items.value, 'indices': c_indices}


    def GetParameterInfo(self, pset, pnam):
        """ Returns information about the parameter 'pnam' of the parameter set 'pset'."""

        if hasattr(self, '_diaref'):
            par_name = str_byt.to_byt(pnam)
            set_name = str_byt.to_byt(pset)
            error   = ct.c_int32(0)
            _error  = ct.byref(error)
            pset    = ct.c_char_p(set_name)
            par     = ct.c_char_p(par_name)
            items   = ct.c_uint32(0)
            _items  = ct.byref(items)
            format  = ct.c_uint16(0)
            _format = ct.byref(format)
            lpar = ct.c_uint64(len(par_name))
            lset = ct.c_uint64(len(set_name))
            result = libddww.dd_prinfo_(_error, self._diaref, pset, par, _items, _format, lset, lpar)
            return {'items': items.value, 'format': format.value}


    def SetObject(self, signame, data):
        logger.info('Setting %s' %(signame))
        if hasattr(self, '_diaref'):
            info  = self._wwoinfo(signame)
            otype = info['otype']
            if otype in (7, 8):
                self.SetSignal(signame, data)
            elif otype == 6:
                self.SetSignalGroup(signame, data)
            elif otype == 13:
                self.SetAreabase(signame, data)


    def SetSignal(self, signame, data, indices=None):
        if hasattr(self, '_diaref'):
            info  = self._wwoinfo(signame)
            dtype = sfdics.fmt2typ[info['format']]
            otype = info['otype']
            ctyp  = sfdics.typ2ct[dtype]
            if dtype == 6:
                lbuf = sfdics.fmt2len[info['format']]
                lsbuf = ct.c_uint64(lbuf)
            else:
                lbuf = np.size(data)

            signame = str_byt.to_byt(signame)
            lbl = sfdics.obj_name[otype]

            error   = ct.c_int32(0)
            name    = ct.c_char_p(signame )
            lname   = ct.c_uint64(len(signame))
            clbuf   = ct.c_uint32(lbuf)
            stride  = ct.c_uint32(1)
            _error  = ct.byref(error)
            _type   = ct.byref(ct.c_uint32(dtype))
            _lbuf   = ct.byref(clbuf)
            _stride = ct.byref(stride)
            if indices is not None:
                _indices = np.array(indices, dtype=np.int32).ctypes.data_as(ct.POINTER(ct.c_uint32))

            if dtype == 6:
                slen = sfdics.fmt2len[info['format']]
#                stride  = ct.c_uint32(slen)
                stride  = ct.c_uint32(1)
                _stride = ct.byref(stride)
                if type(data) == type('str'):
                    sbuf = data.ljust(slen)
                else: #string array
                    sbuf = ''
                    for entry in data:
                        sbuf += entry.ljust(slen)

                sbuf = str_byt.to_byt(sbuf)
                lbuf = ct.c_uint32(len(sbuf))
                _lbuf = ct.byref(lbuf)
                lsbuf = ct.c_uint64(len(sbuf)) 
                buffer = ct.c_char_p(sbuf)
                if otype == 7:   # Signal
                    result = libddww.wwsignal_( \
                             _error, self._diaref, name, _type, _lbuf, buffer, \
                             _stride, lname, lsbuf)
                elif otype == 6: # Signalgroup
                    result = libddww.wwinsert_( \
                             _error, self._diaref, name, _type, _lbuf, buffer, \
                             _stride, _indices, lname, lsbuf)
            else:
                data = np.atleast_1d(data)
                data = np.array(data, dtype=sfdics.fmt2np[info['format']])
                if otype == 7:   # Signal
                    result = libddww.wwsignal_( \
                             _error, self._diaref, name, _type, _lbuf, \
                             data.ctypes.data_as(ct.POINTER(ctyp)), \
                             _stride, lname)
                elif otype == 8: # Timebase
                    result = libddww.wwtbase_( \
                             _error, self._diaref, name, _type, _lbuf, \
                             data.ctypes.data_as(ct.POINTER(ctyp)), \
                             _stride, lname)
                elif otype == 6: #Signalgroup
                    result = libddww.wwinsert_( \
                             _error, self._diaref, name, _type, _lbuf, \
                             data.ctypes.data_as(ct.POINTER(ctyp)), \
                             _stride, _indices, lname)

            if otype in (7, 8):
                sign = signame.decode('utf8')
                if getError( error ):
                    raise Exception('ww: Error Writing %s %s' %(lbl, sign) )
                else:
                    logger.info('Written %s %s' %(lbl, sign))


    def SetSignalGroup(self, signame, data):

        info  = self._wwoinfo(signame)
        dtype = sfdics.fmt2typ[info['format']]
        if dtype == 6:
            for i, dat in enumerate(data):
                dat = dat.ljust(info['leng'])
                indices = [i + 1, 1, 1]
                self.SetSignal(signame, dat, indices=indices)
        else:
            if data.ndim < 2:
                raise Exception('ww: SetSignalGroup array %s has only %d dims' %(signame, data.ndim))
                return False
            if data.ndim == 2:
                for i in range(data.shape[1]):
                    indices = [i + 1, 1, 1]
                    self.SetSignal(signame, data[:, i], indices=indices)
            if data.ndim == 3:
                for i in range(data.shape[1]):
                    for j in range(data.shape[2]):
                        indices = [1 + i, 1 + j, 1]
                        self.SetSignal(signame, data[:, i, j], indices=indices)
        logger.info('Written Signal Group %s' %signame)

        return True


    def SetAreabase(self, areaname, data):

        if hasattr(self, '_diaref'):
            info  = self._wwoinfo(areaname)
            dtype = sfdics.fmt2typ[info['format']]
            ctyp  = sfdics.typ2ct[dtype]

            data = np.array(data, dtype=sfdics.fmt2np[info['format']])
            areaname = str_byt.to_byt(areaname)     
            sizes = (ct.c_uint32 * 3)()
            for jsiz in range(data.ndim):
                sizes[jsiz] = data.shape[jsiz]
            if data.ndim > 1:
                nt = data.shape[0]
                if nt > 1:
                    sizes[0] = sizes[1]
                    sizes[1] = sizes[2]
            else:
                nt = 1
            logger.debug(areaname, dtype, nt, data.shape, sizes[0:3])
            error  = ct.c_int32(0)
            name   = ct.c_char_p(areaname)
            lname  = ct.c_uint64(len(areaname))
            k1     = ct.c_long(1)
            k2     = ct.c_long(nt)
            _k1    = ct.byref(k1)
            _k2    = ct.byref(k2)
            _type  = ct.byref(ct.c_uint32(dtype))
            _error = ct.byref(error)
            _sizes = ct.byref(sizes)

            libddww.wwainsert_(_error, self._diaref, name, _k1, _k2, _type, \
                               data.ctypes.data_as(ct.POINTER(ctyp)), \
                               _sizes, lname)

            if getError(error):
                raise Exception('ww.shotfile.SetAreabase: Error writing areabase %s' %areaname)
            else:
                logger.info('Written Areabase %s' %areaname, sizes[0:3])


    def SetParameter(self, set_name, par_name, data):

        """ ww.shotfile.SetParameter( SetName , ParameterName , data )\n
        types: 0 = raw 1 = integer 2 = float 3 = double 4 = complex 5 = logical 6 = character
        """
        if hasattr(self, '_diaref'):
            info = self.GetParameterInfo(set_name, par_name)
            dattype = sfdics.fmt2typ[info['format']]
            ctyp  = sfdics.typ2ct[dattype]
            set_name = str_byt.to_byt(set_name)
            par_name = str_byt.to_byt(par_name)
            logger.info('PN %s' %par_name)
            data = np.atleast_1d(data)
            logger.debug('Data', data, dattype )
            ndata = len(data)
            nitem = info['items']
            if ndata > nitem:
                logger.error('Too many %d entries for par_nam %s, more than in sfh %d' %(ndata, par_name, nitem))
                return
            if ndata == 0:
                logger.error('No data for par_nam %s' %par_name)
                return
            if ndata < nitem:
                data = np.zeros(nitem, dtype=sfdics.typ2np[dattype])
            error   = ct.c_int32(0)
            pset    = ct.c_char_p(set_name)
            par     = ct.c_char_p(par_name)
            lset    = ct.c_uint64(len(set_name))
            lpar    = ct.c_uint64(len(par_name))
            _type   = ct.byref(ct.c_uint32(dattype))
            _error  = ct.byref(error)
            if dattype == 6:
                slen = sfdics.fmt2len[info['format']]
                stride  = ct.c_uint32(1)
                _stride = ct.byref(stride)
                if type(data) == type('str'):
                    sbuf = data.ljust(slen)
                else: #string array
                    sbuf = ''
                    for entry in data:
                        sbuf += entry.ljust(slen)

                sbuf = str_byt.to_byt(sbuf)
                lbuf = ct.c_uint32(len(sbuf))
                _lbuf = ct.byref(lbuf)
                lsbuf = ct.c_uint64(len(sbuf)) 
                buffer = ct.c_char_p(sbuf)
                result = libddww.wwparm_(_error, self._diaref, pset, par, _type, _lbuf, \
                                         buffer, _stride, lset, lpar, lsbuf)
            else:
                datanp = np.array(data, dtype=sfdics.fmt2np[info['format']])
                if ndata < nitem:
                    datanp = np.append(datanp, np.zeros(nitem - ndata))
                stride  = ct.c_uint32(1)
                _stride = ct.byref(stride)
                lbuf = ct.c_uint32(nitem)
                _lbuf = ct.byref(lbuf)
                if nitem == 1 and dattype == 5:
                    buffer = ctyp(datanp)
                else:
                    buffer = ctyp.from_buffer(datanp)
                _buffer = ct.byref(buffer)
                result = libddww.wwparm_(_error, self._diaref, pset, par, _type, _lbuf, \
                                         _buffer, _stride, lset, lpar)
            if getError( error ):
                raise Exception('ww: Error Writing Parameters into %s -> %s' %(set_name.decode('utf-8'), par_name.decode('utf-8') ) )

            else:
                logger.info('   PN %s' %par_name.decode('utf8'))


def write_sf(nshot, data_d, sfhdir, diag, exp='AUGD'):

    import os

    ww = WW()

    os.chdir(sfhdir)
    logger.info(exp, diag, nshot)
    if not ww.Open(exp, diag, nshot):
        logger.error('Problems opening shotfile')
        return

    otype = {}
    for obj, data in data_d.items():
        logger.debug(obj)
        otype[obj] = ww._wwoinfo(obj)['otype']
        if otype[obj] == 8:
            ww.SetObject(obj, data)

    for obj, data in data_d.items():
        if otype[obj] == 13:
            ww.SetObject(obj, data)

    for obj, data in data_d.items():
        if otype[obj] == 4:
            logger.info('Writing PS %s' %obj)
            for pn, pdata in data.items():
                ww.SetParameter(obj, pn, pdata)
        if otype[obj] in (6, 7):
            ww.SetObject(obj, data)

    ww.Close()
