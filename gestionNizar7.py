import random
import sys
import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"

import pygame

pygame.init()

# Configuration de la fenêtre
WIDTH, HEIGHT = 640, 480  # Dimensions de la fenêtre
CELL_SIZE = 20  # Taille d'une cellule dans la grille
GRID_WIDTH = WIDTH // CELL_SIZE  # Nombre de cellules en largeur
GRID_HEIGHT = HEIGHT // CELL_SIZE  # Nombre de cellules en hauteur

# Couleurs
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
PURPLE = (128, 0, 128)

# Vitesse du jeu
FPS = 10

# Initialisation de la fenêtre
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game")

# Fonts
font = pygame.font.SysFont(None, 36)

# Variables de score
current_score = 0
high_score = 0

# Dessine le serpent sur l'écran
def draw_snake(snake, color):
    for segment in snake:
        pygame.draw.rect(screen, color, pygame.Rect(
            segment[0] * CELL_SIZE, segment[1] * CELL_SIZE, CELL_SIZE, CELL_SIZE))

# Dessine la nourriture sur l'écran
def draw_food(position, color):
    pygame.draw.rect(screen, color, pygame.Rect(
        position[0] * CELL_SIZE, position[1] * CELL_SIZE, CELL_SIZE, CELL_SIZE))

# Crée la nourriture dans une position aléatoire qui n'est pas occupée par le serpent
def create_food(snake, walls=None):
    while True:
        position = (random.randint(1, GRID_WIDTH - 2),
                    random.randint(1, GRID_HEIGHT - 2))
        if position not in snake and (not walls or position not in walls):
            return position

# Dessine les murs sur l'écran
def draw_walls(walls):
    for wall in walls:
        pygame.draw.rect(screen, BLUE, pygame.Rect(
            wall[0] * CELL_SIZE, wall[1] * CELL_SIZE, CELL_SIZE, CELL_SIZE))

# Affiche le message de fin de partie
def game_over():
    global current_score, high_score
    if current_score > high_score:
        high_score = current_score

    text = font.render(f"Game Over! Score: {current_score}", True, RED)
    screen.blit(text, [WIDTH // 2 - text.get_width() //
                2, HEIGHT // 2 - text.get_height() // 2])
    pygame.display.flip()
    pygame.time.wait(2000)
    main_menu()

# Affiche le menu principal
def main_menu():
    screen.fill(BLACK)
    menu_items = ["1. Normal Mode", "2. Maze Mode", "3. Multiplayer Mode",
                  "Player 1: Use arrow keys", "Player 2: Use W, A, S, D",
                  f"High Score: {high_score}"]
    y_offset = 100
    for item in menu_items:
        text = font.render(item, True, WHITE)
        screen.blit(text, [WIDTH // 2 - text.get_width() // 2, y_offset])
        y_offset += 50
    pygame.display.flip()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    game_loop(normal_mode)
                elif event.key == pygame.K_2:
                    game_loop(maze_mode)
                elif event.key == pygame.K_3:
                    game_loop(multiplayer_mode)

# Affiche le menu de pause
def pause_menu():
    screen.fill(BLACK)
    menu_items = ["1. Continue", "2. Restart", "3. Main Menu"]
    y_offset = 100
    for item in menu_items:
        text = font.render(item, True, WHITE)
        screen.blit(text, [WIDTH // 2 - text.get_width() // 2, y_offset])
        y_offset += 50
    pygame.display.flip()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    return "continue"
                elif event.key == pygame.K_2:
                    return "restart"
                elif event.key == pygame.K_3:
                    return "main_menu"

# Mode de jeu normal
def normal_mode(snake, direction, food, walls=None):
    snake, food, game_over_flag = move_snake(snake, direction, food, walls)
    return snake, food, game_over_flag, None

# Mode de jeu avec labyrinthe
def maze_mode(snake, direction, food, walls):
    if not walls:
        walls = create_maze()
    snake, food, game_over_flag = move_snake(snake, direction, food, walls)
    return snake, food, game_over_flag, walls

# Mode de jeu multijoueur
# Mode de jeu multijoueur
def multiplayer_mode(snake, direction, food, walls=None):
    snake2 = [(GRID_WIDTH // 2 + 2, GRID_HEIGHT // 2)]
    direction2 = pygame.K_LEFT
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key in [pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT]:
                    direction = event.key
                if event.key in [pygame.K_w, pygame.K_s, pygame.K_a, pygame.K_d]:
                    if event.key == pygame.K_w:
                        direction2 = pygame.K_UP
                    elif event.key == pygame.K_s:
                        direction2 = pygame.K_DOWN
                    elif event.key == pygame.K_a:
                        direction2 = pygame.K_LEFT
                    elif event.key == pygame.K_d:
                        direction2 = pygame.K_RIGHT
                elif event.key == pygame.K_ESCAPE:
                    action = pause_menu()
                    if action == "continue":
                        continue
                    elif action == "restart":
                        return multiplayer_mode(snake, direction, food, walls)
                    elif action == "main_menu":
                        return main_menu()

        snake, food, game_over_flag1 = move_snake(snake, direction, food, walls)
        snake2, food, game_over_flag2 = move_snake(snake2, direction2, food, walls)
        if game_over_flag1 or game_over_flag2:
            game_over()
            return
        draw(snake, food, walls, snake2)
        pygame.display.flip()
        pygame.time.Clock().tick(FPS)

# Crée un labyrinthe avec des murs aléatoires
def create_maze():
    walls = [(random.randint(1, GRID_WIDTH - 2),
              random.randint(1, GRID_HEIGHT - 2)) for _ in range(30)]
    return walls

# Déplace le serpent dans la direction donnée
def move_snake(snake, direction, food, walls):
    global current_score
    head_x, head_y = snake[0]
    if direction == pygame.K_UP:
        head_y -= 1
    elif direction == pygame.K_DOWN:
        head_y += 1
    elif direction == pygame.K_LEFT:
        head_x -= 1
    elif direction == pygame.K_RIGHT:
        head_x += 1
    new_head = (head_x, head_y)

    # Vérifie si le serpent a touché la bordure
    if new_head in snake or head_x <= 0 or head_x >= GRID_WIDTH - 1 or head_y <= 0 or head_y >= GRID_HEIGHT - 1 or (walls and new_head in walls):
        return snake, food, True

    snake.insert(0, new_head)
    if new_head == food:
        current_score += 1
        food = create_food(snake, walls)
    else:
        snake.pop()
    return snake, food, False

# Dessine la bordure de la grille
def draw_border(color):
    pygame.draw.rect(screen, color, pygame.Rect(
        0, 0, WIDTH, HEIGHT), CELL_SIZE)

# Dessine l'état actuel du jeu
def draw(snake, food, walls=None, snake2=None):
    screen.fill(BLACK)
    draw_border(PURPLE)
    draw_snake(snake, GREEN)
    draw_food(food, RED)
    if walls:
        draw_walls(walls)
    if snake2:
        draw_snake(snake2, BLUE)
    display_score()

# Affiche le score et le meilleur score
def display_score():
    score_text = font.render(f"Score: {current_score}", True, WHITE)
    high_score_text = font.render(f"High Score: {high_score}", True, WHITE)
    screen.blit(score_text, [10, 10])
    screen.blit(high_score_text, [
                WIDTH - high_score_text.get_width() - 10, 10])

# Boucle principale du jeu
def game_loop(mode_function):
    global current_score
    snake = [(GRID_WIDTH // 2, GRID_HEIGHT // 2)]
    direction = pygame.K_RIGHT
    walls = None
    food = create_food(snake, walls)
    current_score = 0

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key in [pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT]:
                    # Vérifie si la nouvelle direction est perpendiculaire à l'ancienne
                    if (direction in [pygame.K_UP, pygame.K_DOWN] and event.key in [pygame.K_LEFT, pygame.K_RIGHT]) or \
                       (direction in [pygame.K_LEFT, pygame.K_RIGHT] and event.key in [pygame.K_UP, pygame.K_DOWN]):
                        direction = event.key
                elif event.key == pygame.K_ESCAPE:
                    action = pause_menu()
                    if action == "continue":
                        continue
                    elif action == "restart":
                        return game_loop(mode_function)
                    elif action == "main_menu":
                        return main_menu()

        snake, food, game_over_flag, walls = mode_function(
            snake, direction, food, walls)
        if game_over_flag:
            game_over()
            return

        draw(snake, food, walls)
        pygame.display.flip()
        pygame.time.Clock().tick(FPS)

# Point d'entrée du programme
if __name__ == "__main__":
    main_menu()
