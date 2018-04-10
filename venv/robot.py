class Robot(object):
	def __init__(self):
		pass


	def get_all_moves(self, board, player):
		moves = []
		pieces = board.check_jump(player)

		if pieces == []:	# if there is no jump step for current player
			for i in xrange(6):
				for j in xrange(6):
					if board.checkerBoard[i][j].piece\
						and board.checkerBoard[i][j].piece.player == player:

						valid_moves = board.valid_moves(i, j)
						# if valid_moves:
						for move in valid_moves:
							moves.append([[i,j],move])
		
		else:				# if jump step exist
			for piece in pieces:
				valid_moves = board.valid_moves(piece[0], piece[1])
				for move in valid_moves:
					moves.append(piece, move)

		
		return moves 		# moves could be empty or only has one move


	def make_move(self, board, player):
		moves = self.get_all_moves(board, player)
		if not moves:
			return None

		if len(moves) == 1:
			return moves[0]

		else:
			return self.A_B_search(player)


		# call get_all_moves() to get moves
		# call A_B_search to get best move
		# return that best move

		# if there is no valid move, return None, and change turn in checkers.py
		# else return piece and it's best move
		return piece, move

	def heuristic(self, ):

		pass

	def A_B_search(self, player):
		pass

	def min_max(self, minMax, player):
		pass
