from params import *

import utils
import keygen
import cipher
import decipher

def benchmark(no, random_msg, keys, crypt, 
              log_msg, log_encrypt,
              log_decrypt, log_keys,
              unit_test): 

    counter = 0
    for _ in range(no):
        public, secret = keygen.gen_keys(keys=keys, log=log_keys, unit_test=unit_test)
        message = utils.gen_message(random=random_msg, log=log_msg)
        ciphertext = cipher.encrypt(message, public, crypt=crypt, log=log_encrypt, unit_test=unit_test)
        plaintext = decipher.decrypt(ciphertext, secret, log=log_decrypt)
        if utils.is_equal(message, plaintext):
#           print("message:\n", message)
#           print("plaintext:\n", plaintext.astype(int))
            counter += 1

    print("passed:", counter / no * 100)

def main():

    # general
    no = 1
    unit_test  = False
    random_msg = True

    # keygen
    random_A      = True
    random_seed_A = True
    random_s      = True
    random_seed_s = True

    # encrypt
    random_seed_sp = True
    random_sp      = True

    # logs
    log_msg     = False
    #log_msg     = True
    log_keys    = False
    #log_keys    = True
    log_encrypt = False
    #log_encrypt = True
    log_decrypt = False
    #log_decrypt = True

    keys = (
            random_A,
            random_seed_A,
            random_s,
            random_seed_s
           )

    crypt = (
             random_seed_sp,
             random_sp,
             random_A
            )

    benchmark(no=no,
              keys=keys,
              random_msg=random_msg,
              crypt=crypt,
              log_msg=log_msg, 
              log_encrypt=log_encrypt,
              log_decrypt=log_decrypt,
              log_keys=log_keys,
              unit_test=unit_test)

main()
