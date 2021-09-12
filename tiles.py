import pygame
import colors

class Tile:
    """A tile with x and y position"""
    def __init__(self,x,y,z, color) -> None:
        self.x = x
        self.y = y
        self.z = z
        self.color = color
    def allow_fall(self,snake):
        return False
    def allow_through(self,snake):
        return False
    
    def died(self, snake):
        """True if snake is  in same tile and either its a wall or the tile is in another elevation(except bridges)"""
        
        if (snake.z > self.z) and not self.allow_fall():
            return snake.fall()
    
    def render(self, display):
        pygame.draw.rect(display, self.color, [self.x*20, self.y*20, 20, 20])
    
    def __str__(self) -> str:
        return  self.__class__.__name__ + " at:(" + str(self.x) + "," + str(self.y) + "," + str(self.z) + ")"

class Base(Tile):
    """The base tile"""
    def __init__(self,x,y,z,colour) -> None:
        super().__init__(x,y,z,colour)

    def allow_through(self,snake):
        return snake.z >= int(self.z)
    

class Wall(Tile):
    """An actual wall"""
    def __init__(self,x,y,z) -> None:
        super().__init__(x,y,z,colors.black)




class Stair(Base):
    """A stair tile to change elevation level"""
    

    def __init__(self, x, y, z, dir) -> None:
        super().__init__(x,y,z, colors.grey)
        self.dir = dir # From lower to upper elevation (e.g. "UP" has the lower level under it)
    def allow_through(self, snake):
        return super().allow_through(snake) and (snake.direction % 2) == (self.direction % 2)
    def allow_fall(self,snake):
        return (snake.direction % 2) == (self.direction % 2) and (snake.get_elevation() == self.z + 1)


class Bridge(Base):
    """A Bridge"""
    def __init__(self, x, y, z, dir) -> None:
        super().__init__(x,y,z,colors.brown)
        self.dir = dir # UP/DOWN and LEFT/RIGHT are the same
    def allow_through(self, snake):
        return True
