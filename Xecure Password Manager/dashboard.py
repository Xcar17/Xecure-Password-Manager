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
import pyperclip
from dbsetup import update_record_name, update_record_email, printAllRecsByID, \
    update_record_username, update_record_password, adding_new_enc_record, fetch_rec_by_id_gen, checkIfNoRecords, checkDuplicateRecName
from random_pwd_generator import generate_password
from passwordRecovery import retrieveIDByName
import threading
import time

#Function uses multithreading to flush the clipboard in the background while the user uses the application
def flushPasswordThread():
    time.sleep(15)
    pyperclip.copy("")


# Once the user logs into the application this function will be called. This is the primary menu
# It contains controls for retrieving a record, adding a record, updating a record, viewing all records, user settings
# The users can also logout and exit the application from this screen
def dashBoard(currentUser):
    pyperclip.copy("")
    while True:
        try:
            clear()
            usrId = retrieveIDByName(currentUser)
            print("--------------Dash Board------------------")  # Presents user's with all options available
            print("\nPlease select between the following options:\n")
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
                getRecord(usrId)

            if menuSelection == 2:
                addRecord(usrId)

            if menuSelection == 3:
                updateRecord(usrId)

            if menuSelection == 4:
                viewAll(usrId)

            if menuSelection == 5:
                recordNamesOnly(usrId, True)

            if menuSelection == 6:
                settings(usrId)

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
            # exc_type, exc_obj, exc_tb = sys.exc_info()
            # fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            # print(exc_type, fname, exc_tb.tb_lineno)

            print("\nPlease enter a number between 1 and 8.")
            print("Press any key to try again...")
            getch()
            clear()


# Function that retrieves a specified record (if found)
def getRecord(userId):
    clear()
    while True:
        try:
            print("--------------Retrieve Record------------------\n[Enter '0' if you wish to go back to the previous screen]")  # Asks user to name the record
            print("\nEnter the name of record you wish to retrieve. ")
            recordName = input("\nRecord name: ")

            if recordName == '0':
                return '0'

            if recordName.isspace() or recordName == "":
                print("\nRecord name cannot be empty.")
                print("Press any key to try again...")
                getch()
                clear()
                break
            elif recordName.isnumeric():
                print("\nRecord name cannot be composed of only numbers.")
                print("Press any key to try again...")
                getch()
                clear()
                break
            else:
                print("Program will search for record.\n")

                userId1 = str(userId)
                recordname1 = recordName
                test = fetch_rec_by_id_gen(userId1, recordname1, "Record_Name" )

                if recordname1 == test[2]:  # todo replace with code to check if record is in database

                    # result = get_user_record(userId, recordName)
                    print(recordName + " Record found.\n")
                    print(recordName + " Account Email: " + test[3])
                    print(recordName + " Account Username: " + test[4])
                    print(recordName + " Account Password: " + test[5])


                    pyperclip.copy(test[5])
                    print("\n**Your password will be saved to your clipboard for only 15 seconds**\n")
                    flush = threading.Thread(target=flushPasswordThread, args=())
                    flush.start()
                    print("Press any key to go back to Dashboard...")
                    getch()
                    clear()
                    break  # breaks to go back to dashboard
                else:
                    print( recordName + " record not found.")
                    print("Press any key to go back...")
                    getch()
                    clear()
                    break

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
                print("--------------Add Record------------------\n[Enter '0' if you wish to go back to the dashboard]")  # Asks for name of record to retrieve
                print("\nEnter the name of the record (You will use this name to retrieve the record).")
                recordName = input("\nRecord Name: ")  # todo implement input validation

                if recordName == '0':
                    return '0'

                if checkDuplicateRecName(userId, recordName):
                    print("\nRecord name taken, please choose another ")
                    print("Press any key to try again...")
                    getch()
                    clear()
                    continue

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
                recordEmail = input("Account Email: ")

                if recordEmail == '0':
                    return '0'

                # todo implement input validation for email
                break

            while True:  # todo implement input validation
                print("\nEnter the Username for your " + recordName + " account.")
                recordUser = input("Account Username: ")

                if recordUser == '0':
                    return '0'

                # todo implement input validation for username
                break

            while True:  # Allows users the option to enter a randomly generated password for their account password
                end = False
                clear()
                print("--------------Add Record------------------")
                print("\nWould you like to generate a random password for your " + recordName + " account?\n")
                print("[1] Yes")
                print("[2] No, I would like to create my own password")
                print("[0] Cancel and go back to dashboard")
                menuSelection = input("\nSelection: ")

                if menuSelection == '0':
                    return '0'

                # todo implement input validation
                # If 1 randomly generated password will be created

                if menuSelection != "1" and menuSelection != "2" and menuSelection != "":
                    print("\nPlease select a number between 0 and 2.\nPress any key to try again...")
                    getch()
                    clear()

                if menuSelection == "":
                    print("\nSelection cannot be blank.\nPress any key to try again...")
                    getch()
                    clear()


                if menuSelection == '1':

                    recordpassword = generate_password()  # todo place the function to generate a random password here
                    moveOn = False
                    while moveOn == False:
                        clear()
                        print("--------------Add Record------------------")
                        print("\nThe random password generated was: " + recordpassword)
                        print("\nWould you like to use this password?\n")
                        print("[1] Yes")
                        print("[2] No")
                        print("[0] Cancel and go back to dashboard\n")
                        passSelect = input("\nSelection: ")

                        if passSelect == '0':
                            return '0'

                        if passSelect == '1':
                            moveOn = True
                            end = True
                        elif passSelect == '2':
                            menuSelection == '2'
                            moveOn = True

                        elif passSelect == "":
                            print("\nSelection cannot be blank.\nPress any key to try again...")
                            getch()
                            clear()
                        elif passSelect != '1' or passSelect != '2':
                            print("\nPlease select a number between 1 and 2.\nPress any key to try again...")
                            getch()
                            clear()

                        else:
                            print("\nInvalid Input.\nPress any key to try again...")
                            getch()
                            clear()


                # If 2 user can enter their own password
                if menuSelection == '2':
                    while True:
                        clear()
                        print("--------------Add Record------------------\n[Enter '0' if you wish to go back to the dashboard]")
                        print("\nEnter the password for your " + recordName + " account:\n")
                        recordpassword = input("Acount Password: (has to be fixed to only display ****) ")

                        if recordpassword == '0':
                            return '0'

                        # todo implement input validation
                        if recordpassword.isspace() or recordpassword == "":
                            print("\nPassword cannot be empty.")
                            print("Press any key to try again...")
                            getch()
                            clear()

                        elif recordpassword.isnumeric():
                            print("\nPassword cannot be composed of only numbers.")
                            print("Press any key to try again...")
                            getch()
                            clear()
                        else:
                            end = True
                            break

                if end == True:    # todo encrypt the 5 variables and send them to add_log2() function below
                    adding_new_enc_record(userId, recordName, recordEmail, recordUser, recordpassword)
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

                    while True:
                        print("--------------Update Record------------------\n[Enter '0' if you wish to go back to the previous screen]")  # User needs to name the record they wish to update
                        print("\nEnter the name of the record you want to update.")
                        oldRecordName = input("\nRecord name: ")  # todo implement input validation

                        if oldRecordName == '0':
                            return '0'

                        test = fetch_rec_by_id_gen(userId, oldRecordName, "Record_Name")

                        if oldRecordName.isspace() or oldRecordName == "":
                            print("\nRecord name cannot be empty.")
                            print("Press any key to try again...")
                            getch()
                            clear()
                            continue

                        if oldRecordName.isnumeric():
                            print("\nRecord name cannot be composed of only numbers.")
                            print("Press any key to try again...")
                            getch()
                            clear()
                            continue

                        if oldRecordName == test[2]:
                            clear()
                            break

                        else:
                            print("\nRecord not found...")
                            print("Press any key to try again...")
                            getch()
                            clear()

                    while True:
                        try:
                            clear()
                            print("--------------Update Record------------------")
                            print("\nWhat would you like to change about your record?\n")
                            print("[1] Change Record Name")
                            print("[2] Change Record Email")
                            print("[3] Change Record Username")
                            print("[4] Change Record Password")
                            print("[0] Back to Dashboard")
                            menuSelection = int(input("\nSelection: "))


                            if menuSelection > 4 or menuSelection < 0 or menuSelection == "":
                                print("\nPlease enter a number between 0 and 4")
                                print("Press any key to try again...")
                                getch()
                                clear()


                            # todo implement all changes specified above in db
                            # todo implement input validation for all of these
                            elif menuSelection == 1:
                                while True:
                                    clear()
                                    print("--------------Update Record Name------------------\n[Enter '0' if you wish to go back to the previous screen]\n")
                                    newRecordName = input("Enter the new record name: ")

                                    if newRecordName == '0':
                                        break

                                    if checkDuplicateRecName(userId, newRecordName):
                                        print("\nRecord name taken, please choose another ")
                                        print("Press any key to try again...")
                                        getch()
                                        clear()
                                        continue

                                    if newRecordName == "":
                                        print("\nRecord Name cannot be blank")
                                        print("Press any key to try again...")
                                        getch()
                                        clear()
                                        continue

                                    update_record_name(newRecordName, userId, oldRecordName)
                                    oldRecordName = newRecordName
                                    print("\nRecord name updated!\nPress any key to continue...")
                                    getch()
                                    clear()
                                    break

                            elif menuSelection == 2:
                                while True:
                                    clear()
                                    print("--------------Update Record Email------------------\n[Enter '0' if you wish to go back to the previous screen]\n")
                                    newEmail = input("Enter the new record email: ")

                                    if newEmail == '0':
                                        break

                                    if newEmail == "":
                                        print("\nRecord email cannot be blank")
                                        print("Press any key to try again...")
                                        getch()
                                        clear()
                                        continue

                                    update_record_email(newEmail, userId, oldRecordName)
                                    print("\nRecord email updated!\nPress any key to continue...")
                                    getch()
                                    clear()
                                    break

                            elif menuSelection == 3:
                                while True:
                                    clear()
                                    print("--------------Update Record Username------------------\n[Enter '0' if you wish to go back to the previous screen]\n")
                                    newRecordName = input("Enter the new record username: ")

                                    if newRecordName == '0':
                                        break

                                    if newRecordName == "":
                                        print("\nRecord username cannot be blank")
                                        print("Press any key to try again...")
                                        getch()
                                        clear()
                                        continue

                                    update_record_username(newRecordName, userId, oldRecordName)
                                    print("\nRecord username updated!\nPress any key to continue...")
                                    getch()
                                    clear()
                                    break

                            elif menuSelection == 4:
                                while True:
                                    clear()
                                    print("--------------Update Record Password------------------\n[Enter '0' if you wish to go back to the previous screen]\n")
                                    newRecordPassword = input("Enter the new record password: ")

                                    if newRecordPassword == '0':
                                        break

                                    if newRecordPassword == "":
                                        print("\nRecord username cannot be blank")
                                        print("Press any key to try again...")
                                        getch()
                                        clear()
                                        continue

                                    update_record_password(newRecordPassword, userId, oldRecordName)
                                    print("\nRecord password updated!\nPress any key to continue...")
                                    getch()
                                    clear()
                                    break

                            elif menuSelection == 0:
                                clear()
                                return '0'


                            else:
                                print("\nInvalid input!\nPress any key to try again...")
                                clear()
                                getch()



                        except Exception:
                            print("\nInvalid input. Please enter a number between 1 and 5\nPress any key to try again...")
                            getch()
                            clear()

                    break

                except Exception:
                    print("\nInvalid Input!")
                    print("Press any key to try again...")
                    getch()
                    clear()
                break
        except Exception:
            print("\nInvalid Input. 10005")
            print("Press any key to try again...")
            getch()
            clear()

        break

def viewAll(userId):
    clear()

    print("--------------View All Record------------------\n")

    if checkIfNoRecords(userId) == 0:
        print("**No records in database**")


    else:
        printAllRecsByID(userId)


    print("\nPress any key to go back to Dashboard...")
    getch()
    clear()


def recordNamesOnly(userId, value):
    clear()

    print("--------------View All Record------------------\n")

    if checkIfNoRecords(userId) == 0:
        print("**No records in database**")

    else:
        printAllRecsByID(userId, value)

    print("\nPress any key to go back to Dashboard...")
    getch()
    clear()
