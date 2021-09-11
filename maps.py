from tiles import *
def render_from_csv(file_name):
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
        y=0
        for tile_code in l.split():
            tile_type = tile_code[0:1]
            tile_z = tile_code[1:]
            if (tile_type == "O"):
                tile = TILE_CODES[tile_type](x,y,tile_z)
            else:
                tile = TILE_CODES[tile_type](x,y,tile_z,COLOUR.white)
            row_tiles.append()
        x+=1
class Map:
    def __init__(self,name,tiles) -> None:
        self.name = name
        self.height = len(tiles)
        self.width = len(tiles[0])
        self.tiles = tiles
    
    def render(self):
        for row in self.tiles:
            for tile in row:
                tile.render()
