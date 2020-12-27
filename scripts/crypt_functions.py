from Crypto.Cipher import AES
from Crypto.Util.Padding import pad,unpad
from base64 import b64encode,b64decode

def crypt(password):
	# !!! Chose the right key !!!
	with  open('config/key.bin','rb') as key_file:
		key = key_file.read()
	
	# Create cipher object and encrypt the password
	cipher = AES.new(key, AES.MODE_CBC)
	ciphered_password = cipher.encrypt(pad(password.encode(), AES.block_size))
	iv = cipher.iv
	
	# from bytes to base64 
	ciphered_password = b64encode(ciphered_password).decode()
	iv = b64encode(iv).decode()
	
	return ciphered_password,iv

def decrypt(ciphered_password, iv):
	# !!! Chose the right key !!!
	with  open('config/key.bin','rb') as key_file:
		key = key_file.read()
	
	# from base64 to bytes
	ciphered_password = b64decode(ciphered_password)
	iv = b64decode(iv)

	# Create cipher object and decrypt the password
	cipher = AES.new(key, AES.MODE_CBC,iv)
	original_password = unpad(cipher.decrypt(ciphered_password), AES.block_size)

	return original_password.decode()