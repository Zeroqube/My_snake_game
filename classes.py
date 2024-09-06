import random
import queue

class block:
    def __init__(self, type):
        self.type = type #"empty", "wall", "apple", "snake"


class player:
    def __init__(self, x, y):
        self.body = dict()
        self.len = 1
        self.body[1] = (x, y)
        self.count = 1

    def move(self, dx, dy):
        self.count += 1
        self.body[self.count] = (self.body[self.count - 1][0] + dx, self.body[self.count - 1][1] + dy)
        res = self.body[self.count - self.len]
        self.body.__delitem__(self.count - self.len)
        return res

    def grow(self, dx, dy):
        self.count += 1
        self.len += 1
        self.body[self.count] = (self.body[self.count - 1][0] + dx, self.body[self.count - 1][1] + dy)

    def head(self):
        return self.body[self.count]


class field:
    def __init__(self, width, height, count_of_apples, count_of_players, count_of_enemies):
        self.width = width
        self.height = height
        self.count_of_apples = count_of_apples
        self.curr_count_of_apples = count_of_apples
        self.grid = [[block("empty") for i in range(self.height)] for j in range(self.width)]

        self.snakes = [player(i * self.width // (count_of_players + 1), 2 * self.height // 3) for i in range(1, count_of_players + 1)]
        for i in range(1, count_of_players + 1):
            self.grid[i * self.height // (count_of_players + 1)][2 * self.width // 3].type = "snake" + str(i - 1)

        for i in range(count_of_players + 1, count_of_players + 1 + count_of_enemies):
            self.snakes.append(player((i - count_of_players) * self.width // (count_of_enemies + 1), self.height // 3))
            self.grid[(i - count_of_players) * self.height // (count_of_enemies + 1)][self.width // 3].type = "snake" + str(i - 1)

        self.used = [[False for i in range(self.height)] for j in range(self.width)]

        for y in range(self.height):
            self.grid[y][self.width - 1].type = "wall"
            self.grid[y][0].type = "wall"
        for x in range(self.width):
            self.grid[self.height - 1][x].type = "wall"
            self.grid[0][x].type = "wall"
        for _ in range(self.count_of_apples):
            self.generate_apple()

    def move(self, direction, n):
        x, y = self.snakes[n].head()
        dx, dy = 0, 0
        if direction == "Up":
            dy = -1
        elif direction == "Down":
            dy = +1
        elif direction == "Left":
            dx = -1
        elif direction == "Right":
            dx = 1
        if self.grid[x + dx][y + dy].type == "wall" or self.grid[x + dx][y + dy].type[:5] == "snake":
            print(dx, dy)
            return False
        elif self.grid[x + dx][y + dy].type == "apple":
            self.grid[x + dx][y + dy].type = "snake" + str(n)
            self.snakes[n].grow(dx, dy)
            self.generate_apple()
        elif self.grid[x + dx][y + dy].type == "empty":
            self.grid[x + dx][y + dy].type = "snake" + str(n)
            xd, yd = self.snakes[n].move(dx, dy)
            self.grid[xd][yd].type = "empty"
        return True

    def generate_apple(self):
        if self.curr_count_of_apples > self.count_of_apples:
            self.curr_count_of_apples -= 1
            return
        empty_cells = list()
        for x in range(self.width):
            for y in range(self.height):
                if self.grid[x][y].type == "empty":
                    empty_cells.append((x, y))
        if not len(empty_cells) == 0:
            x, y = empty_cells[random.randint(0, len(empty_cells) - 1)]
            self.grid[x][y].type = "apple"

    def die(self, n):
        len = self.snakes[n].count
        self.curr_count_of_apples += self.snakes[n].len
        for i in range(self.snakes[n].len):
            x, y = self.snakes[n].body[len - i]
            self.grid[x][y].type = "apple"

    def dfs(self, x, y):
        self.used[x][y] = True
        dr = [(0, 1), (1, 0), (0, -1), (-1, 0)]
        random.shuffle(dr)
        best = (False, (0, 1), 100000000000)
        for dx, dy in dr:
            if self.used[x + dx][y + dy]:
                continue
            if "snake" in self.grid[x + dx][y + dy].type or self.grid[x + dx][y + dy].type == "wall":
                continue
            if self.grid[x + dx][y + dy].type == "empty":
                res, direction, le = self.dfs(x + dx, y + dy)
                if res:
                    if best[-1] >= le:
                        best = (res, (dx, dy), le)
                continue
            if self.grid[x + dx][y + dy].type == "apple":
                return True, (dx, dy), 0
        return best

    def bfs(self, a, b):
        prev = [[(-1, -1) for i in range(self.height)] for j in range(self.width)]
        q = queue.Queue()
        q.put((a, b))
        dr = [(0, 1), (1, 0), (0, -1), (-1, 0)]
        while not q.empty():
            x, y = q.get()
            self.used[x][y] = True
            best = (False, (0, 1), 100000000000)
            for dx, dy in dr:
                if self.used[x + dx][y + dy]:
                    continue
                if "snake" in self.grid[x + dx][y + dy].type or self.grid[x + dx][y + dy].type == "wall":
                    continue
                if self.grid[x + dx][y + dy].type == "empty":
                    q.put((x + dx, y + dy))
                    prev[x + dx][y + dy] = (x, y)
                if self.grid[x + dx][y + dy].type == "apple":
                    prev[x + dx][y + dy] = (x, y)
                    curr_x, curr_y = x + dx, y + dy
                    while prev[curr_x][curr_y] != (a, b):
                        curr_x, curr_y = prev[curr_x][curr_y]
                    return curr_x - a, curr_y - b
        return dr[random.randint(0, 4)]

    def find_path(self, n):
        self.used = [[False for i in range(self.height)] for j in range(self.width)]
        dur = self.bfs(*self.snakes[n].head())
        x, y = self.snakes[n].head()
        print(self.grid[x + dur[0]][y + dur[1]].type)
        if dur == (1, 0):
            return "Right"
        if dur == (-1, 0):
            return "Left"
        if dur == (0, 1):
            return "Down"
        if dur == (0, -1):
            return "Up"
        return "Down"

