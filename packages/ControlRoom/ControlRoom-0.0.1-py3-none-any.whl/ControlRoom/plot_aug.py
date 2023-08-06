import numpy as np

import numpy as np


class ROT_MATRIX:


    def __init__(self, alpha, x_in, y_in, x_cen=0, y_cen=0):

        x_in2  = x_in - x_cen      
        y_in2  = y_in - y_cen
        x_out2 = x_in2*np.cos(alpha) - y_in2*np.sin(alpha)
        y_out2 = x_in2*np.sin(alpha) + y_in2*np.cos(alpha)
        self.x = x_out2 + x_cen
        self.y = y_out2 + y_cen


class STRUCT:


    coils = {'R':2.3, 'phi_beg':1.402, 'dphi':0.730, 'phi_shift':0.7854}


    def __init__(self, f_in= '/afs/ipp/aug/ads-diags/common/diaggeom.data/tor.data'):

# Toroidal

        print('Reading structure data from file %s' %f_in)
        f = open(f_in,'r')

        xtor_struct = {}
        ytor_struct = {}
        jstr = 0
        xtor_struct[jstr] = []
        ytor_struct[jstr] = []
        for line in f.readlines():
            if (line.strip() != ''):
                xval, yval = line.split()
                xtor_struct[jstr].append(float(xval))
                ytor_struct[jstr].append(float(yval))
            else:
                jstr += 1
                xtor_struct[jstr] = []
                ytor_struct[jstr] = []
        f.close()
        nstr = jstr

# Rotate

        gamma = -3*np.pi/8 # 3 sectors out of 16
        self.tor_str = {}
        self.tor_old = {}
        for jstr in range(nstr):
            x_in = np.array(xtor_struct[jstr])
            y_in = np.array(ytor_struct[jstr])
            self.tor_str[jstr] = ROT_MATRIX(gamma, x_in, y_in)
            self.tor_old[jstr] = ROT_MATRIX(0,     x_in, y_in)
