# Group members: Sunanda(netid: sdadi2), Jenna Jordan(netid:jaj5)
import copy
import random
import itertools

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

    def vacant_cells(self, rules):
        v = []
        puzzle = rules['puzzle']
        for i in range(rules['height']):
            for j in range(rules['width']):
                if puzzle[i][j] == ' ':
                    v.append((i, j))
        return v

    def rows_without_mirrors(self, puzzle, width, height):
        ''' Retuns a list of rows indices that do not have a mirror
        '''
        rows = []
        for i in range(height):
            mirror = False
            for j in range(width):
                if puzzle[i][j] == '/' or puzzle[i][j] == '\\':
                    mirror = True
                    break
            if not mirror:
                rows.append(i)
        return rows

    def cols_without_mirrors(self, puzzle, width, height):
        ''' Retuns a list of column indices that do not have a mirror
        '''
        cols = []
        for i in range(width):
            mirror = False
            for j in range(height):
                if puzzle[i][j] == '/' or puzzle[i][j] == '\\':
                    mirror = True
                    break
            if not mirror:
                cols.append(i)
        return cols

    def equal_empty_rows_cols(self, rules, cols, rows):
        ''' If no mirror exisits in a row or column, the monster count top and bottom view of the ith column
            or the monster count left and right view of the ith row must be same
        '''
        top, bottom = rules['top'], rules['bottom']
        for i in cols:
            if top[i] != bottom[i]:
                return False

        left, right = rules['left'], rules['right']
        for i in rows:
            if left[i] != right[i]:
                return False
        return True


    def rule_violation(self, rules, paths, vacant_cells):
        '''
            Check 1: Rows or Columns without mirrors must have same monster count
            Check 2: Hints about monters seen from either side must be less than or equal to the total reachable cells
        '''
        rows = self.rows_without_mirrors(rules['puzzle'], rules['width'], rules['height'])
        cols = self.rows_without_mirrors(rules['puzzle'], rules['width'], rules['height'])
        if not self.equal_empty_rows_cols(rules, cols, rows):
            return True

        for p in paths:
            visible_cell_count = len(list(filter(lambda x: x == ' ', p['path_values'])))
            if p['hint'] > visible_cell_count:
                return True
        return False

    def find_next_mirror(self, idx, rules, view):
        # Find the coordinates of next mirror in the path of view
        puzzle = rules['puzzle']
        if view == 'top':
            for i in range(idx, rules['height']):
                if puzzle[idx][i] == '/' or puzzle[idx][i] == '\\':
                    return ((idx, i))

        elif view == 'bottom':
            for i in range(rules['height']):
                if puzzle[idx][i] == '/' or puzzle[idx][i] == '\\':
                    return ((idx, i))


    def update_zero(self, puzzle, idx, path_coords, path_values):
        # If monster's seen from border 0, then border cells must be Ghosts and reflections must be Vampires
        mirror = False
        for pc,pv in zip(path_coords, path_values):
            if pv == 'M':
                mirror = True
            else:
                if mirror == False:
                    puzzle[pc[0]][pc[1]] = 'G'
                else:
                    puzzle[pc[0]][pc[1]] = 'V'
        return puzzle

    def find_possibilities(self, rules, paths):
        puzzle = rules['puzzle']
        for p in paths:
            if p['hint'] == 0:
                puzzle = self.update_zero(puzzle, p['index'], p['path_coords'], p['path_values'])

        print("Found one solution")
        print(puzzle)
        return puzzle, True

    def find_solutions(self, rules):
        paths = self.find_paths(rules)
        vacant_cells = self.vacant_cells(rules)
        if not self.is_valid_puzzle(rules, paths, vacant_cells):
            return False

        found = self.find_possibilities(rules, paths)
        return found

    def is_valid_puzzle(self, rules, paths, vacant_cells):
        # need to add more rules. This one only check for all empty cells and all filled cells
        if self.rule_violation(rules, paths, vacant_cells):
            return False
        flat = set(rules['flat'])
        return True if len(flat) > 1 and ' ' in flat else False

    def randomize_view(self, rules, flat_view, height=False):
        max = len(list(filter(lambda x: x == ' ', flat_view)))
        r = 'width' if not height else 'height'
        view = random.choices(range(2+1), k=rules[r])
        return view

    def randomize_puzzle(self, height, temp_matrix, permutations):
        count, temp = 0, copy.deepcopy(temp_matrix)
        while count < height:
            temp[count] = random.choice(permutations)
            count += 1
        return temp

    def randomize_rules(self, rules, temp_matrix, permutations):
        puzzle = self.randomize_puzzle(rules['height'], temp_matrix, permutations)
        flat_view = list(itertools.chain.from_iterable(puzzle))

        return {
                'puzzle': puzzle,
                'flat': flat_view,
                'top': self.randomize_view(rules, flat_view),
                'bottom': self.randomize_view(rules, flat_view),
                'left': self.randomize_view(rules, flat_view, height=True),
                'right': self.randomize_view(rules, flat_view, height=True)
            }

    def generate_puzzle(self, height: int, width: int):
        '''
            Create a different valid Haunted Maze puzzle each time. Number of monsters and positions of mirrors will be random.
            Solution to the puzzle should go to a file.
        '''
        permutations = list(map(lambda x: list(x), itertools.product(['\\', '/', ' '], repeat=width)))

        temp_matrix = [[' ']*width]*height
        rules = {'height': height, 'width': width}
        rules.update(self.randomize_rules(rules, temp_matrix, permutations))

        while not self.find_solutions(rules):
            rules.update(self.randomize_rules(rules, temp_matrix, permutations))


    def find_next_cell(self, current_coord: tuple, current_cell: str, orientation: str):
        row, column = current_coord[0], current_coord[1]

        if orientation == "down":
            if current_cell == " ":
                row += 1
            elif current_cell == "\\":
                column += 1
                orientation = "right"
            elif current_cell == "/":
                column -= 1
                orientation = "left"
        elif orientation == "top":
            if current_cell == " ":
                row -= 1
            elif current_cell == "\\":
                column -= 1
                orientation = "left"
            elif current_cell == "/":
                column += 1
                orientation = "right"
        elif orientation == "left":
            if current_cell == " ":
                column -= 1
            elif current_cell == "\\":
                row -= 1
                orientation = "top"
            elif current_cell == "/":
                row += 1
                orientation = "down"
        elif orientation == "right":
            if current_cell == " ":
                column += 1
            elif current_cell == "\\":
                row += 1
                orientation = "down"
            elif current_cell == "/":
                row += 1
                orientation = "top"

        return (row, column), orientation


    def find_paths(self, rules: dict):
      # initialize returned dict of paths
      all_paths = []
      # puzzle dimensions
      puzzle = rules['puzzle']
      h = rules['height']
      w = rules['width']

      # find all "top" paths
      for i in range(w):
        num = rules['top'][i]

        orientation = "down"
        end_of_path = False

        # initialize values, to be updated as next cells in path are found
        row, column = 0, i
        current_cell = puzzle[row][column]
        current_coord = (row, column)

        # initialize path lists, to be appended with next values
        path_coords = [current_coord]
        path_values = []
        if (current_cell == "/") or (current_cell == "\\"):
          path_values.append("M")
        else:
          path_values.append(" ")

      # find the complete path
        while not end_of_path:
          current_coord, orientation = self.find_next_cell(current_coord, current_cell, orientation)
          row, column = current_coord[0], current_coord[1]

          if (row < 0) or (row >= h) or (column < 0) or (column >= w):
            end_of_path = True
          else:
            current_cell = puzzle[row][column]
            path_coords.append(current_coord)
            if (current_cell == "/") or (current_cell == "\\"):
              path_values.append("M")
            else:
              path_values.append(" ")

        # add these paths to the full path list
        path = {'view': 'top', 'index':i, 'hint': num, 'path_values': path_values, 'path_coords': path_coords}
        all_paths.append(path)


      # find all "bottom" paths
      for i in range(w):
        num = rules['bottom'][i]

        orientation = "top"
        end_of_path = False

        # initialize values, to be updated as next cells in path are found
        row, column = h-1, i
        current_cell = puzzle[row][column]
        current_coord = (row, column)

        # initialize path lists, to be appended with next values
        path_coords = [current_coord]
        path_values = []
        if (current_cell == "/") or (current_cell == "\\"):
          path_values.append("M")
        else:
          path_values.append(" ")

        # find the complete path
        while not end_of_path:
          current_coord, orientation = self.find_next_cell(current_coord, current_cell, orientation)
          row, column = current_coord[0], current_coord[1]

          if (row < 0) or (row >= h) or (column < 0) or (column >= w):
            end_of_path = True
          else:
            current_cell = puzzle[row][column]
            path_coords.append(current_coord)
            if (current_cell == "/") or (current_cell == "\\"):
              path_values.append("M")
            else:
              path_values.append(" ")

        # add these paths to the full path list
        path = {'view': 'bottom', 'index':i, 'hint': num, 'path_values': path_values, 'path_coords': path_coords}
        all_paths.append(path)

      # find all "left" paths
      for i in range(h):
        num = rules['left'][i]

        orientation = "right"
        end_of_path = False

        # initialize values, to be updated as next cells in path are found
        row, column = i, 0
        current_cell = puzzle[row][column]
        current_coord = (row, column)

        # initialize path lists, to be appended with next values
        path_coords = [current_coord]
        path_values = []
        if (current_cell == "/") or (current_cell == "\\"):
          path_values.append("M")
        else:
          path_values.append(" ")

      # find the complete path
        while not end_of_path:
          current_coord, orientation = self.find_next_cell(current_coord, current_cell, orientation)
          row, column = current_coord[0], current_coord[1]

          if (row < 0) or (row >= h) or (column < 0) or (column >= w):
            end_of_path = True
          else:
            current_cell = puzzle[row][column]
            path_coords.append(current_coord)
            if (current_cell == "/") or (current_cell == "\\"):
              path_values.append("M")
            else:
              path_values.append(" ")

        # add these paths to the full path list
        path = {'view': 'left', 'index':i, 'hint': num, 'path_values': path_values, 'path_coords': path_coords}
        all_paths.append(path)

      # find all "right" paths
      for i in range(w):
        num = rules['right'][i]

        orientation = "left"
        end_of_path = False

        # initialize values, to be updated as next cells in path are found
        row, column = i, w-1
        current_cell = puzzle[row][column]
        current_coord = (row, column)

        # initialize path lists, to be appended with next values
        path_coords = [current_coord]
        path_values = []
        if (current_cell == "/") or (current_cell == "\\"):
          path_values.append("M")
        else:
          path_values.append(" ")

        # find the complete path
        while not end_of_path:
          current_coord, orientation = self.find_next_cell(current_coord, current_cell, orientation)
          row, column = current_coord[0], current_coord[1]

          if (row < 0) or (row >= h) or (column < 0) or (column >= w):
            end_of_path = True
          else:
            current_cell = puzzle[row][column]
            path_coords.append(current_coord)
            if (current_cell == "/") or (current_cell == "\\"):
              path_values.append("M")
            else:
              path_values.append(" ")

        # add these paths to the full path list
        path = {'view': 'right', 'index':i, 'hint': num, 'path_values': path_values, 'path_coords': path_coords}
        all_paths.append(path)

        return all_paths

if __name__ == '__main__':
    '''
        Commands to run to generate a random puzzle
    '''
    a = HauntedMaze()
    a.generate_puzzle(3, 3)

    '''
        Commands to run to solve a given puzzle
    '''
    # rules = {
    #         'puzzle': [['\\', ' ', ' ', '\\'], [' ', ' ', ' ', '\\'], [' ', '/', ' ', ' '], ['/', ' ', '/', '\\']],
    #         'top': [0, 3, 2, 0],
    #         'bottom': [2, 3, 0, 0],
    #         'left': [0, 0, 0, 3],
    #         'right': [0, 0, 1, 3],
    #         'height': 4,
    #         'width': 4
    #     }
    # a = HauntedMaze()
    # paths = a.find_paths(rules)
    # a.find_possibilities(rules, paths)
