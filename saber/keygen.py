from params import *
from zq import Zq

import Crypto.Hash.SHAKE128
import numpy as np
import utils
import tests

def shake_bits(seed, bit_len, log=False):

    byte_len = bit_len // 8
    shake = Crypto.Hash.SHAKE128.new(seed)
    hash_string = shake.read(byte_len).hex()
    hash_hex = int(hash_string, 16)

    # convert hash to binary
    hash_bin = format(hash_hex, 'b')

    # in the specification hash is being inverted
    bit_string = "".join(list(reversed(hash_bin)))
    padding = "0" * (bit_len - hash_hex.bit_length())
    if hash_hex == 0:
        bit_string = "0" * bit_len

    # append padding, but hash is inverted
    bit_string = bit_string + padding

    if log: print("hash_string:\n", hash_string)

    return bit_string

def gen_A(seed_A, random=False, log=False):

    bit_len = l * l * n * eq
    size = ep
    bit_string = shake_bits(seed_A, bit_len, log=log)

    chunks = []

    for idx in range(0, bit_len, size):
        chunk = bit_string[idx:idx+size]
        chunks.append(chunk)

    idx = 0
    A_q = []
    for _ in range(l):
        vector = []
        for _ in range(l):
            polynomial = []
            for _ in range(n):
                chunk = chunks[idx]
                coeff = int(chunk, 2)
                polynomial.append(coeff)
                idx += 1
            polynomial = np.array(polynomial)
            pol_object = Zq(n, q, polynomial)
            vector.append(pol_object)
        A_q.append(vector)

    A_q = np.array(A_q)

    if log: print("A_q:\n", A_q)

    return A_q

def gen_s(seed_s, random=False, log=False, party='alice'):

    bit_len = l * n * mu
    size = mu // 2
    bit_string = shake_bits(seed_s, bit_len, log)

    chunks = []

    for idx in range(0, bit_len, size):
        chunk = bit_string[idx:idx+size]
        chunks.append(chunk)

    s_q = []
    idx = 0
    for _ in range(l):
        polynomial = []
        for _ in range(n):
            chunk1 = chunks[idx]
            chunk2 = chunks[idx+1]
            h1 = int(chunk1, 2).bit_count()
            h2 = int(chunk2, 2).bit_count()
            coeff = (h1 - h2) % q
            polynomial.append(coeff)
            idx += 2
        polynomial = np.array(polynomial)
        pol_object = Zq(n, q, polynomial)
        s_q.append(pol_object)

    s_q = np.array(s_q)

    if log: print("s_q:\n", s_q)

    return s_q

def log_keygen(keys, log, A_q, s_q, b_q, b_p):

    if not log: return

    random_A, random_seed_A, random_s, random_seed_s = keys

    print("LOGGING KEYGEN ON")
    print("RANDOM SEED_A", "ON" if random_seed_A else "OFF")
    print("RANDOM A"     , "ON" if random_A      else "OFF")
    print("RANDOM SEED_S", "ON" if random_seed_s else "OFF")
    print("RANDOM S"     , "ON" if random_s      else "OFF")
    print("A mod q:\n", A_q)
    print("s mod q:\n", s_q)
    print("b mod q:\n", b_q)
    print("b mod p:\n", b_p)

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

def gen_keys(keys=False, log=False, unit_test=False):

    random_A, random_seed_A, random_s, random_seed_s = keys

    seed_A = randombytes(seedbytes, random_seed=random_seed_A, genfor="A")
    shake = Crypto.Hash.SHAKE128.new(seed_A)
    seed_A = shake.read(seedbytes)

    seed_s = randombytes(noise_seedbytes, random_seed=random_seed_s, genfor="s")

    A_q = gen_A(seed_A, random=random_A, log=log)
    s_q = gen_s(seed_s, random=random_s, log=log, party="alice")
    h_q = utils.gen_h()

    b_q = A_q.T @ s_q + h_q

    shifted_q = b_q >> (eq - ep)
    b_p = shifted_q % p

    secret = utils.polvec2bs(s_q, eq)
    pk = utils.polvec2bs(b_p, ep)

    # TODO: public = seed_A + pk
    seed_A = utils.zfill(seedbytes, seed_A.hex())
    public = (seed_A, pk)

    log_keygen(keys, log, A_q, s_q, b_q, b_p)

    # almost useless now
    tests.test_keygen(keys, unit_test, b_q, b_p)

    return public, secret
