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
    'empty': pygame.transform.scale(pygame.image.load('data/grass2.png'),
                                    (tile_width, tile_height)),
    'capcan': pygame.transform.scale(pygame.image.load('data/trip_capcan.png'),
                                     (tile_width, tile_height)),
    'coin': pygame.transform.scale(pygame.image.load('data/coin.png'),
                                   (tile_width - 20, tile_height - 20)),
    'pit': pygame.transform.scale(pygame.image.load('data/Pit.png'), (tile_width, tile_height)),
    'shield': pygame.transform.scale(pygame.image.load('data/Shield.png'),
                                     (tile_width - 20, tile_height - 10)),
    'car': pygame.transform.scale(pygame.image.load('data/police_car.png'),
                                   (tile_width + 50, tile_height + 20)),
    'healka': pygame.transform.scale(pygame.image.load('data/Trap_devil.png'),
                                     (tile_width, tile_height))}

player_image = pygame.transform.scale(pygame.image.load('data/robber.png'), (120, 120))
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
    choice = 1
    global tile_images
    global player_image
    while done:
        pygame.display.set_caption('Options')
        screen.fill(pygame.Color('black'))
        player1 = pygame.transform.scale(pygame.image.load('data/robber.png'), (150, 150))
        screen.blit(player1, (200, 200))
        player2 = pygame.transform.scale(pygame.image.load('data/men.png'), (150, 150))
        screen.blit(player2, (450, 200))
        for event in pygame.event.get():
            keys = pygame.key.get_pressed()
            if event.type == pygame.QUIT:
                done = False
            mp = pygame.mouse.get_pos()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if 200 < mp[0] < 350 and 200 < mp[1] < 350:
                    choice = 1
                    player_image = pygame.transform.scale(pygame.image.load('data/robber.png'),
                                                          (120, 120))
                    tile_images['coin'] = pygame.transform.scale(pygame.image.load('data/coin.png'),
                                   (tile_width - 20, tile_height - 20))
                    tile_images['car'] = pygame.transform.scale(pygame.image.load('data/police_car.png'),
                                   (tile_width + 20, tile_height + 20))

                if 400 < mp[0] < 550 and 200 < mp[1] < 350:
                    choice = 2
                    player_image = pygame.transform.scale(pygame.image.load('data/men.png'), (100, 100))
                    tile_images['coin'] = pygame.transform.scale(pygame.image.load('data/bottle.png'),
                                                                 (tile_width - 20, tile_height - 20))
                    tile_images['car'] = pygame.transform.scale(pygame.image.load('data/car.png'),
                                                                (tile_width + 20, tile_height + 20))
            if keys[pygame.K_ESCAPE]:
                return
        if choice == 1:
            pygame.draw.rect(screen, (255, 0, 0), (160, 160, 230, 220), 4)
        if choice == 2:
            pygame.draw.rect(screen, (255, 0, 0), (420, 160, 210, 220), 4)
        screen.blit(font_menu.render('Выбери персонажа', 1, (255, 255, 255)), (220, 50))
        pygame.display.flip()


class Land(pygame.sprite.Sprite):
    def __init__(self, tyle_type, pos_x, pos_y):
        super().__init__(grass_group, all_sprites)
        self.image = tile_images[tyle_type]
        self.rect = self.image.get_rect()
        self.rect = self.rect.move(tile_width * pos_x, tile_height * pos_y)
        self.mask = pygame.mask.from_surface(self.image)


class Capcan(pygame.sprite.Sprite):
    def __init__(self, tyle_type, pos_x, pos_y):
        super().__init__(capcans_group, all_sprites)
        self.image = tile_images[tyle_type]
        self.rect = self.image.get_rect()
        self.rect = self.rect.move(tile_width * pos_x + 2, tile_height * pos_y)
        self.mask = pygame.mask.from_surface(self.image)


class Boxes(pygame.sprite.Sprite):
    def __init__(self, tyle_type, pos_x, pos_y):
        super().__init__(boxes_group, all_sprites)
        self.image = tile_images[tyle_type]
        self.rect = self.image.get_rect()
        self.rect = self.rect.move(tile_width * pos_x, tile_height * pos_y)
        self.mask = pygame.mask.from_surface(self.image)


class Coin(pygame.sprite.Sprite):
    def __init__(self, tyle_type, pos_x, pos_y):
        super().__init__(coins_group, all_sprites)
        self.image = tile_images[tyle_type]
        self.rect = self.image.get_rect()
        self.rect = self.rect.move(tile_width * pos_x + 12, tile_height * pos_y + 10)
        self.mask = pygame.mask.from_surface(self.image)


class Healka(pygame.sprite.Sprite):
    def __init__(self, tyle_type, pos_x, pos_y):
        super().__init__(health_group, all_sprites)
        self.image = tile_images[tyle_type]
        self.rect = self.image.get_rect()
        self.rect = self.rect.move(tile_width * pos_x, tile_height * pos_y)
        self.mask = pygame.mask.from_surface(self.image)


class Pit(pygame.sprite.Sprite):
    def __init__(self, tyle_type, pos_x, pos_y):
        super().__init__(pit_group, all_sprites)
        self.image = tile_images[tyle_type]
        self.rect = self.image.get_rect()
        self.rect = self.rect.move(tile_width * pos_x, tile_height * pos_y)
        self.mask = pygame.mask.from_surface(self.image)


class Pila(pygame.sprite.Sprite):
    def __init__(self, tyle_type, pos_x, pos_y):
        super().__init__(pila_group, all_sprites)
        self.image = tile_images[tyle_type]
        self.rect = self.image.get_rect()
        self.rect = self.rect.move(tile_width * pos_x, tile_height * pos_y)
        self.mask = pygame.mask.from_surface(self.image)

    def update(self):
        if pygame.sprite.spritecollideany(self, player_group):
            hp[0] -= 1
        if pygame.sprite.spritecollideany(self, boxes_group):
            if moving_pila[0] == 'Right':
                self.image = pygame.transform.flip(self.image, True, False)
                moving_pila[0] = 'Left'
            elif moving_pila[0] == 'Left':
                self.image = pygame.transform.flip(self.image, True, False)
                moving_pila[0] = 'Right'
        if moving_pila[0] == 'Right':
            self.rect.x -= 5
        else:
            self.rect.x += 5


class Shield(pygame.sprite.Sprite):
    def __init__(self, tyle_type, pos_x, pos_y):
        super().__init__(shield_group, all_sprites)
        self.image = tile_images[tyle_type]
        self.rect = self.image.get_rect()
        self.rect = self.rect.move(tile_width * pos_x + 12, tile_height * pos_y + 8)
        self.mask = pygame.mask.from_surface(self.image)


class Player(pygame.sprite.Sprite):
    global hp

    def __init__(self, pos_x, pos_y):
        super().__init__(player_group, all_sprites)
        self.image = player_image
        self.rect = self.image.get_rect()
        self.rect = self.rect.move(tile_width * pos_x + 15, tile_height * pos_y + 5)
        self.mask = pygame.mask.from_surface(self.image)

    def update(self, x, y, napravlenie):
        if pygame.sprite.spritecollideany(self, boxes_group):
            if napravlenie == 'left':
                player.rect.x += 8
            elif napravlenie == 'right':
                player.rect.x -= 8
            elif napravlenie == 'down':
                player.rect.y -= 8
            elif napravlenie == 'up':
                player.rect.y += 8
        if pygame.sprite.spritecollide(self, capcans_group, True):
            if shields_kolvo[0] == 0:
                if game_sounding[0] is True:
                    capcan_sound.play()
                hp[0] -= 10
            else:
                if game_sounding[0] is True:
                    shield_cancel.play()
                shields_kolvo[0] -= 1
        if pygame.sprite.spritecollide(self, coins_group, True):
            if game_sounding[0] is True:
                coin_claim.play()
            coin_kolvo[0] += 1
        if pygame.sprite.spritecollide(self, pit_group, False) and coin_kolvo[0] != 0:
            running[0] = False
            if game_sounding[0] is True:
                nextLevel_sound.play()
        if pygame.sprite.spritecollide(self, shield_group, True):
            shields_kolvo[0] += 1
            if game_sounding[0] is True:
                shield_claim.play()
        if pygame.sprite.spritecollide(self, health_group, True):
            hp[0] = 100


def generate_level(level):
    new_player, x, y = None, None, None
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '.':
                Land('empty', x, y)
            elif level[y][x] == '#':
                Land('empty', x, y)
                Boxes('wall', x, y)
            elif level[y][x] == '@':
                Land('empty', x, y)
                new_player = Player(x, y)
            elif level[y][x] == '$':
                Land('empty', x, y)
                Capcan('capcan', x, y)
            elif level[y][x] == '*':
                Land('empty', x, y)
                Coin('coin', x, y)
            elif level[y][x] == '^':
                Land('empty', x, y)
                Pit('pit', x, y)
            elif level[y][x] == '!':
                Land('empty', x, y)
                Shield('shield', x, y)
            elif level[y][x] == 'p':
                Land('empty', x, y)
                Pila('car', x, y)
            elif level[y][x] == 'h':
                Land('empty', x, y)
                Healka('healka', x, y)
    return new_player, x, y


class Camera:
    def __init__(self):
        self.dx = 0
        self.dy = 0

    def apply(self, obj):
        obj.rect.x += self.dx
        obj.rect.y += self.dy

    def update(self, target):
        self.dx = width // 2 - target.rect.x - target.rect.w // 2
        self.dy = height // 2 - target.rect.y - target.rect.h // 2


if __name__ == '__main__':
    hp, coin_kolvo, shields_kolvo = [100], [0], [0]
    pygame.display.set_caption('ExitOn')
    camera = Camera()

    x_gameOver, y_gameOver = (-450, 0)

    all_sprites = pygame.sprite.Group()
    grass_group = pygame.sprite.Group()
    boxes_group = pygame.sprite.Group()
    capcans_group = pygame.sprite.Group()
    player_group = pygame.sprite.Group()
    coins_group = pygame.sprite.Group()
    pit_group = pygame.sprite.Group()
    shield_group = pygame.sprite.Group()
    pila_group = pygame.sprite.Group()
    health_group = pygame.sprite.Group()

    game.menu()
    fon, v, clock = pygame.image.load('data/fon.jpg'), 10, pygame.time.Clock()
    font = pygame.font.Font(None, 25)
    player, level_x, level_y = generate_level(load_level('level_2.txt'))
    start = True

    while running[0] is True:
        pygame.display.set_caption('Level1')
        ticking = clock.tick() * 10 / 100
        text = font.render(f"Your HP: {hp[0]}; Bottle: {coin_kolvo[0]}; Shields: {shields_kolvo[0]}",
                           True, (100, 255, 100))
        keys = pygame.key.get_pressed()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.KEYDOWN:  # если событие нажатие клавиши
                if event.key == pygame.K_ESCAPE:  # если клавиша Esc
                    game.menu()
        if keys[pygame.K_LEFT]:
            player.rect.x -= 8
            player_group.update(player.rect.x, player.rect.y, 'left')
        if keys[pygame.K_UP]:
            player.rect.y -= 8
            player_group.update(player.rect.x, player.rect.y, 'up')
        if keys[pygame.K_RIGHT]:
            player.rect.x += 8
            player_group.update(player.rect.x, player.rect.y, 'right')
        if keys[pygame.K_DOWN]:
            player.rect.y += 8
            player_group.update(player.rect.x, player.rect.y, 'down')
        if hp[0] > 0:
            screen.blit(pygame.transform.scale(pygame.image.load('data/background_for_game.jpg'), size), (0, 0))
            camera.update(player)
            for sprite in all_sprites:
                camera.apply(sprite)
            grass_group.draw(screen)
            boxes_group.draw(screen)
            capcans_group.draw(screen)
            coins_group.draw(screen)
            pit_group.draw(screen)
            shield_group.draw(screen)
            player_group.draw(screen)
            pila_group.draw(screen)
            pila_group.update()
            health_group.draw(screen)
            pygame.draw.rect(screen, pygame.Color('purple'), (8, 8, 270, 20))
            screen.blit(text, (10, 10))
            clock.tick(100)
            # all_sprites.draw(screen)
        else:
            game_over_sound.play()
            screen.blit(game_over, (x_gameOver, y_gameOver))
            if x_gameOver >= 0:
                x_gameOver = x_gameOver
            else:
                x_gameOver += clock.tick() * 75 / 350
        pygame.display.flip()