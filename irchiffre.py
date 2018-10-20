#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Auteur :      Olivier de Casanove
# Descritpion : script permettant un echange de cles sur canal irc
# Date :        20/10/2017  Creation
#
# ======================================================================

import socket
import sys
from time import sleep
from threading import Thread

import re
#from Crypto.PublicKey import RSA
import zlib
    
# ======================================================================


SRVR = "irc.freenode.net"
PORT = 6667
CHANNEL = "teub"
BOTNAME = "Netbot"
NICK = BOTNAME
IDENT = BOTNAME
REALNAME = "Real"+BOTNAME
irc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


class Hautparleur(Thread):
    def __init__(self, name):
        Thread.__init__(self, name=name)

    def run(self):
        msg = irc.recv(1024)
        print(msg.decode('utf-8'))
        sleep(1)
        msg = irc.recv(1024)
        print(msg.decode('utf-8'))

def connexion():
    print("... Connexion a : {}".format(SRVR))
    irc.connect((SRVR, PORT))
    print(irc.recv(2040).decode('utf-8'))
    sleep(1)
    req = "USER {} {} {} :{}\n".format(IDENT, SRVR, NICK, REALNAME)
    irc.send(req.encode())
    sleep(1)
    req = "NICK {}\n".format(NICK)
    irc.send(req.encode())
    sleep(1)
    req = "JOIN {}\n".format(CHANNEL)
    irc.send(req.encode())
    sleep(1)

if __name__ == '__main__':
    hp = Hautparleur("hp")
    connexion()
    hp.start()
    irc.close()
