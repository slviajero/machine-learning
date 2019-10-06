from random import randrange, random 


class Board:

	def __init__(self):

		# basic parameters
		self.dim=3
		self.cross='x'
		self.circle='o'
		self.blank=' '
		
		# variables of the board
		self.board=self.emptyboard()
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

	def erase(self):
		self.board=self.emptyboard()
		self.status=self.scan()
		self.history=[]

	def copy(self):
		b=Board()
		for i in range(0,self.dim):
			for j in range(0,self.dim):
				b.board[i][j]=self.board[i][j]
		b.history=self.history.copy()
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

	def __init__(self, board, symbol, function):
		self.function=function
		super().__init__(board, symbol)

	def calculate(self, b):

		board=b.board
		status=b.status
		evaluated_moves=[]

		moves=status['moves']
		evaluated_moves=self.function(b, self.mysymbol)
		total_weight=evaluated_moves[-1][1]

		if total_weight>0:
			r=random()*total_weight
			weight1=0
			for i in range(0, len(evaluated_moves)):
				weight2=evaluated_moves[i][1]
				if (r>weight1) and (r<=weight2):
					next_move=evaluated_moves[i][0]
					break
				weight1=weight2
		else:
			raise ValueError

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
			move_value=1000
		elif move in good_move:
			move_value=10
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
	board=Board()
	result={board.cross : 0, board.circle : 0, board.blank : 0}
	
	pcross=FunctionalPlayer(board, board.cross, onemove_value_function)
	#pcross=OneMovePlayer(board, board.cross)
	#pcircle=FunctionalPlayer(board, board.circle, onemove_value_function)
	#pcircle=OneMovePlayer(board, board.circle)
	pcircle=RandomPlayer(board, board.circle)
	game=Game(board, pcross, pcircle, verbose=False)
	for i in range(0,1000):
		game.reset()
		w=game.play()
		result[w]+=1
	# if w==board.blank:
	#	print("============== No winner - draw =================")
	#else:
	#	print("============== Winner is  - {}  ==================".format(w))

print(result)













