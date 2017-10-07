import bitstring
from functools import singledispatch
import fractions
import cmath
import numbers

@singledispatch
def exp(arg):
    pass

@singledispatch
def sqrt(arg):
    pass

@singledispatch
def pow(arg,n):
    pass

@singledispatch
def inv(arg):
    pass


"""
class Alphabet3:
    def __init__(self):
        self.storagetype = "uint8"
        self.n = 3
        self.n2 = 8
    def exacts(self):
        return (1)
    def one(self):
        pass
    def zero(self):
        pass
    def inf(self):
        raise "implement inf of alphabet"

class Alphabet4:
    def __init__(self):
        self.storagetype = "uint16"
        self.n = 4
        self.n2 = 16
    def exacts(self):
        return (1,2)
    def one(self):
        pass
    def zero(self):
        pass
    def inf(self):
        raise "implement inf of alphabet"
"""

# This is generic
class Alphabet:
    def __init__(self,eexacts):
        self.eexacts = eexacts
        self.n = len(eexacts)+1
        self.n2 = 2**self.n
        self.storagetype = "auto"
    def one(self):
        return self.rawpnum(self.n2>>2)
    def zero(self):
        return Pnum(self,0)
    def inf(self):
        return self.rawpnum(self.n2>>1)
    def pnnvalues(self):
        return self.n2
    def pnnmask(self):
        return self.n2-1 # as type
    def pnmod(self,x):
        return x & self.pnnmask()
    def next(self,x):
        return Pnum(self,(x + (self.n2 >> 2)) & self.pnnmask()) # 1
    def rawpnum(self,x):
        #q = bitstring.BitArray(self.n2)
        #q.int = x
        return Pnum(self,x) # & self.pnmod(,
    def convert(self,value):
        if isinstance(value,numbers.Rational):
            return self.searchvalue(float(value))
        else:
            if cmath.isnan(value):
                raise Exception("cannot cast nan to pnum")
            else:
                return self.searchvalue(value)
    def searchvalue(self,x):
        if x == 0:
            return self.zero()
        if x < 0:
            return -self.convert(-x)
        if cmath.isinf(x):
            return self.inf()
        etable = self.exacts()
        if x < 1:
            while True:
                mid = lo + ((hi - lo) >> 1)
                if (mid == lo or mid == hi):
                    break
                lo, hi = (mid,hi) if (inv(etable[mid]) > x) else (lo, mid)
            #lo > 0 && inv(etable[lo]) == x && return inv(fromexactsindex(T, lo))
            #hi <= length(etable) && inv(etable[hi]) == x && return inv(fromexactsindex(T, hi))
            #lo == 0 && return prevpnum(one(T)) # Never happens
            #hi > length(etable) && return nextpnum(zero(T))
            #return inv(nextpnum(fromexactsindex(T, lo)))
        else:
            while True:
              mid = lo + ((hi - lo) >> 1)
              if (mid == lo or mid == hi):
                break
              lo, hi = (mid,hi) if (etable[mid] < x) else (lo, mid)

            #lo > 0 && etable[lo] == x && return fromexactsindex(T, lo)
            #hi <= length(etable) && etable[hi] == x && return fromexactsindex(T, hi)
            #lo == 0 && return nextpnum(one(T)) # Never happens
            #hi > length(etable) && return prevpnum(pninf(T))
            #return nextpnum(fromexactsindex(T, lo))
    @staticmethod
    def p3():
        return Alphabet((1,))
    @staticmethod
    def p4():
        return Alphabet((1,2))
    @staticmethod
    def p8():
        return Alphabet([fractions.Fraction(2**n*(4 + m),4) for m in range(0,4) for n in range(0,8)])
    @staticmethod
    def p16():
        return Alphabet([fractions.Fraction(2**n*(256 + m),256) for m in range(0,256) for n in range(0,32)])

class Pnum:
    def __init__(self,base,v):
        self.base = base
        self.v = v
    def __mul__(self,other):
        # mapreduce(*,Sopn, eachpnum(self),eachpnum(other)) 
        pass
    def __add__(self,other):
        # mapreduce(+,Sopn, eachpnum(self),eachpnum(other)) 
        pass
    def __div__(self,other):
        return self*(~other)
    def __sub__(self,other):
        return self+(-other)
    def __neg__(self):
        return Pnum(self.base,-self.v)
    def __invert__(self): # ~x == /x
        return Pnum(self.base,-(self.v+self.base.inf()))
    def one(self):
        return self.rawpnum(self.n2 >> 2)
    def zero(self):
        return self.rawpnum(0)
    def inf(self):
        return self.rawpnum(self.n2 >> 1)
    def fromindex(self,i):
        # generic index 0..n2
        return self.rawpnum(i)
    def fromexactsindex(self,i):
        # index 0..len(values)
        return self.rawpnum((self.n2 >> 2) +  ((i-1)<<1) )
    def exacts(self):
        return self.eexacts
    def iszero(self,x):
        return x == 0
    def isinf(self):
        return self.v == (self.base.n2 >> 1)
    def isexact(self,x):
        return (x & 1) == 0 # ubit
    def next(self):
        return (self.v + (self.base.n2 >> 2)) & self.base.pnnmask() # 1
    def prev(self):
        return (self.v - (self.base.n2 >> 2)) & self.base.pnnmask() # 1
    def isstrictlynegative(self):
        return self.v > (self.base.n2>>1) # pinf
    def _exacttimes(self,other):
        rx = self.exactvalue().widen()
        ry = other.exactvalue().widen()
        return self.base.inf() if rx.isinf() or ry.isinf() else Pnum(self.base,rx*ry) # ????
    def _exactsum(self,other):
        rx = self.exactvalue().widen()
        ry = other.exactvalue().widen()
        return self.base.inf() if rx.isinf() or ry.isinf() else Pnum(self.base,rx+ry) # ????
    def slowsquare(self,other):
        ai = self.isinf()
        a0 = self.iszero()
        if a1:
            return Pbound.inf(self.base)
        if a0:
            return Pbound.zero(self.base)
        ae = self.isexact()
        be = other.isexact()
        abe = ae and be
        x = self
        y = self
        x1,x2 = (x,x) if ae else (x.prev(),x.next())
        y1,y2 = (y,y) if be else (y.prev(),y.next())
        if x.isstrictlynegative():
            x1,x2 = x2,x1
            y1,y2 = y2,y1
        z1 = x1._exacttimes(y1)
        #z1 = (!bothexact && isexact(z1)) ? nextpnum(z1) : z1
        z1 = z1.next() if (not abe and z1.isexact()) else z1
        z2 = z2.next() if (not abe and z2.isexact()) else z2
        return Pbound(self.base,z1,z2)
    # ritorns Pbound
    def slowtimes(self,other):
        ai = self.isinf()
        a0 = self.iszero()
        bi = other.isinf()
        b0 = other.iszero()
        if (ai and b0) or (a0 and bi):
            return Pbound.everything(self.base)
        if (ai or bi):
            return Pbound.inf(self.base)
        if (a0 or b0):
            return Pbound.zero(self.base)
        ae = self.isexact()
        be = other.isexact()
        abe = ae and be
        x = self
        y = other
        x1,x2 = (x,x) if ae else (x.prev(),x.next())
        y1,y2 = (y,y) if be else (y.prev(),y.next())
        if x.isstrictlynegative():
            x1,x2 = x2,x1
        if y.isstrictlynegative():
            y1,y2 = y2,y1
        z1 = x1._exacttimes(y1)
        z2 = x2._exacttimes(y2)
        #z1 = (!bothexact && isexact(z1)) ? nextpnum(z1) : z1
        z1 = z1.next() if (not abe and z1.isexact()) else z1
        z2 = z2.next() if (not abe and z2.isexact()) else z2
        return Pbound(self.base,z1,z2)
    # 
    def slowtwice(self):
        ai = self.isinf()
        if a:
            return Pbound.everything(self.base)
        if self.iszero():
            return self
        ae = self.isexact()
        abe = True
        x = self
        y = self
        x1,x2 = (x,x) if ae else (x.prev(),x.next())
        y1,y2 = (y,y) if be else (y.prev(),y.next())
        z1 = x1._exactplus(y1)
        z2 = x2._exactplus(y2)
        #z1 = (!bothexact && isexact(z1)) ? nextpnum(z1) : z1
        z1 = z1.next() if (not abe and z1.isexact()) else z1
        z2 = z2.next() if (not abe and z2.isexact()) else z2
        return Pbound(self.base,z1,z2)
    # ritorns Pbound
    def slowplus(self,other):
        ai = self.isinf()
        bi = other.isinf()
        if (ai and bi):
            return Pbound.everything(self.base)
        if (ai or bi):
            return Pbound.inf(self.base)
        if self.iszero():
            return other
        if other.iszero():
            return self
        ae = self.isexact()
        be = other.isexact()
        abe = ae and be
        x = self
        y = other
        x1,x2 = (x,x) if ae else (x.prev(),x.next())
        y1,y2 = (y,y) if be else (y.prev(),y.next())
        z1 = x1._exactplus(y1)
        z2 = x2._exactplus(y2)
        #z1 = (!bothexact && isexact(z1)) ? nextpnum(z1) : z1
        z1 = z1.next() if (not abe and z1.isexact()) else z1
        z2 = z2.next() if (not abe and z2.isexact()) else z2
        return Pbound(self.base,z1,z2)
    def exactvalue(self):
        x = self.v
        if self.isstrictlynegative():
            return -self.exactvalue(-x)
        if x < (self.base.n2>>2):
            return inv(self.exactvalue(inv(x)))
        else:
            if self.isinf():
                return fractions.Fraction(1,0)
            else:
                return self.base.eexacts[(x -  (self.base.n2>>2))] #index(x) - index(one(x))) >> 1) + 1
    def __str__(self):
        if self.isinf():
            return "pnum(/0)"
        else:
            v = self.exactvalue()
            if v.denominator == 1: 
                return "pnum(%s)" % v.numerator
            elif v.numerator == 1:
                return "pnum(/%s)" % v.denominator
            else:
                return "pnum(%s/%s)" % (v.numerator,v.denominator)


# interval using two Pnum
class Pbound:
    def __init__(self,first_or_empty,last=None):
        if first_or_empty is True:
            self.empty = True
            self.v = (last,last)
        else:   
            if not isinstance(first_or_empty,Pnum):
                raise Exception("expection")
            if last is not None and not isinstance(first_or_empty,Pnum):
                raise Exception("expection")
            self.empty = False
            self.v = (first_or_empty,first_or_empty if last is None else last)
    def complement(self):
        if self.empty:
            return Pbound.everything(self.base)
        elif self.iseverything():
            return Pbound.empty(self.base)
        else:
            return Pbound(self.v[1].next(),self.v[0].prev())
    def iter(self):
        if self.empty:
            return
        f,l = self.v
        while f != l:
            yield f
            f = f.next()
    def iseverything(self):
        return self.v[0] == self.v[1].next()
    @property
    def base(self):
        return self.v[0].base
    @staticmethod
    def inf(base):
        return Pbound(base.inf())
    @staticmethod
    def one(base):
        return Pbound(base.one())
    @staticmethod
    def zero(base):
        return Pbound(base.zero())
    @staticmethod
    def empty(base):
        return Pbound(True,base.zero())
    @staticmethod
    def finite(base):
        return Pbound(base.inf().next(),base.inf().prev())
    @staticmethod
    def nonzero(base):
        return Pbound(base.zero().next(),base.zero().prev())
    @staticmethod
    def everything(base):
        return Pbound(base.inf().next(),base.inf())

"""def asfloat(self):
    pass
def exp(self):
    #mapreduce(exp,union,Sopn,self.eachpnum)
    pass
def sqrt(self):
    #mapreduce(sqrt,union,Sopn,self.eachpnum)
    pass
def pow(self,n):
    pass"""

#https://github.com/jwmerrill/Pnums.jl/blob/master/src/ops.jl

# set of Pnums
class Sopn:
    def __init__(self,x=None):
        # copy other Sopn
        # float
        pass
    def __mul__(self,other):
        # mapreduce(*,Sopn, eachpnum(self),eachpnum(other)) 
        pass
    def __div__(self,other):
        # mapreduce(/,Sopn, eachpnum(self),eachpnum(other)) 
        pass
    def __add__(self,other):
        # mapreduce(+,Sopn, eachpnum(self),eachpnum(other)) 
        pass
    def __sub__(self,other):
        # mapreduce(-,Sopn, eachpnum(self),eachpnum(other)) 
        pass
    def __neg__(self):
        # mapreduce((-),Sopn, eachpnum(self))
        pass
    def __invert__(self): # ~x == /x
        # mapreduce(inv,Sopn, eachpnum(self))
        pass
    def __ior_(self,p):
        # inplace or of the pvvoe
        pass
    def eachpnum(self):
        pass
    def asfloat(self):
        pass
    def exp(self):
        #mapreduce(exp,union,Sopn,self.eachpnum)
        pass
    def sqrt(self):
        #mapreduce(sqrt,union,Sopn,self.eachpnum)
        pass
    def pow(self,n):
        pass
    def indexlength(self,other):
        raise "TBD"
        return pnmod(other.v-self.v) # what?
    def next(self):
        raise "TBD"
    def prev(self):
        raise "TBD"
    def everything(self):
        return self == self.next()

@inv.register(Sopn)
def _(arg ):
    return arg.__invert__(); 

@pow.register(Sopn)
def _(arg,n):
    return arg.pow(n)

@exp.register(Sopn)
def _(arg):
    return self.exp()

@sqrt.register(Sopn)
def _(arg):
    return self.sqrt()



@inv.register(Pnum)
def _(arg ):
    return arg.__invert__(); 

@pow.register(Pnum)
def _(arg,n):
    return arg.pow(n)

@exp.register(Pnum)
def _(arg):
    return self.exp()

@sqrt.register(Pnum)
def _(arg):
    return self.sqrt()

def main():
    pass

if __name__ == '__main__':
    main()