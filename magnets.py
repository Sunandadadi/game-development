# Group members: Sunanda(netid: sdadi2), Xiaohan Wang(netid:xw41) and Xiaofei Luo(dropped)

import itertools
import copy


class Magnets(object):
    """docstring for Magnets
        Variables:
            'pc' is a list of the positive poles in a column. Unknown values are indicated by -1.
            'pr' is a list of the positive poles in a row. Unknown values are indicated by -1.
            'nc' is a list of the negative poles in a column. Unknown values are indicated by -1.
            'nr' is a list of the negative poles in a row. Unknown values are indicated by -1.

            Horizontal arragement of a magnet is indicated by ['H', 'h']
            Vertical arragement of a magnet is indicated by ['V', 'v']
            'm' indicates the arragement of magnets in a matrix
    """

    def __init__(self, arg):
        self.pc = arg.get('pc')
        self.pr = arg.get('pr')
        self.nc = arg.get('nc')
        self.nr = arg.get('nr')
        self.ag = arg.get('ag')
        self.row_count = len(self.ag)
        self.col_count = len(self.ag[0])
        self.possible_values = ['+', '-', 'X']
        self.temp_matrix = [['X']*self.col_count]*self.row_count


    def count(self,array,char):
        """
        Given an array, count how many times one specific character occurs
        :param array: a list of characters
        :param char: a character
        :return: an integer number
        """
        count = 0
        for item in array:
            if item == char:
                count += 1
        return count

    def not_adjacent(self, temp):
        """
        Given a temporary matrix, check if it satisfies the rule that any positive/negative slot cannot be adjacent to negative/positive slots
        :param temp: a list of list of characters representing the matrix
        :return: the bool value indicating whether it satisfies the basic rule or not
        """
        # Check adjacency
        for i in range(len(temp)):
            for j in range(len(temp[i])):
                if temp[i][j] != 'X':
                    # check if positive or negative slots don't have the same slots in the top/left/bottom/right
                    if ((i - 1 >= 0 and temp[i - 1][j] == temp[i][j]) or  # check if the top slot of the current one is the same
                            ((j + 1 < self.col_count) and temp[i][j + 1] == temp[i][j]) or # check if the right slot of the current one is the same
                            (((i + 1 < self.row_count and temp[i + 1][j] == temp[i][j]) or  # check if the below slot of the current one is the same
                        (j - 1 >= 0 and temp[i][j - 1] == temp[i][j])))):  # check if the left slot of the current one is the same
                            return False
                    # check if 'X' slots there's another 'x' in the corresponding right position
                else:
                    if self.ag[i][j] == 'H':  # if 'X' lies in an 'H' slot, then its right slot must be 'X', otherwise, return False
                        if j + 1 < self.col_count and temp[i][j + 1] != 'X':
                            return False
                    elif self.ag[i][j] == 'V':  # if 'X' lies in an 'V' slot, then its below slot must be 'X', otherwise, return False
                        if i + 1 < self.row_count and temp[i + 1][j] != 'X':
                            return False

        return True

    def is_possible_solution(self, temp):
        """
        Given a partially filled matrix, checks if the matrix is a plausible solution
        :param temp: a list of list of characters representing the matrix
        :return: the bool value indicating if the solution is valid
        """
        # Check number validity
        # Check each row
        column_neg_count = [0] * len(temp[0])
        column_poz_count = [0] * len(temp[0])
        # Check row number validity
        for i in range(len(temp)):
            # Check row
            if self.count(temp[i], '+') > self.pr[i] or self.count(temp[i], '-') > self.nr[i]:
                return False
                # Record the number of positive/negative slots in each column
            for j in range(len(temp[i])):
                if temp[i][j] == '-':
                    column_neg_count[j] += 1
                if temp[i][j] == '+':
                    column_poz_count[j] += 1

        # Check column number validity
        for q in range(len(self.pc)):
            if column_neg_count[q] > self.nc[q] or column_poz_count[q] > self.pc[q]:
                return False
        return True


    def is_valid_solution(self, temp):
        """
        Given a complete matrix, checks if the solution is valid
        :param temp: a list of list of characters representing the matrix
        :return: the bool value indicating if the solution is valid
        """
        # Check number validity
        # Check each row
        column_neg_count = [0] * len(temp[0])
        column_poz_count = [0] * len(temp[0])
        # Check row number validity
        for i in range(len(temp)):
            # Check row
            if self.count(temp[i], '+') != self.pr[i] or self.count(temp[i], '-') != self.nr[i]:
                return False
                # Record the number of positive/negative slots in each column
            for j in range(len(temp[i])):
                if temp[i][j] == '-':
                    column_neg_count[j] += 1
                if temp[i][j] == '+':
                    column_poz_count[j] += 1

            # Check column number validity
        for q in range(len(self.pc)):
            if column_neg_count[q] != self.nc[q] or column_poz_count[q] != self.pc[q]:
                return False
        return True


    def all_params_valid(self):
        if not (self.row_count * self.col_count) % 2 == 0:
            return False, 'Incorrect Grid Input for magnet orientation'

        if (len(self.pc) or len(self.nc)) != self.col_count:
            return False, 'Incorrect Input for positive or negative poles in column'

        if (len(self.pr) or len(self.nr)) != self.row_count:
            return False, 'Incorrect Input for positive or negative poles in row'

        return True, ''

    def output(self, ans):
      	"""
        Given the ans, output all the solutions if there are less than 3 solutions, if not, only output the first 3
        :param ans: the list of solutions
        :return:
        """
        out_len = len(ans)
        print("Total Number of Solution(s) are", out_len)
        out_len = 3 if out_len > 3 else out_len
        for i in range(out_len):
            print(ans[i])

    def find_all_solutions(self):
        valid, msg = self.all_params_valid()
        if not valid:
            print msg
            return

        permutations = list(map(lambda x: x, itertools.product(['+', '-', 'X'], repeat=self.col_count)))

        possibilities = {0: []}
        for p in permutations:
            temp = copy.deepcopy(self.temp_matrix)
            temp[0] = list(p)
            if self.not_adjacent(temp) and self.is_possible_solution(temp):
                possibilities[0].append(temp)


        if self.row_count < 2:
            ans = []
            for p in possibilities[0]:
                if self.not_adjacent(p) and self.is_valid_solution(p):
                    ans.append(p)
            return self.output(ans)

        curr_counter = 1
        while curr_counter < self.row_count:

            possibilities[curr_counter] = []
            values = possibilities[curr_counter-1]
            for v in values:
                for p in permutations:
                    temp = copy.deepcopy(v)
                    temp[curr_counter] = list(p)
                    if self.not_adjacent(temp) and self.is_possible_solution(temp):
                        possibilities[curr_counter].append(temp)

            curr_counter += 1

        ans = []
        for p in possibilities[curr_counter-1]:
            if self.not_adjacent(p) and self.is_valid_solution(p):
                ans.append(p)

        return self.output(ans)


if __name__ == '__main__':
    t = {}
    t['pc'] = [1, 0, 1]
    t['pr'] = [2, 0]
    t['nc'] = [0, 1, 1]
    t['nr'] = [1, 1]
    t['ag'] = [['H', 'h', 'V'], ['H', 'h', 'V']]

    a = Magnets(t)
    a.find_all_solutions()
