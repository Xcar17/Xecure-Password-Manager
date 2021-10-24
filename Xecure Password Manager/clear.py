#Xecure Password Manager
#By Carlos Ocasio
#Password Manager lets users create an account and allows them to safely store all of their login credentials for
#various sites. Login credentials can only be accessed by the root user. Application uses SHA256 to hash login
#credentials and encrypts the records of the user inside a secure MySQL database.

#This module contains the functions used throughout the application like clear and exit

import os
from msvcrt import getch

#Function to clear cmd
def clear():
    os.system("cls")

#Function to exit program when called
def myExit():
    while True:
        try:
            #Asks the user to confirm the action to exit
            print("\nAre you sure you want to exit?\n")
            print("[1] Yes")
            print("[2] No\n")
            end = int(input("Selection: "))

            if end == 1:#if 1(yes) the application will close
                print("\nThank you for using Xecure Password Manager. \nPress any key to exit the application...")
                getch()
                exit(0)
            elif end == 2:#if 2(no) the application will go back to prior screen
                clear()
                break
            else:#invalid input
                print("\nPlease enter a number between 1 and 2.")
                print("\nPress any key to try again...")
                getch()
                clear()

        except Exception:
            print("\nInvalid Input.")
            print("Press any key to try again...")
            getch()
            clear()