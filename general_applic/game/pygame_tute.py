import pygame

# Initialize the pygame library
pygame.init()

# Set the screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Set the screen title
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Pygame Example")

# Set the screen background color
bg_color = (0, 0, 0)

# Run the main game loop
running = True
while running:
    # Process events
    for event in pygame.event.get():
        # Quit the game if the window is closed
        if event.type == pygame.QUIT:
            running = False

    # Clear the screen
    screen.fill(bg_color)

    # Update the screen
    pygame.display.flip()

# Clean up
pygame.quit()
