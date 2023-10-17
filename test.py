import pygame

# Pygame initialization
pygame.init()
width, height = 800, 600
screen = pygame.display.set_mode((width, height))

# Create a transparent surface with a size
transparent_surface = pygame.Surface((200, 200), pygame.SRCALPHA)

# Set the alpha value for transparency (0-255)
alpha = 51  # 0.2 * 255
transparent_surface.fill((255, 255, 255))
transparent_surface.set_alpha(alpha)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((0, 0, 0))
    pygame.draw.circle(screen, (255, 0, 0), (100, 100), 50)

    # Draw the transparent surface on the main screen
    screen.blit(transparent_surface, (300, 300))

    pygame.display.flip()

pygame.quit()
