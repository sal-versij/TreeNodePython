import asyncio
import collections
import json
import re
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
	types = dict()
	
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
		return _.__rtruediv__(self)
	
	def __str__(self):
		return json.dumps(self, default=lambda o: o.__dict__(), indent=2)
	
	def __dict__(self):
		return {
			"type": self.type,
			"name": self.name,
			"alias": self.alias,
		}
	
	@staticmethod
	def __from_dict__(_):
		if Entry.type == _["type"]:
			return Entry(_["name"], *_["alias"])
		elif _["type"] in Entry.types:
			return Entry.types[_["type"]].__from_dict__(_)
		else:
			raise Exception("Type unrecognized")


class Folder(Entry):
	type = "Folder"
	
	def __init__(self, name, *alias, children=None):
		Entry.__init__(self, name, *alias)
		self.children = children or {}
	
	def retrieve(self, _):
		if _[0] in self.children:
			if len(_) > 1:
				return self.children[_[0]].retrieve(_[1:])
			else:
				return self.children[_[0]]
	
	def children_list(self):
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
	
	def __dict__(self):
		return {
			"type": self.type,
			"name": self.name,
			"alias": self.alias,
			"children": [*self.children_list()],
		}
	
	@staticmethod
	def __from_dict__(_):
		if Folder.type == _["type"]:
			__ = Folder(_["name"], *_["alias"])
			for i in _["children"]:
				j = Entry.__from_dict__(i)
				__.children[j.name] = j
				for k in j.alias:
					__.children[k] = j
			return __
		else:
			return Entry.__from_dict__(_)


class Page(Entry):
	type = "Page"
	prog = re.compile(r"<#(.*?)#>")
	
	def __init__(self, path, name, *alias):
		Entry.__init__(self, name, *alias)
		self.path = path
	
	def request(self, _):
		def func(f=open(self.path, 'r')):
			out = []
			for i in f.readlines():
				_ = i.strip()
				__ = self.prog.match(_)
				eval(__[1])
				out.append()
			f.close()
			return bytes(' '.join(out), 'utf-8')
		
		return [func], {'Content-type': 'text/html; charset=utf-8'}
	
	def __dict__(self):
		return {
			"type": self.type,
			"path": self.path,
			"name": self.name,
			"alias": self.alias,
		}
	
	@staticmethod
	def __from_dict__(_):
		if Page.type == _["type"]:
			return Page(_["path"], _["name"], *_["alias"])
		else:
			return Entry.__from_dict__(_)


class Command(Entry):
	type = "Command"
	namespaces = dict()
	
	def __init__(self, namespace, name, *alias):
		Entry.__init__(self, name, *alias)
		self.namespace = namespace
	
	def request(self, _):
		try:
			return [json.dumps(Command.namespaces[self.namespace][self.name](self)).encode("utf-8")], {
				'Content-type': 'application/json; charset=utf-8'
			}
		except Exception as e:
			print(e)
			return False
	
	def __dict__(self):
		return {
			"type": self.type,
			"namespace": str(self.namespace),
			"name": self.name,
			"alias": self.alias,
		}
	
	@staticmethod
	def __from_dict__(_):
		if Command.type == _["type"]:
			return Command(_["namespace"], _["name"], *_["alias"])
		else:
			return Entry.__from_dict__(_)


class Root(Folder):
	type = "Root"
	
	def __init__(self):
		Folder.__init__(self, "")
	
	def save_to_json(self, fname):
		f = open(fname, 'w')
		f.write(json.dumps(self.__dict__(), default=lambda o: o.__dict__(), indent=2))
		f.flush()
		f.close()
	
	def load_from_json(self, fname):
		f = open(fname, 'r')
		a = json.loads(f.read())
		print(a)
		self.__from_dict__(a, self)
		f.close()
	
	def __dict__(self):
		return {
			"type": self.type,
			"children": [*self.children_list()],
		}
	
	@staticmethod
	def __from_dict__(_, self=None):
		if self is not None:
			for i in _["children"]:
				j = Entry.__from_dict__(i)
				self.children[j.name] = j
				for k in j.alias:
					self.children[k] = j
			return self
		if Root.type == _["type"]:
			__ = Root()
			for i in _["children"]:
				j = Entry.__from_dict__(i)
				__.children[j.name] = j
				for k in j.alias:
					__.children[k] = j
			return __
		else:
			return Entry.__from_dict__(_)


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
	Entry.types[Entry.type] = Entry
	Entry.types[Folder.type] = Folder
	Entry.types[Page.type] = Page
	Entry.types[Command.type] = Command
	Entry.types[Root.type] = Root
	
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
