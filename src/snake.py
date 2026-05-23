import pygame
import random

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
CELL = 40
COLS = SCREEN_WIDTH // CELL
ROWS = SCREEN_HEIGHT // CELL

MOVE_DELAY = 8
MELE_PER_WORDLE = 3

PAROLE_WORDLE = [
    "GATTO", "TIGRE", "LIBRO", "CARTA", "ROSSO",
    "VERDE", "PIZZA", "PASTA", "SOGNO", "MANIA",
    "PIANO", "FUOCO", "ACQUA", "LUNGO", "CORTO",
    "BASSO", "SEDIA", "VENTO", "NUOVO", "AMORE",
    "DOLCE", "AMARO", "POSTO", "TEMPO", "DANZA",
    "CANTO", "SUONO", "VISTA", "TUONO", "FIUME",
    "MONTE", "VALLE", "BOSCO", "FUNGO", "FIORE",
    "PRATO", "SASSO", "PARTE", "CAMPO", "VIALE",
    "PAESE", "MONDO", "TERRA", "CIELO",
]


class Snake:
    def __init__(self):
        cx, cy = COLS // 2, ROWS // 2
        self.body = [(cx, cy), (cx - 1, cy), (cx - 2, cy)]
        self.direction = (1, 0)
        self.crescita_pendente = 0

    def cambia_direzione(self, nuova):
        dx, dy = self.direction
        nx, ny = nuova
        if dx + nx == 0 and dy + ny == 0:
            return
        self.direction = nuova

    def muovi(self):
        head_x, head_y = self.body[0]
        dx, dy = self.direction
        nuova_testa = (head_x + dx, head_y + dy)
        self.body.insert(0, nuova_testa)
        if self.crescita_pendente > 0:
            self.crescita_pendente -= 1
        else:
            self.body.pop()

    def collide_muro(self):
        x, y = self.body[0]
        return x < 0 or x >= COLS or y < 0 or y >= ROWS

    def collide_se_stesso(self):
        return self.body[0] in self.body[1:]

    def disegna(self, screen):
        for i, (x, y) in enumerate(self.body):
            colore = (0, 255, 0) if i == 0 else (0, 180, 0)
            pygame.draw.rect(screen, colore, (x * CELL + 1, y * CELL + 1, CELL - 2, CELL - 2))


def genera_cibo(snake_body):
    while True:
        c = (random.randint(0, COLS - 1), random.randint(0, ROWS - 1))
        if c not in snake_body:
            return c


def colora_tentativo(tentativo, parola):
    colori = []
    for i, lettera in enumerate(tentativo):
        if lettera == parola[i]:
            colori.append((90, 170, 90))
        elif lettera in parola:
            colori.append((200, 170, 70))
        else:
            colori.append((70, 70, 70))
    return colori


def disegna_wordle(screen, font, font_wordle, parola, tentativi, tentativo_corrente):
    titolo = font.render("WORDLE — indovina per continuare", True, (255, 255, 100))
    screen.blit(titolo, ((SCREEN_WIDTH - titolo.get_width()) // 2, 25))

    cella_w = 60
    riga_h = 70
    gap = 6
    griglia_w = 5 * cella_w + 4 * gap
    start_x = (SCREEN_WIDTH - griglia_w) // 2
    start_y = 80

    for r in range(6):
        for c in range(5):
            x = start_x + c * (cella_w + gap)
            y = start_y + r * (riga_h + gap)
            lettera = ""
            colore_bg = (40, 40, 40)
            if r < len(tentativi):
                lettera = tentativi[r][c]
                colori = colora_tentativo(tentativi[r], parola)
                colore_bg = colori[c]
            elif r == len(tentativi) and c < len(tentativo_corrente):
                lettera = tentativo_corrente[c]
                colore_bg = (60, 60, 60)
            pygame.draw.rect(screen, colore_bg, (x, y, cella_w, riga_h))
            pygame.draw.rect(screen, (120, 120, 120), (x, y, cella_w, riga_h), 2)
            if lettera:
                txt = font_wordle.render(lettera, True, (255, 255, 255))
                tx = x + (cella_w - txt.get_width()) // 2
                ty = y + (riga_h - txt.get_height()) // 2
                screen.blit(txt, (tx, ty))


def run_snake():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Snake")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont(None, 36)
    font_big = pygame.font.SysFont(None, 70)
    font_wordle = pygame.font.SysFont(None, 50)

    snake = Snake()
    cibo = genera_cibo(snake.body)
    score = 0
    mele_mangiate = 0
    move_timer = 0

    parola = ""
    tentativi = []
    tentativo_corrente = ""

    state = "PLAYING"

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"
            if event.type == pygame.KEYDOWN:
                if state == "PLAYING":
                    if event.key == pygame.K_UP:
                        snake.cambia_direzione((0, -1))
                    elif event.key == pygame.K_DOWN:
                        snake.cambia_direzione((0, 1))
                    elif event.key == pygame.K_LEFT:
                        snake.cambia_direzione((-1, 0))
                    elif event.key == pygame.K_RIGHT:
                        snake.cambia_direzione((1, 0))
                elif state == "WORDLE":
                    if event.key == pygame.K_BACKSPACE:
                        tentativo_corrente = tentativo_corrente[:-1]
                    elif event.key == pygame.K_RETURN and len(tentativo_corrente) == 5:
                        tentativi.append(tentativo_corrente)
                        if tentativo_corrente == parola:
                            state = "PLAYING"
                            tentativi = []
                            tentativo_corrente = ""
                        elif len(tentativi) >= 6:
                            state = "GAME_OVER"
                        else:
                            tentativo_corrente = ""
                    else:
                        ch = event.unicode.upper()
                        if "A" <= ch <= "Z" and len(tentativo_corrente) < 5:
                            tentativo_corrente += ch
                elif state == "GAME_OVER":
                    if event.key == pygame.K_r:
                        snake = Snake()
                        cibo = genera_cibo(snake.body)
                        score = 0
                        mele_mangiate = 0
                        move_timer = 0
                        tentativi = []
                        tentativo_corrente = ""
                        state = "PLAYING"
                    elif event.key == pygame.K_m:
                        return "menu"
                    elif event.key == pygame.K_q:
                        return "quit"

        screen.fill((20, 20, 20))

        if state == "PLAYING":
            move_timer += 1
            if move_timer >= MOVE_DELAY:
                snake.muovi()
                move_timer = 0
                if snake.collide_muro() or snake.collide_se_stesso():
                    state = "GAME_OVER"
                elif snake.body[0] == cibo:
                    score += 10
                    mele_mangiate += 1
                    snake.crescita_pendente += 1
                    cibo = genera_cibo(snake.body)
                    if mele_mangiate % MELE_PER_WORDLE == 0:
                        parola = random.choice(PAROLE_WORDLE)
                        tentativi = []
                        tentativo_corrente = ""
                        state = "WORDLE"

            cx, cy = cibo
            pygame.draw.rect(screen, (255, 60, 60), (cx * CELL + 4, cy * CELL + 4, CELL - 8, CELL - 8))
            snake.disegna(screen)
            score_surf = font.render(f"Score: {score}", True, (255, 255, 255))
            screen.blit(score_surf, (10, 10))
            mele_surf = font.render(f"Mele: {mele_mangiate}", True, (255, 255, 255))
            screen.blit(mele_surf, (SCREEN_WIDTH - 150, 10))

        elif state == "WORDLE":
            disegna_wordle(screen, font, font_wordle, parola, tentativi, tentativo_corrente)

        elif state == "GAME_OVER":
            go_surf = font_big.render("GAME OVER", True, (255, 80, 80))
            go_x = (SCREEN_WIDTH - go_surf.get_width()) // 2
            go_y = (SCREEN_HEIGHT - go_surf.get_height()) // 2 - 60
            screen.blit(go_surf, (go_x, go_y))
            sc_surf = font.render(f"Score finale: {score}", True, (255, 255, 255))
            sc_x = (SCREEN_WIDTH - sc_surf.get_width()) // 2
            screen.blit(sc_surf, (sc_x, go_y + 80))
            hint = font.render("R = ricomincia   M = menu   Q = esci", True, (200, 200, 200))
            hint_x = (SCREEN_WIDTH - hint.get_width()) // 2
            screen.blit(hint, (hint_x, go_y + 140))

        pygame.display.update()
        clock.tick(60)


if __name__ == "__main__":
    run_snake()
