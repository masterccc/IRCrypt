#!/usr/bin/python3
# -*- coding: utf-8 -*-

import Crypto
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from Crypto import Random

class RsaManager(object):

	# Init object and create keys
	def __init__(self):
		self.key        = None
		self.pubkey     = None
		self.friend_key = None
		self.key_size   = 1024
		self.gen_key()

	# Generate public and private keys
	def gen_key(self):
		random_generator = Random.new().read
		self.key = RSA.generate(self.key_size, random_generator)
		self.pubkey = self.key.publickey()

	# Encrypt message with friend's key
	def _encrypt(self,msg):
		cipher = PKCS1_OAEP.new(self.friend_key.publickey())
		ciphertext = cipher.encrypt(msg)
		return ciphertext

	# Export public key (pem format)
	def export_key_pem(self):
		str_key = self.pubkey.exportKey('PEM')
		return str_key

	# Import friend's key (pem format)
	def import_friend_key(self, pem_key_bytes):
		self.friend_key = RSA.importKey(pem_key_bytes)

	# Decrypt friend's message 
	def decrypt_msg(self, ciphertext):
		cipher = PKCS1_OAEP.new(self.key)
		message = cipher.decrypt(ciphertext)
		return message


if __name__ == '__main__':
	
	print("test :")

	# Create entities
	alice = RsaManager()
	bob = RsaManager()

	# Import each other's key
	bob.import_friend_key(alice.export_key_pem())
	alice.import_friend_key(bob.export_key_pem())

	# Print Pem keys
	print("Alice :")
	print(alice.export_key_pem().decode('utf-8'))
	print("Bob :")	
	print(bob.export_key_pem().decode('utf-8'))

	# Alice ---> Bob
	cipher = alice._encrypt("Coucou bob ça roule ?".encode())
	print("Bob dechiffre :")
	msg = bob.decrypt_msg(cipher).decode('utf-8')
	print(msg)

	# Bob ---> Alice
	cipher = bob._encrypt("ça va très bien !".encode())
	print("Alice dechiffre :")
	msg = alice.decrypt_msg(cipher).decode('utf-8')
	print(msg)