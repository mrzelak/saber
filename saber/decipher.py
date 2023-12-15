from params import *

import numpy as np
import utils
import keygen

def log_decrypt(log, cm_p, s_p, v_p,
                pre_mp_p, mp_2):

    if not log: return
    print("LOGGING DECIPHER ON")
    print("cm mod p:\n", cm_p)
    print("s mod p:\n", s_p)
    print("v mod p:\n", v_p)
    print("pre_m' mod p:\n", pre_mp_p)
    print("m' mod 2:\n", mp_2)

def decrypt(ciphertext, secret, log=False):

    s_q = utils.bs2polvec(secret, eq)

    cm_size = n * et // 4
    hex_cm = ciphertext[:cm_size]
    hex_bp = ciphertext[cm_size:]

    cm_t = utils.bs2pol(hex_cm, et)
    bp_p = utils.bs2polvec(hex_bp, ep)

    cm_p = cm_t << (ep - et, p)
    
    s_p = s_q % p

    v_p = bp_p.T @ s_p
    
    h2_q = utils.gen_h2()

    pre_mp_p = v_p - cm_p + h2_q % p
    mp_2 = (pre_mp_p >> (ep - 1)) % 2

    log_decrypt(log, cm_p, s_p, v_p,
                pre_mp_p, mp_2)
    
    return mp_2.polynomial
