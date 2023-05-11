import random

import pygame


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.jump_sound = pygame.mixer.Sound("../Audio/jump.mp3")
        self.jump_sound.set_volume(0.07)
        player_walk_1 = pygame.image.load("../Graphic/Player/player_walk_1.png").convert_alpha()
        player_walk_2 = pygame.image.load("../Graphic/Player/player_walk_2.png").convert_alpha()
        self.player_walk = [player_walk_1, player_walk_2]
        self.player_jump = pygame.image.load("../Graphic/Player/jump.png").convert_alpha()
        self.index = 0
        self.surf = self.player_walk[0]
        self.rect = self.surf.get_rect(midbottom=(80, 300))
        self.gravity = 0
        self.health_counter = 0
        self.player_health = 3

    def player_animation(self):
        if self.rect.bottom < 300:
            self.surf = self.player_jump
        else:
            self.index += 0.1
            if self.index >= len(self.player_walk):
                self.index = 0
            self.surf = self.player_walk[int(self.index)]

    def player_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and self.rect.bottom >= 300:
            self.gravity = -22
            self.jump_sound.play()
        if keys[pygame.K_DOWN]:
            self.gravity = 30
    def apply_gravity(self):
        self.gravity += 1
        self.rect.y += self.gravity
        if self.rect.bottom >= 300:
            self.rect.bottom = 300

    def update(self):
        self.player_input()
        self.apply_gravity()
        self.player_animation()


class Fly(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        fly_1 = pygame.image.load('../Graphic/Fly/Fly1.png').convert_alpha()
        fly_2 = pygame.image.load('../Graphic/Fly/Fly2.png').convert_alpha()
        self.assets = [fly_1, fly_2]
        self.index = 0
        self.surf = self.assets[0]
        self.rect = self.surf.get_rect(center=(2000, 190))
        self.speed = -9
        self.score = 0

    def update(self):
        self.animation()
        self.rect.x += self.speed

        if self.rect.right < -100:
            self.random()
            self.score += 1

    def animation(self):
        self.index += 0.1
        if self.index >= len(self.assets):
            self.index = 0
        self.surf = self.assets[int(self.index)]

    def random(self):
        x = random.randint(1300, 1800)
        self.rect.midleft = (x, 190)


class Snail(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        snail_1 = pygame.image.load('../Graphic/snail/snail1.png').convert_alpha()
        snail_2 = pygame.image.load('../Graphic/snail/snail2.png').convert_alpha()
        self.assets = [snail_1, snail_2]
        self.index = 0
        self.surf = self.assets[0]
        self.rect = self.surf.get_rect(center=(800, 285))
        self.speed = -5
        self.score = 0

    def update(self):
        self.animation()
        self.rect.x += self.speed

        if self.rect.right < -100:
            self.random()
            self.score += 1

    def animation(self):
        self.index += 0.1
        if self.index >= len(self.assets):
            self.index = 0
        self.surf = self.assets[int(self.index)]

    def random(self):
        x = random.randint(800, 1200)
        self.rect.midleft = (x, 285)