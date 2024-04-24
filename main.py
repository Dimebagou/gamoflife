import pygame
import sys
from simulation import Simulation
from constants import BACKGROUND_COLOR, WINDOW_WIDTH, WINDOW_HEIGHT, CELL_SIZE, FPS, TEXT_COLOR
from lang import TEXTS


pygame.init()

# variables
initial_grid_state = None
current_language = "fr"  # Français par défaut

drawing = False
erasing = False
show_instructions = True

# window setup
window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Game of Life")

# clock setup
clock = pygame.time.Clock()

# Simulation setup
simulation = Simulation(WINDOW_WIDTH, WINDOW_HEIGHT, CELL_SIZE)


def draw_text(window, key, position, color=TEXT_COLOR):
    if show_instructions:
        font = pygame.font.Font("Poppins Medium 500.ttf", 20)
        text_surface = font.render(TEXTS[current_language][key], True, color)
        window.blit(text_surface, position)


def toggle_language():
    global current_language
    if current_language == "en":
        current_language = "fr"
    else:
        current_language = "en"


def update_fps_text():
    TEXTS["en"]["actual_fps"] = "FPS: " + str(FPS)
    TEXTS["fr"]["actual_fps"] = "FPS : " + str(FPS)


# Simulation Loop
while True:

    current_time = pygame.time.get_ticks()
    
    # 1. Event Handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            row = pos[1] // CELL_SIZE
            column = pos[0] // CELL_SIZE

            if event.button == 1:  # Bouton gauche
                drawing = True
                simulation.grid.cells[row][column] = 1
                print(f"Cell at row {row}, column {column} set to alive.")
            elif event.button == 3:  # Bouton droit
                erasing = True
                simulation.grid.cells[row][column] = 0
                print(f"Cell at row {row}, column {column} set to dead.")

        elif event.type == pygame.MOUSEBUTTONUP:
            drawing = False
            erasing = False

        elif event.type == pygame.MOUSEMOTION:
            if drawing or erasing:
                pos = pygame.mouse.get_pos()
                row = pos[1] // CELL_SIZE
                column = pos[0] // CELL_SIZE
                if drawing:
                    simulation.grid.cells[row][column] = 1
                elif erasing:
                    simulation.grid.cells[row][column] = 0

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if simulation.is_running():
                    simulation.stop()
                    print("Simulation paused.")
                else:
                    simulation.start()
                    print("Simulation started.")
            elif event.key == pygame.K_f:
                FPS += 2
                update_fps_text()
                print(f"FPS increased to {FPS}.")
            elif event.key == pygame.K_s:
                if FPS > 5:
                    FPS -= 2
                    update_fps_text()
                    print(f"FPS decreased to {FPS}.")
            elif event.key == pygame.K_r:
                simulation.create_random_state()
                print("Random state created.")
            elif event.key == pygame.K_c:
                simulation.clear()
                print("Grid cleared.")
            elif event.key == pygame.K_l:
                toggle_language()
                print(f"Language switched to {current_language}")
            elif event.key == pygame.K_z:
                if simulation.initial_state and not simulation.is_running():
                    simulation.grid.cells = [row[:]
                                             for row in simulation.initial_state]
                    print("Grid state restored.")
            elif event.key == pygame.K_i:
                show_instructions = not show_instructions  # Toggle l'affichage des instructions
                print(
                    f"Affichage des instructions: {'Activé' if show_instructions else 'Désactivé'}")

    # 2. Updating State
    simulation.update()

    # 3. Drawing
    window.fill(BACKGROUND_COLOR)
    simulation.draw(window)

    # Draw text on the screen
    if simulation.is_running():
        draw_text(window, "actual_fps", (10, 10))
        draw_text(window, "fps", (10, 40))
        draw_text(window, "toggle_instructions", (10, 70))
        draw_text(window, "start_pause", (10, 100))  # Affiche "SPACE to pause"
    else:
        draw_text(window, "start_pause", (10, 10))  # Affiche "SPACE to start"
        draw_text(window, "restore_grid", (10, 40))
        draw_text(window, "random_state", (10, 70))
        draw_text(window, "clear_grid", (10, 100))
        draw_text(window, "switch_language", (10, 130))
        draw_text(window, "toggle_instructions", (10, 160))

    pygame.display.update()
    clock.tick(FPS)
