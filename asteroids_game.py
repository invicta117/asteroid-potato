import pygame
import math
from random import randint
import neat
import os

pygame.init()
BLACK = (0,0,0)
WHITE = (255, 255 , 255)
clock = pygame.time.Clock()
win = pygame.display.set_mode((700, 500))
background = pygame.Surface(win.get_size())
background.fill((0, 0, 0))

pygame.display.set_caption("First Game")
image = pygame.image.load(os.path.join("images","ship.png"))
image_acc = pygame.image.load(os.path.join("images","ship_acc.png"))

class player(object):
    def __init__(self, x, y, width, height):
        self.image = image
        self.x = x
        self.y = y
        self.angle = 0
        self.width = width
        self.height = height
        self.vel = 5
        self.walkCount = 0
        self.jumpCount = 10
        self.rocket_fire = True
        self.velocity = [0, 0]
        self.direction = [0, 0]
        self.rect = self.image.get_rect()
        self.orig_image = self.image
        self.hitbox = (self.x, self.y, 25, 25)
        self.dead = False

    def draw(self, win):
        if self.rocket_fire:
            self.image = image
        else:
            self.image = image_acc

        self.rotate()
        win.blit((self.image), (self.x, self.y))
        self.hitbox = (self.x, self.y, 25, 25)
        #pygame.draw.rect(win, (255, 0, 0), self.hitbox, 2)

    def move(self):
        self.direction[0] = math.sin(-math.radians(self.angle))
        self.direction[1] = -math.cos(math.radians(self.angle))
        self.velocity[0] += self.direction[0] * 0.1
        self.velocity[1] += self.direction[1] * 0.1
        if self.velocity[0] >= 3:
            self.velocity[0] = 3
        if self.velocity[0] <= -3:
            self.velocity[0] = -3
        if self.velocity[1] >= 3:
            self.velocity[1] = 3
        if self.velocity[1] <= -3:
            self.velocity[1] = -3

    def update(self):
        self.x += self.velocity[0]
        self.y += self.velocity[1]
        if self.x > 700:
            self.x = 0
        if self.x < 0:
            self.x = 700
        if self.y < 70:
            self.y = 500
        if self.y > 500:
            self.y = 70


    def left(self):
        self.angle += 10

    def right(self):
        self.angle -= 10


    def rotate(self):
        """Rotate the image of the sprite around its center."""

        if self.rocket_fire:
            self.image = image
        else:
            self.image = image_acc

        self.orig_image = self.image
        self.image = pygame.transform.rotozoom(self.orig_image, self.angle, 1)
        # Create a new rect with the center of the old rect.
        self.rect = self.image.get_rect(center=self.rect.center)

    def die(self):
        self.x = 350
        self.y = 250
        self.angle = 0
        self.velocity = [0, 0]



class projectile(object):
    def __init__(self,x,y,radius,color, angle):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.velocity = [0,0]
        self.direction = [0, 0]
        self.direction[0] = math.sin(-math.radians(angle))
        self.direction[1] = -math.cos(math.radians(angle))
        self.velocity[0] = self.direction[0] * 10
        self.velocity[1] = self.direction[1] * 10
        self.hitbox = (self.x+3, self.y+3, 12, 12)

    def update(self):
        self.x += self.velocity[0]
        self.y += self.velocity[1]
        if self.x > 700:
            self.x = 0
        if self.x < 0:
            self.x = 700
        if self.y < 70:
            self.y = 500
        if self.y > 500:
            self.y = 70

    def draw(self,win):
        pygame.draw.circle(win, self.color, (round(self.x+10),round(self.y+10)), self.radius)
        self.hitbox = (self.x+5, self.y+5, 10, 10)
        #pygame.draw.rect(win, (255, 0, 0), self.hitbox, 2)



class a(object):
    def __init__(self,x,y,size):
        self.size = size
        self.x = x
        self.y = y
        if size == "large":
            self.radius = 30
            self.hitbox = (self.x - 30, self.y - 30, 60, 60)
        elif size == "medium":
            self.hitbox = (self.x - 20, self.y - 20, 40, 40)
            self.radius = 20
        elif size == "small":
            self.radius = 10
            self.hitbox = (self.x - 10, self.y - 10, 20, 20)
        self.color = (255,255,255)
        self.velocity = [randint(-3,3),randint(-3,3)]
        #self.hitbox = (self.x - 15, self.y - 15, 30, 30)

    def update(self):
        self.x += self.velocity[0]
        self.y += self.velocity[1]
        if self.x > 700:
            self.x = 0
        if self.x < 0:
            self.x = 700
        if self.y < 70:
            self.y = 500
        if self.y > 500:
            self.y = 70

    def draw(self,win):
        pygame.draw.circle(win, self.color, (round(self.x),round(self.y)), self.radius, 1)
        if self.size == "small":
            self.hitbox = (self.x - 10, self.y - 10, 20, 20)
        elif self.size == "medium":
            self.hitbox = (self.x - 20, self.y - 20, 40, 40)
        else:
            self.hitbox = (self.x - 30, self.y - 30, 60, 60)
        #self.hitbox = (self.x-15, self.y-15, 30, 30)
        #pygame.draw.rect(win, (255, 0, 0), self.hitbox, 2)

def redrawGameWindow():
    win.blit(background, (0, 0))
    for i in range(number_lives):
        win.blit(image, (500 + (i * 30), 20))

    text = font.render("SCORE " + str(score), 1, WHITE)
    win.blit(text, (10, 10))
    pygame.draw.line(win, WHITE, [0, 55], [700, 55], 5)

    for bullet in bullets:
        bullet.draw(win)
    for asteroid in asteroids:
        asteroid.draw(win)

    if man.dead == False:
        man.draw(win)
    elif man.dead == True and death_cool_down % 5 == 0:
        man.draw(win)

    pygame.display.update()


# mainloop

number_lives = 3
font = pygame.font.Font(None, 50)
man = player(350, 250, 64, 64)
asteroids = []
num_asteroids = 5
random_range = []
for x in range(num_asteroids):
    inside = True
    while inside == True:
        asteroid_x = randint(0, 700)
        asteroid_y = randint(100, 500)
        distance = math.sqrt(((asteroid_x - 350) **2) + ((asteroid_y - 250) **2))
        if distance > 100:
            inside = False
            random_range.append([asteroid_x, asteroid_y])

for num in range(num_asteroids):
    asteroids.append(a(random_range[num][0], random_range[num][1], "large"))


bullets = []
death_cool_down = 0
angle = 0
shoot_cool = 0
bullet_life = []
run = True
score = 0
gameState = "Menu"
while run:
    clock.tick(27)

    keys = pygame.key.get_pressed()

    while gameState == "Menu":
        win.fill(BLACK)
        text = font.render("WECOME! ", 1, WHITE)
        win.blit(text, (250, 150))
        text = font.render("Please press enter to play", 1, WHITE)
        win.blit(text, (130, 200))
        text = font.render("Please press X to exit", 1, WHITE)
        win.blit(text, (170, 250))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                gameState = "quitting"
                carryOn = False
                pygame.quit()
                quit()
                break
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_x:
                    carryOn = False
                    pygame.quit()
                    quit()
                    break
                gameState = "Playing"
        pygame.display.update()
        clock.tick(5)


    for event in pygame.event.get():  # User did something
        if event.type == pygame.QUIT:  # If user clicked close
            carryOn = False  # Flag that we are done so we exit this loop
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_x:
                carryOn = False
                pygame.quit()
                quit()
                break

    if shoot_cool > 0:
        shoot_cool += 1
    if shoot_cool > 10:
        shoot_cool = 0

    if keys[pygame.K_RIGHT]:
        man.right()

    if keys[pygame.K_LEFT]:
        man.left()

    if keys[pygame.K_UP]:
        man.rocket_fire = False
        man.move()
    else:
        man.rocket_fire = True


    if keys[pygame.K_SPACE] and shoot_cool == 0:
        if len(bullets) < 5:
            bullets.append(projectile(round(man.x), round(man.y), 6, (255,255, 255), man.angle))
            bullet_life.append(0)

    for bullet in bullets:
        bullet.update()

    for bullet in bullets:
        bullet_life[bullets.index(bullet)] += 1
        if bullet_life[bullets.index(bullet)] > 60:
            bullet_life[bullets.index(bullet)] = 0
            bullet_life.pop(bullets.index(bullet))
            bullets.pop(bullets.index(bullet))


    for asteroid in asteroids:
        asteroid.update()


    for asteroid in asteroids:
        if man.hitbox[1] < asteroid.hitbox[1] + asteroid.hitbox[3] and man.hitbox[1] + man.hitbox[3] > asteroid.hitbox[1]:
            if man.hitbox[0] + man.hitbox[2] > asteroid.hitbox[0] and man.hitbox[0] < asteroid.hitbox[0] + asteroid.hitbox[2]:
                if man.dead == False:
                    number_lives -= 1
                    man.die()
                    man.dead = True
                    death_cool_down = 0


    death_cool_down +=1
    if death_cool_down >= 60 and man.dead == True:
        man.dead = False

    for bullet in bullets:
        for asteroid in asteroids:
            if bullet.hitbox[1] < asteroid.hitbox[1] + asteroid.hitbox[3] and bullet.hitbox[1] + bullet.hitbox[3] > asteroid.hitbox[1]:
                if bullet.hitbox[0] + bullet.hitbox[2] > asteroid.hitbox[0] and bullet.hitbox[0] < asteroid.hitbox[0] + asteroid.hitbox[2]:
                    bullets.pop(bullets.index(bullet))
                    if asteroid.size == "large":
                        asteroids.append(a(asteroid.x, asteroid.y, "medium"))
                        asteroids.append(a(asteroid.x, asteroid.y, "medium"))
                    if asteroid.size == "medium":
                        asteroids.append(a(asteroid.x, asteroid.y, "small"))
                        asteroids.append(a(asteroid.x, asteroid.y, "small"))
                    asteroids.pop(asteroids.index(asteroid))
                    score += 1
                    break

    num_big = 0
    total_asteroids = 0
    for asteroid in asteroids:
        total_asteroids += 1
        if asteroid.size == "large":
            num_big += 1

    if num_big <= 2 and total_asteroids <=10:
        asteroids.append(a(randint(0,500), randint(0,700), "large"))


    shoot_cool += 1
    man.update()
    redrawGameWindow()


    if number_lives <= 0:
        pygame.quit()
        carryOn = False
        quit()
        break



pygame.quit()
