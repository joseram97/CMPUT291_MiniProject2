# This is the main code for the Mini Project 2 task given for CMPUT 291
# Authors: Jose Ramirez, Curtis Goud
import sqlite3
import time

def main():
    #the main code for the software applications
    #enable a print to ask the user for their username
    initializeData()

    # show the login prompt
    if not (loginPrompt()):
        return

    # the login was succesful
    # run the main portion of the code
    runApp()
    return

if __name__ == "__main__":
    main()
