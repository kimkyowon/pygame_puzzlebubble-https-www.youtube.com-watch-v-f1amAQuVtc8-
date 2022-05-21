#발사대 겨냥 (키보드 화살표를 통해 각도 조절)
from email.mime import image
import os,random #os를 쓰게 되면 파일의 경로를 알 수 있음.
import pygame


#버블 클래스 생성
class Bubble(pygame.sprite.Sprite):
    def __init__(self, image, color, position=(0,0)):
        super().__init__()
        self.image = image
        self.color = color
        self.rect = image.get_rect(center=position) #sprite를 상속받은 것은 항상 이미지와 rect는 필수적으로 있어야 함.
    def set_rect(self,position):
        self.rect = self.image.get_rect(center=position)

    def draw(self,screen):
        screen.blit(self.image, self.rect)
        
#발사대 클래스 생성
class Pointer(pygame.sprite.Sprite):
    def __init__(self,image,position,angle):
        super().__init__()
        self.image = image
        self.rect = image.get_rect(center=position)         
        self.angle = angle
        self.original_image = image
        self.position = position
    def draw(self,screen):
        screen.blit(self.image, self.rect)
        pygame.draw.circle(screen, RED, self.position,3) #화살표의 빨간점 

    #각도에 맞춰 회전
    def rotate(self,angle):
        self.angle +=angle
        if self.angle  > 170: #각도가 계속 돌아가는 것이 아닌 왼쪽이나 오른쪽 일정이상 넘어가면 멈춰야 함
            self.angle = 170
        elif self.angle < 10:
            self.angle = 10
        self.image = pygame.transform.rotozoom(self.original_image, self.angle, 1) #회전 시킨 이미지를 화면상에 업데이트 하는 작업
        self.rect = self.image.get_rect(center=self.position) #이미지의 rect가 계속 바귀기 때문에 이 문장을 쓰면 항상 포인터의 rect정보는 최초로 지정했던 center좌표 중심으로 돌아가게 됨.


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

def prepare_bubbles():
    global curr_bubble
    curr_bubble= create_bubble() #새 버블 만들기
    curr_bubble.set_rect((screen_width//2, 624))

def create_bubble():
    color = get_random_bubble_color()
    image = get_bubble_image(color)
    Bubble(image, color, )

def get_random_bubble_color():
    colors = [] 
    for row in map: #맵 정보를 받아와 맵에 존재하는  색상만 받아오기
        for col in row:
            if col not in colors and col not in [".","/"]: #버블이 비거나 없는 구간이 아닌경우여야 함
                colors.append(col)
    return random.choice(colors)
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

#발사대 이미지 불러오기
pointer_image = pygame.image.load(os.path.join(current_path,"pointer.png"))
pointer = Pointer(pointer_image,(screen_width//2, 624), 90)

# 게임 관련 변수
CELL_SIZE = 56
BUBBLE_WIDTH = 56
BUBBLE_HEIGHT = 62 
RED = (255,0,0) #튜플형태로 하면 rgb가 돼서 빨간 점이 됨

#화살표 관련 변수
#to_angle = 0 #좌우로 움직일 각도 정보
to_angle_left = 0 #왼쪽으로 움직일 각도 정보
to_angle_right = 0 #오른쪽으로 움직일 각도 정보
angle_speed = 1.5 # 1.5도씩 움직이게 됨

curr_bubble =None #이번에 쏠 버블


map = [] # 맵
bubble_group = pygame.sprite.Group()
setup()


running=True #게임이 실행되고 있는지 아닌지에 대한 변수
while running: 
    clock.tick(60) #FPS 60으로 설정

    for event in pygame.event.get(): #발생하고 있는 모든 이벤트를 받아옴
        if event.type==pygame.QUIT: #창을 끄면
            running = False #게임 끝

        if event.type == pygame.KEYDOWN: #어떤 키가 눌러졌을때
            if event.key==pygame.K_LEFT: #왼쪽 화살표 키보드가 눌러지면
                to_angle_left +=angle_speed
            elif event.key == pygame.K_RIGHT:
                to_angle_right-=angle_speed

        if event.type == pygame.KEYUP:
            if event.key==pygame.K_LEFT:
                to_angle_left = 0
            if event.key==pygame.K_RIGHT:
                to_angle_right=0

    if not curr_bubble:
        prepare_bubbles()

    screen.blit(background, (0,0))
    bubble_group.draw(screen)
    pointer.rotate(to_angle_left+to_angle_right) #왼쪽키와 오른쪽 키를 합산한 각도로 돌아가야함(그래야 멈추지 않고 자연스럽게 돌아가므로)
    pointer.draw(screen)
    if curr_bubble: 
        curr_bubble.draw(screen)

    pygame.display.update()     

pygame.quit()