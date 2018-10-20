import Crypto
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from Crypto import Random
import ast


class RsaManager(object):

	def __init__(self):

		self.key        = None
		self.pubkey     = None
		self.friend_key = None
		self.key_size   = 1024
		self.gen_key()

	def gen_key(self):
		random_generator = Random.new().read
		self.key = RSA.generate(self.key_size, random_generator)
		self.pubkey = self.key.publickey()

	def _encrypt(self,msg):
		cipher = PKCS1_OAEP.new(self.friend_key.publickey())
		ciphertext = cipher.encrypt(msg)
		return ciphertext

	def export_key_pem(self):
		str_key = self.pubkey.exportKey('PEM')
		return str_key

	def import_friend_key(self, pem_key_bytes):
		self.friend_key = RSA.importKey(pem_key_bytes)

	def decrypt_msg(self, ciphertext):
		cipher = PKCS1_OAEP.new(self.key)
		message = cipher.decrypt(ciphertext)
		return message


if __name__ == '__main__':
	
	print("test :")

	alice = RsaManager()
	bob = RsaManager()

	bob.import_friend_key(alice.export_key_pem())
	alice.import_friend_key(bob.export_key_pem())

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