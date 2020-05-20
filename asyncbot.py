#!/usr/bin/env python
import asyncio
import ssl
import time

import config

def debug(status, msg): print('{0} | [{1}] - {2}'.format(time.strftime('%I:%M:%S'), status, msg))

def ssl_ctx(verify):
	ctx = ssl.create_default_context()
	if verify:
		ctx.check_hostname = True
		ctx.load_default_certs()
	else:
		ctx.verify_mode = ssl.CERT_NONE
		ctx.check_hostname = False
	if config.cert.file:
	    ctx.load_cert_chain(config.cert.file, password=config.cert.password)
	return ctx

class IRC:
	def __init__(self):
		self.options = {
			'host'       : config.connection.server,
			'port'       : config.connection.port,
			'limit'      : 1024,
			'ssl'        : ssl_ctx(config.connection.ssl_verify) if config.connection.ssl else None,
			'family'     : 10 if config.connection.ipv6 else 2,
			'local_addr' : (config.connection.vhost, 0) if config.connection.vhost else None
		}
		self.reader  = None
		self.writer  = None

	def _raw(self, data):
		self.writer.write(data[:510].encode('utf-8') + b'\r\n')

	async def _connect(self):
		try:
			self.reader, self.writer = await asyncio.open_connection(**self.options)
			self._raw(f'USER {config.ident.username} 0 * :{config.ident.realname}')
			self._raw('NICK ' + config.ident.nickname)
		except Exception as ex:
			debug('!', f'Failed to connect to IRC server! ({ex!s})')
		else:
			while not Bot.reader.at_eof():
				try:
					line = await self.reader.readline()
					line = line.decode('utf-8').strip()
					debug('~', line)
					args = line.split()
					if args[0] == 'PING':
						self._raw('PONG ' + args[1][1:])
					elif args[1] == '001': #RPL_WELCOME
						self._raw('MODE ')
				except (UnicodeDecodeError, UnicodeEncodeError):
					pass
				except Exception as ex:
					debug('!', f'Unknown error has occured! ({ex!s})')

	def evemt_connect(self):
		if config.settings.modes:
			Commands.raw(f'MODE {config.ident.nickname} +{config.settings.modes}')
		if config.login.nickserv:
			Commands.sendmsg('NickServ', f'IDENTIFY {config.ident.nickname} {config.login.nickserv}')
		if config.login.operator:
			Commands.raw(f'OPER {config.ident.username} {config.login.operator}')
		Commands.join_channel(config.connection.channel, config.connection.key)

# Start
if __name__ == '__main__':
	Bot = IRC()
	asyncio.run(Bot._connect())
	while True: # Keep-alive loop, since we are asyncronous
		input('')