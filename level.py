from snake import Snake
from maps import *
from constants import *
import colors
import random

# STATUSES
RUNNING = 0
LOST = 1
WIN = 2
GAME_OVER = 3


class Level:

    def __init__(self, name, map_name) -> None:
        self.name = name
        self.map = map_from_csv(map_name + ".csv")
        
        self.status = RUNNING
        self.start()

    def tile_at(self, x,y):
        return self.map.tiles[y][x]
    
    def message(self, text, color):

        font = pygame.font.SysFont(None, 50)
        msg = font.render(text, True, color)
        msg_rect = msg.get_rect(center=(self.map.tile_width*(tileSize/2), self.map.tile_width*(tileSize/2)))
        self.display.blit(msg, msg_rect)
    
    def new_food(self):
        while True:
            newXFoodPos = random.randrange(0, self.map.tile_width - 1)
            newYFoodPos = random.randrange(0, self.map.tile_height - 1)

            if(not (newXFoodPos, newYFoodPos) in (self.snake.positions)) and self.tile_at(newXFoodPos,newYFoodPos).allow_through(self.snake):
                break
        self.xFoodPos = newXFoodPos
        self.yFoodPos = newYFoodPos
        pygame.draw.rect(self.display, colors.red, position_to_pixel([self.xFoodPos, self.yFoodPos],1))

    def re_render_objects(self, eaten):
        """Derender moving objects"""
        self.snake.render()

        if eaten:
            food_tile = self.tile_at(self.xFoodPos,self.yFoodPos)
            pygame.draw.rect(self.display, food_tile.color, position_to_pixel([self.xFoodPos, self.yFoodPos],1))
            self.new_food()
        pygame.display.update()

    def reset_level(self):
        self.snake.return_to_initial()
        self.map.render(self.display)
        pygame.display.update()
        self.new_food()
        self.queue = []
        self.status = RUNNING

        self.run_loop()


    def start(self):
        pygame.init()
        self.display = pygame.display.set_mode((self.map.width, self.map.height))
        self.map.render(self.display)
        self.snake = Snake(self.display, (int(self.map.tile_width / 2), int(self.map.tile_height / 2)))
        self.queue = []
        self.clock = pygame.time.Clock()
        self.status = RUNNING
        pygame.display.set_caption('Snake game | ' + self.name)
        pygame.display.update()

        self.new_food()
        self.run_loop()
    
    def run_loop(self):
        while self.status != GAME_OVER:
            self.level_loop()
        pygame.quit()
    def level_loop(self):

       
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.status = GAME_OVER
                return 0
            if event.type == pygame.KEYDOWN:
                self.queue.append(event.key)

        if len(self.queue) != 0:
            key = self.queue[0]
            if key == pygame.K_UP:
                direction = Directions.UP
            if key == pygame.K_RIGHT:
                direction = Directions.RIGHT
            if key == pygame.K_DOWN:
                direction = Directions.DOWN
            if key == pygame.K_LEFT:
                direction = Directions.LEFT
            
            if direction is not None:
                self.snake.change_direction(direction)
            del self.queue[0]
        
        next_position = self.snake.get_next_position()
        next_tile = self.tile_at(next_position[0],next_position[1])
        print(next_tile)
        if not next_tile.allow_through(self.snake):
            self.status = LOST
            self.game_lost_screen()
            return 0
        eaten = (next_position[0] == self.xFoodPos) and (next_position[1] == self.yFoodPos)
        self.snake.de_render(self.map.tiles)
        self.snake.move(eaten)
        self.re_render_objects(eaten)
        self.clock.tick(gameSpeed)

    def game_lost_screen(self):
        while self.status == LOST:
            self.display.fill(colors.dark_red)
            self.message("You lost! Press Q to quit, or C to play again", colors.white)
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_q):
                    self.status = GAME_OVER
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_c:
                    self.reset_level()
            pygame.display.update()

