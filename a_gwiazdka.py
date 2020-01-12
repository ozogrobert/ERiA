import math

class Grid:
    class Node:
        def __init__(self, row, column, val, parent=None):
            self.position = (row, column)
            self.parent = parent
            self.value = val
            self.adjacent = []
            self.heuristic = 0
            self.g = 0
            self.f = 0

        def __str__(self):
            return f"{self.position}: {self.value}"

    def __init__(self):
        self.end_coord = (19, 19)  # y,x
        self.start_coord = (0, 0)
        self.node_grid = []

    def heuristic_calc(self, node):
        y, x = node.position
        end_row, end_col = self.end_coord
        node.heuristic = round(math.sqrt((x - end_col) ** 2 + (y - end_row) ** 2), 2)
        # return node.heuristic

    def load(self, grid_filename):
        if self.node_grid:
            self.node_grid = []
        new_grid = []
        with open(grid_filename) as grid_file:
            for line in grid_file:
                new_grid.append(line.strip('\r\n').split(' '))
        for y, row in enumerate(new_grid):
            node_row = []
            for x, column in enumerate(row):
                node_row.append(self.Node(y, x, column))
            else:
                self.node_grid.append(node_row)
                # print([str(i) for i in node_row])

    def save(self):
        with open("output.txt", "w") as grid_file:
            for row in self.node_grid:
                new_row = []
                for col in row:
                    new_row.append(col.value)
                grid_file.write(" ".join(new_row) + "\n")

    def a_gwiazdka(self):
        def node_adjacent(current):
            y, x = current.position
            for i, j in ((1, 0), (-1, 0), (0, -1), (0, 1)):
                if x + j < 0 or y + i < 0:
                    continue
                try:
                    if self.node_grid[y + i][x + j].value == "5":
                        continue
                    current.adjacent.append(self.node_grid[y + i][x + j])
                except IndexError:
                    pass
            for adjacent_node in current.adjacent:
                if adjacent_node in LZ:
                    continue
                elif adjacent_node in LO and adjacent_node.f <= (current.g + 1 + adjacent_node.heuristic):
                    continue
                else:
                    LO.append(adjacent_node)
                    self.heuristic_calc(adjacent_node)

                adjacent_node.parent = current
                adjacent_node.g = current.g + 1
                adjacent_node.f = adjacent_node.g + adjacent_node.heuristic

        # setup
        start_node = self.node_grid[self.start_coord[0]][self.start_coord[1]]
        self.heuristic_calc(start_node)
        start_node.f = start_node.heuristic
        # print(start_node.heuristic)
        LO = []
        LO.append(start_node)
        LZ = []
        # loop
        while True:
            if LO:
                min_node = min(LO, key=lambda node: node.f)
                # print(min_node)
            else:
                break
            LO.remove(min_node)
            LZ.append(min_node)
            if min_node.position == self.end_coord:
                track_node = min_node
                while True:
                    # print(track_node)
                    track_node.value = "3"
                    if track_node.parent is None:
                        break
                    track_node = track_node.parent
                break
            node_adjacent(min_node)

if __name__ == '__main__':
    eria = Grid()
    eria.load("grid.txt")
    eria.a_gwiazdka()
    eria.save()
