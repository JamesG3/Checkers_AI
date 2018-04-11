import config as conf
import board


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

	def heuristic(self, board, player):
		if player == "white":
			return board.white_piece_Num
		else:
			return board.black_piece_Num
		

	

	def A_B_search(self, board, moves):
		# return final utility value and the curresponding next step 
		v, action = self.max_value(baord, float('-Inf'), float('Inf'), conf.DEPTH)
		return action
		

	def max_value(self, board, alpha, beta, depth):
		# if reach the depth, return utility value
		if depth == 0:
			return self.heuristic(board, player)
		depth -= 1
		moves = self.get_all_moves(board, player)
		v = float('-Inf')
		action = None

		for piece, move in moves:
			tmp_board = board
			# make move on tmp board
			new_val = self.min_value(tmp_board, alpha, beta, depth-1)
			if v < new_val:
				v = new_val
				action = [piece, move]
			if v >= beta:
				return v
			alpha = max(alpha, v)

		return v, action


	def min_value(self, baord, alpha, beta, depth):
		# if reach the depth, return utility value
		if depth == 0 or not board.black_piece_Num or not board.white_piece_Num:
			return self.heuristic(board, player)
		depth -= 1
		moves = self.get_all_moves(board, player)
		v = float('Inf')

		for piece, move in moves:
			tmp_board = board
			# make move on tmp_board
			new_val = self.max_value(tmp_board, alpha, beta, depth-1)[0]
			if v < new_val:
				v = new_val

			if v <= alpha:
				return v
			beta = min(beta, v)

		return v


		
















