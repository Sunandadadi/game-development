import os
import random
import copy
import time
import json

class Connect4(object):

    def __init__(self, board_size=4, curr_move=1, game_over=False):
        self.board_size = board_size
        self.empty_slot = ' '
        self.player1, self.player2, self.appreciate, self.punish = 'R', 'B', 4, 2
        self.grid = self.empty_grid()
        self.horizontal_wins, self.vertical_wins = self.fetch_wins()
        self.diagonal_wins = [{'33', '22', '11', '00'}, {'30', '21', '12', '03'}]
        self.file_path, self.file_data = 'connect4.json', {}
        self.file_data_for_game = {}
        self.p1_moves, self.p2_moves, self.possible_moves = set(), set(), self.board_size*self.board_size
        self.moves_tree, self.game_moves, self.curr_player = {}, {}, self.player1
        self.moves_tree_head = self.moves_tree
        self.curr_move, self.curr_row, self.curr_col, self.game_over = curr_move, None, None, game_over

    def fetch_wins(self):
        hwins, vwins = [], []
        for i in range(4):
            hval, vval = set(), set()
            for j in range(4):
                hval.add(str(i) + str(j))
                vval.add(str(j) + str(i))
            hwins.append(hval)
            vwins.append(vval)
        return hwins, vwins

    def empty_grid(self):
        grid = []
        for i in range(self.board_size):
            grid.append([' ']*self.board_size)
        return grid

    def get_player(self):
        return self.player2 if self.curr_move % 2 == 0 else self.player1

    def get_next_cell(self, col):
        for i in range(self.board_size - 1, -1, -1):
            if self.grid[i][col] == self.empty_slot:
                return i

    def validate_player_input(self, col):
        if col in range(0, self.board_size):
            row = self.get_next_cell(col)
            if row is not None:
                return True, row
        return False, None

    def pretty_print_grid(self):
        for i in self.grid:
            print(i)
        print('--------------------------------------------------')

    def build_machine_moves(self):
        val = str(self.curr_row)+str(self.curr_col)
        if not self.moves_tree or not self.moves_tree.get(val):
            self.moves_tree[val] = {'weight': 10, 'val': {}}
        self.moves_tree = self.moves_tree[val]['val']

    def build_player_moves(self):
        val = str(self.curr_row)+str(self.curr_col)
        if not self.moves_tree or not self.moves_tree.get(val):
            self.moves_tree[val] = {}

        self.moves_tree = self.moves_tree[val]

    def build_moves_tree(self):
        if self.curr_move % 2 == 0:
            self.build_machine_moves()
        else:
            self.build_player_moves()

    def update_move(self):
        self.game_moves[self.curr_move] = str(self.curr_row) + str(self.curr_col)
        self.grid[self.curr_row][self.curr_col] = self.curr_player
        self.pretty_print_grid()
        self.build_moves_tree()

    def fetch_player1_input(self):
        valid = False
        while not valid:
            col = int(input("Which column do you choose?")) - 1
            valid, row = self.validate_player_input(col)
        self.curr_row, self.curr_col = row, col
        move = str(self.curr_row)+str(self.curr_col)
        self.p1_moves.add(move)
        self.update_move()

    def fetch_smart_move(self, row, col):
        old_move = str(self.curr_row)+str(self.curr_col)
        new_move = str(row)+str(col)
        if self.file_data.get(old_move) and self.file_data[old_move].get(new_move) and \
            self.file_data[old_move][new_move] and self.file_data[old_move][new_move]['weight'] < 10:
            # Bad move
            new_val, max_weight = 0, 0
            for key,val in self.file_data[old_move].items():
                if val['weight'] > max_weight:
                    max_weight = val['weight']
                    new_val = key
            self.file_data = self.file_data[old_move][new_val]
            return int(new_val[0]), int(new_val[1])
        return row, col

    def fetch_machine_input(self):
        print('Machine plays as:')
        valid = False
        while not valid:
            col = random.randint(0,3)
            valid, row = self.validate_player_input(col)
        self.curr_row, self.curr_col = self.fetch_smart_move(row, col)
        self.p2_moves.add(str(self.curr_row)+str(self.curr_col))
        self.update_move()

    def check_win(self, moves, wins):
        for w in wins:
            if len(moves.intersection(w)) == 4:
                return True
        return False

    def is_game_over(self):
        if self.curr_move == self.possible_moves:
            val, self.game_over = 'draw', True
            print("Well played! It's a draw")
            return val

        if self.curr_move % 2 != 0:
            self.game_over = self.check_win(self.p1_moves, self.horizontal_wins) or \
                self.check_win(self.p1_moves, self.vertical_wins) or \
                self.check_win(self.p1_moves, self.diagonal_wins)
            if self.game_over:
                val = 'player'
                print("Yay! You won!")
        else:
            self.game_over = self.check_win(self.p2_moves, self.horizontal_wins) or \
                self.check_win(self.p2_moves, self.vertical_wins) or \
                self.check_win(self.p2_moves, self.diagonal_wins)
            if self.game_over:
                val = 'machine'
                print("Oops! Machine beat ya!")

        return val if self.game_over else None

    def merge(self, a, b, weights, path=None):
        "merging b into a"
        if path is None:
            path = []

        for key in b:
            if key in a:
                if isinstance(a[key], dict) and isinstance(b[key], dict):
                    self.merge(a[key], b[key], weights, path + [str(key)])
                elif a[key] == b[key]:
                    pass
                else:
                    # Different weights
                    a[key] = b[key]
            else:
                a[key] = b[key]
        return a

    def write_to_file(self, data):
        with open(self.file_path, 'w') as f:
            json.dump(data, f, ensure_ascii=False)

    def read_from_file(self):
        if not os.path.isfile('connect4.json'):
            return self.file_data
        with open(self.file_path) as f:
            return json.load(f)

    def update_file(self, key, val):
        file_data = self.read_from_file()
        file_data[key] = val

        with open(self.file_path, 'w') as f:
            json.dump(file_data, f, ensure_ascii=False)

    def get_weights(self, result):
        return self.appreciate if result == 'machine' else self.punish if result == 'player' else None

    def add_weights(self, data, weights):
        for key, val in data.items():
            if isinstance(val, dict):
                self.add_weights(val, weights)
            elif key == 'weight':
                if weights == self.appreciate:
                    data['weight'] = data['weight'] + weights
                elif weights == self.punish:
                    data['weight'] = data['weight'] - weights
        return data

    def record_moves(self, result):
        file_data = self.read_from_file()
        write_data = self.moves_tree_head
        weights = self.get_weights(result)
        write_data = self.add_weights(write_data, weights) if weights else write_data
        file_data = self.merge(file_data, write_data, weights) if file_data else write_data
        self.write_to_file(file_data)

    def lets_play(self):
        self.file_data = self.read_from_file()
        while not self.game_over:
            if self.curr_move % 2 != 0:
                self.fetch_player1_input()
            else:
                self.fetch_machine_input()
            result = self.is_game_over()
            self.curr_move += 1
            self.curr_player = self.get_player()
        self.record_moves(result)



if __name__ == '__main__':
    # Program is player 2
    # Player1 is 'Red'
    # Player2 is 'Black', Computer is player2
    a = Connect4()
    a.lets_play()
