import os
import numpy as np
from scipy.io import netcdf
import datetime

lbl_d = {'bt' : 'Recoil light from beam-target neutrons, per unit time and bin-width', \
         'bb' : 'Recoil light from beam-beam neutrons, per unit time and bin-width', \
         'th' : 'Recoil light from thermonuclear neutrons, per unit time and bin-width', \
         'tot': 'Recoil light from neutrons, per unit time and bin-width'}

class HEPRO:


    def __init__(self, fin='/afs/ipp/home/n/nesp/tofana/responses/simresp.rsp'):

        f = open(fin, 'r')

        data = []
        for line in f.readlines():
            data += line.split()
        f.close()

        dsim = np.array(data, dtype = np.float32)
        n_dsim = len(dsim)
        print('%d' %n_dsim)
        ndim = []
        dE = []
        en1 = []
        en2 = []
        spc = []
        self.eka = dsim[0]
        j = 1
        while j < n_dsim:
            dE.append(dsim[j])
            nsize = dsim[j+1]
            ndim.append(nsize)
            en1.append(dsim[j+2])
            en2.append(dsim[j+3])
            j += 4
            spc.append(dsim[j:j+nsize])
            j += nsize
        self.dE   = np.array(dE, dtype=np.float32)
        self.en1  = np.array(en1, dtype=np.float32)
        self.en2  = np.array(en2, dtype=np.float32)
        self.ndim = np.array(ndim, dtype=np.int32)
        nEn = len(self.dE)
        nEp = np.max(self.ndim)
        self.spec = np.zeros((nEn, nEp), dtype=np.float32)
        for jEn, phs in enumerate(spc):
            nphs = len(phs)
            self.spec[jEn, :nphs] = phs[:nphs]


def NES2PHS(f_nes, f_rm='/afs/ipp/home/g/git/python/neutrons/tofana/rm_bg.cdf', w_cdf=False):

    print('Using response matrix %s' %f_rm)

    nes = netcdf.netcdf_file(f_nes, 'r', mmap=False).variables
    En_MeV = 1e-3*nes['E_NEUT'].data
    phs = {}
    reactions = []
    for key in nes.keys():
        if key in ('bt', 'bb', 'th', 'tot'):
            reactions.append(key)

    fname, ext = os.path.splitext(f_rm)
    if ext.lower() == '.cdf':
        rm  = netcdf.netcdf_file(f_rm, 'r', mmap=False).variables
        nbins = len(rm['E_light'].data)
        for react in reactions:
            phs[react] = np.zeros(nbins)
            for jEn, En in enumerate(En_MeV):
                dist = (rm['E_NEUT'].data - En)**2
                jclose = np.argmin(dist)
                phs[react] += nes[react][jEn]*rm['ResponseMatrix'][jclose, :]
    else:
        rsp = HEPRO(fin=f_rm)
        nbins = rsp.ndim[0]
        for react in reactions:
            phs[react] = np.zeros(nbins)
            for jEn, En in enumerate(En_MeV):
                dist = (rsp.dE - En)**2
                jclose = np.argmin(dist)
                phs[react] += nes[react][jEn]*rsp.spec[jclose]


    if w_cdf:

        f_phs = f_nes.replace('nes', 'phs')

        f = netcdf.netcdf_file(f_phs, 'w', mmap=False)

        f.history = 'Created %s\n' %datetime.datetime.today().strftime("%d/%m/%y")

        f.createDimension('Ep', nbins)
        Ep = f.createVariable('Ep', np.float32, ('Ep', ))
        Ep[:] = range(len(phs[react]))
        Ep.units = 'Ch' # keVee
        Ep.long_name = 'Detector channel' #'Equivalent photon energy'

        var = {}
        for key, val in phs.items():
            var[key] = f.createVariable(key, np.float32, ('Ep',))
            var[key].units = '1/(s)'  #'1/(s keVee)'
            var[key][:] = val
            var[key].long_name = lbl_d[key]

        f.close()
        print('Stored %s' %f_phs)

    print('Finished nes2phs', f_rm)
    return phs
