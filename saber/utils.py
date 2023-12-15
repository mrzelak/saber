from params import *
from zq import Zq

import numpy as np

def gen_h1():
    h1 = np.ones(n)
    h1_q = Zq(n, q, h1)
    a = eq - ep - 1
    coeff = 2 ** a
    # coeff == 4
    h1_q = coeff * h1_q
    return h1_q

def gen_h2():
    h2 = np.ones(n)
    h2_q = Zq(n, q, h2)
    a = ep - 2
    b = ep - et - 1
    c = eq - ep - 1
    coeff  = 0
    coeff += 2 ** a
    coeff -= 2 ** b
    coeff += 2 ** c
    h2_q = coeff * h2_q
    return h2_q

def gen_h():
    h_q = [gen_h1() for _ in range(l)]
    h_q = np.array(h_q)
    return h_q

def is_equal(message, plaintext):
    diff = message - plaintext
    if diff.any():
        return False
    return True

def zfill(length, byte_string):
    padding = "0" * (length * 2 - len(byte_string))
    byte_string = padding + byte_string
    return byte_string

def hamming_weight(chunk):
    return sum(map(lambda bit: int(bit), chunk))

def gen_message(random=True, log=False):

    m = np.random.randint(low=0, high=2, size=n)

    if not random:
        m = np.ones(n)

    if log:
        print("RANDOM MESSAGE", "ON" if random else "OFF")
        print("m:\n", m)

    return m

def bs2pol(bit_string, coeff_size):
    
    # bitstring is already inverted
    bit_string = "".join(list(reversed(bit_string)))

    polynomial = []

    for idx in range(0, len(bit_string), coeff_size):
        chunk = bit_string[idx:idx+coeff_size]
        chunk = "".join(list(reversed(chunk)))
        coeff = int(chunk, 2)
        polynomial.append(coeff)

    polynomial = np.array(polynomial)
    pol_object = Zq(n, q, polynomial)

    return pol_object

def pol2bs(polynomial, coeff_size):

    bit_string = ""
    for coeff in polynomial.polynomial:
        coeff = int(coeff)
        binary = format(coeff, 'b')
        padding = "0" * (coeff_size - len(binary))
        binary = padding + binary
        # append binary to the of of bitstring
        bit_string = binary + bit_string

    return bit_string
        
def bs2polvec(bit_string, coeff_size):

    chunk_size = coeff_size * n

    # bit_string is inverted
    bit_string = "".join(list(reversed(bit_string)))
    vector = []

    for idx in range(0, l * chunk_size, chunk_size):
        chunk = bit_string[idx:idx+chunk_size]
        chunk = "".join(list(reversed(chunk)))
        polynomial = bs2pol(chunk, coeff_size)
        vector.append(polynomial)

    vector = np.array(vector)

    return vector

def polvec2bs(vector, coeff_size):

    bit_string = ""
    for polynomial in vector:
        chunk = pol2bs(polynomial, coeff_size)
        bit_string = chunk + bit_string

    return bit_string
