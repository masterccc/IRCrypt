#!/usr/bin/python3
# -*- coding: utf-8 -*-
 
from tkinter import * 
import random

class ChatWindow(object):

	def __init__(self, parent, server, port, canal, pseudo):

		self.server  = server
		self.port    = int(port)
		self.pseudo  = pseudo
		self.channel = canal
		parent.destroy()

		self.win_chat = Tk()

		self.menubar = Menu(self.win_chat)
		self.menu1 = Menu(self.menubar, tearoff=0)
		self.menu1.add_command(label="Quitter", command=self.win_chat.quit)
		#self.menu1.add_separator()
		self.menu1.add_command(label="Aide", command=self.win_chat.quit)
		self.win_chat.config(menu=self.menubar)

		self.chat_pan = PanedWindow(self.win_chat, orient=VERTICAL)

		#txt_chat = Text(chat_pan, height=2, width=30)
		self.txt_chat = Text(self.chat_pan)
		self.txt_chat.pack()
		self.txt_send = Text(self.chat_pan, height=4)
		self.txt_send.pack()

		self.btn_send=Button(self.win_chat, text="Envoyer", command=self.post_message)
		self.btn_send.pack()

		self.chat_pan.add(self.txt_chat)
		self.chat_pan.add(self.txt_send)
		self.chat_pan.add(self.btn_send)
		self.chat_pan.pack()
		#self.win_chat.pack()
		
		self.win_chat.mainloop()

	def post_message(self):
		print("toto")
	
if __name__ == "__main__":
	login = LoginWindow()
