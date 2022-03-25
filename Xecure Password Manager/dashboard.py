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
from input_val import validateRecordName, validateRecordPasswordAndEmail, validateEmail, validateRecordPass
import threading
import time
from hidePassword import hideRecPassword

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
                select = logout()
                if select == True:
                    break
                if select == False:
                    continue


            if menuSelection == 8:  # This will close the application
                clear()
                myExit()

            if menuSelection > 8 or menuSelection < 1:  # Input Validation
                print("\nPlease enter a number between 1 and 8.")
                print("Press any key to try again...")
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
    while True:
        try:
            clear()
            print("--------------Retrieve Record------------------\n[Enter '0' if you wish to go back to the previous screen]")  # Asks user to name the record

            if checkIfNoRecords(userId) == 0:
                print("\n**No records in database**")
                print("\nPress any key to go back to the Dashboard...")
                getch()
                clear()
                return


            print("\nEnter the name of record you wish to retrieve. ")
            recordName = input("\nRecord name: ")

            if recordName == '0':
                return '0'

            if recordName.isspace() or recordName == "":
                print("\nRecord name cannot be empty.")
                print("Press any key to try again...")
                getch()
                clear()
                continue

            if recordName.isnumeric():
                print("\nRecord name cannot be composed of only numbers.\nPress any key to try again...")
                getch()
                continue

            recordName = validateRecordName(recordName)

            if recordName == '1':
                print("\nRecord name must be at least 3 characters long.\nPress any key to try again...")
                getch()
                continue

            if recordName == '2':
                print("\nRecord name must be less than 35 characters long.\nPress any key to try again...")
                getch()
                continue

            if recordName == '3':
                print("\nRecord names must contain letters. Numbers and special characters are optional."
                    "\nSpecial characters allowed: Underscores (_), spaces ( ), and periods (.)"  
                    "\nPress any key to try again...")
                getch()
                continue

            elif recordName.isnumeric():
                print("\nRecord name cannot be composed of only numbers.")
                print("Press any key to try again...")
                getch()
                clear()
                continue

            else:
                print("Program will search for record...\n")

                userId1 = str(userId)
                recordname1 = recordName
                test = fetch_rec_by_id_gen(userId1, recordname1, "Record_Name" )

                if recordname1 == test[2]:

                    # result = get_user_record(userId, recordName)
                    print(recordName + " Record found!\n")
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
                    print( recordName + " record not found!")
                    print("Press any key to try again...")
                    getch()
                    clear()
                    continue

        except Exception:
            print("\nInvalid Input.")
            print("Press any key to try again...")
            getch()
            clear()


# Function allows user to add a new record to their pw manager account
def addRecord(userId):
    while True:
        try:
            while True:
                clear()
                print("--------------Add Record------------------\n[Enter '0' if you wish to go back to the dashboard]")  # Asks for name of record to retrieve
                print("\nEnter the name of the record (You will use this name to retrieve the record).")
                recordName = input("\nRecord Name: ")

                if recordName == '0':
                    return '0'

                if recordName.isspace() or recordName == "":
                    print("\nRecord name cannot be empty.")
                    print("Press any key to try again...")
                    getch()
                    clear()
                    continue

                if recordName.isnumeric():
                    print("\nRecord name cannot be composed of only numbers.\nPress any key to try again...")
                    getch()
                    continue

                recordName = validateRecordName(recordName)

                if recordName == '1':
                    print("\nRecord name must be at least 3 characters long.\nPress any key to try again...")
                    getch()
                    continue

                if recordName == '2':
                    print("\nRecord name must be less than 35 characters long.\nPress any key to try again...")
                    getch()
                    continue

                if recordName == '3':
                    print("\nRecord names must contain letters. Numbers and special characters are optional."
                          "\nSpecial characters allowed: Underscores (_), spaces ( ), and periods (.)"
                          "\nPress any key to try again...")
                    getch()
                    continue


                if checkDuplicateRecName(userId, recordName):
                    print("\nRecord name taken, please choose another one.")
                    print("Press any key to try again...")
                    getch()
                    clear()
                    continue


                else:
                    break

            # Asks user to enter an email for their record
            while True:
                clear()
                print("--------------Add Record------------------\n[Enter '0' if you wish to go back to the dashboard]")  # Asks for name of record to retrieve
                print("\nEnter the Email for your " + recordName + " account. (Leave blank and press enter if no email was linked to the account)")
                recordEmail = input("\nAccount/Record Email: ")

                if recordEmail == '0':
                    return '0'


                if recordEmail.isnumeric():
                    print("\nRecord email cannot be composed of only numbers.\nPress any key to try again...")
                    getch()
                    continue

                if recordEmail.isspace() or recordEmail == "":
                    break

                recordEmail = validateEmail(recordEmail)

                if recordEmail == 1:
                    print(
                        "\nRecord email must be at least 6 characters long.\nPress any key to try again...")
                    getch()
                    continue

                if recordEmail == 2:
                    print(
                        "\nRecord email must be less than 35 characters long.\nPress any key to try again...")
                    getch()
                    continue

                if recordEmail == 3:
                    print("\nRecord email must contain letters, the '@' symbol, and a period (.)."
                          "\nPress any key to try again...")
                    getch()
                    continue

                break



            while True:
                clear()
                print("--------------Add Record------------------\n[Enter '0' if you wish to go back to the dashboard]")  # Asks for name of record to retrieve
                print("\nEnter the Username for your " + recordName + " account. (Leave blank and press enter if no username was linked to the account)")
                recordUser = input("\nAccount/Record Username: ")

                if recordUser == '0':
                    return '0'


                if recordUser.isnumeric():
                    print("\nRecord username cannot be composed of only numbers.\nPress any key to try again...")
                    getch()
                    continue

                if recordUser.isspace() or recordUser == "":
                    break

                if len(recordUser) < 3:
                    print("\nRecord username must be at least 3 characters long. \nPress any key to try again...")
                    getch()
                    continue

                recordUser = validateRecordPasswordAndEmail(recordUser)


                if recordUser == 2:
                    print("\nRecord username must be less than 35 characters long.\nPress any key to try again...")
                    getch()
                    continue

                if recordUser == 3:
                    print("\nRecord username cannot be composed of only symbols and/or numbers.\nPress any key to try again...")
                    getch()
                    continue

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

                if menuSelection != "1" and menuSelection != "2" and menuSelection != "":
                    print("\nPlease select a number between 0 and 2.\nPress any key to try again...")
                    getch()
                    clear()

                if menuSelection == "":
                    print("\nSelection cannot be empty.\nPress any key to try again...")
                    getch()
                    clear()


                if menuSelection == '1':

                    recordpassword = generate_password()
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
                            print("\nSelection cannot be empty.\nPress any key to try again...")
                            getch()
                            clear()
                        elif passSelect != '1' or passSelect != '2':
                            print("\nPlease select a number between 0 and 2.\nPress any key to try again...")
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
                        print("--------------Add Record------------------\n[Enter '0' if you wish to go back to the dashboard]\n")
                        print("Please enter the following: ")
                        recordpassword = hideRecPassword()

                        if recordpassword == '0':
                            return '0'

                        if recordpassword.isspace() or recordpassword == "":
                            print("\nRecord password cannot be empty.")
                            print("Press any key to try again...")
                            getch()
                            continue


                        recordpassword = validateRecordPass(recordpassword)

                        if recordpassword == 2:
                            print("\nRecord password must be less than 35 characters long.\nPress any key to try again...")
                            getch()
                            continue

                        else:
                            end = True
                            break


                if end == True:
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
    while True:
        try:

            while True:
                try:

                    while True:
                        clear()
                        print("--------------Update Record------------------\n[Enter '0' if you wish to go back to the previous screen]")  # User needs to name the record they wish to update

                        if checkIfNoRecords(userId) == 0:
                            print("\n**No records in database**")
                            print("\nPress any key to go back to the Dashboard...")
                            getch()
                            clear()
                            return


                        print("\nEnter the name of the record you want to update")
                        oldRecordName = input("\nRecord name: ")

                        if oldRecordName == '0':
                            return '0'

                        if oldRecordName.isspace() or oldRecordName == "":
                            print("\nRecord name cannot be empty.")
                            print("Press any key to try again...")
                            getch()
                            continue

                        if oldRecordName.isnumeric():
                            print("\nRecord name cannot be composed of only numbers.")
                            print("Press any key to try again...")
                            getch()
                            continue

                        oldRecordName = validateRecordName(oldRecordName)


                        if oldRecordName == '1':
                            print("\nRecord name must be at least 3 characters long.\nPress any key to try again...")
                            getch()
                            continue

                        if oldRecordName == '2':
                            print("\nRecord name must be less than 35 characters long.\nPress any key to try again...")
                            getch()
                            continue

                        if oldRecordName == '3':
                            print("\nRecord names must contain letters. Numbers and special characters are optional."
                                  "\nSpecial characters allowed: Underscores (_), spaces ( ), and periods (.)."
                                  "\nPress any key to try again...")
                            getch()
                            continue

                        test = fetch_rec_by_id_gen(userId, oldRecordName, "Record_Name")


                        if oldRecordName == test[2]:
                            clear()
                            break

                        else:
                            print("\nRecord not found!")
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
                                print("\nPlease enter a number between 0 and 4.")
                                print("Press any key to try again...")
                                getch()
                                clear()


                            elif menuSelection == 1:
                                while True:
                                    clear()
                                    print("--------------Update Record Name------------------\n[Enter '0' if you wish to go back to the previous screen]\n")
                                    newRecordName = input("Enter the new record name: ")

                                    if newRecordName == '0':
                                        break

                                    if newRecordName == "" or newRecordName.isspace():
                                        print("\nRecord name cannot be empty.")
                                        print("Press any key to try again...")
                                        getch()
                                        clear()
                                        continue

                                    if newRecordName.isnumeric():
                                        print("\nRecord name cannot be composed of only numbers.")
                                        print("Press any key to try again...")
                                        getch()
                                        continue

                                    newRecordName = validateRecordName(newRecordName)

                                    if newRecordName == '1':
                                        print(
                                            "\nRecord name must be at least 3 characters long.\nPress any key to try again...")
                                        getch()
                                        continue

                                    if newRecordName == '2':
                                        print(
                                            "\nRecord name must be less than 35 characters long.\nPress any key to try again...")
                                        getch()
                                        continue

                                    if newRecordName == '3':
                                        print(
                                            "\nRecord names must contain letters. Numbers and special characters are optional."
                                            "\nSpecial characters allowed: Underscores (_), spaces ( ), and periods (.)."
                                            "\nPress any key to try again...")
                                        getch()
                                        continue

                                    if checkDuplicateRecName(userId, newRecordName):
                                        print("\nRecord name taken, please choose another one.")
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
                                    newEmail = input("Enter the new record email (Leave blank and press enter if no email was linked to the account): ")

                                    if newEmail == '0':
                                        break

                                    if newEmail.isnumeric():
                                        print("\nRecord email cannot be composed of only numbers.")
                                        print("Press any key to try again...")
                                        getch()
                                        continue

                                    if newEmail.isspace() or newEmail == "":
                                        update_record_email(newEmail, userId, oldRecordName)
                                        print("\nRecord email updated!\nPress any key to continue...")
                                        getch()
                                        clear()
                                        break


                                    newEmail = validateEmail(newEmail)

                                    if newEmail == 1:
                                        print(
                                            "\nRecord email must be at least 6 characters long.\nPress any key to try again...")
                                        getch()
                                        continue

                                    if newEmail == 2:
                                        print(
                                            "\nRecord email must be less than 35 characters long.\nPress any key to try again...")
                                        getch()
                                        continue

                                    if newEmail == 3:
                                        print("\nRecord email must contain letters, the '@' symbol, and a period (.)."
                                            "\nPress any key to try again...")
                                        getch()
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
                                    newRecordUserName = input("Enter the new record username (Leave blank and press enter if no username was linked to the account): ")

                                    if newRecordUserName == '0':
                                        break

                                    if newRecordUserName.isnumeric():
                                        print("\nRecord username cannot be composed of only numbers.")
                                        print("Press any key to try again...")
                                        getch()
                                        continue

                                    if newRecordUserName.isspace() or newRecordUserName == "":
                                        update_record_username(newRecordUserName, userId, oldRecordName)
                                        print("\nRecord username updated!\nPress any key to continue...")
                                        getch()
                                        clear()
                                        break

                                    if len(newRecordUserName) < 3:
                                        print("\nRecord username must be at least 3 characters long. \nPress any key to try again...")
                                        getch()
                                        continue


                                    newRecordUserName = validateRecordPasswordAndEmail(newRecordUserName)

                                    if newRecordUserName == 2:
                                        print("\nRecord name must be less than 35 characters long.\nPress any key to try again...")
                                        getch()
                                        continue

                                    if newRecordUserName == 3:
                                        print("\nRecord username cannot be composed of only symbols and/or numbers.\nPress any key to try again...")
                                        getch()
                                        continue

                                    update_record_username(newRecordUserName, userId, oldRecordName)
                                    print("\nRecord username updated!\nPress any key to continue...")
                                    getch()
                                    clear()
                                    break

                            elif menuSelection == 4:
                                while True:
                                    clear()
                                    print("--------------Update Record Password------------------\n[Enter '0' if you wish to go back to the previous screen]\n")
                                    #newRecordPassword = input("Enter the new record password: ")
                                    print("Enter the new record password:")
                                    newRecordPassword = hideRecPassword()

                                    if newRecordPassword == '0':
                                        break

                                    if newRecordPassword == "" or newRecordPassword.isspace():
                                        print("\nRecord password cannot be empty.")
                                        print("Press any key to try again...")
                                        getch()
                                        clear()
                                        continue

                                    newRecordPassword = validateRecordPass(newRecordPassword)


                                    if newRecordPassword == 2:
                                        print("\nRecord password must be less than 35 characters long.\nPress any key to try again...")
                                        getch()
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
                            print("\nInvalid input. Please enter a number between 0 and 4.\nPress any key to try again...")
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
            print("\nInvalid Input!")
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

def logout():
    # This option will let the user sign out and go back to the login screen
    while True:
        try:
            clear()
            print("--------------Logout------------------")
            print("\nAre you sure you want to logout?\n")
            print("[1] Yes")
            print("[2] No\n")
            end = int(input("Selection: "))


            if end == 1:  # If one the user will be logged out
                pyperclip.copy("")
                print("\nThank you for using Xecure Password Manager!\nPress any key to logout...")
                getch()
                usrtitle = ("title Xecure Password Manager")
                os.system(usrtitle)
                clear()
                return True

            elif end == 2:  # If two the app will go back to the dashboard
                return False

            else:  # Invalid inputs
                print("\nPlease enter a number between 1 and 2.")
                print("Press any key to try again...")
                getch()
                clear()
                continue

        except Exception:
            print("\nInvalid Input! Please enter a number between 1 and 2.")
            print("Press any key to try again...")
            getch()
            clear()
