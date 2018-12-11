import collections
import json
import mimetypes
import os
import subprocess

from PageHandler import PageHandler as ph


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
		return None
	
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
		_ = _.replace('\\', '/').split('/')
		if len(_) > 1:
			return self.retrieve(_[1:])
		return None
	
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
	
	def __init__(self, path, name, *alias):
		Entry.__init__(self, name, *alias)
		self.path = path
	
	def request(self, _):
		return [lambda: ph(self.path).get_bytes()], {'Content-type': 'text/html; charset=utf-8'}
	
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


class SCSS(Entry):
	type = "SCSS"
	
	def __init__(self, path, name, dist="./dist/"):
		Entry.__init__(self, name)
		self.path = path
		self.dist = dist and dist or self.dist
		subprocess.call(["cmd", "/d", "/c", "sass", f"{self.get_path()}:{self.get_dist()}"])
	
	def get_path(self):
		return os.path.abspath(self.path)
	
	def get_dist(self):
		return os.path.abspath(os.path.join(self.dist, self.name))
	
	def request(self, _):
		return [lambda: ph(self.get_path()).get_bytes()], {'Content-type': 'text/css; charset=utf-8'}
	
	def __dict__(self):
		return {
			"type": self.type,
			"path": self.path,
			"name": self.name,
			"dist": self.dist,
		}
	
	@staticmethod
	def __from_dict__(_):
		if SCSS.type == _["type"]:
			return SCSS(_["path"], _["name"], _["dist"])
		else:
			return Entry.__from_dict__(_)


class Resource(Entry):
	type = "Resource"
	
	def __init__(self, path, name):
		Entry.__init__(self, name)
		self.path = path
		self.mime = mimetypes.MimeTypes().guess_type(self.path)
		self.mime = self.mime[0]
	
	def request(self, _):
		return [lambda: bytes(open(self.path).read(), 'utf-8')], {'Content-type': '{}; charset=utf-8'.format(self.mime)}
	
	def __dict__(self):
		return {
			"type": self.type,
			"path": self.path,
			"name": self.name,
		}
	
	@staticmethod
	def __from_dict__(_):
		if Resource.type == _["type"]:
			return Resource(_["path"], _["name"])
		else:
			return Entry.__from_dict__(_)


class ResourceFolder(Folder):
	type = "ResourceFolder"
	
	def __init__(self, name, path):
		Entry.__init__(self, name)
		self.children = {}
		self.path = path
		l = len(self.path)
		for sd, ds, fs in os.walk(self.path):
			print(sd, ds, fs)
			_sd = sd[l:]
			for d in ds:
				Folder(d) / (self[_sd] or self)
			for f in fs:
				Resource(r"{}\{}".format(sd, f), f) / (self[_sd] or self)
	
	def __dict__(self):
		return {
			"type": self.type,
			"name": self.name,
			"path": self.path,
		}
	
	@staticmethod
	def __from_dict__(_):
		if ResourceFolder.type == _["type"]:
			return ResourceFolder(_["name"], _["path"])
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


Entry.types[Entry.type] = Entry
Entry.types[Folder.type] = Folder
Entry.types[Page.type] = Page
Entry.types[Command.type] = Command
Entry.types[Root.type] = Root
Entry.types[SCSS.type] = SCSS
Entry.types[Resource.type] = Resource
Entry.types[ResourceFolder.type] = ResourceFolder
