from colorama import Fore, Style
from itertools import cycle


# Цвет для неиспользованной ячейки
DEFAULT_COLOR = Fore.BLACK

# Список цветов для найденных слов
WORD_COLORS = [Fore.RED, Fore.GREEN, Fore.YELLOW, Fore.BLUE, Fore.MAGENTA, Fore.CYAN]


class Cell:
    """ Ячейка игрового поля """
    def __init__(self, letter, x, y):
        self.letter = letter.lower()
        self.x = x
        self.y = y
        self.color = DEFAULT_COLOR

    def set_color(self, color):
        """ Установка цвета ячейки """
        self.color = color

    def __repr__(self):
        return f'Cell({self.letter}, {self.x}, {self.y})'

class Board:
    """ Игровое поле """

    def __init__(self, letter_rows, dictionary_file='russian_nouns.txt'):
        """ Инициализация игрового поля """
        self.grid = [[Cell(letter, x, y) for x, letter in enumerate(row)] for y, row in enumerate(letter_rows)]
        self.dictionary = self.load_dictionary(dictionary_file)
        self.width = len(letter_rows[0]) if letter_rows else 0
        self.height = len(letter_rows)
        self.existing_paths = set()  # множество кортежей координат ячеек проверяемых слов


    def load_dictionary(self, filename):
        """ Загрузка словаря слов """
        try:
            with open(filename, 'r', encoding='utf-8') as file:
                return set(word.strip().lower() for word in file if len(word.strip()) >= 3)
        except FileNotFoundError:
            print(f'Файл {filename} не найден.')
            return set()

    def get_cell(self, x, y):
        """ Получение ячейки по координатам """
        if 0 <= y < self.height and 0 <= x < self.width:
            return self.grid[y][x]
        return None  # Вывод, если ячейка находится за границами игрового поля

    def display(self):
        """ Вывод игрового поля """
        for row in self.grid:
            print(' '.join(cell.color + cell.letter.upper() + Style.RESET_ALL for cell in row))


class WordPath:
    """ Путь ячеек слова на игровом поле """
    def __init__(self, board, cells):
        """ Инициализация """
        self.board = board
        self.cells = cells
        self.dictionary = board.dictionary

    def get_word(self):
        """ Возвращает строковое представление """
        return ''.join(cell.letter for cell in self.cells)

    def is_valid(self):
        """ Проверка слова в прямом и обратном направлении"""
        word = self.get_word()
        if word in self.dictionary:
            return 1
        if word[::-1] in self.dictionary:
            return 2

    def filter_dictionary(self):
        """ Фильтрация словаря """
        word = self.get_word()
        self.dictionary = {w for w in self.dictionary if word in w or word[::-1] in w}

    def get_adjacent_free_cells(self, begin=True):
        """ Возвращает свободные соседние ячейки прилежащих к началу или к концу слову """
        free_cells = []  # Список свободных ячеек
        if not self.cells:
            return free_cells
        cell = self.cells[0] if begin else self.cells[-1]  # Первая или последняя ячейка, вокруг которой ищутся свободные ячейки
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # Список направлений поиска свободных ячеек

        for dx, dy in directions:
            adjacent = self.board.get_cell(cell.x + dx, cell.y + dy)
            if adjacent and adjacent.color == DEFAULT_COLOR and adjacent not in self.cells:
                free_cells.append(adjacent)

        return free_cells

    def expand_paths(self):
        """ Построение списка производных слов """
        new_paths = []  # Список производных слов

        for begin in [True, False]:  # Поиск свободных ячеек, прилежащих к началу или концу слова
            free_cells = self.get_adjacent_free_cells(begin)  # Список свободных ячеек
            for cell in free_cells:
                # Добавление ячейки к слову с начала или с конца
                new_cells = [cell] + self.cells if begin else self.cells + [cell]
                path_tuple = tuple((c.x, c.y) for c in new_cells)  # Координаты кортежа ячеек
                reverse_tuple = path_tuple[::-1]  # Координаты обратного кортежа ячеек

                # Проверка уникальности кортежа ячеек в прямом и обратном направлении
                if path_tuple not in self.board.existing_paths and reverse_tuple not in self.board.existing_paths:
                    new_paths.append(WordPath(self.board, new_cells))  # Добавление производного слова
                    self.board.existing_paths.add(path_tuple)  # Добавление уникального кортежа ячеек

        return new_paths

    def __repr__(self):
        return f"WordPath('word={self.get_word()}, cells={self.cells})"

def find_words(board, start_cells):
    """ Поиск слов на игровом поле """
    found_words = []  # Список найденных слов

    path = WordPath(board, [start_cells]) # Создаем слово для начальной ячейки
    paths = [path]  # включаем в список поисковых слов

    while paths:  # список поисковых слов не пуст
        current_path = paths.pop()  # извлекаем слово из конца списка
        if len(current_path.cells) >= 3: # Игнорируем слова, которые содержат меньше 3 букв
            current_path.filter_dictionary()  # Обновляем множество подходящих слов

        if not current_path.dictionary:  # Если множество подходящих слов пустое
            continue  # Переходим к началу цикла

        if directions := current_path.is_valid(): # Проверка слова в прямом и обратном направлении
            if directions == 2:  # Если слова содержится в словаре в обратном направлении, то переворачиваем список ячеек
                current_path.cells.reverse()
            found_words.append(current_path)  # Добавим слово в список найденных слов

        paths.extend(current_path.expand_paths())  # Расширяем список поисковых слов

    return found_words

def get_words(board, progress=False):
    result = []
    for x in range(board.width):
        for y in range(board.height):
            start_cell = board.get_cell(x, y)  # Получение ячейки с заданными координатами
            words = find_words(board, start_cell)  # Запуск функции Поиска слов на игровом поле
            result.extend(words)
            if progress:  # Если нужно отразить прогресса
                print('. ', end='')
        if progress:  # Если нужно отразить прогресса
            print()
    return result


# Тестовый пример
if __name__ == '__main__':
    # Данные для создания игрового поля
    test_board = [
        "убльза",
        "зиипир",
        "лнглза",
        "ааьошм",
        "донкои",
        "далоад"
    ]

    # Создание и отображение игрового поля
    board = Board(test_board)
    board.display()

    print("\nПолучаем список слов")
    words = get_words(board, progress=True)

    print('\nВывод результата')
    for word in sorted(words, key=lambda x: (-len(x.get_word()), x.get_word())):
        print(word.get_word(), end=', ')
    
