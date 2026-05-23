import pygame

import dodge
import snake

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600


def disegna_menu(screen, font_title, font, font_hint):
    screen.fill((15, 15, 35))
    titolo = font_title.render("MINI GIOCHI", True, (255, 240, 120))
    screen.blit(titolo, ((SCREEN_WIDTH - titolo.get_width()) // 2, 80))

    sub = font_hint.render("scegli un gioco", True, (180, 180, 200))
    screen.blit(sub, ((SCREEN_WIDTH - sub.get_width()) // 2, 170))

    op1 = font.render("1  —  DODGE  (rivalsa matematica)", True, (255, 255, 255))
    screen.blit(op1, ((SCREEN_WIDTH - op1.get_width()) // 2, 270))

    op2 = font.render("2  —  SNAKE  (sfide Wordle)", True, (255, 255, 255))
    screen.blit(op2, ((SCREEN_WIDTH - op2.get_width()) // 2, 340))

    hint = font_hint.render("premi 1 o 2 per giocare,  Q per uscire", True, (180, 180, 180))
    screen.blit(hint, ((SCREEN_WIDTH - hint.get_width()) // 2, 490))


def menu():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Mini Giochi - Menu")
    clock = pygame.time.Clock()
    font_title = pygame.font.SysFont(None, 90)
    font = pygame.font.SysFont(None, 44)
    font_hint = pygame.font.SysFont(None, 30)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    risultato = dodge.run_dodge()
                    if risultato == "quit":
                        pygame.quit()
                        return
                    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
                    pygame.display.set_caption("Mini Giochi - Menu")
                elif event.key == pygame.K_2:
                    risultato = snake.run_snake()
                    if risultato == "quit":
                        pygame.quit()
                        return
                    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
                    pygame.display.set_caption("Mini Giochi - Menu")
                elif event.key == pygame.K_q:
                    pygame.quit()
                    return

        disegna_menu(screen, font_title, font, font_hint)
        pygame.display.update()
        clock.tick(60)


if __name__ == "__main__":
    menu()
