# example to open a html file
import webbrowser

file = "index.html"

webbrowser.open(file, new=2)  # open in new tab

# use sys module to open an arbitrary file
import sys

file = "test.txt"

sys.stdout = open(file, "w")

# run a process to open a file on the system
import subprocess

file = "test.html"

subprocess.Popen(file, shell=True)

# use os module to open a file
import os

file = "test.html"

os.startfile(file)
