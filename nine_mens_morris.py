# Implemented in Python 3.2
# Author: Sunanda Dadi

from copy import deepcopy
import random
import json
import os


class NineMensMorris(object):
    """docstring for NineMensMorris
        Variables:
            'empty_board' is the initial board state
            'game_board'  is the current board state

            'Player2' is computer
            'Player1' is human
            'empty_board' is the prototype of the game board
            'game_board' contains the current game with the placyed moves
            'pieces_map_to_coordinates' is a dictionary that maps a piece on game board to the coordinates of the 2D array
            'pieces_map_from_coordinates' is a dictionary that maps coordinates in a 2D array to the board piece
            'formed_mills' is a dictionary that tracks all the mills formed
            'file_path' is the name of the file where all the moves are recorded into and read from
            'file_data' is the data from the file at the start of the game
            'game_moves' is a nested dictionary that records moves played in a game
    """

    def __init__(self):
        self.empty_board = self.fetch_board()
        self.game_board = deepcopy(self.empty_board)
        self.game_board_length = len(self.game_board)
        self.pieces_map_to_coordinates, self.pieces_map_from_coordinates = self.construct_pieces_map()
        self.move_pieces = self.pieces_map_to_coordinates.keys()
        self.player1, self.player2 = 1, 2
        self.player1_pieces, self.player2_pieces = 9, 9
        self.game_over = False
        self.formed_mills = {}
        self.excluding_alpas = ['Y', 'Z']
        self.player1_won, self.player2_won = False, False
        self.player1_removed_piece, self.player2_removed_piece = False, False
        self.file_path, self.file_data = 'nine_mens.json', {}
        self.file_data_head = {}
        self.game_moves = {}
        self.game_moves_head = self.game_moves

    def current_empty_slots(self):
        ''' Returns the unoccupied slots on the game board'''
        a = []
        for row in range(len(self.game_board)):
            for col in range(len(self.game_board[row])):
                if self.game_board[row][col] not in [' ', self.player1, self.player2] :
                    a.append(self.game_board[row][col])
        return a

    def construct_pieces_map(self):
        ''' Return a dictionary that contains a mapping of pieces to game board coordinates and vice-a-versa'''
        a, b = {}, {}
        for row in range(len(self.empty_board)):
            for col in range(len(self.empty_board[row])):
                if self.empty_board[row][col] != ' ':
                    a[self.empty_board[row][col]] = (row, col)
                    b[(row, col)] = self.empty_board[row][col]
        return (a, b)

    def fetch_board(self):
        ''' Fetching the initial game empty board for the game - A 6x6 2d array '''
        board = []
        for i in range(7):
            if i == 0:
                t = ['A', ' ', ' ', 'B', ' ', ' ', 'C']
            elif i == 1:
                t = [' ', 'D', ' ', 'E', ' ', 'F', ' ']
            elif i == 2:
                t = [' ', ' ', 'G', 'H', 'I', ' ', ' ']
            elif i == 3:
                t = ['J', 'K', 'L', ' ', 'M', 'N', 'O']
            elif i == 4:
                t = [' ', ' ', 'P', 'Q', 'R', ' ', ' ']
            elif i == 5:
                t = [' ', 'S', ' ', 'T', ' ', 'U', ' ']
            elif i == 6:
                t = ['V', ' ', ' ', 'W', ' ', ' ', 'X']

            board.append(t)
        return board

    def pretty_print_board(self):
        ''' Pretty print the game board '''
        print('Current Game board looks like:')
        for row in self.game_board:
            for i in row:
                print(i, end = ' ')
            print()
        print('------------------------------------------------------------------------------------------------------')
        print('\n')

    def fetch_top_adjacent(self, start):
        ''' Fetch the coordinates of top adjacent position '''
        # (4, 3) - None
        a = None
        row, col = start
        if (row == 0) or (row == 4 and col == 3):
            return a

        while not a and row > 0:
            row = row - 1
            if self.empty_board[row][col] != ' ':
                a = (row, col)

        return a

    def fetch_bottom_adjacent(self, start):
        ''' Fetch the coordinates of bottom adjacent position '''
        # (2, 3) - None
        a = None
        row, col = start
        if (row == 6) or (row == 2 and col == 3):
            return a

        while not a and row < self.game_board_length - 1:
            row = row + 1
            if self.empty_board[row][col] != ' ':
                a = (row, col)

        return a

    def fetch_left_adjacent(self, start):
        ''' Fetch the coordinates of left adjacent position '''
        # (3, 4) - None
        a = None
        row, col = start
        if (col == 0) or (row == 3 and col == 4):
            return a

        while not a and col > 0:
            col = col - 1
            if self.empty_board[row][col] != ' ':
                a = (row, col)

        return a

    def fetch_right_adjacent(self, start):
        ''' Fetch the coordinates of right adjacent position '''
        # (3, 2) - None
        a = None
        row, col = start
        if (col == 6) or (row == 3 and col == 2):
            return a

        while not a and col < self.game_board_length - 1:
            col = col + 1
            if self.empty_board[row][col] != ' ':
                a = (row, col)

        return a

    def fetch_ajacents(self, start):
        ''' Fetch the coordinates of all adjacent positions '''
        adj = []
        adj.append(self.fetch_top_adjacent(start))
        adj.append(self.fetch_bottom_adjacent(start))
        adj.append(self.fetch_left_adjacent(start))
        adj.append(self.fetch_right_adjacent(start))
        adj = [x for x in adj if x is not None]
        return adj

    def check_move_adjacency(self, start, end):
        ''' Returns True if a coordinate is adjancent to another '''
        if end in self.fetch_ajacents(start):
            return True
        return False

    def write_to_file(self, data):
        ''' Writes to a file '''
        with open(self.file_path, 'w') as f:
            json.dump(data, f, ensure_ascii=False)
        return

    def read_from_file(self):
        ''' Reads from a file if exisits else creates a file '''
        if not os.path.isfile(self.file_path):
            return self.file_data
        with open(self.file_path) as f:
            return json.load(f)

    def update_file(self, key, val):
        ''' Updates data to a file '''
        file_data = self.read_from_file()
        file_data[key] = val

        with open(self.file_path, 'w') as f:
            json.dump(file_data, f, ensure_ascii=False)

    def is_valid_move(self, val, player):
        ''' Returns True if the user played a valid move '''
        first_pos, move_pos = val[0], val[1]
        first_pos_index = self.pieces_map_to_coordinates.get(first_pos)
        move_pos_index = self.pieces_map_to_coordinates.get(move_pos)

        # Check 1: see if player's piece exists on the first position
        row, col = first_pos_index
        if self.game_board[row][col] != player:
            print("Oops! You cannot make a move if your piece is not on ", first_pos)
            return False

        # Check 2: adjacency check. Bypassing adjacency check for winning move
        if not self.player1_won:
            if not self.check_move_adjacency(first_pos_index, move_pos_index):
                print("Oops! You can only move to adjacent cells and cannot move diagonally")
                return False

        # Check 3: If a move position is blocked by opponent. Player can only move to available slots
        row, col = move_pos_index
        if self.game_board[row][col] == self.player2:
            print("Oops! You cannot make a move if your opponent's piece is on ", move_pos)
            return False

        return True

    def validate_initial_moves(self, val, bypass=True):
        ''' Return True if a Phase-I move is valid '''
        if len(val) != 1:
            print("Oops! You need to enter a single alphabet")
            return False

        val = val.upper()
        if not val.isalpha():
            print("Oops! You need to enter alphabet")
            return False

        if bypass and val not in self.current_empty_slots():
            print("Oops! You cannot make this move as the slot is occupied")
            return False

        return True

    def validate_intermediate_moves(self, val):
        ''' Return True if a Phase-II move is valid '''
        if len(val) != 2:
            print("Oops! You need to enter a two alphabets (From and to Eg: AB indicates moving your piece from A to B)")
            return False

        val = val.upper()
        if not val.isalpha() or (val[0] in self.excluding_alpas or val[1] in self.excluding_alpas):
            print("Oops! You need to enter a valid alphabet")
            return False

        if not self.is_valid_move(val, self.player1):
            return False

        return True

    def validate_player_input(self, val):
        ''' Return True if a user move is valid '''
        if self.player1_pieces != 0:
            return self.validate_initial_moves(val)
        return self.validate_intermediate_moves(val)

    def fetch_third_row_col_mill_indices(self, half, horizontal=True):
        ''' Return the mill indices of third row and column '''
        a = tuple()
        lis = range(4,7) if half == 2 else range(3)
        if horizontal:
            for i in lis:
                a = a + ((3,i),)
        else:
            for i in lis:
                a = a + ((i,3),)
        return a


    def third_row_col_mill(self, temp, horizontal=True):
        ''' Return a dictionary with the formed mill indices of third row and column '''
        player_wins = {}
        if temp[0:3].count(self.player1) == 3:
            player_wins[self.fetch_third_row_col_mill_indices(1, horizontal)] = self.player1
        if temp[0:3].count(self.player2) == 3:
            player_wins[self.fetch_third_row_col_mill_indices(1, horizontal)] = self.player2

        if temp[4:7].count(self.player1) == 3:
            player_wins[self.fetch_third_row_col_mill_indices(2, horizontal)] = self.player1
        if temp[4:7].count(self.player2) == 3:
            player_wins[self.fetch_third_row_col_mill_indices(2, horizontal)] = self.player2

        return player_wins

    def fetch_horizonatal_mill_indices(self, row):
        ''' Return the mill indices of all horizontal mills '''
        a = tuple()
        for i, val in enumerate(self.empty_board[row]):
            if val != ' ':
                a = a + ((row, i),)
        return a

    def fetch_vertical_mill_indices(self, col):
        ''' Return the mill indices of all vertical mills '''
        a = tuple()
        for i in range(len(self.empty_board)):
            if self.empty_board[i][col] != ' ':
                a = a + ((i, col),)
        return a

    def horizontal_mill(self):
        ''' Return a dictionary with the formed horizontal mill indices '''
        player_wins = {}
        for n, row in enumerate(self.game_board):
            # Edge case: handled separately
            if n == 3:
                player_wins.update(self.third_row_col_mill(row))
            else:
                if row.count(self.player1) == 3:
                    player_wins[self.fetch_horizonatal_mill_indices(n)] = self.player1
                if row.count(self.player2) == 3:
                    player_wins[self.fetch_horizonatal_mill_indices(n)] = self.player2

        return player_wins

    def vertical_mill(self):
        ''' Return a dictionary with the formed vertical mill indices '''
        player_wins = {}
        for col in range(len(self.game_board)):
            temp = {self.player1: 0, self.player2: 0}
            # Edge case: handled separately
            if col == 3:
                temp = []
                for row in range(len(self.game_board)):
                    temp.append(self.game_board[row][col])
                player_wins.update(self.third_row_col_mill(temp, horizontal=False))
                continue

            for row in range(len(self.game_board)):
                if self.game_board[row][col] == self.player1:
                    temp[self.player1] = temp[self.player1] + 1
                elif self.game_board[row][col] == self.player2:
                    temp[self.player2] = temp[self.player2] + 1

            if temp.get(self.player1) == 3:
                player_wins[self.fetch_vertical_mill_indices(col)] = self.player1
            if temp.get(self.player2) == 3:
                player_wins[self.fetch_vertical_mill_indices(col)] = self.player2

        return player_wins

    def fetch_player_indices(self, player):
        ''' Return a list of the indices a player played at '''
        pos = []
        for row in range(len(self.game_board)):
            for col in range(len(self.game_board[row])):
                if self.game_board[row][col] == player:
                    pos.append((row, col))
        return pos

    def fetch_machine_win_move(self):
        ''' Return a move when the machine needs to remove an opponent's piece '''
        move, forbidden_moves = self.fetch_smart_move(phase=3)
        if move:
            row, col = self.pieces_map_to_coordinates.get(move)
        else:
            a = self.fetch_player_indices(self.player1)
            r = random.choice(a)
            row, col = r

        self.game_board[row][col] = self.empty_board[row][col]
        print("Yay! I won! I choose to remove: ", self.empty_board[row][col])
        self.add_to_game_move(self.empty_board[row][col], phase=3, player=self.player2)
        self.player2_removed_piece = True
        self.pretty_print_board()

    def fetch_player_win_move(self):
        ''' Validates and updates a move when the user removes an opponent's piece '''
        valid = False
        while not valid:
            val = input("Yay! We have a winner! You may remove one of your opponent piece\n")
            val = val.upper()
            valid = self.validate_initial_moves(val, bypass=False)
            row, col = self.pieces_map_to_coordinates.get(val)
            if self.game_board[row][col] != self.player2:
                print("Oops! Try Again! You should choose a move where your opponent's piece lies.")
                valid = False

        self.add_to_game_move(self.empty_board[row][col], phase=3, player=self.player1)
        self.game_board[row][col] = self.empty_board[row][col]
        self.player1_removed_piece = True
        self.pretty_print_board()

    def remove_non_existant_mills(self):
        ''' Removes mills from formed_mills if they are no longer exist on the game board '''
        temp = deepcopy(self.formed_mills)
        for key, val in temp.items():
            for i in key:
                row, col = i
                if self.game_board[row][col] != val:
                    self.formed_mills.pop(key)
                    break
        return

    def check_for_mill(self):
        ''' Updates if a player formed a mills on the game board '''
        self.remove_non_existant_mills()
        player_wins = {}
        player_wins.update(self.horizontal_mill())
        player_wins.update(self.vertical_mill())
        if not player_wins or self.is_game_over():
            return

        for key, val in player_wins.items():
            if self.formed_mills.get(key) != val:
                self.formed_mills[key] = val

                if val == self.player1:
                    self.add_to_moves_tree(wins=False)
                    self.fetch_player_win_move()
                    self.player1_won = True
                else:
                    self.add_to_moves_tree(wins=True)
                    self.fetch_machine_win_move()
                    self.player2_won = True

        return

    def fetch_machine_intermediate_move(self):
        ''' Return a Phase-II move '''
        smart_move, forbidden_moves = self.fetch_smart_move(phase=2)
        if smart_move:
            start, end = smart_move[0], smart_move[1]
            start = self.pieces_map_to_coordinates.get(start)
            end = self.pieces_map_to_coordinates.get(end)
            row2, col2 = end

        valid = False
        while not smart_move and not valid:
            pos = self.fetch_player_indices(self.player2)
            start = random.choice(pos)
            if not self.player2_won:
                next = self.fetch_ajacents(start)
                if next:
                    end = random.choice(next)
                    row2, col2 = end
                    if self.game_board[row2][col2] in self.move_pieces:
                        valid = True
            else:
                e = self.current_empty_slots()
                rand = random.choice(e)
                end = self.pieces_map_to_coordinates.get(rand)
                row2, col2 = end
                valid = True

        row1, col1 = start
        self.game_board[row1][col1] = self.empty_board[row1][col1]
        self.game_board[row2][col2] = self.player2
        final_move = self.pieces_map_from_coordinates.get(start) + self.pieces_map_from_coordinates.get(end)
        if final_move in forbidden_moves:
            self.fetch_machine_intermediate_move()
        else:
            return final_move

    def fetch_key_check(self, data):
        ''' Return the key depending on the player '''
        if data.get('player') == self.player1:
            key_check = 'looses'
        else:
            key_check = 'wins'
        return key_check

    def fetch_smart_move(self, phase):
        ''' Returns a smart move by reading from the past moves '''
        smart_move, forbidden_moves = None, []
        if not self.file_data_head:
            return smart_move, forbidden_moves

        # First move:
        if not self.file_data_head.get('player'):
            max = 0
            for key, val in self.file_data_head.items():
                key_check = self.fetch_key_check(val)
                if val.get(key_check) > max:
                    max = val[key_check]
                    smart_move = key

            forbidden_moves = list(set(self.file_data_head.keys() or []) - set([smart_move] or []))
            return smart_move, forbidden_moves

        key_check = self.fetch_key_check(self.file_data_head)
        if self.file_data_head.get(key_check) > 0 and self.file_data_head.get('phase') == phase:
            if len(self.file_data_head.get('move')) == 1:
                smart_move = self.file_data_head['move']
            elif len(self.file_data_head['move'] > 1):
                # Fetch best move
                max = 0
                for key,val in self.file_data_head['move']:
                    if val.get(key_check) > max:
                        max = val[key_check]
                        smart_move = key
                forbidden_moves = list(set(self.file_data_head['move'].keys()) - set(smart_move))

        elif self.file_data_head.get('phase') == phase:
            forbidden_moves = self.file_data_head.get('move').keys()

        return smart_move, forbidden_moves


    def fetch_machine_input(self):
        ''' Returns machine move '''
        if self.player2_pieces == 0:
            print("I have " + str(self.player2_pieces) + " pieces remaining. I choose to make my move as ")
            move = self.fetch_machine_intermediate_move()
            self.add_to_game_move(move, phase=2, player=self.player2)
        else:
            print("I have " + str(self.player2_pieces) + " pieces remaining. I choose to make my move as ")
            move, forbidden_moves = self.fetch_smart_move(phase=1)
            if not move:
                e = self.current_empty_slots()
                e = list(set(e) - set(forbidden_moves))
                move = random.choice(e)

            row, col = self.pieces_map_to_coordinates.get(move)
            self.game_board[row][col] = self.player2
            if self.player2_pieces != 0:
                self.player2_pieces = self.player2_pieces - 1
            self.add_to_game_move(move, phase=1, player=self.player2)

        print(move)
        self.pretty_print_board()
        self.check_for_mill()

        if self.player2_won and not self.player2_removed_piece:
            self.player2_won = False

        self.player2_removed_piece = False
        return

    def format_user_question(self):
        ''' Returns question to be asked to player '''
        if self.player1_won and self.player1_pieces == 0:
            return "As you created a mill in your previous move. You are rewarded to jump over pieces i.e., " + \
                "your moves no longer need to be adjacent. You have " + str(self.player1_pieces) + \
            " pieces remaining. Please enter your move\n"
        else:
            return "It's your turn to make a move. You have " + str(self.player1_pieces) + \
            " pieces remaining. Please enter your move\n"

    def search_file_data_head(self, val, phase):
        ''' Searches the file head from read file data '''
        if not self.file_data_head:
            return
        if self.file_data_head.get(val):
            self.file_data_head = self.file_data_head[val]['move']
        else:
            self.file_data_head = {}
        return

    def add_to_game_move(self, val, phase, player):
        ''' Records all the game moves '''
        if not self.game_moves_head:
            self.game_moves[val] = { 'wins': 0, 'looses': 0, 'phase': phase, 'player': player, 'move': {} }
            self.game_moves = self.game_moves[val]
        else:
            a = {}
            a[val] = { 'wins': 0, 'looses': 0, 'phase': phase, 'player': player, 'move': {} }
            self.game_moves['move'] = a
            self.game_moves = self.game_moves['move'][val]

        self.search_file_data_head(val, phase)
        return

    def mark_loss_in_moves_tree(self, data):
        ''' Return after incrementing looses in the recorded tree '''
        for key, val in data.items():
            if isinstance(val, dict):
                self.mark_loss_in_moves_tree(val)
            elif key == 'looses':
                data['looses'] = data['looses'] + 1
        return data

    def mark_wins_in_moves_tree(self, data):
        ''' Return after incrementing wins in the recorded tree '''
        for key, val in data.items():
            if isinstance(val, dict):
                self.mark_wins_in_moves_tree(val)
            elif key == 'wins':
                data['wins'] = data['wins'] + 1
        return data

    def add_to_moves_tree(self, wins):
        ''' Marks wins or looses int the recorded tree '''
        temp_head = self.game_moves_head
        if wins:
            self.mark_wins_in_moves_tree(temp_head)
        else:
            self.mark_loss_in_moves_tree(temp_head)
        return

    def fetch_player_input(self):
        ''' Fetches and Validates players input '''
        valid = False
        while not valid:
            ques = self.format_user_question()
            val = input(ques)
            val = val.upper()
            valid = self.validate_player_input(val)

        if len(val) == 2:
            user_in = val
            init, val = val[0], val[1]
            row, col = self.pieces_map_to_coordinates.get(init)
            self.game_board[row][col] = init
            self.add_to_game_move(user_in, phase=2, player=self.player1)
        else:
            self.add_to_game_move(val, phase=1, player=self.player1)

        row, col = self.pieces_map_to_coordinates.get(val)

        self.game_board[row][col] = self.player1
        if self.player1_pieces != 0:
            self.player1_pieces = self.player1_pieces - 1
        self.pretty_print_board()
        self.check_for_mill()

        if self.player1_won and not self.player1_removed_piece:
            self.player1_won = False

        self.player1_removed_piece = False
        return

    def is_game_over(self):
        ''' Returns True if the game is over '''
        # If either players have only 2 pieces remaining
        a = {self.player1: 0, self.player2: 0}
        for row in range(len(self.game_board)):
            for col in range(len(self.game_board[row])):
                if self.game_board[row][col] == self.player1:
                    a[self.player1] += 1
                if self.game_board[row][col] == self.player2:
                    a[self.player2] += 1
        if (self.player1_pieces == 0 and a[self.player1] == 2) or (self.player2_pieces == 0 and a[self.player2] == 2):
            if a[self.player2] == 2:
                print("Yay! You won the game!")
            else:
                print("Yay! Player 2 AKA I won the game!")
            return True
        return False

    def fetch_next_player(self, c):
        ''' Returns the next player to play their turn '''
        if c == self.player1:
            return self.player2
        return self.player1

    def merge(self, a, b, path=None):
        ''' Returns merged dictionary '''
        "merging b into a"
        if path is None:
            path = []

        for key in b:
            if key in a:
                if isinstance(a[key], dict) and isinstance(b[key], dict):
                    self.merge(a[key], b[key], path + [str(key)])
                elif a[key] == b[key]:
                    pass
                else:
                    a[key] = b[key]
            else:
                a[key] = b[key]
        return a


    def record_moves_to_file(self):
        ''' Records moves played to a file '''
        write_data = self.game_moves_head
        file_data = self.merge(self.file_data, write_data) if self.file_data else write_data
        self.write_to_file(file_data)

    def start_game(self):
        ''' Start of the game '''
        self.file_data = self.read_from_file()
        self.file_data_head = self.file_data
        print('You are Player - \'1\' and I am \'Player2\'')
        self.pretty_print_board()

        c = random.choice([self.player1, self.player2])
        if c == self.player1:
            print('You have been chosen to make the first move')
            self.fetch_player_input()
        else:
            print('Looks like I chose myself to make the first move')
            self.fetch_machine_input()

        while not self.is_game_over():
            c = self.fetch_next_player(c)
            if c == self.player1:
                self.fetch_player_input()
            else:
                self.fetch_machine_input()
        self.record_moves_to_file()


if __name__ == '__main__':
    a = NineMensMorris()
    a.start_game()
