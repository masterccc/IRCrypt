#!/usr/bin/python3
# -*- coding: utf-8 -*-

import socket
import base64
import threading
from RsaManager import RsaManager
from IrcConnection import IRCConnection
import zlib
import base64


class IRCManager(object):

	def __init__(self, chatbox_window, server, port, canal, pseudo):

		# Connexion details
		self.server      =   server
		self.port        =   int(port)
		self.nick        =   self.ident = self.botname = pseudo
		self.channel     =   canal
		self.realname    =   "Real " + self.ident
		self.irc         =   None
		self.rsa_manager =   RsaManager()
		self.chatbox     =   chatbox_window
		self.friend      =   None
		self.connected   =   []

	# IRC connexion, set nickname, join channel
	def irc_connect(self):
		self.irc = IRCConnection()
		self.irc.on_connect.append(self.on_connect)
		self.irc.on_welcome.append(self.on_welcome)
		self.irc.on_names_received.append(self.rcv_names)
		self.irc.on_notice.append(self.on_notice)
		self.irc.on_private_message.append(self.on_private_message)
		self.irc.connect(self.server)
		self.irc.run_loop()

	def close_conn(self):
		self.irc.socket.shutdown(socket.SHUT_RDWR)


	# À lancer après connexion au serveur
	def on_welcome(self, bot):
		bot.join_channel("#S3cr3tH1de0ut")
	

	# À lancer lors de la connexion au serveur
	def on_connect(self, bot):
	    self.irc.set_nick(self.nick)
	    self.irc.send_user_packet(self.realname)

	def refresh_names(self):
		print("refresh names...")
		self.irc.list_channel(self.channel)

	def rcv_names(self, nicklist):
		print("Reception des pseudos:")
		print(nicklist)
		self.connected = [ ni for ni in nicklist if ni != self.nick ]
		self.chatbox.push_msg("Liste des utilisateurs en ligne :\n")
		self.chatbox.push_msg(",".join(self.connected) + "\n")
		self.chatbox.update_contacts(self.connected)

	def on_notice(self, msg):
		self.chatbox.push_msg(msg + "\n")

	def choose_friend(self,name):

		if(self.friend != None):
			self.chatbox.push_msg("Already bound to friend" + "\n")
			return

		if name not in self.connected:
			print("Friend not in list")
			print("list:", str(self.connected))
			return
		else:
			self.send_key_first(name)

	# Les chaînes circulent compressées (zlib) et encodées (base64):
	# Decode et decompresse
	def unformat_zlib_64(self, msg):
		try:
			return zlib.decompress(base64.b64decode(msg))
		except:
			self.chatbox.push_msg("Error while decoding message")
			return ""

	# Compresse et encode
	def format_zlib_64(self, msg, key=False):
		if(key):
			return base64.b64encode(zlib.compress(msg)).decode("utf-8")
		return base64.b64encode(zlib.compress(msg.encode())).decode("utf-8")
 
	# Amorce l'échange de clés
	def send_key_first(self, friend_name):
		# Send pubkey to friend
		self.chatbox.push_msg("Sending Public Key ...\n")

		msg = "!KEY:"
		my_pem = self.format_zlib_64(self.rsa_manager.export_key_pem())
		
		self.irc.send_message(friend_name, msg + my_pem)
		self.chatbox.push_msg(my_pem + "\n")

	# Reception d'un message privé
	def on_private_message(self, obj, sender, message):

		if( (not self.friend) and (message[:5] == "!KEY:") and  len(message) > 5):
			msg_tab =  message.split(':')
			if(len(msg_tab) == 2 and msg_tab[1] != ''):
				
				# Import friend's RSA key
				try:
					pem = self.unformat_zlib_64(message.split(":")[1]).decode("utf-8")
				except :
					self.chatbox.push_msg("Bad PEM received")
					return

				self.chatbox.push_msg("Received PEM :\n")
				try:
					self.chatbox.push_msg(pem + "\n")
				except:
					print("Clé reçu en bytes, il faut la decoder")
					pem = pem.decode('utf-8')
				

				self.rsa_manager.import_friend_key(pem)
				self.friend = sender
				self.send_key_first(sender)


		elif( self.friend and (message[:5] == "!KEY:")):
			return

		elif(self.rsa_manager.friend_key):
			self.chatbox.push_rcv_msg(self.decrypt_received_msg(message), sender)

		else:
			self.chatbox.push_msg("Unknow data from "+ sender + " : " + message + "\n")

	def decrypt_received_msg(self, message):
		msgdecode= self.unformat_zlib_64(message)
		msg = self.rsa_manager.decrypt_msg(msgdecode)
		return msg

	def encrypt_send_msg(self, message):

		if(not self.rsa_manager.friend_key):
			self.chatbox.push_msg("Aucun contact selectionné\n")
			return
		if(message == ""):
			return

		to_send = self.rsa_manager._encrypt(message)
		ciphercode = self.format_zlib_64(to_send, True)

		self.irc.send_message(self.friend, ciphercode)
		self.chatbox.push_rcv_msg(message, "Moi")

if __name__ == '__main__':
	print("IRCManager test :")
	irc = IRCManager(None, "irc.freenode.net", 6667, "i4m4n4lbatr05", "Eenius564")
