# Решение головоломки Fillwords на Python

## Описание проекта

Этот проект предназначен для автоматического решения головоломки **Fillwords** на Python. Программа позволяет находить все возможные слова на игровом поле, раскрашивать их различными цветами, а также предлагать пользователю возможные решения.

Полный текст с описанием решения размещен в [статье](https://habr.com/ru/articles/885008/) на Хабр.

## Функциональные возможности

- **Автоматический поиск слов** – программа анализирует игровое поле и выявляет все возможные слова.
- **Фильтрация найденных слов** – используется словарь существительных русского языка для проверки допустимых слов.
- **Раскрашивание найденных слов** – выделение слов цветами для наглядного представления.
- **Алгоритм заполнения игрового поля** – подбор таких слов, чтобы каждая ячейка поля была использована.
- **Интерактивный режим** – позволяет пользователю вручную выбирать слова для заполнения игрового поля.

## Установка и запуск

### Требования
- Python 3.8+
- Установленные зависимости:
  ```sh
  pip install -r requirements.txt
  ```

### Запуск программы
```sh
python part_3_3.py
```

## Используемые технологии
- **Python** – основной язык программирования.
- **Colorama** – для цветового выделения слов в терминале.
- **Алгоритмы поиска и backtracking** – для нахождения и распределения слов.

## Примеры использования
Пример игрового поля:
```
Р И Л О  
К А В Т  
Э Р А Й  
Х О Л А  
```
Выход программы:
```
Найденные слова: авто, лава, отвар, рай...
```

## Дальнейшие улучшения
- **Автоматизация взаимодействия с игрой** (распознавание букв с экрана, управление курсором).
- **Добавление новых языков** (английский, немецкий и др.).

## Авторы
Разработчик: [RustamGiz](https://github.com/RustamGiz)

## Лицензия
Этот проект распространяется под лицензией MIT.

