import asyncio
import collections
import json
from http.server import BaseHTTPRequestHandler, HTTPServer

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
					self.wfile.write(i())
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


class Entry:
	type = "Entry"
	
	def __init__(self, name, *alias):
		self.name = name
		self.alias = alias
	
	def request(self, _):
		return [""], {'Content-type': 'text/html; charset=utf-8'}
	
	def get(self, _):
		return self.request(_)
	
	def post(self, _):
		return self.request(_)
	
	def __truediv__(self, _):
		_.__rtruediv__(self)
		return self
	
	def __str__(self):
		_ = '{'
		_ += '"type":"' + self.type + '",'
		_ += '"name":"' + self.name + '",'
		_ += '"alias":' + str([i for i in self.alias]).replace("'", '"')
		_ += '}'
		return _


class Folder(Entry):
	type = "Folder"
	
	def __init__(self, name, *alias, children=dict()):
		Entry.__init__(self, name, *alias)
		self.children = children
	
	def retrieve(self, _):
		if _[0] in self.children:
			if len(_) > 1:
				return self.children[_[0]].retrieve(_[1:])
			else:
				return self.children[_[0]]
	
	def __children_list(self):
		for i in set([j for j in self.children.values()]):
			yield i
	
	def __rtruediv__(self, _):
		if isinstance(_, collections.Iterable):
			for i in _:
				self.children[i.name] = i
				for j in i.alias:
					self.children[j] = i
		else:
			self.children[_.name] = _
			for i in _.alias:
				self.children[i] = _
		return self
	
	def __getitem__(self, _):
		return self.retrieve(_.split('/')[1:])
	
	def __str__(self):
		_ = '{'
		_ += '"type":"' + self.type + '",'
		_ += '"name":"' + self.name + '",'
		_ += '"alias":' + str([i for i in self.alias]).replace("'", '"') + ','
		_ += '"children":['
		_ += ','.join([str(i) for i in self.__children_list()])
		_ += ']}'
		return _


class Page(Entry):
	type = "Page"
	
	def __init__(self, path, name, *alias):
		Entry.__init__(self, name, *alias)
		self.path = path
	
	def request(self, _):
		def func(f=open(self.path, 'r')):
			out = f.read()
			f.close()
			return bytes(out, 'utf-8')
		
		return [func], {'Content-type': 'text/html; charset=utf-8'}
	
	def __str__(self):
		_ = '{'
		_ += '"type":"' + self.type + '",'
		_ += '"path":"' + self.path + '",'
		_ += '"name":"' + self.name + '",'
		_ += '"alias":' + str([i for i in self.alias]).replace("'", '"')
		_ += '}'
		return _


class Command(Entry):
	type = "Command"
	
	def __init__(self, namespace, name, *alias):
		Entry.__init__(self, name, *alias)
		self.namespace = namespace
	
	def request(self, _):
		try:
			return [json.dumps(self.namespace[self.name](self)).encode("utf-8")], {
				'Content-type': 'application/json; charset=utf-8'
			}
		except Exception as e:
			print(e)
			return False
	
	def __str__(self):
		_ = '{'
		_ += '"type":"' + self.type + '",'
		_ += '"namespace":"' + str(self.namespace) + '",'
		_ += '"name":"' + self.name + '",'
		_ += '"alias":' + str([i for i in self.alias]).replace("'", '"')
		_ += '}'
		return _


class Root(Folder):
	type = "Root"
	
	def __init__(self, commands={}):
		Folder.__init__(self, "")
		self.commands = commands
	
	def save_to_json(self, fname):
		f = open(fname, 'w')
		f.write(str(self))
	
	def load_from_json(self, fname):
		f = open(fname, 'r')
		a = json.loads(f.read())
		print(a)


class CommandsNamespace:
	def __init__(self, name):
		self.name = name
		self.__commands = {}
	
	def __str__(self):
		return self.name
	
	def __getitem__(self, i):
		return self.__commands[i]
	
	def __setitem__(self, k, v):
		self.__commands[k] = v


async def main():
	r = Root()
	
	commands = CommandsNamespace("main")
	commands['print'] = lambda self: print('meow')
	root = Root(commands)
	
	p1 = Page('./index.html', 'index', 'home', '')
	p2 = Page('./main.html', 'main')
	c1 = Command(commands, 'print')
	f1 = Folder("a")
	(p2 / f1, p1, c1) / root
	
	root.save_to_json(r'./paths.json')
	
	h = handler(root)
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
