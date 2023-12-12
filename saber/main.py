from params import *
from keygen import gen_keys
from cipher import encrypt, gen_message
from decipher import decrypt, is_equal

def benchmark(no, deterministic_keys,
              deterministic_msg,
              deterministic_crypt,
              debug_keys, debug_msg,
              debug_encrypt, debug_decrypt): 

    counter = 0
    for _ in range(no):
        public, secret = gen_keys(deterministic_keys=deterministic_keys, debug=debug_keys)
        message = gen_message(test=deterministic_msg, debug=debug_msg)
        ciphertext = encrypt(message, public, test=deterministic_crypt, debug=debug_encrypt)
        plaintext = decrypt(ciphertext, secret, debug=debug_decrypt)
        if is_equal(message, plaintext):
            counter += 1

    print("passed:", counter / no * 100)

def main():
    no = 100
    # keygen
    random_A = True
    random_seed_A = True
    random_s = True
    random_seed_s = True

    deterministic_msg = False
    deterministic_crypt = True
    debug_keys = False
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
              debug_msg=debug_msg, debug_keys=debug_keys,
              debug_encrypt=debug_encrypt,
              debug_decrypt=debug_decrypt)

main()
