from params import *
from zq import Zq

import numpy as np

def gen_h1():
    h1 = np.ones(n)
    h1_q = Zq(n, q, h1)
    a = eq - ep - 1
    coeff = 2 ** a
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

def hamming_weight(chunk):
    return sum(map(lambda bit: int(bit), chunk))

def randombytes(length, random_seed=False, genfor=False):

    seed = np.random.default_rng().bytes(length)

    if not random_seed:
        if genfor == "A":
            seed = b"1"
        elif genfor == "s":
            seed = b"2"
        elif genfor == "s'":
            seed = b"3"

    return seed

def gen_message(random=True, log=False):

    m = np.random.randint(low=0, high=2, size=n)

    if not random:
        m = np.ones(n)

    if log:
        print("RANDOM MESSAGE", "ON" if random else "OFF")
        print("m:\n", m)

    return m

def bs2pol(byte_string, coeff_size, bitstring=False):
    
    if not bitstring:
        bit_string = format(int(byte_string, 16), 'b')
        bit_string = bit_string.zfill(n * coeff_size)
    else:
        bit_string = byte_string
    
    # bit_string is already inverted
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

def pol2bs(polynomial, coeff_size, bitstring=False):

    bit_string = ""
    for coeff in polynomial.polynomial:
        binary = format(int(coeff), 'b')
        binary = binary.zfill(coeff_size)
        # append binary to the of of bitstring
        bit_string = binary + bit_string

    if bitstring: return bit_string
    byte_string = format(int(bit_string, 2), 'x')
    hex_len = n * coeff_size // 4
    byte_string = byte_string.zfill(hex_len)
    return byte_string

def bs2polvec(byte_string, coeff_size, bitstring=False):

    chunk_size = coeff_size * n
    if not bitstring:
        vector_size = l * chunk_size

        bit_string = format(int(byte_string, 16), 'b')
        bit_string = bit_string.zfill(vector_size)
    else:
        bit_string = byte_string

    # bit_string is inverted
    bit_string = "".join(list(reversed(bit_string)))
    vector = []

    for idx in range(0, l * chunk_size, chunk_size):
        chunk = bit_string[idx:idx+chunk_size]
        chunk = "".join(list(reversed(chunk)))
        polynomial = bs2pol(chunk, coeff_size, bitstring=True)
        vector.append(polynomial)

    vector = np.array(vector)

    return vector

def polvec2bs(vector, coeff_size, bitstring=False):

    bit_string = ""
    for polynomial in vector:
        chunk = pol2bs(polynomial, coeff_size, bitstring=True)
        bit_string = chunk + bit_string

    if bitstring: return bit_string

    byte_string = format(int(bit_string, 2), 'x')
    hex_len = l * n * coeff_size // 4
    byte_string = byte_string.zfill(hex_len)

    return byte_string

def debug_vector(vector_ref, vector_test):
    out  = vector_ref - vector_test
    dot = out.T @ out
    print("debug:\n", dot.polynomial)

def debug_A(A_ref, A_test):
    test_vec = [Zq(n, q, np.ones(256)) for _ in range(l)]
    test_vec = np.array(test_vec)
    out = (A_ref - A_test) @ test_vec
    dot = out.T @ out
    # if anything non zero then the difference is nonzero
    print(dot.polynomial)

