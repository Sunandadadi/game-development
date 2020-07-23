from client import Client, SuccessResponse, Settings
from itertools import permutations
from scipy.ndimage import label
from copy import deepcopy
from time import sleep
import numpy as np

class Constants(object):
    sixbysix = 3 # 4 regions
    eightbyeight = 4 # 4 regions
    twelvebyfifteen = 8 # 9 regions

class GridChecks(object):

    def check_adjacency(self, board):
        max_row = len(board) - 1
        max_col = len(board[0]) - 1
        for row, lst in enumerate(board):
            for col, val in enumerate(lst):
                cont = False
                if (row < max_row) and (board[row+1][col] in [val, " "]):
                    cont = True
                elif (row > 0) and (board[row-1][col] in [val, " "]):
                    cont = True
                elif (col < max_col) and (board[row][col+1] in [val, " "]):
                    cont = True
                elif (col > 0) and (board[row][col-1] in [val, " "]):
                    cont = True

                if not cont:
                    break
            else:
                continue
            break

        return cont

    def check_totals(self, board, max):
        possible_vals = set()
        for row in board:
            vals = set(row)
            possible_vals.update(vals)
        if " " in possible_vals:
            possible_vals.remove(" ")

        totals_okay = True
        for v in possible_vals:
            if sum(row.count(v) for row in board) > max:
                totals_okay = False

        return totals_okay

    @staticmethod
    def perform_checks(game_id, board):
        if game_id == Constants.sixbysix:
            max = (6*6) / 4
        elif game_id == Constants.eightbyeight:
            max = (8*8) / 4
        elif game_id == Constants.twelvebyfifteen:
            max = (12*15) / 9

        passing = True
        gc = GridChecks()

        if not gc.check_adjacency(board):
            passing = False
        if not gc.check_totals(board, max):
            passing = False

        return passing

    @staticmethod
    def check_contiguity(board):
        contiguous_regions = True
        grid = np.array(board)
        regions = np.unique(grid)
        for r in regions:
            r_grid = grid == r
            r_grid = r_grid.astype(np.int)
            labeled_array, num_features = label(r_grid)
            if num_features > 1:
                contiguous_regions = False

        return contiguous_regions


class Grid(object):

    @staticmethod
    def sixbysix_dimensions():
        return (6, 6)

    @staticmethod
    def eightbyeight_dimensions():
        return (8, 8)

    @staticmethod
    def twelvebyfifteen_dimensions():
        return (12, 15)

    @staticmethod
    def sixbysix(hardcoded=False):
        if not hardcoded:
            return ["aaaadb", "addadb", "acdddb", "acdbdb", "acbbbb", "cccccc"]
        else:
            startergrid = [
                ['a', 'a', 'a', 'b', 'b', 'b'],
                ['a', 'a', 'a', 'b', 'b', 'b'],
                ['a', 'a', 'a', 'b', 'b', 'b'],
                ['c', 'c', 'c', 'd', 'd', 'd'],
                ['c', 'c', 'c', 'd', 'd', 'd'],
                ['c', 'c', 'c', 'd', 'd', 'd']
            ]

    @staticmethod
    def eightbyeight(hardcoded=False):
        if not hardcoded:
            return ["rggggggg", "rrgggggg", "rrgrgygy", "rrrrryyy", "rrrrryoo", "yyyyyyoo", "yyyyoooo", "oooooooo"]
        else:
            startergrid = [
                ['a', 'a', 'a', 'a', 'b', 'b', 'b', 'b'],
                ['a', 'a', 'a', 'a', 'b', 'b', 'b', 'b'],
                ['a', 'a', 'a', 'a', 'b', 'b', 'b', 'b'],
                ['a', 'a', 'a', 'a', 'b', 'b', 'b', 'b'],
                ['c', 'c', 'c', 'c', 'd', 'd', 'd', 'd'],
                ['c', 'c', 'c', 'c', 'd', 'd', 'd', 'd'],
                ['c', 'c', 'c', 'c', 'd', 'd', 'd', 'd'],
                ['c', 'c', 'c', 'c', 'd', 'd', 'd', 'd']
            ]


    @staticmethod
    def twelvebyfifteen(hardcoded=False):
        if not hardcoded:
            return ["rrlllllllllpppp", "oreeellpppppiip", "orrreelllllpiip", "oooreeelppppiip",
                    "yogrrrelllbbiip", "yogggreeeebbiip", "yooogrrreebbbip", "yogggggreeebiii",
                    "yooooogrrrebiii", "yyyogggggrebbbi", "yoooyyyygrbbbbi", "yyyyyyygggbbbbi"]
        else:
            startergrid = [
                ['a', 'a', 'a', 'a', 'a', 'b', 'b', 'b', 'b', 'b', 'c', 'c', 'c', 'c', 'c'],
                ['a', 'a', 'a', 'a', 'a', 'b', 'b', 'b', 'b', 'b', 'c', 'c', 'c', 'c', 'c'],
                ['a', 'a', 'a', 'a', 'a', 'b', 'b', 'b', 'b', 'b', 'c', 'c', 'c', 'c', 'c'],
                ['a', 'a', 'a', 'a', 'a', 'b', 'b', 'b', 'b', 'b', 'c', 'c', 'c', 'c', 'c'],
                ['d', 'd', 'd', 'd', 'd', 'e', 'e', 'e', 'e', 'e', 'f', 'f', 'f', 'f', 'f'],
                ['d', 'd', 'd', 'd', 'd', 'e', 'e', 'e', 'e', 'e', 'f', 'f', 'f', 'f', 'f'],
                ['d', 'd', 'd', 'd', 'd', 'e', 'e', 'e', 'e', 'e', 'f', 'f', 'f', 'f', 'f'],
                ['d', 'd', 'd', 'd', 'd', 'e', 'e', 'e', 'e', 'e', 'f', 'f', 'f', 'f', 'f'],
                ['g', 'g', 'g', 'g', 'g', 'h', 'h', 'h', 'h', 'h', 'i', 'i', 'i', 'i', 'i'],
                ['g', 'g', 'g', 'g', 'g', 'h', 'h', 'h', 'h', 'h', 'i', 'i', 'i', 'i', 'i'],
                ['g', 'g', 'g', 'g', 'g', 'h', 'h', 'h', 'h', 'h', 'i', 'i', 'i', 'i', 'i'],
                ['g', 'g', 'g', 'g', 'g', 'h', 'h', 'h', 'h', 'h', 'i', 'i', 'i', 'i', 'i']
            ]

class Lap(object):
    def __init__(self, game_id):
        self.game_id = game_id
        self.client = Client()
        self.my_board = self.fetch_board()
        self.match_id = self.fetch_match_id()
        self.total_rows, self.total_cols = self.fetch_grid_dimensions()
        self.last_clue = None
        self.player_order = None
        self.possible_grids = []
        self.empty_grid = self.construct_empty_grid()
        self.clue_moves = []
        self.last_clue_grids = None
        self.last_move = False

    def fetch_player_order(self, players):
        for player in players:
            if player.get('netid') == Settings.netid:
                self.player_order = player.get('player_order')
                break
        return

    def check_match_history(self):
        r = self.client.fetch_match_history(self.match_id)
        players = r.content.get('players')
        if not players:
            return
        self.fetch_player_order(players)

        history = r.content.get('history')
        if not history:
            return
        # print("history", history)
        self.construct_from_history(history)

    def fetch_cells_from_move(self, row, col):
        return [(row, col), (row, col + 1), (row + 1, col), (row + 1, col + 1)]

    def convert_move(self, move):
        move = move.strip('()').split(', ')
        row, col = int(move[0]), int(move[1])
        return (row, col)

    def fetch_past_grid(self):
        if not self.possible_grids:
            return [self.empty_grid]
        return self.possible_grids

    def final_dimensions(self, row, col):
        if row == self.total_rows - 2 and col == self.total_cols - 2:
            return True
        return False

    def construct_possible_grids(self, row, col, clue):
        clues = list(str(clue))
        move_permutations = set(list(permutations(clues)))
        possible_cells = self.fetch_cells_from_move(row, col)
        grids = self.fetch_past_grid()
        move_grids = []

        for g in grids:

            for move in move_permutations:
                new_g = deepcopy(g)

                for cell, m in zip(possible_cells, move):
                    r, c = cell[0], cell[1]
                    new_g[r][c] = m

                if GridChecks.perform_checks(self.game_id, new_g) and new_g not in move_grids:
                    if self.final_dimensions(row, col):
                        if GridChecks.check_contiguity(new_g):
                            self.last_move = True
                            move_grids.append(new_g)
                    else:
                        move_grids.append(new_g)

        return move_grids

    def clue_moves_exist(self, move):
        if move not in self.clue_moves:
            self.clue_moves.append(move)
        return

    def convert_string_to_grid(self, move):
        l = str(move).strip('[]\'').split(', ')
        f = []
        for i in l:
            f.append(list(i.strip('"')))
        return f

    def remove_result_from_possibilities(self, move):
        possible_grids = self.possible_grids
        move = self.convert_string_to_grid(move)
        for pg in possible_grids:
            if pg == move:
                possible_grids.remove(pg)

        self.possible_grids = possible_grids
        return


    def construct_from_history(self, history):
        # Sorting history in ascending order of player moves
        history.reverse()
        for h in history:
            if h.get('result').startswith('clue') and h.get('player_num') == self.player_order:
                move = h.get('move')
                result = h.get('result').lstrip('clue:')
                row, col = self.convert_move(move)
                self.clue_moves_exist((row, col))
                self.possible_grids = self.construct_possible_grids(row, col, result)

            elif h.get('player_num') == self.player_order and h.get('result') == 'You have guessed incorrectly.':
                self.remove_result_from_possibilities(h['move'])

    def fetch_match_id(self):
        r = self.client.fetch_match_id(self.game_id)
        return r.content.get('match_id')

    def fetch_board(self):
        if self.game_id == Constants.sixbysix:
            return Grid.sixbysix()
        elif self.game_id == Constants.eightbyeight:
            return Grid.eightbyeight()
        elif self.game_id == Constants.twelvebyfifteen:
            return Grid.twelvebyfifteen()

    def pretty_print_grid(self, board):
        for i in board:
            print(i)
        print('-----------------------------------')
        return

    def fetch_grid_dimensions(self):
        if self.game_id == Constants.sixbysix:
            trows, tcols = Grid.sixbysix_dimensions()
        elif self.game_id == Constants.eightbyeight:
            trows, tcols = Grid.eightbyeight_dimensions()
        elif self.game_id == Constants.twelvebyfifteen:
            trows, tcols = Grid.twelvebyfifteen_dimensions()
        return trows, tcols

    def construct_empty_grid(self):
        grid = []
        for i in range(self.total_rows):
            grid.append([' '] * self.total_cols)
        return grid

    def fetch_clue(self):
        if not self.clue_moves:
            return str((0, 0))
        last_clue = self.clue_moves[-1]
        row, col = last_clue[0], last_clue[1]
        if col + 2 < self.total_cols:
            return str((row, col + 2))
        elif col + 2 == self.total_cols:
            if row + 2 < self.total_rows:
                return str((row + 2, 0))
        return

    def final_grid(self, grid):
        f = []
        for i in grid:
            f.append(''.join(i))
        return f

    def fetch_move(self, turn_data):
        curr_turn = turn_data.get('turn')
        if curr_turn == 1 or curr_turn == 2:
            return self.my_board
        if self.last_move:
            return self.final_grid(self.possible_grids[0])
        return self.fetch_clue()

    def process_clue(self, clue_data):
        if clue_data.get('turn') == 1 or clue_data.get('turn') == 2:
            return

        clue = clue_data.get('outcome')
        if not clue:
            return

        if clue == 'You have guessed incorrectly.':
            self.remove_result_from_possibilities(clue_data.get('your_move'))
        elif clue == 'You are correct!':
            return
        else:
            clue = clue.lstrip('clue:')
            move = clue_data.get('your_move')
            row, col = self.convert_move(move)
            self.possible_grids = self.construct_possible_grids(row, col, clue)
        return

    def start_game(self):
        while True:

            while True:
                turn_data = self.client.fetch_turn(self.match_id).content
                print("turn_data", turn_data)
                match_status = turn_data.get('match_status')
                if match_status == 'in play':
                    turn_status = turn_data.get('turn_status')
                    if turn_status == 'your turn':
                        break
                    if 'Timed out' in turn_status:
                        print('PZ-server said it timed out while waiting for my turn to come up...')
                        sleep(3)

                elif match_status in ['game over', 'scored, final']:
                    print('Game over')
                    return
                elif match_status == "awaiting more player(s)":
                    print('match has not started yet. sleeping a bit...')
                    sleep(5)
                else:
                    raise ValueError('Unexpected match_status: ' + match_status)

            self.check_match_history()
            next_move = self.fetch_move(turn_data)
            print("Making my move as", next_move)

            move_data = self.client.move(next_move, self.match_id)
            self.process_clue(move_data.content)

            if move_data.content["match_status"] in ["game over", "scored, final"]:
                print("move_data", move_data.content)
                print('Game over')
                break
            print('----------------------------------------------------------------------')
            sleep(3)

        return

if __name__ == '__main__':
    # game_id = Constants.sixbysix
    # lp = Lap(game_id)
    # lp.start_game()

    r = Client()
    print(r.resign_match(1430))
