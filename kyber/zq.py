import numpy as np
import numpy.polynomial.polynomial as pl

class Zq():
    def __init__(self, exp_n, mod_q, polynomial):
        self.mod_q = mod_q
        self.exp_n = exp_n
        divisor = np.array([0 for _ in range(exp_n+1)])
        divisor[0] = 1
        divisor[exp_n] = 1
        quotient, reminder = pl.polydiv(polynomial, divisor)
        self.polynomial = np.mod(reminder, mod_q)
        length = len(self.polynomial)
        for _ in range(exp_n-length):
            self.polynomial = np.append(self.polynomial, 0)
    
    def __add__(self, other):
        return Zq(self.exp_n, self.mod_q, self.polynomial + other.polynomial)
    
    def __mul__(self, other):
        return Zq(self.exp_n, self.mod_q, pl.polymul(self.polynomial, other.polynomial))
    
    def __rmul__(self, other):
        return Zq(self.exp_n, self.mod_q, other * self.polynomial)
    
    def __str__(self):
        s = ""
        for i, num in enumerate(self.polynomial):
            s += str(num) + "x^" + str(i) + " + "
        s = s[:-3]
        return s
    
    def __repr__(self):
        return str(self)
        s = ""
        for i, num in enumerate(self.polynomial):
            s += str(num) + "x^" + str(i) + " + "
        s = s[:-3]
        return s
