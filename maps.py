from tiles import *
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
        y=0
        for tile_code in l.split():
            tile_type = tile_code[0:1]
            tile_z = tile_code[1:]
            if (tile_type == "O"):
                tile = TILE_CODES[tile_type](x,y,tile_z,COLOUR.white)
            else:
                tile = TILE_CODES[tile_type](x,y,tile_z)
            row_tiles.append(tile)
            y+=1
        tiles.append(row_tiles)
        x+=1
    return Map("Test",tiles)
class Map:
    def __init__(self,name,tiles) -> None:
        self.name = name
        self.width = len(tiles)
        self.height = len(tiles[0])
        self.tiles = tiles
    
    def render(self):
        print(self.width,self.height)
        display = pygame.display.set_mode((20*self.width, 20*self.height))
        for row in self.tiles:
            for tile in row:
                tile.render(display)
        pygame.display.set_caption('Snake game')
        clock = pygame.time.Clock()
        game_over = False
        while not game_over:
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game_over = True
        pygame.quit()
pygame.init()
test_map = map_from_csv("test_map.csv")
test_map.render()
