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
		self.nick        =   pseudo
		self.ident       =   self.botname = self.nick = pseudo
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

	def on_welcome(self, bot):
		bot.join_channel("#S3cr3tH1de0ut")
	
	def on_connect(self, bot):
	    self.irc.set_nick(self.nick)
	    self.irc.send_user_packet("HelloBot")


	def unformat_zlib_64(msg):
		return zlib.decompress(base64.b64decode(msg))

	def format_zlib_64(msg):
		return base64.b64encode(zlib.compress(msg))

	# We receive base64(compress(pem_key))
	def on_private_message(self, bot, channel, sender, message):
		if( (message[:5] == "!KEY:") and  len(message) > 5):
			
			msg_tab =  message.split(':')
			if(len(msg_tab) == 2 and msg_tab[1] != ''):
				
				# Import friend's RSA key
				pem = unformat_zlib_64(message.split(":")[1])
				self.chatbox.push_msg("Received PEM\n")
				self.chatbox.push_msg(pem + "\n")
				self.rsa_manager.import_friend_key(pem)

				# Send pubkey to friend
				self.chatbox.push_msg("Sending PEM ...\n")
				self.irc.send_message(sender, format_zlib_64(self.rsa_manager.export_key_pem()))


		print("reçu: ", message)
		self.chatbox.push_msg(sender + ":" + message + "\n")


if __name__ == '__main__':
	print("IRCManager test :")
	irc = IRCManager(None, "irc.freenode.net", 6667, "i4m4n4lbatr05", "Eenius564")
