import pygame
import random

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
            
    def collides_with(self, other):
        return (self.x < other.x + other.size and
        self.x + self.size > other.x and
        self.y < other.y + other.size and
        self.y + self.size > other.y)

        




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
enemies = []
spawn_timer = 0
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 36)
score = 0
font_big = pygame.font.SysFont(None, 80)
game_over = False

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    screen.fill((0,0,0))
    if not game_over:
        score +=1
        player.move()
        spawn_timer +=1
        if spawn_timer>=120:
            x_random = random.randint(0, SCREEN_WIDTH-50)
            speed_random = random.randint(2,6)
            enemies.append(Enemy(x_random, 0, 50, speed_random))
            spawn_timer = 0
        enemies = [e for e in enemies if e.y <SCREEN_HEIGHT]
        for e in enemies:
            e.move()
            e.draw(screen)
            if player.collides_with(e):
                game_over = True
        player.draw(screen)
        testo_surface = font.render(f"Score : {score}", True, (255,255,255))
        screen.blit(testo_surface, (10,10))
    else:
        go_surf = font_big.render("GAME OVER", True, (255,0,0))
        go_x = (SCREEN_WIDTH - go_surf.get_width()) // 2
        go_y = (SCREEN_HEIGHT - go_surf.get_height()) // 2 - 30
        screen.blit(go_surf, (go_x, go_y))
        score_surf = font.render(f"Score finale: {score}", True, (255, 255, 255))
        score_x = (SCREEN_WIDTH - score_surf.get_width()) // 2
        score_y = go_y + 100
        screen.blit(score_surf, (score_x, score_y))
    pygame.display.update()
    clock.tick(60)
pygame.quit()

        
        


        









