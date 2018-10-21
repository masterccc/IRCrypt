#!/usr/bin/python3
# -*- coding: utf-8 -*-

import socket
import base64
import threading
from RsaManager import RsaManager

class IRCManager(object):

	def __init__(self, chatbox_window, server, port, canal, pseudo):

		# Connexion details
		self.server      =   server
		self.port        =   int(port)
		self.nick        =   pseudo
		self.ident       =   self.botname = self.nick = pseudo
		self.channel     =   canal
		self.realname    =   "Real " + self.ident
		self.irc         =   socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.rsa_manager =   RsaManager()
		self.chatbox     =   chatbox_window
		self.run = True

	def close_conn(self):
		self.irc.shutdown(socket.SHUT_RDWR)

	# IRC connexion, set nickname, join channel
	def irc_connect(self):
		self.irc.connect((self.server, self.port))
		listen = threading.Thread(target=self.listener)
		listen.start()
		user_str = "USER " #+ self.nick +" "+ self.nick +" "+ self.nick
		user_str +=  " " + self.nick + " * irc.freenode.net :purple\n" # Je suis pidgin
		self.irc.send(user_str.encode())
		self.irc.send(("NICK "+ self.nick +"\n").encode())
		self.irc.send("NOTICE freenode-connect :.VERSION Purple IRC\n".encode()) # Réponse CTCP
		self.irc.send(("JOIN #"+ self.channel +"\n").encode())
		# /names result automatically send from srv

	# Answer to ping
	def ping(self):
		self.irc.send(":pingis\n".encode())
		print("PONG")

	# Wait for incomming messages
	def listener(self):
		while (self.run):
			rcv = self.irc.recv(2048)
			rcv = rcv.decode("utf-8")
			#print("reçu : ", rcv)
			try:
				if rcv.find("PING :") != -1:
					self.ping()
				elif rcv.find(self.nick + " @ #" + self.channel + " :" + self.nick) != -1 :
					raw_list = rcv.split('\n')[0].split(" :" + self.nick)[1]
					print("pseudales:", raw_list.replace('@','').split())
				else:
					self.chatbox.push_msg(rcv)
			except:
				pass # not a ping

if __name__ == '__main__':
	print("IRCManager test :")
	irc = IRCManager(None, "irc.freenode.net", 6667, "i4m4n4lbatr05", "Eenius564")
