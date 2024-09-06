import pygame
import time
from classes import field, player, block
field_size = (15, 15)
bordr_size = 4
cell_size = 40
size = (cell_size * field_size[0], cell_size * field_size[1])

BLACK = (0, 0, 0)
NBLACK = (30, 30, 30)
GRAY = (127, 127, 127)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
tt = 4
turn_time = tt * 100000000
apples = 2
count_of_enemies = 3

choises_menu = [("Play0", "play0"), ("Play1", "play1"), ("Play2", "play2"), ("Settings", "settings"), ("Exit", "quit")]
choises_death = [("Retry0", "play0"), ("Retry1", "play1"), ("Retry2", "play2"), ("Menu", "main_menu"), ("Exit", "quit")]
choises_settings = [("Field size", "field_s"), ("Apples", "apples"), ("Turn Time", "turn_rime"), ("Return", "main_menu")]
choises_Field_size = [("Width", 'width'), ("Heights", 'heights'), ("Return", "main_menu")]
color = {"empty": GRAY, "apple": RED, "wall": NBLACK, "snake0": BLACK, "snake1": GREEN, "snake2": BLUE}


def draw_text(text, x, y, screen, ft):
    img = pygame.font.SysFont('chalkduster.ttf', ft).render(text, True, RED)
    screen.blit(img, (x, y))
    pygame.display.update()


def play1():
    last_move = "Up"
    last_moves = ["Up"] * count_of_enemies
    alives = [True] * count_of_enemies
    last_time = time.monotonic_ns()
    screen = pygame.display.set_mode((field_size[0] * cell_size, field_size[1] * cell_size))
    fie = field(field_size[0], field_size[1], apples, 1, count_of_enemies)
    alive = True
    pause = False
    while alive:
        screen.fill((0, 0, 0))
        if not pause:
            if time.monotonic_ns() - last_time >= turn_time:
                alive = fie.move(last_move, 0)
                last_time = time.monotonic_ns()
                for i in range(count_of_enemies):
                    if not alives[i]:
                        continue
                    last_moves[i] = fie.find_path(1 + i)
                    alives[i] = fie.move(last_moves[i], 1 + i)
                    if not alives[i]:
                        fie.die(i + 1)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w or event.key == pygame.K_UP:
                    last_move = "Up"
                if event.key == pygame.K_a or event.key == pygame.K_LEFT:
                    last_move = "Left"
                if event.key == pygame.K_s or event.key == pygame.K_DOWN:
                    last_move = "Down"
                if event.key == pygame.K_d or event.key == pygame.K_RIGHT:
                    last_move = "Right"
                if event.key == pygame.K_p:
                    pause = not pause
        for x in range(field_size[0]):
            for y in range(field_size[1]):
                pygame.draw.rect(screen, color[fie.grid[x][y].type], (
                x * cell_size + bordr_size, y * cell_size + bordr_size, cell_size - 2 * bordr_size,
                cell_size - 2 * bordr_size))
        pygame.display.flip()
    return "death"


def play0():
    pause = False
    last_moves = ["Up"] * count_of_enemies
    alives = [True] * count_of_enemies
    last_time = time.monotonic_ns()
    screen = pygame.display.set_mode((field_size[0] * cell_size, field_size[1] * cell_size))
    fie = field(field_size[0], field_size[1], apples, 0, count_of_enemies)
    while any(alives):
        screen.fill((0, 0, 0))
        if not pause:
            if time.monotonic_ns() - last_time >= turn_time:
                last_time = time.monotonic_ns()
                for i in range(count_of_enemies):
                    if not alives[i]:
                        continue
                    last_moves[i] = fie.find_path(i)
                    alives[i] = fie.move(last_moves[i], i)
                    if not alives[i]:
                        fie.die(i)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    pause = not pause
        for x in range(field_size[0]):
            for y in range(field_size[1]):
                pygame.draw.rect(screen, color[fie.grid[x][y].type], (
                x * cell_size + bordr_size, y * cell_size + bordr_size, cell_size - 2 * bordr_size,
                cell_size - 2 * bordr_size))
        pygame.display.flip()
    return "death"


def play2():
    last_move0 = "Up"
    last_move1 = "Up"
    last_time = time.monotonic_ns()
    screen = pygame.display.set_mode((field_size[0] * cell_size, field_size[1] * cell_size))
    fie = field(field_size[0], field_size[1], apples, 2, 0)
    alive0 = True
    alive1 = True
    while alive1 and alive0:
        screen.fill((0, 0, 0))
        if time.monotonic_ns() - last_time >= turn_time:
            alive0 = fie.move(last_move0, 0)
            alive1 = fie.move(last_move1, 1)
            last_time = time.monotonic_ns()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w:
                    last_move0 = "Up"
                if event.key == pygame.K_a:
                    last_move0 = "Left"
                if event.key == pygame.K_s:
                    last_move0 = "Down"
                if event.key == pygame.K_d:
                    last_move0 = "Right"
                if event.key == pygame.K_UP:
                    last_move1 = "Up"
                if event.key == pygame.K_LEFT:
                    last_move1 = "Left"
                if event.key == pygame.K_DOWN:
                    last_move1 = "Down"
                if event.key == pygame.K_RIGHT:
                    last_move1 = "Right"
        for x in range(field_size[0]):
            for y in range(field_size[1]):
                pygame.draw.rect(screen, color[fie.grid[x][y].type], (
                x * cell_size + bordr_size, y * cell_size + bordr_size, cell_size - 2 * bordr_size,
                cell_size - 2 * bordr_size))
        pygame.display.flip()
    return "death"


def menu(choises):
    screen = pygame.display.set_mode(size)
    screen.fill((0, 0, 0))
    for i in range(len(choises)):
        draw_text(f"{i + 1} - " + choises[i][0], 0, i * 50, screen, 50)
    alive = True
    while alive:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"
            elif event.type == pygame.KEYDOWN:
                for i in range(len(choises)):
                    if event.key == eval(f"pygame.K_{i + 1}"):
                        return choises[i][1]


def settings():
    return menu(choises_settings)


def field_s():
    return menu(choises_Field_size)


def death():
    return menu(choises_death)


def main_menu():
    return menu(choises_menu)


def main():
    curr_script = "main_menu"
    while curr_script != "quit":
        curr_script = eval(curr_script + "()")


if __name__ == '__main__':
    pygame.init()
    main()
    pygame.quit()
