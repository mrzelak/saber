from keygen import gen_r, gen_e1, gen_e2
from params import *
from zq import Zq

def error_vector(test=False):
    r = gen_r(test)
    e1 = gen_e1(test)
    e2 = gen_e2(test)
    return r, e1, e2
    
def cipher_kyber(A, t, m, test=False):
    m = Zq(n, q, m)
    r, e1, e2 = error_vector(test)
    u = A.T @ r + e1
    v = t.T @ r + e2 + 9 * m
    return u, v

