import pygame
import random
import sys


WIDTH = 500
ROWS = 20
SQUARE_SIZE = WIDTH // ROWS


WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)

class Cube:
    def __init__(self, pos, dirnx=1, dirny=0, color=GREEN):
        self.pos = pos
        self.dirnx = dirnx
        self.dirny = dirny
        self.color = color

    def move(self, dirnx, dirny):
        self.dirnx = dirnx
        self.dirny = dirny
        x, y = self.pos
        self.pos = (x + self.dirnx, y + self.dirny)

    def draw(self, surface, eyes=False):
        dis = SQUARE_SIZE
        i, j = self.pos
        pygame.draw.rect(surface, self.color, (i * dis + 1, j * dis + 1, dis - 2, dis - 2))
        if eyes:
            centre = dis // 2
            radius = 3
            circleMiddle = (i * dis + centre - radius, j * dis + 8)
            circleMiddle2 = (i * dis + dis - radius * 2, j * dis + 8)
            pygame.draw.circle(surface, BLACK, circleMiddle, radius)
            pygame.draw.circle(surface, BLACK, circleMiddle2, radius)

class Snake:
    def __init__(self, color, pos):
        self.color = color
        self.head = Cube(pos)
        self.body = [self.head]
        self.dirnx = 1
        self.dirny = 0
        self.turns = {}

    def move(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            keys = pygame.key.get_pressed()
            for key in keys:
                if keys[pygame.K_LEFT]:
                    if self.dirnx != 1:
                        self.dirnx = -1
                        self.dirny = 0
                        self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]
                elif keys[pygame.K_RIGHT]:
                    if self.dirnx != -1:
                        self.dirnx = 1
                        self.dirny = 0
                        self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]
                elif keys[pygame.K_UP]:
                    if self.dirny != 1:
                        self.dirnx = 0
                        self.dirny = -1
                        self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]
                elif keys[pygame.K_DOWN]:
                    if self.dirny != -1:
                        self.dirnx = 0
                        self.dirny = 1
                        self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]
        for i, c in enumerate(self.body):
            p = c.pos[:]
            if p in self.turns:
                turn = self.turns[p]
                c.move(turn[0], turn[1])
                if i == len(self.body) - 1:
                    self.turns.pop(p)
            else:
                c.move(c.dirnx, c.dirny)
        # Check for wall collision
        head_x, head_y = self.head.pos
        if head_x < 0 or head_x >= ROWS or head_y < 0 or head_y >= ROWS:
            self.reset((10, 10))
        # Check for self collision
        for x in range(len(self.body)):
            if self.body[x].pos in list(map(lambda z: z.pos, self.body[x + 1:])):
                self.reset((10, 10))

    def reset(self, pos):
        self.head = Cube(pos)
        self.body = [self.head]
        self.dirnx = 1
        self.dirny = 0
        self.turns = {}

    def add_cube(self):
        tail = self.body[-1]
        dx, dy = tail.dirnx, tail.dirny
        new_pos = (tail.pos[0] - dx, tail.pos[1] - dy)
        new_cube = Cube(new_pos, dx, dy)
        self.body.append(new_cube)

    def draw(self, surface):
        for i, c in enumerate(self.body):
            if i == 0:
                c.draw(surface, True)
            else:
                c.draw(surface)

def draw_grid(surface):
    size_btwn = WIDTH // ROWS
    x = 0
    y = 0
    for l in range(ROWS):
        x = x + size_btwn
        y = y + size_btwn
        pygame.draw.line(surface, WHITE, (x, 0), (x, WIDTH))
        pygame.draw.line(surface, WHITE, (0, y), (WIDTH, y))

def redraw_window(surface, snake, snack):
    surface.fill(BLACK)
    snake.draw(surface)
    snack.draw(surface)
    draw_grid(surface)
    pygame.display.update()

def random_snack(snake):
    positions = list(map(lambda z: z.pos, snake.body))
    while True:
        x = random.randrange(ROWS)
        y = random.randrange(ROWS)
        if (x, y) not in positions:
            break
    return Cube((x, y), color=RED)

def main():
    pygame.init()
    win = pygame.display.set_mode((WIDTH, WIDTH))
    pygame.display.set_caption('Snake Game by SHAYAN ALI')
    snake = Snake(GREEN, (10, 10))
    snack = random_snack(snake)
    clock = pygame.time.Clock()
    while True:
        pygame.time.delay(50)
        clock.tick(10)
        snake.move()
        if snake.head.pos == snack.pos:
            snake.add_cube()
            snack = random_snack(snake)
        redraw_window(win, snake, snack)

if __name__ == '__main__':
    main() 