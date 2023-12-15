from params import *
from zq import Zq

import utils
import tests
import keygen
import numpy as np

def log_encrypt(log, crypt, sp_q,
                bp_q, bp_p, sp_p,
                vp_p, m_p, cm_t):

    if not log: return

    random_seed_sp, random_sp, random_A = crypt

    print("LOGGING CIPHER ON")
    print("RANDOM SEED_S'", "ON" if random_seed_sp else "OFF")
    print("RANDOM S'"     , "ON" if random_sp      else "OFF")
    print("RANDOM A"      , "ON" if random_A       else "OFF")

    print("s' mod q:\n", sp_q)
    print("b' mod q:\n", bp_q)
    print("b' mod p:\n", bp_p)
    print("s' mod p:\n", sp_p)
    print("v' mod p:\n", vp_p)
    print("m mod p:\n", m_p)
    print("cm mod t:\n", cm_t)

def test_encrypt(unit_test, bp_p, cm_t, bp_q):

    if not unit_test: return

    tests.test_bp_p(bp_p)
    tests.test_cm_t(cm_t)
    tests.test_bp_q(bp_q)

def encrypt(m, public, crypt=False, log=False, unit_test=False):

    random_seed_sp, random_sp, random_A = crypt

    seed_A, pk = public
    seed_A = utils.zfill(seedbytes, seed_A)
    seed_A = bytes.fromhex(seed_A)
    A_q = keygen.gen_A(seed_A, random=random_A, log=log)

    seed_sp = keygen.randombytes(seedbytes, random_seed=random_seed_sp, genfor="s'")
    sp_q = keygen.gen_s(seed_sp, random=random_sp, log=log, party='bob')

    h_q = utils.gen_h()
    bp_q = A_q @ sp_q + h_q

    shifted_q = bp_q >> (eq - ep)
    bp_p = shifted_q % p

    b_p = utils.bs2polvec(pk, ep)
    sp_p = sp_q % p
    vp_p = b_p.T @ sp_p

#   m_p = bs2pol(m, 1)
    m_p = Zq(n, 2, m)
    m_p = m_p << (ep - 1, p)

    h1_q = utils.gen_h1()
    pre_cm_p = vp_p - m_p + h1_q % p
    cm_t = (pre_cm_p >> ep - et) % t

    bit_cm = utils.pol2bs(cm_t, et)
    bit_bp = utils.polvec2bs(bp_p, ep)

    ciphertext = bit_cm + bit_bp

    test_encrypt(unit_test, bp_p, cm_t, bp_q)

    log_encrypt(log, crypt, sp_q,
                bp_q, bp_p, sp_p,
                vp_p, m_p, cm_t)

    return ciphertext
