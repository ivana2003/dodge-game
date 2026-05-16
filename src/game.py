import pygame
pygame.init()
screen = pygame.display.set_mode((800,600))

running = True

player_x = 100
player_y = 100
player_size = 50
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    screen.fill((0,0,0))
    pygame.draw.rect(screen, (255,255,255), (player_x,player_y,player_size,player_size))
    pygame.display.update()
pygame.quit()

        
        


        









