from cryptography.fernet import Fernet
import sys
import os
import time

def decrypt_file(file):
    with open(file, 'rb') as enc_file:
        encrypted = enc_file.read()
    
    try:
        decrypted = fernet.decrypt(encrypted)
    except:
        print(f'Failed to decrypt {encrypted}')
        return
      
    with open(file, 'wb') as dec_file:
        dec_file.write(decrypted)

def decrypt_file_tree(path):

    if os.path.exists(path):
        if os.path.isfile(path):
            print(f"Decrypting {path}")
            decrypt_file(path)
        elif os.path.isdir(path):
            files = os.listdir(path)
            for file in files:
                decrypt_file_tree(f"{path}/{file}")


start = time.time()
args = sys.argv[1:]
try:
    flag = args.index('-k')
except ValueError:
    flag = -1
if len(args) == 0 or flag == -1 or flag == len(args)-1 or len(args) < 3:
    print("Provide the key file with the -k flag and the files to decrypt")
    exit(0)

if args.count('-k') > 1:
    print("Provide only one key file")
    exit(0)
key_filename = args[flag+1]

with open(key_filename, 'rb') as filekey:
    key = filekey.read()
fernet = Fernet(key)

del args[flag+1]
del args[flag]


for path in args:
    decrypt_file_tree(path)    

end = time.time()
print(f'Time to decrypt: {round(end-start, 3)}')


  
