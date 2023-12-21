import pygame
import time
import random

import button
from button import Button

pygame.font.init()

WIDTH, HEIGHT = 1000, 800
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("SkyDart")

BG = pygame.transform.scale(pygame.image.load("pxl.png"), (WIDTH, HEIGHT))

PLAYER_WIDTH = 30
PLAYER_HEIGHT = 40
PLAYER_VEL = 6
ASTROID_WIDTH = 10
ASTROID_HEIGHT = 20
ASTROID_VEL = 8

FONT = pygame.font.SysFont("TickerBit", 30)

def main_menu():
    while True:
        PLAY_MOUSE_POS = pygame.mouse.get_pos()
        WIN.fill((0, 0, 0))  # Use WIN.fill instead of pygame.display.fill

        OPTIONS_TEXT = FONT.render("This is the OPTIONS screen.", True, (0, 0, 0))
        OPTIONS_RECT = OPTIONS_TEXT.get_rect(center=(640, 260))
        WIN.blit(OPTIONS_TEXT, OPTIONS_RECT)  # Use WIN.blit instead of pygame.display.blit

        OPTIONS_BACK = button.Button(image=None, pos=(640, 460),
                                     text_input="BACK", font=pygame.font.SysFont("TickerBit", 75),
                                     base_color=(0, 0, 0), hovering_color=(0, 255, 0))

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    break

            OPTIONS_BACK.draw(WIN)  # Assuming your Button class has a draw method

            pygame.display.flip()

    pygame.display.update()

def draw(player, elapsed_time, astroids):
    WIN.blit(BG, (0, 0))

    time_text = FONT.render(f"Time: {round(elapsed_time)}s", 1, "white")
    WIN.blit(time_text, (10, 10))

    pygame.draw.rect(WIN, "blue", player)

    for astroid in astroids:
        pygame.draw.rect(WIN, "white", astroid)

    pygame.display.update()


def main():
    run = True

    player = pygame.Rect(500, HEIGHT - PLAYER_HEIGHT, PLAYER_WIDTH, PLAYER_HEIGHT)

    clock = pygame.time.Clock()
    start_time = time.time()
    elapsed_time = 0

    astroid_add_increment = 2000
    astroid_count = 0

    astroids = []
    hit = False

    while run:
        astroid_count += clock.tick(70)
        elapsed_time = time.time() - start_time

        if astroid_count > astroid_add_increment:
            for _ in range(5):
                astroid_x = random.randint(0, WIDTH - ASTROID_WIDTH)
                astroid = pygame.Rect(astroid_x, -ASTROID_HEIGHT, ASTROID_WIDTH, ASTROID_HEIGHT)
                astroids.append(astroid)

            astroid_add_increment = max(200, astroid_add_increment - 50)
            astroid_count = 0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break

        keys = pygame.key.get_pressed()
        if keys[pygame.K_a] and player.x - PLAYER_VEL >= 0:
            player.x -= PLAYER_VEL
        if keys[pygame.K_d] and player.x + PLAYER_VEL + player.width <= WIDTH:
            player.x += PLAYER_VEL
        if keys[pygame.K_w] and player.y - PLAYER_VEL >= 0:
            player.y -= PLAYER_VEL
        if keys[pygame.K_s] and player.y + PLAYER_VEL + player.height <= HEIGHT:
            player.y += PLAYER_VEL

        for astroid in astroids[:]:
            astroid.y += ASTROID_VEL
            if astroid.y > HEIGHT:
                astroids.remove(astroid)
            elif astroid.y + astroid.height >= player.y and astroid.colliderect(player):
                astroids.remove(astroid)
                hit = True
                break


        if hit:
            lost_text = FONT.render("YOU LOST!", 1, "white")
            WIN.blit(lost_text, (WIDTH/2 - lost_text.get_width()/2, HEIGHT/2 - lost_text.get_height()/2))
            pygame.display.update()
            pygame.time.delay(3000)
            return True

        draw(player, elapsed_time, astroids)

    pygame.quit()

if __name__ == "__main__":
    while main():
        pass
    pygame.quit()
