from params import *
import numpy as np
from zq import Zq


polynomial_0 = np.array([2, 0, 0, 1])
polynomial_1 = np.array([2, 0, 0, 0, 1, 1])
polynomial_2 = np.array([3, 0, 0, 0, 1, 1])

pol0 = Zq(n, q, polynomial_0)
pol1 = Zq(n, q, polynomial_1)
pol2 = Zq(n, q, polynomial_2)

print("n:", n)
print("q:", q)
print("k:", k)

print(polynomial_0, ":", pol0)
print(polynomial_1, ":", pol1)
print(polynomial_2, ":", pol2)
print("(", pol1, ") + (", pol2, ") =", pol1 + pol2)
print("(", pol1, ") * (", pol2, ") =", pol1 * pol2)
print("5 * ( ", pol1, ") =", 5 * pol1)
