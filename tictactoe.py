from random import randrange 


class Board:

	def __init__(self):
		self.dim=3
		self.cross='x'
		self.circle='o'
		self.blank=' '
		self.history=[]
		self.winner=None
		self.moves_left=9
		self.erase()
		self.status=self.scan()

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

	def erase(self):
		self.board=[ [self.blank, self.blank, self.blank], [self.blank, self.blank, self.blank], [self.blank, self.blank, self.blank]]
		self.history=[]
		self.winner=None
		self.moves_left=9
		self.scan()

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

	def scan(self):

		lines=self.scanlines()
		columns=self.scancolumns()
		diags=self.scandiags()
		moves=self.allowed_moves()

		status=lines
		status.update(columns)
		status.update(diags)
		status.update({'moves' : moves})

		self.status=status

		winnerlines=self.status['winnerlines']
		winnercolumns=self.status['winnercolumns']
		winnerdiags=self.status['winnerdiags']

		if winnerlines!=[]:
			winner=winnerlines.pop(0)
			self.winner=winner[1]

		if winnercolumns!=[]:
			winner=winnercolumns.pop(0)
			self.winner=winner[1]		

		if winnerdiags!=[]:
			winner=winnerdiags.pop(0)
			self.winner=winner[1]

		self.moves_left=len(moves)

		return status

	def move(self, m, s):

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
		self.scan()


class Player:

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

class PlayerPlus(Player):

	def __init__(self, board, symbol):
		super().__init__(board, symbol)

	def calculate(self, b):
		status=b.scan()
		moves=status['moves']
		good_move=[]
		potentiallines=status['potentiallines']
		potentialcolumns=status['potentialcolumns']
		potentialdiags=status['potentialdiags']
		while potentiallines!=[]:
			potential=potentiallines.pop(0)
			i=potential[0]
			for j in range(0,b.dim):
				if not b.notblank(i, j):
					good_move.append((i, j))
					break
		while potentialcolumns!=[]:
			potential=potentialcolumns.pop(0)
			j=potential[0]
			for i in range(0,b.dim):
				if not b.notblank(i, j):
					good_move.append((i, j))
					break
		while potentialdiags!=[]:
			potential=potentialdiags.pop(0)
			d=potential[0]
			if d==0:
				for k in range(0,b.dim):
					if not b.notblank(k, k):
						good_move.append((k, k))
						break
			if d==1:
				for k in range(0, b.dim):
					if not b.notblank(k, b.dim-k-1):
						good_move.append((k, b.dim-k-1))
						break	

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

class HumanPlayer(Player):

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

		while True:
			next(self.pcross)
			if self.verbose:
				self.board.print()
			if self.board.winner!=None:
				w=self.board.winner
				break
			if self.board.moves_left==0:
				w=self.board.blank
				break
			next(self.pcircle)
			if self.verbose:
				self.board.print()
			if self.board.winner!=None:
				w=self.board.winner
				break
			if self.board.moves_left==0:
				w=self.board.blank
				break

		return w

board=Board()
result={board.cross : 0, board.circle : 0, board.blank : 0}
pcross=PlayerPlus(board, board.cross)
pcircle=PlayerPlus(board, board.circle)
game=Game(board, pcross, pcircle)
game.set_verbose(False)
for i in range(0,1000):
	game.reset()
	w=game.play()
	result[w]+=1
	# if w==board.blank:
	#	print("============== No winner - draw =================")
	#else:
	#	print("============== Winner is  - {}  ==================".format(w))

print(result)









