import pygame
import random

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600



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


SIMBOLI = {
    "RIVALSA_ADD": "+",
    "RIVALSA_MULT": "x",
    "RIVALSA_DIV": "/",
}

TEMPI_RIVALSA = {
    "RIVALSA_ADD": 600,
    "RIVALSA_MULT": 500,
    "RIVALSA_DIV": 300,
}


def genera_problema(tipo):
    if tipo == "RIVALSA_ADD":
        a = random.randint(1, 100)
        b = random.randint(1, 100)
        return a, b, a + b
    if tipo == "RIVALSA_MULT":
        a = random.randint(2, 15)
        b = random.randint(2, 15)
        return a, b, a * b
    if tipo == "RIVALSA_DIV":
        b = random.randint(2, 20)
        risultato = random.randint(2, 20)
        a = b * risultato
        return a, b, risultato


def run_dodge():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
    pygame.display.set_caption("Dodge")
    player = Player(100,100,50,5)
    enemies = []
    spawn_timer = 0
    clock = pygame.time.Clock()
    font = pygame.font.SysFont(None, 36)
    score = 0
    problem_a = 0
    problem_b = 0
    correct_answer = 0
    user_input = ""
    problems_done = 0
    rivalsa_timer = 0
    font_big = pygame.font.SysFont(None, 80)
    state = "PLAYING"

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"
            if event.type == pygame.KEYDOWN:
                if state == "GAME_OVER":
                    if event.key == pygame.K_r:
                        state = "PLAYING"
                        score = 0
                        enemies = []
                        player = Player(100,100,50,5)
                    elif event.key == pygame.K_m:
                        return "menu"
                    elif event.key == pygame.K_q:
                        return "quit"
                if state in ("RIVALSA_ADD", "RIVALSA_MULT", "RIVALSA_DIV"):
                    if event.unicode.isdigit() and len(user_input) < 6:
                        user_input += event.unicode
                    elif event.key == pygame.K_BACKSPACE:
                        user_input = user_input[:-1]
                    elif event.key == pygame.K_RETURN and user_input != "":
                        if int(user_input) == correct_answer:
                            problems_done += 1
                            user_input = ""
                            if problems_done < 2:
                                problem_a, problem_b, correct_answer = genera_problema(state)
                                rivalsa_timer = TEMPI_RIVALSA[state]
                            else:
                                problems_done = 0
                                if state == "RIVALSA_ADD":
                                    state = "RIVALSA_MULT"
                                elif state == "RIVALSA_MULT":
                                    state = "RIVALSA_DIV"
                                else:
                                    state = "PLAYING"
                                    enemies = []
                                if state in TEMPI_RIVALSA:
                                    problem_a, problem_b, correct_answer = genera_problema(state)
                                    rivalsa_timer = TEMPI_RIVALSA[state]
                        else:
                            state = "GAME_OVER"
                            user_input = ""
        screen.fill((0,0,0))
        if state == "PLAYING":
            score +=1
            player.move()
            spawn_timer +=1
            if spawn_timer>=20:
                x_random = random.randint(0, SCREEN_WIDTH-50)
                speed_random = random.randint(2,6)
                enemies.append(Enemy(x_random, 0, 50, speed_random))
                spawn_timer = 0
            enemies = [e for e in enemies if e.y <SCREEN_HEIGHT]
            for e in enemies:
                e.move()
                e.draw(screen)
                if player.collides_with(e):
                    state = "RIVALSA_ADD"
                    problems_done = 0
                    user_input = ""
                    problem_a, problem_b, correct_answer = genera_problema(state)
                    rivalsa_timer = TEMPI_RIVALSA[state]
            player.draw(screen)
            testo_surface = font.render(f"Score : {score}", True, (255,255,255))
            screen.blit(testo_surface, (10,10))
        elif state == "GAME_OVER":
            go_surf = font_big.render("GAME OVER", True, (255,0,0))
            go_x = (SCREEN_WIDTH - go_surf.get_width()) // 2
            go_y = (SCREEN_HEIGHT - go_surf.get_height()) // 2 - 30
            screen.blit(go_surf, (go_x, go_y))
            score_surf = font.render(f"Score finale: {score}", True, (255, 255, 255))
            score_x = (SCREEN_WIDTH - score_surf.get_width()) // 2
            score_y = go_y + 100
            screen.blit(score_surf, (score_x, score_y))
            hint_surf = font.render("R = ricomincia   M = menu   Q = esci", True, (200, 200, 200))
            hint_x = (SCREEN_WIDTH - hint_surf.get_width()) // 2
            screen.blit(hint_surf, (hint_x, score_y + 60))
        elif state in ("RIVALSA_ADD", "RIVALSA_MULT", "RIVALSA_DIV"):
            rivalsa_timer -= 1
            if rivalsa_timer <= 0:
                state = "GAME_OVER"
                user_input = ""
            else:
                simbolo = SIMBOLI[state]
                titolo = font.render(f"RIVALSA — problema {problems_done + 1}/2", True, (255,255,0))
                screen.blit(titolo, (220, 120))
                testo = font_big.render(f"{problem_a} {simbolo} {problem_b} = ?", True, (255,255,0))
                screen.blit(testo, (150, 230))
                risposta_surf = font_big.render(user_input, True, (255,255,255))
                screen.blit(risposta_surf, (350, 340))
                secondi = rivalsa_timer // 60 + 1
                timer_surf = font.render(f"Tempo: {secondi}s", True, (255,100,100))
                screen.blit(timer_surf, (SCREEN_WIDTH - 200, 10))
        pygame.display.update()
        clock.tick(60)



if __name__ == "__main__":
    run_dodge()
