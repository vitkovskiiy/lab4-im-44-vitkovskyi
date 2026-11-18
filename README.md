# Лабораторна робота №4 — Tetris++

- Студент: Іван Вітковський
- Група: ІМ-44
- Pull request: [PR URL]
- Демо-відео (необов'язково): [DEMO VIDEO URL]

Продовження лабораторної №3. Програма читає початковий стан екрана гри, схожої
на Тетріс (одна «підвішена» фігура `p` і «ландшафт» `#`), і виводить стан після
того, як фігура впала. З параметром `--all-steps` виводить екран на кожному
кроці падіння (`STEP 0`, `STEP 1`, ...). Без параметра програма працює, як раніше.
Якщо вхідний файл некоректний або його не вдалося прочитати, програма виводить
`Error: invalid input` без подробиць.

## Встановлення

```bash
pip install -r requirements.txt
```

## Тести

```bash
pytest
```

## Що змінилось порівняно з лабораторною №3

- **Mock'и з бібліотеки.** Власноруч написані `FakeReader` і `RecordingWriter`
  замінені на `unittest.mock.create_autospec(FileReader)` /
  `create_autospec(ConsoleWriter)` (`tests/test_app.py`). Autospec будує mock
  за справжнім класом, тому виклик методу, якого немає, або з неправильними
  аргументами, валить тест.
- **Property-based тести з бібліотекою.** Власний генератор полів замінено на
  стратегію [Hypothesis](https://hypothesis.readthedocs.io/)
  (`tests/test_properties.py`): ті самі властивості + властивості режиму
  «усі кроки». Hypothesis сам зменшує поле, на якому тест упав, до мінімального
  прикладу (shrinking).
- **Режим «усі кроки».** `fall_steps` (логіка), `render_steps` (формат),
  `TetrisApp.run(path, all_steps=True)` (комунікаційний шар), прапорець
  `--all-steps` (CLI).
- **Покриття коду в PR.** GitHub Actions рахує покриття рядків і гілок
  (`pytest-cov --cov-branch`) і пише його коментарем у PR, який оновлюється на
  кожному новому коміті.

## Шари програми

| Шар | Модуль | Що робить |
|---|---|---|
| Логічний | `src/tetris/field.py` | `Point`, `Field`, `step_down`, `drop`, `fall_steps` |
| Логічний | `src/tetris/codec.py` | `parse_field`, `render_field`, `render_steps` |
| Введення/виведення | `src/tetris/io_adapters.py` | `FileReader`, `ConsoleWriter` |
| Комунікаційний | `src/tetris/app.py` | `TetrisApp(reader, writer)` — DI через конструктор |
| Точка входу | `src/tetris/cli.py` | розбирає аргументи, збирає `TetrisApp` зі справжніми класами |

## Приклад запуску

Вхідний файл `examples/example1.txt`:

```
7 8
..p.....
.ppp....
..p.....
........
...#....
...#...#
#..#####
```

Тільки фінальний екран:

```bash
python -m src.tetris examples/example1.txt
```

```
........
........
..p.....
.ppp....
..p#....
...#...#
#..#####
```

Усі кроки:

```bash
python -m src.tetris --all-steps examples/example1.txt
```

```
STEP 0
..p.....
.ppp....
..p.....
........
...#....
...#...#
#..#####
STEP 1
........
..p.....
.ppp....
..p.....
...#....
...#...#
#..#####
STEP 2
........
........
..p.....
.ppp....
..p#....
...#...#
#..#####
```
