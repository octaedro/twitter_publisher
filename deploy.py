#!/usr/bin/env python
# __author__ = 'FernandoMarichal'
from obj.connection import Connection
from obj.controller import Controller

con = Connection()
con.openCursor()
if con.createTwitterAccountsTable():
    print "Now you should to add files to your twitter accounts table and after that run again this file: (deploy.py)"
con.closeConnection()

mp = Controller()
mp.deploy()