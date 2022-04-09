#Xecure Password Manager
#By Carlos Ocasio

#This module contains the function used throughout the application to clear the command line screen, and the function
#to exit the application properly.

import os #Used to change the title of the command line screen.
from msvcrt import getch #Used to prevent the command screen from continuing until a key is pressed
import pyperclip #Used to save record’s password into the computer’s clipboard.

#Function to clear the command screen.
def clear():
    os.system("cls")

#Function to exit program when called
def myExit():
    while True:
        clear()
        pyperclip.copy("")#Used to ensure clipboard is cleared before closing application.
        try:
            #Asks the user to confirm the action to
            print("--------------Exit------------------")
            print("\nAre you sure you want to exit and close the application?\n")
            print("[1] Yes")
            print("[2] No\n")
            end = int(input("Selection: "))

            if end == 1:#if 1(yes) the application will close
                print("\nThank you for using Xecure Password Manager! \nPress any key to exit the application...")
                getch()
                exit(0)
            elif end == 2:#if 2(no) the application will go back to prior screen
                clear()
                break
            else:#invalid input
                print("\nPlease enter a number between 1 and 2.")
                print("Press any key to try again...")
                getch()
                clear()

        except Exception:#Catches exeptions that are not expected
            print("\nInvalid Input. Please enter a number between 1 and 2.")
            print("Press any key to try again...")
            getch()
            clear()