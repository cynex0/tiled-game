import pygame
from constants import *


class Enemy:
    def __init__(self, level, x, y):
        self.level = level
        self.direction = "right"
        self.falling = False
        self.dead = False

        idle_img = pygame.image.load('sprites/ene/idle.png')
        self.idle_frames = {"right": idle_img,
                            "left": pygame.transform.flip(idle_img, True, False)}

        self.width = self.idle_frames["right"].get_width()
        self.half_width = round(self.width / 2)
        self.height = self.idle_frames["right"].get_height()
        self.half_height = round(self.height / 2)

        self.x = x  # середина
        self.y = y  # низ
        self.dx = -1
        self.accel_x = 4.2
        self.accel_y = 4

        self.run_cycle = {"right": [], "left": []}  # len = 4
        self.fall_img = pygame.image.load('sprites/ene/fall.png')
        self.anim_start = millis()
        self.anim_tick = 100

        for i in range(4):
            run_img = pygame.image.load('sprites/ene/run/frame' + str(i) + '.png')
            self.run_cycle["right"].append(run_img)
            self.run_cycle["left"].append(pygame.transform.flip(run_img, True, False))

    def move(self):
        if self.level.isSolid(self.x, self.y):
            # if self.x - self.half_width < 0:
            #     self.x = self.half_width
            #     self.dx = 1
            #
            # if self.x + self.half_width > WIDTH:
            #     self.x = WIDTH - self.half_width
            #     self.dx = -1

            if self.level.isSolid(self.x + self.half_width, self.y - self.half_height, True):
                # print("Collision right")
                self.x = (self.x // TILE_SIZE) * TILE_SIZE + TILE_SIZE - self.half_width
                self.dx = -1

            if self.level.isSolid(self.x - self.half_width, self.y - self.half_height, True):
                # print("Collision left")
                self.x = (self.x // TILE_SIZE) * TILE_SIZE + self.half_width
                self.dx = 1

            if self.dx < 0:
                self.direction = "left"

            elif self.dx > 0:
                self.direction = "right"

            self.x += self.dx * self.accel_x
        else:
            self.falling = True
            self.y += self.accel_y
            if self.y >= HEIGHT:
                self.dead = True

    def draw(self, screen):
        img = self.run_cycle[self.direction][
            ((millis() - self.anim_start) // self.anim_tick) % len(self.run_cycle[self.direction])
            ]

        left_upper_x = self.x - self.half_width
        left_upper_y = self.y - self.height
        screen.blit(img, (left_upper_x, left_upper_y))

    def collideWithPlayer(self, player):
        # if player.x in range(self.x - self.half_width, self.x + self.half_width + 1):
        #     if player.y in range(self.y, self.y - self.height):
        #         return True
        player_rect = pygame.Rect((player.x - player.half_width, player.y - player.height),
                                  (player.width, player.height))
        mob_rect = pygame.Rect((self.x - self.half_width, self.y - self.height),
                               (self.width, self.height))
        return mob_rect.colliderect(player_rect)
