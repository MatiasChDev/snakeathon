class Tile:
    """A tile with x and y position"""
    def __init__(self,x,y,z, wall) -> None:
        self.x = x
        self.y = y
        self.z = z
        self.wall = wall

class Base(Tile):
    """The base tile"""
    def __init__(self,x,y,z) -> None:
        super().__init__(x,y,z,False)

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


class Bridge(Base):
    """A Bridge"""
    def __init__(self, x, y, z, dir) -> None:
        super().__init__(x,y,z)
        self.dir = dir # UP/DOWN and LEFT/RIGHT are the same
