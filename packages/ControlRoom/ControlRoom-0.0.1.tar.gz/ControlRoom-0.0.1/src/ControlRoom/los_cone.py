import sys, logging
import numpy as np
try:
    import Tkinter as tk
except:
    import tkinter as tk
import los

fmt = logging.Formatter('%(asctime)s | %(name)s | %(levelname)s: %(message)s', '%H:%M:%S')
hnd = logging.StreamHandler()
hnd.setFormatter(fmt)
logger = logging.getLogger('los_cone')
logger.addHandler(hnd)
logger.setLevel(logging.INFO)

# No collimator tube
coll_diam = 8.8e-2
# Collimator tube 1
#coll_diam = 1.9e-2
# Collimator tube 2
#coll_diam = 0.9e-2

geo_aug_old = {'disk_thick':0.008, 'cell_radius':0.004, \
           'coll_diam':coll_diam, 'd_det_coll': 6.50, 'det_radius':0.0254, 'tilt':0, \
           'tan_radius':0.2, 'y_det':-13.63, 'z_det':0.1, \
           'Rmaj':1.65, 'r_chamb':0.6}
geo_aug = {'disk_thick':0.008, 'cell_radius':0.004, \
           'coll_diam':coll_diam, 'd_det_coll': 7.16, 'det_radius':0.0254, 'tilt':0, \
           'tan_radius':0.4, 'y_det':-13.32, 'z_det':0.1, \
           'Rmaj':1.65, 'r_chamb':0.6}
tok_lbl = 'aug'


def plot_los_cone(flos='aug.los'):


    import matplotlib.pylab as plt

    logger.info('Reading %s' %flos)

    try:
        x_m, y_m, z_m, Omega, V_m3 = np.loadtxt(flos, unpack=True)
    except IOError:
        raise
    R_m = np.hypot(x_m, y_m)

    f = plt.figure(1,figsize=(13, 5.5))
    f.subplots_adjust(left=0.05, bottom=0.05, right=0.95, top=0.98)

    ax1 = plt.subplot(1, 2, 1, aspect='equal')
    ax1.set_xlim([0.5, 3.5])
    ax1.set_ylim([-1.5, 1.5])
    ax1.plot(R_m, z_m, 'ro') 

    ax2 = plt.subplot(1, 2, 2, aspect='equal')
    ax2.set_xlim([-3, 3])

# Plot AUG wall
    try:
        import aug_sfutils as sf
        gc_d = sf.getgc()
        for gc in gc_d.values():
            ax1.plot(gc.r, gc.z, 'b-')
    except:
        logger.error('No coordinates of wall structures available for poloidal section drawing')

    try:
        import plot_aug
        dic = plot_aug.STRUCT().tor_old
        for key in dic.keys():
            ax2.plot(dic[key].x, dic[key].y, 'b-')
    except:
        logger.error('No coordinates of wall structures available for toroidal section drawing')

    ax2.plot(x_m, y_m, 'ro')
    ax2.set_xlabel('x [m]', labelpad=2)
    ax2.set_ylabel('y [m]', labelpad=-14)
    ax2.tick_params(which='major', length=4, width=0.5)

    plt.show()


class DET_LOS:


    def __init__(self):


        myframe = tk.Tk(className=' Detector line of sight')

        geo_init = geo_aug

        menuframe = tk.Frame(myframe)
        toolframe = tk.Frame(myframe)
        entframe  = tk.Frame(myframe)
        toolframe.grid(row=0, sticky=tk.W+tk.E)
        entframe.grid(row=1, sticky=tk.W+tk.E)

# Menubar
        menubar = tk.Menu(myframe)

        filemenu = tk.Menu(menubar, tearoff=0)
        filemenu.add_command(label="Run", command=self.run)
        filemenu.add_separator()
        filemenu.add_command(label="Exit", command=sys.exit)
        menubar.add_cascade(label="File", menu=filemenu)
        myframe.config(menu=menubar)

# Toolbar

        try:
            okfig = tk.PhotoImage(file='ed_execute.gif')
            qtfig = tk.PhotoImage(file='bld_exit.gif')
            btok = tk.Button(toolframe, command=self.run, image=okfig)
            btqt = tk.Button(toolframe, command=sys.exit, image=qtfig)
            btok.pack(side=tk.LEFT)
            btqt.pack(side=tk.LEFT)
        except:
            pass

# Entries

        enwid = 11

        self.geo_d = {}
        nrow = 0
        for key, val in geo_init.items():
            lbl = tk.Label(entframe, text=key)
            var = tk.Entry(entframe, width=enwid)
            var.insert(0, val)
            self.geo_d[key] = var
            lbl.grid(row=nrow, column=0, sticky=tk.W+tk.E)
            var.grid(row=nrow, column=1, sticky=tk.W+tk.E)
            nrow += 1
        myframe.mainloop()


    def run(self):

        logger.info('Starting LOS cone calculation')
        geo = {}
        for key, val in self.geo_d.items():
            geo[key] = float(val.get())
        los_d = {}
        los_d['x0']    = -geo['y_det']
        los_d['y0']    = 0.001
        los_d['z0']    = geo['z_det']
        los_d['xend']  = 0 # 1 plasma crossing
#        los_d['xend']  = geo['y_det'] # 2 plasma crossings
        los_d['theta'] = np.radians(geo['tilt'])
        los_d['phi']   = -np.arctan2(geo['tan_radius'], geo['y_det'])

        ctilt = np.cos(los_d['theta'])
        dy = geo['disk_thick']*ctilt
        ndisks = int(-2*geo['y_det']/dy)

        det_los = los.PHILOS(los_d, npoints=ndisks)

# Get separatrix {R,z}

        rmin = geo['Rmaj']  - geo['r_chamb'] 
        rmax = geo['Rmaj']  + geo['r_chamb'] 

# Restrict to LOS inside the plasma

        dr = det_los.rline[1] - det_los.rline[0]
        dz = det_los.zline[1] - det_los.zline[0]
        dl = np.hypot(dr, dz)
        ind = (det_los.rline > rmin - dl) & (det_los.rline < rmax + dl)
        r_in = det_los.rline[ind]
        z_in = det_los.zline[ind]
        x_in = det_los.xline[ind]
        y_in = det_los.yline[ind]

# Write ASCII file for LOS, used in the spectrum evaluation

        y_los = x_in
        z_los = z_in
        det_pos = (geo['tan_radius'], geo['y_det'], geo['z_det'])
        det_dist = np.hypot(y_los - det_pos[1], z_los - det_pos[2])
        ctilt = np.cos(np.radians(geo['tilt']))
        stilt = np.sin(np.radians(geo['tilt']))
        dy = geo['disk_thick']*ctilt
        coll_rad = 0.5*geo['coll_diam']
        dist_corr = geo['d_det_coll']/(1. + geo['det_radius']/coll_rad) # Shifting the cone vertex to the point where lines (det-left - coll-right, det-right - coll-left) cross
        tan_cone_aper = coll_rad/dist_corr
        logger.debug(coll_rad, dist_corr, tan_cone_aper)
        cone_aper = np.degrees(np.arctan(tan_cone_aper))
        offset = geo['d_det_coll'] - dist_corr # scalar, r2
        logger.debug('Cone aperture: %6.3f deg' %cone_aper)
        disk_radius = (det_dist - offset)*tan_cone_aper # array on discretised LoS
        n_disks = len(y_los)

# Each disk is divided in n_circles circular sectors,
# n_circles depends on the disk radius (which is almost constant)
# Every circular sector is divided in n_sectors sectors,
# equidistant poloidally; n_sectors is proportional to the radius
# of the circular sector

        cell_posx  = []
        cell_posy  = []
        cell_posz  = []
        cell_omega = []
        cell_vol   = []

        for jdisk in range(n_disks):
            n_circles = int(0.5 + disk_radius[jdisk]/geo['cell_radius'])
            delta_radius = disk_radius[jdisk]/float(n_circles)

# radius, alpha in the 'middle' of the sector
# The central circle has only one sector (cell)
            cvol = np.pi * delta_radius**2 * dy
            cell_vol = np.append(cell_vol, np.repeat(cvol, n_circles**2))

            radius = (0.5 + np.arange(n_circles))*delta_radius
            radius[0] = 0.
            omega_fac = np.pi * geo['det_radius']**2/det_dist[jdisk]**3
            for j_circle in range(n_circles):
                n_sectors = 2*j_circle + 1
                cell_det_dist = np.hypot(det_dist[jdisk], radius[j_circle])
                omega_circle = omega_fac * cell_det_dist
                cell_omega = np.append(cell_omega, np.repeat(omega_circle, n_sectors))

# Poloidal sectors (cells) in a circle
                alpha = 2.*np.pi/float(n_sectors) * np.arange(n_sectors)
                rcos = radius[j_circle]*np.cos(alpha)
                rsin = radius[j_circle]*np.sin(alpha)
# cell_pos: with respect to torus center
                cell_posx = np.append(cell_posx, det_pos[0] + rcos)
                cell_posy = np.append(cell_posy, -y_los[jdisk] - rsin*stilt)
                cell_posz = np.append(cell_posz,  z_los[jdisk] + rsin*ctilt)

        n_cells = len(cell_vol)

        header = \
           'LOS\n' + \
           '   y1 = %9.4f m\n'  % y_los[0]  + \
           '   y2 = %9.4f m\n'  % y_los[-1] + \
           '   z1 = %9.4f m\n'  % z_los[0]  + \
           '   z2 = %9.4f m\n'  % z_los[-1] + \
           'Detector:\n' + \
           '   Position [m] x, y, z: %9.4f, %9.4f, %9.4f\n' %det_pos + \
           '   Radius = %9.4f m\n' % geo['det_radius'] + \
           '   Collimation angle = %9.4f deg\n' % cone_aper + \
           'Disks:\n' + \
           '   Thickness = %9.4f m\n' % dy + \
           '   # disks = %5d\n' % n_disks + \
           'Cells:\n' + \
           '   Radius = %9.4f m\n' % geo['cell_radius'] + \
           '   # cells = %d\n' %n_cells + \
"""
   (x,y,x) cell cartensian coordinates [m]
   Omega  Steradians is the volume in the solid angle
   Vol = cell volume [m**3]
x             y             z             Omega         Vol
"""

        los_file = '%s.los' %tok_lbl

        logger.info('Storing ASCII output, n_cells=%d', n_cells)
        np.savetxt(los_file, np.hstack((cell_posx, cell_posy, cell_posz, cell_omega, cell_vol)).reshape(5, n_cells).T, header=header, fmt='%13.6E')
        logger.info('Written output file %s' %los_file)
        plot_los_cone()


if __name__ == '__main__':


    DET_LOS()
