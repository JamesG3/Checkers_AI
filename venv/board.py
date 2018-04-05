class Piece(object):
	def __init__(self, player, frozen = 0):		# player "black"and "white"
		self.player = player
		self.frozen = frozen

class Grid(object):
	def __init__(self, color, piece = None):	# color "W" - white and "B" - black
		self.color = color
		self.piece = piece
		
		  
class Board(object):
	def __init__(self):
		self.checkerBoard = [[-1 for _ in xrange(6)] for _ in xrange(6)]
		self._create()

	def _create(self):
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
					if i<3:
						self.checkerBoard[i][j].piece = Piece("white")
					elif 3<i<6:
						self.checkerBoard[i][j].piece = Piece("black")
			return



	def move(self, start, end):				# move piece from start to end coordinate
		s_i, s_j = start[0], start[1]
		e_i, e_j = end[0], end[1]
		self.checkerBoard[e_i][e_j].piece = self.checkerBoard[s_i][s_j].piece
		self.checkerBoard[s_i][s_j].piece = None


	def direction(self, i, j, moveto):
		return {'UpLeft': lambda: (i-1, j-1),
				'UpRight': lambda: (i-1, j+1),
				'DownLeft': lambda: (i+1, j-1),
				'DownRight': lambda: (i+1, j+1),
		}.get(moveto)()

	def _valid_position(self, i, j):
		return (-1 < i < 6) and (-1 < i < 6)


	def valid_moves(self, i, j, jump = False):		# return all valid moves for self.checkerBoard[i][j]
		cur_grid = self.checkerBoard[i][j]
		if cur_grid.piece == None:					# if no piece in that grid
			return []

		valid_moves = []
		if jump:			# if current piece is from elsewhere after one jump, 
							# then check whether there are other place to jump.
			# computer move
			if cur_grid.piece.player == "white":    					
				L_move1 = self.direction(i, j, 'DownLeft')
				R_move1 = self.direction(i, j, 'DownRight')
				L_move2 = self.direction(L_move1[0], L_move1[1], 'DownLeft')
				R_move2 = self.direction(R_move1[0], R_move1[1], 'DownRight')
				L1_i, L1_j, R1_i, R1_j = L_move1[0], L_move1[1], R_move1[0], R_move1[1]
				L2_i, L2_j, R2_i, R2_j = L_move2[0], L_move2[1], R_move2[0], R_move2[1]

				if (self._valid_position(L2_i, L2_j))\
					and self.checkerBoard[L1_i][L1_j].piece\
					and self.checkerBoard[L1_i][L1_j].piece.player == "black"\
					and self.checkerBoard[L2_i][L2_j].piece is None:					# empty

					valid_moves.append([L2_i, L2_j])

				if self._valid_position(R2_i, R2_j)\
					and self.checkerBoard[R1_i][R1_j].piece\
					and self.checkerBoard[R1_i][R1_j].piece.player == "black"\
					and self.checkerBoard[R2_i][R2_j].piece is None:					# empty

					valid_moves.append([R2_i, R2_j])
			
			# human move
			elif cur_grid.piece.player == "black":
				L_move1 = self.direction(i, j, 'UpLeft')
				R_move1 = self.direction(i, j, 'UpRight')
				L_move2 = self.direction(L_move1[0], L_move1[1], 'UpLeft')
				R_move2 = self.direction(R_move1[0], R_move1[1], 'UpRight')
				L1_i, L1_j, R1_i, R1_j = L_move1[0], L_move1[1], R_move1[0], R_move1[1]
				L2_i, L2_j, R2_i, R2_j = L_move2[0], L_move2[1], R_move2[0], R_move2[1]

				if self._valid_position(L2_i, L2_j)\
					and self.checkerBoard[L1_i][L1_j].piece\
					and self.checkerBoard[L1_i][L1_j].piece.player == "white"\
					and self.checkerBoard[L2_i][L2_j].piece is None:				# empty

					valid_moves.append([L2_i, L2_j])

				if self._valid_position(R2_i, R2_j)\
					and self.checkerBoard[R1_i][R1_j].piece\
					and self.checkerBoard[R1_i][R1_j].piece.player == "white"\
					and self.checkerBoard[R2_i][R2_j].piece is None:				# empty

					valid_moves.append([R2_i, R2_j])


		else:
			# computer move
			jump_exist = 0		# jump step has priority

			if cur_grid.piece.player == "white":
				L_move1 = self.direction(i, j, 'DownLeft')
				R_move1 = self.direction(i, j, 'DownRight')
				L_move2 = self.direction(L_move1[0], L_move1[1], 'DownLeft')
				R_move2 = self.direction(R_move1[0], R_move1[1], 'DownRight')
				L1_i, L1_j, R1_i, R1_j = L_move1[0], L_move1[1], R_move1[0], R_move1[1]
				L2_i, L2_j, R2_i, R2_j = L_move2[0], L_move2[1], R_move2[0], R_move2[1]

				if self._valid_position(L2_i, L2_j) or self._valid_position(R2_i, R2_j):
					if self._valid_position(L2_i, L2_j)\
						and self.checkerBoard[L1_i][L1_j].piece\
						and self.checkerBoard[L1_i][L1_j].piece.player == "black"\
						and self.checkerBoard[L2_i][L2_j].piece is None:

						jump_exist = 1
						valid_moves.append([L2_i, L2_j])
					
					if self._valid_position(R2_i, R2_j)\
						and self.checkerBoard[R1_i][R1_j].piece\
						and self.checkerBoard[R1_i][R1_j].piece.player == "black"\
						and self.checkerBoard[R2_i][R2_j].piece is None:

						jump_exist = 1
						valid_moves.append([R2_i, R2_j])


				if jump_exist == 0:		# there is no jump step
					if self._valid_position(L1_i, L1_j)\
						and self.checkerBoard[L1_i][L1_j].piece == None:

						valid_moves.append([L1_i, L1_j])

					if self._valid_position(R1_i, R1_j)\
						and self.checkerBoard[R1_i][R1_j].piece == None:

						valid_moves.append([R1_i, R1_j])


			elif cur_grid.piece.player == "black":
				L_move1 = self.direction(i, j, 'UpLeft')
				R_move1 = self.direction(i, j, 'UpRight')
				L_move2 = self.direction(L_move1[0], L_move1[1], 'UpLeft')
				R_move2 = self.direction(R_move1[0], R_move1[1], 'UpRight')
				L1_i, L1_j, R1_i, R1_j = L_move1[0], L_move1[1], R_move1[0], R_move1[1]
				L2_i, L2_j, R2_i, R2_j = L_move2[0], L_move2[1], R_move2[0], R_move2[1]

				if self._valid_position(L2_i, L2_j) or self._valid_position(R2_i, R2_j):
					if self._valid_position(L2_i, L2_j)\
						and self.checkerBoard[L1_i][L1_j].piece\
						and self.checkerBoard[L1_i][L1_j].piece.player == "white"\
						and self.checkerBoard[L2_i][L2_j].piece is None:

						jump_exist = 1
						valid_moves.append([L2_i, L2_j])
					
					if self._valid_position(R2_i, R2_j)\
						and self.checkerBoard[R1_i][R1_j].piece\
						and self.checkerBoard[R1_i][R1_j].piece.player == "white"\
						and self.checkerBoard[R2_i][R2_j].piece is None:

						jump_exist = 1
						valid_moves.append([R2_i, R2_j])


				if jump_exist == 0:		# there is no jump step
					if self._valid_position(L1_i, L1_j)\
						and self.checkerBoard[L1_i][L1_j].piece == None:

						valid_moves.append([L1_i, L1_j])

					if self._valid_position(R1_i, R1_j)\
						and self.checkerBoard[R1_i][R1_j].piece == None:

						valid_moves.append([R1_i, R1_j])

		return valid_moves
			













