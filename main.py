import pygame
import sys
import time
import random

from pygame.locals import *
# 윈도우창
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
# 실제 사이즈
GRID_SIZE = 20
GRID_WIDTH = WINDOW_WIDTH/GRID_SIZE
GRID_HEIGHT = WINDOW_HEIGHT/GRID_SIZE

WHITE = (255, 255, 255)
GREEN = (0, 100, 0)
RED = (250, 0, 0)
GRAY = (100, 100, 100)

UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

FPS = 10


class Python(object):
    # 초기화
    def __init__(self):
        self.create()
        self.color = GREEN

    def create(self):
        self.length = 2
        # 중앙 배치
        self.positions = [((WINDOW_WIDTH/2), (WINDOW_HEIGHT/2))]
        self.direction = random.choice([UP, DOWN, LEFT, RIGHT])

    def control(self, xy):
        # 현재xy와 반대xy가 같으면 아무행동도 안함 (반대방향 조작X)
        if(xy[0]*-1, xy[1]*-1) == self.direction:
            return
        else:
            self.direction = xy

    def move(self):
        # 현재 값은 뱀의 머리
        cur = self.positions[0]
        x, y = self.direction
        # 머리 이후 부분 cur[0]은 x cur[1]은 y, 창을 넘어갈때 반대쪽으로 계속 나오게 계산
        new = (((cur[0] + (x*GRID_SIZE)) % WINDOW_WIDTH),
               (cur[1] + (y*GRID_SIZE)) % WINDOW_HEIGHT)
        # 새로운 부분이 머리 이후 부분에 포함되면 죽음
        if new in self.positions[2:]:
            self.create()
        else:
            # 이동하면서 새로운 부분 삽입
            self.positions.insert(0, new)
            # 먹이를 먹지 않았는데 길이가 커질때 (이동시)
            if len(self.positions) > self.length:
                self.positions.pop()

    def eat(self):
        self.length += 1

    # 뱀 실제 화면 출력
    def draw(self, surface):
        for p in self.positions:
            draw_object(surface, self.color, p)


# 먹이
class Feed(object):
    def __init__(self):
        self.position = (0, 0)
        self.color = RED
        self.create()

    def create(self):
        # 랜덤 먹이 생성(0부터)
        self.position = (random.randint(0, GRID_WIDTH - 1) * GRID_SIZE,
                         random.randint(0, GRID_HEIGHT - 1)*GRID_SIZE)

    def draw(self, surface):
        draw_object(surface, self.color, self.position)


# 뱀과 먹이 출력
def draw_object(surface, color, pos):
    # pos[0]:x ,pos[1]:y
    r = pygame.Rect((pos[0], pos[1]), (GRID_SIZE, GRID_SIZE))
    pygame.draw.rect(surface, color, r)


def check_eat(python, eat):
    if python.positions[0] == feed.position:
        python.eat()
        feed.create()


def show_info(length, speed, surface):
    font = pygame.font.Font(None, 34)
    text = font.render(
        f"Length : {str(length)}  Speed : {str(round(speed,2))}", 1, GRAY)
    pos = text.get_rect()
    pos.centerx = 150
    surface.blit(text, pos)


# 초기화
if __name__ == '__main__':
    python = Python()
    feed = Feed()

    pygame.init()
    window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT), 0, 32)
    pygame.display.set_caption('Python Game')
    surface = pygame.Surface(window.get_size())
    surface = surface.convert()
    surface.fill(WHITE)
    clock = pygame.time.Clock()
    # 최초 keydown 이벤트까지걸리는 시간 ,다른 이벤트가 보내지는 시간간격
    pygame.key.set_repeat(1, 40)
    # 화면 출력
    window.blit(surface, (0, 0))

    # 키조작
    while True:

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN:
                if event.key == K_UP:
                    python.control(UP)
                elif event.key == K_DOWN:
                    python.control(DOWN)
                elif event.key == K_LEFT:
                    python.control(LEFT)
                elif event.key == K_RIGHT:
                    python.control(RIGHT)

        surface.fill(WHITE)
        python.move()
        check_eat(python, feed)
        speed = (FPS+python.length)/2
        show_info(python.length, speed, surface)
        python.draw(surface)
        feed.draw(surface)
        window.blit(surface, (0, 0))
        pygame.display.flip()
        pygame.display.update()
        clock.tick(speed)
