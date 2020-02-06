import matplotlib.pyplot as plt
import pygame
import math
from random import randint
import neat
import os
from operator import itemgetter
import numpy as np
import csv

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

    def move(self, accel):
        self.direction[0] = math.sin(-math.radians(self.angle))
        self.direction[1] = -math.cos(math.radians(self.angle))
        self.velocity[0] += self.direction[0] * accel
        self.velocity[1] += self.direction[1] * accel
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


    def left(self, ang):
        self.angle += ang

    def right(self, ang):
        self.angle -= ang


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
        self.velocity = [randint(-2,2),randint(-2,2)]
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


#man,
def redrawGameWindow(background, image, score, bullets, asteroids, man, number_lives, generation_high_score, gen_number):

    for i in range(len(bullets)):
        for bullet in bullets[i]:
            bullet.draw(win)
    for i in range(len(asteroids)):
        for asteroid in asteroids[i]:
            asteroid.draw(win)
    for i in range(len(man)):
        man[i].draw(win)

    win.blit(background, (0, 0))

    for j in range(len(number_lives)):
        if number_lives[j] > 0:
            for i in range(number_lives[j]):
                win.blit(image, (550 + (i * 30), 20))

    font = pygame.font.Font(None, 30)
    if len(score) >= 1:
        high_score = 0 #score.index(max(score))
        text = font.render("Current Score " + str(score[high_score]), 1, WHITE)
        text1 = font.render("# Alive " + str(len(man)), 1, WHITE)
        text2 = font.render("Gen High Score " + str(generation_high_score), 1, WHITE)
        text3 = font.render("Gen Number " + str(gen_number), 1, WHITE)
        win.blit(text3, (350, 30))
        win.blit(text2, (10, 10))
        win.blit(text1, (350, 10))
        man[high_score].draw(win)
        for asteroid in asteroids[high_score]:
            asteroid.draw(win)
        for bullet in bullets[high_score]:
            bullet.draw(win)
    else:
        text = font.render("SCORE " + str(0), 1, WHITE)

    win.blit(text, (10, 30))
    pygame.draw.line(win, WHITE, [0, 55], [700, 55], 5)


    pygame.display.update()


def torus_distance(asteroid, man):
    if abs(asteroid.x - man.x) > 350:
        distance_x = 700 - abs(asteroid.x - man.x)
    else:
        distance_x = abs(asteroid.x - man.x)
    if abs(asteroid.y - man.y) > 250:
        distance_y = 500 - abs(asteroid.y - man.y)
    else:
        distance_y = abs(asteroid.y - man.y)

    return np.sqrt((distance_x **2) + (distance_y**2))

def torus_angle(asteroid, man):
    if man.x > asteroid.x:
        if abs(man.x - asteroid.x) > 350:
            distance_x = (700 - man.x) + (asteroid.x)
        else:
            distance_x = (asteroid.x - man.x)
    else:
        if abs(man.x - asteroid.x) > 350:
            distance_x = (man.x) + (700 - asteroid.x)
        else:
            distance_x = (asteroid.x - man.x)
    if man.y > asteroid.y:
        if abs(man.y - asteroid.y) > 250:
            distance_y = (500 - man.y) + (asteroid.y)
        else:
            distance_y = (asteroid.y - man.y)
    else:
        if abs(man.y - asteroid.y) > 250:
            distance_y = (man.y) + (500 - asteroid.y)
        else:
            distance_y = (asteroid.y - man.y)
    return (np.degrees(np.arctan2(distance_x,(distance_y * (-1)))) * (-1)) % 360


store_high_score = []
gen_number = -1
def eval_genomes(genomes, config):
    # mainloop
    global gen_number, store_high_score
    store_high_score.append(0)
    gen_number +=1
    nets = []
    ge = []
    for genome_id, genome in genomes:
        genome.fitness = 0  # start with fitness level of 0
        net = neat.nn.FeedForwardNetwork.create(genome, config)
        nets.append(net)
        ge.append(genome)

    population = 150
    number_lives = []
    score = []
    shoot_cool = []
    no_move_timeout = []
    for y in  range(population):
        number_lives.append(1)
        score.append(0)
        shoot_cool.append(0)
        no_move_timeout.append(0)

    neat_bullets = []
    for individual in range(population):
        neat_bullets.append([])

    #bullets = []
    neat_man = []
    neat_asteroids = []
    for y in  range(population):
        man = player(350, 250, 64, 64)
        neat_man.append(man)
        asteroids = []
        num_asteroids = 5
        random_range = []
        for x in range(num_asteroids):
            inside = True
            while inside == True:
                asteroid_x = randint(0, 700)
                asteroid_y = randint(100, 500)
                distance = math.sqrt(((asteroid_x - 350) ** 2) + ((asteroid_y - 250) ** 2))
                if distance > 100:
                    inside = False
                    random_range.append([asteroid_x, asteroid_y])
        for num in range(num_asteroids):
            asteroids.append(a(random_range[num][0], random_range[num][1], "large"))

        neat_asteroids.append(asteroids)


    bullet_life = []
    run = True
    generatiom_high_score = 0

    while run and len(neat_man) > 0:

        clock.tick(40)
        keys = pygame.key.get_pressed()

        for event in pygame.event.get():  # User did something
            if event.type == pygame.QUIT:  # If user clicked close
                carryOn = False  # Flag that we are done so we exit this loop
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_x:
                    carryOn = False
                    pygame.quit()
                    quit()
                    break

        asteroid_distances = []
        for individual in range(len(neat_man)):
            temp_distances = []
            for asteroid in neat_asteroids[individual]:
                ast_dist = torus_distance(asteroid, neat_man[individual])
                ast_angle = torus_angle(asteroid, neat_man[individual])
                temp_distances.append([ast_dist, ast_angle, asteroid])
            asteroid_distances.append(sorted(temp_distances, key=itemgetter(0)))

        for man in neat_man:  # give each bird a fitness of 0.1 for each frame it stays alive
            try:
                ge[neat_man.index(man)].fitness += 0.1
                output = nets[neat_man.index(man)].activate((len(neat_bullets[neat_man.index(man)]), man.y, man.x, man.velocity[0], man.velocity[1], asteroid_distances[neat_man.index(man)][0][0], asteroid_distances[neat_man.index(man)][0][1], asteroid_distances[neat_man.index(man)][0][2].radius, asteroid_distances[neat_man.index(man)][0][2].x, asteroid_distances[neat_man.index(man)][0][2].y, asteroid_distances[neat_man.index(man)][0][2].velocity[0], asteroid_distances[neat_man.index(man)][0][2].velocity[1], asteroid_distances[neat_man.index(man)][1][0], asteroid_distances[neat_man.index(man)][1][1], asteroid_distances[neat_man.index(man)][1][2].radius, asteroid_distances[neat_man.index(man)][1][2].x, asteroid_distances[neat_man.index(man)][1][2].y, asteroid_distances[neat_man.index(man)][1][2].velocity[0], asteroid_distances[neat_man.index(man)][1][2].velocity[1], asteroid_distances[neat_man.index(man)][2][0], asteroid_distances[neat_man.index(man)][2][1], asteroid_distances[neat_man.index(man)][2][2].radius, asteroid_distances[neat_man.index(man)][2][2].x, asteroid_distances[neat_man.index(man)][2][2].y, asteroid_distances[neat_man.index(man)][2][2].velocity[0], asteroid_distances[neat_man.index(man)][2][2].velocity[1], asteroid_distances[neat_man.index(man)][3][0], asteroid_distances[neat_man.index(man)][3][1], asteroid_distances[neat_man.index(man)][3][2].radius, asteroid_distances[neat_man.index(man)][3][2].x, asteroid_distances[neat_man.index(man)][3][2].y, asteroid_distances[neat_man.index(man)][3][2].velocity[0], asteroid_distances[neat_man.index(man)][3][2].velocity[1], asteroid_distances[neat_man.index(man)][4][0], asteroid_distances[neat_man.index(man)][4][1], asteroid_distances[neat_man.index(man)][4][2].radius, asteroid_distances[neat_man.index(man)][4][2].x, asteroid_distances[neat_man.index(man)][4][2].y, asteroid_distances[neat_man.index(man)][4][2].velocity[0], asteroid_distances[neat_man.index(man)][4][2].velocity[1], man.angle))
                if output[0] > 0.6:  # we use a tanh activation function so result will be between -1 and 1. if over 0.5 jump
                    man.right(10)
                elif output[0] > 0.2 and output[0] < 0.6:
                    man.right(5)
                elif output[0] < -0.6:
                    man.left(10)
                elif output[0] < -0.2 and output[0] > -0.6:
                    man.left(5)
                else:
                    pass


                if output[1] > 0:
                    man.rocket_fire = False
                    man.move(0.25)
                else:
                    man.rocket_fire = True


                if output[2] > 0:
                    if len(neat_bullets[neat_man.index(man)]) < 5:
                        neat_bullets[neat_man.index(man)].append(projectile(round(neat_man[neat_man.index(man)].x), round(neat_man[neat_man.index(man)].y), 6, (255,255, 255), neat_man[neat_man.index(man)].angle))
                        bullet_life.append(0)

            except IndexError:
                    run = False

        for individual in range(len(neat_man)):
            if shoot_cool[individual] >= 0:
                shoot_cool[individual] += 1
            if shoot_cool[individual] > 10:
                shoot_cool[individual] = 0



        for individual in range(len(neat_man)):
            for bullet in neat_bullets[individual]:
                bullet.update()

            for bullet in neat_bullets[individual]:
                bullet_life[neat_bullets[individual].index(bullet)] += 1
                if bullet_life[neat_bullets[individual].index(bullet)] > 60:
                    bullet_life[neat_bullets[individual].index(bullet)] = 0
                    bullet_life.pop(neat_bullets[individual].index(bullet))
                    neat_bullets[individual].pop(neat_bullets[individual].index(bullet))

        for individual in range(len(neat_man)):
            for asteroid in neat_asteroids[individual]:
                asteroid.update()

        for individual in range(len(neat_man)):
            for asteroid in neat_asteroids[individual]:
                if neat_man[individual].hitbox[1] < asteroid.hitbox[1] + asteroid.hitbox[3] and neat_man[individual].hitbox[1] + neat_man[individual].hitbox[3] > asteroid.hitbox[1]:
                    if neat_man[individual].hitbox[0] + neat_man[individual].hitbox[2] > asteroid.hitbox[0] and neat_man[individual].hitbox[0] < asteroid.hitbox[0] + asteroid.hitbox[2]:
                        if neat_man[individual].dead == False:
                            number_lives[individual] -= 1
                            neat_asteroids[individual].clear()
                            ge[neat_man.index(neat_man[individual])].fitness -= 3

        for individual in range(len(neat_man)):
            for data in asteroid_distances[individual]:
                if data[0] < 100:
                    ge[neat_man.index(neat_man[individual])].fitness -= 0.1
                if data[0] < 75:
                    ge[neat_man.index(neat_man[individual])].fitness -= 0.1
                if data[0] < 50:
                    ge[neat_man.index(neat_man[individual])].fitness -= 0.1

        for individual in range(len(neat_man)):
            no_move_timeout[individual] += 1
            #ge[neat_man.index(neat_man[individual])].fitness -= 1000

        for individual in range(len(neat_man)):
            if number_lives[individual] <= 0 or no_move_timeout[individual] > 2400:
                nets.pop(neat_man.index(neat_man[individual]))
                ge.pop(neat_man.index(neat_man[individual]))
                number_lives.pop(neat_man.index(neat_man[individual]))
                neat_asteroids.pop(neat_man.index(neat_man[individual]))
                neat_bullets.pop(neat_man.index(neat_man[individual]))
                score.pop(neat_man.index(neat_man[individual]))
                no_move_timeout.pop(neat_man.index(neat_man[individual]))
                neat_man.pop(neat_man.index(neat_man[individual]))
                break



        for individual in range(len(neat_man)):
            for bullet in neat_bullets[individual]:
                for asteroid in neat_asteroids[individual]:
                    if bullet.hitbox[1] < asteroid.hitbox[1] + asteroid.hitbox[3] and bullet.hitbox[1] + bullet.hitbox[3] > asteroid.hitbox[1]:
                        if bullet.hitbox[0] + bullet.hitbox[2] > asteroid.hitbox[0] and bullet.hitbox[0] < asteroid.hitbox[0] + asteroid.hitbox[2]:
                            neat_bullets[individual].pop(neat_bullets[individual].index(bullet))
                            if asteroid.size == "large":
                                neat_asteroids[individual].append(a(asteroid.x, asteroid.y, "medium"))
                                neat_asteroids[individual].append(a(asteroid.x, asteroid.y, "medium"))
                            if asteroid.size == "medium":
                                neat_asteroids[individual].append(a(asteroid.x, asteroid.y, "small"))
                                neat_asteroids[individual].append(a(asteroid.x, asteroid.y, "small"))
                            neat_asteroids[individual].pop(neat_asteroids[individual].index(asteroid))
                            score[individual] += 1
                            no_move_timeout[individual] = 0
                            ge[neat_man.index(neat_man[individual])].fitness += 5
                            break

        for individual in range(len(neat_man)):
            total_asteroids = len(neat_asteroids[individual])
            while total_asteroids < 5:
                inside = True
                while inside == True:
                    asteroid_x = randint(0, 700)
                    asteroid_y = randint(100, 500)
                    distance = math.sqrt(((asteroid_x - neat_man[individual].x) ** 2) + ((asteroid_y - neat_man[individual].y) ** 2))
                    if distance > 200:
                        inside = False
                neat_asteroids[individual].append(a(asteroid_x, asteroid_y, "large"))
                total_asteroids = len(neat_asteroids[individual])
            shoot_cool[individual] += 1
            neat_man[individual].update()


        for s in score:
            if s > generatiom_high_score:
                generatiom_high_score = s

        store_high_score[gen_number] = generatiom_high_score

        redrawGameWindow(background, image, score, neat_bullets, neat_asteroids,neat_man, number_lives, generatiom_high_score, gen_number)




def run(config_file):
    """
    runs the NEAT algorithm to train a neural network to play flappy bird.
    :param config_file: location of config file
    :return: None
    """
    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction,
                         neat.DefaultSpeciesSet, neat.DefaultStagnation,
                         config_file)

    # Create the population, which is the top-level object for a NEAT run.
    p = neat.Population(config)

    # Add a stdout reporter to show progress in the terminal.
    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)
    #p.add_reporter(neat.Checkpointer(5))

    # Run for up to 50 generations.
    winner = p.run(eval_genomes, 250)
        #p.run(eval_genomes, 50)
    pygame.quit()
    # show final stats
    print('\nBest genome:\n{!s}'.format(winner))
    global store_high_score
    print(store_high_score)

    x_len = []
    for n in range(len(store_high_score)):
        x_len.append(n)

    plt.plot(x_len, store_high_score)
    plt.xlabel('Generation')
    plt.ylabel('Best Score')
    plt.show()
    #with open("out.csv", "w", newline="") as f:
    #    writer = csv.writer(f)
    #    writer.writerows(store_high_score)


if __name__ == '__main__':
    # Determine path to configuration file. This path manipulation is
    # here so that the script will run successfully regardless of the
    # current working directory.
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, 'config-feedforward.txt')
    run(config_path)
