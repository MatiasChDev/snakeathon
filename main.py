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
def draw_snake(tileSize, snake_list):
    for x in snake_list:
        pygame.draw.rect(window_surface, white, [x[0]+1, x[1]+1, tileSize-2, tileSize-2])

def message(text, color):
    msg = font.render(text, True, color)
    msg_rect = msg.get_rect(center=(display_width/2, display_height/2))
    window_surface.blit(msg, msg_rect)
def generateFoodPosition(snakeList):
    while True:
        xFoodPos = round(random.randrange(0, display_width - tileSize) / tileSize ) * tileSize
        yFoodPos = round(random.randrange(0, display_height - tileSize) / tileSize ) * tileSize
        if(not (xFoodPos,yFoodPos) in (snakeList)):
            break
    return xFoodPos,yFoodPos

def gameLoop():
    game_over = False
    game_lost = False
    
    xPos = display_width/2
    yPos = display_height/2
    xChange = 0
    yChange = 0
    
    lastCommand = None
    
    queue = []
    snake_list = []
    lengthOfSnake = 1

    xFoodPos,yFoodPos = generateFoodPosition(snake_list)

    while not game_over:

        if (xPos >= display_width or xPos < 0 or yPos >= display_height or yPos < 0):
            game_lost = True
        
        while game_lost == True:
            time_delta = clock.tick(60)/1000.0
            # window_surface.fill(black)
            # message("You lost! Press Q to quit, or C to play again", red)
            window_surface.blit(background, (0, 0))
            play_again.show()
            quit_game.show()
            manager.update(time_delta)
            window_surface.blit(background, (0, 0))
            manager.draw_ui(window_surface)
            pygame.display.update()
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game_over = True
                    game_lost=False
                if event.type == pygame.USEREVENT:
                    if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                        if event.ui_element == play_again:
                            gameLoop()
                        if event.ui_element == quit_game:
                            game_over = True
                            game_lost=False
                        play_again.hide()
                        quit_game.hide()
            
            manager.process_events(event)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                queue.append(event.key)

        if len(queue) != 0:
            if queue[0] == pygame.K_LEFT and lastCommand != pygame.K_RIGHT:
                xChange = -tileSize
                yChange = 0
                lastCommand = pygame.K_LEFT
            if queue[0] == pygame.K_RIGHT and lastCommand != pygame.K_LEFT:
                xChange = tileSize
                yChange = 0
                lastCommand = pygame.K_RIGHT
            if queue[0] == pygame.K_UP and lastCommand != pygame.K_DOWN:
                xChange = 0
                lastCommand = pygame.K_UP
                yChange = -tileSize
            if queue[0] == pygame.K_DOWN and lastCommand != pygame.K_UP:
                xChange = 0
                yChange = tileSize
                lastCommand = pygame.K_DOWN
            del queue[0]
        xPos += xChange
        yPos += yChange

        window_surface.fill(black)
              
        # Draw food
        snake_head = []
        snake_head.append(xPos)
        snake_head.append(yPos)
        snake_list.append(snake_head)
        if len(snake_list) > lengthOfSnake:
            del snake_list[0]
        
        if snake_head in snake_list[:-1]:
            game_lost=True
        window_surface.blit(background, (0, 0))
        pygame.draw.rect(window_surface, red, [xFoodPos+1, yFoodPos+1, tileSize-2, tileSize-2])
        draw_snake(tileSize, snake_list)
        
        
        if(not (xChange == 0 and  yChange == 0)):
            surf1 = pygame.Surface((display_width, display_height), pygame.SRCALPHA)
            surf2 = pygame.Surface((display_width, display_height), pygame.SRCALPHA)
            surf3 = pygame.Surface((display_width, display_height), pygame.SRCALPHA)
            surf4 = pygame.Surface((display_width, display_height), pygame.SRCALPHA) 
            pygame.draw.circle(surf1, (255, 0, 0, 255), (xPos + tileSize/2,yPos + tileSize/2), view_distance)
            pygame.draw.polygon(surf2, (0, 0, 0, 255), [(0,0),(0,display_height),(display_width,display_height),(display_width,0)])
            
            for x in range(view_circle_size):
                pygame.draw.circle(surf3, (0, 0, 0, gradientStep* x), (xPos + tileSize/2,yPos + tileSize/2), view_circle_size - x)

            for x in range(view_distance):
                pygame.draw.circle(surf4, (0, 0, 0, (255/view_distance)* x), (xPos + tileSize/2,yPos + tileSize/2), view_distance - x)

            if(xChange == 0):
                if(yChange > 0): #moving down
                    pygame.draw.polygon(surf3,(255,0,0,150),[(xPos + tileSize/2, yPos + tileSize/2),(xPos + tileSize/2 + viewOffset,yPos + tileSize/2 + view_distance),(xPos + tileSize/2 - viewOffset,yPos + tileSize/2 + view_distance)])
                else: #moving up
                    pygame.draw.polygon(surf3,(255,0,0,150),[(xPos + tileSize/2, yPos + tileSize/2),(xPos + tileSize/2 + viewOffset,yPos + tileSize/2 - view_distance),(xPos + tileSize/2 - viewOffset,yPos + tileSize/2 - view_distance)])
            if(yChange == 0):
                if(xChange > 0): #moving right
                    pygame.draw.polygon(surf3,(255,0,0,150),[(xPos + tileSize/2, yPos + tileSize/2),(xPos + tileSize/2 + view_distance,yPos + tileSize/2 - viewOffset),(xPos + tileSize/2 + view_distance,yPos + tileSize/2 + viewOffset)])
                else: #moving left
                    pygame.draw.polygon(surf3,(255,0,0,150),[(xPos + tileSize/2, yPos + tileSize/2),(xPos + tileSize/2 - view_distance,yPos + tileSize/2 - viewOffset),(xPos + tileSize/2 - view_distance,yPos + tileSize/2 + viewOffset)])
            
            
            surf1.blit(surf3, (0, 0), special_flags = pygame.BLEND_RGBA_MIN)
            surf3.blit(surf1, (0, 0), special_flags = pygame.BLEND_RGBA_SUB)

            surf1.blit(surf2, (0, 0), special_flags = pygame.BLEND_RGBA_MIN)
            surf2.blit(surf1, (0, 0), special_flags = pygame.BLEND_RGBA_SUB)

            surf1.blit(surf2, (0, 0), special_flags = pygame.BLEND_RGBA_MIN)
            surf2.blit(surf4, (0, 0), special_flags = pygame.BLEND_RGBA_SUB)

            window_surface.blit(surf2,(0,0))
        pygame.display.update()
        
        if xPos == xFoodPos and yPos == yFoodPos:
            xFoodPos,yFoodPos = generateFoodPosition(snake_list)
            lengthOfSnake += 1
        clock.tick(gameSpeed)

    pygame.quit()
    quit()

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