import re


class PageHandler:
	prog = re.compile(r"<#\s*(.*?)\s*#>")
	
	def __init__(self, f):
		self.f = f
		self.currentContainer = None
		self.containers = {None: Container()}
		self.inherit = None
		self.data = {}
		self.elaborate()
	
	def get_bytes(self):
		_ = self.inherit and self.inherit.get_bytes() or bytes(str(self.containers[None]), "utf-8")
		return _
	
	def elaborate(self):
		for line in self.f.readlines():
			striped = line.strip()
			match = self.prog.match(striped)
			if match:
				eval(match[1], {'__builtins__': None}, {'self': self})
			else:
				self.handle(striped)
		self.f.close()
	
	def handle(self, v, cc=None):
		cc = cc or self.currentContainer
		if cc in self.containers:
			self.containers[cc].handle(v)
		elif self.inherit:
			self.inherit.handle(v, cc)
	
	def header(self, inherit=None, **data):
		try:
			self.inherit = PageHandler(open(inherit, 'r'))
			self.data = self.inherit.data
		except:
			pass
		self.data.update(data)
	
	def print(self, f):
		self.handle(Printed(f, self))
	
	def create_container(self, id):
		self.containers[id] = Container()
	
	def set_container_point(self, id):
		self.handle(self.containers[id])
	
	def container(self, id=None):
		self.currentContainer = id
	
	def __getitem__(self, k):
		if k in self.data:
			return self.data[k]
		else:
			return None


class Printed:
	def __init__(self, f, _):
		self.f = f
		self._ = _
	
	def __str__(self):
		return self.f(self._)


class Container:
	def __init__(self):
		self.html = []
	
	def handle(self, v):
		self.html.append(v)
	
	def __dict__(self):
		return self.html
	
	def __str__(self):
		return ' '.join(str(i) for i in self.html)
