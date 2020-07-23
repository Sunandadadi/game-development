from client import Client, SuccessResponse
from ast import literal_eval
from copy import deepcopy
from time import sleep
import json
import random

class TurningPoints(object):
    def __init__(self, game_id):
        self.game_id = game_id
        self.client = Client()
        self.height, self.width, self.num_players = self.fetch_game_params()
        self.empty_grid = self.empty_grid()
        self.match_id = self.fetch_match_id()
        self.board = [[0] * self.width] * self.height
        self.board_cells = self.fetch_board_cells()
        self.board_cells_count = len(self.board_cells)
        self.rotations_key = {
            1: 2,
            2: 3,
            3: 4,
            4: 1
        }
        self.direction_keys = self.rotations_key.keys()
        self.moves_tree = {}
        self.history = {}
        self.threshold = 5
        self.player_num = 0
        if self.board_cells_count > self.threshold:
            self.threshold = self.board_cells_count - self.threshold
        else:
            self.threshold = 1


    def empty_grid(self):
        grid = []
        for i in range(self.height):
            grid.append([' ']*self.width)
        return grid


    def fetch_board_cells(self):
        cells = []
        for h in range(self.height):
            for w in range(self.width):
                cells.append((h,w))
        return cells

    def fetch_game_params(self):
        r = self.client.fetch_game_details(self.game_id)
        data = r.content[0]
        params = json.loads(data.get('class_params'))
        height, width = params.get('height'), params.get('width')
        players = data.get('num_players')
        return (height, width, players)

    def fetch_match_id(self):
        r = self.client.fetch_match_id(self.game_id)
        return r.content.get('match_id')

    def fetch_possible_cells(self, visited):
        row_cols = []
        for visit in visited:
            row_cols.append((visit[0], visit[1]))
        return list(set(self.board_cells) - set(row_cols))

    def check_up_rotation(self, grid, row, col):
        return True if row - 1 >= 0 and grid[row - 1][col] not in [1, ' '] else False

    def check_down_rotation(self, grid, row, col):
        return True if row + 1 < self.height and grid[row + 1][col] not in [3, ' '] else False

    def check_right_rotation(self, grid, row, col):
        return True if col + 1 < self.width and grid[row][col + 1] not in [2, ' '] else False

    def check_left_rotation(self, grid, row, col):
        return True if col - 1 >= 0 and grid[row][col - 1] not in [4, ' '] else False

    def update_grid_rotations(self, grid, curr_row, curr_col, curr_dir):
        if curr_dir == 1:
            if self.check_up_rotation(grid, curr_row, curr_col):
                grid[curr_row - 1][curr_col] = self.rotations_key[grid[curr_row - 1][curr_col]]
                self.update_grid_rotations(grid, curr_row - 1, curr_col, grid[curr_row - 1][curr_col])

        elif curr_dir == 2:
            if self.check_right_rotation(grid, curr_row, curr_col):
                grid[curr_row][curr_col + 1] = self.rotations_key[grid[curr_row][curr_col + 1]]
                self.update_grid_rotations(grid, curr_row, curr_col + 1, grid[curr_row][curr_col + 1])

        elif curr_dir == 3:
            if self.check_down_rotation(grid, curr_row, curr_col):
                grid[curr_row + 1][curr_col] = self.rotations_key[grid[curr_row + 1][curr_col]]
                self.update_grid_rotations(grid, curr_row + 1, curr_col, grid[curr_row + 1][curr_col])

        elif curr_dir == 4:
            if self.check_left_rotation(grid, curr_row, curr_col):
                grid[curr_row][curr_col - 1] = self.rotations_key[grid[curr_row][curr_col - 1]]
                self.update_grid_rotations(grid, curr_row, curr_col - 1, grid[curr_row][curr_col - 1])

        return grid

    def update_move_score(self, visited):
        score = 0
        grid = deepcopy(self.empty_grid)
        temp_moves = self.moves_tree
        for visit in visited:
            row, col, dir = visit[0], visit[1], visit[2]
            grid[row][col] = dir
            key = str(row) + str(col) + str(dir)
            grid = self.update_grid_rotations(grid, row, col, dir)
            temp_moves = temp_moves[key]

        temp_moves['score'] = [y for rows in grid for y in rows].count(self.player_num)

    def build_move_tree(self, temp_dict, parent, visited):
        poss_moves = self.fetch_possible_cells(visited)
        for move in poss_moves:
            val = str(move[0]) + str(move[1])
            for x in self.direction_keys:
                new_key = val + str(x)
                v = visited + [(move[0], move[1], x)]
                temp_dict[parent].update({new_key: {} })
                self.build_move_tree(temp_dict[parent], new_key, v)

        if len(visited) == self.board_cells_count:
            self.update_move_score(visited)

    def fetch_max_score(self, moves_tree, values):
        for key, value in moves_tree.items():
            if key != 'score' and moves_tree[key]:
                self.fetch_max_score(moves_tree[key], values)
            elif key == 'score':
                values.append(value)

    def fetch_best_next_move(self, moves_tree):
        max_key, max_score, key_scores = None, 0, {}
        for key, moves in moves_tree.items():
            values = []
            self.fetch_max_score(moves_tree[key], values)
            key_score = max(values)
            key_scores[key] = key_score
            if key_score > max_score:
                max_score = key_score
                max_key = key
        return max_key

    def fetch_updated_moves_tree(self, turn_data, updated_tree):
        turn = 1
        while turn < turn_data.get('turn'):
            if self.history.get(turn):
                key = self.history[turn]
            else:
                for each_move in turn_data.get('history'):
                    if each_move.get('turn') == turn:
                        move = literal_eval(each_move.get('move'))
                        key = str(move[0])+ str(move[1]) + str(move[2])
                        self.history.update({turn: key})
            updated_tree = updated_tree[key]
            turn += 1

        return updated_tree

    def fetch_next_move(self, turn_data):
        updated_tree = self.moves_tree
        updated_tree = self.fetch_updated_moves_tree(turn_data, updated_tree)
        next_move = self.fetch_best_next_move(updated_tree)
        return (int(next_move[0]), int(next_move[1]), int(next_move[2]))

    def fetch_random(self, turn):
        row_vals, col_vals, history_vals = range(self.height), range(self.width), []
        if self.history:
            history_vals = self.history.values()
            history_vals = [x[0] + x[1] for x in history_vals]

        row = random.choice(row_vals)
        col = random.choice(col_vals)
        if history_vals:
            while str(row)+str(col) in history_vals:
                row = random.choice(row_vals)
                col = random.choice(col_vals)

        direction = random.choice(range(1, 5))
        tree_key = str(row) + str(col) + str(direction)
        if not self.history.get(turn):
            self.history.update({turn: tree_key})
        return (row, col, direction)

    def match_over(self, data):
        history = data.get('history')
        for his in history:
            if his.get('turn') == self.board_cells_count:
                result = his.get('result')
                break
        print("Final board is", result, "and my alloted direction is", self.player_num)

    def lets_play(self):
        while True:

            while True:
                turn_data = self.client.fetch_turn(self.match_id).content
                print("turn_data", turn_data)
                if self.player_num == 0:
                    self.player_num = turn_data.get('current_player_turn')
                match_status = turn_data.get('match_status')
                if match_status == 'in play':
                    turn_status = turn_data.get('turn_status')
                    if turn_status == 'your turn':
                        break
                    if 'Timed out' in turn_status:
                        print('PZ-server said it timed out while waiting for my turn to come up...')
                        sleep(3)

                elif match_status in ['game over', 'scored, final']:
                    self.match_over(turn_data)
                    print('Game over')
                    return
                elif match_status == "awaiting more player(s)":
                    print('match has not started yet. sleeping a bit...')
                    sleep(5)
                else:
                    raise ValueError('Unexpected match_status: ' + match_status)

            next_move = self.fetch_move(turn_data)
            move_data = self.client.move(next_move, self.match_id)

            if move_data.content["match_status"] in ["game over", "scored, final"]:
                self.match_over(move_data.content)
                print('Game over')
                break

            sleep(3)

        return

    def fetch_history(self, turn_data, turn):
        print("self.history", self.history)
        print("turn", turn)
        if self.history.get(turn):
            print("1")
            print(self.history[turn])
            return self.history[turn]
        for each_move in turn_data.get('history'):
            if each_move.get('turn') == turn:
                print("each_move", each_move)
                return each_move

    def construct_base_moves_tree(self, temp, last_move):
        print("self.history", self.history)
        if self.history:
            for key in sorted(self.history):
                val = self.history[key]
                temp[val] = {}
                temp = temp[val]
        else:
            temp[last_move] = {}

    def fetch_visited(self):
        visited = []
        for v in self.history.values():
            visited.append( (int(v[0]), int(v[1]), int(v[2])) )
        return visited

    def update_prev_move(self, move, temp):
        for k,v in temp.items():
            if v.keys():
                self.update_prev_move(move, v)
            else:
                v[move] = {}

    def fetch_move(self, turn_data):
        curr_turn = turn_data.get('turn')
        if turn_data.get('turn') == 1 or curr_turn <= self.threshold:
            row, col, dir = self.fetch_random(curr_turn)
        else:
            if not self.moves_tree:
                move_data = self.fetch_history(turn_data, turn = curr_turn - 1)

                if isinstance(move_data, dict):
                    curr_move = literal_eval(move_data.get('move'))
                    row, col, dir = curr_move[0], curr_move[1], curr_move[2]
                    key = str(row) + str(col) + str(dir)
                else:
                    key = move_data
                    row, col, dir = int(key[0]), int(key[1]), int(key[2])

                root = {}
                self.construct_base_moves_tree(root)
                print("root", root)
                self.moves_tree = root
                print("self.moves_tree", self.moves_tree)
                tdict = self.moves_tree
                print("tdict", tdict)

                while tdict.items() and tdict.items()[0][0] != key:
                    tdict = tdict.items()[0][1]

                visited = self.fetch_visited()
                self.build_move_tree(tdict, key, visited)

            if self.player_num != 1:
                move_data = self.fetch_history(turn_data, turn = curr_turn - 1)
                curr_move = literal_eval(move_data.get('move'))
                row, col, dir = curr_move[0], curr_move[1], curr_move[2]
                key = str(row) + str(col) + str(dir)
                temp_tree = self.moves_tree
                self.update_prev_move(key, temp_tree)

            row, col, dir = self.fetch_next_move(turn_data)

        print('I moved as: ({}, {}) with direction: {} for match_id: {} for turn {}'.format(row, col, dir, self.match_id, curr_turn))
        return str((row, col, dir))


if __name__ == '__main__':
    # game_id = 14
    game_id = 15
    tp = TurningPoints(game_id)
    tp.lets_play()

    # r = Client()
    # r.resign_match(1321)
