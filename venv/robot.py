import config as conf
import board as B
import copy


class Robot(object):
	def __init__(self, AI_depth):
		self.max_depth = 0
		self.total_nodeNum = 0
		self.max_prunNum = 0
		self.min_prunNum = 0

		self.DEPTH = AI_depth


	def _get_all_moves(self, board, player, selected_piece = None):
		'''
		selected_piece is None if it's not after a capture move
		Find all valid moves for current player
		return all valid moves for current state
		moves = [[piece, move], [piece, move], [piece, move], ....]
		return type: list
		'''
		moves = []
		if selected_piece:
			valid_moves = board.valid_moves(selected_piece, 1)

			for move in valid_moves:
				moves.append([selected_piece, move])
			
			return moves

		# if there is no piece selected -> not after a capture move
		pieces = board.check_jump(player)

		if pieces == []:	# if there is no capture move for current player
			for i in xrange(6):	# find all regular moves
				for j in xrange(6):
					if board.checkerBoard[i][j].piece\
						and board.checkerBoard[i][j].piece.player == player:

						valid_moves = board.valid_moves([i, j])
						
						for move in valid_moves:
							moves.append([[i,j],move])
		
		else:		# if capture moves exist
			for piece in pieces:	# save all capture moves
				valid_moves = board.valid_moves(piece)
				for move in valid_moves:
					moves.append([piece, move])

		return moves 		# moves could be empty


	def _heuristic(self, board, terminal = 0):
		'''
		heuristic function
		return utility value for non-terminal and terminal state
		using heuristic function
		return type: int
		'''
		if terminal:
			if board.white_piece_Num > board.black_piece_Num:		# AI win
				return 1000
			elif board.white_piece_Num < board.black_piece_Num:		# AI lose
				return -1000
			else:													# draw
				return 0
		else:
			return board.white_piece_Num - board.black_piece_Num


	def _A_B_search(self, board, moves):
		'''
		start alpha beta search here
		return the best move
		action = [piece, move]
		return type: list
		'''
		# return final utility value and the curresponding next step 
		v, action = self._max_value(board, -1000, 1000, self.DEPTH)
		return action


	def _max_value(self, board, alpha, beta, depth):
		self.total_nodeNum += 1
		self.max_depth = max(self.max_depth, self.DEPTH - depth)

		moves = self._get_all_moves(board, 'white')
		if not moves:									# terminal state
			return self._heuristic(board, 1), None
		# if reach the depth, return utility value
		if depth == 0:
			return self._heuristic(board), None

		v = float('-Inf')
		action = None

		for piece, move in moves:
			# make move on tmp_board
			tmp_board = self._make_move(board, piece, move)
			new_val = self._min_value(tmp_board, alpha, beta, depth-1)
			
			if v < new_val:
				v = new_val
				action = [piece, move]
			
			if v >= beta:	# pruning
				self.max_prunNum += 1
			alpha = max(alpha, v)

		if v == float('-Inf'):		# if there is no valid move -> terminal state
			return self._heuristic(board), None
		else:
			return v, action
			

	def _min_value(self, board, alpha, beta, depth):
		self.total_nodeNum += 1
		self.max_depth = max(self.max_depth, self.DEPTH - depth)

		moves = self._get_all_moves(board, 'black')
		if not moves:
			return self._heuristic(board, 1)

		# if reach the depth, return utility value
		if depth == 0:
			return self._heuristic(board)
		
		v = float('Inf')

		for piece, move in moves:
			# make move on tmp_board
			tmp_board = self._make_move(board, piece, move)
			new_val = self._max_value(tmp_board, alpha, beta, depth-1)[0]
			if v > new_val:
				v = new_val

			if v <= alpha:	# pruning
				self.min_prunNum += 1
				return v
			beta = min(beta, v)

		if v == float('Inf'):		# if terminal state
			return self._heuristic(board)
		else:
			return v


	def _make_move(self, board, piece, move):
		'''
		make a deepcopy on given board object
		make move on this tmp_board
		return this tmp_board
		return type: object
		'''
		tmp_board = copy.deepcopy(board)
		if abs(piece[0] - move[0]) == 2:		# jump step
			tmp_board.remove([(piece[0] + move[0]) / 2, (piece[1] + move[1]) / 2])
		tmp_board.move(piece, move)

		return tmp_board


		
	def choose_move(self, board, selected_piece = None):
		'''
		Get all valid moves by calling function _get_all_moves()
		Get the best action by calling function _A_B_search()
		return the best action
		return [] if no valid move
		return type: list
		'''

		self.max_depth = 0				# reset all counters
		self.total_nodeNum = 0
		self.max_prunNum = 0
		self.min_prunNum = 0

		moves = self._get_all_moves(board, 'white', selected_piece)
		
		if not moves:
			return []

		if len(moves) == 1:		# if only have one choice
			return moves[0]

		else:
			action = self._A_B_search(board, moves)
			
			print 'max_depth: ' + str(self.max_depth)
			print 'total_nodeNum: ' + str(self.total_nodeNum)
			print 'max_prunNum: ' + str(self.max_prunNum)
			print 'min_prunNum: ' + str(self.min_prunNum)
			print '======================'

			return action















