import config as conf
import board


class Robot(object):
	def __init__(self):
		pass


	def _get_all_moves(self, board, player):
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
					moves.append([piece, move])

		return moves 		# moves could be empty or only has one move


	def _heuristic(self, board):
		# if player == "white":
			# return board.white_piece_Num
		# else:
			# return board.black_piece_Num
		return board.white_piece_Num


	def _A_B_search(self, board, moves):
		# return final utility value and the curresponding next step 
		v, action = self._max_value(baord, float('-Inf'), float('Inf'), conf.DEPTH)
		return action


	def _max_value(self, board, alpha, beta, depth):
		# if reach the depth, return utility value
		if depth == 0:
			return self._heuristic(board), None
		moves = self._get_all_moves(board, 'white')
		v = float('-Inf')
		action = None

		for piece, move in moves:
			# make move on tmp board
			tmp_board = self._make_move(board, piece, move)
			new_val = self._min_value(tmp_board, alpha, beta, depth-1)
			action = [piece, move]
			if v < new_val:
				v = new_val
			
			if v >= beta:
				return v, action
			alpha = max(alpha, v)

		if v == float('-Inf'):		# if there is no valid move -> terminal state
			return self._heuristic(board), None
		else:
			return v, action
			

	def _min_value(self, baord, alpha, beta, depth):
		# if reach the depth, return utility value
		if depth == 0:
			return self._heuristic(board)
		moves = self._get_all_moves(board, 'black')
		v = float('Inf')

		for piece, move in moves:
			# make move on tmp_board
			tmp_board = self._make_move(board, piece, move)
			new_val = self._max_value(tmp_board, alpha, beta, depth-1)[0]
			if v < new_val:
				v = new_val

			if v <= alpha:
				return v
			beta = min(beta, v)

		if v == float('Inf'):		# if terminal state
			return self._heuristic(board)
		else:
			return v


	def _make_move(self, board, piece, move):
		tmp_board = board
		if abs(piece[0] - move[0]) == 2:		# jump step
			tmp_board.remove([(piece[0] + move[0]) / 2, (piece[1] + move[1]) / 2])
		tmp_board.move(piece, move)

		return tmp_board


		
	def choose_move(self, board):
		# return None if no move
		# return the best (piece, move)
		moves = self._get_all_moves(board, 'white')
		if not moves:
			return None

		if len(moves) == 1:
			return moves[0]

		else:
			return self._A_B_search(board)


		# call _get_all_moves() to get moves
		# call _A_B_search to get best move
		# return that best move

		# if there is no valid move, return None, and change turn in checkers.py
		# else return piece and it's best move















