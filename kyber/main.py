from params import *

import numpy as np
from keygen import keygen
from cipher import cipher_kyber
from decipher import decipher_kyber, clip_polynomial

failed = 0
no = 10000

for _ in range(no):
    private, public, A = keygen(test=False)
    # print("public: ")
    # print(public)
    s, t = private, public

    #m = np.array([1, 1, 0, 1])
    m = np.random.randint(low=0, high=2, size=n)
    u, v = cipher_kyber(A, t, m, test=False)
    # print("u: ")
    # print(u)
    # print("v: ")
    # print(v)

    mn = decipher_kyber(v, s, u)
    # print("mn:")
    # print(mn)
    ans = clip_polynomial(mn)
    # print(ans)
    if any(ans - m):
        failed += 1

print("passed:", 1 - failed / no)

