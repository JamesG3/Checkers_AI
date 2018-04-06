import pygame
# import board as b
from pygame.locals import *
import config as conf


# pygame.font.init()

# a = board.Board()
# print a.direction(1, 2, 'UpLeft')
class Display(object):
	def __init__(self):
		# self.timer = pygame.time.Clock()
		self.screen = pygame.display.set_mode((conf.WINDOWSIZE, conf.WINDOWSIZE))
		self.background = pygame.image.load('images/board.png')
		self.grid_size = conf.WINDOWSIZE / 6
		self.piece_size = self.grid_size / 2

		self.stopGame = False


	# show all valid moves for current piece on board
	def _show_moves(self, cur_piece, valid_moves):
		if not cur_piece:
			return

		rect = (cur_piece[0] * self.grid_size, cur_piece[1] * self.grid_size, self.grid_size, self.grid_size)
		pygame.draw.rect(self.screen, conf.DARK, rect)

		for grid in valid_moves:
			rect = (grid[0] * self.grid_size, grid[1] * self.grid_size, self.grid_size, self.grid_size)
			pygame.draw.rect(self.screen, conf.DARK, rect)
	


	def update_board(self, board, cur_piece, valid_moves):
		self.screen.blit(self.background, (0, 0))			# draw a new clean board above the previous board
		self._show_moves(cur_piece, valid_moves)
		# draw all pieces
		# print board.checkerBoard
		for i,row in enumerate(board.checkerBoard):
			for j,grid in enumerate(row):
				if grid.piece:
					color1 = conf.BLACK if grid.piece.player == "black" else conf.WHITE
					color2 = conf.WHITE if grid.piece.player == "black" else conf.BLACK
					coord = (i * self.grid_size + self.piece_size, j * self.grid_size + self.piece_size)
					pygame.draw.circle(self.screen, color1, coord, int(self.piece_size / 1.2))
					pygame.draw.circle(self.screen, color2, coord, self.piece_size / 4)

		if self.stopGame:
			# for temp
			self.screen.blit(self.text_surface_obj, self.text_rect_obj)
			# show messages?????????????????
			# show restart button
			# maybe show some statistical data???
			pass

		pygame.display.update()

		# update later, change position
	def show_msg(self, msg):
		self.stopGame = True
		self.font_obj = pygame.font.Font('freesansbold.ttf', 44)
		self.text_surface_obj = self.font_obj.render(msg, True, conf.DARK, conf.BLACK)
		self.text_rect_obj = self.text_surface_obj.get_rect()
		self.text_rect_obj.center = (conf.WINDOWSIZE / 2, conf.WINDOWSIZE / 2)


	def mouse_to_grid(self, (i, j)):
		return [i / self.grid_size, j / self.grid_size]







