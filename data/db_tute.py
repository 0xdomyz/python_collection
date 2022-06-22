"""
https://www.sqlitetutorial.net/wp-content/uploads/2018/03/chinook.zip
"""

from dwopt import db

d = db("sqlite:///chinook.db")

d.list_tables()


