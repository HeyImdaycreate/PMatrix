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
    curses.curs_set(0)          
    stdscr.nodelay(True)        
    stdscr.timeout(0)
    
    curses.start_color()
    
    # Получаем цвет из словаря, если что-то пойдет не так — берем зеленый
    chosen_color = COLOR_MAP.get(target_color_name, curses.COLOR_GREEN)
    
    # Инициализируем пару цветов: 1 — выбранный цвет, 2 — белая "голова"
    curses.init_pair(1, chosen_color, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_WHITE, curses.COLOR_BLACK) 
    
    symbols = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz$+-*/%=<>!:"
    height, width = stdscr.getmaxyx()
    columns = [[-1, random.randint(1, 3), random.randint(5, height - 5)] for _ in range(width - 1)]

    while True:
        key = stdscr.getch()
        if key == ord('q') or key == 27: 
            break

        new_height, new_width = stdscr.getmaxyx()
        if new_height != height or new_width != width:
            height, width = new_height, new_width
            columns = [[-1, random.randint(1, 3), random.randint(5, height - 5)] for _ in range(width - 1)]
            stdscr.clear()

        for x in range(min(width - 1, len(columns))):
            curr_y, speed, length = columns[x]

            if curr_y == -1:
                if random.random() < 0.02: 
                    columns[x][0] = 0 # Стартуем только координату Y
                continue

            erase_y = curr_y - length
            if 0 <= erase_y < height:
                stdscr.addch(erase_y, x, ' ')

            if 0 <= curr_y < height:
                char = random.choice(symbols)
                if random.random() < 0.15:
                    stdscr.addch(curr_y, x, char, curses.color_pair(2) | curses.A_BOLD)
                else:
                    stdscr.addch(curr_y, x, char, curses.color_pair(1))

            # ИСПРАВЛЕНО: Увеличиваем только координату Y внутри списка, а не весь элемент
            columns[x][0] += 1

            if columns[x][0] - length >= height:
                columns[x] = [-1, random.randint(1, 3), random.randint(5, height - 5)]

        stdscr.refresh()
        time.sleep(0.05)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Python Matrix Effect (CMatrix Clone)")
    
    parser.add_argument(
        '-color', '--color',
        choices=['green', 'red', 'blue', 'cyan', 'yellow', 'magenta', 'white', 'black'],
        default='green',
        help='Цвет падающих символов (по умолчанию: green).'
    )
    
    args = parser.parse_args()

    try:
        curses.wrapper(matrix_effect, args.color)
    except KeyboardInterrupt:
        pass
