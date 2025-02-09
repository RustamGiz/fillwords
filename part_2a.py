from colorama import Fore, Style


# Цвет для неиспользованной ячейки
DEFAULT_COLOR = Fore.BLACK

# Список цветов для найденных слов
WORD_COLORS = [Fore.RED, Fore.GREEN, Fore.YELLOW, Fore.BLUE, Fore.MAGENTA, Fore.CYAN]


class Cell:

    def __init__(self, letter, x, y):
        self.letter = letter.lower()
        self.x = x
        self.y = y
        self.color = DEFAULT_COLOR

    def set_color(self, color):
        self.color = color

    def __repr__(self):
        return f'Cell({self.letter}, {self.x}, {self.y})'


class Board:
    def __init__(self, letter_rows, dictionary_file='russian_nouns.txt'):
        self.grid = [[Cell(letter, x, y) for x, letter in enumerate(row)] for y, row in enumerate(letter_rows)]
        self.dictionary = self.load_dictionary(dictionary_file)
        self.width = len(letter_rows[0]) if letter_rows else 0
        self.height = len(letter_rows)
        self.count = 0
        self.failed_cell = []

    def load_dictionary(self, filename):
        try:
            with open(filename, 'r', encoding='utf-8') as file:
                return set(word.strip().lower() for word in file if len(word.strip()) >= 3)
        except FileNotFoundError:
            print(f'Файл {filename} не найден.')
            return set()

    def get_cell(self, x, y):
        if 0 <= y < self.height and 0 <= x < self.width:
            return self.grid[y][x]
        return None

    def get_top_left_free_cell(self):
        for y in range(self.height):
            for x in range(self.width):
                cell = self.grid[y][x]
                if cell.color == DEFAULT_COLOR and cell not in self.failed_cell:
                    return cell
        return None

    def display(self):
        for row in self.grid:
            print(' '.join(cell.color + cell.letter.upper() + Style.RESET_ALL for cell in row))


class WordPath:
    def __init__(self, board, cells):
        self.board = board
        self.cells = cells
        self.dictionary = board.dictionary

    def get_word(self):
        return ''.join(cell.letter for cell in self.cells)

    def is_valid(self):
        word = self.get_word()
        if word in self.dictionary:
            return 1
        if word[::-1] in self.dictionary:
            return 2


    def filter_dictionary(self):
        word = self.get_word()
        self.dictionary = {w for w in self.dictionary if word in w or word[::-1] in w}

    def get_adjacent_free_cells(self, begin=True):
        free_cells = []
        if not self.cells:
            return free_cells
        cell = self.cells[0] if begin else self.cells[-1]
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

        for dx, dy in directions:
            adjacent = self.board.get_cell(cell.x + dx, cell.y + dy)
            if (adjacent and adjacent.color == DEFAULT_COLOR and adjacent not in self.cells):
                free_cells.append(adjacent)

        return free_cells

    def expand_paths(self):
        new_paths = []
        existing_paths = set()

        for begin in [True, False]:
            free_cells = self.get_adjacent_free_cells(begin)
            for cell in free_cells:
                new_cells = [cell] + self.cells if begin else self.cells + [cell]
                path_tuple = tuple((c.x, c.y) for c in new_cells)
                reverse_tuple = path_tuple[::-1]

                if path_tuple not in existing_paths and reverse_tuple not in existing_paths:
                    new_paths.append(WordPath(self.board, new_cells))
                    existing_paths.add(path_tuple)

        return new_paths

    def highlight_word(self, color=Fore.RED):
        for cell in self.cells:
            cell.set_color(color)


def find_words(board, start_cell):
    found_words = []

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
        'дранетс',
        'нахьваа',
        'негироб',
        'рвинпри',
        'авакмуд',
        'котплан',
        'сикозре'
    ]

    board = Board(test_board)
    board.display()

    start_cell = board.get_top_left_free_cell()

    while True:
        words = find_words(board, start_cell)
        print(f'Координаты ячейки: {start_cell.x} {start_cell.y}')
        if not words:
            print('\nНет подходящих слов.')
            board.failed_cell.append(start_cell)
            start_cell = board.get_top_left_free_cell()
            continue
        print('\nНайденные слова:')
        for word in sorted(words, key=lambda x: len(x.get_word()), reverse=True):
            print(word.get_word())
            word.highlight_word(WORD_COLORS[board.count % len(WORD_COLORS)])
            board.display()
            print()
            result = input('Слово подходит? (y/n): ').strip().lower()
            if result == 'y':
                board.count += 1
                start_cell = board.get_top_left_free_cell()
                break

            word.highlight_word(DEFAULT_COLOR)
        else:
            print('\nНет подходящих слов.')
            x, y = map(int, input('Введите координаты свободной ячейки (x y): ').split())
            start_cell = board.get_cell(x, y)

        if not start_cell:
            break

    print('\nГоловоломка закончена!')
    print('\nКоличество найденных слов:', board.count)