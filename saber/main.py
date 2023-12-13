from params import *
from keygen import gen_keys
from cipher import encrypt, gen_message
from decipher import decrypt, is_equal

def benchmark(no, deterministic_keys,
              deterministic_msg,
              deterministic_crypt,
              unit_test, debug_msg,
              debug_encrypt, debug_decrypt,
              log_keygen): 

    counter = 0
    for _ in range(no):
        public, secret = gen_keys(deterministic_keys=deterministic_keys, log=log_keygen, unit_test=unit_test)
        message = gen_message(test=deterministic_msg, debug=debug_msg)
        ciphertext = encrypt(message, public, test=deterministic_crypt, debug=debug_encrypt)
        plaintext = decrypt(ciphertext, secret, debug=debug_decrypt)
        if is_equal(message, plaintext):
            counter += 1

    print("passed:", counter / no * 100)

def main():
    no = 100
    unit_test = False
    # keygen
    random_A = True
    random_seed_A = True
    random_s = True
    random_seed_s = True
    log_keygen = False

    deterministic_msg = False
    deterministic_crypt = True
    debug_msg = False
    debug_encrypt = False
    debug_decrypt = False

    deterministic_keys = (
            random_A,
            random_seed_A,
            random_s,
            random_seed_s
            )

    benchmark(no=no,
              deterministic_keys=deterministic_keys,
              deterministic_msg=deterministic_msg,
              deterministic_crypt=deterministic_crypt,
              debug_msg=debug_msg, unit_test=unit_test,
              debug_encrypt=debug_encrypt,
              debug_decrypt=debug_decrypt,
              log_keygen=log_keygen)

main()
