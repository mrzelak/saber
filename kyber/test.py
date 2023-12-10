from params import *
import numpy as np
from keygen import keygen
from cipher import cipher_kyber
from decipher import decipher_kyber, clip_polynomial

private, public, A = keygen(test=True)
print("A:")
print(A)
print("public key:")
print(public)
s, t = private, public
m = np.array([1, 1, 0, 1])
u, v = cipher_kyber(A, t, m, test=True)

print("u:")
print(u)
print("v:")
print(v)

mn = decipher_kyber(v, s, u)
print("deciphered message:")
print(mn)
ans = clip_polynomial(mn)
print("clipped message:")
print(ans)

print("correct answers")
