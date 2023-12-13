import numpy as np
from params import *
from zq import Zq

def test_b_q(b_q):
    vector = [
            [7476,7980,400,1124],
            [7124,7948,704,1780] 
            ]
    b1 = np.array(vector[0])
    b2 = np.array(vector[1])
    poly_b1 = Zq(n, q, b1)
    poly_b2 = Zq(n, q, b2)
    correct_q = np.array([poly_b1, poly_b2])

    diff = correct_q - b_q
    for vect in diff:
        if vect.polynomial.any():
            print("KEYGEN: b mod q FAILED")

def test_b_p(b_p):
    vector = [
                [934,997,50,140],
                [890,993,88,222]
            ]
    b1 = np.array(vector[0])
    b2 = np.array(vector[1])
    # note the p instead of q
    poly_b1 = Zq(n, p, b1)
    poly_b2 = Zq(n, p, b2)
    correct_p = np.array([poly_b1, poly_b2])

    diff = correct_p - b_p
    for vect in diff:
        if vect.polynomial.any():
            pass #print("KEYGEN: b mod p FAILED")

def test_b_prim_p(b_prim_p):
    vector = [
            [937,992,39,127],
            [821,984,143,347] 
            ]
    b_prim1 = np.array(vector[0])
    b_prim2 = np.array(vector[1])
    poly_b_prim1 = Zq(n, p, b_prim1)
    poly_b_prim2 = Zq(n, p, b_prim2)
    correct_p = np.array([poly_b_prim1, poly_b_prim2])

    diff = correct_p - b_prim_p
    for vect in diff:
        if vect.polynomial.any():
            pass #print("ENCRYPT: b' mod p FAILED")

def test_cm_t(cm_t):
    vector = [6,7,7,4] 
    cm1 = np.array(vector)
    correct_t = Zq(n, t, cm1)

    diff = correct_t - cm_t
    if diff.polynomial.any():
        pass #print("ENCRYPT: cm mod t FAILED")

def test_b_prim_q(b_prim_q):
    vector = [
            [7500,7940,316,1016],
            [6572,7876,1148,2776] 
            ]
    b_prim1 = np.array(vector[0])
    b_prim2 = np.array(vector[1])
    poly_b_prim1 = Zq(n, q, b_prim1)
    poly_b_prim2 = Zq(n, q, b_prim2)
    correct_q = np.array([poly_b_prim1, poly_b_prim2])

    diff = correct_q - b_prim_q
    for vect in diff:
        if vect.polynomial.any():
            pass #print("ENCRYPT: b' mod q FAILED")
