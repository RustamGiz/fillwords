from colorama import Fore, Style
from itertools import cycle


# Цвет для неиспользованной ячейки
DEFAULT_COLOR = Fore.BLACK

# Список цветов для найденных слов
WORD_COLORS = [Fore.RED, Fore.GREEN, Fore.YELLOW, Fore.BLUE, Fore.MAGENTA, Fore.CYAN]

# Итератор для циклического перебора цветов
COLOR_CYCLE = cycle(WORD_COLORS)

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

    def fill_color(self, color):
        """ Заполняет все ячейки слова заданным цветом """
        for cell in self.cells:
            cell.set_color(color)

    def reset_color(self):
        """ Присваивает ячейкам цвет по умолчанию """
        for cell in self.cells:
            cell.set_color(DEFAULT_COLOR)

    def is_free(self):
        """ Проверяет, что все ячейки свободны """
        return all(cell.color == DEFAULT_COLOR for cell in self.cells)

    def __repr__(self):
        return f"WordPath('word={self.get_word()}, cells={self.cells})"

def find_words(board, start_cells):
    """ Поиск слов для заданной ячейки на игровом поле """
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
    """ Поиск всех слов на игровом поле"""
    result = []
    for x in range(board.width):
        for y in range(board.height):
            start_cell = board.get_cell(x, y)  # Получение ячейки с заданными координатами
            words = find_words(board, start_cell)  # Запуск функции Поиска слов на игровом поле
            result.extend(words)
            if progress:  # Если нужно отразить прогресс работы функции
                print('. ', end='')
        if progress:  # Если нужно отразить прогресс работы функции
            print()
    return result


def backtracking_fill(board, word_paths):
    """
    Поиск полного покрытия игрового поля с помощью алгоритма поиска с возвратом.
    Возвращает итоговый список со словами или None.
    """

    # Базовый случай
    # Проверяем, все ли ячейки заняты
    if all(cell.color != DEFAULT_COLOR for row in board.grid for cell in row):
        return []

    # Для каждого доступного слова (word_path) в списке word_paths.
    for i in range(len(word_paths)):
        word_path = word_paths[i]

        word_path.fill_color(WORD_COLORS[1])  # Слово добавляется на поле
        # Отбираются только те слова, которые можно разместить на оставшихся свободных ячейках.
        next_word_paths = [wp for wp in word_paths[i + 1:] if wp.is_free()]

        # Рекурсивный вызов
        result = backtracking_fill(board, next_word_paths)

        # Проверка результата, если текущий выбор слова оказался неправильным
        if result is None:
            word_path.reset_color()  # Слово убирается с поля
            continue # Переходим к следующему слову

        # решение найдено
        result = [word_path] + result
        word_path.reset_color()  # Слово убирается с поля
        return result

    # Проверили все слова, но ни один не подошел
    return None

# Тестовый пример
if __name__ == '__main__':
    test_board = [
        "РИЛО",
        "КАВТ",
        "ЭРАЙ",
        "ХОЛА"
    ]
    # Данные для создания игрового поля
    test_board = [
        "еразалс",
        "тдалвоо",
        "яьещирк",
        "хратром",
        "инукесб",
        "пдарави",
        "елагило"
    ]

    # Создание и отображение игрового поля
    board = Board(test_board)
    print('Игровое поле:')
    board.display()

    words = get_words(board, progress=True)
    # Сортируем слова в порядке убывания их длины
    words = [word for word in sorted(words, key=lambda x: (-len(x.get_word(),)))]


    print('\nВывод результата')
    print('Всего слов:', len(words))
    words_list = [word.get_word() for word in words]
    print(*words_list, sep=', ')

    # Ищем решение
    solution = backtracking_fill(board, words)

    if solution: # Если решение найдено
        # Выводим результат
        print('\nИгровое поле можно заполнить следующими словами:')
        for word_path in solution:
            color = next(COLOR_CYCLE)
            print(color + word_path.get_word() + Style.RESET_ALL)

            word_path.fill_color(color)  # Окрашиваем найденное решение

        print("\nРешение:")
        board.display()
    else:
        print("\nИгровое поле заполнить не удалось.")
    
