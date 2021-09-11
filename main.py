import pygame
import time

pygame.init()

display_width = 800
display_height = 600
display = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption('Snake game')
pygame.display.update()

game_over = False

blue = (0, 0, 255)
red = (255, 0, 0)
black = (0, 0, 0)
white = (255, 255, 255)

font = pygame.font.SysFont(None, 50)

xPos = display_width/2
yPos = display_height/2

xChange = 0
yChange = 0

tileSize = 20
gameSpeed = 10

clock = pygame.time.Clock()

def message(text, color):
    msg = font.render(text, True, color)
    display.blit(msg, [display_width/2, display_height/2])

while not game_over:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_over = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                xChange = -tileSize
                yChange = 0
            if event.key == pygame.K_RIGHT:
                xChange = tileSize
                yChange = 0
            if event.key == pygame.K_UP:
                xChange = 0
                yChange = -tileSize
            if event.key == pygame.K_DOWN:
                xChange = 0
                yChange = tileSize
      
    if (xPos >= display_width or xPos <= 0 or yPos >= display_height or yPos <= 0):
        game_over = True
    
    xPos += xChange
    yPos += yChange
    
    display.fill(blue)
    
    pygame.draw.rect(display, white, [xPos, yPos, tileSize, tileSize])
    pygame.display.update()
    
    clock.tick(gameSpeed)

message("You lost", red)
pygame.display.update()
time.sleep(1)

pygame.quit()
quit()
