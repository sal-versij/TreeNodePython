import re


class PageHandler:
	prog = re.compile(r"<#\s*(.*?)\s*#>")
	
	def __init__(self, f):
		self.f = f
		self.currentContainer = None
		self.containers = {None: Container()}
		self.inherit = None
		self.backend = None
		self.data = {}
		self.elaborate()
	
	def get_bytes(self):
		pass
	
	def elaborate(self):
		for line in self.f.readlines():
			striped = line.strip()
			match = self.prog.match(striped)
			if match:
				eval(match[1], {'__builtins__': None}, {'self': self})
			else:
				self.handle(striped)
		self.f.close()
	
	def handle(self, v):
		if self.currentContainer in self.containers:
			self.containers[self.currentContainer].handle(v)
		elif self.inherit:
			self.inherit.handle(v)
	
	def header(self, inherit="", backend="", **data):
		self.inherit = PageHandler(open(inherit, 'r'))
		self.backend = backend
		self.data = data
	
	def create_container(self, id):
		self.containers[id] = Container()
		self.handle(self.containers[id])
	
	def container(self, id=None):
		self.currentContainer = id
	
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
	
	def __dict__(self):
		return self.html
	
	def __str__(self):
		return ' '.join(self.html)
