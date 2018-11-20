import numpy as np
from pyrr import vector3 as v3, vector4 as v4, matrix33 as m33,matrix44 as m44,quaternion as q,ray,utils as u
import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *

class Object:
	def __init__(self):
		self.vs=np.array([])
		self.fs=np.array([])
	def render(self):
		for f in self.fs:
			f.render(self.vs)
	def __add__(self,_):
		if type(_) == list:
			if len(_)>0:
				if type(_[0]) == Face:
					self.fs = np.append(self.fs,_)
				elif type(_[0]) == Vertex:
					self.vs = np.append(self.vs,_)
				else:
					return _.__radd__(self)
			else:
				return _.__radd__(self)
		elif type(_) == Face:
			self.fs = np.append(self.fs,_)
		elif type(_) == Vertex:
			self.vs = np.append(self.vs,_)
		else:
			return _.__radd__(self)
		return self
#

class Face:
	def __init__(self,vs=np.array([],dtype='int8')):
		self.f = vs
	def render(self,vs):
		glBegin(GL_POLYGON)
		for i in self.f:
			vs[i].render()
		glEnd()
	def __add__(self,_):
		if type(_) == list:
			if len(_)>0:
				if type(_[0]) == int:
					self.f = np.append(self.f,_)
				else:
					return _.__radd__(self)
			else:
				return _.__radd__(self)
		elif type(_) == int:
			self.f = np.append(self.f,_)
		else:
			return _.__radd__(self)
		return self
#

class Vertex:
	def __init__(self,v=np.array([0,0,0],dtype='float'),c=np.array([1,1,1,1],dtype='float')):
		self.x,self.y,self.z = v
		self.r,self.g,self.b,self.a = c
	def render(self):
		glColor4fv(self.color)
		glVertex3fv(self.pos)
	@property
	def pos(self):
		return np.array([self.x,self.y,self.z],dtype='float')
	@pos.setter
	def pos(self,_):
		self.x,self.y,self.z = _
	@property
	def color(self):
		return np.array([self.r,self.g,self.b,self.a],dtype='float')
	@color.setter
	def color(self,_):
		self.r,self.g,self.b,self.a = c
#

objects = [
	Object()+(Face()+[0,1,2,3])+[Vertex([0,1,0])]+[Vertex([1,1,0])]+[Vertex([1,0,0])]+[Vertex([0,0,0])]
]

def display(size):
	glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
	
	glMatrixMode(GL_PROJECTION)
	glLoadIdentity()
	glOrtho( 0, 1, 0, 1, 0, 1)
	glMatrixMode(GL_MODELVIEW)
	glLoadIdentity()
	
	for o in objects:
		o.render()
#

def main():
	pygame.init()
	size = (800,600)
	pygame.display.set_mode(size, DOUBLEBUF|OPENGL)

	while True:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				quit()
		display(size)
		pygame.display.flip()
		pygame.time.wait(10)
#

if __name__ == '__main__':
	main()
#