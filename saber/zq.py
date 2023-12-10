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
        # przydaloby sie to przetestowac czy to w ogole jest istotne
        if self.mod_q != other.mod_q:
            raise Exception("different q of poly")

        return Zq(self.exp_n, self.mod_q, self.polynomial + other.polynomial)

    def __sub__(self, other):
        return Zq(self.exp_n, self.mod_q, self.polynomial - other.polynomial)

    def mod(self, new_q):
        return Zq(self.exp_n, new_q, self.polynomial % new_q)

    def right_shift(self, shift):
        #return Zq(self.exp_n, self.mod_q, np.right_shift(self.polynomial.astype(int), shift))
        return Zq(self.exp_n, self.mod_q, self.polynomial.astype(int) >> shift)

    def left_shift(self, shift, new_q):
        # bardzo problematyczny shift. Zwiekszasz liczby, wiec zeby ci clipowalo do starego,
        # zakresu, musisz podac nowy mod_q w ktorym sie znajdzie.
        #return Zq(self.exp_n, self.mod_q, np.right_shift(self.polynomial.astype(int), shift))
        return Zq(self.exp_n, new_q, self.polynomial.astype(int) << shift)

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
