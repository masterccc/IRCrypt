#!/usr/bin/python3
# -*- coding: utf-8 -*-

from tkinter import * 
from ChatWindow import ChatWindow
import random

# cheatsheet :
#http://apprendre-python.com/page-tkinter-interface-graphique-python-tutoriel

class LoginWindow(object):

	def __init__(self):

		self.server  = "irc.epiknet.org"
		self.port    = "6667"
		self.login   = "Toto" + str(random.randint(1,9999))
		self.channel = "S3cr3tH1de0ut"

		self.win_connexion = Tk()

		self.main_pan = PanedWindow(self.win_connexion, orient=VERTICAL)
		self.main_pan.pack(side=TOP, fill=BOTH, pady=2, padx=2)

		self.connect_items_pan = PanedWindow(self.win_connexion, orient=HORIZONTAL)
		#connect_items_pan.pack(side=TOP, expand=Y, fill=BOTH, pady=2, padx=2)
		self.connect_items_pan.pack(side=TOP, fill=BOTH, pady=2, padx=2)

		self.srv    = self.ui_conf(self.main_pan,"Serveur : ",self.server)
		self.port   = self.ui_conf(self.main_pan,"Port (tcp): ", self.port)
		self.canal  = self.ui_conf(self.main_pan,"Canal : #", self.channel)
		self.pseudo = self.ui_conf(self.main_pan,"Pseudo : ", self.login)

		self.btn_conn=Button(self.main_pan, text="Connexion", command=self.connexion)
		self.btn_conn.pack()

		self.btn_quit=Button(self.main_pan, text="Fermer", command=self.win_connexion.quit)
		self.btn_quit.pack()

		self.main_pan.add(self.btn_conn)
		self.main_pan.add(self.btn_quit)
		self.main_pan.pack()
		self.win_connexion.mainloop()

	def connexion(self):
		print(self.srv.get(),':',self.port.get())
		print(self.pseudo.get() +"@#" + self.canal.get())
		ChatWindow(self.win_connexion, self.srv.get(), self.port.get(), self.canal.get(), self.pseudo.get())

	def ui_conf(self,parent,label_value,default_value):

		srv_pan = PanedWindow(parent, orient=HORIZONTAL)
		srv_label = Label(srv_pan, text='{:15}'.format(label_value))#, bg="white")
		srv_label.pack()

		srv_value = StringVar() 
		srv_value.set(default_value)
		txt_srv = Entry(srv_pan, textvariable=srv_value, width=15)
		txt_srv.pack()

		srv_pan.add(srv_label)
		srv_pan.add(txt_srv)
		srv_pan.pack()

		self.main_pan.add(srv_pan)

		return txt_srv

if __name__ == "__main__":
	login = LoginWindow()
