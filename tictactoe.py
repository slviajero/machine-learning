from random import randrange, random 
import pickle

#
# the Board class contains the game logic and a helper functions 
# to evaluate the Board state, its history 
#
class Board:

	def __init__(self, preload=('x'), autoscan=True):

		# basic parameters
		self.dim=3
		self.cross='x'
		self.circle='o'
		self.blank=' '
		
		# variables of the board
		if preload==('x'):
			self.board=self.emptyboard()
		else:
			self.board=self.preloadboard(preload)
		if autoscan:
			self.status=self.scan()
		self.history=[]

	def print(self):
		line=self.board[0]
		print("{}|{}|{}".format(line[0], line[1], line[2]))
		print("-+-+-")
		line=self.board[1]
		print("{}|{}|{}".format(line[0], line[1], line[2]))
		print("-+-+-")
		line=self.board[2]
		print("{}|{}|{}".format(line[0], line[1], line[2]))
		print("")

	def emptyboard(self):
		b=[]
		emptyline=[]
		for i in range(0,self.dim):
			emptyline.append(self.blank)
		for i in range(0,self.dim):
			b.append(emptyline[:])
		return b

	def preloadboard(self, tuple):
		b=[]
		for i in range(0,self.dim):
			line=[]
			for j in range(0, self.dim):
				line.append(tuple[i][j])
			b.append(line[:])
		return b

	def erase(self, autoscan=True):
		self.board=self.emptyboard()
		if autoscan:
			self.status=self.scan()
		self.history=[]

	def copy(self, autoscan=True):
		b=Board()
		for i in range(0,self.dim):
			for j in range(0,self.dim):
				b.board[i][j]=self.board[i][j]
		b.history=self.history.copy()
		if autoscan:
			b.status=b.scan()
		return b

	def allowed_moves(self):
		moves=[]
		for i in range(0,self.dim):
			for j in range(0, self.dim):
				if self.board[i][j]==self.blank:
					moves.append((i, j))
		return moves

	def setcross(self,i,j):
		self.board[i][j]=self.cross

	def setcircle(self,i,j):
		self.board[i][j]=self.circle
		
	def setblank(self,i,j):
		self.board[i][j]=self.blank

	def getvalue(self, i, j):
		return self.board[i][j]

	def notblank(self, i, j):
		return self.board[i][j]!=self.blank

	# the scanners find out how many items are in one 
	# line, column or diag

	def scanlines(self):
		potentiallines=[]
		winnerlines=[]
		lines=[]
		for i in range(0, self.dim):
			q=0
			for j in range(0, self.dim):
				if self.notblank(i,j):
					q=q+1
			lines.append(q)
			if (q==3):
				if 	self.getvalue(i,0)==self.getvalue(i,1) and \
					self.getvalue(i,1)==self.getvalue(i,2):
					symbol=self.getvalue(i,0)
					winnerlines.append((i, symbol))

			if (q==2):
				if 	self.getvalue(i,0)==self.getvalue(i,1) or \
					self.getvalue(i,1)==self.getvalue(i,2) or \
					self.getvalue(i,0)==self.getvalue(i,2):
					for j in range(0,2):
						if self.notblank(i,j):
							symbol=self.getvalue(i,j)
							break
					potentiallines.append((i, symbol))

		status={ 'lines' : lines, 'winnerlines' : winnerlines, 'potentiallines' : potentiallines}
		return status

	def scancolumns(self):
		columns=[]
		winnercolumns=[]
		potentialcolumns=[]
		for j in range(0, self.dim):
			q=0
			for i in range(0, self.dim):
				if self.notblank(i,j):
					q=q+1

			columns.append(q)
			if (q==3):
				if 	self.getvalue(0,j)==self.getvalue(1,j) and \
					self.getvalue(1,j)==self.getvalue(2,j):
					symbol=self.getvalue(0,j)
					winnercolumns.append((j, symbol))
			if (q==2):
				if 	self.getvalue(0,j)==self.getvalue(1,j) or \
					self.getvalue(1,j)==self.getvalue(2,j) or \
					self.getvalue(0,j)==self.getvalue(2,j):
					for i in range(0,2):
						if self.notblank(i,j):
							symbol=self.getvalue(i,j)
							break
					potentialcolumns.append((j, symbol))

		status={ 'columns' : columns, 'winnercolumns' : winnercolumns, 'potentialcolumns' : potentialcolumns}
		return status

	# the i=j diag is 1, the other one 2
	def scandiags(self):
		diags=[]
		winnerdiags=[]
		potentialdiags=[]
		q=0
		for k in range(0, self.dim):
			if self.notblank(k,k):
				q=q+1
		diags.append(q)

		if (q==3):
			if 	self.getvalue(0,0)==self.getvalue(1,1) and \
				self.getvalue(1,1)==self.getvalue(2,2):
				symbol=self.getvalue(0,0)
				winnerdiags.append((0, symbol))
		if (q==2):
			if 	self.getvalue(0,0)==self.getvalue(1,1) or \
				self.getvalue(1,1)==self.getvalue(2,2) or \
				self.getvalue(0,0)==self.getvalue(2,2):
				for k in range(0,2):
					if self.notblank(k,k):
						symbol=self.getvalue(k,k)
						break
				potentialdiags.append((0, symbol))

		q=0
		for k in range(0, self.dim):
			if self.notblank(k, self.dim-k-1):
				q=q+1
		diags.append(q)

		if (q==3):
			if 	self.getvalue(0,2)==self.getvalue(1,1) and \
				self.getvalue(1,1)==self.getvalue(2,0):
				symbol=self.getvalue(1,1)
				winnerdiags.append((1, symbol))
		if (q==2):
			if 	self.getvalue(0,2)==self.getvalue(1,1) or \
				self.getvalue(1,1)==self.getvalue(2,0) or \
				self.getvalue(0,2)==self.getvalue(2,0):
				for k in range(0,2):
					if self.notblank(k,self.dim-k-1):
						symbol=self.getvalue(k,self.dim-k-1)
						break
				potentialdiags.append((1, symbol))

		status={ 'diags' : diags, 'winnerdiags' : winnerdiags, 'potentialdiags' : potentialdiags}
		return status

	# do I win in one move or do I lose in one move
	# not the best possible implementation
	def onemove(self, status):

		moves=status['moves']
		cross_wins=[]
		circle_wins=[]
		potentiallines=status['potentiallines']
		potentialcolumns=status['potentialcolumns']
		potentialdiags=status['potentialdiags']
		while potentiallines!=[]:
			potential=potentiallines.pop(0)
			i=potential[0]
			for j in range(0, self.dim):
				if not self.notblank(i, j):
					if potential[1]==self.cross:
						cross_wins.append((i, j))
					else:
						circle_wins.append((i, j))
					break
		while potentialcolumns!=[]:
			potential=potentialcolumns.pop(0)
			j=potential[0]
			for i in range(0, self.dim):
				if not self.notblank(i, j):
					if potential[1]==self.cross:
						cross_wins.append((i, j))
					else:
						circle_wins.append((i, j))
					break
		while potentialdiags!=[]:
			potential=potentialdiags.pop(0)
			d=potential[0]
			if d==0:
				for k in range(0, self.dim):
					if not self.notblank(k, k):
						if potential[1]==self.cross:
							cross_wins.append((k, k))
						else:
							circle_wins.append((k, k))
						break
						if potential[1]==self.mysymbol:
							i_win.append((k, k))
						break
			if d==1:
				for k in range(0, self.dim):
					if not self.notblank(k, self.dim-k-1):
						if potential[1]==self.cross:
							cross_wins.append((k, self.dim-k-1))
						else:
							circle_wins.append((k, self.dim-k-1))					
						break

		return cross_wins, circle_wins

	def scan(self):

		lines=self.scanlines()
		columns=self.scancolumns()
		diags=self.scandiags()
		moves=self.allowed_moves()

		status={}
		status.update(lines)
		status.update(columns)
		status.update(diags)
		status.update({'moves' : moves})

		winnerlines=status['winnerlines']
		winnercolumns=status['winnercolumns']
		winnerdiags=status['winnerdiags']

		cross_wins, circle_wins = self.onemove(status)

		status.update({'circle_wins' : circle_wins})
		status.update({'cross_wins'  : cross_wins})

		winner=''

		if winnerlines!=[]:
			winner=winnerlines[0][1]
		elif winnercolumns!=[]:
			winner=winnercolumns[0][1]		
		elif winnerdiags!=[]:
			winner=winnerdiags[0][1]
		elif len(moves)==0:
				winner=self.blank
		else:
			winner='n'

		status.update({'winner' : winner})

		return status

	def move(self, m, s, autoscan=True):
		moves=self.status['moves']
		if m in moves:
			 if s==self.cross:
			 	self.setcross(m[0], m[1])
			 elif s==self.circle:
			 	self.setcircle(m[0], m[1])
			 else:
			 	print("Illegal symbol")
			 	raise ValueError
		else:
			print("Illegal move")
			raise ValueError
		self.history.append((m, s))
		if autoscan:
			self.status=self.scan()
		return self.winner()

	def replay(self, history, n=9):
		h=len(history)
		if n<0:
			n=h-n
		if n<=0:
			return 0
		i=0
		self.erase()
		for h in history:
			move=h[0]
			symbol=h[1]
			self.move(move, symbol)
			i+=1
			if (i>=n):
				break
		return i

	def winner(self):
		return self.status['winner']

	def tuplize(self):
		list=[]
		for line in self.board:
			list.append(tuple(line))
		return tuple(list)

# 
# This class generates and index consiting of all possible board
# states and stores the index into a file, to each index value 
# the is a tag assigned 
#	tag values:  x - cross  has won - mapped to 1
#			     o - circle has won - mapped to -1 
#				' ' - a draw - mapped to 0.25 statically 
#				0.0 - all other moves are real number 
# these tage values are the first derivative of a true value function
# 	tag(b, move)=v(b+m)-v(b)
# to generate the value function an initial value has to be determined
# and then this function has to be used to evaluate moves
# the function function() uses 1 as an initial value setting a loss to 
# to 0, a win to 2 and a draw to 1.25, all other moves to 1. 
# with this definition FunctionalPlayer can play a value function 
# defined over an index. 
# we reverse win and lose depending on the symbol we play this doesn't work 
# well in a learning situation
# 

class ValueFunction:

	def __init__(self):
		self.values={}

	#
	# evaluates all possible moves using the value function 
	# and an heuristic that assignes a transition function 
	# to to the deltas of current and next state 
	#
	def evaluate(self, board, mysymbol):

		greedy_moves=[]
		exploratory_moves=[]
		deltas=[]
		moves=board.status['moves']
		t1=board.tuplize()
		for move in moves:
			b=board.copy(autoscan=False)
			b.move(move, mysymbol, autoscan=False)
			t2=b.tuplize()
			delta=self.function(t2, mysymbol)-self.function(t1, mysymbol)
			deltas.append(delta)
			if delta>0.0: 
				greedy_moves.append((move, delta, 'g'))
			else:
				exploratory_moves.append((move, delta, 'e'))
		if len(deltas)>0:
			minimum=min(deltas)
			maximum=max(deltas)
		weighted_moves=[]
		for g in greedy_moves:
			move=g[0]
			value=g[1]*100+1
			weighted_moves.append((move, value, 'g'))
		for e in exploratory_moves:
			move=e[0]
			if minimum==0 and e[1]==0:
				value=0.01
			else:
				value=e[1]/minimum*0.5
			weighted_moves.append((move, value, 'e'))
		evaluated_moves=[]
		total_weight=0
		for w in weighted_moves:
			move=w[0]
			weight=w[1]
			getype=w[2]
			total_weight+=weight
			evaluated_moves.append((move, total_weight, getype))
		return evaluated_moves		

	#
	# takes a tuple, looks up the index and gets the value
	# depending on the role we play (cross or circle)
	# the value is reversed 2.0 is winner, 0.25 is draw,
	# 0.0 is a loose, all other values are taken as is
	# this has the character of a boundary condition of
	# the value function in learning scenarios
	#
	def function(self, t, s='x'):
		
		try:
			v=self.values[t]
		except: 
			raise ValueError

		if s=='x':
			m=1.0
		else:
			m=-1.0

		if v=='x': 
			v=1.0*m
		elif v=='o':
			v=-1.0*m
		elif v==' ':
			v=0.25
		v=v+1.0
		return v

	#
	# the learning function, it is called after the move 
	# to adapt the function
	#
	def learn(self, board, move, symbol):
		t1=board.tuplize()
		b=board.copy()
		b.move(move, symbol)
		t2=b.tuplize()
		v1=self.function(t1, symbol)
		v2=self.function(t2, symbol)
		delta=(v2-v1)*0.1
		state=self.values[t1]
		if state!='x' and state!='o' and state!=' ':
			if (symbol=='x'):
				self.values.update({t1 : state+delta})
			else:
				self.values.update({t1 : state-delta})
			#print("Update ", delta)
		return

	# 
	# recursive function that generates all possible 
	# game scenarios and build up the index from tuples
	# it does not use the symmetries and results in 
	# 5500 indices
	#
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
				self.values.update({b_next.tuplize() : 0.0})
				self.generateindex(b_next, next_s)
			elif winner==' ':
				value=' '
				self.values.update({b_next.tuplize() : value})
			elif winner==b.cross:
				value='x'
				self.values.update({b_next.tuplize() : value})
			else:
				value='o'
				self.values.update({b_next.tuplize() : value})
		return self.values
	#
	# write the index to a file 
	#
	def writeindex(self):
		f = open("file.pkl","wb")
		pickle.dump(self.values,f)
		f.close()

	#
	# read the index from a file 
	#
	def readindex(self):
		f = open("file.pkl","rb")
		self.values=pickle.load(f)
		f.close()
		return self.values

	#
	# linear arithemtic on value functions, not really needed
	#

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

	#
	# clone the value function over the same index
	#
	def clone(self):
		f=ValueFunction()
		for v in self.values:
			f.values[v]=self.values[v]
		return f

#
# The Player classes all inherit from RandomPlayer.
#
# 	RandomPlayer: 		play a random move every time called
#	OneMoverPlayer: 	finds a winning and losing last move 
#						and reacts to it, but otherwise plays randomly
#	HumanPlayer: 		a human player module, asks for input and plays
#	FunctionalPlayer: 	needs a value function as parameter 
#						the value function accepts the board state, 
#						derives all possible next moves and evalutes them
#						assigning weights, the FunctionalPlayer selects
#						a move randomly
#

class RandomPlayer:

	def __init__(self, board, symbol):
		self.board=board
		self.mysymbol=symbol

	#this function generates the next move, returns it and sets it in the board
	def __next__(self):
		m=self.calculate(self.board)
		self.board.move(m, self.mysymbol)
		return (m, self.mysymbol)

	def calculate(self, b):
		status=b.scan()
		moves=status['moves']
		n=len(moves)
		r=randrange(0,n)
		next_move=moves[r]
		return next_move

	def lastwords(self, w):
		return

class OneMovePlayer(RandomPlayer):

	def __init__(self, board, symbol):
		super().__init__(board, symbol)

	def calculate(self, b):
		
		status=b.scan()
		moves=status['moves']
		if self.mysymbol==b.cross:
			i_win=status['cross_wins']
			good_move=status['circle_wins']
		else:
			i_win=status['circle_wins']
			good_move=status['cross_wins']
		if len(i_win)>0:
			next_move=i_win.pop()
		if len(good_move)>0:
			r=randrange(0, len(good_move))
			next_move=good_move[r]
		else:	
			r=randrange(0, len(moves))
			next_move=moves[r]
		
		if False:
			print("Board state:")
			b.print()
			print("New calculate produced move ", next_move)

		return next_move

class FunctionalPlayer(RandomPlayer):

	def __init__(self, board, symbol, evaluate, learn=None):
		self.evaluate=evaluate
		if learn!=None:
			self.learn=learn
		else:
			self.learn=lambda a, b, c : a
		super().__init__(board, symbol)

	def calculate(self, b):

		board=b.board
		status=b.status

		#
		# walk through all moves of the board, evaluate them 
		# and select one of them randomly
		#
		getype=''
		evaluated_moves=self.evaluate(b, self.mysymbol)
		total_weight=evaluated_moves[-1][1]
		if total_weight>0:
			r=random()*total_weight
			weight1=0
			for i in range(0, len(evaluated_moves)):
				weight2=evaluated_moves[i][1]
				if (r>weight1) and (r<=weight2):
					next_move=evaluated_moves[i][0]
					if len(evaluated_moves[i])==3:
						getype=evaluated_moves[i][2]
					break
				weight1=weight2
		else:
			raise ValueError

		# here we know what of next move will be 
		# and we know if it was a greedy of exploratory move
		# from the variable getype, evaluators which do not
		# support learning don't provide the infomation

		if getype=='g':
			self.learn(b, next_move, self.mysymbol) 

		if False:
			print("Board state:")
			b.print()
			print("New calculate produced move ", next_move)

		return next_move

class HumanPlayer(RandomPlayer):

	def __init__(self, board, symbol):
		super().__init__(board, symbol)
		print("Welcome to tictactoe, you are playing ", self.mysymbol)

	def calculate(self, b):
		next_move=[]
		while next_move==[]:
			b.print()
			print("Enter move")
			i=-1
			while i>2 or i<0:
				i=int(input("line (0-2):"))
			j=-1
			while j>2 or j<0:
				j=int(input("column (0-2):"))
			next_move=(i, j)
			if not next_move in b.status['moves']:
				print("Illegal move: ", next_move)
				print("Try again!")
				next_move=[]
			else:
				print("Move:", next_move)
				return next_move

	def lastwords(self, w):
		if w==board.blank:
			print("============== No winner - draw =================")
		else:
			print("============== Winner is  - {}  ==================".format(w))

#
# the Game class need a board, and two players, one for cross and one for circle
# it plays the game until it has a winner
#

class Game:

	def __init__(self, board, pcross, pcircle, verbose=False):

		self.board=board
		self.pcross=pcross
		self.pcircle=pcircle
		self.verbose=verbose

	def set_verbose(self, v):
		self.verbose=v

	def reset(self):
		self.board.erase()

	def play(self):
		if self.verbose:
			self.board.print()
		while True:
			next(self.pcross)
			w=self.board.winner()
			if self.verbose:
				self.board.print()
				print(w)
			if w!='n':
				break
			next(self.pcircle)
			w=self.board.winner()
			if self.verbose:
				self.board.print()
				print(w)
			if w!='n':
				break
		return w

	def lastwords(self, w):
		self.pcross.lastwords(w)
		self.pcircle.lastwords(w)

#
# stand alone value functions that work with the functional player class
# the value function in this form generates values for each move (!)
# the values are not normalized, there relative size is all that 
# matters 
# 
# random_value_function: generates the same moves as RandomPlayer
#							every move receives a weight 0.5
# centercorner_value_function: tries to set a piece to 
#							the center with weight 1.0
#							a corner with weight 2.0
#							any other field with weight 0.5
# onemove_value_function: detects sure wins and losses like 
#							the OneMovePlayer and in addition
#							behaves like the centercorner function
#							it is slightly stronger then OneMove
# nextmove_value_function: like onemove and tries to look ahead
#							one more move (not yet fully implemented)
#

def random_value_function(board, mysymbol):

	evaluated_moves=[]
	moves=board.status['moves']
	total_weight=0
	for move in moves:
		move_value=0.5
		total_weight+=move_value
		evaluated_moves.append((move, total_weight))
	return evaluated_moves

def centercorner_value_function(board, symbol):

	evaluated_moves=[]
	moves=board.status['moves']
	total_weight=0
	for move in moves:
		if move==(1,1):
			move_value=1.0
		elif move==(0,0) or move==(0,2) or move==(2,2) or move==(2, 0):
			move_value=2.0
		else:
			move_value=0.25
		total_weight+=move_value
		evaluated_moves.append((move, total_weight))
	return evaluated_moves


def onemove_value_function(board, symbol):

	evaluated_moves=[]
	moves=board.status['moves']
	status=board.status
	if symbol==board.circle:
		i_win=status['circle_wins']
		good_move=status['cross_wins']
	else:
		i_win=status['cross_wins']
		good_move=status['circle_wins']

	total_weight=0
	for move in moves:
		if move in i_win:
			move_value=10000
		elif move in good_move:
			move_value=100
		else:
			if move==(1,1):
				move_value=1.0
			elif move==(0,0) or move==(0,2) or move==(2,2) or move==(2, 0):
				move_value=1.0
			else:
				move_value=0.25
		total_weight+=move_value
		evaluated_moves.append((move, total_weight))
	return evaluated_moves

def nextmove_value_function(board, symbol):

	evaluated_moves=[]
	moves=board.status['moves']
	status=board.status
	if symbol==board.circle:
		i_win=status['circle_wins']
		good_move=status['cross_wins']
	else:
		i_win=status['cross_wins']
		good_move=status['circle_wins']

	# the winning moves are treated here
	total_weight=0
	for move in moves:
		if move in i_win:
			move_value=1000
		elif move in good_move:
			move_value=20			
		else:
			# here we are in the dark and try the move, this is 
			# not correctly written
			# something is wrong - begin -
			b=board.copy()
			b.move(move, symbol)
			new_status=b.scan()
			if symbol==board.circle:
				new_i_win=new_status['circle_wins']
			else:
				new_i_win=new_status['cross_wins']
			if len(new_i_win)==1:
				move_value=2
			elif len(new_i_win)==2:
				move_value=5	
			# something is wrong - end -
			else:
				if move==(1,1):
					move_value=1.0
				elif move==(0,0) or move==(0,2) or move==(2,2) or move==(2, 0):
					move_value=1.0
				else:
					move_value=0.25
		total_weight+=move_value
		evaluated_moves.append((move, total_weight))
	return evaluated_moves

if True:

	# 
	# a board and a dict to store the results
	#
	board=Board()

	#
	# create a dynamic value function
	#
	v=ValueFunction()
	try:
		print("Reading index")
		v.readindex()
	except:
		print("Generating Index from scratch - takes one minute")
		v.generateindex()
		v.writeindex()	

	# 
	# the Players
	#
	pcross=FunctionalPlayer(board, board.cross, v.evaluate, v.learn)
	pcircle=FunctionalPlayer(board, board.circle, onemove_value_function)
	#pcircle=HumanPlayer(board, board.circle)

	game=Game(board, pcross, pcircle, verbose=False)
	for k in range(0,100):
		result={board.cross : 0, board.circle : 0, board.blank : 0}
		for i in range(0,1000):
			game.reset()
			w=game.play()
			game.lastwords(w)
			result[w]+=1
		print(k, result)















