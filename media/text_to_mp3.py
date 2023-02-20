# text to mp3
from pathlib import Path

import pyttsx3

here = Path("media/")
# here = Path(__file__).parent

# save mp3 file
def save_to_file(text, filename):
    engine = pyttsx3.init()
    engine.save_to_file(text, filename)
    engine.runAndWait()
    engine.stop()


save_to_file("Hello World", here / "test.mp3")

large_text = """
Lorem ipsum dolor sit amet, consectetur adipiscing elit.
Pellentesque nec nunc non nisl tincidunt lacinia.
Sed euismod, nisl vel tincidunt lacinia, nisl nisl aliquet nisl, nec
vulputate nisl nisl eget nisl. Donec euismod, nisl vel tincidunt
lacinia, nisl nisl aliquet nisl, nec vulputate nisl nisl eget nisl.
Donec euismod, nisl vel tincidunt lacinia, nisl nisl aliquet nisl, nec
vulputate nisl nisl eget nisl. Donec euismod, nisl vel tincidunt
lacinia, nisl nisl aliquet nisl, nec vulputate nisl nisl eget nisl.
Donec euismod, nisl vel tincidunt lacinia, nisl nisl aliquet nisl, nec
vulputate nisl nisl eget nisl. Donec euismod, nisl vel tincidunt
"""

save_to_file(large_text, here / "test2.mp3")

large_english_text = """
The quick brown fox jumps over the lazy dog.
A wizard's job is to vex chumps quickly in fog.
The five boxing wizards jump quickly.
But the jay, pig, fox, zebra, and my wolves quack!

On the first day of Christmas my true love sent to me
A partridge in a pear tree.

On the second day of Christmas my true love sent to me
Two turtle doves and a partridge in a pear tree.

On the third day of Christmas my true love sent to me
Three French hens, two turtle doves and a partridge in a pear tree.

On the fourth day of Christmas my true love sent to me
Four calling birds, three French hens, two turtle doves and a partridge in a pear tree.

"""

save_to_file(large_english_text, here / "test3.mp3")

# settings
engine = pyttsx3.init()

""" RATE"""
rate = engine.getProperty("rate")  # getting details of current speaking rate
print(rate)  # printing current voice rate
engine.setProperty("rate", 125)  # setting up new voice rate


"""VOLUME"""
volume = engine.getProperty(
    "volume"
)  # getting to know current volume level (min=0 and max=1)
print(volume)  # printing current volume level
engine.setProperty("volume", 1.0)  # setting up volume level  between 0 and 1

"""VOICE"""
voices = engine.getProperty("voices")  # getting details of current voice
# engine.setProperty('voice', voices[0].id)  #changing index, changes voices. o for male
engine.setProperty(
    "voice", voices[1].id
)  # changing index, changes voices. 1 for female

engine.say("Hello World!")
engine.say("My current speaking rate is " + str(rate))
engine.runAndWait()
engine.stop()
