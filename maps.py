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
    