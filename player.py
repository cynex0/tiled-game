import pygame
from constants import *


class Player:
    def __init__(self, level):
        self.level = level
        self.direction = "right"
        self.idling = True
        self.running = False
        self.jumping = False

        idle_img = pygame.transform.scale2x(pygame.image.load('sprites/player/idle.png'))
        self.idle_frames = {"right": idle_img,
                            "left": pygame.transform.flip(idle_img, True, False)}

        self.width = self.idle_frames["right"].get_width()
        self.half_width = round(self.width / 2)
        self.height = self.idle_frames["right"].get_height()
        self.half_height = round(self.height / 2)
        self.screen_width = TILE_SIZE * TILES_X
        self.screen_height = TILE_SIZE * TILES_Y

        self.x = TILE_SIZE / 2  # середина
        self.floor = HEIGHT - self.level.getGroundTile(self.x) * TILE_SIZE
        self.y = self.floor  # низ
        self.accel_x = 3.4
        self.accel_y = 0.7
        self.speed_y = 0
        self.lifes = MAX_LIFES

        self.run_cycle = {"right": [], "left": []}   # len = 4
        self.jump_cycle = {"right": [], "left": []}  # len = 4
        self.anim_start = millis()
        self.anim_tick = 100

        for i in range(4):
            run_img = pygame.image.load('sprites/player/run/frame' + str(i) + '.png')
            run_img = pygame.transform.scale2x(run_img)
            self.run_cycle["right"].append(run_img)
            self.run_cycle["left"].append(pygame.transform.flip(run_img, True, False))

            jump_img = pygame.image.load('sprites/player/jump/frame' + str(i) + '.png')
            jump_img = pygame.transform.scale2x(jump_img)
            self.jump_cycle["right"].append(jump_img)
            self.jump_cycle["left"].append(pygame.transform.flip(jump_img, True, False))

    def reset(self):
        self.direction = "right"
        self.idling = True
        self.running = False
        self.jumping = False
        self.x = TILE_SIZE / 2
        self.y = self.floor

    def draw(self, screen):
        if self.idling:
            img = self.idle_frames[self.direction]
        elif self.running:
            img = self.run_cycle[self.direction][
                ((millis() - self.anim_start) // self.anim_tick) % len(self.run_cycle[self.direction])
                ]
        elif self.jumping:
            if self.speed_y > 0:
                img = self.jump_cycle[self.direction][2]
            else:
                img = self.jump_cycle[self.direction][1]

        left_upper_x = self.x - self.half_width
        left_upper_y = self.y - self.height
        screen.blit(img, (left_upper_x, left_upper_y))

    def completed(self):
        player_rect = pygame.Rect((self.x - self.half_width, self.y - self.height),
                                  (self.width, self.height))
        return player_rect.colliderect(self.level.door_rect)

    def move(self, dx):
        self.x += dx * self.accel_x
        currtile_x = self.x // TILE_SIZE
        currtile_y = self.y // TILE_SIZE

        if dx < 0:
            self.direction = "left"
            if not self.jumping:
                self.setState("running")

        if dx > 0:
            self.direction = "right"
            if not self.jumping:
                self.setState("running")

        if dx == 0:
            if not self.jumping:
                self.setState("idling")

        if self.jumping:
            self.speed_y += self.accel_y
            self.y += self.speed_y

        if self.y >= HEIGHT:
            self.reset()
            self.takeDmg()

        if self.speed_y > 20:
            self.speed_y = 20

        if self.level.isSolid(self.x, self.y):  # if ground directly below player
            if self.jumping:
                self.setState('idling')
                self.speed_y = 0
        else:
            self.setState('jumping')

        if self.level.isSolid(self.x, self.y - self.height):
            if self.jumping:
                self.speed_y = 0

        if self.x - self.half_width < 0:
            self.x = self.half_width

        if self.x + self.half_width > self.screen_width:
            self.x = self.screen_width - self.half_width

        if self.level.isSolid(self.x + self.half_width, self.y - self.half_height):
            # print("Collision right")
            self.x = currtile_x * TILE_SIZE + TILE_SIZE - self.half_width

        if self.level.isSolid(self.x - self.half_width, self.y - self.half_height):
            # print("Collision left")
            self.x = currtile_x * TILE_SIZE + self.half_width

    def jump(self):
        if not self.jumping:
            self.setState("jumping")
            self.speed_y = -12

    def setState(self, state):
        if state == "idling":
            self.idling = True
            self.running = False
            self.jumping = False
        elif state == "running":
            self.idling = False
            self.running = True
            self.jumping = False
        elif state == "jumping":
            self.idling = False
            self.running = False
            self.jumping = True

    def takeDmg(self):
        self.lifes = self.lifes - 1
