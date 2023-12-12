from params import *
import numpy as np
from utils import *
from keygen import gen_keys
from cipher import gen_message, encrypt

def log_decrypt(debug, cm_p, s_p, v_p,
                pre_m_prim_p, m_prim_2):

    if not debug: return
    print("DEBUG DECIPHER ON")
    print("cm mod p:\n", cm_p)
    print("s mod p:\n", s_p)
    print("v mod p:\n", v_p)
    print("pre_m' mod p:\n", pre_m_prim_p)
    print("m' mod 2:\n", m_prim_2)

def decrypt(ciphertext, secret, debug=False):
    s_q = secret
    cm_t, b_prim_p = ciphertext
    cm_p = cm_t.left_shift(ep - et, p)
    
    s_p = s_q % p

    v_p = b_prim_p.T @ s_p
    
    h2_q = gen_h2()

    pre_m_prim_p = v_p - cm_p + h2_q % p
    m_prim_2 = (pre_m_prim_p >> (ep - 1)) % 2

    log_decrypt(debug, cm_p, s_p, v_p,
                pre_m_prim_p, m_prim_2)
    
    return m_prim_2.polynomial

def is_equal(message, plaintext):
    diff = message - plaintext
    if diff.any():
        return False
    return True

