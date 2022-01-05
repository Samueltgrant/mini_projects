import random
import numpy as np
import string


def create_grid(size=(10, 10)):
    return [['-'] * size[0] for _ in range(size[1])]


def random_reverse(*words: str):
    return [word if random.getrandbits(1) else word[::-1] for word in words][0]


def random_orientation():
    return random.choice(['horizontal', 'vertical'])  # diagonal - to add


def horizontal_possible(grid, word):
    possible_rows = []
    for index, row in enumerate(grid):
        if len(word) * "-" in "".join(row):
            possible_rows.append(index)
    return possible_rows


def vertical_possible(grid, word):
    arr = np.array(grid)
    possible_cols = []

    for index, column in enumerate(arr.transpose()):
        if len(word) * "-" in "".join(column):
            possible_cols.append(index)
    return possible_cols


def valid_diagonal(grid, word):
    """Finds possible locations of word in grid for all four orientations and stores them in a list.
     Returns a single valid starting index, and a string representing the orientation"""
    down_right, down_left = ["down_right", []], ["down_left", []]
    for row_index, row in enumerate(grid):
        # THIS COULD BE A LOT SHORTER. Just need a down_right / down_left as it's going to be reversed some times.
        # also: I'm repeating a lot of code here. what I should so is randomise between two strings: "+", "-" and use
        # these - use eval with the strings e.g eval(row index {random "+" or "-"} 1)
        # make more efficient by selecting random grid location then getting random right down / left down.
        # If not valid, remove from list of options.
        # right down
        for col_index, cell in enumerate(row):
            if (len(row) - col_index < len(word)) or (len(grid) - row_index) < len(word):  # not space left in row/ col
                continue
            down_right_series = [grid[row_index + i][col_index + i] for i in range(len(word))]
            for index, letter in enumerate(word):
                if down_right_series[index] not in ['-', letter]:
                    break
            else:
                down_right[1].append([row_index, col_index])

        # left down
        for col_index, cell in enumerate(row):
            if (col_index + 1 < len(word)) or (len(grid) - row_index < len(word)):  # not space left in row/ col
                continue
            down_left_series = [grid[row_index + i][col_index - i] for i in range(len(word))]
            for index, letter in enumerate(word):
                if down_left_series[index] not in ['-', letter]:
                    break
            else:
                down_left[1].append([row_index, col_index])

    possible_options = [x for x in [down_right, down_left] if len(x[1]) != 0]
    if len(possible_options) == 0:
        print("Can't place diagonally.")
        pass
    selected_orientation = random.choice(possible_options)

    return selected_orientation[0], random.choice(selected_orientation[1])


def place_diagonal(grid, diagonal, word):
    orientation, start_index = diagonal
    print(orientation, start_index[0], start_index[1])
    if orientation == 'down_right':
        for index, letter in enumerate(word):  # place on grid
            grid[start_index[0] + index][start_index[1] + index] = letter

    elif orientation == 'down_left':
        for index, letter in enumerate(word):  # place on grid
            grid[start_index[0] + index][start_index[1] - index] = letter

    return grid


def valid_word_points(series: list, word: str):
    '''Checks for possible locations within series to place word.
    Returns list of ints representing valid first index's of word. '''
    valid_starting_point = []
    for index, position in enumerate(series):
        letters_checked = 0
        try:
            for letter in word:
                if series[index + letters_checked] not in ['-', letter]:
                    break
                else:
                    letters_checked += 1
                    if letters_checked == len(word):
                        valid_starting_point.append(index)
        except IndexError:
            break
    return valid_starting_point


def random_row_index(series: list):
    return random.choice(series)


def place_words_on_grid(grid, words):
    for word in words:
        orientation = random_orientation()
        word = random_reverse(word).upper()

        if orientation == "horizontal":
            if horizontal_possible(grid, word) == []:
                raise IndexError("Horizontal not possible for word:", word)
                # TODO - try again with other orientations
                # If fails, return error in creating wordearch. - maybe refsfstry 10times?
            selected_row = random.choice(horizontal_possible(grid, word))
            row_index_options = valid_word_points(grid[selected_row], word)
            random_index = random_row_index(row_index_options)

            for index, letter in enumerate(word):  # place on grid
                grid[selected_row][index + random_index] = letter

        elif orientation == 'vertical':
            if vertical_possible(grid, word) == []:
                raise IndexError("Vertical not possible for word:", word)
            selected_col = random.choice(vertical_possible(grid, word))
            col_index_options = valid_word_points(np.array(grid)[:, selected_col], word)
            random_index = random_row_index(col_index_options)
            for index, letter in enumerate(word):  # place on grid
                grid[index + random_index][selected_col] = letter

    return grid


def fill_grid(grid):
    for row_index, row in enumerate(grid):
        for col_index, char in enumerate(row):
            if char == '-':
                grid[row_index][col_index] = random.choice(string.ascii_uppercase)
    return grid


def wordsearch_gen(words, size=(10, 10)):
    grid = create_grid(size=size)
    place_words_on_grid(grid, words)
    fill_grid(grid)
    print(words)
    return grid
