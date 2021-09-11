import pygame
class State:
    ALIVE = 0
    CRASHED = 1
    FELL = 2
    HIT = 3

class COLOUR:
    blue = (0, 0, 255)
    red = (255, 0, 0)
    black = (0, 0, 0)
    grey = (100,100,100)
    white = (255, 255, 255)
    brown = (155,103,60)

class Tile:
    """A tile with x and y position"""
    def __init__(self,x,y,z, colour) -> None:
        self.x = x
        self.y = y
        self.z = z
        self.colour = colour
    def allow_fall(self,snake):
        return False
    def allow_through(self,snake):
        return False
    
    def died(self, snake):
        """True if snake is  in same tile and either its a wall or the tile is in another elevation(except bridges)"""
        snake_z =  snake.get_elevation()
        if snake_z > self.z and not self.allow_fall():
            return State.FELL
    
    def render(self, display):
        pygame.draw.rect(display, self.colour, [self.x*20, self.y*20, 20, 20])

class Base(Tile):
    """The base tile"""
    def __init__(self,x,y,z,colour) -> None:
        super().__init__(x,y,z,colour)

    def allow_through(self,snake):
        return snake.get_elevation() >= self.z
    

class Wall(Tile):
    """An actual wall"""
    def __init__(self,x,y,z) -> None:
        super().__init__(x,y,z,COLOUR.black)


DIRECTIONS = {
        "UP":0,
        "RIGHT":1,
        "DOWN":2,
        "LEFT":3
    }

class Stair(Base):
    """A stair tile to change elevation level"""
    

    def __init__(self, x, y, z, dir) -> None:
        super().__init__(x,y,z, COLOUR.grey)
        self.dir = dir # From lower to upper elevation (e.g. "UP" has the lower level under it)
    def allow_through(self, snake):
        return super().allow_through(snake) and (snake.direction % 2) == (self.direction % 2)
    def allow_fall(self,snake):
        return (snake.direction % 2) == (self.direction % 2) and (snake.get_elevation() == self.z + 1)


class Bridge(Base):
    """A Bridge"""
    def __init__(self, x, y, z, dir) -> None:
        super().__init__(x,y,z,COLOUR.brown)
        self.dir = dir # UP/DOWN and LEFT/RIGHT are the same
    def allow_through(self, snake):
        return True
