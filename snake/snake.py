import pygame
import random
import numpy as np


SCREEN_WIDTH = 600 
SCREEN_HEIGHT = 480 
BLOCK_SIZE = 20 
FPS = 10 

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT+50))
pygame.display.set_caption("Snake")

COLORS = {
'BLACK': (0, 0, 0),
'WHITE': (255, 255, 255),
'RED': (255, 0, 0),
'GREEN': (0, 255, 0),
'BLUE': (0, 0, 255),
'GRAY': (128, 128, 128)
}

clock=pygame.time.Clock()

class Snake:
    def __init__(self):
        self.x, self.y=BLOCK_SIZE,BLOCK_SIZE
        self.xdir=1
        self.ydir=0
        self.head=pygame.Rect(self.x, self.y, BLOCK_SIZE, BLOCK_SIZE)
        self.body=[pygame.Rect(self.x-BLOCK_SIZE, self.y, BLOCK_SIZE, BLOCK_SIZE)]
        self.dead=False
    def update(self):
        global apple
        self.body.append(self.head)
        for i in range(len(self.body)-1):
            self.body[i].x, self.body[i].y = self.body[i+1].x, self.body[i+1].y
        self.head.x += self.xdir*BLOCK_SIZE
        self.head.y += self.ydir*BLOCK_SIZE
        self.body.remove(self.head)
        for square in self.body:
            if self.head.x==square.x and self.head.y==square.y:
                self.dead=True
            if self.head.x not in range(0, SCREEN_WIDTH) or self.head.y not in range(0, SCREEN_HEIGHT):
                self.dead=True
        
        if self.dead:
            self.x, self.y=BLOCK_SIZE,BLOCK_SIZE
            self.head=pygame.Rect(self.x, self.y, BLOCK_SIZE, BLOCK_SIZE)
            self.body=[pygame.Rect(self.x-BLOCK_SIZE, self.y, BLOCK_SIZE, BLOCK_SIZE)]
            self.xdir=1
            self.ydir=0
            self.dead=False
            apple = Apple()

class Apple:
    def __init__(self):
        self.x = int(random.randint(0,SCREEN_WIDTH)/BLOCK_SIZE)*BLOCK_SIZE
        self.y = int(random.randint(0,SCREEN_HEIGHT)/BLOCK_SIZE)*BLOCK_SIZE
        self.rect = pygame.Rect(self.x, self.y, BLOCK_SIZE, BLOCK_SIZE)
    def update(self):
        pygame.draw.rect(screen, "orange", self.rect)

def draw_grid():
    for x in range(0, SCREEN_WIDTH+1, BLOCK_SIZE):
        pygame.draw.line(screen, COLORS['GRAY'], (x, 0), (x, SCREEN_HEIGHT))
    for y in range(0, SCREEN_HEIGHT+1, BLOCK_SIZE):
        pygame.draw.line(screen, COLORS['GRAY'], (0, y), (SCREEN_WIDTH, y))
    #pygame.draw.line(screen, COLORS['GRAY'], (0, SCREEN_HEIGHT), (SCREEN_WIDTH, SCREEN_HEIGHT))

f1 = pygame.font.Font(None, 36)
text1 = f1.render('Hello Привет', 1, (255, 255, 255))

def main():
    snake = Snake()
    apple=Apple()
    running=True
    dirSymbol=">"
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running=False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN and snake.ydir!=-1:
                    snake.ydir = 1
                    snake.xdir = 0
                    dirSymbol="\/"
                if event.key == pygame.K_UP and snake.ydir!=1:
                    snake.ydir = -1
                    snake.xdir = 0
                    dirSymbol="^"
                if event.key == pygame.K_RIGHT and snake.xdir!=-1:
                    snake.ydir = 0
                    snake.xdir = 1
                    dirSymbol=">"
                if event.key == pygame.K_LEFT and snake.xdir!=1:
                    snake.ydir = 0
                    snake.xdir = -1
                    dirSymbol="<"

        screen.fill(COLORS['BLACK'])
        draw_grid()
        snake.update()
        apple.update()
        pygame.draw.rect(screen,"red",snake.head)
        for square in snake.body:
            pygame.draw.rect(screen, "green", square)
        
        if snake.head.x==apple.x and snake.head.y==apple.y:
            snake.body.append(pygame.Rect(square.x, square.y, BLOCK_SIZE, BLOCK_SIZE))
            apple=Apple()
        text1 = f1.render(f'score: {len(snake.body)-1} long: {len(snake.body)+1} head x: {snake.head.x//BLOCK_SIZE} head y: {snake.head.y//BLOCK_SIZE} dir: {dirSymbol}', 1, (255, 255, 255))

        screen.blit(text1, (10, SCREEN_HEIGHT+15))

        pygame.display.flip()
        clock.tick(FPS)
    pygame.quit()

if __name__ == "__main__":
    main()