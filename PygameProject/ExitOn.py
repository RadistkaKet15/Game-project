import os
import sys
import pygame
import pygame_gui
import sqlite3

pygame.init()
icon = pygame.image.load('data/exit_ico.ico')
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
game_sounding, moving_pila_right_side, moving_pila_left_side = [True], ['Right'], ['Left']
coin_kolvo_mustClaim, find_the_exit = [0], [False]
font_helping_card, color_helping_card = pygame.font.Font('purisa-boldoblique.ttf',
                                                         30), pygame.Color('white')
hero = 1
name_polzovyatel = ['']
ALPH_UPPERCASE = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
ALPH_LOWERCASE = 'abcdefghijklmnopqrstuvwxyz'
ALPH_DIGITS = '0123456789'

size = width, height = (800, 600)
screen, running, clock = pygame.display.set_mode(size), [True], pygame.time.Clock()
tile_images = {
    'wall': pygame.transform.scale(pygame.image.load('data/box1.png'), (tile_width, tile_height)),
    'empty': pygame.transform.scale(pygame.image.load('data/grass1.png'),
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
    'healka': pygame.transform.scale(pygame.image.load('data/Aptechka.png'),
                                     (tile_width, tile_height))}
exit_on = pygame.image.load('data/ExitOn!.png')
player_image = pygame.transform.scale(pygame.image.load('data/robber.png'), (120, 120))
game_over = pygame.transform.scale(pygame.image.load('data/Game-Over.jpg'), (size))

player = None

font_menu = pygame.font.SysFont('Comic Sans MS', 40)

manager = pygame_gui.UIManager(size)

font = pygame.font.SysFont('serif', 35)

all_sprites = pygame.sprite.Group()
grass_group = pygame.sprite.Group()
boxes_group = pygame.sprite.Group()
capcans_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()
coins_group = pygame.sprite.Group()
pit_group = pygame.sprite.Group()
shield_group = pygame.sprite.Group()
pila_group_right_side = pygame.sprite.Group()
pila_group_left_side = pygame.sprite.Group()
health_group = pygame.sprite.Group()
hp, coin_kolvo_claim, shields_kolvo = [100], [0], [0]
lose_game = [False]


def cleaning_group_of_sprites():
    all_sprites.empty()
    grass_group.empty()
    boxes_group.empty()
    capcans_group.empty()
    player_group.empty()
    coins_group.empty()
    pit_group.empty()
    shield_group.empty()
    pila_group_right_side.empty()
    pila_group_left_side.empty()
    health_group.empty()
    running[0], hp[0], coin_kolvo_claim[0], shields_kolvo[0], coin_kolvo_mustClaim[
        0] = True, 100, 0, 0, 0
    moving_pila_right_side[0], moving_pila_left_side[0] = 'Right', 'Left'
    if game_sounding[0] is True:
        pygame.mixer.music.load('sounds/BACKGROUND_MUSIC_TEST.mp3')
        pygame.mixer.music.set_volume(0.7)
        pygame.mixer.music.play(-1)
    counter[0] = 15


class PasswordError(BaseException):
    pass


con = sqlite3.connect('Users_Base.db')
cur = con.cursor()


def registration():
    manager_gui = pygame_gui.UIManager(size)
    clock = pygame.time.Clock()
    screen, running, complited, text_size = pygame.display.set_mode(size), True, False, 19
    background, complit_regist = pygame.transform.scale(
        pygame.image.load('data/background1.jpg'), (size)), \
                                 pygame.transform.scale(
                                     pygame.image.load('data/ok.png'),
                                     (60, 60))
    logo = pygame.transform.scale(pygame.image.load('data/ExitOn!.png'), (350, 100))
    pygame.display.set_caption('Registration')
    font = pygame.font.SysFont('serif', 35)
    font1 = pygame.font.SysFont('serif', 25)
    name_label = font1.render('Login:', True, (200, 200, 200))
    password_label = font1.render('Password:', True, (200, 200, 200))
    registration_label = font.render('Registration', True, (255, 255, 255))
    condition_label, PasswordError_label = None, None

    regist_button = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((325, 210), (150, 50)),
        manager=manager_gui, text='Regist')
    log_in_button = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((400, 290), (100, 35)),
        manager=manager_gui, text='Sign In')

    entryline_name = pygame_gui.elements.ui_text_entry_line.UITextEntryLine(
        relative_rect=pygame.Rect((300, 110), (200, 30)), manager=manager_gui)

    entryline_passsword = pygame_gui.elements.ui_text_entry_line.UITextEntryLine(
        relative_rect=pygame.Rect((300, 159), (200, 30)), manager=manager_gui)

    while running:
        time_delta = clock.tick(60) / 1000
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.USEREVENT:
                if event.user_type == pygame_gui.UI_BUTTON_PRESSED or \
                        event.user_type == pygame_gui.UI_TEXT_ENTRY_FINISHED:
                    PasswordError_label = None
                    if event.ui_element == regist_button or event.ui_element == entryline_name \
                            or event.ui_element == entryline_passsword:
                        try:
                            if not entryline_name.text and not entryline_passsword.text:
                                condition_label = pygame.font.SysFont('serif',
                                                                      text_size).render(
                                    'You have to make a registration!', True, (255, 0, 0))
                            elif not entryline_name.text:
                                condition_label = pygame.font.SysFont('serif',
                                                                      text_size).render(
                                    'You have to write your nick name!', True, (255, 0, 0))
                            elif not entryline_passsword.text:
                                condition_label = pygame.font.SysFont('serif',
                                                                      text_size).render(
                                    'You have to write your password!', True, (255, 0, 0))
                            elif entryline_name.text and entryline_passsword.text:
                                pas_check = checking_password(entryline_passsword.text)
                                if pas_check:
                                    cur.execute(
                                        "INSERT INTO users(name, password) VALUES(?, ?)",
                                        (entryline_name.text, entryline_passsword.text))
                                    con.commit()
                                    complited = True
                                    condition_label = condition_label = pygame.font.SysFont(
                                        'serif',
                                        text_size).render(
                                        'Successfully registration!', True, (0, 255, 0))
                                else:
                                    raise PasswordError
                        except sqlite3.IntegrityError:
                            condition_label = condition_label = pygame.font.SysFont(
                                'serif', text_size).render(
                                'Sorry, change your Login, please!', True, (255, 0, 0))
                        except PasswordError:
                            condition_label = pygame.font.SysFont('serif',
                                                                  text_size).render(
                                'Something wrong with your password!', True,
                                (255, 0, 0))
                            PasswordError_label = True
                    elif event.ui_element == log_in_button:
                        running = False
                        loggining()
                        return
            manager_gui.process_events(event)

        manager_gui.update(time_delta)
        screen.blit(background, (0, 0))
        screen.blit(logo, (230, 350))
        screen.blit(name_label, (220, 108))
        screen.blit(password_label, (183, 160))
        screen.blit(registration_label, (width / 2 - 85, 30))
        if condition_label:
            if PasswordError_label:
                screen.blit(pygame.font.SysFont('serif',
                                                text_size).render(
                    'Your password must have lower letter, upper letter', True,
                    (255, 0, 0)), (10, 330))
                screen.blit(pygame.font.SysFont('serif',
                                                text_size).render(
                    'and digit! The password must be longer than 6 symbols!', True,
                    (255, 0, 0)), (10, 350))
            screen.blit(condition_label, (10, 297))
        if complited:
            screen.blit(complit_regist, (210, 255))
            manager_gui.draw_ui(screen)
            pygame.display.flip()
            name_polzovyatel[0] = entryline_name.text
            pygame.time.delay(2000)
            return
        manager_gui.draw_ui(screen)
        pygame.display.flip()


def checking_password(password):
    letter_upper, letter_lower, digit = None, None, None
    for elem in password:
        if elem in ALPH_UPPERCASE:
            letter_upper = 1
        elif elem in ALPH_LOWERCASE:
            letter_lower = 1
        elif elem in ALPH_DIGITS:
            digit = 1
    return True if letter_upper == letter_lower == digit == 1 and len(password) > 6 else False


def loggining():
    pygame.display.set_caption('Logging')
    manager_gui = pygame_gui.UIManager(size)
    clock = pygame.time.Clock()
    con = sqlite3.connect('Users_Base.db')
    cur = con.cursor()
    screen, running, complited, text_size = pygame.display.set_mode(size), True, False, 19
    background, complit_logging = pygame.transform.scale(
        pygame.image.load('data/background2.jpg'), (size)), \
                                  pygame.transform.scale(pygame.image.load(
                                      'data/ok.png'),
                                      (60, 60))
    logo = pygame.transform.scale(pygame.image.load('data/ExitOn!.png'), (350, 100))

    pygame.display.set_caption('Sign In')
    font = pygame.font.SysFont('serif', 35)
    font1 = pygame.font.SysFont('serif', 25)
    name_label = font1.render('Login:', True, (255, 255, 170))
    password_label = font1.render('Password:', True, (255, 255, 170))
    registration_label = font.render('Sign In', True, (255, 255, 0))
    condition_label, PasswordError_label = None, None

    log_in_button = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((325, 210), (150, 50)),
        manager=manager_gui, text='Sign In')

    regist_button = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((380, 290), (120, 35)),
        manager=manager_gui, text='Registration')

    entryline_name = pygame_gui.elements.ui_text_entry_line.UITextEntryLine(
        relative_rect=pygame.Rect((300, 110), (200, 30)), manager=manager_gui)

    entryline_passsword = pygame_gui.elements.ui_text_entry_line.UITextEntryLine(
        relative_rect=pygame.Rect((300, 159), (200, 30)), manager=manager_gui)

    while running:
        time_delta = clock.tick(60) / 1000
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.USEREVENT:
                if event.user_type == pygame_gui.UI_BUTTON_PRESSED or \
                        event.user_type == pygame_gui.UI_TEXT_ENTRY_FINISHED:
                    PasswordError_label = None
                    if event.ui_element == log_in_button or event.ui_element == entryline_name \
                            or event.ui_element == entryline_passsword:
                        try:
                            if not entryline_name.text and not entryline_passsword.text:
                                condition_label = pygame.font.SysFont('serif',
                                                                      text_size - 2).render(
                                    'You have to logging or make a registration!', True,
                                    (255, 0, 0))
                            elif not entryline_name.text:
                                condition_label = pygame.font.SysFont('serif',
                                                                      text_size).render(
                                    'You have to write your nick name!', True, (255, 0, 0))
                            elif not entryline_passsword.text:
                                condition_label = pygame.font.SysFont('serif',
                                                                      text_size).render(
                                    'You have to write your password!', True, (255, 0, 0))
                            elif entryline_name.text and entryline_passsword.text:
                                test = list(con.execute(f"""SELECT password FROM USERS
                                                          WHERE name = '{entryline_name.text}'"""))
                                if not test:
                                    condition_label = pygame.font.SysFont('serif',
                                                                          text_size).render(
                                        'We can`t find anything in our base!', True,
                                        (255, 0, 0))
                                    PasswordError_label = True
                                elif test[0][0] == entryline_passsword.text:
                                    complited = True
                                    condition_label = pygame.font.SysFont('serif',
                                                                          text_size).render(
                                        'Successfully logging!', True, (0, 255, 0))
                        except PasswordError:
                            PasswordError_label = True
                    elif event.ui_element == regist_button:
                        running = False
                        registration()
                        return
            manager_gui.process_events(event)

        manager_gui.update(time_delta)
        screen.blit(background, (0, 0))
        screen.blit(logo, (230, 350))
        screen.blit(name_label, (220, 108))
        screen.blit(password_label, (183, 160))
        screen.blit(registration_label, (width / 2 - 50, 30))
        if condition_label:
            if PasswordError_label:
                screen.blit(pygame.font.SysFont('serif',
                                                text_size).render(
                    'Your have to rewrite your password or login...', True,
                    (255, 0, 0)), (10, 315))
                screen.blit(pygame.font.SysFont('serif',
                                                text_size).render(
                    'Or you have to regist!', True,
                    (255, 0, 0)), (10, 332))
            screen.blit(condition_label, (10, 297))
        if complited:
            screen.blit(complit_logging, (190, 255))
            manager_gui.draw_ui(screen)
            pygame.display.flip()
            pygame.time.delay(2000)
            running = False
            name_polzovyatel[0] = entryline_name.text
            return
        manager_gui.draw_ui(screen)
        pygame.display.flip()


counter = [15]
timer_event = pygame.USEREVENT + 1


def main():
    pygame.display.set_caption('ExitOn')
    camera = Camera()
    x_gameOver, y_gameOver = (-450, 0)
    fon, v, clock = pygame.image.load('data/background1.jpg'), 10, pygame.time.Clock()
    font = pygame.font.Font(None, 25)
    start = True

    while running[0] is True:
        # pygame.display.set_caption('Level1')
        ticking = clock.tick() * 10 / 100
        text = font.render(
            f"Your HP: {hp[0]}; Currency: {coin_kolvo_claim[0]}; Shields: {shields_kolvo[0]}",
            True, (100, 255, 100))
        keys = pygame.key.get_pressed()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                confirmation_dialog = pygame_gui.windows.UIConfirmationDialog(
                    rect=pygame.Rect((250, 200), (300, 200)),
                    manager=manager, window_title='Подтверждение',
                    action_long_desc='Вы уверены, что хотите выйти?) Весь ваш прогресс сброситься!',
                    action_short_name='OK',
                    blocking=True)
            if event.type == pygame.KEYDOWN:  # если событие нажатие клавиши
                if event.key == pygame.K_ESCAPE:  # если клавиша Esc
                    game.menu()
            if event.type == pygame.USEREVENT:
                if event.user_type == pygame_gui.UI_CONFIRMATION_DIALOG_CONFIRMED:
                    terminate()
            if event.type == timer_event:
                counter[0] -= 1
                time_text = font.render(str(counter[0]), True, (0, 128, 0))
                if counter[0] == -1:
                    pygame.time.set_timer(timer_event, 0)
                    hp[0] = 0
            manager.process_events(event)
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
            screen.blit(
                pygame.transform.scale(pygame.image.load('data/background1.jpg'), size),
                (0, 0))

            camera.update(player)
            for sprite in all_sprites:
                camera.apply(sprite)
            grass_group.draw(screen)
            boxes_group.draw(screen)
            capcans_group.draw(screen)
            coins_group.draw(screen)
            if coin_kolvo_claim[0] >= coin_kolvo_mustClaim[0]:
                time_font = pygame.font.SysFont(None, 100)
                time_text = time_font.render(str(counter[0]), True, (255, 0, 0))
                pit_group.draw(screen)
                pit_group.update()
                screen.blit(exit_on, (width / 2 - exit_on.get_width() / 2, 30))
                screen.blit(time_text, (width - 90, 10))
                if find_the_exit[0] is True:
                    pygame.time.set_timer(timer_event, 1500)
                    if game_sounding[0] is True:
                        pygame.mixer.music.load('sounds/Find_the_exit.mp3')
                        pygame.mixer.music.set_volume(0.7)
                        pygame.mixer.music.play(-1)
                    find_the_exit[0] = False
            shield_group.draw(screen)
            player_group.draw(screen)
            pila_group_right_side.draw(screen)
            pila_group_right_side.update()
            pila_group_left_side.draw(screen)
            pila_group_left_side.update()
            health_group.draw(screen)
            pygame.draw.rect(screen, pygame.Color('black'), (8, 8, 310, 20))
            if hp[0] <= 25:
                text = font.render(
                    f"Your HP: {hp[0]}; Currency: {coin_kolvo_claim[0]}; Shields: {shields_kolvo[0]}",
                    True, pygame.Color('red'))
            elif hp[0] <= 50:
                text = font.render(
                    f"Your HP: {hp[0]}; Currency: {coin_kolvo_claim[0]}; Shields: {shields_kolvo[0]}",
                    True, pygame.Color('orange'))
            elif hp[0] <= 75:
                text = font.render(
                    f"Your HP: {hp[0]}; Currency: {coin_kolvo_claim[0]}; Shields: {shields_kolvo[0]}",
                    True, pygame.Color('yellow'))
            screen.blit(text, (10, 10))
            clock.tick(100)
            # all_sprites.draw(screen)
        else:
            if game_sounding[0] is True:
                game_over_sound.play()
            screen.blit(game_over, (x_gameOver, y_gameOver))
            lose_game[0] = True
            Game_over()
            if x_gameOver >= 0:
                x_gameOver = x_gameOver
            else:
                x_gameOver += clock.tick() * 75 / 350
        manager.update(ticking)
        manager.draw_ui(screen)
        pygame.display.flip()


def Game_over():
    done = True
    clock = pygame.time.Clock()
    manager_gui = pygame_gui.UIManager(size)
    fon = pygame.transform.scale(pygame.image.load('data/background2.jpg'), (size))
    text = font_menu.render(
        f"!scored {sum(coin_kolvo_claim)} points!",
        True, (255, 255, 0))
    menu_button = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((325, 210), (150, 50)),
        manager=manager_gui, text='menu')
    exit_button = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((340, 320), (170, 40)),
        manager=manager_gui, text='exit')
    # while done:
    #     time_delta = clock.tick(60) / 1000
    #     for event in pygame.event.get():
    #         keys = pygame.key.get_pressed()
    #         if event.type == pygame.QUIT:
    #             terminate()
    #         if event.type == pygame.USEREVENT:
    #             if event.user_type == pygame_gui.UI_BUTTON_PRESSED or \
    #                     event.user_type == pygame_gui.UI_TEXT_ENTRY_FINISHED:
    #                 if event.ui_element == menu_button:
    #                     Menu()
    #                 if event.ui_element == exit_button:
    #                     terminate()
    #         manager_gui.process_events(event)
    # manager_gui.update(time_delta)
    manager_gui.draw_ui(screen)
    screen.blit(fon, (0, 0))
    screen.blit(text, (250, 150))
    pygame.display.flip()
    # game = Menu(items)


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
            fon = pygame.transform.scale(pygame.image.load('data/background1.jpg'), (size))
            screen.blit(fon, (0, 0))
            if game_sounding[0]:
                sound = pygame.transform.scale(pygame.image.load('data/sound.png'), (50, 50))
            else:
                sound = pygame.transform.scale(pygame.image.load('data/sound-off.png'), (50, 50))
            screen.blit(sound, (700, 30))
            mp = pygame.mouse.get_pos()
            for i in self.items:
                if i[0] < mp[0] < i[0] + 200 and i[1] < mp[1] < i[1] + 50:
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
                    if item == 5:
                        store()
            screen.blit(screen, (0, 0))
            pygame.display.flip()


items = [(340, 85, 'Play', (255, 255, 255), (255, 255, 0), 0),
         (340, 175, 'Help', (255, 255, 255), (255, 255, 0), 1),
         (290, 265, 'Options', (255, 255, 255), (255, 255, 0), 4),
         (315, 355, 'Store', (255, 255, 255), (255, 255, 0), 5),
         (340, 445, 'Exit', (255, 255, 255), (255, 255, 0), 2)]
game = Menu(items)


def help():
    done = True  # условие существования цикла меню
    pygame.key.set_repeat(0, 0)  # отключение залипания кнопок

    while done:
        pygame.display.set_caption('Help')
        fon = pygame.transform.scale(pygame.image.load('data/background2.jpg'), (size))
        screen.blit(fon, (0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    done = False
                    pygame.display.set_caption('ExitOn')
        screen.blit(font_helping_card.render('Control:', True, color_helping_card), (340, 10))
        screen.blit(font_helping_card.render('Go down - down arrow', True, color_helping_card),
                    (110, 60))
        screen.blit(font_helping_card.render('Go up - up arrow', True, color_helping_card),
                    (110, 110))
        screen.blit(font_helping_card.render('Go right - right arrow', True, color_helping_card),
                    (110, 160))
        screen.blit(font_helping_card.render('Go left - left arrow', True, color_helping_card),
                    (110, 210))
        screen.blit(font_helping_card.render('Target:', True, color_helping_card), (340, 260))
        screen.blit(font_helping_card.render('The target of our game is to claim all', True,
                                             color_helping_card), (10, 310))
        screen.blit(font_helping_card.render('coins from the level and find an exit from', True,
                                             color_helping_card), (10, 360))
        screen.blit(
            font_helping_card.render('it... But be very accurate ^-^', True, color_helping_card),
            (10, 410))
        screen.blit(font_helping_card.render('Exit help card - ESC', True, color_helping_card),
                    (220, 500))
        pygame.display.flip()  # всё отобразить


def options():
    done = True
    choice = 1
    global tile_images
    global player_image
    global hero
    while done:
        pygame.display.set_caption('Options')
        screen.blit(pygame.image.load('data/background2.jpg'), (0, 0))
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
                    hero = 1
                    player_image = pygame.transform.scale(pygame.image.load('data/robber.png'),
                                                          (120, 120))
                    tile_images['coin'] = pygame.transform.scale(pygame.image.load('data/coin.png'),
                                                                 (
                                                                     tile_width - 20,
                                                                     tile_height - 20))
                    tile_images['car'] = pygame.transform.scale(
                        pygame.image.load('data/police_car.png'),
                        (tile_width + 50, tile_height + 20))
                    tile_images['empty'] = pygame.transform.scale(
                        pygame.image.load('data/grass1.png'),
                        (tile_width, tile_height))
                    tile_images['wall'] = pygame.transform.scale(
                        pygame.image.load('data/box1.png'), (tile_width, tile_height))

                if 400 < mp[0] < 550 and 200 < mp[1] < 350:
                    choice = 2
                    hero = 2
                    player_image = pygame.transform.scale(pygame.image.load('data/men.png'),
                                                          (100, 100))
                    tile_images['coin'] = pygame.transform.scale(
                        pygame.image.load('data/bottle.png'),
                        (tile_width - 5, tile_height - 5))
                    tile_images['car'] = pygame.transform.scale(pygame.image.load('data/car.png'),
                                                                (tile_width + 20, tile_height + 20))
                    tile_images['empty'] = pygame.transform.scale(
                        pygame.image.load('data/grass2.png'),
                        (tile_width, tile_height))
                    tile_images['wall'] = pygame.transform.scale(
                        pygame.image.load('data/box.png'), (tile_width, tile_height))
                if 350 < mp[0] < 450 and 450 < mp[1] < 500:
                    done = False
            if keys[pygame.K_ESCAPE]:
                return
        if choice == 1:
            pygame.draw.rect(screen, (255, 0, 0), (160, 160, 230, 220), 4)
        if choice == 2:
            pygame.draw.rect(screen, (255, 0, 0), (420, 160, 210, 220), 4)
        screen.blit(font_menu.render('Apply', 1, (255, 255, 255)), (350, 450))
        screen.blit(font_menu.render('Choose your hero...', 1, (255, 255, 255)), (220, 50))
        pygame.display.flip()


def store():
    done = True
    time = 15
    manager_gui = pygame_gui.UIManager(size)
    clock = pygame.time.Clock()
    pygame.display.set_caption('Store')
    screen.blit(pygame.image.load('data/background2.jpg'), (0, 0))
    product1 = pygame.transform.scale(pygame.image.load('data/shield1.png'), (140, 190))
    product2 = pygame.transform.scale(pygame.image.load('data/clock.png'), (120, 150))
    screen.blit(product1, (100, 150))
    screen.blit(product2, (360, 150))
    text = font.render(
        f"Currency: {coin_kolvo_claim[0]}; Shields: {shields_kolvo[0]}; Time: {time}",
        True, (100, 255, 100))  # из бд значения надо взять
    buy_button1 = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((80, 320), (170, 40)),
        manager=manager_gui, text='buy')
    buy_button2 = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((340, 320), (170, 40)),
        manager=manager_gui, text='buy')
    while done:
        time_delta = clock.tick(60) / 1000
        for event in pygame.event.get():
            keys = pygame.key.get_pressed()
            if event.type == pygame.QUIT:
                done = False
            if event.type == pygame.USEREVENT:
                if event.user_type == pygame_gui.UI_BUTTON_PRESSED or \
                        event.user_type == pygame_gui.UI_TEXT_ENTRY_FINISHED:
                    if event.ui_element == buy_button1:
                        shields_kolvo[0] += 1
                    if event.ui_element == buy_button2:
                        time += 15
            manager_gui.process_events(event)
            if keys[pygame.K_ESCAPE]:
                return
        screen.blit(text, (10, 10))
        manager_gui.update(time_delta)
        screen.blit(font_menu.render('Catalog', 1, (255, 255, 0)), (340, 50))
        manager_gui.draw_ui(screen)
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


class PilaRight(pygame.sprite.Sprite):
    def __init__(self, tyle_type, pos_x, pos_y):
        super().__init__(pila_group_right_side, all_sprites)
        self.image = pygame.transform.flip(tile_images[tyle_type], True, False)
        self.rect = self.image.get_rect()
        self.rect = self.rect.move(tile_width * pos_x, tile_height * pos_y)
        self.mask = pygame.mask.from_surface(self.image)

    def update(self):
        if pygame.sprite.spritecollideany(self, player_group):
            hp[0] -= 1
        if pygame.sprite.spritecollideany(self, boxes_group):
            if moving_pila_right_side[0] == 'Right':
                self.image = pygame.transform.flip(self.image, True, False)
                moving_pila_right_side[0] = 'Left'
            elif moving_pila_right_side[0] == 'Left':
                self.image = pygame.transform.flip(self.image, True, False)
                moving_pila_right_side[0] = 'Right'
        if moving_pila_right_side[0] == 'Right':
            self.rect.x += 5
        else:
            self.rect.x -= 5


class PilaLeft(pygame.sprite.Sprite):
    def __init__(self, tyle_type, pos_x, pos_y):
        super().__init__(pila_group_left_side, all_sprites)
        self.image = tile_images[tyle_type]
        self.rect = self.image.get_rect()
        self.rect = self.rect.move(tile_width * pos_x, tile_height * pos_y)
        self.mask = pygame.mask.from_surface(self.image)

    def update(self):
        if pygame.sprite.spritecollideany(self, player_group):
            hp[0] -= 1
        if pygame.sprite.spritecollideany(self, boxes_group):
            if moving_pila_left_side[0] == 'Right':
                self.image = pygame.transform.flip(self.image, True, False)
                moving_pila_left_side[0] = 'Left'
            elif moving_pila_left_side[0] == 'Left':
                self.image = pygame.transform.flip(self.image, True, False)
                moving_pila_left_side[0] = 'Right'
        if moving_pila_left_side[0] == 'Right':
            self.rect.x += 5
        else:
            self.rect.x -= 5


class Shield(pygame.sprite.Sprite):
    def __init__(self, tyle_type, pos_x, pos_y):
        super().__init__(shield_group, all_sprites)
        self.image = tile_images[tyle_type]
        self.rect = self.image.get_rect()
        self.rect = self.rect.move(tile_width * pos_x + 12, tile_height * pos_y + 8)
        self.mask = pygame.mask.from_surface(self.image)


class Player(pygame.sprite.Sprite):
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
            coin_kolvo_claim[0] += 1
            if coin_kolvo_mustClaim[0] == coin_kolvo_claim[0]:
                find_the_exit[0] = True
            cur.execute(f"""UPDATE USERS
                                       SET AllCurrency = AllCurrency + 1
                                       WHERE Name = '{name_polzovyatel[0]}'""")
            con.commit()
        if pygame.sprite.spritecollide(self, pit_group, False) and coin_kolvo_claim[0] >= \
                coin_kolvo_mustClaim[0] and lose_game[0] is False:
            running[0] = False
            pygame.time.set_timer(timer_event, 0)
            if game_sounding[0] is True:
                nextLevel_sound.play()
        if pygame.sprite.spritecollide(self, shield_group, True):
            shields_kolvo[0] += 1
            if game_sounding[0] is True:
                shield_claim.play()
        if pygame.sprite.spritecollide(self, health_group, True):
            if lose_game[0] is False:
                hp[0] = 100


class AnimatedSprites(pygame.sprite.Sprite):
    def __init__(self, sheet, columns, rows, pos_x, pos_y):
        super(AnimatedSprites, self).__init__(pit_group, all_sprites)
        self.frames = []
        self.crop_sheet(sheet, columns, rows)
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        self.rect = self.rect.move(tile_width * pos_x + 10, tile_height * pos_y + 5)

    def crop_sheet(self, sheet, columns, rows):
        self.rect = pygame.Rect(0, 0, sheet.get_width() // columns, sheet.get_height() // rows)
        for j in range(rows):
            for i in range(columns):
                frame_coords = (self.rect.w * i, self.rect.h * j)
                self.frames.append(sheet.subsurface(pygame.Rect(frame_coords, self.rect.size)))

    def update(self):
        self.cur_frame = (self.cur_frame + 1) % len(self.frames)
        self.image = self.frames[self.cur_frame]


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
                coin_kolvo_mustClaim[0] += 1
            elif level[y][x] == '^':
                Land('empty', x, y)
                AnimatedSprites(pygame.transform.scale(
                    pygame.transform.flip(pygame.image.load('data/exit_portal.png'), True, False),
                    (200, 140)), 4, 1, x, y)
            elif level[y][x] == '!':
                Land('empty', x, y)
                Shield('shield', x, y)
            elif level[y][x] == '>':
                Land('empty', x, y)
                PilaRight('car', x, y)
            elif level[y][x] == '<':
                Land('empty', x, y)
                PilaLeft('car', x, y)
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


registration()
game.menu()
game.menu()
player, level_x, level_y = generate_level(load_level('level_1.txt'))
main()
tile_images['empty'] = pygame.transform.scale(pygame.image.load('data/grass4.png'),
                                              (tile_width, tile_height))
tile_images['wall'] = pygame.transform.scale(pygame.image.load('data/box2.png'),
                                             (tile_width, tile_height))
tile_images['capcan'] = pygame.transform.scale(pygame.image.load('data/capcan.png'),
                                               (tile_width + 10, tile_height + 10))
if hero == 1:
    tile_images['coin'] = pygame.transform.scale(pygame.image.load('data/key.png'),
                                                 (tile_width - 10, tile_height - 10))
if hero == 2:
    tile_images['coin'] = pygame.transform.scale(pygame.image.load('data/bottle1.png'),
                                                 (tile_width + 5, tile_height + 5))
cleaning_group_of_sprites()
player, level_x, level_y = generate_level(load_level('level_2.txt'))
main()
tile_images['empty'] = pygame.transform.scale(pygame.image.load('data/land.png'),
                                              (tile_width, tile_height))
tile_images['wall'] = pygame.transform.scale(pygame.image.load('data/box1.png'),
                                             (tile_width, tile_height))
tile_images['capcan'] = pygame.transform.scale(pygame.image.load('data/fair.png'),
                                               (tile_width - 10, tile_height - 10))
cleaning_group_of_sprites()
player, level_x, level_y = generate_level(load_level('level_3.txt'))
main()
tile_images['empty'] = pygame.transform.scale(pygame.image.load('data/grass3.png'),
                                              (tile_width, tile_height))
tile_images['wall'] = pygame.transform.scale(pygame.image.load('data/box3.png'),
                                             (tile_width, tile_height))
tile_images['capcan'] = pygame.transform.scale(pygame.image.load('data/capcan.png'),
                                               (tile_width - 10, tile_height - 10))
cleaning_group_of_sprites()
player, level_x, level_y = generate_level(load_level('level_4.txt'))
main()
tile_images['empty'] = pygame.transform.scale(pygame.image.load('data/water.png'),
                                              (tile_width, tile_height))
tile_images['capcan'] = pygame.transform.scale(pygame.image.load('data/bird.png'),
                                               (tile_width, tile_height))
if hero == 1:
    tile_images['coin'] = pygame.transform.scale(pygame.image.load('data/coin.png'),
                                                 (tile_width - 10, tile_height - 10))
if hero == 2:
    tile_images['coin'] = pygame.transform.scale(pygame.image.load('data/bottle.png'),
                                                 (tile_width + 5, tile_height + 5))
cleaning_group_of_sprites()
player, level_x, level_y = generate_level(load_level('level_5.txt'))
main()
tile_images['empty'] = pygame.transform.scale(pygame.image.load('data/ground3.jpg'),
                                              (tile_width, tile_height))
tile_images['wall'] = pygame.transform.scale(pygame.image.load('data/box.png'),
                                             (tile_width, tile_height))
if hero == 2:
    tile_images['coin'] = pygame.transform.scale(pygame.image.load('data/bottle1.png'),
                                                 (tile_width + 5, tile_height + 5))
tile_images['capcan'] = pygame.transform.scale(pygame.image.load('data/trip_capcan.png'),
                                               (tile_width + 5, tile_height + 5))
cleaning_group_of_sprites()
player, level_x, level_y = generate_level(load_level('level_6.txt'))
main()
tile_images['empty'] = pygame.transform.scale(pygame.image.load('data/ground2.png'),
                                              (tile_width, tile_height))
tile_images['wall'] = pygame.transform.scale(pygame.image.load('data/box1.png'),
                                             (tile_width, tile_height))
if hero == 1:
    tile_images['coin'] = pygame.transform.scale(pygame.image.load('data/coin.png'),
                                                 (tile_width - 10, tile_height - 10))
if hero == 2:
    tile_images['coin'] = pygame.transform.scale(pygame.image.load('data/bottle.png'),
                                                 (tile_width + 5, tile_height + 5))
tile_images['capcan'] = pygame.transform.scale(pygame.image.load('data/pit1.png'),
                                               (tile_width, tile_height))
cleaning_group_of_sprites()
player, level_x, level_y = generate_level(load_level('level_7.txt'))
main()
