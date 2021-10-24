#Xecure Password Manager
#By Carlos Ocasio
#Password Manager lets users create an account and allows them to safely store all of their login credentials for
#various sites. Login credentials can only be accessed by the root user. Application uses SHA256 to hash login
#credentials and encrypts the records of the user inside a secure MySQL database.

#This module contains the primary menu once the user logs into the application. Contains all needed controls.

import os
from clear import clear, myExit
from settings import settings
from msvcrt import getch

#Once the user logs into the application this function will be called. This is the primary menu
#It contains controls for retrieving a record, adding a record, updating a record, viewing all records, user settings
#The users can also logout and exit the application from this screen
def dashBoard():
    clear()
    while True:
        try:
            print("--------------Dash Board------------------") # Presents user's with all options available
            print("\nPlease select between the following options.\n")
            print("[1] Retrieve a Record")
            print("[2] Add a New Record")
            print("[3] Update Record")
            print("[4] View All Records")
            print("[5] User Settings")
            print("[6] Logout")
            print("[7] Exit\n")
            menuSelection = int(input("Selection: "))

            if menuSelection == 1:
                getRecord()

            if menuSelection == 2:
                addRecord()

            if menuSelection == 3:
                updateRecord()

            if menuSelection == 4:
                viewAll()

            if menuSelection == 5:
                settings()

            if menuSelection == 6:
                #This option will let the user sign out and go back to the login screen
                print("\nAre you sure you want to logout?\n")
                print("[1] Yes")
                print("[2] No\n")
                end = int(input("Selection: "))

                if end == 1:#If one the user will be logged out
                    clear()
                    print("\nThank you for using Xecure Password Manager. \nPress any key to logout...")
                    getch()
                    usrtitle = ("title Xecure Password Manager")
                    os.system(usrtitle)
                    clear()
                    break

                elif end == 2:#If two the app will go back to the dashboard
                    clear()

                else:#Invalid inputs
                    print("\nPlease enter a number between 1 and 2.")
                    print("\nPress any key to try again...")
                    getch()
                    clear()

            if menuSelection == 7:#This will close the application
                clear()
                myExit()

            if menuSelection > 7 or menuSelection < 1:#Input Validation
                print("\nPlease enter a number between 1 and 7.")
                print("\nPress any key to try again...")
                getch()
                clear()

        except Exception:
            print("\nInvalid Input.")
            print("Press any key to try again...")
            getch()
            clear()

#Function that retrieves a specified record (if found)
def getRecord():
    clear()
    while True:
        try:
            print("--------------Retrieve Record------------------") #Asks user to name the record
            print("\nEnter the name of record you wish to retrieve. ")
            recordName = input("\nRecord name: ")

            if recordName.isspace() or recordName == "":
                print("\nRecord name cannot be empty.")
                print("Press any key to try again...")
                getch()
                clear()
            elif recordName.isnumeric():
                print("\nRecord name cannot be composed of only numbers.")
                print("Press any key to try again...")
                getch()
                clear()
            else:
                print("Program will search for record.\n")

                if recordName == "Facebook": #todo temporary code and it should be replaced with func to detect record
                    print(recordName + " Record found.\n")
                    print(recordName + " Account Email: " + "THE USERS EMAIL WILL BE RETRIEVED AND DISPLAYED HERE")
                    print(recordName + " Account User Name: " + "THE USRNM WILL BE RETRIEVED AND DISPLAYED HERE")
                    print(recordName + " Account Password: " + "THE USERS RECORD PASSWORD WILL BE DISPLAYED HERE")
                    print("Press any key to go back to Dashboard...")
                    getch()
                    clear()
                    break #breaks to go back to dashboard
                else:
                    print(recordName +" record not found.")#todo implement if statement that detects if record was found
                    print("Press any key to search for another record...")#todo might need to ask if they wan to try again of go back to menu
                    getch()
                    clear()

        except Exception:
            print("\nInvalid Input.")
            print("Press any key to try again...")
            getch()
            clear()

#Function allows user to add a new record to their pw manager account
def addRecord():
    clear()
    while True:
        try:
            while True:
                print("--------------Add Record------------------")#Asks for name of record to retrieve
                print("\nEnter the name of the record (You will use this name to retrieve the record).")
                recordName = input("\nRecord name: ")#todo implement input validation
                if recordName.isspace() or recordName == "":
                    print("\nRecord name cannot be empty.")
                    print("Press any key to try again...")
                    getch()
                    clear()

                elif recordName.isnumeric():
                    print("\nRecord name cannot be composed of only numbers.")
                    print("Press any key to try again...")
                    getch()
                    clear()

                elif recordName == 'duplicate':  # todo implement function to detect if this user already has an account with this name. THis is temp code
                    print("\nRecord for " + recordName + " already exists." )
                    print("Press any key to try again...")
                    getch()
                    clear()
                else:
                    break
            #Asks user to enter an email for their record
            while True:#todo implement input validation
                print("\nEnter the Email for your " + recordName + " account.")
                recordEmail = input("\nAcount Email: ")

                #todo implement input validation for email
                break

            while True:#todo implement input validation
                print("\nEnter the Username for your " + recordName +  " account.")
                recordUser = input("\nAcount Username: ")

                #todo implement input validation for username
                break

            while True:#Allows users the option to enter a randomly generated password for their account password
                print("\nWould you like to generate a random password for your " + recordName + " account?")
                print("[1] Yes")
                print("[2] No")
                menuSelection = int(input("\nSelection: "))

                #todo implement input validation
                #If 1 randomly generated password will be created
                if menuSelection == 1:
                    print("\nA function to genearate a random password will be called here.")
                    recordpassword = ""#todo place the function to generate a random password here
                    print("Press any key to continue...")
                    getch()
                    clear()

                # If 2 user can enter their own password
                elif menuSelection == 2:
                    while True:
                        print("\nEnter the password for your " + recordName + " account")
                        recordpassword = input("\nAcount password (has to be fixed to only display ****): ")
                        # todo implement input validation
                        if recordpassword.isspace() or recordpassword == "":
                            print("\nPassword cannot be empty.")
                            print("Press any key to try again...")
                            getch()
                            clear()
                        # todo implement function to detect if this user already has an account with this name.

                        elif recordpassword.isnumeric():
                            print("\nPassword cannot be composed of only numbers.")
                            print("Press any key to try again...")
                            getch()
                            clear()
                        else:
                            break

                print("\nRecord created!")
                print("Press any key to go back to Dashboard...")
                getch()
                clear()
                break
            break
        except Exception:
            print("\nSomething went wrong. Please try again.")
            print("Press any key to try again...")
            getch()
            clear()

#Function allows users to update a previously created record
def updateRecord():
    clear()
    while True:
        try:
            while True:
                print("--------------Update Record------------------")#User needs to name the record they wish to update
                print("\nEnter the name of the record you want to update.")
                recordName = input("\nRecord name: ")#todo implement input validation

                if recordName.isspace() or recordName == "":
                    print("\nRecord name cannot be empty.")
                    print("Press any key to try again...")
                    getch()
                    clear()

                elif recordName.isnumeric():
                    print("\nRecord name cannot be composed of only numbers.")
                    print("Press any key to try again...")
                    getch()
                    clear()

                #todo look for record and see if its in db
                elif recordName == "found":################################temp code #todo replace with actual found code
                    print("\nRecord found!")
                    print("Press any key to continue...")
                    getch()
                    clear()
                    break

                else:#if record not found this will be displayed
                    print("\n" + recordName + " not found!")
                    print("Press any key to try again...")
                    getch()
                    clear()

            #ready = 1#Flag used to exit loop#todo test if you need this

            while True:#todo implement input validation
                try:
                    print("--------------Update Record------------------")
                    print("\nWhat would you like to change about the " + recordName + " record?")
                    print("[1] Change Record Name")
                    print("[2] Change Record Email")
                    print("[3] Change Record Username")
                    print("[4] Change Record Password")
                    print("[5] Back to Dashboard")
                    menuSelection = int(input("\nSelection: "))

                    if menuSelection > 5 or menuSelection < 1 or menuSelection == "":
                        print("\nPlease enter a number between 1 and 5.")
                        print("\nPress any key to try again...")
                        getch()
                        clear()

                    # todo implement all changes specified above in db
                    # todo implement input validation for all of these
                    elif menuSelection == 1:
                        change = input("Enter the new record name: ")
                        print("\nRecord name updated!\nPress any key to continue...")
                        getch()
                        clear()

                    elif menuSelection == 2:
                        change = input("Enter the new record email: ")
                        print("\nRecord email updated!\nPress any key to continue...")
                        getch()
                        clear()

                    elif menuSelection == 3:
                        change = input("Enter the new record username: ")
                        print("\nRecord username updated!\nPress any key to continue...")
                        getch()
                        clear()

                    elif menuSelection == 4:
                        change = input("Enter the new record password: ")
                        print("\nRecord password updated!\nPress any key to continue...")
                        getch()
                        clear()

                    elif menuSelection == 5:
                        #ready = 2#todo test if you need this
                        clear()
                        break

                    else:
                        print("Invalid input!\n\nPress any key to try again...")
                        clear()
                        getch

                except Exception:
                    print("\nInvalid Input.")
                    print("Press any key to try again...")
                    getch()
                    clear()
            break

        except Exception:
            print("\nInvalid Input.")
            print("Press any key to try again...")
            getch()
            clear()



#Function will display all of the records of the user
def viewAll():
    clear()
    #todo implement function that displays all records
    print("--------------View All Record------------------")
    print("\n***LIST OF ALL RECORDS WILL BE PRINTED HERE*** (TEMP CODE)")

    print("\nRecord Name: XXXXX")
    print("Record Email: XXXXX@XXXX.COM")
    print("Record Username: XXXXX")
    print("Record Password: **********")

    print("\nRecord Name: XXXXX")
    print("Record Email: XXXXX@XXXX.COM")
    print("Record Username: XXXXX")
    print("Record Password: **********")

    print("\nRecord Name: XXXXX")
    print("Record Email: XXXXX@XXXX.COM")
    print("Record Username: XXXXX")
    print("Record Password: **********")

    print("\n\nPress any key to go back to Dashboard...")
    getch()
    clear()