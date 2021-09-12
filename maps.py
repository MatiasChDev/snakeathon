from tiles import *
from constants import tileSize
def map_from_csv(file_name):
    TILE_CODES = {
        "O": Base,
        "W": Wall,
        "B": Bridge,
        "S": Stair
    }
    f = open(file_name, "r")
    lines = f.readlines()
    tiles = []
    x=0
    y=0
    for l in lines:
        row_tiles = []
        x=0
        for tile_code in l.split():
            tile_type = tile_code[0:1]
            tile_z = tile_code[1:]
            if (tile_type == "O"):
                tile = TILE_CODES[tile_type](x,y,tile_z,colors.white)
            else:
                tile = TILE_CODES[tile_type](x,y,tile_z)
            row_tiles.append(tile)
            x+=1
        tiles.append(row_tiles)
        y+=1
    return Map("Test",tiles)

class Map:
    def __init__(self,name,tiles) -> None:
        self.name = name
        self.tile_height = len(tiles)
        self.tile_width = len(tiles[0])
        self.height = tileSize*self.tile_height
        self.width = tileSize*self.tile_width
        self.tiles = tiles
    
    def render(self, display):
        print("render map")
        for row in self.tiles:
            for tile in row:
                tile.render(display)
