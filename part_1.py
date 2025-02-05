from colorama import Fore, Style

# Цвет для неиспользованной ячейки
DEFAULT_COLOR = Fore.BLACK

# Список цветов для найденных слов
WORD_COLORS = [Fore.RED, Fore.GREEN, Fore.YELLOW, Fore.BLUE, Fore.MAGENTA, Fore.CYAN]

class Cell:
    def __init__(self, letter, x, y,  color=DEFAULT_COLOR):
        self.letter = letter.lower()
        self.x = x
        self.y = y
        self.is_used = False  # Флаг использования в слове
        self.color = color  # Цвет буквы

    def mark_used(self, color_index: int):
        """Помечает ячейку как использованную и изменяет её цвет."""
        self.is_used = True
        self.color = WORD_COLORS[color_index]

    def reset(self):
        """Сбрасывает состояние ячейки."""
        self.is_used = False
        self.color = DEFAULT_COLOR

    def __repr__(self):
        return f"Cell({self.letter}, {self.x}, {self.y}, used={self.is_used}, color={self.color})"


class Board:
    def __init__(self, letter_rows, dictionary_file="russian_nouns.txt"):
        """
        Инициализирует игровое поле.
        :param letter_rows: список строк, каждая из которых содержит буквы
        :param dictionary_file: путь к файлу со списком русских существительных
        """
        self.grid = [[Cell(letter, x, y) for x, letter in enumerate(row)] for y, row in enumerate(letter_rows)]
        self.dictionary = self.load_dictionary(dictionary_file)
        self.width = len(letter_rows[0]) if letter_rows else 0
        self.height = len(letter_rows)

    def load_dictionary(self, filename):
        """Считывает список слов из файла и возвращает их в виде множества."""
        try:
            with open(filename, "r", encoding="utf-8") as file:
                return set(word.strip().lower() for word in file)
        except FileNotFoundError:
            print(f"Файл {filename} не найден.")
            return set()

    def get_cell(self, x, y):
        """Возвращает ячейку по координатам."""
        if 0 <= y < len(self.grid) and 0 <= x < len(self.grid[y]):
            return self.grid[y][x]
        return None

    def display(self):
        """Выводит игровое поле на экран с цветами найденных слов."""
        for row in self.grid:
            print(" ".join(cell.color + cell.letter.upper() + Style.RESET_ALL for cell in row))

    def __repr__(self):
        """Возвращает строковое представление игрового поля."""
        return "\n".join(" ".join(cell.letter.upper() for cell in row) for row in self.grid)


class WordPath:
    def __init__(self, board, start_x, start_y):
        """
        Инициализирует объект WordPath.
        :param board: Игровое поле (Board)
        :param start_x: Начальная координата X
        :param start_y: Начальная координата Y
        """
        self.board = board  # Ссылка на игровое поле
        self.cells = [board.get_cell(start_x, start_y)] if board.get_cell(start_x, start_y) else []
        self.dictionary = board.dictionary  # Словарь допустимых слов

    def add_cell(self, x, y):
        """Добавляет ячейку в путь слова по координатам."""
        cell = self.board.get_cell(x, y)
        if cell:
            self.cells.append(cell)

    def get_word(self):
        """Возвращает слово, составленное из букв ячеек."""
        return "".join(cell.letter for cell in self.cells)

    def is_valid(self):
        """Проверяет, является ли слово допустимым."""
        return self.get_word() in self.dictionary

    def highlight_word(self, color=Fore.RED):
        """Подсвечивает найденное слово цветом."""
        for cell in self.cells:
            cell.set_color(color)

    def reset(self):
        """Очищает путь слова."""
        self.cells.clear()

    def __repr__(self):
        """Возвращает строковое представление объекта."""
        return f"WordPath({self.get_word()}, valid={self.is_valid()})"


# Тестовый пример
if __name__ == "__main__":
    test_letters = [
        "РИЛО",
        "КАВТ",
        "ЭРАЙ",
        "ХОЛА"
    ]

    board = Board(test_letters)
    print("Игровое поле:")
    board.display()

    print("\nЯчейка (1,1):", board.get_cell(1, 1))
