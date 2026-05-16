import pygame
pygame.init()
screen = pygame.display.set_mode((800,600))

class Player:
    def __init__(self, x:int, y:int, size:int):
        self.x = x
        self.y = y
        self.size = size
        



running = True
player = Player(100,100,50)
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    screen.fill((0,0,0))
    pygame.draw.rect(screen, (255,255,255), (player.x,player.y,player.size,player.size))
    pygame.display.update()
pygame.quit()

        
        


        









