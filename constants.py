display_width = 800
display_height = 600
tileSize = 20
gameSpeed = 10


class Directions:
    UP=0
    RIGHT=1
    DOWN=2
    LEFT=3

    def to_delta(direction):
        negator = -1 if direction == 0 or direction==3 else 1
        xChange = negator*(direction % 2)
        yChange = negator*((direction-1) % 2)
        return (xChange,yChange)
    def opposite_direction(direction):
        return direction + (1 if direction < 2 else -1)*2

def position_to_pixel(position, padding):
    return [
        tileSize*position[0] + padding,tileSize*position[1] + padding,
        tileSize - 2*padding, tileSize - 2*padding
    ]
