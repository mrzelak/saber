import numpy as np
from params import *
from zq import Zq

def gen_h1():
    h1 = np.ones(n)
    poly_h1_q = Zq(n, q, h1)
    a = eq - ep - 1
    coeff = 2 ** a
    # coeff tutaj wynosi 4
    poly_h1_q = coeff * poly_h1_q
    return poly_h1_q

def gen_h2():
    h2 = np.ones(n)
    poly_h2_q = Zq(n, q, h2)
    a = ep - 2
    b = ep - et - 1
    c = eq - ep - 1
    coeff = 2 ** a - 2 ** b + 2 ** c
    poly_h2_q = coeff * poly_h2_q
    return poly_h2_q

def gen_h():
    h = np.array([gen_h1() for _ in range(l)])
    return h

#def vec_mod(vecpol, new_q):
#    f = lambda polynomial: polynomial.mod(new_q)
#    new_vecpol = list(map(f, vecpol))
#    new_vecpol = np.array(new_vecpol)
#    return new_vecpol
#
#def vec_right_shift(vecpol, shift):
#    f = lambda polynomial: polynomial.right_shift(shift)
#    new_vecpol = list(map(f, vecpol))
#    new_vecpol = np.array(new_vecpol)
#    return new_vecpol
