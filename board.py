from colorama import init, Fore, Style

init()


class Cell:
    def __init__(self, letter, x, y):
        """
        Инициализация ячейки с буквой и координатами.
        :param letter: Буква, которая будет храниться в ячейке.
        :param x: Координата по горизонтали.
        :param y: Координата по вертикали.
        """
        self.letter = letter  # Буква в ячейке
        self.is_used = False  # Флаг, что ячейка уже используется в отгаданном слове
        self.x = x            # Координата X
        self.y = y            # Координата Y


    def __eq__(self, other):
        """
        Проверяет, являются ли две ячейки одинаковыми.
        :param other: Другая ячейка.
        :return: True, если ячейки равны, иначе False.
        """
        return self.x == other.x and self.y == other.y

    def __repr__(self):
        """
        Возвращает строковое представление ячейки.
        """
        status = []
        if self.is_used:
            status.append("used")
        return f"Cell('{self.letter}', x={self.x}, y={self.y}, {' | '.join(status) if status else 'free'})"

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
        self.grid = [[Cell('', x, y) for x in range(size)] for y in range(size)]
        self.chans = []
        self.found_words = set()

    def __repr__(self):
        """
        Возвращает строковое представление игрового поля.
        """
        return '\n'.join([' '.join([cell.letter if cell.letter else '.' for cell in row]) for row in self.grid])

    def find_free_cell(self):
        """
        Находит первую свободную ячейку на игровом поле.
        :return: Координаты (x, y) свободной ячейки.
        """
        for y in range(self.size):
            for x in range(self.size):
                if not self.grid[y][x].is_used:
                    return x, y
        return None

    def display_grid(self):
        """
        Отображает сетку с буквами, где отгаданные слова выделяются зелёным цветом, а остальные чёрным.
        """
        for row in self.grid:
            row_display = []
            for cell in row:
                if cell.is_used:
                    row_display.append(Fore.GREEN + cell.letter + Style.RESET_ALL)  # Зелёный цвет для отгаданных
                else:
                    row_display.append(Fore.WHITE + cell.letter + Style.RESET_ALL)  # Белый цвет для остальных
            print(' '.join(row_display))

    def populate_grid(self):
        """
        Построчно заполняет матрицу буквами, введёнными пользователем.
        Если строка имеет длину, отличную от размера матрицы, выводится сообщение об ошибке.
        """
        print("Введите строки для заполнения поля. Длина каждой строки должна быть равна размеру матрицы.")
        for y in range(self.size):
            while True:
                row_input = input(f"Строка {y + 1}: ").strip()
                if len(row_input) == self.size:
                    for x, letter in enumerate(row_input):
                        self.grid[y][x] = Cell(letter, x, y)
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
        for y, row in enumerate(test_data):
            for x, letter in enumerate(row):
                self.grid[y][x] = Cell(letter, x, y)

class CheckWord:
    def __init__(self, word, words):
        """
        Инициализация объекта проверки слов.
        :param word: Проверяемое слово.
        :param words: Список допустимых слов.
        """
        self.word = word
        if len(self.word) >= 3:
            self.check_words = [w for w in words if word in w]
        else:
            self.check_words = words

    def is_exact_match(self):
        """
        Проверяет, есть ли точное совпадение слова в списке.
        :return: True, если есть точное совпадение, иначе False.
        """
        return self.word in self.check_words

class Chain:
    def __init__(self, start_x, start_y, board, forward_words, backward_words):
        """
        Инициализация цепочки для составления слова.
        :param start_x: Начальная координата X.
        :param start_y: Начальная координата Y.
        :param board: Игровое поле Board.
        """
        self.cells = [board.grid[start_y][start_x]]  # Список ячеек, составляющих цепочку
        self.forward_check = None  # Проверка слова в прямом направлении
        self.backward_check = None  # Проверка слова в обратном направлении
        self.forward_words = forward_words
        self.backward_words = backward_words
        self.board = board

    def __eq__(self, other):
        if isinstance(other, Chain):
            if len(self.cells) != len(other.cells):
                return False
            for i in range(len(self.cells)):
                reversed_self = self.cells[::-1]
                if self.cells[i] != other.cells[i]:
                    return False
            return True
        return False

    def get_word_forward(self):
        """
        Возвращает слово из цепочки, составленное в прямом направлении.
        :return: Слово в прямом направлении.
        """
        return ''.join(cell.get_letter() for cell in self.cells) if self.cells else ''

    def get_word_backward(self):
        """
        Возвращает слово из цепочки, составленное в обратном направлении.
        :return: Слово в обратном направлении.
        """
        return ''.join(cell.get_letter() for cell in reversed(self.cells))

    def update_checks(self):
        """
        Обновляет проверки слов в прямом и обратном направлениях.
        """
        forward_word = self.get_word_forward()
        backward_word = self.get_word_backward()
        self.forward_check = CheckWord(forward_word, self.forward_words)
        self.backward_check = CheckWord(backward_word, self.backward_words)

    def get_adjacent_free_cells(self, cell):
        """
        Возвращает кортеж свободных ячеек, примыкающих к заданной ячейке.
        :param cell: Ячейка, вокруг которой ищутся свободные примыкающие ячейки.
        :return: Список примыкающих свободных ячеек.
        """
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        adjacent_cells = []
        for dx, dy in directions:
            nx, ny = cell.x + dx, cell.y + dy
            if 0 <= nx < self.board.size and 0 <= ny < self.board.size:
                neighbor = self.board.grid[ny][nx]
                if not neighbor.is_used and neighbor not in self.cells:
                    adjacent_cells.append(neighbor)
        return adjacent_cells

    def __repr__(self):
        return f"Chain(cells={self.cells})"

    def create_new_chains(self):
        """
        Создаёт список новых цепочек на основе текущей цепочки, добавляя ячейки в начало или конец.
        :return: Список новых цепочек.
        """
        new_chains = []
        start_cell = self.cells[0]
        end_cell = self.cells[-1]

        # Для ячеек, примыкающих к первой ячейке
        for adj_cell in self.get_adjacent_free_cells(start_cell):
            new_chain = Chain(adj_cell.x, adj_cell.y, self.board, self.forward_words, self.backward_words)
            new_chain.cells = [adj_cell] + self.cells
            new_chain.update_checks()

            if new_chain.forward_check.check_words or new_chain.backward_check.check_words:
                new_chains.append(new_chain)

        # Для ячеек, примыкающих к последней ячейке
        if len(self.cells) > 1:
            for adj_cell in self.get_adjacent_free_cells(end_cell):
                new_chain = Chain(adj_cell.x, adj_cell.y, self.board, self.forward_words, self.backward_words)
                new_chain.cells = self.cells + [adj_cell]
                new_chain.update_checks()

                if new_chain.forward_check.check_words or new_chain.backward_check.check_words:
                    new_chains.append(new_chain)

        return new_chains

# Глобальная переменная для допустимых слов
# words = ["слово", "слон", "молоко", "кислота", "ананас", "игра", "цвет", "гол", "лад", "раскачка",
#         "залог", "политбюро", "утепление", "коварство"]

words = []

with open('zdf.txt', 'r', encoding='utf-8') as f:
    for line in f:
        words.append(line.strip())

def main():
    """
    Основная функция программы. Запрашивает размер матрицы, заполняет её и отображает.
    """
    size = 7

    board = Board(size)

    # Тестовые данные для заполнения поля
    test_data = [
        'асстчка',
        'рльроба',
        'тптонкн',
        'оерелив',
        'рафиьлу',
        'шдансоб',
        'лангроз'
    ]

    if size == len(test_data):
        board.test_fill_grid(test_data)
    else:
        board.populate_grid()

    print("\nВаше поле:")
    board.display_grid()

    start_x, start_y = board.find_free_cell()
    chain = Chain(start_x, start_y, board, words, words)
    board.chans = [chain]

    i = 0

    while True:
        i += 1
        print('шаг', i)
        new_chains = []
        for chain in board.chans:
            curr_chains = chain.create_new_chains()
            for curr_chain in curr_chains:
                if curr_chain not in new_chains:
                    if curr_chain.forward_check.is_exact_match():
                        board.found_words.add(curr_chain.get_word_forward())
                    if curr_chain.backward_check.is_exact_match():
                        board.found_words.add(curr_chain.get_word_backward())
                    new_chains.append(curr_chain)

        board.chans = new_chains

        if new_chains:
            for chain in board.chans:

                print(chain, chain.get_word_forward(), chain.get_word_backward())
                if i >= 2:
                    print(chain.forward_check.check_words, chain.backward_check.check_words)

        else:
            break

    print("\nВсе слова:")
    for word in board.found_words:
        print(word)


if __name__ == "__main__":
    main()
