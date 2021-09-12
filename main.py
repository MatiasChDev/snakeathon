import pygame
import time
import random
import math
from colors import *
from constants import *
import level

pygame.init()

window_surface = pygame.display.set_mode((display_width, display_height))
background = pygame.Surface((display_width, display_height))
background.fill(pygame.Color(grey))

pygame.display.set_caption('Snake game')
pygame.display.update()

game_over = False

font = pygame.font.SysFont(None, 50)

clock = pygame.time.Clock()

viewOffset = math.tan(fov)*view_distance
gradientStep = 255/view_circle_size

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
            
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                
                level.Level("Level Test")
                pygame.init()
                window_surface = pygame.display.set_mode((display_width, display_height))
                background = pygame.Surface((display_width, display_height))
                background.fill(pygame.Color(grey))
                pygame.display.set_caption('Snake game')
                pygame.display.update()
    
    window_surface.blit(background, (0, 0))
    message("Press space to start.", blue)
    pygame.display.update()