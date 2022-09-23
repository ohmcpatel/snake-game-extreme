from time import sleep
import pygame
import random
from enum import Enum
from collections import namedtuple

pygame.init()
font = pygame.font.Font('arial.ttf', 25)
font2 = pygame.font.Font('SnakeGameDemoRegular.ttf', 65)
font3 = pygame.font.Font('SystemsAnalysis.ttf', 65)

class Direction(Enum):
    RIGHT = 1
    LEFT = 2
    UP = 3
    DOWN = 4
    
Point = namedtuple('Point', 'x, y')

# rgb colors
WHITE = (255, 255, 255)
RED = (200,0,0)
BLUE1 = (0, 0, 255)
BLUE2 = (0, 100, 255)
BLACK = (0,0,0)
GREEN = (175, 215, 70)

BLOCK_SIZE = 20
SPEED = 20

class SnakeGame:
    
    def __init__(self, w=640, h=480):
        self.w = w
        self.h = h
        # init display
        self.display = pygame.display.set_mode((self.w, self.h))
        pygame.display.set_caption('Snake')
        self.clock = pygame.time.Clock()
        
        # init game state
        self.direction = Direction.RIGHT
        
        self.head = Point(self.w/2, self.h/2)
        self.snake = [self.head, 
                      Point(self.head.x-BLOCK_SIZE, self.head.y),
                      Point(self.head.x-(2*BLOCK_SIZE), self.head.y)]
        
        self.score = 0
        self.food = None
        self.bomb = None
        self._place_food()
        self._place_bomb()
        
    def _place_food(self):
        x = random.randint(0, (self.w-BLOCK_SIZE )//BLOCK_SIZE )*BLOCK_SIZE 
        y = random.randint(0, (self.h-BLOCK_SIZE )//BLOCK_SIZE )*BLOCK_SIZE
        self.food = Point(x, y)
        if self.food in self.snake:
            self._place_food()
            self._place_bomb()
    
    def _place_bomb(self):
        x = random.randint(0, (self.w-BLOCK_SIZE )//BLOCK_SIZE )*BLOCK_SIZE 
        y = random.randint(0, (self.h-BLOCK_SIZE )//BLOCK_SIZE )*BLOCK_SIZE
        self.bomb = Point(x, y)
        if self.bomb in self.snake:
            return game_over
        
    def play_step(self):
        # 1. collect user input
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and self.direction != Direction.RIGHT:
                    self.direction = Direction.LEFT
                elif event.key == pygame.K_RIGHT and self.direction != Direction.LEFT:
                    self.direction = Direction.RIGHT
                elif event.key == pygame.K_UP and self.direction != Direction.DOWN:
                    self.direction = Direction.UP
                elif event.key == pygame.K_DOWN and self.direction != Direction.UP:
                    self.direction = Direction.DOWN
        
        # 2. move
        self._move(self.direction) # update head
        self.snake.insert(0, self.head)
        
        # 3. check if game is over
        game_over = False
        if self._is_collision() or self._is_blown_up():
            game_over = True
            return game_over, self.score
            
        # 4. place new food or move
        if self.head == self.food:
            self.score += 1
            self._place_food()
            self._place_bomb()
        else:
            self.snake.pop()
        
        #place bomb 
        
        # 5. update ui and clock
        self._update_ui()
        self.clock.tick(SPEED)
        # 6. return game over and score
        return game_over, self.score
    
    def _is_collision(self):
        # hits boundary
        if self.head.x > self.w - BLOCK_SIZE or self.head.x < 0 or self.head.y > self.h - BLOCK_SIZE or self.head.y < 0:
            return True
        # hits itself
        if self.head in self.snake[1:]:
            return True
        
        return False
    
    def _is_blown_up(self):
        if self.head == self.bomb:
            return True
        
    def _update_ui(self):
        self.display.fill(GREEN)
        
        for pt in self.snake:
            pygame.draw.rect(self.display, BLUE1, pygame.Rect(pt.x, pt.y, BLOCK_SIZE, BLOCK_SIZE))
            pygame.draw.rect(self.display, BLUE2, pygame.Rect(pt.x+4, pt.y+4, 12, 12))
            
        pygame.draw.rect(self.display, RED, pygame.Rect(self.food.x, self.food.y, BLOCK_SIZE, BLOCK_SIZE))
        pygame.draw.rect(self.display, BLACK, pygame.Rect(self.bomb.x, self.bomb.y, BLOCK_SIZE, BLOCK_SIZE))
        
        text = font.render("Score: " + str(self.score), True, BLACK)
        self.display.blit(text, [0, 0])
        pygame.display.flip()
        
    def _move(self, direction):
        x = self.head.x
        y = self.head.y
        if direction == Direction.RIGHT:
            x += BLOCK_SIZE
        elif direction == Direction.LEFT:
            x -= BLOCK_SIZE
        elif direction == Direction.DOWN:
            y += BLOCK_SIZE
        elif direction == Direction.UP:
            y -= BLOCK_SIZE
            
        self.head = Point(x, y)
    
    def print_intro(self):
        self.text = font2.render("Eat Apples Avoid Bombs", True, WHITE)
        self.display.fill(('#483248'))     
        self.display.blit(self.text, (self.w/2 - 270, self.h/2 - 30))
        pygame.display.update()
        sleep(5)

    def print_final_score(self, score):
        self.text = font2.render("Final Score ", True, WHITE)
        self.text2 = font3.render(str(score), True, WHITE)  
  
        self.display.fill(('#483248'))     
        self.display.blit(self.text, (self.w/2 - 140, self.h/2 - 30))
        self.display.blit(self.text2, (self.w/2 + 150, self.h/2 - 45))
        pygame.display.update()
        sleep(5)

            

if __name__ == '__main__':
    game = SnakeGame()
    
    while True:
        game.print_intro()
        sleep(5)
        break

    # game loop
    while True:
        game_over, score = game.play_step()
        
        if game_over == True:
            sleep(2)
            break
        
    game.print_final_score(score)
        
        
    pygame.quit()