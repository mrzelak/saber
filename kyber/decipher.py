from params import *

def decipher_kyber(v, s, u):
    mn = v + (-1) * s.T @ u
    return mn

def clip_polynomial(mn):
    answer = []
    mn = mn[0][0]
    for coeff in mn.polynomial:
        if 5 <= coeff <= 12:
            answer.append(1)
        else:
            answer.append(0)
    return answer
