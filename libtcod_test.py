import os
import libtcodpy as libtcod
import random
import numpy

#init
screen_w = 78
screen_h = 48
screen_x = 1
screen_y = 1

orange = libtcod.Color(240, 85, 5)
blue = libtcod.Color(0, 85, 240)

font = os.path.join('data', 'fonts', 'consolas10x10_gs_tc.png')
libtcod.console_set_custom_font(font, libtcod.FONT_TYPE_GREYSCALE | libtcod.FONT_LAYOUT_TCOD)
libtcod.console_init_root(80, 50, 'libtcod python sample', False)
game_console = libtcod.console_new(screen_w, screen_h)

key = libtcod.Key()
mouse = libtcod.Mouse()

def allowed_directions(cmap, x, y, w, h):
    directions = []
    if x != 0 and cmap[x-1][y] == '#':
        directions.append((-1, 0))
    if y != 0 and cmap[x][y-1] == '#':
        directions.append((0, -1))
    if x != w - 1 and cmap[x+1][y] == '#':
        directions.append((1, 0))
    if y != h - 1 and cmap[x][y+1] == '#':
        directions.append((0, 1))
    return directions

#random walk, not so good...
def generate_level(w, h):
    level_map = [['#' for y in xrange(h)] for x in xrange(w)]
    x, y = (0, 0)
    while True:
        allowed = allowed_directions(level_map, x, y, w, h)
        if not allowed:
            level_map[x][y] = '!'
            break
        else:
            dx, dy = random.choice(allowed)
            x, y = (x + dx, y + dy)
            level_map[x][y] = ' '
    return level_map

#TODO: refactor, structure to bind keypress -> actions?
def handle_input(key, mouse):
    if key.vk == libtcod.KEY_ENTER and key.lalt:
        print 'fullscreen'
        libtcod.console_set_fullscreen(not libtcod.console_is_fullscreen())
    elif key.vk == libtcod.KEY_PRINTSCREEN or key.c == 'p':
        print "screenshot"
        if key.lalt :
            libtcod.console_save_apf(None,"samples.apf")
            print "apf"
        else :
            libtcod.sys_save_screenshot()
            print "png"
    elif key.vk == libtcod.KEY_ESCAPE:
        return True

def render(cmap):
    for y in range(screen_h):
        for x in range(screen_w):
            if cmap[x][y] == '#':
                libtcod.console_set_char_background(game_console, x, y, orange, libtcod.BKGND_SET)
            if cmap[x][y] == '!':
                libtcod.console_set_char_background(game_console, x, y, blue, libtcod.BKGND_SET)
                

def main_loop(cmap):
    while not libtcod.console_is_window_closed():
        libtcod.sys_check_for_event(libtcod.EVENT_KEY_PRESS|libtcod.EVENT_MOUSE, key, mouse)
        render(cmap)
        libtcod.console_blit(game_console, 0, 0, screen_w, screen_h, 0, screen_x, screen_y)
        libtcod.console_set_default_foreground(None,libtcod.grey)
        libtcod.console_set_default_background(None,libtcod.black)
        if handle_input(key, mouse):
             raise SystemExit
        libtcod.console_flush()

level_map = generate_level(screen_w, screen_h)
main_loop(level_map)