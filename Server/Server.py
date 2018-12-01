import asyncio
from http.server import BaseHTTPRequestHandler, HTTPServer

from SiteMap import Command, CommandsNamespace, Root

PORT_NUMBER = 8080


def handler(root):
	class H(BaseHTTPRequestHandler):
		def do_GET(self):
			_ = root[self.path]
			if bool(_):
				response = _.get(self)
				if bool(response):
					self.response(*response[0], **response[1])
				else:
					self.server_error()
			else:
				self.not_found()
		
		def do_POST(self):
			_ = root[self.path]
			if bool(_):
				response = _.post(self)
				if bool(response):
					self.response(response)
				else:
					self.server_error()
			else:
				self.not_found()
		
		def response(self, *_, **__):
			self.send_response(200)
			for i in __.keys():
				self.send_header(i, __[i])
			self.end_headers()
			for i in _:
				if hasattr(i, '__call__'):
					_ = i()
					self.wfile.write(_)
				else:
					self.wfile.write(i)
		
		def not_found(self):
			self.send_response(404)
			self.send_header('Content-type', 'text/html')
			self.end_headers()
		
		def server_error(self):
			self.send_response(500)
			self.send_header('Content-type', 'text/html')
			self.end_headers()
	
	return H


async def main():
	commands = CommandsNamespace("main")
	Command.namespaces[commands.name] = commands
	commands['print'] = lambda self: {"a": 1, "b": "2", "c": "d"}
	
	r = Root()
	
	r.load_from_json(r'./sitemap.json')
	
	h = handler(r)
	server = HTTPServer(('', PORT_NUMBER), h)
	try:
		print('Started http server on port ', PORT_NUMBER)
		server.serve_forever()
	except KeyboardInterrupt:
		print('^C received, shutting down the web server')
		server.socket.close()


if __name__ == '__main__':
	loop = asyncio.get_event_loop()
	loop.run_until_complete(main())
	loop.close()
