#!/usr/bin/env python
# Scroll IRC Art Bot - Developed by acidvegas in Python (https://acid.vegas/scroll)
# config.py

class connection:
	server     = 'irc.supernets.org'
	port       = 6697
	ipv6       = False
	ssl        = True
	ssl_verify = False
	vhost      = None
	channel    = '#dev'
	key        = None

class cert:
	file     = None
	password = None

class ident:
	nickname = 'async'
	username = 'asyncio'
	realname = 'acid.vegas/asyncirc'

class login:
	network  = None
	nickserv = None
	operator = None

class settings:
	admin = 'nick!user@host' # Must be in nick!user@host format (Wildcards accepted)
	modes = None