# Group members: Sunanda(netid: sdadi2), Jenna Jordan(netid:jaj5)
import random
import copy

class HauntedMaze(object):
    """docstring for HauntedMaze
        Variables:
            'puzzle': is a 2D - list of with empty slots denotated as ' ' and mirrors as '/' and '\\'
            'top': is a list of the count of monsters from the top view
            'bottom': is a list of the count of monsters from the bottom view
            'left': is a list of the count of monsters from the left view
            'right': is a list of the count of monsters from the right view
            'height': is the height of the 2D - list
            'width': is the width of the 2D - list
    """
    def __init__(self):
        self.monsters = ['V', 'G', 'Z', 'T']
        self.mirrors = ['\\', '/']
        self.gap = ' '
        self.weighted_vals = {
            'V': 0.16,
            'G': 0.16,
            'Z': 0.16,
            'T': 0.16,
            '\\': 0.16,
            '/': 0.16
        }

    def get_vampire_count(self, reflection: bool) -> bool:
        return 0 if reflection else 1

    def get_ghost_count(self, reflection: bool) -> bool:
        return 1 if reflection else 0

    def get_zombie_count(self, reflection: bool) -> bool:
        return 1

    def get_troll_count(self, reflection: bool) -> bool:
        return 1

    def get_monster_count(self, val: str, reflection: bool) -> int:
        if val == 'V':
            return self.get_vampire_count(reflection)
        elif val == 'G':
            return self.get_ghost_count(reflection)
        elif val == 'Z':
            return self.get_zombie_count(reflection)
        elif val == 'T':
            return self.get_troll_count(reflection)

    def next_left_mirror_cell(self, view: str, row: int, col: int) -> tuple:
        if view == 'top':
            return (row, col + 1, 'right') if col + 1 < self.width else (-1, -1, -1)
        elif view == 'bottom':
            return (row, col - 1, 'left') if col - 1 >= 0 else (-1, -1, -1)
        elif view == 'left':
            return (row + 1, col, 'bottom') if row + 1 < self.height else (-1, -1, -1)
        elif view == 'right':
            return (row - 1, col, 'top') if row - 1 >= 0 else (-1, -1, -1)

    def next_right_mirror_cell(self, view: str, row: int, col: int) -> tuple:
        if view == 'top':
            return (row, col - 1, 'left') if col - 1 >= 0 else (-1, -1, -1)
        elif view == 'bottom':
            return (row, col + 1, 'right') if col + 1 < self.width else (-1, -1, -1)
        elif view == 'left':
            return (row - 1, col, 'top') if row - 1 >= 0 else (-1, -1, -1)
        elif view == 'right':
            return (row + 1, col, 'bottom') if row + 1 < self.height else (-1, -1, -1)

    def get_next_cell(self, val: str, view: str, row_index: int, col_index: int) -> tuple:
        if val == '\\':
            return self.next_left_mirror_cell(view, row_index, col_index)
        elif val == '/':
            return self.next_right_mirror_cell(view, row_index, col_index)

    def move(self, row: int, col: int, move: str) -> tuple:
        if move == 'top':
            return (row - 1, col) if row - 1 >= 0 else (-1, -1)
        elif move == 'bottom':
            return (row + 1, col) if row + 1 < self.height else (-1, -1)
        elif move == 'left':
            return (row, col - 1) if col - 1 >= 0 else (-1, -1)
        elif move == 'right':
            return (row, col + 1) if col + 1 < self.width else (-1, -1)

    def get_new_view(self, move: str) -> str:
        if move == 'top':
            return 'bottom'
        elif move =='bottom':
            return 'top'
        elif move == 'left':
            return 'right'
        elif move == 'right':
            return 'left'

    def get_mirror_path_count(self, row: int, col: int, view: str, val: str, puzzle: list) -> list:
        count = 0
        while row != -1 and col != -1 and puzzle[row][col] != self.gap:
            if val in self.monsters:
                count += self.get_monster_count(puzzle[row][col], reflection = True)
                if puzzle[row][col] == 'T':
                    break
                row, col = self.move(row, col, move)
                val = puzzle[row][col]
            elif val in self.mirrors:
                row, col, move = self.get_next_cell(val, view, row, col)
                view, val = self.get_new_view(move), puzzle[row][col]

        return count

    def top_view(self, puzzle: list, view: str = 'top') -> list:
        top_view = [0] * self.width
        for i in range(self.width):
            for j in range(self.height):
                if puzzle[j][i] in self.monsters:
                    top_view[i] += self.get_monster_count(puzzle[j][i], reflection = False)
                    if puzzle[j][i] == 'T':
                        break

                elif puzzle[j][i] in self.mirrors:
                    top_view[i] += self.get_mirror_path_count(j, i, view, puzzle[j][i], puzzle)
                    break
        return top_view

    def bottom_view(self, puzzle: list, view: str = 'bottom') -> list:
        bottom_view = [0] * self.width
        for i in range(self.width):
            for j in range(self.height - 1, -1, -1):
                if puzzle[j][i] in self.monsters:
                    bottom_view[i] += self.get_monster_count(puzzle[j][i], reflection = False)
                    if puzzle[j][i] == 'T':
                        break

                elif puzzle[j][i] in self.mirrors:
                    bottom_view[i] += self.get_mirror_path_count(j, i, view, puzzle[j][i], puzzle)
                    break
        return bottom_view

    def left_view(self, puzzle: list, view: str = 'left') -> list:
        left_view = [0] * self.height
        for i in range(self.height):
            for j in range(self.width):
                if puzzle[i][j] in self.monsters:
                    left_view[i] += self.get_monster_count(puzzle[i][j], reflection = False)
                    if puzzle[i][j] == 'T':
                        break

                elif puzzle[i][j] in self.mirrors:
                    left_view[i] += self.get_mirror_path_count(i, j, view, puzzle[i][j], puzzle)
                    break
        return left_view

    def right_view(self, puzzle: list, view: str = 'right') -> list:
        right_view = [0] * self.height
        for i in range(self.height):
            for j in range(self.width - 1, -1, -1):
                if puzzle[i][j] in self.monsters:
                    right_view[i] += self.get_monster_count(puzzle[i][j], reflection = False)
                    if puzzle[i][j] == 'T':
                        break

                elif puzzle[i][j] in self.mirrors:
                    right_view[i] += self.get_mirror_path_count(i, j, view, puzzle[i][j], puzzle)
                    break
        return right_view

    def total_monster_count(self, puzzle: list) -> int:
        cells = self.cell_distribution(puzzle)
        total_monsters = {}
        for m in self.monsters:
            total_monsters[m] = cells.get(m, -1)
        return total_monsters

    def get_rules(self, puzzle: list) -> dict:
        return {
            'top': self.top_view(puzzle),
            'bottom': self.bottom_view(puzzle),
            'left': self.left_view(puzzle),
            'right': self.right_view(puzzle),
            'monsters': self.total_monster_count(puzzle)
        }

    def get_puzzle(self) -> list:
        puzzle = [[' '] * self.width] * self.height
        for i in range(self.height):
            puzzle[i] = random.choices(
                    population = list(self.weighted_vals.keys()),
                    weights = list(self.weighted_vals.values()),
                    k = self.width
                )
        return puzzle

    def squarred_mirrors_check(self, puzzle: list) -> bool:
        for i in range(0, len(puzzle) - 1):
            for j in range(1, len(puzzle[i])):
                if puzzle[i][j] == self.mirrors[0] and puzzle[i+1][j] == self.mirrors[1] and \
                    puzzle[i][j-1] == self.mirrors[1] and puzzle[i+1][j-1] == self.mirrors[0]:
                    return False
        return True

    def cell_distribution(self, puzzle: list) -> dict:
        a = {}
        for i in puzzle:
            for j in i:
                if not a.get(j):
                    a[j] = 1
                else:
                    a[j] += 1
        return a

    def cell_distribution_check(self, cells):
        cell_count = self.width * self.height
        total_monsters, total_mirros = 0, 0
        for m in self.monsters:
            total_monsters += cells.get(m, 0)
        for m in self.mirrors:
            total_mirros += cells.get(m, 0)

        return False if cell_count == total_monsters or cell_count == total_mirros else True

    def basic_checks(self, puzzle: list) -> bool:
        cells = self.cell_distribution(puzzle)
        return self.squarred_mirrors_check(puzzle) and self.cell_distribution_check(cells)

    def get_empty_puzzle(self, puzzle: list) -> list:
        e = copy.deepcopy(puzzle)
        for i in range(0, self.height):
            for j in range(0, self.width):
                if e[i][j] in self.monsters:
                    e[i][j] = ' '
        return e

    def fill_vertical_ghosts(self, empty_puzzle: list, index: int, list: list):
        for i in list:
            if empty_puzzle[i][index] not in self.mirrors:
                empty_puzzle[i][index] = 'G'
            else:
                break

    def fill_horizontal_ghosts(self, empty_puzzle: list, index: int, list: list):
        for i in list:
            if empty_puzzle[index][i] not in self.mirrors:
                empty_puzzle[index][i] = 'G'
            else:
                break

    def fill_ghosts(self, empty_puzzle: list, index: int, view: str):
        if view == 'top':
            list = range(self.height)
            self.fill_vertical_ghosts(empty_puzzle, index, list)
        elif view == 'bottom':
            list = range(self.height - 1, -1, -1)
            self.fill_vertical_ghosts(empty_puzzle, index, list)
        elif view == 'left':
            list = range(self.width)
            self.fill_horizontal_ghosts(empty_puzzle, index, list)
        elif view == 'right':
            list = range(self.width - 1, -1, -1)
            self.fill_horizontal_ghosts(empty_puzzle, index, list)

    def v_ending_mirror(self, empty_puzzle: list, index: int, view_index: int, start: str, end: str) -> bool:
        mirror, i = False, 0
        for i in range(index, self.width):
            if empty_puzzle[view_index][i] == start:
                return -1
            elif empty_puzzle[view_index][i] == end:
                return i
        return i + 1

    def h_ending_mirror(self, empty_puzzle: list, index: int, view_index: int, start: str, end: str) -> bool:
        mirror, i = False, 0
        for i in range(index, self.height):
            if empty_puzzle[i][view_index] == start:
                return -1
            elif empty_puzzle[i][view_index] == end:
                return i
        return i + 1

    def fill_horizontal_vamps(self, empty_puzzle: list, list: list, view_index: int):
        for i in list:
            empty_puzzle[view_index][i] = 'V'

    def fill_vertical_vamps(self, empty_puzzle: list, list: list, view_index: int):
        for i in list:
            empty_puzzle[view_index][i] = 'V'

    def check_for_vamps(self, empty_puzzle: list, index: int, view:str):
        if view == 'top' and empty_puzzle[0][index] == self.mirrors[0]:
            end_idx = self.v_ending_mirror(empty_puzzle, index + 1, 0, self.mirrors[0], self.mirrors[1])
            if end_idx != -1:
                list = range(index + 1, end_idx)
                self.fill_vertical_vamps(empty_puzzle, list, 0)

        elif view == 'bottom' and empty_puzzle[self.height - 1][index] == self.mirrors[1]:
            end_idx = self.v_ending_mirror(empty_puzzle, index + 1, self.height - 1, self.mirrors[1], self.mirrors[0])
            if end_idx != -1:
                list = range(index + 1, end_idx)
                self.fill_vertical_vamps(empty_puzzle, list, self.height - 1)

        elif view == 'left' and empty_puzzle[index][0] == self.mirrors[0]:
            end_idx = self.h_ending_mirror(empty_puzzle, index + 1, 0, self.mirrors[0], self.mirrors[1])
            if end_idx != -1:
                list = range(index + 1, end_idx)
                self.fill_horizontal_vamps(empty_puzzle, list, 0)

        elif view == 'right' and empty_puzzle[index][self.width - 1] == self.mirrors[1]:
            end_idx = self.h_ending_mirror(empty_puzzle, index + 1, self.width - 1, self.mirrors[1], self.mirrors[0])
            if end_idx != -1:
                list = range(index + 1, end_idx)
                self.fill_horizontal_vamps(empty_puzzle, list, self.width - 1)


    def apply_deterministic_rules(self, empty_puzzle: list, rules: dict):
        for key,val in rules.items():
            if key != 'monsters':
                for idx in range(len(val)):
                    if val[idx] == 0:
                        self.fill_ghosts(empty_puzzle, idx, key)
                        self.check_for_vamps(empty_puzzle, idx, key)

    def possible_solution(self, possible_rule, rule):
        idx, valid = 0, True
        for i, j in zip(possible_rule, rule):
            if i > j:
                valid = False
                break
        return valid

    def is_valid(self, empty_puzzle: list, rules: dict) -> bool:
        return self.possible_solution(self.top_view(empty_puzzle), rules['top']) and \
            self.possible_solution(self.bottom_view(empty_puzzle), rules['bottom']) and \
            self.possible_solution(self.left_view(empty_puzzle), rules['left']) and \
            self.possible_solution(self.right_view(empty_puzzle), rules['right'])

    def fill_random_monsters(self, puzzle: list, empty_puzzle: list, rules: dict, temp_mc: list):
        for i in range(self.height):
            for j in range(self.width):
                if empty_puzzle[i][j] == self.gap:
                    for m in self.monsters:
                        if puzzle[i][j] != m:
                            empty_puzzle[i][j] = m
                            if not self.is_valid(empty_puzzle, rules):
                                empty_puzzle[i][j] = self.gap
                            else:
                                temp_mc[m] += 1
                                self.fill_random_monsters(puzzle, empty_puzzle, rules, temp_mc)

                if empty_puzzle[i][j] == self.gap:
                    return

    def puzzle_not_empty(self, empty_puzzle: list) -> bool:
        valid = True
        for p in empty_puzzle:
            if self.gap in p:
                valid = False
                break
        return valid


    def find_solutions(self, puzzle: list, rules: dict):
        empty_puzzle = self.get_empty_puzzle(puzzle)
        e = copy.deepcopy(empty_puzzle)
        self.apply_deterministic_rules(e, rules)
        temp_mc = self.total_monster_count(empty_puzzle)
        self.fill_random_monsters(puzzle, e, rules, temp_mc)
        if self.puzzle_not_empty(e):
            return 2, empty_puzzle, e
        return 1, empty_puzzle, e

    def pretty_print(self, empty_puzzle: int, rules: dict):
        print('    ', "  ".join(str(x) for x in rules['top']))
        for i, j, k in zip(rules['left'], empty_puzzle, rules['right']):
            print('  ', end='')
            print(i, ' ', end='')
            print("  ".join(str(x) for x in j), end='')
            print(' ', k)
        print('    ', "  ".join(str(x) for x in rules['bottom']))

    def generate_puzzle(self, height: int, width: int):
        self.__dict__['height'], self.__dict__['width'] = height, width

        while True:
            puzzle = self.get_puzzle()
            if self.basic_checks(puzzle):
                rules = self.get_rules(puzzle)
                found, empty_puzzle, partial_puzzle = self.find_solutions(puzzle, rules)
                if found == 1:
                    break

        print("Solution is: ")
        self.pretty_print(puzzle, rules)
        print("------------------------------------------------------------------")
        self.pretty_print(empty_puzzle, rules)



if __name__ == '__main__':
    '''
        Commands to run to generate a random puzzle
    '''
    a = HauntedMaze()
    a.generate_puzzle(10, 10)
