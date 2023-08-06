import logging, pickle, os, sys, datetime
sys.path.append(os.getenv('CONTROLROOM_LIBDIR'))
import numpy as np
from scipy.io import netcdf
import classes, units
import fi_codes

try:
    from mpi4py import MPI
    comm = MPI.COMM_WORLD
    n_threads = comm.size
    jrank = comm.rank
    mpi_flag = True
except:
    n_threads = 1
    jrank = 0
    mpi_flag = False

#name = MPI.Get_processor_name()

"""
The programs returns and plots the LOS integrated neutron spectrum
from d-d -> n-He3 reactions.
Usage:
module load anaconda/2
module load intel impi impi-interactive
module load mpi4py
mpirun -np 10 python los_nes.py
"""

__author__ = 'Giovanni Tardini (Tel. 1898)'
__version__ = '0.1'
__date__ = '04.10.2021'


classes.registerPythonUnitsClass(units.Units)
classes.registerPythonScalarClass(units.Scalar)
classes.registerPythonVectorClass(units.Vector)
classes.Files.dataDir = os.getenv('CONTROLROOM_DATADIR')

fmt = logging.Formatter('[%(asctime)s] %(levelname)s: %(message)s')
hnd = logging.StreamHandler()
hnd.setFormatter(fmt)
logging.root.addHandler(hnd)
logging.root.setLevel(logging.INFO)
log = logging.getLogger()

lbl_d = {'bt' : 'Beam-target neutrons per unit time and energy', \
         'bb' : 'Beam-beam neutrons per unit time and energy', \
         'th' : 'Thermonuclear neutrons per unit time and energy', \
         'tot': 'Neutrons per unit time and energy'}

crpy_dir = os.path.dirname(os.path.realpath(__file__))


def los_dd():

    f_dic = '%s/nes.pkl' %crpy_dir
    f = open(f_dic, 'rb')
    setup_d = pickle.load(f)
    f.close()

    code = setup_d['code']

    verb = False
    if jrank == 0:
        verb = True

    cdf_file = setup_d['cdf']
    los_file = setup_d['los']
    EcutL    = float(setup_d['EcutL'])
    EcutH    = float(setup_d['EcutH'])
    reac = setup_d['reac']
    code = setup_d['code']

    Emin  = float(setup_d['Emin'])
    Emax  = float(setup_d['Emax'])
    Ebins = int(setup_d['n_bin'])
    samples = int(setup_d['n_samp'])/n_threads

    Egrid_MeV = np.linspace(Emin, Emax, Ebins)
    dE = (Egrid_MeV[-1] - Egrid_MeV[0])/float(Ebins-1)

    if verb:
        log.info('\nStarting los_nes')
        print('# threads: %d' %n_threads)
        print('# samples per thread: %d' %samples)
        print('# MPI rank: %d' %jrank)
        log.info('Load LOS %s', los_file)
    try:
        x_m, y_m, z_m, omega, V_m3 = np.loadtxt(los_file, unpack=True)
    except IOError:
        raise
    omega = omega*units.steradians
    x, y, z = x_m*units.meters, y_m*units.meters, z_m*units.meters
    V = V_m3*units.meters**3
    R_m = np.hypot(x_m, y_m)
    R_cm = 100.*R_m
    z_cm = 100.*z_m

    with open(los_file) as f:
        head = [next(f) for jline in range(25)]
        for line in head:
            if 'Position' in line:
                strarr = line.split(':')[1]
                det_pos = [float(pos) for pos in strarr.split(',')]

    if verb:
        log.info('Fetching ion population from external codes')
# Interface to codes' output
    if code == 'tr':
        f_dist = setup_d['fbm']
        profile = fi_codes.TRANSP(f_dist, cdf_file, R_cm, z_cm, EcutL=EcutL, EcutH=EcutH, verb=verb)
    elif code == 'asc':
        f_dist = setup_d['asc']
        profile = fi_codes.ASCOT(f_dist, R_m, z_m, EcutL=EcutL, EcutH=EcutH, verb=verb)
    elif code == 'tc':
        f_dist = setup_d['fp']
        profile = fi_codes.TORIC(f_dist, R_m, z_m, verb=verb)
#        v_fluid = units.Vector(2e5, 0, 0)*units.meter/second
    v_fluid = units.Vector(0, 0, 0)*units.meters/units.second

    if verb:
        log.info('Setting cells')
        log.info('%8.4f %8.4f %8.4f', det_pos[0], det_pos[1], det_pos[2])
    cells = {}
    if code == 'tc':
        reactions = ('tot', )
    else:
        reactions = ('bt', 'th', 'bb')
    for react in reactions:
        cells[react] = []

    u1 = x_m - det_pos[0]
    v1 = y_m - det_pos[1]
    w1 = z_m - det_pos[2]
    for i in range(len(x_m)):
        posx = units.Vector.Cartesian(x[i], y[i], z[i])
        posv = -units.Vector.Cartesian(u1[i], v1[i], w1[i]).versor
        if code == 'tc':
            jrho = profile.idrho[i]
            if jrho >= 0:
                f1 = profile.fbmdata[jrho]
                n1 = profile.ni[jrho]
                cells['tot'].append( \
                    classes.Cell(f1=f1, f2=f1, n1=n1, n2=n1, \
                    position=posx, volume=V[i], \
                    solidAngle=omega[i], lineOfSight=posv, weight=1.0) )
        else:
            add_cell = False
            if code == 'tr':
                jfbm = profile.idx[i]
                if jfbm >= 0:
                    add_cell = True
                    f_fi  = profile.fbmdata[jfbm]
                    n_fi  = profile.n_fi[jfbm]
                    nd    = profile.nd[jfbm]
                    f_mxw = profile.maxw_ti[jfbm]
            elif code == 'asc':
                jR = profile.idxr[i]
                jz = profile.idxz[i]
                if jR >= 0 and jz >= 0:
                    if profile.n_fi[jR][jz] is not None:
                        add_cell = True
                        f_fi  = profile.fbmdata[jR][jz]
                        n_fi  = profile.n_fi[jR][jz]
                        nd    = profile.nd[jR][jz]
                        f_mxw = profile.maxw_ti[jR][jz]

            if add_cell:

                cells['bt'].append( \
                    classes.Cell(f1=f_fi, f2=f_mxw, n1=n_fi, n2=nd, \
                    position=posx, volume=V[i], \
                    solidAngle=omega[i], lineOfSight=posv, weight=1.0) )

                cells['th'].append( \
                    classes.Cell(f1=f_mxw, f2=f_mxw, n1=nd, n2=nd, \
                    position=posx, volume=V[i], \
                    solidAngle=omega[i], lineOfSight=posv, weight=1.0) )

                cells['bb'].append( \
                    classes.Cell(f1=f_fi, f2=f_fi, n1=n_fi, n2=n_fi, \
                    position=posx, volume=V[i], \
                    solidAngle=omega[i], lineOfSight=posv, weight=1.0) )

    if verb:
        log.info('Reaction %s' %reac)
    reaction = classes.DDN3HeReaction()
    whichProduct = 1 # 1 <-> Neutron
    classes.Kinematics.setMode(classes.RELATIVISTIC)

# Make the randomisation reproducible, but different for each thread
    rdm = np.random.RandomState(seed=156677)
    seed_arr = rdm.random_integers(0, 10000, size=n_threads)
    nseed = int(seed_arr[jrank])
#    print('Rank %d, random seed %d' %(jrank, nseed))
    classes.Randomizer.seed(nseed)

    Egrid = Egrid_MeV*units.MeV
    nes  = {}
    rate = {}
    tmp = np.zeros(Ebins)

    for react in reactions:
        if verb:
            log.info('Calculating %s' %react)
            print('# of valid %s-cells: %d' %(react, len(cells[react]) ))
# Reducing accuracy for beam-beam, thermonuclear
        if react in ('bb', 'th'):
            n_samp = samples/5
        else:
            n_samp = samples
        spc = classes.CalculateVolumeSpectrum( \
              reaction, whichProduct, cells[react], \
              Emin*units.MeV, Emax*units.MeV, Ebins, n_samp, \
              E1range = (0.0*units.MeV, 1.0*units.MeV), \
              E2range = (0.0*units.MeV, 1.0*units.MeV), \
              Bdirection = classes.Clockwise, \
              vCollective = v_fluid)

        spec = np.zeros(Ebins)
        for jE, En in enumerate(Egrid):
            spec[jE] = spc[En]*units.seconds
        spec /= dE

        if mpi_flag:
            comm.Reduce(spec, tmp, op=MPI.SUM)
            nes[react] = tmp/n_threads
        else:
            nes[react] = spec

    if code == 'tc':
        nes['tot'] *= 0.5
    else:
        nes['bb']  *= 0.5
        nes['th']  *= 0.5
    for react in reactions:
        rate[react] = dE*np.sum(nes[react])


    if jrank == 0:

        log.info('Finished los_nes calculation')
        rate_tot = 0
        for react in reactions:
            print('Rate for %s: %12.4e Hz' %(react, rate[react]) )
            rate_tot += rate[react]
        print('Total rate in LoS: %12.4e Hz' %rate_tot ) 

        Egrid_keV = np.array(Egrid/units.keV, dtype=np.float32)
        nE = len(Egrid_keV)

# NetCDF file output

        dir_out = ('%s/output/%s' %(crpy_dir, code))
        os.system('mkdir -p %s' %dir_out)
        ftmp  = os.path.basename(f_dist)
        fname, ext = os.path.splitext(ftmp)
        fcdf  = ftmp.replace(ext, '_nes_%s.cdf' %code)
        cdf_out = ('%s/%s' %(dir_out, fcdf))
        print(ext, code)
        print(fcdf)
        f = netcdf.netcdf_file(cdf_out, 'w', mmap=False)

        f.history = 'Created %s\n' %datetime.datetime.today().strftime("%d/%m/%y")
        f.history += 'Fast ion distribution function from file %s\n' %f_dist
        f.history += 'Cone-of-sight geometry from file %s' %setup_d['los']

        f.createDimension('E_NEUT', nE)
        En = f.createVariable('E_NEUT', np.float32, ('E_NEUT', ))
        En[:] = Egrid_keV
        En.units = 'keV'
        En.long_name = 'Neutron energy'

        var = {}
        for key, val in nes.items():
            var[key] = f.createVariable(key, np.float32, ('E_NEUT',))
            var[key].units = '1/(s keV)'
            var[key][:] = 1e-3*val
            var[key].long_name = lbl_d[key]

        f.close()
        print('Stored %s' %cdf_out)


if __name__ == '__main__':

    los_dd()
