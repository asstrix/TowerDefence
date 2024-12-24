import pygame
import sys

# Инициализация Pygame
pygame.init()

# Параметры окна
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Button Example")

# Цвета
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
DARK_BLUE = (0, 0, 200)

# Шрифт для текста
font = pygame.font.SysFont(None, 36)

# Создаём кнопку
button_rect = pygame.Rect(300, 250, 200, 60)  # x, y, width, height
button_color = BLUE
button_hover_color = DARK_BLUE
button_text = font.render("Click Me!", True, WHITE)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Проверка нажатия на кнопку
        if event.type == pygame.MOUSEBUTTONDOWN:
            if button_rect.collidepoint(event.pos):  # Проверяем, находится ли курсор на кнопке
                print("Button clicked!")

    # Проверка наведения мыши на кнопку
    mouse_pos = pygame.mouse.get_pos()
    if button_rect.collidepoint(mouse_pos):
        current_color = button_hover_color
    else:
        current_color = button_color

    # Отрисовка экрана
    screen.fill(WHITE)
    pygame.draw.rect(screen, current_color, button_rect)  # Рисуем кнопку
    screen.blit(button_text, (button_rect.x + 50, button_rect.y + 15))  # Рисуем текст в центре кнопки
    pygame.display.flip()

pygame.quit()
sys.exit()
