import pygame
import math
import time
import random

# Inicializar Pygame
pygame.init()

# Dimensiones de la pantalla
WIDTH, HEIGHT = 800, 600

# Colores
BLACK = (0, 0, 0)
TURQUOISE = (64, 224, 208)
WHITE = (255, 255, 255)

# Velocidad de movimiento y rotación
MOVE_SPEED = 5
ROTATE_SPEED = 3
ACCELERATION = 0.1

# Número de estrellas y su radio
NUM_STARS = 100
STAR_RADIUS = 2

# Lista para almacenar las posiciones de las estrellas
stars = []

# Generar posiciones aleatorias para las estrellas
for _ in range(NUM_STARS):
    x = random.randint(0, WIDTH)
    y = random.randint(0, HEIGHT)
    stars.append((x, y))

# Inicializar la pantalla
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Triángulo Móvil")

# Inicializar variables de posición, velocidad y ángulo
x, y = WIDTH // 2, HEIGHT // 2
angle = 0
x_speed, y_speed = 0, 0
angular_speed = 0
moving = False
rotating_left = False
rotating_right = False

# Tiempo en el que se detendrá el movimiento
stop_time = None

# Reloj para controlar el tiempo
clock = pygame.time.Clock()

# Variable para alternar la visibilidad de las estrellas
star_visible = True

# Bucle principal
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Detectar teclas presionadas
    keys = pygame.key.get_pressed()

    # Movimiento vertical
    if keys[pygame.K_UP]:
        moving = True
        y_speed -= ACCELERATION * math.cos(math.radians(angle))
        x_speed += ACCELERATION * math.sin(math.radians(angle))
        stop_time = None  # Reiniciar el temporizador de detención
    elif keys[pygame.K_DOWN]:
        moving = True
        y_speed += ACCELERATION * math.cos(math.radians(angle))
        x_speed -= ACCELERATION * math.sin(math.radians(angle))
        stop_time = None  # Reiniciar el temporizador de detención

    # Comprobar si se debe detener el movimiento
    if not keys[pygame.K_UP] and not keys[pygame.K_DOWN]:
        if stop_time is None:
            stop_time = time.time() + 1.5  # Detener el movimiento en 1.5 segundos
        elif time.time() > stop_time:
            y_speed = 0
            x_speed = 0

    # Rotación
    if keys[pygame.K_LEFT]:
        rotating_left = True
    else:
        rotating_left = False

    if keys[pygame.K_RIGHT]:
        rotating_right = True
    else:
        rotating_right = False

    if rotating_left and not rotating_right:
        angular_speed = -ROTATE_SPEED
    elif rotating_right and not rotating_left:
        angular_speed = ROTATE_SPEED
    else:
        angular_speed = 0

    # Actualizar posición y rotación
    x += x_speed
    y += y_speed
    angle += angular_speed

    # Asegurarse de que el triángulo atraviese los bordes
    if x < 0:
        x = WIDTH
    elif x > WIDTH:
        x = 0

    if y < 0:
        y = HEIGHT
    elif y > HEIGHT:
        y = 0

    # Limpiar la pantalla
    screen.fill(BLACK)

    # Dibujar las estrellas
    if star_visible:
        for star in stars:
            pygame.draw.circle(screen, WHITE, star, STAR_RADIUS)

    # Alternar la visibilidad de las estrellas en cada fotograma
    star_visible = not star_visible

    # Dibujar el triángulo
    triangle_points = [
        (x, y - 20),
        (x - 20, y + 20),
        (x + 20, y + 20)
    ]
    rotated_triangle = []
    for point in triangle_points:
        # Rotar el punto alrededor del centro del triángulo
        dx = point[0] - x
        dy = point[1] - y
        new_x = x + dx * math.cos(math.radians(angle)) - dy * math.sin(math.radians(angle))
        new_y = y + dx * math.sin(math.radians(angle)) + dy * math.cos(math.radians(angle))
        rotated_triangle.append((new_x, new_y))

    pygame.draw.polygon(screen, TURQUOISE, rotated_triangle)

    # Actualizar la pantalla
    pygame.display.flip()

    # Controlar la velocidad de actualización
    clock.tick(60)

# Salir de Pygame
pygame.quit()
