#버블 이미지 생성
import os #os를 쓰게 되면 파일의 경로를 알 수 있음.
import pygame

#버블 클래스 생성
class Bubble(pygame.sprite.Sprite):
    def __init__(self, image, color, position):
        super().__init__()
        self.image = image
        self.color = color
        self.rect = image.get_rect(center=position) #sprite를 상속받은 것은 항상 이미지와 rect는 필요한 값.

#맵 만들기
def setup():
    global map
    map = [
        # ["R","R","Y","Y","B","B","G","G"],
        list("RRYYBBGG"),
        list("RRYYBBG/"),# / : 버블이 위치할 수 없는 곳
        list("BBGGRRY"),
        list("BGGRRYY/"), 
        list("........"), # . : 비어있는 곳
        list("......./"),
        list("........"),
        list("......./"),
        list("........"),
        list("......./"),
        list("........"),
    ]

    for row_idx, row in enumerate(map):
        for col_idx, col in enumerate(row):
            if col in [".","/"]:
                continue
            position=get_bubble_position(row_idx,col_idx)
            image = get_bubble_image(col)
            bubble_group.add(Bubble(image,col,position))
def get_bubble_position(row_idx,col_idx):
    pos_x = col_idx*CELL_SIZE+(BUBBLE_WIDTH//2) # /를 두개 넣어 정수형으로 바꿔준 것
    pos_y = row_idx*CELL_SIZE+(BUBBLE_HEIGHT//2)
    if row_idx%2 ==1:
        pos_x += CELL_SIZE//2;
    return pos_x,pos_y

def get_bubble_image(color):
    if color == "R":
        return bubble_images[0]
    elif color == "Y":
        return bubble_images[1]
    elif color == "B":
        return bubble_images[2]
    elif color == "G":
        return bubble_images[3]
    elif color == "P":
        return bubble_images[4]
    else:
        return bubble_images[-1]
    
    
pygame.init()
screen_width=448
screen_height=720
screen = pygame.display.set_mode((screen_width,screen_height))
pygame.display.set_caption("Puzzle Bubble")
clock = pygame.time.Clock()

#배경 이미지 불러오기
current_path =  os.path.dirname(__file__) #지금 실행하는 파일이 있는 폴더 경로를 알려줌
background = pygame.image.load(os.path.join(current_path, "background.png"))

#버블 이미지 불러오기
bubble_images=[
    pygame.image.load(os.path.join(current_path, "red.png")).convert_alpha(),
    pygame.image.load(os.path.join(current_path, "yellow.png")).convert_alpha(),
    pygame.image.load(os.path.join(current_path, "blue.png")).convert_alpha(),
    pygame.image.load(os.path.join(current_path, "green.png")).convert_alpha(),
    pygame.image.load(os.path.join(current_path, "purple.png")).convert_alpha(),
    pygame.image.load(os.path.join(current_path, "black.png")).convert_alpha() #게임 종료시 모든 구슬 색이 검정색으로 변하는것을 표현       
]

# 게임 관련 변수
CELL_SIZE = 56
BUBBLE_WIDTH = 56
BUBBLE_HEIGHT = 62 

map = [] # 맵
bubble_group = pygame.sprite.Group()
setup()

running=True #게임이 실행되고 있는지 아닌지에 대한 변수
while running: 
    clock.tick(60) #FPS 60으로 설정

    for event in pygame.event.get(): #발생하고 있는 모든 이벤트를 받아옴
        if event.type==pygame.QUIT: #창을 끄면
            running = False #게임 끝

    screen.blit(background, (0,0))
    bubble_group.draw(screen)
    pygame.display.update()     

pygame.quit()