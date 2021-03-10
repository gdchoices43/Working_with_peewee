#! /usr/bin/env python3
from collections import OrderedDict
import datetime
import sys
import os

from peewee import *

# Creating our Database
db = SqliteDatabase("diary.db")


class Entry(Model):
    # Making a text field for our content
    content = TextField()
    # Creating a time stamp for entries
    timestamp = DateTimeField(default=datetime.datetime.now)

    class Meta:
        # telling our database to use the variable we created as db to use SqliteDatabase("diary.db")
        database = db


# Our initialize function
def initialize():
    """Create the database and the table if they don't exist"""
    # Connecting to our database
    db.connect()
    # Creating our safe tables for entries
    db.create_tables([Entry], safe=True)


# Function for the option to clear the screen
def clear():
    os.system("cls" if os.name == "nt" else "clear")


# Our menu function
def menu_loop():
    """Show the menu"""
    # Setting our choice variable to None
    choice = None

    # Starting the while loop and if the user has not chosen "q" to quit
    while choice != "q":
        # While choice is not "q" call the clear function
        clear()
        # We print out this message to let them know they can type "q" to quit
        print("Enter 'q' to quit.")
        # Loop through each item in our dictionary, the key and the value
        for key, value in menu.items():
            # Then we are gonna print out the key and the values ex: key= A)  value= Add an entry
            print("{}) {}".format(key, value.__doc__))
        # Asking the user to choose an option and lowercase it and strip it
        choice = input("Action: ").lower().strip()

        # We check if it's "q" if it's not "q" we come back to our menu, we find the function
        # they have selected and we run it
        if choice in menu:
            # Before we call for a new action we clear the screen again
            clear()
            menu[choice]()


# Our function to add entries
def add_entry():
    """Add an entry."""
    # Message to user of how to complete the entry when finished, with EOF key sequence ctrl+d
    print("Enter your entry. Press ctrl+d when finished.")
    # Creating a variable to read all the content coming in and striping it of all the white space on either
    # side of it
    data = sys.stdin.read().strip()

    # If there is data input from the user
    if data:
        # If user inputs anything other than "n"
        if input("Save entry? [Y/n] ").lower() != "n":
            # Create an instance with the Entry Model where data they just typed = content
            Entry.create(content=data)
            # Message to the user that their Entry was Saved successfully
            print("Saved successfully!")


# Our function to view entries, with a search_query default of None. This let's the user search for an
# entry if they would like to find a specific one
def view_entries(search_query=None):
    """View previous entries."""
    # Creating a variable to view our entries from most recent timestamp in descending order
    entries = Entry.select().order_by(Entry.timestamp.desc())
    # Checking to see "if" a search_query was selected
    if search_query:
        # Setting a variable to check if entry where the content contains search_query
        entries = entries.where(Entry.content.contains(search_query))

    # Using a for loop to print out our entries using timestamp
    for entry in entries:
        # Setting up our timestamp up and into a string
        # %A=Weekday %B=Month %d=Number of day in month %Y=Year %I=MilitaryHour:%M=Minute %p=AM/PM
        timestamp = entry.timestamp.strftime("%A %B %d, %Y %I:%M%p")
        # Before we print out our entry we clear the screen again
        clear()
        # Creating a menu for our Actions:
        print("="*len(timestamp))
        print(timestamp)
        print("="*len(timestamp))
        print(entry.content)
        print("\n\n"+"="*len(timestamp))
        print("N) Next entry")
        print("d) Delete an entry")
        print("q) Return to main menu")

        next_action = input("Action: [N/d/q] ").lower().strip()
        if next_action == "q":
            break
        elif next_action == "d":
            delete_entry(entry)


# Creating a function to search for a specific entry
def search_entries():
    """Search entries for a string."""
    # Calling our view_entries function and asking for a string/word to search for
    view_entries(input("Search query: "))


# Our function to delete entries we no longer want
def delete_entry(entry):
    """Delete an entry."""
    # Making sure the user wants to delete the entry before we delete it
    if input("Are you sure you want to delete? [y/N] ").lower() == "y":
        entry.delete_instance()
        print("Entry deleted successfully!")


# Creating values for our users to choose from
menu = OrderedDict([
    ("a", add_entry),
    ("v", view_entries),
    ("s", search_entries),
])


# Dunder main statement
if __name__ == "__main__":
    initialize()
    menu_loop()
