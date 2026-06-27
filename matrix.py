import os
import random
import time
import curses
import argparse

# Словарь для сопоставления текстовых аргументов с цветами curses
COLOR_MAP = {
    'green': curses.COLOR_GREEN,
    'red': curses.COLOR_RED,
    'blue': curses.COLOR_BLUE,
    'cyan': curses.COLOR_CYAN,
    'yellow': curses.COLOR_YELLOW,
    'magenta': curses.COLOR_MAGENTA,
    'white': curses.COLOR_WHITE,
    'black': curses.COLOR_BLACK
}

def matrix_effect(stdscr, target_color_name):
    # Настройки терминала
    curses.curs_set(0)          # Прячем мигающий курсор
    stdscr.nodelay(True)        # Не блокируем поток в ожидании нажатия клавиш
    stdscr.timeout(0)
    
    curses.start_color()
    
    # Определяем основной цвет. Если передан неверный — берем зеленый
    chosen_color = COLOR_MAP.get(target_color_name, curses.COLOR_GREEN)
    
    # Инициализируем цветовые пары: 
    # 1 — цвет темы на черном фоне
    # 2 — белый цвет для светящейся "головы" потока
    curses.init_pair(1, chosen_color, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_WHITE, curses.COLOR_BLACK) 
    
    # Символы цифрового дождя (ASCII, которые точно отобразит любая Windows-консоль)
    symbols = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz$+-*/%=<>!:"
    
    height, width = stdscr.getmaxyx()
    
    # Структура списка потоков: [текущий_y, скорость, длина_потока]
    # Если текущий_y == -1, значит столбец ожидает старта
    columns = [[-1, random.randint(1, 3), random.randint(5, height - 5)] for _ in range(width - 1)]

    while True:
        # Считываем нажатие клавиш для выхода
        key = stdscr.getch()
        if key == ord('q') or key == 27: # Выход по 'q' или Esc
            break

        # Проверка изменения размеров окна консоли на лету
        new_height, new_width = stdscr.getmaxyx()
        if new_height != height or new_width != width:
            height, width = new_height, new_width
            columns = [[-1, random.randint(1, 3), random.randint(5, height - 5)] for _ in range(width - 1)]
            stdscr.clear()

        for x in range(min(width - 1, len(columns))):
            curr_y, speed, length = columns[x]

            # Если поток спит, даем ему шанс 2% активироваться на этом кадре
            if curr_y == -1:
                if random.random() < 0.02: 
                    columns[x][0] = 0 # Задаем стартовый Y = 0
                continue

            # 1. Стираем символ на хвосте потока
            erase_y = curr_y - length
            if 0 <= erase_y < height:
                stdscr.addch(erase_y, x, ' ')

            # 2. Рисуем текущий символ на позиции Y
            if 0 <= curr_y < height:
                char = random.choice(symbols)
                # 15% шанс сделать символ белым и жирным ("светящаяся голова")
                if random.random() < 0.15:
                    stdscr.addch(curr_y, x, char, curses.color_pair(2) | curses.A_BOLD)
                else:
                    stdscr.addch(curr_y, x, char, curses.color_pair(1))

            # Продвигаем координату Y конкретного столбца вниз
            columns[x][0] += 1

            # Если весь поток (вместе с хвостом) скрылся за экраном — сбрасываем его
            if columns[x][0] - length >= height:
                columns[x] = [-1, random.randint(1, 3), random.randint(5, height - 5)]

        stdscr.refresh()
        time.sleep(0.05) # Задержка обновления экрана (скорость анимации)

if __name__ == "__main__":
    # Парсер аргументов командной строки
    parser = argparse.ArgumentParser(description="Python Matrix Effect (CMatrix Clone for Windows)")
    
    parser.add_argument(
        '-color', '--color',
        choices=['green', 'red', 'blue', 'cyan', 'yellow', 'magenta', 'white', 'black'],
        default='green',
        help='Цвет падающих символов (по умолчанию: green).'
    )
    
    args = parser.parse_args()

    try:
        # Безопасный запуск curses-приложения с передачей выбранного цвета
        curses.wrapper(matrix_effect, args.color)
    except KeyboardInterrupt:
        pass
