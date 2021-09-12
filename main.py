import pygame
import time
import random
import math
from colors import *
from constants import *
import pygame_gui
import level

pygame.init()

window_surface = pygame.display.set_mode((display_width, display_height))
background = pygame.Surface((display_width, display_height))
background.fill(pygame.Color(grey))

pygame.display.set_caption('Snake game')
pygame.display.update()

manager = pygame_gui.UIManager((display_width, display_height))
hello_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((display_width/2 - 50, display_height/2 - 25), (100, 50)),
                                             text='Start Game',
                                             manager=manager)
game_over = False

font = pygame.font.SysFont(None, 50)

clock = pygame.time.Clock()

viewOffset = math.tan(fov)*view_distance
gradientStep = 255/view_circle_size
print(gradientStep)

def message(text, color):
    msg = font.render(text, True, color)
    msg_rect = msg.get_rect(center=(display_width/2, display_height/2))
    window_surface.blit(msg, msg_rect)

is_running = True

while is_running:
    time_delta = clock.tick(60)/1000.0
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            is_running = False
            
        if event.type == pygame.USEREVENT:
            if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == hello_button:
                    hello_button.hide()
                    level.Level("Level Test","test_map")
                    pygame.init()

                    window_surface = pygame.display.set_mode((display_width, display_height))
                    background = pygame.Surface((display_width, display_height))
                    background.fill(pygame.Color(grey))

                    pygame.display.set_caption('Snake game')
                    pygame.display.update()
                    hello_button.show()
            
        manager.process_events(event)
    
    manager.update(time_delta)
    
    window_surface.blit(background, (0, 0))
    manager.draw_ui(window_surface)
    
    pygame.display.update()