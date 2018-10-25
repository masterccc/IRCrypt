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
		self.irc_mgr = IRCManager(self, self.server, self.port, self.channel, self.pseudo)
		self.helpmsg =  "IRCrypt - End to end encrypted messaging over IRC."
		self.helpmsg += "\nMore informations:"
		self.helpmsg += "\nhttps://github.com/masterccc/IRCrypt\n"
		self.default_contact = "--- Contacts ---"
		parent.destroy()
		self.start()
		listener = threading.Thread(target=self.irc_mgr.irc_connect)
		listener.start()
		listener.join()

	# Thread pour gérer l'interface graphique
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

		# Barre de refresh/choix du correspondant
		
		## Bouton refresh
		self.tool_pan = PanedWindow(self.chat_pan, orient=HORIZONTAL)
		self.btn_refresh=Button(self.tool_pan, text="Refresh names", command=self.irc_mgr.refresh_names)
		self.btn_refresh.pack()
		
		## selection contact
		self.lst_users = Listbox(self.tool_pan, height=1)
		self.lst_users.pack()
		self.lst_users.insert(END, self.default_contact)

		## Bouton select friend
		self.btn_selfriend=Button(self.tool_pan, text="Choose as friend", command=self.ui_choose_friend)
		self.btn_selfriend.pack()

		# Ajout des éléments aus layouts
		self.tool_pan.add(self.btn_refresh)
		self.tool_pan.add(self.lst_users)
		self.tool_pan.add(self.btn_selfriend)
		self.tool_pan.pack()

		self.chat_pan.add(self.tool_pan)
		self.chat_pan.add(self.txt_chat)
		self.chat_pan.add(self.txt_send)
		self.chat_pan.add(self.btn_send)
		self.chat_pan.pack()

		self.print_ban()
		self.win_chat.mainloop()

	def do_exit(self):
		self.irc_mgr.run = False
		self.win_chat.destroy()
		self.irc_mgr.close_conn()
		sys.exit(0)

	# Affiche un message dans la conversation
	def push_msg(self, msg):
		self.txt_chat.insert(INSERT,msg)

	# fenêtre "about"
	def helpbox(self):
		messagebox.showinfo("About", self.helpmsg)

	# Envoie un message depuis le champs texte
	def post_message(self, bind=None):
		_msg = self.txt_send.get("1.0","end-1c").strip()
		self.txt_send.delete("0.0","end")
		if(_msg != ""):
			self.irc_mgr.encrypt_send_msg(_msg)

	# Met à jour la liste de contacts dans l'interface
	def update_contacts(self, new_list):
		self.lst_users.delete(0, END)
		
		if(len(new_list) == 0):
			self.lst_users.insert(END,self.default_contact)
		else:
			for item in new_list:
				self.lst_users.insert(END, item)

	# Selectionne un contact avec qui communiquer
	def ui_choose_friend(self):
		
		ls = self.lst_users.get(0)

		if(len(ls) > 0 and ls != self.default_contact):
			self.irc_mgr.choose_friend(ls)
			print("choosed :", ls)
		else :
			self.push_msg("Impossible d'ajouter cette personne")
			return

	def print_ban(self):
		self.push_msg("Connexion...\n")
		self.push_msg(self.server + ':' + str(self.port) + "\n")
		self.push_msg(self.pseudo +"@#" + self.channel + "\n")

if __name__ == "__main__":
	print("main...")