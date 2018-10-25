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
		self.msg_prefix  =   "m:"
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
		self.irc.shutdown(socket.SHUT_RDWR)
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
			self.send_key_first(self.friend)

	# Les chaînes circulent compressées (zlib) et encodées (base64):
	# Decode et decompresse
	def unformat_zlib_64(self, msg):
		try:
			return zlib.decompress(base64.b64decode(msg))
		except:
			self.chatbox.push_msg("Error while decoding message")
			return ""

	# Convertit en base 64, récupère la chaine correspondante
	def base64_string(self, msg):
		return base64.b64encode(msg).decode('utf-8')

	# Compresse et encode
	def format_zlib_64(self, msg):
		return self.base64_string(zlib.compress(msg))

	# Amorce l'échange de clés
	def send_key_first(self, friend_name):
		# Send pubkey to friend
		self.chatbox.push_msg("Sending PEM ...\n")

		msg = "!KEY:"
		my_pem = self.format_zlib_64(self.rsa_manager.export_key_pem())
		
		self.irc.send_message(self.friend, msg + my_pem)

	# Reception d'un message privé
	def on_private_message(self, obj, sender, message):

		if( (not self.friend) and (message[:5] == "!KEY:") and  len(message) > 5):
			msg_tab =  message.split(':')
			if(len(msg_tab) == 2 and msg_tab[1] != ''):
				
				# Import friend's RSA key
				try:
					pem = self.unformat_zlib_64(message.split(":")[1])
				except :
					self.chatbox.push_msg("Bad PEM received")
					return

				self.chatbox.push_msg("Received PEM\n")
				self.chatbox.push_msg(pem.decode("utf-8") + "\n")
				self.rsa_manager.import_friend_key(pem)
				self.friend = sender
				self.send_key_first(sender)
				self.chatbox.push_msg("renvoie de la clé a " + sender)
		elif(self.rsa_manager.friend_key):
			self.chatbox.push_msg(self.decrypt_received_msg(message))

		self.chatbox.push_msg(sender + " :(cleartext) " + message + "\n")

	def decrypt_received_msg(self, message):
		
		try:
			unc = self.unformat_zlib_64(message)
			return unc
		except:
			return "unformated message received\n"
	

	def encrypt_send_msg(self, message):

		if(not self.rsa_manager.friend_key):
			self.chatbox.push_msg("Aucun contact selectionné\n")
			return
		if(message == ""):
			return
		message = self.msg_prefix + message
		self.rsa_manager._encrypt(message)
		self.irc.send_message(self.friend, self.format_zlib_64(message))

if __name__ == '__main__':
	print("IRCManager test :")
	irc = IRCManager(None, "irc.freenode.net", 6667, "i4m4n4lbatr05", "Eenius564")
