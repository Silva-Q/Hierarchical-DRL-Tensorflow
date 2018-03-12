
import random
import numpy as np
import sys

import utils

class Environment(object):
	def __init__(self, config):
		self.env = utils.get_env(config.env_name)
		

		self.state_size, self.action_repeat, self.random_start = \
				config.state_size, config.action_repeat, config.random_start

		self.display = config.display
		

		self._screen = None
		self.reward = 0
		self.terminal = True

	def new_game(self, from_random_game=False):
		#if self.lives == 0:
		self._screen = self.env.reset()
		self.render()
		return self.screen, 0, 0, self.terminal

	def new_random_game(self):
		self.new_game(True)
		for _ in range(random.randint(0, self.random_start - 1)):
			self._step(0)
		self.render()
		return self.screen, 0, 0, self.terminal

	def _step(self, action):
		self._screen, self.reward, self.terminal, _ = self.env.step(action)

	def _random_step(self):
		action = self.env.action_space.sample()
		self._step(action)

	@property
	def screen(self):
		#return imresize(rgb2gray(self._screen)/255., self.dims)
		#return cv2.resize(cv2.cvtColor(self._screen, cv2.COLOR_BGR2YCR_CB)/255., self.dims)[:,:,0]
		return self._screen

	@property
	def action_size(self):
		return self.env.action_space.n

	@property
	def lives(self):
		#return self.env.ale.lives()
		return self.env.lives()

	@property
	def state(self):
		return self.screen, self.reward, self.terminal

	def render(self):
		if self.display:
			self.env.render()

	def after_act(self, action):
		self.render()

class GymEnvironment(Environment):
	def __init__(self, config):
		super(GymEnvironment, self).__init__(config)

	def act(self, action, is_training=True):
		cumulated_reward = 0
		#start_lives = self.lives
		
		for _ in range(self.action_repeat):
			self._step(action)
			cumulated_reward = cumulated_reward + self.reward

			if 0:#is_training and start_lives > self.lives:
				continue #TODO better understand this
				cumulated_reward -= 1
				self.terminal = True

			if self.terminal:
				break

		self.reward = cumulated_reward

		self.after_act(action)
		
		return self.state

class SimpleGymEnvironment(Environment):
	def __init__(self, config):
		super(SimpleGymEnvironment, self).__init__(config)

	def act(self, action, is_training=True):
		self._step(action)

		self.after_act(action)
		return self.state
