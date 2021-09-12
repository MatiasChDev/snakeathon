from tiles import *
from colors import *
from constants import tileSize
import random
import sys
import os

def resource_path(relative_path):
    try:
    # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

def map_from_csv():
    ran_map = random.randrange(0,2)
    maps = ["test_map","test_map2"]
    file_name = maps[ran_map]
    TILE_CODES = {
        "O": Base,
        "W": Wall,
        "B": Bridge,
        "S": Stair
    }
    f = open(resource_path(file_name + ".csv"), "r")
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
    return Map(file_name,tiles)

class Map:
    def __init__(self,name,tiles) -> None:
        self.name = name
        self.tile_height = len(tiles)
        self.tile_width = len(tiles[0])
        self.height = tileSize*self.tile_height
        self.width = tileSize*self.tile_width
        self.tiles = tiles
    
    def render(self, display):
        for row in self.tiles:
            for tile in row:
                tile.render(display)
    def moveUp(self):
        for y in range(1,len(self.tiles) -1):
            row = self.tiles[y]
            for x in range(1,len(row) - 1):
                tile = row[x]
                if(tile.__class__.__name__ == "Wall"):
                    tile.y-=1
                    self.tiles[y-1][x] = tile
                    row[x] = Base(tile.x,tile.y + 1,tile.z,white)

            # spawn new walls
        numWalls = round(random.randrange(1,5))
        ran = round(random.randrange(1,self.tile_width - numWalls))
        for x in range(numWalls):
            self.tiles[self.tile_height - 2 ][ran + x] = Wall(ran + x,self.tile_height - 2,1)






                    
