from pygame.locals import *
import random
import pygame
import math
import time


WIDTH = 600
HEIGHT = 400

routex = [0, 100, 100, 220, 220, 380, 380, 600, 0]
routey = [220, 220, 100, 100, 260, 260, 180, 180, 0]

backimg = pygame.image.load("Tower Defense res/background_path.png")
towerimg = pygame.image.load("Tower Defense res/tower.png")
tower2img = pygame.image.load("Tower Defense res/tower2.png")
enemyimg = pygame.image.load("Tower Defense res/enemy.png")
bigenemyimg =  pygame.image.load("Tower Defense res/bigenemy.png")

#Three type 1 then a break then four type 1 then a break.. etc.
waves = [1,1,1,0,1,1,1,1,0,1,1,1,1,1,2,0,1,2,1,2,1,2,1,0]

EMPTY_SQUARES = [[0,0,0,0,0,-1,0,0,0,0],[0,0,0,0,0,-1,0,0,0,0],[0,0,-1,-1,-1,-1,0,0,0,0],[0,0,-1,0,0,0,0,0,0,0],[0,0,-1,0,0,0,0,0,0,0],[0,0,-1,-1,-1,-1,-1,0,0,0],[0,0,0,0,0,0,-1,0,0,0],[0,0,0,0,0,0,-1,0,0,0],[0,0,0,0,0,0,-1,0,0,0],[0,0,0,0,-1,-1,-1,0,0,0],[0,0,0,0,-1,0,0,0,0,0],[0,0,0,0,-1,0,0,0,0,0],[0,0,0,0,-1,0,0,0,0,0],[0,0,0,0,-1,0,0,0,0,0],[0,0],[0,0,0,0,0,-1,0,0,0,0],[0,0,-1,-1,-1,-1,0,0,0,0],[0,0,-1,0,0,0,0,0,0,0],[0,0,-1,0,0,0,0,0,0,0],[0,0,-1,-1,-1,-1,-1,0,0,0],[0,0,0,0,0,0,-1,0,0,0],[0,0,0,0,0,0,-1,0,0,0],[0,0,0,0,0,0,-1,0,0,0],[0,0,0,0,-1,-1,-1,0,0,0],[0,0,0,0,-1,0,0,0,0,0],[0,0,0,-1,0,0,0,0,0]]

#Baddie class
class Baddie:
    def __init__(self, health):
        self.dest = 1
        self.health = health
        self.rect = pygame.Rect(routex[0], routey[0], 10, 10)

    def move(self):
        if self.rect.x < routex[self.dest]:
            self.rect.x += 1
        elif self.rect.x > routex[self.dest]:
            self.rect.x -= 1
        if self.rect.y < routey[self.dest]:
            self.rect.y += 1
        elif self.rect.y > routey[self.dest]:
            self.rect.y -= 1
        if (self.rect.x == routex[self.dest]):
            if (self.rect.y == routey[self.dest]):
                self.dest += 1

    def draw(self, screen):
        screen.blit(enemyimg, (self.rect.x-10, self.rect.y-10))
        #pygame.draw.rect(screen, (0,0,255), pygame.Rect(self.rect.x-10, self.rect.y-10, 20, 20))

class BigBaddie(Baddie):
    def __init__(self, health):
        super().__init__(health)

    def draw(self, screen):
        screen.blit(bigenemyimg, (self.rect.x-10,self.rect.y-10))

class Tower:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.reload = 20

    def shoot(self, baddies, bullets, screen):
        self.reload -= 1
        if(self.reload <=0):
            self.reload = 20
            for i in range (0, len(baddies)):
                xx = baddies[i].rect.x-self.x-20
                yy = baddies[i].rect.y-self.y-20
                dist = math.hypot(xx,yy)
                if(dist <125):
                    xp = (20 * xx) / (abs(xx) + abs(yy))
                    yp = (20 * yy) / (abs(xx) + abs(yy))
                    bullet = Bullet(self.x+20, self.y+20, xp, yp)
                    bullets.append(bullet)
                    return

    def draw(self, screen):
        screen.blit(towerimg, (self.x, self.y))
        #pygame.draw.rect(screen, (0,255,0), pygame.Rect(self.x, self.y, 40, 40))

class LaserTower(Tower):
    def __init__(self,x,y):
        super().__init__(x,y)

    def shoot(self, baddies, bullets, screen):
        for i in range(0, len(baddies)):
            xx = baddies[i].rect.x - self.x - 20
            yy = baddies[i].rect.y - self.y - 20
            dist = math.hypot(xx, yy)
            if dist >= 125:
                continue
            pygame.draw.line(screen, (255,0,0),(self.x+20,self.y+20),(baddies[i].rect.x,baddies[i].rect.y))
            baddies[i].health -= 0.08
            return

    def draw(self, screen):
        screen.blit(tower2img,(self.x,self.y))

class Bullet:
    #constructor
    def __init__(self,x,y,xv,yv):
        self.rect = pygame.Rect(x, y, 10, 10)
        self.xv = xv
        self.yv = yv

        #move bullet
    def move(self, baddies):
        self.rect.x = self.rect.x + self.xv
        self.rect.y = self.rect.y + self.yv
        #hit boundary wall so not needed, xv used to null bullet
        if ((self.rect.x > WIDTH) or (self.rect.x < 0)):
            self.xv = 0
        if ((self.rect.x > HEIGHT) or (self.rect.x < 0)):
            self.yv = 0
        for i in range(0, len(baddies)):
            if(self.rect.colliderect(baddies[i].rect)):
                baddies[i].health -= 1
                self.xv = 0
                self.yv = 0
                return

    def draw(self, screen):
        pygame.draw.rect(screen, (255,255,255), pygame.Rect(self.rect.x-3, self.rect.y-3, 6, 6))


def main(screen):

    font = pygame.font.SysFont("comicsansms",16)
    clock = pygame.time.Clock()
    baddies = []
    bullets = []
    towers = []
    print(towers)
    empty_squares = EMPTY_SQUARES
    health = 20
    score = 0
    gold = 200

    tower1cost = 100
    tower2cost = 150
    tower_selected = 0

    tick = int(time.time())
    next_item = 0

    #Main Game Loop
    running = True
    game_over = False
    while running == True:
        clock.tick(60)
        if (int(time.time()) != tick):
            tick = int(time.time())
            score += 1
            if len(waves):
                next_item = waves[0]
                if(next_item == 1):
                    baddie = Baddie(5)
                    baddies.append(baddie)
                    waves.pop(0)
                elif(next_item == 2):
                    baddie = BigBaddie(20)
                    baddies.append(baddie)
                    waves.pop(0)
                else:
                    if(len(baddies) == 0):
                        waves.pop(0)
            else:
                #a third of small baddies if no waves left
                if(random.randint(0,2)==0):
                    baddie = Baddie(5)
                else:
                    baddie = BigBaddie(20)
                baddies.append(baddie)

        #get ESCAPE to quit
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                running = False
            if (e.type == KEYDOWN and e.key == K_ESCAPE):
                running = False
            if (e.type == KEYDOWN and e.key == K_0):
                tower_selected = 0
            if (e.type == KEYDOWN and e.key == K_1 and gold >= tower1cost):
                tower_selected = 1
            if (e.type == KEYDOWN and e.key == K_2 and gold >= tower2cost):
                tower_selected = 2
            if e.type == pygame.MOUSEBUTTONDOWN:
                if (tower_selected != 0):
                    (mx, my) = pygame.mouse.get_pos()
                    mx = (mx // 40)
                    my = (my//40)
                    if (empty_squares[mx][my] == 0):
                        empty_squares[mx][my] = 1
                        mx = mx * 40
                        my = my * 40
                        tower = Tower(mx, my)
                        if (tower_selected == 1):
                            tower = Tower(mx, my)
                            gold -= tower1cost
                        elif (tower_selected == 2):
                            tower = LaserTower(mx, my)
                            gold -= tower2cost
                        towers.append(tower)
                        tower_selected = 0

        if (health <= 0):
            running = False
            game_over = True


        #move and draw
        screen.fill((0,0,0))
        screen.blit(backimg, (0,0))

        for i in range(0, len(baddies)):
            baddies[i].move()
            baddies[i].draw(screen)
        for i in range(0, len(bullets)):
            bullets[i].move(baddies)
            bullets[i].draw(screen)
        for i in range(0, len(towers)):
            towers[i].shoot(baddies, bullets, screen)
            towers[i].draw(screen)

        if (tower_selected != 0):
            (mx, my) = pygame.mouse.get_pos()
            mx = (mx // 40)
            my = (my//40)
            if (empty_squares[mx][my] == 0):
                mx = mx * 40
                my = my * 40
                pygame.draw.circle(screen, (0,0,255), (mx+20, my+20), 125, 1)
                pygame.draw.rect(screen, (255,255,255), pygame.Rect(mx, my, 40, 40))


        healthtext = font.render("Health: " +str(health), True, (255, 255, 255))
        scoretext = font.render("Score: " +str(score), True, (255, 255, 255))
        goldtext = font.render("Gold: " +str(gold), True, (255, 255, 255))
        text = ""
        if (gold < tower1cost):
            text = "Not enough gold. "
            tower_selected = 0
        if (gold >= tower2cost):
            text += "Press 1 for type 1 and 2 for type 2. "
        elif (gold >= tower1cost):
            text = "Can build tower 1. "
        if (tower_selected == 0):
            text += "No type selected. "
        elif (tower_selected == 1):
            text += "Type 1 selected, place tower. "
        elif (tower_selected == 2):
            text += "Type 2 selected, place tower. "
        towertext = font.render(text, True, (255,255,255))
        if (game_over == True):
            overtext = font.render("GAME OVER", True, (0,0,0))
            screen.blit(overtext, (400, 360))

        screen.blit(healthtext,(10, 10))
        screen.blit(scoretext,(510, 10))
        screen.blit(goldtext,(280, 10))
        screen.blit(towertext, (10, 360))
        pygame.display.flip()

        #remove stale buddies
        for i in range(0, len(baddies)):
            if (baddies[i].dest == (len(routex)-1)):
                baddies.pop(i)
                health-=1
                break
        for i in range(0, len(baddies)):
            if (baddies[i].health <=0):
                baddies.pop(i)
                gold+= 10
                break
        for i in range(0, len(bullets)):
            if ((bullets[i].xv == 0) and bullets[i].yv == 0):
                bullets.pop(i)
                break

    while game_over == True:
        clock.tick(10)
        #get escape to quit
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                game_over = False
            if ((e.type == KEYDOWN) and (e.key == K_ESCAPE)):
                game_over = False

    return score
