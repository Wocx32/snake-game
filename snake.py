import sys
import pygame
import random
import time

pygame.init()

SIZE = width, height = 700, 500
BLOCKSIZE = 10

BLACK = pygame.Color(0, 0, 0)
WHITE = pygame.Color(255, 255, 255)
RED = pygame.Color(255, 0, 0)
GREEN = pygame.Color(0, 255, 0)

CLOCK = pygame.time.Clock()


difficulty = 20
velocity = BLOCKSIZE
score = 0
x, y = 150, 150

pygame.display.set_caption('Snake')
screen = pygame.display.set_mode(SIZE)
screen.fill(BLACK)

class Snake:
    def __init__(self, x: int, y: int, blocksize: int, velocity: int, screen):
        self.x = x
        self.y = y
        self.BLOCKSIZE = blocksize
        self.screen = screen
        self.color = pygame.Color(255, 255, 255)


        self.snake = [[self.x, self.y], [self.x - self.BLOCKSIZE, self.y], [self.x - self.BLOCKSIZE*2, self.y], [self.x - self.BLOCKSIZE*3, self.y]]
        self.velocity = velocity
        self.direction = 'RIGHT'

    def insert(self, x, y):
        self.x = x
        self.y = y
        self.snake.insert(0, [self.x, self.y])

    def pop(self):
        self.snake.pop()

    def draw(self, color=None):
        snake_color = color if color else self.color

        for position in self.snake:
            part = pygame.Rect(position[0], position[1], self.BLOCKSIZE, self.BLOCKSIZE)
            pygame.draw.rect(self.screen, snake_color, part)
    
    def check_collision(self):
        if [self.x, self.y] in self.snake[1:]:
            return True
        return False


class Food:
    def __init__(self, blocksize: int, size: tuple, screen):
        self.width, self.height = size
        self.BLOCKSIZE = blocksize
        self.screen = screen
        self.color = pygame.Color(255, 0, 0)

        self.x, self.y = self.generate_pos()

    def change_pos(self):
        self.x, self.y = self.generate_pos()

    def draw(self, color=None):
        food_color = color if color else self.color
        block = pygame.Rect(self.x, self.y, self.BLOCKSIZE, self.BLOCKSIZE)
        pygame.draw.rect(self.screen, food_color, block)

    def generate_pos(self):
        """Returns tuple (x,y)"""
        return random.randrange(0, self.width, self.BLOCKSIZE), random.randrange(0, self.height, self.BLOCKSIZE)


# https://github.com/rajatdiptabiswas/snake-pygame/blob/master/Snake%20Game.py
##############################################################################

def game_over():
    font = pygame.font.SysFont('time new roman', 90)
    game_over_surface = font.render('You Died', True, RED)
    game_over_rect = game_over_surface.get_rect()
    game_over_rect.midtop = (width/2, height/4)
    screen.fill(BLACK)
    screen.blit(game_over_surface, game_over_rect)
    show_score(RED, 'times', 20, True)
    pygame.display.flip()
    time.sleep(3)
    pygame.quit()
    sys.exit()
    
def show_score(color, font, size, game_over: bool = False):
    score_font = pygame.font.SysFont(font, size)
    score_surface = score_font.render('Score : ' + str(score), True, color)
    score_rect = score_surface.get_rect()

    if game_over:
        score_rect.midtop = (width/2, height/1.25)
    else:
        score_rect.midtop = (width/10, 15)

    screen.blit(score_surface, score_rect)

##############################################################################

snake = Snake(x, y, BLOCKSIZE, velocity, screen)
food = Food(BLOCKSIZE, SIZE, screen)

change_to = None

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP or event.key == ord('w'):
                change_to = 'UP'

            if event.key == pygame.K_DOWN or event.key == ord('s'):
                change_to = 'DOWN'

            if event.key == pygame.K_LEFT or event.key == ord('a'):
                change_to = 'LEFT'

            if event.key == pygame.K_RIGHT or event.key == ord('d'):
                change_to = 'RIGHT'
    
    # https://github.com/rajatdiptabiswas/snake-pygame/blob/master/Snake%20Game.py
    # Making sure the snake cannot move in the opposite direction instantaneously
    if change_to == 'UP' and snake.direction != 'DOWN':
        snake.direction = 'UP'

    if change_to == 'DOWN' and snake.direction != 'UP':
        snake.direction = 'DOWN'

    if change_to == 'LEFT' and snake.direction != 'RIGHT':
        snake.direction = 'LEFT'

    if change_to == 'RIGHT' and snake.direction != 'LEFT':
        snake.direction = 'RIGHT'

    # movement
    if snake.direction == 'UP':
        y -= velocity
    if snake.direction == 'DOWN':
        y += velocity
    if snake.direction == 'RIGHT':
        x += velocity
    if snake.direction == 'LEFT':
        x -= velocity

    # make the snake emerge from the opposite side
    if x < 0:
        x = width - BLOCKSIZE
    if x > width:
        x = 0

    if y < 0:
        y = height - BLOCKSIZE
    if y > height:
        y = 0
    
    snake.insert(x, y)

    if abs(snake.x - food.x) < 10 and abs(snake.y - food.y) < 10:
        food.change_pos()
        score += 1
    else:
        snake.pop()

    food.draw()
    snake.draw()

    if snake.check_collision():
        game_over()
    
    show_score(GREEN, 'consolas', 20)
    pygame.display.update()
    screen.fill(BLACK)
    CLOCK.tick(difficulty)