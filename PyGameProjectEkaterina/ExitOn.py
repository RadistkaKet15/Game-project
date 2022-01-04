import os
import sys
import pygame
import random

pygame.init()
icon = pygame.image.load('femida.png')
pygame.display.set_icon(icon)
pygame.mixer.music.load('sounds/BACKGROUND_MUSIC_TEST.mp3')
pygame.mixer.music.set_volume(0.7)
pygame.mixer.music.play(-1)
capcan_sound = pygame.mixer.Sound('sounds/hit_capcan.wav')
coin_claim = pygame.mixer.Sound('sounds/coin.wav')
game_over_sound = pygame.mixer.Sound('sounds/game-over.wav')
shield_claim = pygame.mixer.Sound('sounds/shield.wav')
shield_cancel = pygame.mixer.Sound('sounds/minus_shield.wav')
nextLevel_sound = pygame.mixer.Sound('sounds/next_level.wav')
tile_width = tile_height = 75
game_sounding, moving_pila = [True], ['Right']

size = width, height = (800, 600)
screen, running, clock = pygame.display.set_mode(size), [True], pygame.time.Clock()
tile_images = {
    'wall': pygame.transform.scale(pygame.image.load('data/box.png'), (tile_width, tile_height)),
    'empty': pygame.transform.scale(pygame.image.load('data/grass.png'),
                                    (tile_width, tile_height)),
    'capcan': pygame.transform.scale(pygame.image.load('data/trip_capcan.png'),
                                     (tile_width, tile_height)),
    'coin': pygame.transform.scale(pygame.image.load('data/coin.png'),
                                   (tile_width - 20, tile_height - 20)),
    'pit': pygame.transform.scale(pygame.image.load('data/Pit.png'), (tile_width, tile_height)),
    'shield': pygame.transform.scale(pygame.image.load('data/Shield.png'),
                                     (tile_width - 20, tile_height - 10)),
    'pila': pygame.transform.scale(pygame.image.load('data/trap_pila.png'),
                                   (tile_width, tile_height)),
    'healka': pygame.transform.scale(pygame.image.load('data/Trap_devil.png'),
                                     (tile_width, tile_height))}

player_image = pygame.transform.scale(pygame.image.load('data/Player_test.png'), (55, 65))
game_over = pygame.transform.scale(pygame.image.load('data/Game-Over.jpg'), (size))

player = None

font_menu = pygame.font.SysFont('Comic Sans MS', 40)


def terminate():
    pygame.quit()
    sys.exit()


def load_level(filename):
    filename = 'Levels/' + filename
    with open(filename, 'r', encoding='utf-8') as my_file:
        level_map = [line.strip() for line in my_file.readlines()]
    max_width = max([len(x) for x in level_map])
    return list(map(lambda x: x.ljust(max_width, '.'), level_map))


class Menu:
    def __init__(self, items=[120, 140, 'Punkt', (0, 0, 0), (255, 255, 255), 0]):
        self.items = items

    def render(self, poverhnost, font, number_item):
        for i in self.items:
            if number_item == i[5]:
                poverhnost.blit(font.render(i[2], 1, i[4]), (i[0], i[1]))
            else:
                poverhnost.blit(font.render(i[2], 1, i[3]), (i[0], i[1]))

    def menu(self):
        done = True
        font_menu = pygame.font.Font('purisa-boldoblique.ttf', 50)
        item = 0
        while done:
            # screen.fill("#fdc294")
            fon = pygame.transform.scale(pygame.image.load('data/background_for_game.jpg'), (size))
            screen.blit(fon, (0, 0))
            if game_sounding[0]:
                sound = pygame.transform.scale(pygame.image.load('data/sound.png'), (50, 50))
            else:
                sound = pygame.transform.scale(pygame.image.load('data/sound-off.png'), (50, 50))
            screen.blit(sound, (700, 30))
            mp = pygame.mouse.get_pos()
            for i in self.items:
                if mp[0] > i[0] and mp[0] < i[0] + 200 and mp[1] > i[1] and mp[1] < i[1] + 50:
                    item = i[5]
                if 700 < mp[0] < 750 and 30 < mp[1] < 80:
                    item = 3
            self.render(screen, font_menu, item)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    terminate()
                if event.type == pygame.KEYDOWN:  # если событие нажатие клавиши
                    if event.key == pygame.K_ESCAPE:  # если клавиша Esc
                        terminate()
                    if event.key == pygame.K_UP:
                        if item > 0:
                            item -= 1
                    if event.key == pygame.K_DOWN:
                        if item < len(self.items) - 1:
                            item += 1
                    if event.key == pygame.K_RETURN:
                        if item == 0:
                            return
                        if item == 1:
                            help()
                        if item == 2:
                            terminate()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if item == 0:
                        return
                    if item == 1:
                        help()
                    if item == 2:
                        terminate()
                    if item == 3:
                        if game_sounding[0] is True:
                            pygame.mixer.music.pause()
                            sound = pygame.transform.scale(pygame.image.load('data/sound-off.png'),
                                                           (50, 50))
                            screen.blit(sound, (700, 30))
                            game_sounding[0] = False
                        else:
                            pygame.mixer.music.unpause()
                            sound = pygame.transform.scale(pygame.image.load('data/sound.png'),
                                                           (50, 50))
                            screen.blit(sound, (700, 30))
                            game_sounding[0] = True
                    if item == 4:
                        options()
                        pygame.display.set_caption('ExitOn')
            screen.blit(screen, (0, 0))
            pygame.display.flip()


items = [(340, 110, 'Play', (255, 255, 255), (255, 255, 0), 0),
         (340, 200, 'Help', (255, 255, 255), (255, 255, 0), 1),
         (290, 290, 'Options', (255, 255, 255), (255, 255, 0), 4),
         (340, 380, 'Exit', (255, 255, 255), (255, 255, 0), 2)]
game = Menu(items)


def help():
    done = True  # условие существования цикла меню
    pygame.key.set_repeat(0, 0)  # отключение залипания кнопок

    while done:
        pygame.display.set_caption('Help')
        fon = pygame.transform.scale(pygame.image.load('data/optionfon.jpg'), (size))
        screen.blit(fon, (0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    done = False
                    pygame.display.set_caption('ExitOn')
        screen.blit(font_menu.render('движение вниз - стрелка вниз', 1, (0, 0, 0)), (110, 100))
        screen.blit(font_menu.render('движение вверх - стрелка вверх', 1, (0, 0, 0)), (110, 160))
        screen.blit(font_menu.render('движение влево - стрелка влево', 1, (0, 0, 0)), (110, 220))
        screen.blit(font_menu.render('движение вправо - стрелка вправо', 1, (0, 0, 0)),
                    (110, 280))
        screen.blit(font_menu.render('выход в меню - ESC', 1, (0, 0, 0)), (180, 450))
        screen.blit(screen, (0, 30))  # прорисовка на окне экрана для меню

        pygame.display.flip()  # всё отобразить


def options():
    done = True

    while done:
        pygame.display.set_caption('Options')
        screen.blit(pygame.transform.scale(pygame.image.load('data/optionfon.jpg'), size), (0, 0))
        for event in pygame.event.get():
            keys = pygame.key.get_pressed()
            if event.type == pygame.QUIT:
                done = False

            if keys[pygame.K_ESCAPE]:
                return

        pygame.display.flip()


if __name__ == '__main__':
    game.menu()
