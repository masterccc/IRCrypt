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
		self.menu1.add_separator()
		self.menu1.add_command(label="Aide", command=self.win_chat.quit)
		#self.win_chat.config(menu=self.menubar)

		self.chat_pan = PanedWindow(self.win_chat, orient=VERTICAL)

		#self.value = StringVar() 
		#self.value.set("texte par défaut")
		#self.entree = Entry(self.chat_pan, textvariable=self.value, heigth=5,width=30)
		#self.entree.pack()

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

		
		self.win_chat.mainloop()
		self.connect_msg()

	def connect_msg(self):
		print("exec")
		msg = "Tototo\nlele"
		content = self.txt_chat.get()
		content += "toto"
		self.txt_chat.set(content)
		#self.txt_chat.config(state=NORMAL)
		#self.txt_chat.set(msg)
		#self.txt_chat.config(state=DISABLED)


	def post_message(self):
		print("toto")
	
if __name__ == "__main__":
	print("main...")
