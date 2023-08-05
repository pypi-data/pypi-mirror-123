"""
COCOS utilities
See https://crppwww.epfl.ch/~sauter/cocos/Sauter_COCOS_Tokamak_Coordinate_Conventions.pdf
Especially Table I page 8
"""

import logging
import numpy as np

log = logging.getLogger()

# Table I page 8

sigma = { \
    'bp'       : [ 1,  1, -1, -1,  1,  1, -1, -1], \
    'rphiz'    : [ 1, -1,  1, -1,  1, -1,  1, -1], \
    'rhothephi': [ 1,  1, -1, -1, -1, -1,  1,  1]}

explain = {'rphiz'    : {1: '(R, phi, Z) r'    , -1: '(R, Z, phi) l'}, \
           'rhothephi': {1: '(rho, the, phi) r', -1: '(rho, phi, the) l'    } }

for key, val in sigma.items():
    sigma[key] = np.array(val)


def check_coco(equ_in, ip_shot='ccw', bt_shot='cw'):
    """
    Routine to assess the COCO of a given equilibrium object

    Input
    --------
    equ_in: equilibrium object
        Tokamak equilibrium

    Output
    --------
    ncoco: int
        COCO number
    """

# dpsi_sign positive if psi_sep > psi0
    dpsi_sign = np.sign(np.mean(equ_in.psix) - np.mean(equ_in.psi0))
# Known plasma discharge
    ccw_ip = 1 if(ip_shot == 'ccw') else -1 # AUG default: 1
    ccw_bt = 1 if(bt_shot == 'ccw') else -1 # AUG default: -1

# Table III

    sign_q  = np.sign(np.nanmean(equ_in.q))
    sign_ip = np.sign(np.nanmean(equ_in.ipipsi))
    sign_bt = np.sign(np.nanmean(equ_in.jpol))
    sigma_rphiz = sign_ip*ccw_ip
    sigma_bp    = dpsi_sign*sign_ip
# Eq 45
    sigma_rhothephi = sign_q*sign_ip*sign_bt
    log.debug(sigma_bp, sigma_rphiz, sigma_rhothephi)
    for jc, rhothephi in enumerate(sigma['rhothephi']):
        if(sigma['bp'   ][jc] == sigma_bp    and \
           sigma['rphiz'][jc] == sigma_rphiz and \
           rhothephi          == sigma_rhothephi):
            ncoco = jc + 1
            break

# Find out 2*pi factor for Psi

    dphi = np.gradient(equ_in.tfl, axis=1)
    dpsi = np.gradient(equ_in.pfl, axis=1)

# Radial+time average
# It is either q_ratio ~ 1 (COCO > 10) or ~ 2*pi (COCO < 10)
    q_ratio = np.abs(np.nanmean(dphi/(equ_in.q*dpsi)))
    log.debug('Ratio %8.4f' %q_ratio)
    if q_ratio < 4:
        ncoco += 10

    return ncoco


class EQUIL:
    pass

def coco2coco(equ_in, cocos_out=11):
    """
    Routine to transform an equilibrium object to any wished output COCO

    Input
    --------
    equ_in: equilibrium object
        Tokamak equilibrium
    cocos_out: int
        Wished COC for output equilibrium

    Output
    --------
    equ_out: equilibrium object
        Tokamak equilibrium with COCO=cocos_out
    """

# Assuming SI for both equ_in and equ_out

    cocos_in = equ_in.cocos
    log.info('COCOS conversion from %d to %d' %(cocos_in, cocos_out))
    jc_in   = cocos_in %10 - 1
    jc_out  = cocos_out%10 - 1
    ebp_in  = cocos_in//10
    ebp_out = cocos_out//10
#    sign_ip_in = np.sign(np.nanmean(equ_in.ipipsi))
# Equation 9, table I, equation 39, 45
    q_sign   = sigma['rhothephi'][jc_in]*sigma['rhothephi'][jc_out]
    phi_sign = sigma['rphiz'][jc_in]*sigma['rphiz'][jc_out]
    psi_sign = sigma['rphiz'][jc_in]*sigma['bp'][jc_in] * sigma['rphiz'][jc_out]*sigma['bp'][jc_out]
    psi_2pi  = (2.*np.pi)**(ebp_out - ebp_in)
    psi_fac = psi_sign*psi_2pi
    try:
        log.debug(np.mean(equ_in.jav), phi_sign)
    except:
        pass
    equ_out = EQUIL()
    for key, val in equ_in.__dict__.items():
        if val is None:
            continue
        if key in ('B0', 'jpol', 'jav', 'tfl', 'ip', 'ipipsi'):
            equ_out.__dict__[key] = phi_sign*val
        elif key in ('psi0', 'psix', 'pfl', 'pfm'):
            equ_out.__dict__[key] = psi_fac*val
        elif key in ('dpres', 'darea', 'dvol', 'ffp'):
            equ_out.__dict__[key] = val/psi_fac
        elif key in ('djpol', ):
            equ_out.__dict__[key] = val/psi_fac * phi_sign
        elif key in ('q', 'q0', 'q25', 'q50', 'q75', 'q95'):
            equ_out.__dict__[key] = q_sign*val
        else:
            equ_out.__dict__[key] = val
    equ_out.cocos = cocos_out

    return equ_out


if __name__ == '__main__':

    import sys, time
    sys.path.append('/afs/ipp-garching.mpg.de/aug/ads-diags/common/python/lib')
    from sf2equ_20200525 import EQU
    import mapeq_20200507 as meq

    shot = 28053
    t1 = time.time()
    eq_in = EQU(shot)
    t2 = time.time()
    eq_out = coco2coco(eq_in, cocos_out=12)
    t3 = time.time()
    log.info('Time for reading EQU', t2 - t1)
    log.info('Time for COCOs conversion', t3 - t2)
    ncoco_in  = check_coco(eq_in )
    ncoco_out = check_coco(eq_out)
    log.info('AUG equ_in  has COCO %d' %ncoco_in )
    log.info('AUG equ_out has COCO %d' %ncoco_out)

    br_in , bz_in , bt_in  = meq.Bmesh(eq_in)
    br_out, bz_out, bt_out = meq.Bmesh(eq_out)
    nt, nR, nZ = br_in.shape
    log.info(nt, nR, nZ)
    jt = nt//2
    jR = nR//2
    jZ = nZ//2
    log.info(eq_in.cocos)
    log.info(eq_in.pfl[jt])
    log.info(eq_in.q[jt])
    log.info(eq_out.cocos)
    log.info(eq_out.pfl[jt])
    log.info(eq_out.q[jt])

# Plot B components

    plot = False

    if plot:

        import matplotlib.pylab as plt

# EQUin

        X, Y = np.meshgrid(eq_in.Rmesh, eq_in.Zmesh)
        br = br_in[jt]
        bz = bz_in[jt]
        bt = bt_in[jt]
        b_p = np.hypot(br, bz)

        n_levels = 21

        plt.figure(eq_in.cocos, (9, 7))
        plt.subplot(2, 2, 1, aspect='equal')
        plt.title('BR')
        plt.xlabel('R [cm]')
        plt.ylabel('z [cm]')
        levels = np.linspace(np.min(br), np.max(br), n_levels)
        plt.contourf(X, Y, br.T, levels)
        plt.colorbar()

        plt.subplot(2, 2, 2, aspect='equal')
        plt.title('Bz')
        plt.xlabel('R [cm]')
        plt.ylabel('z [cm]')
        levels = np.linspace(np.min(bz), np.max(bz), n_levels)
        plt.contourf(X, Y, bz.T, levels)
        plt.colorbar()

        plt.subplot(2, 2, 3, aspect='equal')
        plt.title('Bpol')
        plt.xlabel('R [cm]')
        plt.ylabel('z [cm]')
        levels = np.linspace(np.min(b_p), np.max(b_p), n_levels)
        plt.contourf(X, Y, b_p.T, levels)
        plt.colorbar()

        plt.subplot(2, 2, 4, aspect='equal')
        plt.title('Btor')
        plt.xlabel('R [cm]')
        plt.ylabel('z [cm]')
        levels = np.linspace(np.min(bt), np.max(bt), n_levels)
        plt.contourf(X, Y, bt.T, levels)
        plt.colorbar()

# EQUout

        X, Y = np.meshgrid(eq_out.Rmesh, eq_out.Zmesh)
        br = br_out[jt]
        bz = bz_out[jt]
        bt = bt_out[jt]
        b_p = np.hypot(br, bz)

        n_levels = 21

        plt.figure(eq_out.cocos, (9, 7))
        plt.subplot(2, 2, 1, aspect='equal')
        plt.title('BR')
        plt.xlabel('R [cm]')
        plt.ylabel('z [cm]')
        levels = np.linspace(np.min(br), np.max(br), n_levels)
        plt.contourf(X, Y, br.T, levels)
        plt.colorbar()

        plt.subplot(2, 2, 2, aspect='equal')
        plt.title('Bz')
        plt.xlabel('R [cm]')
        plt.ylabel('z [cm]')
        levels = np.linspace(np.min(bz), np.max(bz), n_levels)
        plt.contourf(X, Y, bz.T, levels)
        plt.colorbar()

        plt.subplot(2, 2, 3, aspect='equal')
        plt.title('Bpol')
        plt.xlabel('R [cm]')
        plt.ylabel('z [cm]')
        levels = np.linspace(np.min(b_p), np.max(b_p), n_levels)
        plt.contourf(X, Y, b_p.T, levels)
        plt.colorbar()

        plt.subplot(2, 2, 4, aspect='equal')
        plt.title('Btor')
        plt.xlabel('R [cm]')
        plt.ylabel('z [cm]')
        levels = np.linspace(np.min(bt), np.max(bt), n_levels)
        plt.contourf(X, Y, bt.T, levels)
        plt.colorbar()

        plt.show()
