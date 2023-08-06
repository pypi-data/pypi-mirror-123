import math

class Units:
    names = {}
    def __init__(self,L,M,T,C):
        self.L = L
        self.M = M
        self.T = T
        self.C = C
    def __eq__(self,x):
        return self.L == x.L and self.M == x.M \
           and self.T == x.T and self.C == x.C
    def __ne__(self,x):
        return self.L != x.L or self.M != x.M \
           and self.T != x.T or self.C != x.C
    def __mul__(self,x):
        return Units(self.L+x.L,self.M+x.M,self.T+x.T,self.C+x.C)
    def __div__(self,x):
        return Units(self.L-x.L,self.M-x.M,self.T-x.T,self.C-x.C)
    def inverse(self):
        return Units(-self.L,-self.M,-self.T,-self.C)
    def power(self,n):
        return Units(self.L*n,self.M*n,self.T*n,self.C*n)
    def root(self,n):
        if self.L % n or self.M % n or self.T % n or self.C % n:
            raise TypeError("cannot take %d-th root" % n)
        else:
            return Units(self.L/n,self.M/n,self.T/n,self.C/n)

class Scalar(object):
    def __init__(self,value,units):
        self.value = value
        self.units = units
    def __float__(self):
        if self.units == Units(0,0,0,0):
            return self.value
        else:
            raise TypeError("not a dimensionless number")
    def __pos__(self):
        return Scalar(self.value,self.units)
    def __neg__(self):
        return Scalar(-self.value,self.units)
    def __add__(self,x):
        if type(x) is not Scalar:
            return float(self)+x
        elif self.units == x.units:
            return Scalar(self.value+x.value,self.units)
        else:
            raise TypeError("incompatible units")
    def __radd__(self,x):
        # were x a Scalar, it would have triggered __add__
        return x + float(self)
    def __sub__(self,x):
        if type(x) is not Scalar:
            return float(self)-x
        elif self.units == x.units:
            return Scalar(self.value-x.value,self.units)
        else:
            raise TypeError("incompatible units")
    def __rsub__(self,x):
        # were x a Scalar, it would have triggered __sub__
        return x - float(self)
    def __mul__(self,x):
        if type(x) is Scalar:
            return Scalar(self.value*x.value,self.units*x.units)
        elif type(x) is Vector:
            return Vector(x.x*self,x.y*self,x.z*self)
        else:
            return Scalar(self.value*x,self.units)
    def __rmul__(self,x):
        # were x a Scalar or a Vector, it would have triggered __mul__
        return Scalar(self.value*x,self.units)
    def __div__(self,x):
        if type(x) is Scalar:
            return Scalar(self.value/x.value,self.units/x.units)
        else:
            return Scalar(self.value/x,self.units)
    def __rdiv__(self,x):
        # were x a Scalar, it would have triggered __div__
        return Scalar(x/self.value,self.units.inverse())
    def __pow__(self,n):
        return Scalar(pow(self.value,n),self.units.power(n))
    def __cmp__(self,x):
        if type(x) is not Scalar:
            return cmp(float(self),x)
        elif self.units == x.units:
            return cmp(self.value,x.value)
        else:
            raise TypeError("incompatible units")
    def __nonzero__(self):
        return self.value != 0.0
    # formatting
    formatters = {}
    def __format(self):
        u = (self.units.L,self.units.M,self.units.T,self.units.C)
        if u in Scalar.formatters:
            value, units = Scalar.formatters[u](self.value)
        else:
            value = self.value
            value, l_units = Scalar.formatters['length'](value, self.units.L)
            value, m_units = Scalar.formatters['mass'](value, self.units.M)
            value, t_units = Scalar.formatters['time'](value, self.units.T)
            value, c_units = Scalar.formatters['charge'](value, self.units.C)
            units = " ".join([u for u in l_units,m_units,t_units,c_units
                                if u != '' ])
        return value, units
    def __repr__(self):
        value, units = self.__format()
        if units:
            return "%s %s" % (repr(value),units)
        else:
            return repr(value)
    def __str__(self):
        value, units = self.__format()
        if units:
            return "%.8g %s" % (value,units)
        else:
            return str(value)

def _formatLength(x, L):
    if L == 0:
        return x, ''
    elif L == 1:
        return x, 'm'
    else:
        return x, 'm^%d' % L
Scalar.formatters['length'] = _formatLength
del _formatLength

def _formatMass(x, M):
    if M == 0:
        return x, ''
    elif M == 1:
        return x, 'kg'
    else:
        return x, 'kg^%d' % M
Scalar.formatters['mass'] = _formatMass
del _formatMass

def _formatTime(x, T):
    if T == 0:
        return x, ''
    elif T == 1:
        return x, 's'
    else:
        return x, 's^%d' % T
Scalar.formatters['time'] = _formatTime
del _formatTime

def _formatCharge(x, C):
    if C == 0:
        return x, ''
    elif C == 1:
        return x, 'A'
    else:
        return x, 'A^%d' % C
Scalar.formatters['charge'] = _formatCharge
del _formatCharge

def fabs(x):
    if type(x) is Scalar:
        return Scalar(math.fabs(x.value),x.units)
    else:
        return math.fabs(x)

def sqrt(x):
    if type(x) is Scalar:
        return Scalar(math.sqrt(x.value),x.units.root(2))
    else:
        return math.sqrt(x)
def root(x,n):
    if type(x) is Scalar:
        return Scalar(pow(x.value,1.0/n),x.units.root(n))
    else:
        return pow(x,1.0/n)

def sin(x):
    if type(x) is Scalar:
        x = float(x)
    return math.sin(x)
def cos(x):
    if type(x) is Scalar:
        x = float(x)
    return math.cos(x)
def tan(x):
    if type(x) is Scalar:
        x = float(x)
    return math.tan(x)

def asin(x):
    if type(x) is Scalar:
        x = float(x)
    return math.asin(x)
def acos(x):
    if type(x) is Scalar:
        x = float(x)
    return math.acos(x)
def atan(x):
    if type(x) is Scalar:
        x = float(x)
    return math.atan(x)
def atan2(x,y):
    if type(x) is Scalar and type(y) is Scalar:
        if x.units == y.units:
            x = x.value
            y = y.value
        else:
            raise TypeError("incompatible units")
    return math.atan2(x,y)

def exp(x):
    if type(x) is Scalar:
        x = float(x)
    return math.exp(x)
def log(x):
    if type(x) is Scalar:
        x = float(x)
    return math.log(x)


class Vector(object):
    def __init__(self,x,y,z):
        # don't use this. Use the factory methods below.
        try:
            self.x = Scalar(float(x),Units(0,0,0,0))
        except:
            self.x = x
        try:
            self.y = Scalar(float(y),Units(0,0,0,0))
        except:
            self.y = y
        try:
            self.z = Scalar(float(z),Units(0,0,0,0))
        except:
            self.z = z
        if self.x.units != self.y.units or self.y.units != self.z.units:
            raise TypeError("incompatible units")
        self.units = self.x.units
    def Cartesian(x,y,z):
        return Vector(x,y,z)
    Cartesian = staticmethod(Cartesian)
    def Polar(r,theta,phi):
        return Vector(r*sin(phi)*cos(theta),
                      r*sin(phi)*sin(theta),
                      r*cos(phi))
    Polar = staticmethod(Polar)
    def __abs__(self):
        return sqrt(self.x*self.x+self.y*self.y+self.z*self.z)
    def r(self):
        return abs(self)
    def phi(self):
        return math.atan2(self.y.value,self.x.value)
    def mu(self):
        if self.z.value:
            return self.z/abs(self)
        else:
            return 0.0
    r = property(r,None,None)
    phi = property(phi,None,None)
    mu = property(mu,None,None)
    def versor(self):
        r = abs(self)
        return Vector(self.x/r,self.y/r,self.z/r)
    versor = property(versor,None,None)
    def __pos__(self):
        return Vector(self.x,self.y,self.z)
    def __neg__(self):
        return Vector(-self.x,-self.y,-self.z)
    def __add__(self,v):
        if self.x.units == v.x.units:
            return Vector(self.x+v.x,self.y+v.y,self.z+v.z)
        else:
            raise TypeError("incompatible units")
    def __sub__(self,v):
        if self.x.units == v.x.units:
            return Vector(self.x-v.x,self.y-v.y,self.z-v.z)
        else:
            raise TypeError("incompatible units")
    def __mul__(self,a):
        if type(a) is Vector:
            return self.x*a.x+self.y*a.y+self.z*a.z
        else:
            return Vector(self.x*a,self.y*a,self.z*a)
    def __rmul__(self,a):
        # were x a Scalar or a Vector, it would have triggered __mul__
        return Vector(self.x*a,self.y*a,self.z*a)
    def __div__(self,a):
        return Vector(self.x/a,self.y/a,self.z/a)
    # comparisons
    def __eq__(self,v):
        if self.units == v.units:
            return self.x == v.x and self.y == v.y and self.z == v.z
        else:
            raise TypeError("incompatible units")
    def __ne__(self,v):
        if self.units == v.units:
            return self.x != v.x or self.y != v.y or self.z != v.z
        else:
            raise TypeError("incompatible units")
    def __nonzero__(self):
        return not (not self.x and not self.y and not self.z)
    # formatting
    formatters = {}
    def __repr__(self):
        u = (self.units.L,self.units.M,self.units.T,self.units.C)
        if u in Vector.formatters:
            x, y, z, units = Vector.formatters[u](self.x.value,
                                                  self.y.value,
                                                  self.z.value)
        else:
            x = self.x.value ; y = self.y.value ; z = self.z.value
            x, y, z, l_units = Vector.formatters['length'](x,y,z,self.units.L)
            x, y, z, m_units = Vector.formatters['mass'](x,y,z,self.units.M)
            x, y, z, t_units = Vector.formatters['time'](x,y,z,self.units.T)
            x, y, z, c_units = Vector.formatters['charge'](x,y,z,self.units.C)
            units = " ".join([u for u in l_units,m_units,t_units,c_units
                                if u != '' ])
        return "<%s, %s, %s> %s" % (x,y,z,units)

def _formatLength(x, y, z, L):
    if L == 0:
        return x, y, z, ''
    elif L == 1:
        return x, y, z, 'm'
    else:
        return x, y, z, 'm^%d' % L
Vector.formatters['length'] = _formatLength
del _formatLength

def _formatMass(x, y, z, M):
    if M == 0:
        return x, y, z, ''
    elif M == 1:
        return x, y, z, 'kg'
    else:
        return x, y, z, 'kg^%d' % M
Vector.formatters['mass'] = _formatMass
del _formatMass

def _formatTime(x, y, z, T):
    if T == 0:
        return x, y, z, ''
    elif T == 1:
        return x, y, z, 's'
    else:
        return x, y, z, 's^%d' % T
Vector.formatters['time'] = _formatTime
del _formatTime

def _formatCharge(x, y, z, C):
    if C == 0:
        return x, y, z, ''
    elif C == 1:
        return x, y, z, 'A'
    else:
        return x, y, z, 'A^%d' % C
Vector.formatters['charge'] = _formatCharge
del _formatCharge


# standard and non-standard units

meter = Scalar(1.0,Units(1,0,0,0))
centimeter = 0.01 * meter
inch = 2.54 * centimeter
meters = meter
centimeters = centimeter
inches = inch

kilogram = Scalar(1.0,Units(0,1,0,0))
gram = 0.001 * kilogram
amu = 1.66053873e-27 * kilogram
kilograms = kilogram
grams = gram

second = Scalar(1.0,Units(0,0,1,0))
minute = 60 * second
seconds = second
minutes = minute

Ampere = Scalar(1.0,Units(0,0,0,1))
statAmpere = 3.3356409e-10 * Ampere

radian = Scalar(1.0,Units(0,0,0,0))
degree = (math.pi/180)*radian
radians = radian
degrees = degree
steradian = Scalar(1.0,Units(0,0,0,0))
steradians = steradian

barn = 1.0e-24 * centimeter * centimeter
millibarn = 0.001 * barn

Hertz = 1/second
Scalar.formatters[(0,0,-1,0)] = lambda x: (x, 'Hz')

Newton = kilogram*meter/(second*second)
dyne = 1.0e-5 * Newton
Scalar.formatters[(1,1,-2,0)] = lambda x : (x,'N')
Vector.formatters[(1,1,-2,0)] = lambda x,y,z : (x,y,z,'N')

Joule = Newton*meter
erg = 1.0e-7 * Joule
keV = 1.602176462e-16 * Joule
eV = keV / 1000
MeV = 1000 * keV
GeV = 1000 * MeV
Scalar.formatters[(2,1,-2,0)] = lambda x : (x, 'J')

Watt = Joule/second
Scalar.formatters[(2,1,-3,0)] = lambda x : (x, 'W')

Pascal = Newton/(meter*meter)
Scalar.formatters[(-1,1,-2,0)] = lambda x : (x, 'Pa')

Coulomb = Ampere*second
esu = 3.3356409e-10 * Coulomb
statCoulomb = esu
Scalar.formatters[(0,0,1,1)] = lambda x : (x, 'C')

Volt = Watt/Ampere
Farad = Coulomb/Volt
Ohm = Volt/Ampere
Siemens = 1/Ohm
Weber = Volt*second
Tesla = Weber/(meter*meter)
Henry = Weber/Ampere

# angles

parallel = 0*degrees      # with respect to z
perpendicular = 90*degrees
antiparallel = 180*degrees

tangential = parallel
radial = perpendicular

# other constants

pi = math.pi
