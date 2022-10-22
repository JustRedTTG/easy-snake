import pygameextra as pe
import random

"""
Код направен от Ред с любов <3 

моля ползвайте pygameextra 2 версия 2.0.0b7 или по-нова
`pip install pygameextra 2.0.0b7`

Лесна Змия функционалност:
1. Променлив размер на екрана
2. Лесна логика за таблото
3. Лесна логика за посоки
4. Лесна логика за движение
5. Лесна логика за графиката
6. Лесен монитор на точни
7. Лесни функций за пауза, край на играта и рестартиране на играта 
8. Цветове на змията според дължината, лично любима функционалност!


Всичко е лесно!
Змия е много лесна игра!
Благодарение на pygameextra, че прави нещата още по-лесни <3
"""

full_screen = False # Преференций за пълен екран

if full_screen:
    pe.init((0, 0)) # Инициализираме PygameExtra със ширина 0 и височина 0, което е максималния размер
    w, h = pe.display.get_size() # Взимаме и си го запазваме този максимален размер
else:
    pe.init() # Инициализираме PygameExtra
    w, h = 700, 500 # Задаваме размери на екрана


offset_x = w//2 - h//2                   # Изместване на X
offset_y = 0                             # Изместване Y

board_size = 25                          # Размер на места в таблото
board_pixel_size = h // board_size       # Размер в пихели на едно място в таблото

time_in_milliseconds_till_movement = 120 # Колко време между да взима между местене на змията

temp = {}  # Временен речник за съхраняване на неща които често се ползват в кода
colors = { # Речник със цветовете които се ползват в играта
    'board outline': pe.colors.white,            # Цвета на очертаването на таблото
    'score color': pe.colors.white,              # Цвета на текста за точки
    'game over color': pe.colors.red,            # Цвета на текста за край на играта
    'game over background': pe.colors.black,     # Цвета на фона на текста за край на играта
    'pause color': pe.colors.white,              # Цвета на текста за пауза
    'snake color': pe.colors.green,              # Цвета на змията
    'snake color final': pe.colors.verydarkaqua, # Втория Цвят на змията
    'apple color': pe.colors.red                 # Цвета на ябълката
}

board: list                       # Казваме, че табото ни е от тип лист

snake_size: int                   # Тази променлива съхранява колко е дълфа змията
snake_direction: int              # Тази променлива съхранява на коя страна гледа змията
snake_begin_size = 3              # Тук си запазваме началния размер на змията, за да може да го ползваме после
snake_direction_change_chain = [] # Правим си лист за да може да запазваме когато играча натисне няколко бутана едно след друго

enable_teleport = True # Чрез тази променлива разрешаваме на змията да може да се телепортира от едната страна към другата вместо да губи играта
game_over = False      # Тази променлива индикира дали сме загубила играта :(
pause = False          # Тази променлива индикира, че играта е в пауза


def initialize_board(): # Като отделяме тази инициализация може да рестартираме играта когато играча загуби и иска да опита пак!
    global board, snake_size, snake_direction
    board = [[-2 for _ in range(board_size)] for _ in range(board_size)] # Правим вложен лист за таблото!
    # [print(*x) for x in board] # - ТОВА Е ЗА ДА СЕ ПРИНТИРА ТАБЛОТО ЗА ТЕСТВАНЕ
    board[board_size//3][board_size//2] = 1               # Индикираме, че на това място в таблото се намира змията
    board[board_size - board_size//3][board_size//2] = -1 # Индикираме, че на това място в таблото се намира ябълката

    snake_size = snake_begin_size   # Запазваме си колко дълга е змията
    snake_direction = 1             # Това може да го визуализираме като 0 когато е нагоре и 1 когато е на дясно и т.н.


def temp_calibrate():
    global temp
    temp['board outline rect'] = (offset_x, offset_y,            # Почваме от изместването
                                  board_size * board_pixel_size, # Смятаме размера на таблото
                                  board_size * board_pixel_size)
    temp['board outline width'] = h // 200                       # Смятаме ширината на очертаването
    temp['move time requirement'] = time_in_milliseconds_till_movement / 1000 # Смятаме нужното време за действие
    temp['score font size'] = int(w * .035)    # Правиме шрифта на точките да е .035 размера на ширината на екрана
    temp['score'] = pe.text.Text('0', 'font.ttf', temp['score font size'], (offset_x//2, temp['score font size']), [colors['score color'], None]) # Правиме текста за точките
    temp['game over font size'] = int((board_size * board_pixel_size) * .14) # Правиме шрифта на точките да е .14 размера на таблото
    temp['pause font size'] = int((board_size * board_pixel_size) * .14)     # Същото и за паузата
    temp['game over'] = pe.text.Text('GAME OVER', 'font.ttf', temp['game over font size'], (w//2, h//2), [colors['game over color'], colors['game over background']]) # Правиме тескта за край на играта
    temp['game over translucent'] = pe.text.Text('GAME OVER', 'font.ttf', temp['game over font size'], (w//2, h//2), [colors['game over color'], None])               # Правиме прозрачен тескт за край на играта
    temp['pause'] = pe.text.Text('PAUSED', 'font.ttf', temp['pause font size'], (w // 2, h // 2), [colors['pause color'], None]) # >>>                                # Прарим текста за паузата


def calculate_snake_color(snake_index, translucency):
    if snake_index == 1: # Ако индекса на змията е 1, тоест главата на змията
        return *colors['snake color'], translucency # Връщаме главния цвят със прозрачност
    snake_color_change = ( # Намираме разликите между двата цветове на змията
        colors['snake color final'][0] - colors['snake color'][0], # За червено
        colors['snake color final'][1] - colors['snake color'][1], # За зелено
        colors['snake color final'][2] - colors['snake color'][2]  # За синьо
    )
    percent_of_change = (snake_index / snake_size) # Смятаме колко да избледним между цветовете
    return (
        colors['snake color'][0] + snake_color_change[0] * percent_of_change, # За червено
        colors['snake color'][1] + snake_color_change[1] * percent_of_change, # За зелено
        colors['snake color'][2] + snake_color_change[2] * percent_of_change, # За синьо
        translucency                                                          # За прозрачност
    )


def draw_board(translucency):
    x = 0                 # Слагаме го да почне от първата колона в таблото
    x_in_pixel = offset_x # Слагаме x да е изместването на x
    y_in_pixel = offset_y # Слагаме y да е изместването на y
    while x < board_size: # Минаваме през колоните в таблото
        for index, y in enumerate(board[x]): # Минаваме през всички редове в тази колона
            if y == -1:                      # Ябълка е, рисуваме ябълка!!
                pe.draw.rect((*colors['apple color'], translucency), (x_in_pixel, y_in_pixel, board_pixel_size, board_pixel_size))
            elif 0 < y <= snake_size:        # Това е част от змията, рисуваме змия!!
                pe.draw.rect(calculate_snake_color(y, translucency), (x_in_pixel, y_in_pixel, board_pixel_size, board_pixel_size))
            y_in_pixel += board_pixel_size   # Увеличаваме y със размера на едно място в таблото
        x += 1                               # Следваща колона
        x_in_pixel += board_pixel_size       # Увеличаваме x със размера не едно място в таблото
        y_in_pixel = offset_y                # Връщаме y обратно към неговото изместване
    pe.draw.rect((*colors['board outline'], translucency), temp['board outline rect'], temp['board outline width'])  # Очертаваме таблото


def find_snake_head():
    for xi, x in enumerate(board):         # Минаваме през всяка колона в таблото
        for yi, y in enumerate(board[xi]): # Минаваме през всеки ред в тази колона
            if y == 1:                     # Ако е 1, това е главата на змията
                return xi, yi              # Връщаме къде се намира!


def generate_new_apple():
    xi, yi = find_snake_head() # Намираме къде е змията, за да предотвратим ябълката да е много близо до змията!
    new_xi, new_yi = xi, yi    # Слагаме позицията на ябълката където е змията, правейки го невалида позиция!
    # Правим няколко проверки в следния цикъл
    # 1. Ябълката още ли е в 2 места радиус от змията?
    # 2. Ябълката върху талото на змията ли е?
    while xi-2 <= new_xi <= xi+2 or yi-2 <= new_yi <= yi+2 or 1 <= board[new_xi][new_yi] <= snake_size:
        new_xi, new_yi = random.randint(0, board_size-1), random.randint(0, board_size-1) # Правим си случайна локация
    # Когато цикъла излеза значи, че проверките за минали и ябълката е точко където я искаме!
    board[new_xi][new_yi] = -1 # Слагаме новата локация на ябълката на таблото!


def get_next_snake_position():
    xi, yi = find_snake_head() # Намираме на змията главата

    # Сега трябва да я преместим змията
    if snake_direction == 0:   # Нагоре
        yi -= 1                # Махаме едно от y индекса, което е нагоре в нашия случай
    elif snake_direction == 1: # Надясно
        xi += 1                # Добавяме едно към x индекса, което е надясно
    elif snake_direction == 2: # Надолу
        yi += 1                # Добавяме едно към y индекса, което е надолу в нашия случай
    elif snake_direction == 3: # Наляво
        xi -= 1                # Махаме едно от x индекса, което е наляво

    # Сега трябва да потвърдим позицията
    if xi < 0:               # Змията е отишла твърде далече наляво
        xi = board_size-1    # > Отиваме на най-дясната точна
    elif xi >= board_size:   # Змията е отишла твърде далече надясно
        xi = 0               # > Отиваме на най-лявата точна
    elif yi < 0:             # Змията е отишла твърде далече нагоре
        yi = board_size-1    # > Отиваме на най-долната точна
    elif yi >= board_size:   # Змията е отишла твърде далече надолу
        yi = 0               # > Отиваме на най-горната точна
    else:
        return xi, yi, False # Връщаме позицията и False за да индикираме, че не е отишла твърде далече!
    return xi, yi, True      # Връщаме позицията и True за да индикираме, че е отишла твърде далече и се е телепортирала!


def move_snake():
    global game_over, snake_size, snake_direction

    if len(snake_direction_change_chain) > 0:                          # Проверяваме дали има верига от посоки
        snake_direction = snake_direction_change_chain.pop(0)          # Взимаме първото нещо

    next_xi, next_yi, teleported = get_next_snake_position()           # Взимаме следващата локация на змията и дали се е телепортирала

    for xi, x in enumerate(board):                                     # Минаваме през всяка колона в таблото
        board[xi] = [value + 1 if value > 0 else value for value in x] # Добавяме 1 ако е по-голямо от 0

    if teleported and not enable_teleport:          # Змията се е телепортирала и това не е разрешено
        game_over = True                            # > Край на играта
    elif 1 < board[next_xi][next_yi] <= snake_size: # Ако змията се охапала сама
        game_over = True                            # > Край на играта
    else:                                           # Змията не е нарушила правилата ни
        if board[next_xi][next_yi] == -1:           # > Змията е изяла ябълка!
            snake_size += 1                         # >> РАЗТЕМ!
            board[next_xi][next_yi] = 1             # >> Съхраняваме новите координати преди да генерираме нова ябълка
            generate_new_apple()                    # >> Генерираме нова ябълка някъде на таблото
        else:
            board[next_xi][next_yi] = 1             # Слагаме новите координати да са 1, дамек главата на змията


def update_score_text():
    string = str(snake_size-snake_begin_size) # Стойноста която брояча на точки трябва да съхранява
    if temp['score'].text != string:          # Проверяваме стойноста
        temp['score'].text = string           # Слагаме стойноста
        temp['score'].init()                  # Повторно инициализираме текста


def event_handler():
    global snake_direction, pause, game_over
    pe.event.quitcheckauto() # Излез ако е натиснат X бутона

    new_snake_direction = -1 # Инициализираме нова посока дори да не я знаем дали ще я получим още

    if pe.event.key_DOWN(pe.pygame.K_LEFT) or pe.event.key_DOWN(pe.pygame.K_a):       # Натиснато е left
        new_snake_direction = 3                                                       # > Обновяваме новата посока да е наляво
    elif pe.event.key_DOWN(pe.pygame.K_RIGHT) or pe.event.key_DOWN(pe.pygame.K_d):    # Натиснато е right
        new_snake_direction = 1                                                       # > Обновяваме новата посока да е надясно
    if pe.event.key_DOWN(pe.pygame.K_DOWN) or pe.event.key_DOWN(pe.pygame.K_s):       # Натиснато е down
        new_snake_direction = 2                                                       # > Обновяваме новата посока да е надолу
    elif pe.event.key_DOWN(pe.pygame.K_UP) or pe.event.key_DOWN(pe.pygame.K_w):       # Натиснато е up
        new_snake_direction = 0                                                       # > Обновяваме новата посока да е нагоре
    if pe.event.key_DOWN(pe.pygame.K_ESCAPE) or pe.event.key_DOWN(pe.pygame.K_SPACE): # Натиснато е ESC или интервал
        if game_over:          # Ако играта е свършила и играча е натиснал един от бутоните
            initialize_board() # Започни отново играта
            game_over = False  # Вече не е свършила все пак
            return             # Връщаме
        pause = not pause      # Иначе пауза или излизаме от пауза

    if new_snake_direction < 0 or game_over: return # Връщаме защото няма друго за правене

    old_snake_direction = snake_direction           # Запазваме старата посока

    if len(snake_direction_change_chain) > 0: # Проверяваме дали има нещо във веригата със посоки
        # Проверяваме дали последната посока във веригата е същата посока като новата посока
        if snake_direction_change_chain[len(snake_direction_change_chain) - 1] == new_snake_direction:
            return
    else:
        # Проверяваме дали текущата посока е същата посока като новата посока
        if snake_direction == new_snake_direction:
            return

    if len(snake_direction_change_chain) > 0: # Проверяваме дали има нещо във веригата със посоки
        snake_direction = snake_direction_change_chain[len(snake_direction_change_chain)-1]  # Слагаме следващата посока
    else:                                                                                    #
        snake_direction = new_snake_direction                                                # Слагаме следващата посока
    xi, yi, _ = get_next_snake_position()                        # Взимаме следващата позиция на змята
    snake_direction = old_snake_direction                        # Връщаме посоката както си беше
    if board[xi][yi] != 2:                                       # Ако змята не се обръща върху себе си
        snake_direction_change_chain.append(new_snake_direction) # добавяме посоката към веригата със посоки


initialize_board() # Инициализираме таблото
temp_calibrate()   # Смятаме временните стойности
delta_time = 0     # Слагаме начална стойност за delta time
pre_delta_time = 0 # Слагаме начална стойност за предишния delta time
await_move = 0     # Слагаме начална стойност за времето за реакция

# Правим си екран ползвайки променливите за ширина, дължина и дали да е на пълен екран
pe.display.make((w, h), "Лесна Змия", pe.display.DISPLAY_MODE_FULLSCREEN if full_screen else pe.display.DISPLAY_MODE_NORMAL)

while True:
    t = pe.pygame.time.get_ticks()                     # Взимаме си тиковете
    [event_handler() for pe.event.c in pe.event.get()] # Оправяме си събитията
    pe.fill.full(pe.colors.black)                      # Изчистваме екрана със черно

    temp['score'].display()                     # Рисуваме точките
    draw_board(150 if pause else 255)           # Рисуваме таблото, ако играта е на пауза го правим прозрачно
    if not pause and not game_over and await_move >= temp['move time requirement']: # Проверяваме, че играта още тече и е време за реакция!
        move_snake()                            # > Местим змията
        await_move = 0                          # > Връщаме времето за реакция обратно на 0
    elif pause:                                 # Време за почивка :)
        temp['pause'].display()                 # > Рисуваме текста за пауза на екрана
    elif game_over:                             # Играта свърши?!
        temp['game over'].display()             # Рисуваме КРАЙ НА ИГРАТА!
        draw_board(150)                         # Рисуваме отново таблото но по-прозрачно
        temp['game over translucent'].display() # Рисуваме прозрачнотия КРАЙ НА ИГРАТА!
        # Желания ефект е, че изглежда сякаш нещата зад текста са малко избледняла за да направят текста по четим
    else:
        await_move += delta_time             # Добавяме delta към времето за реакция

    update_score_text()                      # Актуализираме текста за точки в случай, че змията е пораснала!

    delta_time = (t - pre_delta_time) / 1000 # Задаваме си delta
    pe.display.update()                      # Актуализираме дисплея
    pre_delta_time = t                       # Задаваме стария delta