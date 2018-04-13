
import random
import numpy as np
import sys
import gym
import utils
import logging
from configuration import Constants as CT


class Environment():
    def __init__(self, cnf):
        self.env_name = cnf.env.env_name
        self.gym = self.load_gym()
        self.gym.configure(cnf)
        print(type(self.gym), vars(self.gym))
        self.action_size = self.gym.action_space.n
        self.state_size = self.gym.state_space.n
        self.action_repeat, self.random_start = \
                cnf.env.action_repeat, cnf.env.random_start

        self.display_prob = cnf.gl.display_prob
        self._screen = None
        self.reward = 0
        self.terminal = True
        
        #Update configuration
        cnf.env.update({"state_size" : self.state_size,
                       "action_size": self.action_size}, add = True)
        
      
    def load_gym(self):
        if self.env_name in CT.GYM_envs:
            gym_env = gym.make(self.env_name).env
            gym_env.configure = lambda x: None
            gym_env.state_space = gym_env.observation_space
            gym_env.state_space.n = gym_env.state_space.shape[0]
            
        elif self.env_name in CT.MDP_envs:
            import gym_stochastic_mdp
            gym_env = gym.make(self.env_name).env
        elif self.env_name in CT.SF_envs:
            import space_fortress
            gym_env = gym.make(self.env_name)#.env
        else:
            assert False, self.env_name + str(CT.GYM_envs)
        logging.debug("Gym %s built", self.env_name)
        return gym_env
    
    
    def new_game(self, from_random_game=False):
        #if self.lives == 0:
        self.display_current_episode = random.random() < self.display_prob
        self._screen = self.gym.reset()
        
        return self.screen, 0., 0., self.terminal


    def _step(self, action):
        self._screen, self.reward, self.terminal, _ = self.gym.step(action)

    def _random_step(self):
        action = self.gym.action_space.sample()
        self._step(action)

    @property
    def screen(self):
        #return imresize(rgb2gray(self._screen)/255., self.dims)
        #return cv2.resize(cv2.cvtColor(self._screen, cv2.COLOR_BGR2YCR_CB)/255., self.dims)[:,:,0]
        return self._screen


    @property
    def lives(self):
        #return self.gym.ale.lives()
        return self.gym.lives()

    @property
    def state(self):
        return self.screen, self.reward, self.terminal

    def render(self):
        self.gym.render()

    def after_act(self, action):
        pass
#        if self.display_current_episode:
#            pass#self.render()
        
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
        

                



