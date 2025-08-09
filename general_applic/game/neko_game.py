"""neko game"""

import os
import random
import subprocess
import sys
import urllib.error
import urllib.parse
import urllib.request
from io import BytesIO

import requests
from PIL import Image


def main():
    """main function"""
    print("Welcome to the neko game!")
    print("You will be asked to")
    print("enter a number between 1 and 10")
    print("If you guess the number correctly")
    print("you will be rewarded with a neko image")
    print("If you guess incorrectly")
    print("you will be punished with a neko image")
    print("You will have 3 chances to guess the number")
    print("Good luck!")
    print("")

    # generate random number
    number = random.randint(1, 10)
    # print(number)

    # set number of guesses
    guesses = 3

    # loop until guesses are used up
    while guesses > 0:
        # get user input
        guess = int(input("Enter a number: "))
        # check if guess is correct
        if guess == number:
            print("You guessed correctly!")
            print("You have been rewarded with a neko image")
            print("")
            # get neko image
            neko()
            # exit
            sys.exit()
        # check if guess is incorrect
        elif guess != number:
            print("You guessed incorrectly!")
            print("You have been punished with a neko image")
            print("")
            # get neko image
            neko()
            # decrement guesses
            guesses -= 1
            # check if guesses are used up
            if guesses == 0:
                print("You have used up all your guesses")
                print("You have been punished with a neko image")
                print("")
                # get neko image
                neko()
                # exit
                sys.exit()
            # print number of guesses left
            print("You have " + str(guesses) + " guesses left")
            print("")


def neko():
    """get neko image"""
    # get neko image
    url = "https://nekos.life/api/v2/img/neko"
    r = requests.get(url)
    data = r.json()
    image = data["url"]
    # download neko image
    req = urllib.request.Request(image)
    req.add_header(
        "User-Agent",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36",
    )
    content = urllib.request.urlopen(req).read()
    img = Image.open(BytesIO(content))
    img.save("neko.png")

    # play neko image
    subprocess.call(["display", "neko.png"])
    # delete neko image
    os.remove("neko.png")


if __name__ == "__main__":
    main()
