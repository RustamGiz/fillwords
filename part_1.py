from colorama import Fore, Style

# Цвет для незанятой ячейки
DEFAULT_COLOR = Fore.BLACK

# Список цветов для найденных слов
WORD_COLORS = [Fore.RED, Fore.GREEN, Fore.YELLOW, Fore.BLUE, Fore.MAGENTA, Fore.CYAN]


class Cell:
    """ Ячейка игрового поля """

    def __init__(self, letter, x, y):
        """Инициализация ячейки"""
        self.letter = letter.lower()
        self.x = x
        self.y = y
        self.color = DEFAULT_COLOR

    def set_color(self, color):
        """Установка цвета ячейки"""
        self.color = color


class Board:
    """ Игровое поле """

    def __init__(self, letter_rows, dictionary_file='russian_nouns.txt'):
        """ Инициализация игрового поля """
        self.grid = [[Cell(letter, x, y) for x, letter in enumerate(row)] for y, row in enumerate(letter_rows)]
        self.dictionary = self.load_dictionary(dictionary_file)
        self.width = len(letter_rows[0]) if letter_rows else 0
        self.height = len(letter_rows)

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
        return None

    def display(self):
        """ Вывод игрового поля """
        for row in self.grid:
            print(' '.join(cell.color + cell.letter.upper() + Style.RESET_ALL for cell in row))


# Тестовый пример
if __name__ == "__main__":
    # Элементы поля. Символы в строках соответствуют строкам игрового поля
    test_letters = [
        "РИЛО",
        "КАВТ",
        "ЭРАЙ",
        "ХОЛА"
    ]

    # Проверка правильности заполнения и вывода поля
    board = Board(test_letters)
    print("Чистое поле:")
    board.display()

    # Проверка правильности заполнения ячеек игрового поля и их отображения при выводе
    cells = ((0, 0), (1, 0), (2, 0), (0, 1), (1, 1))
    for cell in cells:
        board.get_cell(*cell).set_color(WORD_COLORS[0])  # 0 -раскрашивает ячейки в красный цвет (Fore.RED)
    print("\nЗаполнено одно слово:")
    board.display()
