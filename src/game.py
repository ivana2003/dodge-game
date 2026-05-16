import pygame
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))

class Player:
    def __init__(self, x:int, y:int, size:int, speed : int):
        self.x = x
        self.y = y
        self.size = size
        self.speed = speed
    
    def draw(self, screen):
        pygame.draw.rect(screen, (255,255,255), (self.x, self.y, self.size, self.size))
        
    def move(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] == True:
            self.x -= self.speed
        if keys[pygame.K_RIGHT] == True:
            self.x += self.speed
        if keys[pygame.K_UP] == True:
            self.y -= self.speed
        if keys[pygame.K_DOWN] == True:
            self.y += self.speed
        if self.x<0:
            self.x = 0
        if self.x> SCREEN_WIDTH - self.size:
            self.x = SCREEN_WIDTH - self.size
        if self.y<0:
            self.y = 0
        if self.y> SCREEN_HEIGHT - self.size:
            self.y = SCREEN_HEIGHT - self.size
        




class Enemy:
    def __init__(self, x:int, y: int,size : int, speed: int):
        self.x = x
        self.y = y
        self.size = size
        self.speed = speed
    
    def draw(self, screen):
        pygame.draw.rect(screen, (255,0,0), (self.x, self.y, self.size, self.size))
        
    def move(self):
        self.y += self.speed
    
    




running = True
player = Player(100,100,50,5)
enemy = Enemy(400,0,50,3)
clock = pygame.time.Clock()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    screen.fill((0,0,0))
    player.move()
    enemy.move()
    enemy.draw(screen)
    player.draw(screen)
    pygame.display.update()
    clock.tick(60)
pygame.quit()

        
        


        









