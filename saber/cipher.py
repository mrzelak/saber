from params import *
from utils import *
import numpy as np
from keygen import gen_keys, gen_s
from tests import test_b_prim_p, test_cm_t, test_b_prim_q

# TODO: change passing matrix A into passing seed_A
def gen_message(test=False, debug=False):
    # here 256 is ok, later we will convert m to polynomial
    # so it has to have length of the polynomial representation
    m = np.random.randint(low=0, high=2, size=n)
    if test:
        m = np.ones(n)
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
        if debug:
            print("RANDOM MESSAGE", "OFF" if test else "ON")
            print("m:\n", m)
        return m
    if debug:
        print("RANDOM MESSAGE", "OFF" if test else "ON")
        print("m:\n", m)
    return m

def log_encrypt(test, debug, s_prim_q,
                b_prim_q, b_prim_p,
                s_prim_p, v_prim_p,
                m_p, cm_t):

    if not debug: return
    print("CIPHER DEBUG ON")
    print("RANDOM ENCRYPT", "OFF" if test else "ON")
    print("s' mod q:\n", s_prim_q)
    print("b' mod q:\n", b_prim_q)
    print("b' mod p:\n", b_prim_p)
    print("s' mod p:\n", s_prim_p)
    print("v' mod p:\n", v_prim_p)
    print("m mod p:\n", m_p)
    print("cm mod t:\n", cm_t)

def test_encrypt(test, b_prim_p, cm_t,
                 b_prim_q):

    if not test: return

    test_b_prim_p(b_prim_p)
    test_cm_t(cm_t)
    test_b_prim_q(b_prim_q)

def encrypt(m, public, test=False, debug=False):
    # TODO: seed_A instead of A
    # TODO: A = gen_A(seed_A)

    A_q, b_p = public
    s_prim_q = gen_s(test=test, party='bob')
    h_q = gen_h()
    b_prim_q = A_q @ s_prim_q + h_q

    shifted_q = vec_right_shift(b_prim_q, eq - ep)
    b_prim_p = vec_mod(shifted_q, p)

    s_prim_p = vec_mod(s_prim_q, p)
    v_prim_p = b_p.T @ s_prim_p

    m_p = Zq(n, 2, m)
    m_p = m_p.left_shift(ep - 1, p)

    h1_q = gen_h1()
    pre_cm_p = v_prim_p - m_p + h1_q.mod(p)
    cm_t = pre_cm_p.right_shift(ep - et).mod(t)

    ciphertext = cm_t, b_prim_p

    test_encrypt(test, b_prim_p, cm_t,
                 b_prim_q)

    log_encrypt(test, debug, s_prim_q,
                b_prim_q, b_prim_p,
                s_prim_p, v_prim_p,
                m_p, cm_t)

    return ciphertext
