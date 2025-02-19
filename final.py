import pygame
import random
import sys


from pygame.locals import (K_UP, K_DOWN, K_LEFT, K_RIGHT, K_ESCAPE, KEYDOWN, QUIT, )

pygame.init()
s_height = 800
s_width = 800
screen = pygame.display.set_mode((s_width, s_height))
pygame.display.set_caption('TETRİS')
timer = pygame.time.Clock()
global auto_move_delay
auto_move_delay= 600
last_auto_move_time = pygame.time.get_ticks()
move_delay = 250
last_move_time = pygame.time.get_ticks()
exit = False
  
score=0
font = pygame.font.Font(None, 36)
dic = [
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],

    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
]
choice = ["L","line","Z","T","square"]

pygame.mixer.music.load('Original Tetris theme (Tetris Soundtrack).mp3')
pygame.mixer.music.play(-1)  # -1 sonsuza kadar tekrar eder
pygame.mixer.music.set_volume(0.5)  # Ses seviyesi (0.0 - 1.0)


def game_over(screen, score):
    font = pygame.font.Font(None, 74)
    text = font.render(f"Skorun: {score}", True, (255, 255, 255))
    replay_text = font.render("Yeniden oyna? (E/H)", True, (255, 255, 255))

    screen.fill((0, 0, 0))
    screen.blit(text, (150, 200))
    screen.blit(replay_text, (100, 300))
    pygame.display.flip()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_e:  # E tuşu -> Yeniden oyna
                    return True
                elif event.key == pygame.K_h:  # H tuşu -> Çık
                    return False



class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player, self).__init__()
        self.type = random.choice(choice)
        self.index1 = 0
        self.index2 = random.randint(0, 8)
        self.konum = [100 + 50 * self.index2, 50]
        self.stopped = False
        self.colour = (30 * random.randint(1, 8), 30 * random.randint(1, 8), 30 * random.randint(1, 8))

        if self.type == 'line':
            self.indexes = [[self.index1, self.index2 + 1], [self.index1, self.index2 + 2],
                            [self.index1, self.index2 + 3]]
            self.h_v = 'h'
            for index in self.indexes:
                dic[index[0]][index[1]] = 1
        if self.type == 'square':
            self.indexes = [[self.index1, self.index2+1], [self.index1, self.index2 + 2],[self.index1 + 1, self.index2+1], [self.index1 + 1, self.index2 + 2]]
            for index in self.indexes:
                dic[index[0]][index[1]] =1
        if self.type == 'T':
            self.indexes = [[self.index1, self.index2 + 2], [self.index1+1, self.index2 + 1],[self.index1+1, self.index2 + 2], [self.index1 + 1, self.index2 + 3]]
            self.pos=0
            for index in self.indexes:
                dic[index[0]][index[1]] = 1
        if self.type == 'L':
            self.indexes = [[self.index1, self.index2 + 1], [self.index1 + 1, self.index2 + 1],[self.index1 + 1, self.index2 + 2], [self.index1 + 1, self.index2 + 3]]
            self.pos = 0
            for index in self.indexes:
                dic[index[0]][index[1]] = 1
        if self.type == 'Z':
            self.indexes = [[self.index1, self.index2 + 1], [self.index1 , self.index2 + 2],[self.index1 + 1, self.index2 +2], [self.index1 + 1, self.index2 + 3]]
            self.pos = 0
            for index in self.indexes:
                dic[index[0]][index[1]] = 1

    def auto_down(self):

        if self.stopped:
            return

        engel = False
        for index in self.indexes:
            if  dic[index[0] + 1][index[1]] == 1 and [index[0] + 1, index[1]] not in self.indexes:
                engel = True

                break
        if not engel:
            for index in self.indexes:
                dic[index[0]][index[1]] = 0
            for index in self.indexes:
                dic[index[0] + 1][index[1]] = 1
            for index in self.indexes:
                index[0] += 1
        else:
            self.stopped = True
            self.shift()
            players.append(new_player())

    def kayma_efekti(self, satir):
        for player in players:
            # 1. Remove blocks on the cleared line
            player.indexes = [index for index in player.indexes if index[0] != satir]

            # 2. Shift blocks above the cleared line down by one
            for index in player.indexes:

                if index[0] < satir:
                    index[0] += 1

    def shift(self):
        global score
        completed = 0
        p1 = 11

        for i in range(0, 11):
            if dic[p1] == [1] * 12:
                completed += 1
                break
            else:
                p1 -= 1
        if p1 > 0 and completed == 1:
            if dic[p1 - 1] == [1] * 12:
                completed += 1
            if p1 > 1:
                if dic[p1 - 2] == [1] * 12:
                    completed += 1
        if (completed == 1):

            satir = p1
            while p1 != 0:
                dic[p1] = dic[p1 - 1]
                p1 -= 1
            dic[0] = [0] * 12
            self.kayma_efekti(satir)

        if (completed == 2):
            satir = p1

            if dic[satir - 1] == [1] * 12:
                satir2 = p1 - 1
            else:
                satir2 = satir - 2
            p2 = satir2

            while p2 != 0:
                dic[p2] = dic[p2 - 1]
                p2 -= 1
            dic[0] = [0] * 12
            while p1 != 0:
                dic[p1] = dic[p1 - 1]
                p1 -= 1
            dic[0] = [0] * 12
            self.kayma_efekti(satir2)
            self.kayma_efekti(satir)

        if (completed == 3):
            satir = p1
            satir2 = p1 - 1
            satir3 = p1 - 2
            p2 = p1 - 1
            p3 = p1 - 2
            while p3 > 0:
                dic[p3] = dic[p3 - 1]
                p3 -= 1
            dic[0] = [0] * 12
            while p2 > 0:
                dic[p2] = dic[p2 - 1]
                p2 -= 1
            dic[0] = [0] * 12
            while p1 > 0:
                dic[p1] = dic[p1 - 1]
                p1 -= 1
            dic[0] = [0] * 12

            self.kayma_efekti(satir3)
            self.kayma_efekti(satir2)
            self.kayma_efekti(satir)
        score = score +100 *completed

    def update(self, pressed_keys):
        if self.stopped:
            return 0
        global last_move_time
        current_time = pygame.time.get_ticks()

        if current_time - last_move_time > move_delay:
            if pressed_keys[K_UP]:

                last_move_time = current_time

                if self.type == 'line':
                    if self.h_v == 'h' :
                        orta=self.indexes[1]
                        if dic[orta[0]-1][orta[1]]==0 and dic[orta[0]+1][orta[1]]==0:
                            self.h_v='v'
                            dic[orta[0]][orta[1]-1]=0
                            dic[orta[0]][orta[1]+1]= 0
                            dic[orta[0]-1][orta[1] ] = 1
                            dic[orta[0]-1][orta[1] ] = 1
                            self.indexes=[]
                            self.indexes=[[orta[0]-1,orta[1]],orta,[orta[0]+1,orta[1]]]
                    elif self.h_v == 'v' :
                        orta = self.indexes[1]
                        if orta[1]>0 and orta[1]<11 and dic[orta[0]][orta[1]-1] == 0 and dic[orta[0] ][orta[1]+1] == 0:
                            self.h_v = 'h'

                            dic[orta[0]-1][orta[1] ] = 0
                            dic[orta[0]+1][orta[1] ] = 0
                            dic[orta[0] ][orta[1]-1] = 1
                            dic[orta[0] ][orta[1]+1] = 1

                            self.indexes = [[orta[0] , orta[1]-1], orta, [orta[0] , orta[1]+1]]
                elif self.type == 'T':
                    if self.pos==0:
                        orta=self.indexes[2]
                        if dic[orta[0]+1][orta[1]]==0 :
                            self.pos=90
                            dic[orta[0]][orta[1]-1]=0
                            dic[orta[0]+1][orta[1]]=1
                            self.indexes=[[orta[0]-1,orta[1]],[orta[0],orta[1]+1],orta,[orta[0]+1,orta[1]]]

                    elif self.pos == 90:
                        orta = self.indexes[2]
                        if orta[1]>0 and dic[orta[0]][orta[1]-1]==0:
                            self.pos=180
                            dic[orta[0]-1][orta[1]] = 0
                            dic[orta[0]][orta[1] - 1] = 1
                            self.indexes = [[orta[0] , orta[1]-1],orta, [orta[0]+1, orta[1]],  [orta[0] , orta[1]+1]]

                    elif self.pos == 180:
                        orta=self.indexes[1]
                        if  dic[orta[0]-1][orta[1]]==0:
                            self.pos = 270
                            dic[orta[0] ][orta[1]+1] = 0
                            dic[orta[0]-1][orta[1] ] = 1
                            self.indexes = [[orta[0], orta[1] - 1] , orta , [orta[0] + 1, orta[1]] , [orta[0]-1, orta[1] ]]


                    elif self.pos == 270:
                        orta = self.indexes[1]
                        if orta[1]<11 and dic[orta[0]][orta[1]+1]==0:
                            self.pos = 0
                            dic[orta[0]+1][orta[1] ] = 0
                            dic[orta[0] ][orta[1]+1] = 1
                            self.indexes = [[orta[0]-1, orta[1] ], [orta[0] , orta[1]-1],orta,
                                            [orta[0] , orta[1]+1]]
                if self.type =="Z":
                    if self.pos==0 :
                        orta=self.indexes[0]
                        if dic[orta[0]+1][orta[1]]==0 and dic[orta[0]+2][orta[1]]==0:
                            self.pos=180
                            dic[orta[0]][orta[1]]=0
                            dic[orta[0]+1][orta[1] +2] = 0
                            dic[orta[0]+1][orta[1]]=1
                            dic[orta[0] + 2][orta[1]] = 1
                            self.indexes=[[orta[0],orta[1]+1],[orta[0]+1,orta[1]],[orta[0]+1,orta[1]+1],[orta[0]+2,orta[1]]]
                    elif self.pos ==180:
                        orta=self.indexes[0]
                        if orta[1]<11 and dic[orta[0]][orta[1]-1]==0 and dic[orta[0]+1][orta[1]+1]==0:
                            self.pos = 0
                            dic[orta[0]+1][orta[1]-1] = 0
                            dic[orta[0] + 2][orta[1] -1] = 0
                            dic[orta[0] ][orta[1]-1] = 1
                            dic[orta[0] +1][orta[1]+1] = 1
                            self.indexes = [[orta[0], orta[1] -1 ], [orta[0] , orta[1]], [orta[0] + 1, orta[1] ], [orta[0] + 1, orta[1]+1]]
                if self.type =="L":
                    if self.pos==0:
                        orta=self.indexes[0]
                        if orta[0]>0 and dic[orta[0]][orta[1]+1]==0 and dic[orta[0]-1][orta[1]+1]==0 :
                            self.pos=90
                            dic[orta[0]][orta[1]] = 0
                            dic[orta[0] + 1][orta[1] +2] = 0
                            dic[orta[0] ][orta[1]+1] = 1
                            dic[orta[0] -1][orta[1]+1] = 1
                            self.indexes = [[orta[0]+1, orta[1]  ], [orta[0] +1, orta[1]+1], [orta[0] , orta[1]+1 ], [orta[0] -1, orta[1]+1]]
                    elif self.pos==90 :
                        orta=self.indexes[0]
                        if orta[1]>0 and dic[orta[0]-1][orta[1]] ==0 and  dic[orta[0]-1][orta[1]-1]==0:
                            self.pos=180
                            dic[orta[0]][orta[1]] = 0
                            dic[orta[0] -2][orta[1] +1] = 0
                            dic[orta[0] -1][orta[1]-1] = 1
                            dic[orta[0] -1][orta[1]] = 1
                            self.indexes= [[orta[0],orta[1]+1],[orta[0]-1,orta[1]+1],[orta[0]-1,orta[1]],[orta[0]-1,orta[1]-1]]
                           

                    elif self.pos==180 :

                        self.pos=270
                        orta=self.indexes[2]
                        if dic[orta[0]-1][orta[1]] == 0 and dic[orta[0]-1][orta[1]+1]==0 and dic[orta[0]+1][orta[1]]==0:
                            dic[orta[0]][orta[1]-1] = 0
                            dic[orta[0] ][orta[1] +1] = 0
                            dic[orta[0] +1][orta[1] +1] = 0
                            dic[orta[0]-1][orta[1]] = 1
                            dic[orta[0] -1][orta[1]+1] = 1    
                            dic[orta[0]+1][orta[1]] = 1
                            self.indexes=[[orta[0]+1,orta[1]],orta,[orta[0]-1,orta[1]],[orta[0]-1,orta[1]+1]  ]
                    elif self.pos==270:
                        self.pos=0
                        orta=self.indexes[1]
                        if  10>orta[1] and dic[orta[0]+1][orta[1]+1]==0 and dic[orta[0]+1][orta[1]+2]==0  :
                            dic[orta[0] -1][orta[1] +1] = 0
                            dic[orta[0] -1][orta[1] ] = 0
                            dic[orta[0]+1][orta[1]+2] = 1
                            dic[orta[0]+1][orta[1]+1] = 1  

                            self.indexes=[orta,[orta[0]+1,orta[1]],[orta[0]+1,orta[1]+1],[orta[0]+1,orta[1]+2]]


    
            if pressed_keys[K_DOWN]:
                global score
                while (not self.stopped):
                    self.auto_down()
                    score +=2
               


                last_move_time = current_time
            elif pressed_keys[K_LEFT]:
                last_move_time = current_time

                engell = False
                for index in self.indexes:
                    if  index[1]<1 or dic[index[0]][index[1]-1] == 1 and [index[0] , index[1]-1] not in self.indexes:
                        engell = True
                        break
                if not engell:
                    for index in self.indexes:
                        dic[index[0]][index[1]] = 0
                    for index in self.indexes:
                        dic[index[0] ][index[1]-1] = 1
                    for index in self.indexes:
                        index[1] -= 1
            elif pressed_keys[K_RIGHT]:
                last_move_time = current_time

                engell = False
                for index in self.indexes:
                    if  index[1]>10 or dic[index[0]][index[1]+1] == 1 and [index[0] , index[1]+1] not in self.indexes:
                        engell = True
                        break
                if not engell:
                    for index in self.indexes:
                        dic[index[0]][index[1]] = 0
                    for index in self.indexes:
                        dic[index[0] ][index[1]+1] = 1
                    for index in self.indexes:
                        index[1] += 1

def new_player():
    return Player()


players = [Player()]


def draw():
    for player in players:
        for index in player.indexes:
            pygame.draw.rect(screen, player.colour, (100 + 50 * index[1], 50 + 50 * index[0], 50, 50))

while not exit:

    if score>500 and score<1000:
        auto_move_delay=530
    if score>1000 and score<1500 :
        auto_move_delay = 450
    if score>1500 and score<2000 :
        auto_move_delay = 380
    if score>2000  :
        auto_move_delay = 30
    for player in players:
        if exit:
            break
        for index in player.indexes:
            
            if index[0]<2 and player.stopped:
                play_again = game_over(screen,score)
                if play_again:
                    score=0
                    players = [Player()]
                    dic = [
                        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],

                        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
                    ]
                    break
                else :

                    exit = True
                    break

    for event in pygame.event.get():
        if event.type == QUIT:
            exit = True
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                exit = True

    pressed_keys = pygame.key.get_pressed()
    current_time = pygame.time.get_ticks()

    for player in players:
        player.update(pressed_keys)
    if current_time - last_auto_move_time > auto_move_delay:
        for player in players:
            player.auto_down()

        last_auto_move_time = current_time

    draw()
    for i in range(13):
        pygame.draw.line(screen, (255, 255, 255), (100, 50 + 50 * i), (700, 50 + 50 * i))
    for k in range(13):
        pygame.draw.line(screen, (255, 255, 255), (100 + 50 * k, 50), (100 + 50 * k, 650))

    score_text = font.render(f"Score: {score}", True, (255, 255, 255))
    screen.blit(score_text, (360, 700))  # Draw score at (20,20)

    pygame.display.flip()
    screen.fill((0, 0, 0))
