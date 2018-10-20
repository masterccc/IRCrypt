#!/usr/bin/python3
# -*- coding: utf-8 -*-
 
from tkinter import *
from tkinter import messagebox
import random
import threading

class ChatWindow(object):

	def __init__(self, parent, server, port, canal, pseudo):

		# Connexion details
		self.server  = server
		self.port    = int(port)
		self.pseudo  = pseudo
		self.channel = canal
		self.IRCManager = IRCManager(self.server, self.port, self.pseudo, self.channel)
		self.helpmsg = """
IRCrypt - End to end encrypted messaging over IRC.

More informations:
https://github.com/masterccc/IRCrypt\n
		"""
		parent.destroy()

		self.win_chat = Tk()

		# Menu
		menubar = Menu(self.win_chat)
		menubar.add_command(label="Quitter", command=self.win_chat.quit)
		menubar.add_command(label="Aide", command=self.helpbox)
		self.win_chat.config(menu=menubar)

		# Layout principal
		self.chat_pan = PanedWindow(self.win_chat, orient=VERTICAL)

		# Conversation
		self.txt_chat = Text(self.chat_pan)
		self.txt_chat.pack()
		self.txt_send = Text(self.chat_pan, height=4)
		self.txt_send.pack()

		# Bouton envoyer
		self.btn_send=Button(self.win_chat, text="Envoyer", command=self.post_message)
		self.btn_send.pack()

		# Ajout des éléments au layout
		self.chat_pan.add(self.txt_chat)
		self.chat_pan.add(self.txt_send)
		self.chat_pan.add(self.btn_send)
		self.chat_pan.pack()

		# Démarrage du thread ui ()
		self.ui_thread = threading.Thread(target=self.win_chat.mainloop)
		self.ui_thread.start()
		self.connect_msg()

	# Banniere de connexion
	def connect_msg(self):		
		msg =  "Connexion " + self.server + ":" + str(self.port)
		msg += '\n'+ self.pseudo + '@' + self.channel + '...'
		self.txt_chat.insert(INSERT,msg)

	def helpbox(self):
		messagebox.showinfo("About", self.helpmsg)

	def post_message(self, msg):
		self.IRCManager.post_message(msg)
	
if __name__ == "__main__":
	print("main...")
