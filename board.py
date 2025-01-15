class Cell:
    def __init__(self, letter):
        """
        Инициализация ячейки с буквой.
        :param letter: Буква, которая будет храниться в ячейке.
        """
        self.letter = letter  # Буква в ячейке
        self.is_used = False  # Флаг, что ячейка уже используется в отгаданном слове
        self.is_active = False  # Флаг, что ячейка используется для поиска нового слова

    def __repr__(self):
        """
        Возвращает строковое представление ячейки.
        """
        status = []
        if self.is_used:
            status.append("used")
        if self.is_active:
            status.append("active")
        return f"Cell('{self.letter}', {' | '.join(status) if status else 'free'})"

    def get_letter(self):
        """
        Возвращает букву из ячейки.
        :return: Буква, хранящаяся в ячейке.
        """
        return self.letter

class Board:
    def __init__(self, size):
        """
        Инициализация игрового поля с заданным размером.
        :param size: Размер поля (количество ячеек по вертикали и горизонтали).
        """
        self.size = size
        self.grid = [[Cell('') for _ in range(size)] for _ in range(size)]

    def __repr__(self):
        """
        Возвращает строковое представление игрового поля.
        """
        return '\n'.join([' '.join([cell.letter if cell.letter else '.' for cell in row]) for row in self.grid])

    def display_grid(self):
        """
        Отображает сетку с буквами, где отгаданные слова выделяются зелёным цветом, а остальные чёрным.
        """
        for row in self.grid:
            row_display = []
            for cell in row:
                if cell.is_used:
                    row_display.append(f"\033[92m{cell.letter}\033[0m")  # Зелёный цвет для отгаданных
                else:
                    row_display.append(f"\033[30m{cell.letter}\033[0m")  # Чёрный цвет для остальных
            print(' '.join(row_display))

    def populate_grid(self):
        """
        Построчно заполняет матрицу буквами, введёнными пользователем.
        Если строка имеет длину, отличную от размера матрицы, выводится сообщение об ошибке.
        """
        print("Введите строки для заполнения поля. Длина каждой строки должна быть равна размеру матрицы.")
        for i in range(self.size):
            while True:
                row_input = input(f"Строка {i + 1}: ").strip()
                if len(row_input) == self.size:
                    for j, letter in enumerate(row_input):
                        self.grid[i][j] = Cell(letter)
                    break
                else:
                    print(f"Ошибка: длина строки должна быть ровно {self.size} символов. Попробуйте снова.")

    def test_fill_grid(self, test_data):
        """
        Заполняет сетку тестовыми данными.
        :param test_data: Список строк, содержащих буквы.
        """
        if len(test_data) != self.size or any(len(row) != self.size for row in test_data):
            raise ValueError("Тестовые данные не соответствуют размеру матрицы.")
        for i, row in enumerate(test_data):
            for j, letter in enumerate(row):
                self.grid[i][j] = Cell(letter)

def main():
    """
    Основная функция программы. Запрашивает размер матрицы, заполняет её и отображает.
    """
    while True:
        try:
            size = int(input("Введите размер матрицы (одно число): "))
            if size > 0:
                break
            else:
                print("Размер матрицы должен быть положительным числом. Попробуйте снова.")
        except ValueError:
            print("Ошибка: введите целое число.")

    board = Board(size)

    # Тестовые данные для заполнения поля
    test_data = [
        'опшлаан',
        'раяитки',
        'гамьлоф',
        'нетизмб',
        'колориу',
        'сопентк',
        'едаацив'
    ]

    if size == len(test_data):
        board.test_fill_grid(test_data)
    else:
        board.populate_grid()

    print("\nВаше поле:")
    board.display_grid()

if __name__ == "__main__":
    main()
