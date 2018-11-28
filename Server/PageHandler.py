import re


class PageHandler:
	prog = re.compile(r"<#\s*(.*?)\s*#>")
	
	def __init__(self, f):
		self.f = f
		self.currentContainer = None
		self.containers = {None: Container()}
		self.inherit = None
		self.backend = None
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
				self.containers[self.currentContainer].handle(striped)
		self.f.close()
	
	def header(self, inherit="", backend=""):
		self.inherit = PageHandler(open(inherit, 'r'))
		self.backend = backend
	
	def container(self, id=None):
		self.currentContainer = id


class Container:
	def __init__(self):
		self.html = []
	
	def handle(self, v):
		self.html.append(v)
	
	def __dict__(self):
		return self.html
	
	def __str__(self):
		return ' '.join(self.html)
