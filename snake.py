import pygame
import colors
import constants
import math

#STATUSES
ALIVE = 0
CRASHED = 1
FELL = 2


class Snake:

    def __init__(self, display, initial_position) -> None:
        self.z = 1
        self.display = display
        self.initial_position = initial_position
        self.head_position = initial_position
        self.positions = [initial_position]
        self.status = ALIVE
        self.direction = None
    
    def get_elevation(self):
        return self.z
    def return_to_initial(self):
        self.positions = [self.initial_position]
        self.head_position = self.initial_position
        self.status = ALIVE
        self.direction = None
    
    def change_direction(self, direction):
        print(direction)
        if (len(self.positions) == 1) or (constants.Directions.opposite_direction(direction) != self.direction):
            self.direction = direction

    def fall(self):
        self.status = FELL
    def crash(self):
        self.status = CRASHED

    def get_deltas(self):
        return constants.Directions.to_delta(self.direction)
    def get_next_position(self):
        if self.direction is None:
            return self.head_position
        deltas = self.get_deltas()
        newX = self.head_position[0] + deltas[0]
        newY = self.head_position[1] + deltas[1]
        return (newX, newY)
    
    def move(self, eaten):
        next_pos = self.get_next_position()
        self.positions.append(next_pos)
        self.head_position = next_pos
        if not eaten:
            del self.positions[0]



    def de_render(self, tiles):
        for position in self.positions:
            tile = tiles[position[1]][position[0]]
            pygame.draw.rect(self.display, tile.color, constants.position_to_pixel(position,0))

    def render(self, map):
        for position in self.positions:
            pygame.draw.rect(self.display, colors.blue, constants.position_to_pixel(position,1))
        if (self.direction is not None):
            viewOffset = math.tan(constants.fov)*constants.view_distance
            gradientStep = 255/constants.view_circle_size
            surf1 = pygame.Surface((map.width, map.height), pygame.SRCALPHA)
            surf2 = pygame.Surface((map.width, map.height), pygame.SRCALPHA)
            surf3 = pygame.Surface((map.width, map.height), pygame.SRCALPHA)
            surf4 = pygame.Surface((map.width, map.height), pygame.SRCALPHA) 
            pygame.draw.circle(
                surf1, (255, 0, 0, 255), 
                (self.head_position[0]*constants.tileSize + constants.tileSize/2, self.head_position[1]*constants.tileSize + constants.tileSize/2), 
                constants.view_distance
            )
            pygame.draw.polygon(surf2, (0, 0, 0, 255), [(0,0),(0,map.height),(map.width,map.height),(map.width,0)])
            
            for x in range(constants.view_circle_size):
                pygame.draw.circle(surf3, (0, 0, 0, gradientStep* x), (self.head_position[0]*constants.tileSize + constants.tileSize/2,self.head_position[1]*constants.tileSize + constants.tileSize/2), constants.view_circle_size - x)

            for x in range(constants.view_distance):
                pygame.draw.circle(surf4, (0, 0, 0, (255/constants.view_distance)* x), (self.head_position[0]*constants.tileSize + constants.tileSize/2,self.head_position[1]*constants.tileSize + constants.tileSize/2), constants.view_distance - x)

            if(self.direction == constants.Directions.DOWN): #moving down
                pygame.draw.polygon(
                    surf3,
                    (255,0,0,150),
                    [
                        (self.head_position[0]*constants.tileSize + constants.tileSize/2, self.head_position[1]*constants.tileSize + constants.tileSize/2),(self.head_position[0]*constants.tileSize + constants.tileSize/2 + viewOffset,self.head_position[1]*constants.tileSize + constants.tileSize/2 + constants.view_distance),(self.head_position[0]*constants.tileSize + constants.tileSize/2 - viewOffset,self.head_position[1]*constants.tileSize + constants.tileSize/2 + constants.view_distance)
                    ]
                )
            elif(self.direction == constants.Directions.UP): #moving up
                pygame.draw.polygon(surf3,(255,0,0,150),[(self.head_position[0]*constants.tileSize + constants.tileSize/2, self.head_position[1]*constants.tileSize + constants.tileSize/2),(self.head_position[0]*constants.tileSize + constants.tileSize/2 + viewOffset,self.head_position[1]*constants.tileSize + constants.tileSize/2 - constants.view_distance),(self.head_position[0]*constants.tileSize + constants.tileSize/2 - viewOffset,self.head_position[1]*constants.tileSize + constants.tileSize/2 - constants.view_distance)])
            elif(self.direction == constants.Directions.RIGHT): #moving right
                pygame.draw.polygon(surf3,(255,0,0,150),[(self.head_position[0]*constants.tileSize + constants.tileSize/2, self.head_position[1]*constants.tileSize + constants.tileSize/2),(self.head_position[0]*constants.tileSize + constants.tileSize/2 + constants.view_distance,self.head_position[1]*constants.tileSize + constants.tileSize/2 - viewOffset),(self.head_position[0]*constants.tileSize + constants.tileSize/2 + constants.view_distance,self.head_position[1]*constants.tileSize + constants.tileSize/2 + viewOffset)])
            else: #moving left
                pygame.draw.polygon(surf3,(255,0,0,150),[(self.head_position[0]*constants.tileSize + constants.tileSize/2, self.head_position[1]*constants.tileSize + constants.tileSize/2),(self.head_position[0]*constants.tileSize + constants.tileSize/2 - constants.view_distance,self.head_position[1]*constants.tileSize + constants.tileSize/2 - viewOffset),(self.head_position[0]*constants.tileSize + constants.tileSize/2 - constants.view_distance,self.head_position[1]*constants.tileSize + constants.tileSize/2 + viewOffset)])
            
            surf1.blit(surf3, (0, 0), special_flags = pygame.BLEND_RGBA_MIN)
            surf3.blit(surf1, (0, 0), special_flags = pygame.BLEND_RGBA_SUB)

            surf1.blit(surf2, (0, 0), special_flags = pygame.BLEND_RGBA_MIN)
            surf2.blit(surf1, (0, 0), special_flags = pygame.BLEND_RGBA_SUB)

            surf1.blit(surf2, (0, 0), special_flags = pygame.BLEND_RGBA_MIN)
            surf2.blit(surf4, (0, 0), special_flags = pygame.BLEND_RGBA_SUB)

            self.display.blit(surf2,(0,0))
            
            pygame.display.update()