from params import *
from utils import *
import numpy as np
from zq import Zq
from tests import test_b_q, test_b_p
import Crypto.Hash.SHAKE128

def gen_A(seed_A, random=False, debug=False):
    if not random:
        A_q = [
                [Zq(n, q, [ 1,  2,  3,  4]), Zq(n, q, [ 5,  6,  7,  8])],
                [Zq(n, q, [ 9, 10, 11, 12]), Zq(n, q, [13, 14, 15, 16])],
            ]

        A_q = np.array(A_q)
        return A_q

    shake = Crypto.Hash.SHAKE128.new(seed_A)
    bit_len = l * l * n * eq
    byte_len = int(bit_len / 8)
    buf_hex = shake.read(byte_len).hex()
    if debug: print(buf_hex)
    num = int(buf_hex, 16)
    rev_bin = "".join(list(reversed(bin(num))))
    rev_bin = rev_bin[:-2]
    padding = "0" * (bit_len - num.bit_length())
    rev_bin = rev_bin + padding
    A_q = []
    k = 0
    for _ in range(l):
        vector = []
        for _ in range(l):
            pol = []
            for j in range(n):
                chunk_str = rev_bin[k:k+ep]
                chunk_dec = int(chunk_str, 2)
                pol.append(chunk_dec)
                k += ep
            pol_object = Zq(n, q, np.array(pol))
            vector.append(pol_object)
        A_q.append(vector)

    A_q = np.array(A_q)
    if debug: print(A_q)
    return A_q

    A_q = np.array([
            Zq(n, q, np.random.randint(low=0, high=q, size=n))
            for _ in range(l * l)
    ])
    A_q = A_q.reshape((l, l))
    return A_q


def hamming_weight(chunk):
    return sum(map(lambda bit: int(bit), chunk))

def gen_s(seed_s, random=False, debug=False, party='alice'):
    if False:
        s_q = np.array([
            Zq(n, q, np.random.randint(low=0, high=q, size=n))
            for _ in range(l)
            ])
        return s_q

    if not random:
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
            #print(s_q)

        return s_q

    buf_len = int(l * n * mu / 8)
    bit_len = buf_len * 8
    shake = Crypto.Hash.SHAKE128.new(seed_s)
    buf_hex = shake.read(buf_len).hex()
    buf_bin = bin(int(buf_hex, 16))
    rev_buf_bin = "".join(list(reversed(buf_bin)))
    rev_buf_bin = rev_buf_bin[:-2]
    padding = "0" * (bit_len - len(rev_buf_bin))
    rev_buf_bin = padding + rev_buf_bin
    s_q = []
    k = 0
    for _ in range(l):
        pol = []
        for j in range(n):
            chunk1 = rev_buf_bin[k:k+mu//2]
            chunk2 = rev_buf_bin[k+1:k+1+mu//2]
            h1 = hamming_weight(chunk1)
            h2 = hamming_weight(chunk2)
            coeff = (h1 - h2) % q
            pol.append(coeff)
            k += 2
        pol_object = Zq(n, q, np.array(pol))
        s_q.append(pol_object)
    s_q = np.array(s_q)

    return s_q


def log_keygen(deterministic_keys, log, A_q, s_q,
               b_q, b_p):

    if not log: return

    random_A, random_seed_A, random_s, random_seed_s = deterministic_keys

    print("LOGGING KEYGEN ON")
    print("RANDOM SEED_A", "ON" if random_seed_A else "OFF")
    print("RANDOM A"     , "ON" if random_A      else "OFF")
    print("RANDOM SEED_S", "ON" if random_seed_s else "OFF")
    print("RANDOM S"     , "ON" if random_s      else "OFF")
    print("A mod q:\n", A_q)
    print("s mod q:\n", s_q)
    print("b mod q:\n", b_q)
    print("b mod p:\n", b_p)

def test_keygen(deterministic_keys, unit_test, b_q, b_p):
    # w sumie teraz to funkcje test sa najbardziej bezutyczne
    # bo testy zostaly napisane dla n=4 i bez SHAKE'a

    if not unit_test: return

    random_A, random_seed_A, random_s, random_seed_s = deterministic_keys

    if random_A: return
    if random_seed_A: return 
    if random_s: return
    if random_seed_s: return

    test_b_q(b_q)
    test_b_p(b_p)

def randombytes(length, random_seed=False, genfor=False):
    if random_seed:
        seed = np.random.default_rng().bytes(length)
        return seed
    if genfor == "A":
        seed = b'1'
    elif genfor == "s":
        seed = b'2'
    elif genfor == "s'":
        seed = b'3'
    return seed

def gen_keys(deterministic_keys=False, log=False, unit_test=False):

    random_A, random_seed_A, random_s, random_seed_s = deterministic_keys

    seed_A = randombytes(seedbytes, random_seed=random_seed_A, genfor='A')
    shake = Crypto.Hash.SHAKE128.new(seed_A)
    seed_A = shake.read(seedbytes)
    seed_s = randombytes(noise_seedbytes, random_seed=random_seed_s, genfor='s')

    A_q = gen_A(seed_A, random=random_A)
    s_q = gen_s(seed_s, random=random_s, party='alice')
    h_q = gen_h()

    b_q = A_q.T @ s_q + h_q

    shifted_q = b_q >> (eq - ep)
    b_p = shifted_q % p

    public = (seed_A, A_q, b_p)
    secret = s_q

    log_keygen(deterministic_keys, log, A_q, s_q, b_q, b_p)

    # allmost useless now
    test_keygen(deterministic_keys, unit_test, b_q, b_p)

    return public, secret

    # TODO: serialize your keys in given ring
    # TODO: secret_key = polvec2bs(q, s)
    # TODO: pk = polvec2bs(p, b)
    # TODO: public_key = seed_A concat pk
    # TODO: return (public_key, secret_key)
