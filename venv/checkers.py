import display
import board
import robot
import config as conf
import sys
import pygame
from pygame.locals import *
import time


class Checkers:
	def __init__(self):	
		self.display = display.Display()
		self.board = board.Board()

		self.set_difficulty = 0
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
		self.set_difficulty = 0
		self._window()
	

	def game(self):
		def check_move():
			if self.Hum_noMove and self.Rbt_noMove:
				self._check_winner()
				if pygame.mouse.get_pressed() == conf.RIGHTKEY:
					self._restart()
				else:
						# time.sleep(0.5)
					return
		
			else:			# if current player has move, reset Rbt_noMove and Hum_noMove
				if self._has_move(self.turn):
					if self.turn == "black":
						self.Rbt_noMove = 0
					elif self.turn == "white":
						self.Hum_noMove = 0
				else:					# if current player cannot move, change turn
					if self.turn == "black":
						self.Hum_noMove = 1
						self._changeTurn()
						# continue
					elif self.turn == "white":
						self.Rbt_noMove = 1
						self._changeTurn()
						# continue

		# select which player moves first
		if self.turn is None:
			if self.set_difficulty == 0:	# choose AI level
				self.display.show_msg("Choose AI level: Easy-1, Mid-2, Hard-3")
				pygame.display.update()

				for event in pygame.event.get():
					if event.type == QUIT:
						pygame.quit()
						sys.exit()

					if event.type == KEYDOWN:
						if event.unicode == '1':
							self.robot = robot.Robot(conf.DEPTH_EASY)
							self.set_difficulty = 1
						elif event.unicode == '2':
							self.robot = robot.Robot(conf.DEPTH_MID)
							self.set_difficulty = 1
						elif event.unicode == '3':
							self.robot = robot.Robot(conf.DEPTH_HARD)
							self.set_difficulty = 1
					else:
						return

			else:	# choose who goes first
				self.display.show_msg("Who goes first? 1: U / 2: Me")
				pygame.display.update()

				for event in pygame.event.get():
					if event.type == QUIT:
						pygame.quit()
						sys.exit()
					
					if event.type == KEYDOWN:
						if event.unicode == '1':
							self.turn = "black"
							self.display = display.Display()
						elif event.unicode == '2':
							self.turn = "white"
							self.display = display.Display()
					else:
						return

		# if all players cannot move, game is over.
		# print self.Hum_noMove, self.Rbt_noMove

		check_move()
		if self.turn == "white":
			if not self.jump:
				action = self.robot.choose_move(self.board)
				if action:
					time.sleep(0.5)
					piece, move = action
					if abs(piece[0] - move[0]) == 2:	# jump step
						self.jump = 1
						self.board.remove([(piece[0] + move[0]) / 2, (piece[1] + move[1]) / 2])
					self.board.move(piece, move)
					self.curr_piece = move
					time.sleep(0.5)
				else:
					self._changeTurn()
				
			if self.jump:
				action = self.robot.choose_move(self.board, self.curr_piece)
				if action:
					time.sleep(0.5)
					piece, move = action
					self.board.remove([(piece[0] + move[0]) / 2, (piece[1] + move[1]) / 2])
					self.board.move(piece, move)
					self.curr_piece = move
					time.sleep(0.5)
					
					return	# break the current loop, keep looking whether there are other jump steps
				else:
					self._changeTurn()	
			else:
				self._changeTurn()
				

		check_move()
		self.mouse = self.display.mouse_to_grid(pygame.mouse.get_pos())

		for event in pygame.event.get():

			if event.type == QUIT:
				pygame.quit()
				sys.exit()

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


				while self.jump:
					self.valid_moves = self.board.valid_moves(self.curr_piece[0], self.curr_piece[1], 1)
					self.display.update_board(self.board, self.curr_piece, self.valid_moves)
					if not self.valid_moves:
						self._changeTurn()
						return
					
					else:
						if pygame.mouse.get_pressed() == conf.LEFTKEY:
							if self.mouse in self.valid_moves:
								self.board.move(self.curr_piece, self.mouse)
								piece_rmv = ((self.curr_piece[0]+self.mouse[0])/2, (self.curr_piece[1]+self.mouse[1])/2)
								self.board.remove(piece_rmv)
								self.curr_piece = self.mouse
								continue
						return


	def main(self):
		while True:
			self.game()
			self.display. update_board(self.board, self.curr_piece, self.valid_moves)



checkers = Checkers()
checkers.main()














