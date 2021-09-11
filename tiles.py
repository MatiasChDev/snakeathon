class State:
    ALIVE = 0
    CRASHED = 1
    FELL = 2
    HIT = 3

class Tile:
    """A tile with x and y position"""
    def __init__(self,x,y,z, colour) -> None:
        self.x = x
        self.y = y
        self.z = z
    def allow_fall(self,snake):
        return False
    def allow_through(self,snake):
        return False
    
    def died(self, snake):
        """True if snake is  in same tile and either its a wall or the tile is in another elevation(except bridges)"""
        snake_z =  snake.get_elevation()
        if snake_z > self.z and not self.allow_fall():
            return State.FELL
        pass

class Base(Tile):
    """The base tile"""
    def __init__(self,x,y,z) -> None:
        super().__init__(x,y,z,False)

    def allow_through(self,snake):
        return snake.get_elevation() >= self.z
    

class Wall(Tile):
    """An actual wall"""
    def __init__(self,x,y,z) -> None:
        super().__init__(x,y,z,True)


DIRECTIONS = {
        "UP":0,
        "RIGHT":1,
        "DOWN":2,
        "LEFT":3
    }

class Stair(Base):
    """A stair tile to change elevation level"""
    

    def __init__(self, x, y, z, dir) -> None:
        super().__init__(x,y,z)
        self.dir = dir # From lower to upper elevation (e.g. "UP" has the lower level under it)
    def allow_through(self, snake):
        return super().allow_through(snake) and (snake.direction % 2) == (self.direction % 2)
    def allow_fall(self,snake):
        return (snake.direction % 2) == (self.direction % 2) and (snake.get_elevation() == self.z + 1)


class Bridge(Base):
    """A Bridge"""
    def __init__(self, x, y, z, dir) -> None:
        super().__init__(x,y,z)
        self.dir = dir # UP/DOWN and LEFT/RIGHT are the same
    def allow_through(self, snake):
        return True
