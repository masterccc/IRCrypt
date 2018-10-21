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
		self.run = True

	# IRC connexion, set nickname, join channel
	def irc_connect(self):
		self.irc = IRCConnection()
		self.irc.on_connect.append(self.on_connect)
		self.irc.on_welcome.append(self.on_welcome)
		#self.irc.on_public_message.append(self.on_message)
		self.irc.on_private_message.append(self.on_private_message)

		self.irc.connect(self.server)
		self.irc.run_loop()

	# À lancer après connexion au serveur
	def on_welcome(self, bot):
		bot.join_channel("#S3cr3tH1de0ut")
	
	# À lancer lors de la connexion au serveur
	def on_connect(self, bot):
	    self.irc.set_nick(self.nick)
	    self.irc.send_user_packet("HelloBot")


	# Les chaînes circulent compressée (zlib) et encodées (base64):
	# Decode et decompresse
	def unformat_zlib_64(self, msg):
		return zlib.decompress(base64.b64decode(msg))

	# Compresse et encode
	def format_zlib_64(self, msg):
		return base64.b64encode(zlib.compress(msg))

	# Reception d'un message privé
	def on_private_message(self, obj, sender, message):
		if( (message[:5] == "!KEY:") and  len(message) > 5):
			
			msg_tab =  message.split(':')
			if(len(msg_tab) == 2 and msg_tab[1] != ''):
				
				# Import friend's RSA key
				pem = self.unformat_zlib_64(message.split(":")[1])
				self.chatbox.push_msg("Received PEM\n")
				self.chatbox.push_msg(pem + "\n")
				self.rsa_manager.import_friend_key(pem)

				# Send pubkey to friend
				self.chatbox.push_msg("Sending PEM ...\n")
				my_pem = self.format_zlib_64(self.rsa_manager.export_key_pem())
				self.irc.send_message(sender, my_pem)


		print("reçu: message:", message, "|sender :", sender)
		self.chatbox.push_msg(sender + " : " + message + "\n")


if __name__ == '__main__':
	print("IRCManager test :")
	irc = IRCManager(None, "irc.freenode.net", 6667, "i4m4n4lbatr05", "Eenius564")
