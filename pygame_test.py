# -*- coding: utf-8 -*-
# jmcgee

import time
import numpy as np
import pygame
from pygame.locals import *
from cellular import Cellular


game_dim = (80, 60)
disp_dim = (1000, 800)

dtype = np.int8  
game_tmp = np.ndarray(game_dim, dtype=dtype)
depth = 8
max_int = 2**8/2 - 1

def handle_events():
    e = pygame.event.poll()
    if e.type == pygame.locals.QUIT: raise SystemExit
    #elif e.type == pygame.locals.KEYDOWN: break

def mapgen(dim, passes=20):
    c = Cellular(dim, orthogonal=True)
    for i in xrange(passes):
        if c.cellular_next_step(2, 4, 4):
            break
        
    return c.state

def show_array(data_array, data_surf, disp_surf):
    np.multiply(max_int, data_array, out=game_tmp)
    pygame.surfarray.blit_array(data_surf, game_tmp)
    pygame.transform.scale(data_surf, disp_surf.get_size(), disp_surf)
    pygame.display.update()

def main_loop():
    step = 0
    while True:
        show_array(game_state, game_surf, screen_surf)
        handle_events()
        step += 1
        time.sleep(0.01)

pygame.init()
screen_surf = pygame.display.set_mode(disp_dim, 0, depth)
game_surf = pygame.Surface(game_dim, 0, depth)

game_state = mapgen(game_dim)
main_loop()