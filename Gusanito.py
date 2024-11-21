import pygame
import random
import sys

# Inicializar Pygame
pygame.init()

# Configuración de pantalla
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("GUSANO 2025")

# Colores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
COLORS = {"VERDE": GREEN, "AZUL": BLUE, "ROJO": RED, "AMARILLO": YELLOW}

# Música
pygame.mixer.music.load("background_music.mp3")
game_over_sound = pygame.mixer.Sound("game_over.wav")
collect_sound = pygame.mixer.Sound("collect.wav")
end_music = pygame.mixer.Sound("end_music.wav")

# Fuente
font = pygame.font.Font(None, 36)

def draw_text(text, color, x, y, center=False):
    """Dibuja texto en pantalla."""
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect(center=(x, y)) if center else (x, y)
    screen.blit(text_surface, text_rect)

def show_intro():
    """Muestra la pantalla de introducción."""
    pygame.mixer.music.play(-1)  # Música en bucle
    screen.fill(BLACK)
    draw_text("GUSANO 2025", GREEN, WIDTH // 2, HEIGHT // 3, center=True)
    draw_text("Presiona cualquier tecla para comenzar", WHITE, WIDTH // 2, HEIGHT // 2, center=True)
    pygame.display.flip()
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                waiting = False

def get_player_info():
    """Solicita el nombre del jugador y elige el color del gusano."""
    screen.fill(BLACK)
    draw_text("Ingresa tu nombre:", WHITE, WIDTH // 2, HEIGHT // 3, center=True)
    pygame.display.flip()
    name = ""
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN and name:
                    waiting = False
                elif event.key == pygame.K_BACKSPACE:
                    name = name[:-1]
                elif len(name) < 10:
                    name += event.unicode.upper()
                screen.fill(BLACK)
                draw_text("Ingresa tu nombre:", WHITE, WIDTH // 2, HEIGHT // 3, center=True)
                draw_text(name, WHITE, WIDTH // 2, HEIGHT // 2, center=True)
                pygame.display.flip()
    
    # Seleccionar color
    screen.fill(BLACK)
    draw_text(f"{name}, selecciona un color para tu gusano:", WHITE, WIDTH // 2, HEIGHT // 3, center=True)
    for idx, (color_name, color_value) in enumerate(COLORS.items()):
        draw_text(color_name, color_value, WIDTH // 2, HEIGHT // 2 + idx * 40, center=True)
    pygame.display.flip()
    
    selected_color = None
    while selected_color is None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                for idx, color_name in enumerate(COLORS.keys()):
                    if event.key == pygame.K_1 + idx:
                        selected_color = COLORS[color_name]
                        break
    return name, selected_color

def game_loop(player_name, worm_color):
    """Lógica principal del juego."""
    clock = pygame.time.Clock()
    cell_size = 20
    worm_positions = [(WIDTH // 2, HEIGHT // 2)]
    direction = (cell_size, 0)
    food_position = (random.randint(0, (WIDTH - cell_size) // cell_size) * cell_size,
                     random.randint(0, (HEIGHT - cell_size) // cell_size) * cell_size)
    score = 0
    speed = 10

    running = True
    while running:
        screen.fill(BLACK)

        # Dibujar paredes
        pygame.draw.line(screen, WHITE, (0, 0), (0, HEIGHT), 5)
        pygame.draw.line(screen, WHITE, (WIDTH - 5, 0), (WIDTH - 5, HEIGHT), 5)

        # Eventos
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and direction != (0, cell_size):
                    direction = (0, -cell_size)
                elif event.key == pygame.K_DOWN and direction != (0, -cell_size):
                    direction = (0, cell_size)
                elif event.key == pygame.K_LEFT and direction != (cell_size, 0):
                    direction = (-cell_size, 0)
                elif event.key == pygame.K_RIGHT and direction != (-cell_size, 0):
                    direction = (cell_size, 0)

        # Mover gusano
        head_x, head_y = worm_positions[0]
        new_head = (head_x + direction[0], head_y + direction[1])
        worm_positions = [new_head] + worm_positions[:-1]

        # Verificar colisiones
        if new_head in worm_positions[1:] or \
                new_head[0] < 5 or new_head[0] >= WIDTH - 5 or \
                new_head[1] < 0 or new_head[1] >= HEIGHT:
            game_over_sound.play()
            running = False

        # Comer alimento
        if new_head == food_position:
            collect_sound.play()
            worm_positions.append(worm_positions[-1])
            food_position = (random.randint(0, (WIDTH - cell_size) // cell_size) * cell_size,
                             random.randint(0, (HEIGHT - cell_size) // cell_size) * cell_size)
            score += 1
            speed += 1

        # Dibujar gusano y alimento
        for pos in worm_positions:
            pygame.draw.rect(screen, worm_color, (*pos, cell_size, cell_size))
        pygame.draw.rect(screen, RED, (*food_position, cell_size, cell_size))

        draw_text(f"Puntuación: {score}", WHITE, 10, 10)
        pygame.display.flip()
        clock.tick(speed)

    # Fin del juego
    end_music.play()
    screen.fill(BLACK)
    draw_text(f"Juego Terminado!", RED, WIDTH // 2, HEIGHT // 3, center=True)
    draw_text(f"Jugador: {player_name}", WHITE, WIDTH // 2, HEIGHT // 2, center=True)
    draw_text(f"Puntuación: {score}", WHITE, WIDTH // 2, HEIGHT // 2 + 40, center=True)
    draw_text("¿Jugar de nuevo? (S/N)", WHITE, WIDTH // 2, HEIGHT // 2 + 80, center=True)
    pygame.display.flip()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_s:
                    return True
                if event.key == pygame.K_n:
                    return False

if __name__ == "__main__":
    while True:
        show_intro()
        player_name, worm_color = get_player_info()
        if not game_loop(player_name, worm_color):
            break
