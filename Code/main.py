import json
import sys

import pygame
import pygame_gui

from Button import Button
from characters import Player, Fly, Snail

with open("high_scores.json") as f:
    high_scores = json.load(f)
pygame.init()

WIDTH = 800
HEIGHT = 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Pixel Runner')
pygame.display.set_icon(pygame.image.load('../Graphic/Player/jump.png'))
clock = pygame.time.Clock()
FONT = pygame.font.Font("../Font/Pixeltype.ttf", 75)
score = 0
background_music = pygame.mixer.Sound("../Audio/music.wav")
background_music.set_volume(0.025)

MANAGER = pygame_gui.UIManager((WIDTH, HEIGHT))
text_input = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect((25, 325), (350, 50)), manager=MANAGER,
                                                 object_id='#high_score_text')


def draw_text_with_rect(screen, text, rect_color, text_color, font, rect_pos):
    text_surface = font.render(text, True, text_color)
    text_rect = text_surface.get_rect(center=rect_pos)

    rect_width = text_rect.width + 20
    rect_height = text_rect.height + 20
    rect_pos = (rect_pos[0] - rect_width / 2, rect_pos[1] - rect_height / 2)
    rect = pygame.Rect(rect_pos, (rect_width, rect_height))

    pygame.draw.rect(screen, rect_color, rect)
    screen.blit(text_surface, text_rect)


def play():
    global score
    player = Player()
    fly = Fly()
    snail = Snail()
    enemies = pygame.sprite.Group()
    enemies.add(snail)
    enemies.add(fly)
    player_group = pygame.sprite.GroupSingle()
    player_group.add(player)
    scroll_speed = 4
    background = pygame.image.load('../Graphic/SKY.png')
    ground = pygame.image.load('../Graphic/ground.png')

    game_active = True
    background_pos = 0
    while True:
        if game_active:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            background_music.play(-1)
            background_pos -= scroll_speed
            if background_pos <= -WIDTH:
                background_pos = 0
            screen.blit(background, (background_pos, 0))
            screen.blit(background, (background_pos + WIDTH, 0))
            screen.blit(ground, (0, 300))

            screen.blit(player.surf, player.rect)
            player.update()

            screen.blit(fly.surf, fly.rect)
            screen.blit(snail.surf, snail.rect)
            fly.update()
            snail.update()
            score = snail.score + fly.score
            draw_text_with_rect(screen, f'Score : {score}', '#D0F4F7', '#8CB3B7', FONT, (400, 40))

            for enemy in enemies:
                if pygame.math.Vector2(player.rect.center).distance_to(enemy.rect.center) < 50:
                    game_active = False
                    if isinstance(enemy, Snail):
                        snail.random()
                    elif isinstance(enemy, Fly):
                        fly.random()

            pygame.display.update()
            clock.tick(60)
        else:
            score_screen()


def main_menu():
    play_button = Button((600, 100), 'PLAY', FONT, "#d7fcd4", "White", [200, 100], '#5F80A1')
    quit_button = Button((600, 300), 'QUIT', FONT, "#d7fcd4", "White", [200, 100], '#5F80A1')
    high_score_button = Button((600, 200), 'HIGH SCORES', FONT, "#d7fcd4", "White", [200, 100], '#5F80A1')
    player_image = pygame.image.load('../Graphic/Player/player_stand.png')
    player_image = pygame.transform.scale(player_image, (68 * 2.5, 84 * 2.5))
    player_rect = player_image.get_rect(center=(200, 200))
    pygame.mixer.music.stop()
    while True:
        screen.fill('#5F80A1')
        menu_pos = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if play_button.checkForInput(menu_pos):
                    play()
                if high_score_button.checkForInput(menu_pos):
                    high_score_menu()
                if quit_button.checkForInput(menu_pos):
                    pygame.quit()
                    sys.exit()
        for button in [play_button, quit_button, high_score_button]:
            button.changeColor(menu_pos)
            button.update(screen)
        screen.blit(player_image, player_rect)
        pygame.display.update()
        clock.tick(60)


def score_screen():
    player_image = pygame.image.load('../Graphic/Player/player_stand.png')
    player_image = pygame.transform.scale(player_image, (68 * 2, 84 * 2))
    player_rect = player_image.get_rect(center=(200, 150))
    main_menu_button = Button((600, 200), 'MAIN MENU', FONT, "#d7fcd4", "White", [200, 100], '#5F80A1')
    while True:
        menu_pos = pygame.mouse.get_pos()
        screen.fill('#5F80A1')
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame_gui.UI_TEXT_ENTRY_FINISHED and event.ui_object_id == '#high_score_text':
                add_high_score(event.text, score)
                high_score_menu()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if main_menu_button.checkForInput(menu_pos):
                    background_music.stop()
                    main_menu()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    play()
            MANAGER.process_events(event)
        MANAGER.update(clock.tick(60) / 300)
        MANAGER.draw_ui(screen)
        for button in [main_menu_button]:
            button.changeColor(menu_pos)
            button.update(screen)
        screen.blit(player_image, player_rect)
        score_text = FONT.render("Score: " + str(score), True, '#6DC1A6')
        score_rect = score_text.get_rect(center=(200, 300))
        screen.blit(score_text, score_rect)
        pygame.display.update()
        clock.tick(60)


def high_score_menu():
    main_menu_button = Button((600, 200), 'MAIN MENU', FONT, "#d7fcd4", "White", [200, 100], '#5F80A1')
    while True:
        menu_pos = pygame.mouse.get_pos()
        screen.fill('#5F80A1')
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if main_menu_button.checkForInput(menu_pos):
                    background_music.stop()
                    main_menu()

        for button in [main_menu_button]:
            button.changeColor(menu_pos)
            button.update(screen)
        y = 50
        for i, high_score in enumerate(high_scores):
            text = f"{i + 1}. {high_score['name']} - {high_score['score']}"
            draw_text_with_rect(screen, text, '#5F80A1', '#d7fcd4', FONT, (200, y))
            y += 75
        pygame.display.update()
        clock.tick(60)


def add_high_score(name, score):
    global high_scores
    high_scores.append({"name": name, "score": score})
    high_scores = sorted(high_scores, key=lambda x: x["score"], reverse=True)[:5]
    with open('high_scores.json', 'w') as f:
        json.dump(high_scores, f)


main_menu()
