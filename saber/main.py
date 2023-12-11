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
        public, secret = gen_keys(test=deterministic_keys, debug=debug_keys)
        message = gen_message(test=deterministic_msg, debug=debug_msg)
        ciphertext = encrypt(message, public, test=deterministic_crypt, debug=debug_encrypt)
        plaintext = decrypt(ciphertext, secret, debug=debug_decrypt)
        if is_equal(message, plaintext):
            counter += 1

    print("passed:", counter, "/", no)

def main():
    no = 1
    deterministic_keys = True
    deterministic_msg = True
    deterministic_crypt = True
    debug_keys = True
    debug_msg = True
    debug_encrypt = True
    debug_decrypt = True
    benchmark(no=no,
              deterministic_keys=deterministic_keys,
              deterministic_msg=deterministic_msg,
              deterministic_crypt=deterministic_crypt,
              debug_msg=debug_msg, debug_keys=debug_keys,
              debug_encrypt=debug_encrypt,
              debug_decrypt=debug_decrypt)

main()
