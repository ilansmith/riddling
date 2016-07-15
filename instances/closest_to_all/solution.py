#!/usr/bin/python3

###########
# imports #
###########
import sys # for maxsize

########
# code #
########

'''
efficient solution:
first calculate the shortest path of each person to each square
(create matrix per person) and then calculate the square which is
the best. If several squares have the same value - print them all.
'''

def add_tup(t1, t2):
	return tuple(map(lambda x, y: x + y, t1, t2))

class Position:
	def __init__(self, x, y):
		self.x=x
		self.y=y
	def add(self, p):
		self.x+=p.x
		self.y+=p.y
	def __str__(self):
		return '({x},{y})'.format(x=self.x, y=self.y)

directions=[
	Position(0,1),
	Position(1,0),
	Position(0,-1),
	Position(-1,0),
]


class Matrix:
	def __init__(self, v, w, h):
		self.data=[[v for x in range(w)] for y in range(h)]
		self.w=w
		self.h=h
	def get(self, x, y):
		return self.data[y][x]
	def get_pos(self, p):
		return self.data[p.y][p.x]
	def set(self, x, y, v):
		self.data[y][x]=v
	def set_pos(self, p, v):
		self.data[p.y][p.x]=v
	def illegal(self, x, y):
		return x<0 or x>=self.w or y<0 or y>=self.h
	def illegal_pos(self, p):
		return p.x<0 or p.x>=self.w or p.y<0 or p.y>=self.h
	def add(self, m):
		for y,l in enumerate(self.data):
			for x,e in enumerate(l):
				if m.get(x,y) is not None and l[x] is not None:
					l[x]+=m.get(x,y)
	def minimum(self):
		val=sys.maxsize
		for l in self.data:
			for e in l:
				if e is not None and e<val:
					val=e
		return val
	def duplicate(self):
		m=Matrix(None, self.w, self.h)
		for y,l in enumerate(self.data):
			for x,e in enumerate(l):
				m.set(x,y,e)
		return m
	def __str__(self):
		res=''
		for l in self.data:
			for e in l:
				res+=str(e)+', ';
			res+='\n'
		return res

def create_matrix(v, w, h):
	return [[0 for x in range(w)] for y in range(h)]

def solve(m):
	# find the height and width of the matrix
	h=len(m)
	w=len(m[0])
	# first find all the people in the matrix
	people=[]
	for y,l in enumerate(m):
		for x,c in enumerate(l):
			if c=='P':
				people.append(Position(x,y))
	assert len(people)>0
	# now calculate shortest distance per person
	sdms=[]
	for p in people:
		sdm=Matrix(None, w, h)
		sdm.set_pos(p, 0)
		positions=[p]
		while len(positions)>0:
			pos=positions.pop()
			steps=sdm.get_pos(pos)
			for d in directions:
				cpos=Position(pos.x, pos.y)
				cpos.add(d)
				if sdm.illegal_pos(cpos):
					continue
				place=m[cpos.y][cpos.x]
				if place=='*':
					continue
				cval=sdm.get_pos(cpos)
				if cval is not None:
					if steps+1<cval:
						sdm.set_pos(cpos, steps+1)
					else:
						continue
				else:
					sdm.set_pos(cpos, steps+1)
				positions.append(cpos)
		#print(sdm)
		sdms.append(sdm)
	# now find the ideal position for the kitchen
	sums=sdms[0].duplicate()
	for sdm in sdms[1:]:
		sums.add(sdm)
	#print(sums)
	# now find the minimum and convert to a matrix of results...
	mini=sums.minimum()
	#print(mini)
	# create a boolean matrix showing the solutions
	results=Matrix(False, sums.w, sums.h)
	for x in range(sums.w):
		for y in range(sums.h):
			if sums.get(x, y)==mini:
				results.set(x, y, True)
	print(m)
	print(results)


#########
# tests #
#########
m1=[
	'P___P',
	'_____',
	'_____',
	'_____',
	'P___P',
]
solve(m1)

m2=[
	'P___P',
	'_*_*_',
	'_*_*_',
	'_***_',
	'P___P',
]
solve(m2)

m3=[
	'P*__P',
	'_*___',
	'_*___',
	'_*___',
	'P___P',
]
solve(m3)

m4=[
	'P*__P',
	'_*___',
	'_*___',
	'_*___',
	'P*__P',
]
solve(m4)
