# pyboids by mancaf
# Implementing the Boid Flocking Behaviour algorithm
# in Python and Pygame

import pygame
from .flock import Flock
from .boid import Boid
from . import params, utils
from time import time

key_to_function = {
	# insert lambda hooks here
}

class Simulation:
	running = True
	screen = pygame.display.set_mode(params.SCREEN_SIZE)
	pygame.display.set_caption(params.CAPTION)
	clock = pygame.time.Clock()
	flock = Flock()
	to_update = pygame.sprite.Group()
	to_display = pygame.sprite.Group()

	def update(self, motion_event, click_event):
		self.to_update.update(motion_event, click_event)

	def display(self):
		for sprite in self.to_display:
			sprite.display(self.screen)

	def run(self):
		key_to_function = {
			pygame.K_ESCAPE: lambda self, event: setattr(self, "running", False),
			pygame.K_s: lambda self, event: self.flock.toggle_seek(),
		}
		self.to_update = pygame.sprite.Group(
			self.flock
		)
		self.to_display = pygame.sprite.Group(
			self.to_update,
		)
		while self.running:
			t = time()
			motion_event, click_event = None, None
			self.screen.fill(params.BACKGROUND)
			self.clock.tick(params.FPS)
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					self.running = False
				elif event.type == pygame.KEYDOWN and event.key in key_to_function:
					key_to_function[event.key](self, event)
				elif event.type == pygame.MOUSEBUTTONDOWN:
					click_event = event
				elif event.type == pygame.MOUSEMOTION:
					motion_event = event
			self.update(motion_event, click_event)
			self.display()
			pygame.display.flip()
			print("FPS :", 1/(time()-t))

	def quit(self):
		self.running = False