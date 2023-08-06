import os
import numpy as np
from matplotlib.path import Path
from scipy.io import netcdf
from scipy.interpolate import interp1d
import classes, units
import read_ascot, read_toric


class TRANSP:


    def __init__(self, fbm_file, cdf_file, R_cm, z_cm, verb=False, EcutL=0, EcutH=1e2):

        if verb:
            print('Distributions for %s' %fbm_file)

        if not os.path.isfile(fbm_file):
            if verb:
                print('NetCDF file %s not found' %fbm_file)
            return
        fv = netcdf.netcdf_file(fbm_file, 'r', mmap=False).variables

        spc_lbl = "".join(fv['SPECIES_1'].data)
        fbm  = 0.5*fv['F_%s' %spc_lbl].data
        E_eV = fv['E_%s' %spc_lbl].data
        mu   = fv['A_%s' %spc_lbl].data
        rhot_fbm = fv['X2D'].data

        cv = netcdf.netcdf_file(cdf_file, 'r', mmap=False).variables

        tfbm = fv['TIME'].data
        tim = cv['TIME3'].data
        jt = np.argmin(np.abs(tim - tfbm))

        rhot_cdf = cv['X'].data[jt, :]

        Rfbm = fv['R2D'].data
        zfbm = fv['Z2D'].data

# Separatrix
        Rfbm_sep = fv['RSURF'].data[-1, :]
        zfbm_sep = fv['ZSURF'].data[-1, :]
        my_poly = zip(*(Rfbm_sep, zfbm_sep))
        sep_path = Path(my_poly)
        inside_sep = sep_path.contains_points(zip(R_cm, z_cm))

        n_los = len(R_cm)
        self.idx = np.zeros(n_los, dtype=np.int32) - 1
        for jlos in range(n_los):
            if inside_sep[jlos]:
                d2 = (Rfbm - R_cm[jlos])**2 + (zfbm - z_cm[jlos])**2
                self.idx[jlos] = np.argmin(d2)

        E_MeV = 1e-6*E_eV
        EindL = (E_MeV <= EcutL)
        EindH = (E_MeV >= EcutH)
        if verb:
            print('Selecting %8.4f <= Energy/MeV <= %8.4f' %(EcutL, EcutH))

        fbm[:, :, EindL] = 0
        fbm[:, :, EindH] = 0

        self.fbmdata = {}
        self.n_fi = {}
        self.maxw_ti = {}
        n_rhot = len(rhot_fbm)
        Ti_fbm = interp1d(rhot_cdf, cv['TI'].data[jt, :])(rhot_fbm)*units.eV
        self.nd = interp1d(rhot_cdf, cv['ND'].data[jt, :])(rhot_fbm)/units.centimeters**3
        for jmc in range(n_rhot):
            fs = fbm[jmc, :, :].ravel()
            self.fbmdata[jmc] = classes.TabulatedDistribution(E_eV, mu, fs, units.eV)
            self.n_fi[jmc] = self.fbmdata[jmc].integral()/units.centimeters**3
            self.maxw_ti[jmc] = classes.Maxwellian(Ti_fbm[jmc])


class ASCOT:


    def __init__(self, asc_file, R_m, z_m, verb=False, EcutL=0, EcutH=1e2):

        if verb:
            print('Distributions for %s' %asc_file)

        if not os.path.isfile(asc_file):
            if verb:
                print('HDF5 file %s not found' %asc_file)
            return

        asc = read_ascot.ASCOT(asc_file)

        Rgrid_b = asc.grid['R_b']
        zgrid_b = asc.grid['z_b']

        E_J    = asc.grid['energy'] # J
        mu     = asc.grid['pitch']
        rhop_map = asc.rho_pol
        nR, nz = rhop_map.shape

# Distribution

        fbm_MeV = asc.fbm[0, 0, :, ::-1, :, :, 0]*1.602e-13 #energy, pitch, z, R [MeV] | cm**-3 s**-1

        E_MeV = E_J*6.242e+12
        EindL = np.where(E_MeV <= EcutL)[0]
        EindH = np.where(E_MeV >= EcutH)[0]
        if verb:
            print('Selecting %8.4f <= Energy/MeV <= %8.4f' %(EcutL, EcutH))

        fbm_MeV[EindL, :, :, :, ] = 0
        fbm_MeV[EindH, :, :, :, ] = 0

        Rmin = Rgrid_b[0]
        Rmax = Rgrid_b[-1]
        zmin = zgrid_b[0]
        zmax = zgrid_b[-1]
        print(Rmin, Rmax, zmin, zmax, nR, len(Rgrid_b))
        dR = (Rmax - Rmin)/float(nR)
        dz = (zmax - zmin)/float(nz)
        n_los = len(R_m)
        self.idxr = np.zeros(n_los, dtype=np.int32) - 1
        self.idxz = np.zeros(n_los, dtype=np.int32) - 1
        for jlos, Rloc in enumerate(R_m):
            if Rloc >= Rmin and Rloc <= Rmax:
                self.idxr[jlos] = int((Rloc - Rmin)/dR)
        for jlos, zloc in enumerate(z_m):
            if zloc >= zmin and zloc <= zmax:
                self.idxz[jlos] = int((zloc - zmin)/dz)

        self.fbmdata = {}
        self.n_fi = {}
        self.maxw_ti = {}
        self.nd = {}
        for jR in range(nR):
            self.fbmdata[jR] = {}
            self.n_fi[jR] = {}
            self.maxw_ti[jR] = {}
            self.nd[jR] = {}
            for jz in range(nz):
                rhop = rhop_map[jR, jz]
                if np.isnan(rhop) or (rhop > 1):
                    self.n_fi[jR][jz] = None
                else:
                    fs = fbm_MeV[:, :, jz, jR].T.ravel()
                    self.fbmdata[jR][jz] = classes.TabulatedDistribution(E_MeV, mu, fs, units.MeV)
                    self.n_fi[jR][jz] = self.fbmdata[jR][jz].integral()/units.centimeters**3
                    ti_cell = np.interp(rhop, asc.rho_p, asc.ti)*units.eV
                    self.nd[jR][jz] = np.interp(rhop, asc.rho_p, asc.nD)/units.centimeters**3
                    self.maxw_ti[jR][jz]  = classes.Maxwellian(ti_cell)


class TORIC:


    def __init__(self, fp_file, R_m, z_m, verb=False):


        nthe_eq = 41
        rfp = read_toric.READ_FP(fp_file)
        equ_file = '%seq.cdf' %fp_file[:-6]
        Rgl, zgl = read_toric.read_tc_eq(equ_file, rfp.rho_grid, nthe_eq=nthe_eq)

        Rgl_sep = Rgl[-1, :]
        zgl_sep = zgl[-1, :]
        my_poly = zip(*(Rgl_sep, zgl_sep))
        sep_path = Path(my_poly)
        inside_sep = sep_path.contains_points(zip(R_m, z_m))

        nrho, nthe_eq = Rgl.shape

        n_los = len(R_m)
        self.idrho = np.zeros(n_los, dtype=np.int32) - 1
        for jlos, Rloc in enumerate(R_m):
            zloc = z_m[jlos]
            if inside_sep[jlos]:
                d2 = (Rgl.ravel() - Rloc)**2 + (zgl.ravel() - zloc)**2
                self.idrho[jlos] = np.argmin(d2) % nthe_eq

        fbm = rfp.f_mu_E
        E   = rfp.Egrid # eV
        mu  = rfp.mu_grid
        rho = rfp.rho_grid

        if verb:
            print('fbm density = %12.4e' %np.max(rfp.nd))
        self.fbmdata = {}
        self.ni = rfp.nd/units.centimeters**3
        for jrho, rholoc in enumerate(rho):
            fs = fbm[jrho, :, :].ravel()
            self.fbmdata[jrho] = classes.TabulatedDistribution(E[:, jrho], mu, fs, units.eV)
