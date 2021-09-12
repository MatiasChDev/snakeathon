import pygame
import time
import random
import math
from colors import *
from constants import *

pygame.init()

display = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption('Snake game')
pygame.display.update()

game_over = False

font = pygame.font.SysFont(None, 50)

clock = pygame.time.Clock()

viewOffset = math.tan(fov)*view_distance
gradientStep = 255/view_circle_size
print(gradientStep)
def draw_snake(tileSize, snake_list):
    for x in snake_list:
        pygame.draw.rect(display, black, [x[0]+1, x[1]+1, tileSize-2, tileSize-2])

def message(text, color):
    msg = font.render(text, True, color)
    msg_rect = msg.get_rect(center=(display_width/2, display_height/2))
    display.blit(msg, msg_rect)
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
            display.fill(blue)
            message("You lost! Press Q to quit, or C to play again", red)
            pygame.display.update()
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game_over = True
                    game_lost=False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over = True
                        game_lost=False
                    if event.key == pygame.K_c:
                        gameLoop()
        
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

        display.fill(blue)
              
        # Draw food
        pygame.draw.rect(display, red, [xFoodPos+1, yFoodPos+1, tileSize-2, tileSize-2])
        snake_head = []
        snake_head.append(xPos)
        snake_head.append(yPos)
        snake_list.append(snake_head)
        if len(snake_list) > lengthOfSnake:
            del snake_list[0]
        
        if snake_head in snake_list[:-1]:
            game_lost=True
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
                    pygame.draw.polygon(surf3,(255,0,0,255),[(xPos + tileSize/2, yPos + tileSize/2),(xPos + tileSize/2 + viewOffset,yPos + tileSize/2 + view_distance),(xPos + tileSize/2 - viewOffset,yPos + tileSize/2 + view_distance)])
                else: #moving up
                    pygame.draw.polygon(surf3,(255,0,0,255),[(xPos + tileSize/2, yPos + tileSize/2),(xPos + tileSize/2 + viewOffset,yPos + tileSize/2 - view_distance),(xPos + tileSize/2 - viewOffset,yPos + tileSize/2 - view_distance)])
            if(yChange == 0):
                if(xChange > 0): #moving right
                    pygame.draw.polygon(surf3,(255,0,0,255),[(xPos + tileSize/2, yPos + tileSize/2),(xPos + tileSize/2 + view_distance,yPos + tileSize/2 - viewOffset),(xPos + tileSize/2 + view_distance,yPos + tileSize/2 + viewOffset)])
                else: #moving left
                    pygame.draw.polygon(surf3,(255,0,0,255),[(xPos + tileSize/2, yPos + tileSize/2),(xPos + tileSize/2 - view_distance,yPos + tileSize/2 - viewOffset),(xPos + tileSize/2 - view_distance,yPos + tileSize/2 + viewOffset)])
            
            
            surf1.blit(surf3, (0, 0), special_flags = pygame.BLEND_RGBA_MIN)
            surf3.blit(surf1, (0, 0), special_flags = pygame.BLEND_RGBA_SUB)

            surf1.blit(surf2, (0, 0), special_flags = pygame.BLEND_RGBA_MIN)
            surf2.blit(surf1, (0, 0), special_flags = pygame.BLEND_RGBA_SUB)

            surf1.blit(surf2, (0, 0), special_flags = pygame.BLEND_RGBA_MIN)
            surf2.blit(surf4, (0, 0), special_flags = pygame.BLEND_RGBA_SUB)

            display.blit(surf2,(0,0))
        pygame.display.update()
        
        if xPos == xFoodPos and yPos == yFoodPos:
            xFoodPos,yFoodPos = generateFoodPosition(snake_list)
            lengthOfSnake += 1
        clock.tick(gameSpeed)

    pygame.quit()
    quit()  


gameLoop()