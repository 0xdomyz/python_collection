import random

import pygame

# Define colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Define snake movement direction constants
UP = 0
RIGHT = 1
DOWN = 2
LEFT = 3


# Define the Snake class
class Snake:
    # Initialize the snake
    def __init__(self):
        self.length = 1
        self.positions = [((SCREEN_WIDTH / 2), (SCREEN_HEIGHT / 2))]
        self.direction = random.randint(UP, LEFT)
        self.color = WHITE
        self.score = 0

    # Move the snake
    def move(self):
        # Calculate the new position of the snake's head
        cur = self.positions[0]
        x, y = cur
        if self.direction == UP:
            self.positions = [(x, y - 20)] + self.positions[:-1]
        elif self.direction == DOWN:
            self.positions = [(x, y + 20)] + self.positions[:-1]
        elif self.direction == LEFT:
            self.positions = [(x - 20, y)] + self.positions[:-1]
        elif self.direction == RIGHT:
            self.positions = [(x + 20, y)] + self.positions[:-1]

    # Check if the snake has eaten a food item
    def check_eaten_food(self, food):
        if self.positions[0] == food.position:
            self.score += 1
            self.length += 1
            return True
        else:
            return False

    # Draw the snake on the screen
    def draw(self, surface):
        for p in self.positions:
            draw_object(surface, self.color, p)


# Define the Food class
class Food:
    # Initialize the food
    def __init__(self):
        self.position = (0, 0)
        self.color = WHITE
        self.randomize_position()

    # Generate a random position for the food
    def randomize_position(self):
        self.position = (
            random.randint(0, (SCREEN_WIDTH - 20) / 20) * 20,
            random.randint(0, (SCREEN_HEIGHT - 20) / 20) * 20,
        )

    # Draw the food on the screen
    def draw(self, surface):
        draw_object(surface, self.color, self.position)


# Define a function to draw objects on the screen
def draw_object(surface, color, pos):
    r = pygame.Rect((pos[0], pos[1]), (20, 20))
    pygame.draw.rect(surface, color, r)
    pygame.draw.rect(surface, BLACK, r, 1)


# Define the main function
def main():
    pygame.init()

    # Set the screen dimensions
    global SCREEN_WIDTH
    global SCREEN_HEIGHT
    SCREEN_WIDTH = 800
    SCREEN_HEIGHT = 600

    # Set the screen title
    global screen
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set
