import pygame
import random

pygame.init()

win_width = 800
win_height = 800

level = 1
facing = "right"
platform_init = random.randint(0, 2)
platform_num = platform_init

x_init = random.randint(40, 730)
platform_x = x_init

win = pygame.display.set_mode((win_width, win_height))
pygame.display.set_caption("Hub world")

clock = pygame.time.Clock()

character_right = pygame.image.load('img/character_right.png')
character_left = pygame.image.load('img/character_left.png')
background = pygame.image.load('img/background.png')
garbage = [pygame.image.load('img/can.png'), pygame.image.load('img/flaming-trash.png'), pygame.image.load('img/apple.png')]
grave = pygame.image.load('img/grave.jpg')


class Player(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.vel = 5
        self.health = 100
        self.alive = True

    def hit(self, damage):
        self.damage = damage
        self.health -= self.damage

    def reset(self):
        self.__init__(win_width/2, win_height - 285)

    def draw(self, win):
        if facing == "right":    
            win.blit(character_right, (self.x, self.y))

        if facing == "left":
            win.blit(character_left, (self.x, self.y))


class Platform(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.vel = 4*level
        self.resetHeight = 1200

    def reset(self):
        self.y = self.resetHeight
    
    def draw(self, win):
        win.blit(garbage[platform_num], (platform_x, self.y))


class Health(object):
    def draw(win):
        # red background
        pygame.draw.rect(win, (255, 0, 0), (win_width-200, 50, 150, 20))

        # green foreground
        pygame.draw.rect(win, (0, 255, 0), (win_width-200, 50, player.health*1.5, 20))


def deathScreen():
    win.blit(grave, (0,0))


def redraw():
    if player.alive == True:
        win.blit(background, (0, 0))
        
        player.draw(win)
        platform.draw(win)
        Health.draw(win)
        
    else:
        deathScreen()

    pygame.display.update()


player = Player(win_width/2, win_height - 285)
platform = Platform(330, 0)

hitCount = 0

run = True
while run:
    clock.tick(60)

    keys = pygame.key.get_pressed()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()

            if pos[0] >= 148 and pos[0] <= 347:
                if pos[1] >= 713 and pos[1] <= 790:
                    player.reset()
                    platform.reset()
            
            elif pos[0] >= 446 and pos[0] <= 750:
                if pos[1] >= 709 and pos[1] <= 787:
                    print("Thank you for playing!")
                    run = False
    

    if keys[pygame.K_a] and player.x > 0:
        facing = "left"
        player.x -= player.vel

    if keys[pygame.K_d] and player.x < win_width - 100:
        facing = "right"
        player.x += player.vel
    
    if platform.y == win_height - 284 or platform.y == platform.resetHeight:
        platform_num = random.randint(0,2)
        platform_x = random.randint(40, 730)
        platform.y = 0
    
    else:
        platform.y += platform.vel
    

    # check for collision with garbage
    if player.y >= platform.y and player.y - 100 <= platform.y:
        if player.x <= platform_x and player.x + 100 >= platform_x:
            platform.reset()

            if player.health <= 20:
                player.alive = False
            
            else:
                player.hit(20)


    redraw()