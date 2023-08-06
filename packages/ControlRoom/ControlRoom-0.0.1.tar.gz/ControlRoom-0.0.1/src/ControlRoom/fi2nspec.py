#!/usr/bin/env python

import sys, os, pickle, logging

import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
try:
    from matplotlib.backends.backend_tkagg import NavigationToolbar2Tk as nt2tk
except:
    from matplotlib.backends.backend_tkagg import NavigationToolbar2TkAgg as nt2tk
from matplotlib.figure import Figure
import matplotlib.pylab as plt
try:
    import Tkinter as tk
    import ttk
    import tkFileDialog as tkfd
    import tkMessageBox as tkmb
except:
    import tkinter as tk
    from tkinter import ttk
    from tkinter import filedialog as tkfd
    from tkinter import messagebox as tkmb

import tkhyper, read_equ, mom2rz, nes2phs, tot_nes, plot_aug
from scipy.io import netcdf

crwd = os.path.dirname(os.path.realpath(__file__))

fold = nes2phs.NES2PHS

titles = {'th':'Thermonuclear', 'bt':'Beam-target', 'bb':'Beam-beam', 'tot':'Total'}
sym_d = {'th':'r-', 'bt':'b-', 'bb':'g-', 'tot':'k-'}
reacts = ('bt', 'th', 'bb')

n_mpi = 10
mpi_root = os.getenv('I_MPI_ROOT')
if mpi_root is None or mpi_root.strip() == '':
    pre_comm = 'python'
    print('Running serial version')
else:
    pre_comm = 'mpirun -n %d python' %n_mpi
    print('Running parallel version')

crpy_dir = os.path.dirname(os.path.realpath(__file__))
out_dir = '%s/output' %crpy_dir

"""
The programs returns and plots the volume integrated neutron spectrum
from d-d -> n-He3 reactions
separating the thermonuclear, beam-target and beam-beam contributions
"""

__author__ = 'Giovanni Tardini (Tel. 1898)'
__version__ = '0.1'
__date__ = '27.02.2014'

home_dir = os.getenv('HOME')

fmt = logging.Formatter('[%(asctime)s] %(levelname)s: %(message)s')
hnd = logging.StreamHandler()
hnd.setFormatter(fmt)
logging.root.addHandler(hnd)
logging.root.setLevel(logging.INFO)
log = logging.getLogger()


def parse_los(f_los):

    pars_d = {}
    with open(f_los) as myfile:
        head = [next(myfile) for x in range(25)]
    for line in head:
        for lbl in ('nshot', 'time', 'y1', 'y2', 'z1', 'z2'):
            if lbl in line:
                tmp = line.split('=')
                pars_d[lbl] = float(tmp[1].split()[0])
        if 'Position' in line:
            strarr = line.split(':')[1]
            pars_d['xdet'], pars_d['ydet'], pars_d['zdet'] = [float(x) for x in strarr.split(',')]

    return pars_d


class FI2SPECTRUM:


    def __init__(self,  f_fbm=None, f_los=None, f_tor=None, f_asc=None):

        if f_fbm is not None:
            if os.path.isfile(f_fbm):
                self.fcdf = f_fbm.split('_fi_')[0] + '.CDF'
        if not hasattr(self, 'fcdf'):
            self.fcdf = ''

        os.system('mkdir -p %s' %out_dir)
# Widget frame

        nesframe = tk.Tk()
        nesframe.title('Neutron energy spectrum')
        nesframe.option_add("*Font", "Helvetica")

# Menu bar

        menubar = tk.Menu(nesframe)

        filemenu = tk.Menu(menubar, tearoff=0)
        filemenu.add_command(label="TRANSP LoS spectrum", command=self.fi2nes)
        filemenu.add_command(label="ASCOT LoS spectrum" , command=lambda: self.fi2nes(code='asc'))
        filemenu.add_command(label="TORIC LoS spectrum" , command=lambda: self.fi2nes(code='tc'))
        filemenu.add_separator()
        filemenu.add_command(label="TRANSP tot spectrum", command=self.tot_nes)
        filemenu.add_command(label="ASCOT tot spectrum" , command=lambda: self.tot_nes(code='asc'))
#        filemenu.add_command(label="TORIC tot spectrum" , command=self.tc_dd_he3n)
        filemenu.add_command(label="TORIC tot spectrum" , command=lambda: self.tot_nes(code='tc'))
        filemenu.add_separator()
        filemenu.add_command(label="Exit", command=sys.exit)

        loadmenu = tk.Menu(menubar, tearoff=0)
        loadmenu.add_command(label="TRANSP FBM..." , command=self.callfbm)
        loadmenu.add_command(label="ASCOT FBM..."  , command=self.callasc)
        loadmenu.add_command(label="TORIC FP..."   , command=self.callfp)
        loadmenu.add_command(label="Load LOS..."   , command=self.calllos)

        helpmenu = tk.Menu(menubar, tearoff=0)
        helpmenu.add_command(label="About", command=self.about)

        menubar.add_cascade(label="File", menu=filemenu)
        menubar.add_cascade(label="Load", menu=loadmenu)
        menubar.add_cascade(label="Help", menu=helpmenu)

        nesframe.config(menu = menubar)

# Figure frame

        nb_nes = ttk.Notebook(nesframe, name='notebook')
        nb_nes.pack(side=tk.TOP, fill=tk.BOTH, expand=1)
        fig_tab   = ttk.Frame(nb_nes, name='figures')
        input_tab = ttk.Frame(nb_nes, name='input')
        nb_nes.add(fig_tab, text='Figures')
        nb_nes.add(input_tab, text='Input Files')
        fig1frame = ttk.Frame(fig_tab)

        nesfig = Figure()
        nesfig.set_size_inches((7.4, 4.))
        canv_nes = FigureCanvasTkAgg(nesfig, master=fig1frame)
        nesfig.subplots_adjust(left=0.12, bottom=0.1, right=0.95, top=0.94)

# Initialise plots

        self.ax_nes = nesfig.add_subplot(1, 2, 1)
        self.nes_plot = {}
        for react in reacts + ('tot',):
            self.nes_plot[react], = self.ax_nes.plot([], [], sym_d[react], label=titles[react])
        self.line2452kev, = self.ax_nes.plot([], [], 'k-')
        self.ax_nes.set_xlim((2e3, 3e3))
        self.ax_nes.set_title('Energy spectrum along NE213 LOS')
        self.ax_nes.legend()

        self.ax_phs = nesfig.add_subplot(1, 2, 2)
        self.phs_plot = {}
        for react in reacts + ('tot',):
            self.phs_plot[react], = self.ax_phs.plot([], [], sym_d[react], label=titles[react])
        self.ax_phs.set_xlim((0, 300))
#        self.ax_phs.set_xlim((0, 4000))
        self.ax_phs.set_ylim((0, 1e7))
        self.ax_phs.legend()

        if f_fbm is None:
            self.ffbm = ''
        else:
            self.ffbm = f_fbm
        if f_asc is None:
            self.fasc = ''
        else:
            self.fasc = f_asc
        if f_los is None:
            self.flos = ''
        else:
            self.flos = f_los
        if f_tor is None:
            self.ffp = ''
        else:
            self.ffp = f_tor

        keys   = ['CDF file', 'FBM file', 'LOS file', 'TORIC file', 'ASCOT file']
        values = [self.fcdf, self.ffbm, self.flos, self.ffp, self.fasc]
        input_d = dict(zip(keys, values))
        self.ent_d = {}
        for key in keys:
            rowframe = ttk.Frame(input_tab)
            rowframe.pack(side=tk.TOP)
            ttk.Label(rowframe, text=key, width=14).pack(side=tk.LEFT)
            var = ttk.Entry(rowframe, width=74)
            var.insert(0, input_d[key])
            var.pack(side=tk.LEFT)
            self.ent_d[key] = var

# Get separatrix {R, z}

        time = 6.5 # still hardcoded
        eq = read_equ.READ_EQU(self.fcdf, tvec=time, rho=1)
        r_plot, z_plot = mom2rz.mom2rz(eq.rc, eq.rs, eq.zc, eq.zs)
        r_sepx = 0.01*r_plot[0]
        z_sepx = 0.01*z_plot[0]
        rmin = np.min(r_sepx)
        rmax = np.max(r_sepx)

# Plot LOS in poloidal section

        fig2frame = ttk.Frame(fig_tab)
        self.augfig = Figure()
        self.augfig.set_size_inches((4.8, 2.0))
        canv_los = FigureCanvasTkAgg(self.augfig, master=fig2frame)
        self.augfig.subplots_adjust(left=0.08, bottom=0.1, right=0.95, top=0.9)

        self.ax_pol = self.augfig.add_subplot(1, 2, 1, aspect='equal')
        self.ax_pol.set_xlim([ 0.5, 3])
        self.ax_pol.set_ylim([-1.5, 1.5])
        self.ax_pol.set_xlabel('R [cm]', labelpad=2)
        self.ax_pol.set_ylabel('z [cm]', labelpad=-14)
        self.pol_aug, = self.ax_pol.plot(r_sepx, z_sepx, '-', color='k', linewidth=0.5)
        self.pol_los, = self.ax_pol.plot([], [], 'r-')
        try:
            import aug_sfutils as sf
            gc_d = sf.getgc()
            for gc in gc_d.values():
                self.ax_pol.plot(gc.r, gc.z, 'b-')
        except:
            print('No coordinates of wall structures available for poloidal section drawing')

# Plot LOS in toroidal section
        ntheta = 101
        theta = np.linspace(0, 2*np.pi, ntheta)

        self.ax_tor = self.augfig.add_subplot(1, 2, 2, aspect='equal')
        self.ax_tor.set_xlim([-3, 4])
        self.ax_tor.set_ylim([-3, 3])
        self.ax_tor.set_xlabel('x [cm]', labelpad=2)
        self.ax_tor.set_ylabel('y [cm]', labelpad=-14)
        self.ax_tor.tick_params(which='major', length=4, width=0.5)
        self.tor_rmin, = self.ax_tor.plot(rmin*np.cos(theta), rmin*np.sin(theta), 'k-')
        self.tor_rmax, = self.ax_tor.plot(rmax*np.cos(theta), rmax*np.sin(theta), 'k-')
        self.tor_los, = self.ax_tor.plot([], [], 'r-')
        self.ax_tor.plot(0, 0, 'go')
        try:
            tor_d = plot_aug.STRUCT(f_in='/afs/ipp/home/g/git/python/aug/tor.data').tor_old
            for key, tor_pl in tor_d.items():
                self.ax_tor.plot(tor_pl.x, tor_pl.y, 'b-')        
        except:
            print('No coordinates of wall structures available for toroidal section drawing')

# Energy entries

        entframe = tk.Frame(nesframe, height=35)
        en_init = {'Emin':1.7, 'Emax':3.7, '#Ebins':301, '#MC samples':int(1e6), 'EcutL':0, 'EcutH':1e3}
        self.en_d = {}
        n_col=0
        for key in ('Emin', 'Emax', '#Ebins', '#MC samples', 'EcutL', 'EcutH'):
            lbl = tk.Label(entframe, text=key, width=len(key))
            wid = 7
            if key == '#MC samples':
                wid = 11
            var = tk.Entry(entframe, width=wid)
            var.insert(0, en_init[key])
            lbl.pack(side=tk.LEFT)
            var.pack(side=tk.LEFT)
            self.en_d[key] = var

        reac_lbl = tk.StringVar()
        reac_lbl.set('D-D')
        menub = tk.Menubutton(entframe, text='Reaction')
        menub.pack(side=tk.LEFT)
        mb = tk.Menu(menub)
        for reac in ('D-D', 'D-T'):
            mb.add_radiobutton(label=reac, variable=reac_lbl, value=reac)
        menub.config(menu=mb)
        self.en_d['reac'] = reac_lbl

        canv_nes._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=1)
        canv_los._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=1)
        fig1frame.pack(side=tk.TOP, fill=tk.BOTH, expand=1)
        entframe.pack( side=tk.TOP, fill=tk.BOTH, expand=1)
        fig2frame.pack(side=tk.TOP, fill=tk.BOTH, expand=1)

        self.los_draw()

# Navigation toolbar

        toolbar = nt2tk(canv_nes, fig1frame)
        toolbar.update()

        nesframe.mainloop()


    def los_draw(self):

        parse_d = parse_los(self.flos)
        Rpol = [parse_d['y1'], parse_d['y2']]
        zpol = [parse_d['z1'], parse_d['z2']]
        print(Rpol)
        self.pol_los.set_data(Rpol, zpol)

        ydet = float(parse_d['xdet'])
        print('Tan. radius %8.4f' %ydet)
        ytor = [ydet, ydet]
        xtor = [0, -parse_d['ydet']]
        self.tor_los.set_data(xtor, ytor)
        self.augfig.canvas.draw()


    def wsetup(self):

        spc_d = {}
        spc_d['Emin'] = float(self.en_d['Emin'].get())
        spc_d['Emax'] = float(self.en_d['Emax'].get())
        spc_d['n_bin']  = int(self.en_d['#Ebins'].get())
        spc_d['n_samp'] = int(self.en_d['#MC samples'].get())
        spc_d['EcutL'] = float(self.en_d['EcutL'].get())
        spc_d['EcutH'] = float(self.en_d['EcutH'].get())
        spc_d['reac'] = self.en_d['reac'].get().strip()
        spc_d['code'] = self.code

        spc_d['cdf'] = self.fcdf
        spc_d['fbm'] = self.ffbm
        spc_d['asc'] = self.fasc
        spc_d['los'] = self.flos
        spc_d['fp']  = self.ffp

        dout = '%s/nes.pkl' %crwd
        log.info('Writing setup dictionary in %s' %dout)
        f = open(dout, 'wb')
        pickle.dump(spc_d, f)
        f.close()
        return spc_d


    def fi2nes(self, code='tr'):

        import subprocess
# Dump setup dictionary
        self.code = code
        set_d = self.wsetup()

        log.info('Running LOS calculation')
      
        command = '%s %s/los_nes.py' %(pre_comm, crwd)
        err = os.system(command)

        
# Fold NES into PHS

        if err != 0:
            print('%s not executed' %command)
            return
        else:
            if code == 'tr':
                dir_spl = self.ffbm.split('/')
                ftmp1 = dir_spl[-1]
                ftmp = ftmp1.replace('.cdf', '_nes_%s.dat' %code)
            elif code == 'tc':
                ftmp1 = self.ffp.split('/')[-1]
                ftmp = ftmp1.replace('.cdf', '_nes_%s.dat' %code)
            elif code == 'asc':
                dir_spl = self.fasc.split('/')
                ftmp1 = dir_spl[-1]
                ftmp = ftmp1.replace('.h5', '_nes_%s.dat' %code)

            f_spc = ('%s/%s/%s' %(out_dir, code, ftmp))
            f_nes = f_spc.replace('.dat', '.cdf')
            f_phs = f_spc.replace('nes', 'phs')

            print('Folding spectrum from file %s' %f_nes)

#            f_rm = '/afs/ipp/home/n/nesp/tofana/responses/simresp_aug.rsp_broad'
            f_rm = '/afs/ipp/home/g/git/python/neutrons/tofana/sim_aug_gb.cdf'
            phs = fold(f_nes, f_rm=f_rm, w_cdf=True)

# Plot NES, PHS

            nes = netcdf.netcdf_file(f_nes, 'r', mmap=False).variables

            lbln = nes.keys()[0]
            if 'tot' in nes.keys():
                nes_tot = nes['tot'][:]
                phs_tot = phs['tot']
            else:
                lblp = phs.keys()[0]
                nes_tot = np.zeros_like(nes[lbln][:])
                phs_tot = np.zeros(len(phs[lblp][:]))
                for react in reacts:
                    self.nes_plot[react].set_data(nes['E_NEUT'][:], nes[react][:])
                    self.phs_plot[react].set_data(range(len(phs[react])), phs[react])
                    nes_tot += nes[react][:]
                    phs_tot += phs[react]
            self.ax_nes.set_xlabel('E %s' %nes['E_NEUT'].units)
            self.ax_nes.set_ylabel('Counts %s' %nes[lbln].units)

            yrange1 = [0, 1.1*np.max(nes_tot)]
            yrange2 = [0, 1.1*np.max(phs_tot)]
            self.ax_nes.set_ylim(yrange1)
            self.ax_phs.set_ylim(yrange2)
            self.nes_plot['tot'].set_data(nes['E_NEUT'][:], nes_tot)
            self.phs_plot['tot'].set_data(range(len(phs_tot)), phs_tot)
            self.line2452kev.set_data( [2452]*2, yrange1)
            self.ax_nes.figure.canvas.draw()


    def tot_nes(self, code='tr'):

# Dump setup dictionary

        self.code = code
        set_d = self.wsetup()

        mcE = tot_nes.TOT_NES(set_d, code=code)
        e_min  = set_d['Emin']
        e_max  = set_d['Emax']
        n_bins = set_d['n_bin']
        dE = (e_max - e_min)/float(n_bins - 1)
        Egrid = np.linspace(e_min, e_max, n_bins)

        if code == 'tr':

            cv = netcdf.netcdf_file(self.fcdf, 'r', mmap=False).variables
            tcdf = cv['TIME'][:]

            tfbm = mcE['time']
            jt = np.argmin(np.abs(tcdf - tfbm))

            rho  = cv['X'][jt]
            trprof = {}
            trprof['bt'] = cv['BTNT2_DD'][jt]
            trprof['bb'] = cv['BBNT2_DD'][jt]
            trprof['th'] = cv['THNTX'][jt]

            nmc = len(mcE['bt'])
            xmc = range(nmc)

            x = {'th':rho, 'bt':xmc, 'bb':xmc}
            dvol  = {'th':cv['DVOL'][jt] , 'bt':mcE['bmvol']   , 'bb':mcE['bmvol']}
            trneu = {'th':cv['NEUTX'][jt], 'bt':cv['BTNTS'][jt], 'bb':cv['BBNTS'][jt]}
            nes  = {}
            prof = {}
            nyield = {}
            neut_tot = 0
            for react in reacts:
                nes [react] = np.tensordot(mcE[react], dvol[react], axes=(0, 0))
                prof[react] = np.sum(mcE[react], axis=1)*dE
                nyield[react] = np.sum(prof[react]*dvol[react])
                print('Neutron yield %s: %12.4e [1/s] %12.4e [1/s]' %(react, nyield[react], trneu[react]))
                neut_tot += nyield[react]

            print('Total neutron yield: %12.4e [1/s] %12.4e [1/s]' %(neut_tot, cv['NEUTT'][jt]))

#=======
# Plots
#=======

            dvolframe = tk.Toplevel()
            dvolframe.geometry('1000x1000')
            figframe  = tk.Frame(dvolframe)
            figframe.pack(side=tk.TOP, fill=tk.X)

            dvolfig = Figure(figsize=(16, 10), dpi=100)
            dvolcan = FigureCanvasTkAgg(dvolfig, master=dvolframe)
            dvolcan._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=1)

            dvolfig.text(.5, .95, '%s - %s' %(cdf_file, self.ffbm), ha='center')

            nes_lbl  = {'th':'CDF->CtrRoom' , 'bt':'CDF, FBM->CtrRoom', 'bb':'FBM->CtrRoom'}
            prof_lbl = {'th':'CDF:THNTX'    , 'bt':'CDF:BTNT2_DD'     , 'bb':'CDF:BBNT2_DD'}
            x_lbl    = {'th':r'$\rho_{tor}$', 'bt':'MC index'         , 'bb':'MC index'}

            for j_spl, lbl in enumerate(reacts):
                ax = dvolfig.add_subplot(2, 3, j_spl+1)
                ax.plot(Egrid, nes[lbl][:], 'b-', label=nes_lbl[lbl])
                ax.set_title(titles[lbl]+' spectrum')
                ax.axvline(x=2.452, color='k', linewidth=1.5)
                ax.set_xlabel('E [MeV]')
                ax.set_ylabel('Counts [1/(s * MeV)]')
                ax.legend()

                ax = dvolfig.add_subplot(2, 3, j_spl+4)
                ax.plot(x[lbl], prof[lbl]  , 'b-', label=nes_lbl[lbl])
                ax.plot(x[lbl], trprof[lbl], 'g-', label=prof_lbl[lbl])
                ax.set_title(titles[lbl]+' yield profile')
                ax.set_xlabel(x_lbl[lbl])
                ax.set_ylabel('Counts [1/(s * cm**3)]')
                ax.legend()

            toolbar = nt2tk(dvolcan, dvolframe)
            toolbar.update()

        elif code == 'tc':

            prof = np.sum(mcE['tot'], axis=1)*dE
            drho = np.gradient(mcE['rho'])
            dvol = 1e6*mcE['dV'][:]*drho # cm**3 ; Improve: trapezoidal
            nes = np.tensordot(mcE['tot'], dvol, axes=(0, 0))

            plt.figure(2, figsize=(14, 9))
            plt.clf()

            plt.subplot(2, 1, 1)
            plt.plot(Egrid, nes, 'b-', label='FP->CtrRoom')
            plt.title('Total spectrum')
            plt.axvline(x=2.452, color='k', linewidth=1.5)
            plt.xlabel('E [MeV]')
            plt.ylabel('Counts  [1/(s MeV)]')
            plt.legend()

            plt.subplot(2, 1, 2)
            plt.plot(mcE['rho'], prof, 'b-', label='FP->CtrRoom')
            plt.title('Total yield profile')
            plt.xlabel(r'$\rho_{tor}$')
            plt.ylabel('Counts dN/dV [1/(s cm**3)]')
            plt.legend()

            plt.show()

        elif code == 'asc':

            nmc = len(mcE['bt'])
            xmc = range(nmc)

            x     = {'th': mcE['rhop'], 'bt':xmc         , 'bb':xmc}
            dvol  = {'th': 1e6*mcE['dvol'], 'bt':1e6*mcE['bmvol'], 'bb':1e6*mcE['bmvol']}
            nes  = {}
            prof = {}
            nyield = {}
            neut_tot = 0
            for react in reacts:
                print(react)
                print(mcE[react].shape, dvol[react].shape)
                nes [react] = np.tensordot(mcE[react], dvol[react], axes=(0, 0))
                prof[react] = np.sum(mcE[react], axis=1)*dE
                nyield[react] = np.sum(prof[react]*dvol[react])
                print('Neutron yield %s: %12.4e [1/s]' %(react, nyield[react]) )
                neut_tot += nyield[react]

            print('Total neutron yield: %12.4e [1/s]' %neut_tot)

#=======
# Plots
#=======

            dvolframe = tk.Toplevel()
            dvolframe.geometry('1000x1000')
            figframe  = tk.Frame(dvolframe)
            figframe.pack(side=tk.TOP, fill=tk.X)

            dvolfig = Figure(figsize=(16, 10), dpi=100)
            dvolcan = FigureCanvasTkAgg(dvolfig, master=dvolframe)
            dvolcan._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=1)

            dvolfig.text(.5, .95, self.fasc, ha='center')

            nes_lbl  = {'th': 'h5->CtrRoom', 'bt': 'h5->CtrRoom', 'bb': 'h5->CtrRoom'}
            x_lbl    = {'th': r'$\rho_{pol}$', 'bt': 'MC index' , 'bb': 'MC index'}

            for j_spl, lbl in enumerate(reacts):
                ax = dvolfig.add_subplot(2, 3, j_spl+1)
                ax.plot(Egrid, nes[lbl], 'b-', label=nes_lbl[lbl])
                ax.set_title(titles[lbl]+' spectrum')
                ax.axvline(x=2.452, color='k', linewidth=1.5)
                ax.set_xlabel('E [MeV]')
                ax.set_ylabel('Counts [1/(s * MeV)]')
                ax.legend()

                ax = dvolfig.add_subplot(2, 3, j_spl+4)
                ax.plot(x[lbl], prof[lbl]  , 'b-', label=nes_lbl[lbl])
                ax.set_title(titles[lbl]+' yield profile')
                ax.set_xlabel(x_lbl[lbl])
                ax.set_ylabel('Counts [1/(s * cm**3)]')
                ax.legend()

            toolbar = nt2tk(dvolcan, dvolframe)
            toolbar.update()


    def set_text(self, key, val):

        self.ent_d[key].delete(0, tk.END)
        self.ent_d[key].insert(0, val)


    def replot_aug(self):

# Get separatrix {R, z}

        parse_d = parse_los(self.flos)
        time = 6.5
        eq = read_equ.READ_EQU(self.fcdf, tvec=time, rho=1)
        r_plot, z_plot = mom2rz.mom2rz(eq.rc, eq.rs, eq.zc, eq.zs)
        r_sepx = 0.01*r_plot[0]
        z_sepx = 0.01*z_plot[0]

        self.set_text('CDF file', self.fcdf)

        self.pol_aug.set_data(r_sepx, z_sepx)
        self.augfig.canvas.draw()


    def callasc(self):

        dir_in = '%s/ascot/fbm' %home_dir
        self.fasc = tkfd.askopenfilename(initialdir=dir_in, filetypes=[("All formats", "*.h5")])
        self.set_text('ASCOT file', self.fasc)

    def callfp(self):

        dir_in = '%s/toric' %home_dir
        self.ffp = tkfd.askopenfilename(initialdir=dir_in, filetypes=[("All formats", "*.cdf")])
        self.set_text('TORIC file', self.ffp)

    def callfbm(self):

        dir_in = '%s/tr_client/AUGD' %home_dir
        self.ffbm = tkfd.askopenfilename(initialdir=dir_in, filetypes=[("All formats", "*.cdf")])
        self.set_text('FBM file', self.ffbm)
        self.fcdf = self.ffbm.split('_fi_')[0] + '.CDF'
        self.set_text('CDF file', self.fcdf)
        self.replot_aug()

    def calllos(self):

        self.flos = tkfd.askopenfilename(initialdir='%s/los' %crwd, filetypes=[("All formats", "*.los")])
        self.set_text('LOS file', self.flos)
        self.los_draw()


    def about(self):

        mytext = 'Documentation at <a href="http://www2.ipp.mpg.de/~git/ne213/simul.html">Simulation of Neutron Energy Spectra</a>'
        h = tkhyper.HyperlinkMessageBox("Help", mytext, "340x60")


if __name__ == "__main__":


    aug_defaults = False
    aug_defaults = True

    if aug_defaults:
        f_fbm = '/afs/ipp/home/g/git/tr_client/AUGD/29783/A01/29783A01_fi_1.cdf'
        f_los = '%s/los/aug.los' %crwd
        f_fp  = '/afs/ipp/home/g/git/toric/aug29783-2.15fp.cdf'
        f_asc = '/afs/ipp/home/g/git/ascot/fbm/29795_3.0s_ascot.h5'

        FI2SPECTRUM(f_fbm=f_fbm, f_los=f_los, f_tor=f_fp, f_asc=f_asc)
    else:
        FI2SPECTRUM()
