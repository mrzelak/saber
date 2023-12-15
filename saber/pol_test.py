from params import *
import numpy as np
from zq import Zq
from keygen import pol2bs, bs2pol, polvec2bs, bs2polvec

"""
polynomial_0 = np.array([2, 0, 0, 1])
polynomial_1 = np.array([2, 0, 0, 0, 1, 1])
polynomial_2 = np.array([3, 0, 0, 0, 1, 1])

pol0 = Zq(n, q, polynomial_0)
pol1 = Zq(n, q, polynomial_1)
pol2 = Zq(n, q, polynomial_2)

print("n:", n)
print("q:", q)
#print("k:", k)

print(polynomial_0, ":", pol0)
print(polynomial_1, ":", pol1)
print(polynomial_2, ":", pol2)
print("(", pol1, ") + (", pol2, ") =", pol1 + pol2)
print("(", pol1, ") * (", pol2, ") =", pol1 * pol2)
print("5 * ( ", pol1, ") =", 5 * pol1)
"""

pol1 = np.zeros(256)
pol2 = np.ones(256)
pol3 = np.zeros(256)
pol4 = np.ones(256)
pol2[0] = 50
pol1 = Zq(n, q, pol1)
pol2 = Zq(n, q, pol2)
pol3 = Zq(n, q, pol3)
pol4 = Zq(n, q, pol4)
bs1 = pol2bs(pol1, eq)
bs2 = pol2bs(pol2, eq)
#pol1 = bs2pol(bs1, eq)
#pol2 = bs2pol(bs2, eq)
#print(pol1.polynomial)
#print(pol2.polynomial)
v = [pol1, pol2, pol3, pol4]
v = np.array(v)
v_bs = polvec2bs(v, eq)
print(v_bs)
v_pol = bs2polvec(v_bs, eq)
print((v_pol - v)[0].polynomial)
print((v_pol - v)[1].polynomial)
print((v_pol - v)[2].polynomial)
print((v_pol - v)[3].polynomial)
