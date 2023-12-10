from params import *
import numpy as np
from utils import *
from keygen import gen_keys
from cipher import gen_message, encrypt

def decrypt(ciphertext, secret, test=False):
    s_q = secret
    cm_t, b_prim_p = ciphertext
    cm_p = cm_t.left_shift(ep - et, p)
    
    s_p = vec_mod(s_q, p)
    #f = lambda poly: poly.mod(p)
    #s_p = list(map(f, s_q))
    #s_p = np.array(s_p)

    v_p = b_prim_p.reshape((2, 1)).T @ s_p
    v_p = v_p[0]
    
    h2_q = gen_h2()

    pre_m_prim_p = v_p - cm_p + h2_q.mod(p)
    m_prim_2 = pre_m_prim_p.right_shift(ep - 1)
    # now m_prim_2 should be in R2

    return m_prim_2.polynomial

def compare(m, plaintext):
    diff = message - plaintext
    if diff.any():
        return True
        print("DECRYPTION FAILED")
        print("message:\n", message)
        print("plaintext:\n", plaintext)
    else:
        return False
        print("message:\n", message)
        print("plaintext:\n", plaintext)
        print("DECRYPTION PASSED")

no =1000
counter = 0
for _ in range(no):
    public, secret = gen_keys(test=deterministic_test)
    message = gen_message(test=deterministic_test)
    ciphertext = encrypt(message, public, test=deterministic_test)
    plaintext = decrypt(ciphertext, secret, test=deterministic_test)
    if compare(message, plaintext):
        counter += 1

print("passed:", 1 - counter/ no)

