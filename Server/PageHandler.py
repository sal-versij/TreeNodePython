import re
from pathlib import Path


class PageHandler:
	prog = re.compile(r"<#\s*(.*?)\s*#\s*/>")
	
	def __init__(self, path):
		self.ok = False
		self.f = None
		self.path = path
		if path and Path(path).exists():
			self.f = open(path, 'r')
		else:
			return
		self.currentContainer = None
		self.containers = {None: Container()}
		self.inherit = None
		self.data = {}
		self.__builtins = {}
		self.elaborate()
		self.ok = True
	
	def get_bytes(self):
		_ = self.inherit and self.inherit.get_bytes() or bytes(str(self.containers[None]), "utf-8")
		return _
	
	def elaborate(self):
		for line in self.f.readlines():
			striped = line.strip()
			match = self.prog.match(striped)
			if match:
				try:
					eval(match[1], {'__builtins__': self.__builtins, 'self': self})
				except Exception as e:
					print(match[1], ": ", e)
			else:
				self.handle(striped)
		self.f.close()
	
	def handle(self, v, cc=None):
		cc = cc or self.currentContainer
		if not self.getcontainer(cc).handle(v):
			self.container()
			return False
		return True
	
	def header(self, inherit=None, **data):
		self.inherit = PageHandler(inherit)
		if self.inherit.ok:
			self.data = self.inherit.data
		else:
			self.inherit = None
		self.data.update(data)
	
	def print(self, f):
		self.handle(Printed(f, self))
	
	def println(self, l=1, **f):
		self.create_container('__temp__', PrintedLine(self, l, **f))
		self.set_container_point('__temp__')
		self.container('__temp__')
	
	def create_container(self, id, e=None):
		self.containers[id] = e or Container()
	
	def set_container_point(self, id):
		self.handle(self.getcontainer(id))
	
	def container(self, id=None):
		self.currentContainer = id
	
	def getcontainer(self, id):
		if id in self.containers:
			return self.containers[id]
		elif self.inherit:
			return self.inherit.getcontainer(id)
	
	def require(self, k):
		if k in __builtins__:
			self.__builtins[k] = __builtins__[k]
			return True
		return False
	
	def __getitem__(self, k):
		if k in self.data:
			return self.data[k]
		else:
			return None


class Container:
	def __init__(self):
		self.html = []
	
	def handle(self, v):
		self.html.append(v)
		return True
	
	def __dict__(self):
		return self.html
	
	def __str__(self):
		return ' '.join(str(i) for i in self.html)


class Printed:
	def __init__(self, _, f):
		self._ = _
		self.f = f
	
	def __str__(self):
		return self.f(self._)


class PrintedLine(Container, Printed):
	def __init__(self, _, l, **f):
		Container.__init__(self)
		Printed.__init__(self, _, f)
		self.l = l
		self.t = 0
	
	def handle(self, v):
		Container.handle(self, v)
		self.t += 1
		return self.t < self.l
	
	def __str__(self):
		return ' '.join(
				str(i).format(**{
					k: (hasattr(v, '__call__') and v(self._) or v)
					for k, v in self.f.items()
				}) for i in self.html)
