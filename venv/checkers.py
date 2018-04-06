import display
import board
import config as conf
import sys
import pygame
from pygame.locals import *



class Checkers:
	def __init__(self):
		self.display = display.Display()
		self.board = board.Board()

		self.turn = None
		self.valid_moves = []

		self.jump = 0
		self.curr_piece = None

		self.Rbt_noMove = 0
		self.Hum_noMove = 0

		self._window()


	def _window(self):
		pygame.init()
		pygame.display.set_caption("Smart Checkers Robot")


	# reset all variables
	def _changeTurn(self):
		self.turn = "black" if self.turn == "white" else "white"
		self.curr_piece = None
		self.valid_moves = []
		self.jump = 0


	# return whether the current player has move
	def _has_move(self, player):
		for i in xrange(6):
			for j in xrange(6):
				grid = self.board.checkerBoard[i][j]
				if grid.color == "B"\
					and grid.piece\
					and grid.piece.player == player\
					and self.board.valid_moves(i, j):
					return True
		return False

	# check winner and print message
	def _check_winner(self):
		if self.board.white_piece_Num > self.board.black_piece_Num:
			self.display.show_msg("Haha you lose! Click Right Key to Restart")
			pygame.display.update()

		elif self.board.white_piece_Num < self.board.black_piece_Num:
			self.display.show_msg("Congratulation, you win! Click Right Key to Restart")
			pygame.display.update()
		
		else:
			self.display.show_msg("Draw! Click Right Key to Restart")
			pygame.display.update()

	# restart game, reset all global variables
	def _restart(self):
		self.display = display.Display()
		self.board = board.Board()
		self.turn = None
		self.valid_moves = []
		self.jump = 0
		self.curr_piece = None
		self.Rbt_noMove = 0
		self.Hum_noMove = 0
		self._window()
	

	def game(self):
		self.mouse = self.display.mouse_to_grid(pygame.mouse.get_pos())

		for event in pygame.event.get():
			if event.type == QUIT:
				pygame.quit()
				sys.exit()

			# select which player moves first
			if self.turn is None:
				self.display.show_msg("Who goes first? Left Key: U / Right Key: Me")
				pygame.display.update()

				if pygame.mouse.get_pressed() == (1,0,0):
					self.turn = "black"
					self.display = display.Display()
				elif pygame.mouse.get_pressed() == (0,0,1):
					self.turn = "white"
					self.display = display.Display()
				else:
					continue

			# if all players cannot move, game is over.
			if self.Hum_noMove and self.Rbt_noMove:
				self._check_winner()
				if event.type == MOUSEBUTTONDOWN and pygame.mouse.get_pressed() == (0,0,1):
					self._restart()
			
			else:
				if self._has_move(self.turn):
					if self.turn == "black":
						self.Rbt_noMove = 0
					elif self.turn == "white":
						self.Hum_noMove = 0
				else:
					if self.turn == "black":
						self.Hum_noMove = 1
						self._changeTurn()
					elif self.turn == "white":
						self.Rbt_noMove = 1
						self._changeTurn()


			if event.type == MOUSEBUTTONDOWN:
				if not self.jump:
					jump_step = self.board.check_jump(self.turn)

					grid = self.board.checkerBoard[self.mouse[0]][self.mouse[1]]
					
					# select piece
					if grid.piece and grid.piece.player == self.turn:
						if jump_step == []:
							self.curr_piece = self.mouse
							self.valid_moves = self.board.valid_moves(self.curr_piece[0], self.curr_piece[1])
						else:
							if self.mouse in jump_step:
								self.curr_piece = self.mouse
								self.valid_moves = self.board.valid_moves(self.curr_piece[0], self.curr_piece[1])

					# choose a move
					elif self.curr_piece and self.mouse in self.valid_moves:
						self.board.move(self.curr_piece, self.mouse)

						# if jump, then remove an adversary piece
						if abs(self.curr_piece[0] - self.mouse[0]) == 2:
							piece_rmv = ((self.curr_piece[0]+self.mouse[0])/2, (self.curr_piece[1]+self.mouse[1])/2)
							self.board.remove(piece_rmv)
							self.jump = 1
							self.curr_piece = self.mouse

						else:
							self._changeTurn()

				if self.jump:
					self.valid_moves = self.board.valid_moves(self.curr_piece[0], self.curr_piece[1], 1)
					self.display.update_board(self.board, self.curr_piece, self.valid_moves)
					if not self.valid_moves:
						self._changeTurn()
					
					else:
						if self.mouse in self.valid_moves:
							self.board.move(self.curr_piece, self.mouse)
							piece_rmv = ((self.curr_piece[0]+self.mouse[0])/2, (self.curr_piece[1]+self.mouse[1])/2)
							self.board.remove(piece_rmv)
							self.curr_piece = self.mouse


	def main(self):
		while True:
			self.game()
			self.display. update_board(self.board, self.curr_piece, self.valid_moves)



checkers = Checkers()
checkers.main()














