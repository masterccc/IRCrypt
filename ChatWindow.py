#!/usr/bin/python3
# -*- coding: utf-8 -*-
 
from tkinter import *
from tkinter import messagebox
from IRCManager import IRCManager
import random
import threading
import sys

class ChatWindow(threading.Thread):

	def __init__(self, parent, server, port, canal, pseudo):

		threading.Thread.__init__(self)

		# Connexion details
		self.server  = server
		self.port    = int(port)
		self.pseudo  = pseudo
		self.channel = canal
		self.IRCManager = IRCManager(self, self.server, self.port, self.pseudo, self.channel)
		self.helpmsg =  "IRCrypt - End to end encrypted messaging over IRC."
		self.helpmsg += "\nMore informations:"
		self.helpmsg += "\nhttps://github.com/masterccc/IRCrypt\n"
		parent.destroy()
		self.start()

		listener = threading.Thread(target=self.IRCManager.irc_connect)
		listener.start()
		listener.join()

	def run(self):
		
		self.win_chat = Tk()

		# Menu
		menubar = Menu(self.win_chat)
		menubar.add_command(label="Quitter", command=self.do_exit)
		menubar.add_command(label="Aide", command=self.helpbox)
		self.win_chat.config(menu=menubar)

		# Layout principal
		self.chat_pan = PanedWindow(self.win_chat, orient=VERTICAL)

		# Conversation
		self.txt_chat = Text(self.chat_pan)
		self.txt_chat.pack()
		self.txt_send = Text(self.chat_pan, height=4)
		self.txt_send.bind("<Return>", self.post_message)
		self.txt_send.pack()
		self.txt_send.focus_set()

		# Bouton envoyer
		self.btn_send=Button(self.win_chat, text="Envoyer", command=self.post_message)
		self.btn_send.pack()

		# Ajout des éléments au layout
		self.chat_pan.add(self.txt_chat)
		self.chat_pan.add(self.txt_send)
		self.chat_pan.add(self.btn_send)
		self.chat_pan.pack()

		self.win_chat.mainloop()

	def do_exit(self):
		self.IRCManager.run = False
		self.win_chat.destroy()
		self.IRCManager.close_conn()
		sys.exit(0)


	# Banniere de connexion
	def connect_msg(self):		
		msg =  "Connexion " + self.server + ":" + str(self.port)
		msg += '\n'+ self.pseudo + '@' + self.channel + '...'
		self.txt_chat.insert(INSERT,msg)

	def push_msg(self, msg):
		self.txt_chat.insert(INSERT,msg)

	def helpbox(self):
		messagebox.showinfo("About", self.helpmsg)

	def post_message(self):
		_msg = self.txt_send.get("1.0","end-1c").strip()
		self.txt_send.delete("0.0","end")
		print("send" + _msg)

if __name__ == "__main__":
	print("main...")
