from params import *
from utils import *
import numpy as np
from zq import Zq
from tests import test_b_q, test_b_p

def gen_A(test=False):
    # TODO: change it to secure generation using SHAKE
    if not test:
        A_q = np.array([
                Zq(n, q, np.random.randint(low=0, high=q, size=n))
                for _ in range(l * l)
        ])
        A_q = A_q.reshape((l, l))
        return A_q

    A_q = [
            [Zq(n, q, [ 1,  2,  3,  4]), Zq(n, q, [ 5,  6,  7,  8])],
            [Zq(n, q, [ 9, 10, 11, 12]), Zq(n, q, [13, 14, 15, 16])],
        ]

    A_q = np.array(A_q)
    return A_q

def gen_s(test=False, party='alice'):
    # TODO: generate using random seed
    if not test:
        s_q = np.array([
            Zq(n, q, np.random.randint(low=0, high=q, size=n))
            for _ in range(l)
            ])
        return s_q

    if party == 'alice':
        s_q = [Zq(n, q, [17, 18, 19, 20]), Zq(n, q, [21, 22, 23, 24])]
        s_q = np.array(s_q)

    elif party == 'bob':
        s_q = [Zq(n, q, [24, 25, 26, 27]), Zq(n, q, [28, 29, 30, 31])]
        s_q = np.array(s_q)

        pol1 = "1627.0x^0 + 1197.0x^1 + 5617.0x^2 + 3638.0x^3"
        pol2 = "1929.0x^0 + 7105.0x^1 + 2798.0x^2 + 4984.0x^3"
        s_q = [Zq(n, q, pol1), Zq(n, q, pol2)]
        s_q = np.array(s_q)
        print(s_q)

    return s_q

def log_keygen(test, debug, A_q, s_q,
               h_q, b_q, b_p):

    if not debug: return
    print("DEBUG KEYGEN ON")
    print("RANDOM KEYGEN", "OFF" if test else "ON")
    print("A mod q:\n", A_q)
    print("s mod q:\n", s_q)
    print("h mod q:\n", h_q)
    print("b mod q:\n", b_q)
    print("b mod p:\n", b_p)

def test_keygen(test, b_q, b_p):

    if not test: return

    test_b_q(b_q)
    test_b_p(b_p)


def gen_keys(test=False, debug=False):
    """
    A[0, 0] * s[0] = 80x^6+136x^5+169x^4+180x^3+106x^2+52x+17      = 180x^3+26x^2-84x-152
    A[1, 0] * s[1] = 288x^6+540x^5+757x^4+940x^3+658x^2+408x+189   = 940x^3+370x^2-132x-568
                                                                   +
                                                                   _________________________
                                                                     1120x^3+396x^2-216x-720 (mod 8192)
                                                                     1120x^3+396x^2+7976x+7472 (inv)
                                                                     7472+7976x+396x^2+1120x^3
                                                                   + 4+4x+4x^2+4x^3
                                                                   _________________________
                                                           TEST      7476+7980x+400x^2+1124x^3
                                                                     ~~~~~~~~~~~~~~~~~~~~~~~~~
                                                                     7476+7980x+400x^2+1124x^3 >> 3
                                                           TEST      934+997x+50x^2+140x^3
                                                                     ~~~~~~~~~~~~~~~~~~~~~
    ________________________________________________________________________________________

    A[0, 1] * s[0] = 160x^6+292x^5+397x^4+476x^3+322x^2+192x+85    = 476x^3+162x^2-100x-312
    A[1, 1] * s[1] = 384x^6+728x^5+1033x^4+1300x^3+922x^2+580x+273 = 1300x^3+538x^2-148x-760
                                                                   +
                                                                   _________________________
                                                                     1776x^3+700x^2-248x-1072 (mod 8192)
                                                                     1776x^3+700x^2+7944x+7120 (inv)
                                                                     7120+7944x+700x^2+1776x^3
                                                                   + 4+4x+4x^2+4x^3
                                                                   _________________________
                                                           TEST      7124+7948x+704x^2+1780x^3
                                                                     ~~~~~~~~~~~~~~~~~~~~~~~~~
                                                                     7124+7948x+704x^2+1780x^3 >> 3
                                                           TEST      890+993x+88x^2+222x^3
                                                                     ~~~~~~~~~~~~~~~~~~~~~
    """
    # TODO: seed_A = randombytes(seed_bytes)
    # TODO: seed_A = shake(seed_A, seed_bytes)
    # TODO: seed_s = randombytes(seed_bytes_noise)
    # TODO: A = gen_A(seed_A)
    # TODO: s = gen_s(seed_s)
    A_q = gen_A(test=test)
    s_q = gen_s(test=test, party='alice')
    h_q = gen_h()

    b_q = A_q.T @ s_q + h_q

    shifted_q = vec_right_shift(b_q, eq - ep)
    b_p = vec_mod(shifted_q, p)
    # after the shift b_p is in p, but you have to change mod_q
    # to be consistent

    public = (A_q, b_p)
    secret = s_q

    log_keygen(test, debug, A_q, s_q,
               h_q, b_q, b_p)

    test_keygen(test, b_q, b_p)

    return public, secret

    # TODO: serialize your keys in given ring
    # TODO: secret_key = polvec2bs(q, s)
    # TODO: pk = polvec2bs(p, b)
    # TODO: public_key = seed_A concat pk
    # TODO: return (public_key, secret_key)
