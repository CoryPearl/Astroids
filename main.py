import pygame
import random
import math

#record 152

pygame.init()
screen_width = 1280
screen_height = 720
screen = pygame.display.set_mode((screen_width, screen_height))
clock = pygame.time.Clock()
running = True
font = pygame.font.SysFont('Comic Sans MS', 30)
font_large = pygame.font.SysFont('Comic Sans MS', 45)
score = 0
game_tick_count = 0
spawn_rate = 45
heal_rate = 25

rates = {
    15: 35,
    30: 25,
    45: 20,
    60: 15,
    75: 10,
    90: 5,
    115: 4,
    130: 3,
    145: 2,
    150: 1,
}

class Objects():
    def __init__(self):
        pass

class Player(Objects):
    def __init__(self,x,y,dx,dy):

        super().__init__()

        self.x = x
        self.y = y
        self.dx = dx
        self.dy = dy
        self.hp = 100
        self.speed = 2
        self.boost = 100

    def draw(self, dx, dy):
        pygame.draw.line(screen,(255,255,255), (self.x, self.y), (self.x + (dx*35), self.y + (dy*35)),2)
        pygame.draw.circle(screen,(255,255,255),(self.x,self.y),14)
        pygame.draw.circle(screen,(0,0,0),(self.x,self.y),12)
    
    def update(self):
        if  0 < self.x < screen_width and 0 < self.y < screen_height:
            if player.boost > 0:
                self.x += self.dx * self.speed
                self.y += self.dy * self.speed
            else:
                self.x += self.dx * 2
                self.y += self.dy * 2
        if self.x > screen_width:
            self.x -= 5
        elif self.x < 0:
            self.x += 5
        if self.y > screen_height:
            self.y -= 5
        elif self.y < 0:
            self.y += 5

class Bullet():
    def __init__(self,x,y,dx,dy):
        self.x = x
        self.y = y
        self.dx = dx
        self.dy = dy
        self.speed = 25

    def draw(self):
        pygame.draw.line(screen, (255,255,255), (self.x,self.y),(self.x + (self.dx*25), self.y + (self.dy*25)),2)
    
    def update(self):
        self.x += self.dx * self.speed
        self.y += self.dy * self.speed

class Astroid():
    def __init__(self):
        self.size = random.randint(15, 45)
        sideX = random.randint(1,2)
        sideY = random.randint(1,2)

        self.kind = random.randint(1,heal_rate)
        self.heal = False

        if self.kind == 7:
            self.heal = True

        if sideX == 1:
            self.x = -50
            self.dx = random.randint(1,7)
            
        elif sideX == 2:
            self.x = 1330
            self.dx = random.randint(-7,-1)
        
        if sideY == 1:
            self.y = -50
            self.dy = random.randint(1,7)
        elif sideY == 2:
            self.y = 770
            self.dy = random.randint(-7,-1)

        self.sides = random.randint(7,11)
    
    def draw(self):
        points = []
        for i in range(self.sides):
            angle_deg = 45 * i
            angle_rad = math.radians(angle_deg)
            x = self.x + self.size * math.cos(angle_rad)
            y = self.y + self.size * math.sin(angle_rad)
            points.append((x, y))
        
        if self.heal == True:
            pygame.draw.polygon(screen,(0,255,0), points,3)
        else:
            pygame.draw.polygon(screen,(255,255,255), points,3)
        pygame.draw.polygon(screen,(0,0,0), points,1)

    def update(self):
        self.x += self.dx
        self.y += self.dy

class LoseText():
    def __init__(self):
        self.x = 5
        self.y = 5
        self.dx = 2
        self.dy = 2

    def draw(self):       
        dead_text = font_large.render("You lose! Final Score:" + str(score) ,False, (255,255,255))
        screen.blit(dead_text, (self.x,self.y))
    
    def update(self):
        if self.x > screen_width - 475:
            self.x -= 5
            self.dx = -2
        elif self.x < 0:
            self.x += 5
            self.dx = 2
            
        if self.y > screen_height - 40:
            self.y -= 5
            self.dy = -2
        elif self.y < 0:
            self.y += 5
            self.dy = 2

        self.x += self.dx
        self.y += self.dy


def draw_score():
    start_text = font.render('Score: ' + str(score),False, (255,255,255))
    screen.blit(start_text, (5,0))

def draw_bars():
    #healthbar
    start_text = font.render('HP:',False, (255,255,255))
    screen.blit(start_text, (925,3))
    pygame.draw.rect(screen, (255,255,255),(978,5,297,40))
    pygame.draw.rect(screen, (0,0,0),(979,6,2.95 * player.hp,38))

    #boost bar
    start_text = font.render('Boost:',False, (255,255,255))
    screen.blit(start_text, (885,48))
    pygame.draw.rect(screen, (255,255,255),(978,50,297,40))
    pygame.draw.rect(screen, (0,0,0),(979,51,2.95 * player.boost,38))

bullets = []
astroids = []
player = Player(screen_width/2,screen_height/2,1,1)
lose_text = LoseText()

while running:
    if player.hp > 0:
        press_state = pygame.mouse.get_pressed()

        if press_state[0] == True:
            if player.boost > 0:
                player.boost -= 1.5
                player.speed = 7
        else:
            if player.boost < 100:
                player.boost += 0.5
                player.speed = 2

        mouse_pos = pygame.mouse.get_pos()

        x1 = player.x
        y1 = player.y
        x2 = mouse_pos[0]
        y2 = mouse_pos[1]

        player.mouseX = mouse_pos[0]
        player.mouseY = mouse_pos[1]

        dx = x2 - x1
        dy = y2 - y1

        distance = pygame.math.Vector2(dx, dy)
        direction = distance.normalize()

        player.dx = direction[0]
        player.dy = direction[1]

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    newBullet = Bullet(x1,y1,direction[0],direction[1])
                    bullets.append(newBullet)

            if event.type == pygame.QUIT:
                running = False

        screen.fill("black")

        if game_tick_count % spawn_rate == 0:
            astroids.append(Astroid())
        
        for item in astroids:
            for bullet in bullets:
                if item.x-item.size <= bullet.x <= item.x+item.size and item.y-item.size <= bullet.y <= item.y+item.size:
                    if item.heal == True:
                        if player.hp < 100:
                            player.hp += 10
                    score += 1
                    astroids.remove(item)
                    bullets.remove(bullet)
        
        for item in astroids:
            if item.x-item.size <= player.x <= item.x+item.size and item.y-item.size <= player.y <= item.y+item.size:
                if item.heal == False:
                    astroids.remove(item)
                    player.hp -= 20
                elif item.heal == True:
                    astroids.remove(item)
                    if player.hp < 100:
                        player.hp += 10
            item.update()
            item.draw()

        for bullet in bullets:
            if  0 < bullet.x < screen_width and 0 < bullet.y < screen_height:
                bullet.draw()
                bullet.update()
            else:
                bullets.remove(bullet)
        player.draw(direction[0],direction[1])
        player.update()
        draw_score()
        draw_bars()

        if score in rates:
            spawn_rate = rates[score]

        game_tick_count += 1

    if player.hp <= 0:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill("black")
        lose_text.draw()
        lose_text.update()

    pygame.display.flip()
    pygame.display.set_caption('Astroid Defence | FPS: ' + str(int(clock.get_fps())))
    clock.tick(60)


pygame.quit()