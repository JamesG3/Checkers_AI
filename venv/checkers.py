import display
import board as b
import config as conf
import sys
import pygame
from pygame.locals import *



class Checkers:
	def __init__(self):
		self.display = display.Display()
		self.board = b.Board()


		self.turn = "black"				# init -> human moves first, OR can be choosen??
		self.valid_moves = []

		self.jump = 0
		self.curr_piece = None

		self._window()



	def _window(self):
		pygame.init()
		pygame.display.set_caption("Smart Checkers Robot")

	def game(self):
		self.mouse = self.display.mouse_to_grid(pygame.mouse.get_pos())
		# print self.mouse[::-1]

		for event in pygame.event.get():
			if event.type == QUIT:
				pygame.quit()

			if event.type == MOUSEBUTTONDOWN:
				if not self.jump:
					grid = self.board.checkerBoard[self.mouse[0]][self.mouse[1]]
					
					# select piece
					if grid.piece and grid.piece.player == self.turn:
						self.curr_piece = self.mouse
						self.valid_moves = self.board.valid_moves(self.curr_piece[0], self.curr_piece[1])

					# choose a move
					elif self.curr_piece and list(self.mouse) in self.valid_moves:
						self.board.move(self.curr_piece, self.mouse)

						# if jump, then remove an adversary piece
						if abs(self.curr_piece[0] - self.mouse[0]) == 2:
							piece_rmv = ((self.curr_piece[0]+self.mouse[0])/2, (self.curr_piece[1]+self.mouse[1])/2)
							self.board.remove(piece_rmv)
							self.jump = 1
							self.curr_piece = self.mouse

						else:
							self._if_gameover()
							self.changeTurn()

				if self.jump:
					valid_moves = self.board.valid_moves(self.curr_piece[0], self.curr_piece[1], 1)
					if not valid_moves:
						self.changeTurn()
					
					else:
						if self.mouse in valid_moves:
							self.board.move(self.curr_piece, self.mouse)
							piece_rmv = ((self.curr_piece[0]+self.mouse[0])/2, (self.curr_piece[1]+self.mouse[1])/2)
							self.board.remove(piece_rmv)
							self.curr_piece = self.mouse





	def changeTurn(self):
		# reset all variables
		self.turn = "black" if self.turn == "white" else "white"
		self.curr_piece = None
		self.valid_moves = []
		self.jump = 0


	def _if_gameover(self):
		for i in xrange(6):
			for j in xrange(6):
				grid = self.board.checkerBoard[i][j]
				if grid.color == "B"\
					and grid.piece\
					and grid.piece.player == self.turn\
					and self.board.valid_moves(i, j):
					return
		
		# game is over
		if self.turn == "black":
			self.display.show_msg("Robot wins!!")
		else:
			self.display.show_msg("Congratulation, you win!!")

		# show start a new round (***************)



	def main(self):
		while True:
			self.game()
			self.display.update_board(self.board, self.curr_piece, self.valid_moves)




checkers = Checkers()
checkers.main()














