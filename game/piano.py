# Import the Pygame library
import pygame

# Define the notes for the piano
notes = ["C", "D", "E", "F", "G", "A", "B"]


# Create a function to play a note
def play_note(note):
    # Use the Pygame library to play the specified note
    pygame.mixer.Sound("sounds/{}.wav".format(note)).play()


# Initialize the Pygame library
pygame.init()

# Bind the keys on your keyboard to the notes on your piano
pygame.key.set_repeat(100, 100)
while True:
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                print("You pressed the A key!")
                play_note(notes[0])
            elif event.key == pygame.K_s:
                play_note(notes[1])
            elif event.key == pygame.K_d:
                play_note(notes[2])
            elif event.key == pygame.K_f:
                play_note(notes[3])
            elif event.key == pygame.K_g:
                play_note(notes[4])
            elif event.key == pygame.K_h:
                play_note(notes[5])
            elif event.key == pygame.K_j:
                play_note(notes[6])
