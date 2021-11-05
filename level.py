import pygame
import ast
import random
from enemy import Enemy
from constants import *


class Level:
    def __init__(self, level_map):
        map_file = open(level_map, 'r')
        self.map = ast.literal_eval(map_file.read())
        map_file.close()

        self.door_img = pygame.image.load('sprites/door.png')
        self.tile_imgs = []
        self.dirt_imgs = []
        self.tiles = []
        self.enemies = []

        for i in range(14):
            img = pygame.image.load('sprites/tiles/tile' + str(i).rjust(3, '0') + '.png')
            self.tile_imgs.append(pygame.transform.scale(img, (TILE_SIZE, TILE_SIZE)))
        for i in range(5):
            img = pygame.image.load('sprites/tiles/dirt/tile' + str(i) + '.png')
            self.dirt_imgs.append(pygame.transform.scale(img, (TILE_SIZE, TILE_SIZE)))

        row_count = 0
        for row in self.map:
            col_count = 0
            for tile in row:
                if tile >= 0 and tile != 15:
                    if tile != 14:
                        if tile == 11:
                            img = self.dirt_imgs[random.randint(0, 4)]
                        else:
                            img = self.tile_imgs[tile]
                        tile = (img, (col_count * TILE_SIZE, row_count * TILE_SIZE))
                    else:
                        img = self.door_img
                        tile = (img, (col_count * TILE_SIZE, row_count * TILE_SIZE + 16))
                        self.door_rect = pygame.Rect(
                            (col_count * TILE_SIZE, row_count * TILE_SIZE + 16),
                            (self.door_img.get_width(), self.door_img.get_height()))

                    self.tiles.append(tile)
                elif tile == 15:
                    self.enemies.append(Enemy(self, col_count * TILE_SIZE, (row_count - 1) * TILE_SIZE))
                col_count = col_count + 1
            row_count = row_count + 1

    def draw(self, screen):
        for tile in self.tiles:
            screen.blit(tile[0], tile[1])

    def getGroundTile(self, x):
        x = round(x // TILE_SIZE)
        i = len(self.map) - 1
        while self.map[i][x] > 0:
            i = i - 1
        return len(self.map) - i - 1

    def isSolid(self, x, y, emptyblock_isSolid=False):
        x = round(x // TILE_SIZE)
        y = round(y // TILE_SIZE)  # coords to tile index

        if y >= TILES_Y:
            return True
        if x >= TILES_X:
            return True

        excluded_blocks = [-1, 14, 15]
        if not emptyblock_isSolid:
            excluded_blocks.append(-2)

        if y >= TILE_SIZE * TILES_Y + TILE_SIZE:
            return False

        if self.map[y][x] not in excluded_blocks:
            return True

        else:
            return False
