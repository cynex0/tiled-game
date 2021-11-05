import pygame
from level import Level
from player import Player
from constants import *


class Game:
    def __init__(self):
        pygame.init()
        self.clock = pygame.time.Clock()

        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption('Tiled')

        self.status = 'menu'
        self.levels = [Level('levels/1.txt'), Level('levels/2.txt'), Level('levels/3.txt')]
        self.current_level = 0
        self.player = Player(self.levels[self.current_level])

        self.background = pygame.transform.scale(pygame.image.load('sprites/Background.png'), (WIDTH, HEIGHT))
        self.heart_full = pygame.transform.scale2x(pygame.image.load('sprites/heart/full.png'))
        self.heart_empty = pygame.transform.scale2x(pygame.image.load('sprites/heart/empty.png'))

        self.title = pygame.font.Font("sprites/gumball.ttf", 192).render("Tiled", True,
                                                                         (238, 138, 69))
        self.title_rect = self.title.get_rect()
        self.title_rect.center = (WIDTH // 2, HEIGHT // 2)

        self.starttext = pygame.font.Font("sprites/gumball.ttf", 32).render("Press any button to start",
                                                                            True, (10, 10, 10))
        self.starttext_rect = self.starttext.get_rect()
        self.starttext_rect.center = (WIDTH // 2, (HEIGHT // 2) + 150)

        self.over_text = pygame.font.Font("sprites/gumball.ttf", 192).render("Game Over", True,
                                                                             (210, 36, 36))
        self.over_text_rect = self.over_text.get_rect()
        self.over_text_rect.center = (WIDTH // 2, HEIGHT // 2)

        self.win_text = pygame.font.Font("sprites/gumball.ttf", 192).render("Game Over", True,
                                                                            (36, 210, 57))
        self.win_text_rect = self.win_text.get_rect()
        self.win_text_rect.center = (WIDTH // 2, HEIGHT // 2)

        self.restext = pygame.font.Font("sprites/gumball.ttf", 32).render("Press [r] to restart",
                                                                          True, (10, 10, 10))
        self.restext_rect = self.restext.get_rect()
        self.restext_rect.center = (WIDTH // 2, (HEIGHT // 2) + 110)

        self.quittext = pygame.font.Font("sprites/gumball.ttf", 32).render("Press [ESC] to quit",
                                                                           True, (10, 10, 10))
        self.quittext_rect = self.quittext.get_rect()
        self.quittext_rect.center = (WIDTH // 2, (HEIGHT // 2) + 140)

        self.level_text_font = pygame.font.Font("sprites/gumball.ttf", 52)

    def game_loop(self):
        while self.status == 'menu':
            self.screen.blit(self.background, (0, 0))
            matte = pygame.Surface((WIDTH, HEIGHT))
            matte.fill((0, 0, 0))
            matte.set_alpha(20)
            self.screen.blit(matte, (0, 0))
            self.screen.blit(self.title, self.title_rect)
            self.screen.blit(self.starttext, self.starttext_rect)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.status = ''
            pressed = pygame.key.get_pressed()
            if True in pressed:
                self.status = 'playing'

            pygame.display.flip()
            self.clock.tick(60)

        while self.status == 'playing':
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.status = ''

            pressed = pygame.key.get_pressed()
            delta_x = 0
            if pressed[pygame.K_LEFT]:
                delta_x += -1

            if pressed[pygame.K_RIGHT]:
                delta_x += 1

            if pressed[pygame.K_UP]:
                self.player.jump()

            self.player.move(delta_x)

            if self.player.completed():
                self.current_level = self.current_level + 1
                if self.current_level >= len(self.levels):
                    self.status = 'win'
                else:
                    self.player = Player(self.levels[self.current_level])
                continue

            for enemy in self.levels[self.current_level].enemies:
                if not enemy.dead:
                    enemy.move()
                    if enemy.collideWithPlayer(self.player):
                        self.player.takeDmg()
                        self.player.reset()

            if self.player.lifes <= 0:
                self.status = 'over'

            self.screen.blit(self.background, self.background.get_rect())
            level_text = self.level_text_font.render("Level " + str(self.current_level + 1), True, (238, 138, 69))
            level_text_rect = level_text.get_rect()
            level_text_rect.center = (WIDTH / 2, 20)
            self.screen.blit(level_text, level_text_rect)

            self.levels[self.current_level].draw(self.screen)

            for i in range(self.player.lifes):
                self.screen.blit(self.heart_full, ((i + 1) * TILE_SIZE, TILE_SIZE))
            for j in range(self.player.lifes, MAX_LIFES):
                self.screen.blit(self.heart_empty, ((j + 1) * TILE_SIZE, TILE_SIZE))

            self.player.draw(self.screen)
            for enemy in self.levels[self.current_level].enemies:
                if not enemy.dead:
                    enemy.draw(self.screen)

            pygame.display.flip()
            self.clock.tick(60)

        while self.status == 'over':
            self.screen.blit(self.background, (0, 0))
            matte = pygame.Surface((WIDTH, HEIGHT))
            matte.fill((0, 0, 0))
            matte.set_alpha(20)
            self.screen.blit(matte, (0, 0))
            self.screen.blit(self.over_text, self.over_text_rect)
            self.screen.blit(self.restext, self.restext_rect)
            self.screen.blit(self.quittext, self.quittext_rect)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.status = ''
            pressed = pygame.key.get_pressed()
            if pressed[pygame.K_ESCAPE]:
                self.status = ''
            if pressed[pygame.K_r]:
                self.__init__()
                self.status = 'playing'
                # self.current_level = 0
                # self.player = Player(self.levels[self.current_level])

            pygame.display.flip()
            self.clock.tick(60)

        while self.status == 'win':
            self.screen.blit(self.background, (0, 0))
            matte = pygame.Surface((WIDTH, HEIGHT))
            matte.fill((0, 0, 0))
            matte.set_alpha(20)
            self.screen.blit(matte, (0, 0))
            self.screen.blit(self.win_text, self.win_text_rect)
            self.screen.blit(self.restext, self.restext_rect)
            self.screen.blit(self.quittext, self.quittext_rect)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.status = ''

            pressed = pygame.key.get_pressed()
            if pressed[pygame.K_ESCAPE]:
                self.status = ''
            if pressed[pygame.K_r]:
                self.__init__()
                self.status = 'playing'
                # self.current_level = 0
                # self.player = Player(self.levels[self.current_level])

            pygame.display.flip()
            self.clock.tick(60)


if __name__ == '__main__':
    game = Game()
    while game.status != '':
        game.game_loop()
    pygame.quit()
