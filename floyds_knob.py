import random
import networkx as nx
import matplotlib.pyplot as plt

class Directions(object):

    def __init__(self):
        self.bdown_right = 1 # Bidirectional arrow from down to right and right to down
        self.bleft_down = 2 # Bidirectional arrow from left to down and down to left
        self.btop_right = 3 # Bidirectional arrow from top to right and right to top
        self.btop_left = 4 # Bidirectional arrow from top to left and left to top

        self.left_right = 5 # Unidirectional arrow from left to right
        self.right_left = 6 # Unidirectional arrow from right to left
        self.top_down = 7 # Unidirectional arrow from top to down
        self.down_top = 8 # Unidirectional arrow from down to top

    def bidirections(self):
        return [self.bdown_right, self.bleft_down, self.btop_right, self.btop_left]

    def fetch_all(self):
        return self.bidirections() + [self.left_right, self.right_left, self.top_down, self.down_top]

class FloydKnob(object):
    """docstring for FloydKnob
        Variables:
            'row' is the height of the town
            'col' is the width of the town
            'town' is a 2D array representation of the town
            'start' is the cell from where the car can enter (start point of puzzle)
            'end' is the cell from where the car exits (exit point of puzzle)
            'puzzle_graph' is the graphical representation of the solved puzzle
            'dir' is an object of the class Directions
    """

    def __init__(self, row, col):
        self.row = row
        self.col = col
        self.town = self.generate_town()
        self.start = self.fetch_random_coordinates(col=0)
        self.end = self.fetch_random_coordinates(col=self.col-1)
        self.last_visted = None
        self.last_dir = None
        self.puzzle_graph = nx.DiGraph()
        self.dir = Directions()
        self.all_directions = self.dir.fetch_all()

    def generate_town(self):
        grid = []
        for i in range(self.row):
            grid.append([0]*self.col)
        return grid

    def fetch_random_coordinates(self, col):
        return (random.randint(0, self.row-1), col)

    def fetch_top_below_coords(self, cell):
        op = []
        row = cell[0]
        col = cell[1]
        if row != 0:
            op.append((row - 1), col)
        if row != self.row - 1:
            op.append((row + 1), col)
        return op

    def add_distractions(self, row, col):
        cell = self.town[row][col]
        directions = self.all_directions
        if cell in self.dir.bidirections():
            return

        if cell == 100:
            a = ''
        else:
            a = str(cell)
        r = random.choice(range(2, 5))

        if row == 0:
            directions = list(set(self.all_directions) - {self.dir.right_left})

        if col == 0:
            directions = list(set(self.all_directions) - {self.dir.down_top})

        while r != 0:
            choice = str(random.choice(directions))
            if choice not in a:
                a += choice
            r -= 1
        self.town[row][col] = int(a)


    def mark_directions(self):
        self.print_matrix()
        self.town[0][0] = self.dir.bdown_right
        self.town[self.row-1][0] = self.dir.btop_right
        self.town[0][self.col-1] = self.dir.bleft_down
        self.town[self.row-1][self.col-1] = self.dir.btop_left
        self.print_matrix()

        for row in range(self.row):
            for col in range(self.col):
                self.add_distractions(row, col)
        self.print_matrix()

    def connect_down(self, start, end):
        crow = start[0]
        curr = start
        while crow != self.row - 1:
            crow += 1
            next = (crow, start[1])
            self.create_edge(curr, next)
            self.mark_visited(next, visit=self.dir.top_down)
            curr = next

        next = (self.row - 1, start[1] + 1)
        self.create_edge(curr, next)
        self.mark_visited(next)

        if next != end:
            erow = self.row - 1
            curr = next
            while erow != end[0] + 1:
                erow -= 1
                next = (erow, end[1])
                self.create_edge(curr, next)
                self.mark_visited(next, visit=self.dir.down_top)
                curr = next

            self.create_edge(curr, end)
            self.mark_visited(end, visit=self.dir.down_top)

    def connect_top(self, start, end):
        crow = start[0]
        curr = start
        while crow != 0:
            crow -= 1
            next = (crow, start[1])
            self.create_edge(curr, next)
            self.mark_visited(next, visit=self.dir.down_top)
            curr = next

        next = (0, start[1] + 1)
        self.create_edge(curr, next)
        self.mark_visited(next)

        if next != end:
            erow = 0
            curr = next
            while erow != end[0] - 1:
                erow += 1
                next = (erow, end[1])
                self.create_edge(curr, next)
                self.mark_visited(next, visit=self.dir.top_down)
                curr = next

            self.create_edge(curr, end)
            self.mark_visited(end, visit=self.dir.top_down)

    def fetch_dir_choices(self, start):
        op = {'up', 'down'}
        if self.last_dir:
            op = op - {self.last_dir}
        return list(op)


    def connect(self, start, end):
        dir = random.choice(self.fetch_dir_choices(start))
        self.last_dir = dir
        if dir == 'up':
            self.connect_top(start, end)
        else:
            self.connect_down(start, end)

    def create_edge(self, start, end):
        self.puzzle_graph.add_node(end)
        self.puzzle_graph.add_edge(start, end)

    def mark_visited(self, coordinates, visit=None):
        visit = visit or 100
        self.town[coordinates[0]][coordinates[1]] = visit
        self.last_visted = coordinates

    def print_matrix(self):
        for i in self.town:
            print(i)
        print('--------------------------------------------------')

    def generate_path(self):
        self.mark_visited(self.start)
        self.print_matrix()
        start = self.start
        self.puzzle_graph.add_node(start)

        for w in range(1, self.col - 1):
            curr = (random.randint(0, self.row - 1), w)
            self.connect(start, curr)
            self.print_matrix()
            start = curr

        self.puzzle_graph.add_node(self.end)
        self.connect(self.last_visted, self.end)
        self.mark_visited(self.end)
        self.print_matrix()

    def generate_puzzle(self):
        self.generate_path()
        self.mark_directions()
        nx.draw(self.puzzle_graph, with_labels=True)
        plt.draw()
        plt.show()


if __name__=='__main__':
    row = 6
    col = 6
    a = FloydKnob(row, col)
    a.generate_puzzle()
