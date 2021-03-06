import pygame
from pygame.locals import *
import config as conf


class Display(object):
	def __init__(self):
		self.screen = pygame.display.set_mode((conf.WINDOWSIZE, conf.WINDOWSIZE))
		self.background = pygame.image.load(conf.BACKGROUND)
		self.grid_size = conf.WINDOWSIZE / 6
		self.piece_size = self.grid_size / 2

		self.stopGame = False


	def _show_moves(self, cur_piece, valid_moves):
		'''
		given a selected piece, shade the grids for all valid moves
		show all valid moves for selected piece
		'''
		if not cur_piece:
			return

		rect = (cur_piece[0] * self.grid_size, cur_piece[1] * self.grid_size, self.grid_size, self.grid_size)
		pygame.draw.rect(self.screen, conf.DARK, rect)

		for grid in valid_moves:
			rect = (grid[0] * self.grid_size, grid[1] * self.grid_size, self.grid_size, self.grid_size)
			pygame.draw.rect(self.screen, conf.DARK, rect)
	

	def update_board(self, board, cur_piece, valid_moves):
		'''
		update the checker borad
		if game is over, show text box to declare the winner/draw
		'''
		self.screen.blit(self.background, (0, 0))	# draw a new clean board above the previous board
		self._show_moves(cur_piece, valid_moves)
		
		# draw all pieces
		for i,row in enumerate(board.checkerBoard):
			for j,grid in enumerate(row):
				if grid.piece:
					color1 = conf.BLACK if grid.piece.player == "black" else conf.WHITE
					color2 = conf.WHITE if grid.piece.player == "black" else conf.BLACK
					coord = (i * self.grid_size + self.piece_size, j * self.grid_size + self.piece_size)
					pygame.draw.circle(self.screen, color1, coord, int(self.piece_size / 1.2))
					pygame.draw.circle(self.screen, color2, coord, self.piece_size / 4)

		if self.stopGame:
			self.screen.blit(self.textbox, self.textbox_rect)

		pygame.display.update()


	def show_msg(self, msg):
		self.stopGame = True
		self.text = pygame.font.SysFont("comicsansms", 27)
		self.textbox = self.text.render(msg, True, conf.BLACK)
		self.textbox_rect = self.textbox.get_rect()
		self.textbox_rect.center = (conf.WINDOWSIZE / 2, conf.WINDOWSIZE / 2)

	
	def mouse_to_grid(self, mouse):
		'''
		convert mouse coord into a coord on checkerBoard
		'''
		return [mouse[0] / self.grid_size, mouse[1] / self.grid_size]







