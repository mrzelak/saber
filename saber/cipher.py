from params import *
from utils import *
import numpy as np
from keygen import gen_keys, gen_s

# TODO: change passing matrix A into passing seed_A
def gen_message(test=False):
    if test:
        #m = np.ones(n)
        #m = np.zeros(n)
        #m = np.array([0, 0, 0, 0])
        #m = np.array([0, 0, 0, 1])
        #m = np.array([0, 0, 1, 0])
        #m = np.array([0, 0, 1, 1])
        #m = np.array([0, 1, 0, 0])
        #m = np.array([0, 1, 0, 1])
        #m = np.array([0, 1, 1, 0])
        #m = np.array([0, 1, 1, 1])
        #m = np.array([1, 0, 0, 0])
        #m = np.array([1, 0, 0, 1])
        #m = np.array([1, 0, 1, 0])
        #m = np.array([1, 0, 1, 1])
        #m = np.array([1, 1, 0, 0])
        #m = np.array([1, 1, 0, 1])
        #m = np.array([1, 1, 1, 0])
        #m = np.array([1, 1, 1, 1])
        return m
    # here 256 is ok, later we will convert m to polynomial
    # so it has to have length of the polynomial representation
    m = np.random.randint(low=0, high=2, size=n)
    return m

def encrypt(m, public, test=False, debug=False):
    # TODO: seed_A instead of A
    # TODO: A = gen_A(seed_A)

    A_q, b_p = public
    s_prim_q = gen_s(test=test, party='bob')
    h_q = gen_h()
    b_prim_q = A_q @ s_prim_q + h_q

    f = lambda polynomial: polynomial.right_shift(eq - ep)
    b_prim_q = list(map(f, b_prim_q))
    b_prim_q = np.array(b_prim_q)
    # now b_prim is in p

    s_prim_p = vec_mod(s_prim_q, p)
    #f = lambda polynomial: polynomial.mod(p)
    #s_prim_p = list(map(f, s_prim_q))
    #s_prim_p = np.array(s_prim_p)

    #v_prim = np.array([b]) @ s_prim_p
    v_prim_p = b_p.reshape((2, 1)).T @ s_prim_p
    v_prim_p = v_prim_p[0]
    # now v_prim is in p
    m_p = Zq(n, 2, m)
    m_p = m_p.left_shift(ep - 1, p)
    # i think that m_p is now in p
    h1_q = gen_h1()
    pre_cm_p = v_prim_p - m_p.mod(p) + h1_q.mod(p)
    cm_t = pre_cm_p.right_shift(ep - et).mod(t)
    # now cm is in t

    # this can go earlier to be more consistent
    b_prim_p = vec_mod(b_prim_q, p)
    #f = lambda poly: poly.mod(p)
    #b_prim_p = list(map(f, b_prim_q))
    #b_prim_p = np.array(b_prim_p)
    if debug:
        print("v':")
        print(v_prim_p)
        print("s'_q:")
        print(s_prim_q)
        print("cm:\n", cm_t)
        print("b':\n", b_prim_p)

    if test:
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
                print("ENCRYPT: B' FAILED")

        vector = [6,7,7,4] 
        cm1 = np.array(vector)
        correct_t = Zq(n, t, cm1)

        diff = correct_t - cm_t
        if diff.polynomial.any():
            print("ENCRYPT: CM FAILED")

    ciphertext = cm_t, b_prim_p
    return ciphertext
