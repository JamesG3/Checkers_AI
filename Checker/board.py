class Piece(object):
	'''
	two type of players: black and white
	'''
	def __init__(self, player):
		self.player = player

class Grid(object):
	'''
	each grid has one color: W - white / B - black
	a grid may point to a piece object
	'''
	def __init__(self, color, piece = None):
		self.color = color
		self.piece = piece
		
class Board(object):
	def __init__(self):
		self.checkerBoard = [[0 for _ in xrange(6)] for _ in xrange(6)]
		self._create()

		# OR (conf.BOARDSIZE/2) * (conf.BOARDSIZE/2 - 1)
		self.white_piece_Num = 6
		self.black_piece_Num = 6

	def _create(self):
		'''
		initialize a checker board
		assign grid color and pieces
		'''
		for i in xrange(6):
			for j in xrange(6):
				if not i%2 and not j%2:		# both even
					self.checkerBoard[i][j] = Grid("W")
				elif i%2 and not j%2:		# odd, even
					self.checkerBoard[i][j] = Grid("B")
				elif not i%2 and j%2:		# even, odd
					self.checkerBoard[i][j] = Grid("B")
				else:						# odd, odd
					self.checkerBoard[i][j] = Grid("W")

				if self.checkerBoard[i][j].color == "B":
					if j<2:
						self.checkerBoard[i][j].piece = Piece("white")
					elif 3<j<6:
						self.checkerBoard[i][j].piece = Piece("black")
		return


	def _direction(self, i, j, moveto):
		'''
		calculate coordinates after a move on selected direction
		return type: tuple
		'''
		return {'UpLeft': lambda: (i-1, j-1),
				'UpRight': lambda: (i+1, j-1),
				'DownLeft': lambda: (i-1, j+1),
				'DownRight': lambda: (i+1, j+1),
		}.get(moveto)()


	def _valid_position(self, i, j):
		'''
		check whether given position is valid in checkerBoard
		return type: bool
		'''
		return (-1 < i < 6) and (-1 < j < 6)

	def move(self, start, end):
		'''
		move piece from start to end (coordinate)
		'''
		s_i, s_j = start[0], start[1]
		e_i, e_j = end[0], end[1]
		self.checkerBoard[e_i][e_j].piece = self.checkerBoard[s_i][s_j].piece
		self.checkerBoard[s_i][s_j].piece = None


	def remove(self, piece):
		'''
		remove piece from board
		'''
		i, j = piece[0], piece[1]
		if self.checkerBoard[i][j].piece.player == "white":
			self.white_piece_Num -= 1
		else:
			self.black_piece_Num -= 1
			
		self.checkerBoard[i][j].piece = None


	def check_jump(self, player):
		'''
		return all capture moves for given player
		return type: list[list, list, ...]
		'''
		jump_list = []

		for i in xrange(6):
			for j in xrange(6):
				if self.checkerBoard[i][j].piece\
					and self.checkerBoard[i][j].piece.player == player:

					if player == "white":
						adversary = "black"
						L_move1 = self._direction(i, j, 'DownLeft')
						R_move1 = self._direction(i, j, 'DownRight')
						L_move2 = self._direction(L_move1[0], L_move1[1], 'DownLeft')
						R_move2 = self._direction(R_move1[0], R_move1[1], 'DownRight')
						L1_i, L1_j, R1_i, R1_j = L_move1[0], L_move1[1], R_move1[0], R_move1[1]
						L2_i, L2_j, R2_i, R2_j = L_move2[0], L_move2[1], R_move2[0], R_move2[1]
					else:
						adversary = "white"
						L_move1 = self._direction(i, j, 'UpLeft')
						R_move1 = self._direction(i, j, 'UpRight')
						L_move2 = self._direction(L_move1[0], L_move1[1], 'UpLeft')
						R_move2 = self._direction(R_move1[0], R_move1[1], 'UpRight')
						L1_i, L1_j, R1_i, R1_j = L_move1[0], L_move1[1], R_move1[0], R_move1[1]
						L2_i, L2_j, R2_i, R2_j = L_move2[0], L_move2[1], R_move2[0], R_move2[1]

					if self._valid_position(L2_i, L2_j) or self._valid_position(R2_i, R2_j):
						if self._valid_position(L2_i, L2_j)\
							and self.checkerBoard[L1_i][L1_j].piece\
							and self.checkerBoard[L1_i][L1_j].piece.player == adversary\
							and self.checkerBoard[L2_i][L2_j].piece is None:

							jump_list.append([i, j])

						if self._valid_position(R2_i, R2_j)\
							and self.checkerBoard[R1_i][R1_j].piece\
							and self.checkerBoard[R1_i][R1_j].piece.player == adversary\
							and self.checkerBoard[R2_i][R2_j].piece is None:
							
							jump_list.append([i, j])
		return jump_list


	def valid_moves(self, piece, jump = 0):
		'''
		return all valid moves for selected piece
		return type: list[list, list, ...]
		'''
		i, j = piece
		cur_grid = self.checkerBoard[i][j]
		if cur_grid.piece == None:			# if no piece in that grid
			return []

		valid_moves = []
		if jump:		# if current piece is from another position after one capture move, 
						# then check whether there are other capture moves
			# robot move
			if cur_grid.piece.player == "white":
				adversary = "black"
				L_move1 = self._direction(i, j, 'DownLeft')
				R_move1 = self._direction(i, j, 'DownRight')
				L_move2 = self._direction(L_move1[0], L_move1[1], 'DownLeft')
				R_move2 = self._direction(R_move1[0], R_move1[1], 'DownRight')
				L1_i, L1_j, R1_i, R1_j = L_move1[0], L_move1[1], R_move1[0], R_move1[1]
				L2_i, L2_j, R2_i, R2_j = L_move2[0], L_move2[1], R_move2[0], R_move2[1]
			
			# human move
			else:
				adversary = "white"
				L_move1 = self._direction(i, j, 'UpLeft')
				R_move1 = self._direction(i, j, 'UpRight')
				L_move2 = self._direction(L_move1[0], L_move1[1], 'UpLeft')
				R_move2 = self._direction(R_move1[0], R_move1[1], 'UpRight')
				L1_i, L1_j, R1_i, R1_j = L_move1[0], L_move1[1], R_move1[0], R_move1[1]
				L2_i, L2_j, R2_i, R2_j = L_move2[0], L_move2[1], R_move2[0], R_move2[1]

			# check left
			if (self._valid_position(L2_i, L2_j))\
				and self.checkerBoard[L1_i][L1_j].piece\
				and self.checkerBoard[L1_i][L1_j].piece.player == adversary\
				and self.checkerBoard[L2_i][L2_j].piece is None:					# empty

				valid_moves.append([L2_i, L2_j])

			# check right
			if self._valid_position(R2_i, R2_j)\
				and self.checkerBoard[R1_i][R1_j].piece\
				and self.checkerBoard[R1_i][R1_j].piece.player == adversary\
				and self.checkerBoard[R2_i][R2_j].piece is None:					# empty

				valid_moves.append([R2_i, R2_j])

		# if not after a capture move
		else:
			# computer move
			jump_exist = 0			# capture move flag
			player = cur_grid.piece.player

			if cur_grid.piece.player == "white":
				adversary = "black"
				L_move1 = self._direction(i, j, 'DownLeft')
				R_move1 = self._direction(i, j, 'DownRight')
				L_move2 = self._direction(L_move1[0], L_move1[1], 'DownLeft')
				R_move2 = self._direction(R_move1[0], R_move1[1], 'DownRight')
				L1_i, L1_j, R1_i, R1_j = L_move1[0], L_move1[1], R_move1[0], R_move1[1]
				L2_i, L2_j, R2_i, R2_j = L_move2[0], L_move2[1], R_move2[0], R_move2[1]

			else:
				adversary = "white"
				L_move1 = self._direction(i, j, 'UpLeft')
				R_move1 = self._direction(i, j, 'UpRight')
				L_move2 = self._direction(L_move1[0], L_move1[1], 'UpLeft')
				R_move2 = self._direction(R_move1[0], R_move1[1], 'UpRight')
				L1_i, L1_j, R1_i, R1_j = L_move1[0], L_move1[1], R_move1[0], R_move1[1]
				L2_i, L2_j, R2_i, R2_j = L_move2[0], L_move2[1], R_move2[0], R_move2[1]

			# if capture moves exist, return all capture moves
			if self._valid_position(L2_i, L2_j) or self._valid_position(R2_i, R2_j):
				if self._valid_position(L2_i, L2_j)\
					and self.checkerBoard[L1_i][L1_j].piece\
					and self.checkerBoard[L1_i][L1_j].piece.player == adversary\
					and self.checkerBoard[L2_i][L2_j].piece is None:

					jump_exist = 1
					valid_moves.append([L2_i, L2_j])
				
				if self._valid_position(R2_i, R2_j)\
					and self.checkerBoard[R1_i][R1_j].piece\
					and self.checkerBoard[R1_i][R1_j].piece.player == adversary\
					and self.checkerBoard[R2_i][R2_j].piece is None:

					jump_exist = 1
					valid_moves.append([R2_i, R2_j])

			if jump_exist == 0:		# if there is no capture move
				if self._valid_position(L1_i, L1_j)\
					and self.checkerBoard[L1_i][L1_j].piece == None:

					valid_moves.append([L1_i, L1_j])

				if self._valid_position(R1_i, R1_j)\
					and self.checkerBoard[R1_i][R1_j].piece == None:

					valid_moves.append([R1_i, R1_j])

		return valid_moves
			













