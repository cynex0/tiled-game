import time

TILE_SIZE = 32
TILES_X = 32
TILES_Y = 17
WIDTH = TILES_X * TILE_SIZE
HEIGHT = TILES_Y * TILE_SIZE
MAX_LIFES = 5


def millis():
    return int(time.time()*1000)
