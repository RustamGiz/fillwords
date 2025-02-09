from colorama import Fore, Style


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


class Board:
    """ Игровое поле """

    def __init__(self, letter_rows, dictionary_file='russian_nouns.txt'):
        """ Инициализация игрового поля """
        self.grid = [[Cell(letter, x, y) for x, letter in enumerate(row)] for y, row in enumerate(letter_rows)]
        self.dictionary = self.load_dictionary(dictionary_file)
        self.width = len(letter_rows[0]) if letter_rows else 0
        self.height = len(letter_rows)
        self.count = 0
        self.failed_cell = []

    def load_dictionary(self, filename):
        """ Загрузка словаря """
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
        """ Проверка слова """
        word = self.get_word()
        return word in self.dictionary


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
            if (adjacent and adjacent.color == DEFAULT_COLOR and adjacent not in self.cells):
                free_cells.append(adjacent)

        return free_cells

    def expand_paths(self):
        new_paths = []  # Список производных слов
        existing_paths = set()  # Множество кортежей координат ячеек

        for begin in [True, False]:  # Поиск свободных ячеек, прилежащих к началу или концу слова
            free_cells = self.get_adjacent_free_cells(begin)  # Список свободных ячеек
            for cell in free_cells:
                # Добавление ячейки к слову с начала или с конца
                new_cells = [cell] + self.cells if begin else self.cells + [cell]
                path_tuple = tuple((c.x, c.y) for c in new_cells)  # Координаты кортежа ячеек
                reverse_tuple = path_tuple[::-1]  # Координаты обратного кортежа ячеек

                # Проверка уникальности кортежа ячеек в прямом и обратном направлении
                if path_tuple not in existing_paths and reverse_tuple not in existing_paths:
                    new_paths.append(WordPath(self.board, new_cells))  # Добавление производного слова
                    existing_paths.add(path_tuple)  # Добавление уникального кортежа ячеек

        return new_paths

    def highlight_word(self, color=Fore.RED):
        """ Выделение ячеек цепочки cells слова цветом"""
        for cell in self.cells:
            cell.set_color(color)


def find_words(board, start_cell):
    """ Поиск слов на игровом поле """
    found_words = []  # Список найденных слов

    path = WordPath(board, [start_cell])
    paths = [path]
    existing_paths = set()

    while paths:
        current_path = paths.pop()
        current_path.filter_dictionary()

        if directions := current_path.is_valid():
            path_tuple = tuple((c.x, c.y) for c in current_path.cells)
            reverse_tuple = path_tuple[::-1]

            if path_tuple not in existing_paths and reverse_tuple not in existing_paths:
                existing_paths.add(path_tuple)
                if directions == 2:
                    current_path.cells.reverse()
                found_words.append(current_path)

        if current_path.dictionary:
            paths.extend(current_path.expand_paths())

    return found_words


if __name__ == '__main__':
    test_board = [
        "РИЛО",
        "КАВТ",
        "ЭРАЙ",
        "ХОЛА"
    ]

    board = Board(test_board)
    board.display()

    start_cell = board.get_cell(2, 1)

    words = find_words(board, start_cell)

    print('\nНайденные слова:')
    for word in sorted(words, key=lambda x: len(x.get_word()), reverse=True):
        print(word.get_word())
