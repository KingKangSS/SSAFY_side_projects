import pygame
import sys
import random

# Pygame 모듈 초기화
pygame.init()

# 이미지 로드
img_neko = [
    None,
    pygame.image.load("neko1.png"),
    pygame.image.load("neko2.png"),
    pygame.image.load("neko3.png"),
    pygame.image.load("neko4.png"),
    pygame.image.load("neko5.png"),
    pygame.image.load("neko6.png"),
    pygame.image.load("neko_niku.png"),
]

bg = pygame.image.load("neko_bg.png")
cursor = pygame.image.load("neko_cursor.png")

# 게임 설정 변수
map_y, map_x = 10, 8
display_width, display_height = 912, 768
neko = [[random.choice(range(1, 7)) for _ in range(map_x)] for _ in range(map_y)]
check = [[0] * map_x for _ in range(map_y)]

import pygame
import sys
import random

pygame.init() # pygame 모듈 초기화

img_neko = [ 
    None,
    pygame.image.load("neko1.png"),
    pygame.image.load("neko2.png"),
    pygame.image.load("neko3.png"),
    pygame.image.load("neko4.png"),
    pygame.image.load("neko5.png"),
    pygame.image.load("neko6.png"),
    pygame.image.load("neko_niku.png"),
]




map_y = 10
map_x = 8
display_width = 912
display_height = 768
bg = pygame.image.load("neko_bg.png")
cursor = pygame.image.load("neko_cursor.png")

neko = [[] for _ in range(map_y)]
check = [[0 for _ in range(map_x)] for _ in range(map_y)]

for y in range(map_y):
    for x in range(map_x):
        neko[y].append(random.choice(range(1,7)))


gameDisplay = pygame.display.set_mode((display_width, display_height)) #스크린 초기화
pygame.display.set_caption("애니팡")  # 타이틀
clock = pygame.time.Clock() #Clock 오브젝트 초기화

class Mouse :
    def __init__(self,cursor,map_y,map_x):
        self.turn = False
        self.cursor = cursor
        self.map_y = map_y
        self.map_x = map_x

    def get_mouse(self):
        position = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        for y in range(map_y):
            for x in range(map_x):
                if x*72+20 < position[0] < (x+1)*72+20 and y*72+20 < position[1] < (y+1)*72+20:
                    if not self.turn:
                        gameDisplay.blit(self.cursor, (x*72+20, y*72+20))
                        if click[0]:
                            self.turn = True
                            check[y][x] = 1
                    else:
                        gameDisplay.blit(self.cursor, (x*72+20, y*72+20))
                        if click[0]:
                            # 인접한 블록을 선택했는지 확인
                            if (0 <= y-1 and check[y-1][x] == 1) or (y+1 < self.map_y and check[y+1][x] == 1) \
                                    or (self.map_x > x+1 and check[y][x+1] == 1) or (0 <= x-1 and check[y][x-1] == 1):
                                switch_neko()  # 블록 교환 실행
                                self.turn = False
                                cursor_set()  # 커서 및 선택 초기화
                            else:
                                # 선택된 두 번째 블록이 인접하지 않는 경우 첫 번째 블록의 선택만 해제
                                cursor_set()
                                self.turn = True
                                check[y][x] = 1
                        elif click[2]:
                            # 우클릭으로 선택 해제
                            cursor_set()
                            self.turn = False

def switch_neko():
    selected = [(y, x) for y in range(map_y) for x in range(map_x) if check[y][x] == 1]
    if len(selected) == 2:
        (y1, x1), (y2, x2) = selected
        neko[y1][x1], neko[y2][x2] = neko[y2][x2], neko[y1][x1]
        pygame.display.update()  # 화면 갱신
        pygame.time.wait(500)  # 변화를 확인할 수 있도록 잠시 대기
        if not check_neko():
            # 매칭이 없으면 다시 교환
            neko[y1][x1], neko[y2][x2] = neko[y2][x2], neko[y1][x1]
        cursor_set()  # 커서 및 선택 초기화


def check_neko():
    match_found = False
    for y in range(map_y):
        for x in range(map_x - 2):
            if neko[y][x] == neko[y][x+1] == neko[y][x+2] != 0:
                match_found = True
                for i in range(3):
                    neko[y][x+i] = 7
    for y in range(map_y - 2):
        for x in range(map_x):
            if neko[y][x] == neko[y+1][x] == neko[y+2][x] != 0:
                match_found = True
                for i in range(3):
                    neko[y+i][x] = 7

    if match_found:
        apply_gravity()
    return match_found

def apply_gravity():
    for x in range(map_x):
        for y in range(map_y-1, -1, -1):  # 아래에서 위로 검사
            if neko[y][x] == 7:
                for pull_down in range(y, 0, -1):
                    neko[pull_down][x] = neko[pull_down-1][x]
                neko[0][x] = random.choice(range(1,7))  # 가장 위에 새 블록 생성

def cursor_set():
    for y in range(map_y):
        for x in range(map_x):
            check[y][x] = 0


def cursor_draw():
    for y in range(map_y):
        for x in range(map_x):
            if check[y][x] == 1:
                gameDisplay.blit(cursor,(x*72+20, y*72+20))

def neko_draw():
    for y in range(map_y):
        for x in range(map_x):
            gameDisplay.blit(img_neko[neko[y][x]], (x*72+20, y*72+20))


def game(): # 메인 게임 함수
    
    tmr = 0 # 시간 관리 변수
    # 마우스 클래스 부르기
    m = Mouse(cursor,map_y,map_x)
    while True:
        tmr += 1 # 매 시간 1초 증가
        for event in pygame.event.get(): # 윈도운 X 누를 시 나오게끔
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        gameDisplay.blit(bg,(0,0))
        neko_draw()
        m.get_mouse()
        cursor_draw()
        check_neko()
        pygame.display.update()
        clock.tick(20)

        

game()

# 게임 디스플레이 설정
gameDisplay = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption("애니팡")
clock = pygame.time.Clock()

class Mouse:
    def __init__(self, cursor, map_y, map_x):
        self.turn = False
        self.selected_pos = None
        self.cursor = cursor
        self.map_y = map_y
        self.map_x = map_x

    def get_mouse(self):
        position = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        if click[0]:
            for y in range(map_y):
                for x in range(map_x):
                    if x * 72 + 20 < position[0] < (x + 1) * 72 + 20 and y * 72 + 20 < position[1] < (y + 1) * 72 + 20:
                        if not self.turn:
                            self.selected_pos = (x, y)
                            self.turn = True
                        else:
                            if self.is_adjacent((x, y), self.selected_pos):
                                self.switch_neko((x, y), self.selected_pos)
                                self.turn = False
                                self.selected_pos = None
                            else:
                                self.selected_pos = (x, y)
        elif click[2]:  # 우클릭으로 선택 해제
            self.turn = False
            self.selected_pos = None

    def is_adjacent(self, pos1, pos2):
        return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1]) == 1

    def switch_neko(self, pos1, pos2):
        x1, y1 = pos1
        x2, y2 = pos2
        neko[y1][x1], neko[y2][x2] = neko[y2][x2], neko[y1][x1]
        if not check_neko():
            # 매칭이 없으면 다시 교환
            neko[y1][x1], neko[y2][x2] = neko[y2][x2], neko[y1][x1]

def check_neko():
    # 여기에 매칭 검사 및 처리 로직 추가
    pass

def apply_gravity():
    # 여기에 중력 적용 로직 추가
    pass

def neko_draw():
    for y in range(map_y):
        for x in range(map_x):
            gameDisplay.blit(img_neko[neko[y][x]], (x * 72 + 20, y * 72 + 20))

def game():
    m = Mouse(cursor, map_y, map_x)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        gameDisplay.blit(bg, (0, 0))
        neko_draw()
        m.get_mouse()
        check_neko()
        pygame.display.update()
        clock.tick(20)

game()
