import pickle
from tictactoe import Board

class ValueFunction:

	def __init__(self):

		self.values={}

	def generateindex(self, b=None, s=''):

		if b==None:
			b=Board()

		self.values.update({b.tuplize() : 0.0})

		if s=='' or s==b.circle: 
			next_s=b.cross
		else:
			next_s=b.circle

		for m in b.status['moves']:
			b_next=b.copy()
			b_next.move(m, next_s)
			winner=b_next.winner()
			if winner=='n':
				self.generateindex(b_next, next_s)
			elif winner==' ':
				value=0.5
				self.values.update({b_next.tuplize() : value})
			elif winner==b.cross:
				value=1.0
				self.values.update({b_next.tuplize() : value})
			else:
				value=-1.0
				self.values.update({b_next.tuplize() : value})

		return self.values

	def writeindex(self):
		f = open("file.pkl","wb")
		pickle.dump(self.values,f)
		f.close()

	def readindex(self):
		f = open("file.pkl","rb")
		self.values=pickle.load(f)
		f.close()
		return self.values

	def multiply(self, a):
		f=ValueFunction()
		for v in self.values:
			f.values[v]=self.values[v]*a
		return f

	def add(self, vf):
		f=ValueFunction()
		for v in self.values:
			f.values[v]=vf.values[v]+self.values[v]
		return f

	def clone(self):
		f=ValueFunction()
		for v in self.values:
			f.values[v]=self.values[v]
		return f

f1=ValueFunction()
#print("Generatetest")
#f.generateindex()
#print("Write it")
#f.writeindex()
print("Read it")
f1.readindex()
f2=f1.clone()

if True:
	cross_wins=0
	circle_wins=0
	draw=0
	nowin=0
	for v in f2.values:
		if f2.values[v]==1.0:
			cross_wins+=1
		elif f2.values[v]==-1.0:
			circle_wins+=1
		elif f2.values[v]==0.5:
			draw+=1
			print(v, f1.values[v])
		else:
			nowin+=1

	print(cross_wins, circle_wins, draw, nowin)


if False:
	print(len(v.values))
	list=[]
	for x in v.values:
		list.append(x)
		if v.values[x]=='x':
			print(x)
	i=list[990]
	print(i)
	print(v.function(i, 'x'))
	b=Board(preload=i, autoscan=True)
	b.print()
	print(b.status['moves'])
	print(v.evaluate(b, 'o'))



