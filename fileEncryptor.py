from cryptography.fernet import Fernet
from datetime import datetime
import time
import sys
import os

def encrypt_file(file):
	with open(file, 'rb') as og_file:
		original = og_file.read()
	try:
		encrypted = fernet.encrypt(original)
	except:
		print(f'Failed to encrypt {original}')
	with open(file, 'wb') as encrypted_file:
		encrypted_file.write(encrypted)

def encrypt_file_tree(path):
	if os.path.exists(path):
		if os.path.isfile(path):
			encrypt_file(path)
		elif os.path.isdir(path):
			print(f"Encrypting {path}")
			files = os.listdir(path)
			for file in files:
				encrypt_file_tree(f"{path}/{file}")

start = time.time()
dt = datetime.now()
key_filename = f'key_file_{dt.strftime("%d-%m-%y_%H:%M:%S")}.key'

key = Fernet.generate_key()
with open(key_filename, 'w') as keyfile:
	keyfile.write(key.decode('utf-8'))

fernet = Fernet(key)

for i in range(1, len(sys.argv)):
	encrypt_file_tree(sys.argv[i])
	
end = time.time()
print(f'Time to decrypt: {round(end-start, 3)}')


