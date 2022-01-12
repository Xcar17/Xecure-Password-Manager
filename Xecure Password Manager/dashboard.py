# Xecure Password Manager
# By Carlos Ocasio
# Password Manager lets users create an account and allows them to safely store all of their login credentials for
# various sites. Login credentials can only be accessed by the root user. Application uses SHA256 to hash login
# credentials and encrypts the records of the user inside a secure MySQL database.
# This module contains the primary menu once the user logs into the application. Contains all needed controls.

import os
import sys

from clear import clear, myExit
from settings import settings
from msvcrt import getch
from dbsetup import update_record_name, update_record_email, printAllRecsByID, \
    update_record_username, update_record_password, adding_new_enc_record, fetch_rec_by_id_gen
from random_pwd_generator import generate_password


# Once the user logs into the application this function will be called. This is the primary menu
# It contains controls for retrieving a record, adding a record, updating a record, viewing all records, user settings
# The users can also logout and exit the application from this screen
def dashBoard(currentUser):
    clear()
    while True:
        try:

            userId = input("enter User Id: ") #get_id(currentUser)
            print("--------------Dash Board------------------")  # Presents user's with all options available
            print("\nPlease select between the following options.\n")
            print("[1] Retrieve a Record")
            print("[2] Add a New Record")
            print("[3] Update Record")
            print("[4] View All Records")
            print("[5] View All Record Names Only")
            print("[6] User Settings")
            print("[7] Logout")
            print("[8] Exit\n")
            menuSelection = int(input("Selection: "))

            if menuSelection == 1:
                getRecord(userId)

            if menuSelection == 2:
                addRecord(userId)

            if menuSelection == 3:
                updateRecord(userId)

            if menuSelection == 4:
                viewAll(userId)

            if menuSelection == 5:
                recordNamesOnly(userId, True)

            if menuSelection == 6:
                settings(currentUser)

            if menuSelection == 7:
                # This option will let the user sign out and go back to the login screen
                print("\nAre you sure you want to logout?\n")
                print("[1] Yes")
                print("[2] No\n")
                end = int(input("Selection: "))

                if end == 1:  # If one the user will be logged out
                    clear()
                    print("\nThank you for using Xecure Password Manager. \nPress any key to logout...")
                    getch()
                    usrtitle = ("title Xecure Password Manager")
                    os.system(usrtitle)
                    clear()
                    break

                elif end == 2:  # If two the app will go back to the dashboard
                    clear()

                else:  # Invalid inputs
                    print("\nPlease enter a number between 1 and 2.")
                    print("\nPress any key to try again...")
                    getch()
                    clear()

            if menuSelection == 8:  # This will close the application
                clear()
                myExit()

            if menuSelection > 8 or menuSelection < 1:  # Input Validation
                print("\nPlease enter a number between 1 and 8.")
                print("\nPress any key to try again...")
                getch()
                clear()

        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            print("\nInvalid Input. 333333")
            print("Press any key to try again...")
            getch()
            clear()


# Function that retrieves a specified record (if found)
def getRecord(userId):
    clear()
    while True:
        try:
            print("--------------Retrieve Record------------------")  # Asks user to name the record
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

                #userId1 = input("Enter ****userId: ")
                #recordname1 = input("Enter ****record Name: ")
                userId1 = str(userId)

                recordname1 = recordName
                #test = fetch_rec_by_id_name(userId1, recordname1)
                test = fetch_rec_by_id_gen(userId1, recordname1, "Record_Name" )
                #print(test)
                getch()

                if recordname1 == test[2]:  # todo replace with code to check if record is in database

                    # result = get_user_record(userId, recordName)
                    print(recordName + " Record found.\n")
                    print(recordName + " Account Email: " + test[3])
                    print(recordName + " Account Username: " + test[4])
                    print(recordName + " Account Password: " + test[5])
                    print("Press any key to go back to Dashboard...")
                    getch()
                    clear()
                    break  # breaks to go back to dashboard
                else:
                    print(
                        recordName + " record not found.")  # todo implement if statement that detects if record was found
                    print(
                        "Press any key to search for another record...")  # todo might need to ask if they wan to try again of go back to menu
                    getch()
                    clear()

        except Exception:
            print("\nInvalid Input. 10001")
            print("Press any key to try again...")
            getch()
            clear()


# Function allows user to add a new record to their pw manager account
def addRecord(userId):
    clear()
    while True:
        try:
            while True:
                print("--------------Add Record------------------")  # Asks for name of record to retrieve
                print("\nEnter the name of the record (You will use this name to retrieve the record).")
                recordName = input("\nRecord name: ")  # todo implement input validation
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
                    print("\nRecord for " + recordName + " already exists.")
                    print("Press any key to try again...")
                    getch()
                    clear()
                else:
                    break
            # Asks user to enter an email for their record
            while True:  # todo implement input validation
                print("\nEnter the Email for your " + recordName + " account.")
                recordEmail = input("\nAcount Email: ")

                # todo implement input validation for email
                break

            while True:  # todo implement input validation
                print("\nEnter the Username for your " + recordName + " account.")
                recordUser = input("\nAcount Username: ")

                # todo implement input validation for username
                break

            while True:  # Allows users the option to enter a randomly generated password for their account password
                end = False
                clear()
                print("\nWould you like to generate a random password for your " + recordName + " account?")
                print("[1] Yes")
                print("[2] No")
                menuSelection = int(input("\nSelection: "))

                # todo implement input validation
                # If 1 randomly generated password will be created
                if menuSelection == 1:

                    recordpassword = generate_password()  # todo place the function to generate a random password here
                    print("\nThe random password generated was: " + recordpassword)
                    moveOn = False
                    while moveOn == False:
                        print("\nWould you like to use this password?")
                        print("[1] Yes")
                        print("[2] No")
                        passSelect = int(input("\nSelection: "))
                        if passSelect == 1:
                            moveOn = True
                            end = True
                        elif passSelect == 2:
                            menuSelection == 2
                            moveOn = True
                        else:
                            print("\nInvalid Input 10002")


                # If 2 user can enter their own password
                if menuSelection == 2:
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
                            end = True
                            break

                if end == True:    # todo encrypt the 5 variables and send them to add_log2() function below
                    adding_new_enc_record(int(userId), recordName, recordEmail, recordUser, recordpassword)
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


# Function allows users to update a previously created record
def updateRecord(userId):
    clear()
    while True:
        try:

            while True:  # todo implement input validation
                try:
                    print(
                        "--------------Update Record------------------")  # User needs to name the record they wish to update
                    print("\nEnter the name of the record you want to update.")
                    oldRecordName = input("\nRecord name: ")  # todo implement input validation

                    if oldRecordName.isspace() or oldRecordName == "":
                        print("\nRecord name cannot be empty.")
                        print("Press any key to try again...")
                        getch()
                        clear()

                    elif oldRecordName.isnumeric():
                        print("\nRecord name cannot be composed of only numbers.")
                        print("Press any key to try again...")
                        getch()
                        clear()

                    print("--------------Update Record------------------")
                    print("\nWhat would you like to newRecordName about the " + oldRecordName + " record?")
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
                        newRecordName = input("Enter the new record name: ")
                        update_record_name(newRecordName, userId, oldRecordName)
                        print("\nRecord name updated!\nPress any key to continue...")
                        getch()
                        clear()

                    elif menuSelection == 2:
                        newEmail = input("Enter the new record email: ")
                        update_record_email(newEmail, userId, oldRecordName)
                        print("\nRecord email updated!\nPress any key to continue...")
                        getch()
                        clear()

                    elif menuSelection == 3:
                        newRecordName = input("Enter the new record username: ")
                        update_record_username(newRecordName, userId, oldRecordName)
                        print("\nRecord username updated!\nPress any key to continue...")
                        getch()
                        clear()

                    elif menuSelection == 4:
                        newRecordName = input("Enter the new record password: ")
                        update_record_password(newRecordName, userId, oldRecordName)
                        print("\nRecord password updated!\nPress any key to continue...")
                        getch()
                        clear()

                    elif menuSelection == 5:
                        # ready = 2#todo test if you need this
                        clear()
                        break

                    else:
                        print("Invalid input!\n\nPress any key to try again...")
                        clear()
                        getch()

                except Exception:
                    print("\nInvalid Input. 10003")
                    print("Press any key to try again...")
                    getch()
                    clear()
            break

        except Exception:
            print("\nInvalid Input. 10005")
            print("Press any key to try again...")
            getch()
            clear()


def viewAll(userId):
    clear()

    print("--------------View All Record------------------\n")

    printAllRecsByID(userId)
    #todo implement code that displays "no records for this account"

    print("\n\nPress any key to go back to Dashboard...")
    getch()
    clear()


def recordNamesOnly(userId, value):
    clear()

    print("--------------View All Record------------------\n")

    printAllRecsByID(userId, value)
    #todo implement code that displays "no records for this account"

    print("\n\nPress any key to go back to Dashboard...")
    getch()
    clear()
