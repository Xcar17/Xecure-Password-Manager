# Xecure Password Manager
# By Carlos Ocasio

#This module contains the primary menu once the user logs into the application. Contains all needed controls that the
#user interacts with. The following controls are contained within this modules:
#Flushing password, dashboard, retrieving records, adding records, update records, view all records, and logout

import os #Used to change the title of the command line screen.
from clear import clear, myExit #Used in this module to clear command line and properly exit the application.
from settings import settings #Used as one of the commands a user can select.
from msvcrt import getch #Prevents the command screen from continuing to the next screen until a key is pressed.
import pyperclip #Used to enable the functions of the clipboard.
from dbsetup import update_record_name, update_record_email, printAllRecsByID, \
    update_record_username, update_record_password, adding_new_enc_record, fetch_rec_by_id_gen, checkIfNoRecords,\
    checkDuplicateRecName #The functions in this module contain the majority of the sql queries,
from random_pwd_generator import generate_password_long #Used to generate passwords.
from passwordRecovery import retrieveIDByName #Used to retrieve the user's ID
from input_val import validateRecordName, validateRecordUserPasswordAndEmail, validateEmail, \
    validateRecordPass #Used for validation
import threading #Used to clear the clipboard after 15 seconds. This is done in the background.
import time #Sets a 15 second time for the clipboard to be wiped.
from hidePassword import hideRecPassword #Used to hide the password being entered to the screen.

#Function uses multithreading to flush the clipboard in the background while the user uses the application.
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
            print("--------------Dashboard------------------")  # Presents user's with all options available
            print("\nPlease select between the following options:\n")
            print("[1] Retrieve a Record")
            print("[2] Add a New Record")
            print("[3] Update Record")
            print("[4] View All Records")
            print("[5] View All Record Names Only")
            print("[6] Settings & Delete Records")
            print("[7] Logout")
            print("[8] Exit\n")
            menuSelection = int(input("Selection: "))

            if menuSelection == 1: #Calls retrieve record function
                getRecord(usrId)

            if menuSelection == 2: #Calls add record function.
                addRecord(usrId)

            if menuSelection == 3: #Calls update record function
                updateRecord(usrId)

            if menuSelection == 4: #Calls view all records function
                viewAll(usrId)

            if menuSelection == 5:  #Calls view all record names function
                recordNamesOnly(usrId, True)

            if menuSelection == 6: #Calls settings function
                settings(usrId)

            if menuSelection == 7: #Calls the logout function
                select = logout()
                #Select is used to exit/loop the function
                if select == True:
                    break
                if select == False:
                    continue

            if menuSelection == 8:  # Calls the exit function
                clear()
                myExit()

            if menuSelection > 8 or menuSelection < 1:  # Invalid integer inputs will display message below
                print("\nPlease enter a number between 1 and 8.")
                print("Press any key to try again...")
                getch()
                clear()

        except Exception:
            print("\nPlease enter a number between 1 and 8.")
            print("Press any key to try again...")
            getch()
            clear()


# Function that retrieves a specified record (if found). User has to type in the record name in order to retrieve it.
def getRecord(userId):
    while True:
        try:
            clear()
            print("--------------Retrieve Record------------------\n[Enter '0' if you wish to go back to the previous "
                  "screen]")  # Asks user to name the record

            #If there are no records in the user's account, they will see a "no records in database" message.
            if checkIfNoRecords(userId) == 0:
                print("\n**No records in database**")
                print("\nPress any key to go back to the Dashboard...")
                getch()
                clear()
                return


            print("\nEnter the name of record you wish to retrieve. ")
            recordName = input("\nRecord name: ")

            if recordName == '0': #Used to go back to previous menu.
                return '0'

            if recordName.isspace() or recordName == "": #Checks for empty input.
                print("\nRecord name cannot be empty.")
                print("Press any key to try again...")
                getch()
                clear()
                continue

            if recordName.isnumeric(): #Checks for numeric only input.
                print("\nRecord name cannot be composed of only numbers.\nPress any key to try again...")
                getch()
                continue

            recordName = validateRecordName(recordName) #calls function that validates input.

            if recordName == '1': #If entered input is shorter than 3 characters.
                print("\nRecord name must be at least 3 characters long.\nPress any key to try again...")
                getch()
                continue

            if recordName == '2': #If record is longer than 35 characters.
                print("\nRecord name must be less than 35 characters long.\nPress any key to try again...")
                getch()
                continue

            if recordName == '3': #If record does not match format.
                print("\nRecord names must contain letters. Numbers and special characters are optional."
                    "\nSpecial characters allowed: Underscores (_), spaces ( ), and periods (.)"  
                    "\nPress any key to try again...")
                getch()
                continue

            elif recordName.isnumeric(): #if record is numberic.
                print("\nRecord name cannot be composed of only numbers.")
                print("Press any key to try again...")
                getch()
                clear()
                continue

            else: #If the input entered is valid search for record.
                print("Program will search for record...\n")

                userIdString = str(userId) #Converting userID to string.
                recordNameOriginal = recordName #Creating a new variable with the same value (to be used later).
                recordRetrieved = fetch_rec_by_id_gen(userIdString, recordNameOriginal, "Record_Name" ) #Retrieving.

                #If the record entered is found on the user's database, its information will be displayed.
                if recordNameOriginal == recordRetrieved[2]:
                    print(recordName + " Record found!\n")
                    print(recordName + " Account Email: " + recordRetrieved[3])
                    print(recordName + " Account Username: " + recordRetrieved[4])
                    print(recordName + " Account Password: " + recordRetrieved[5])

                    pyperclip.copy(recordRetrieved[5]) #Copies password into clipboard for 15 seconds.
                    print("\n**Your password will be saved to your clipboard for only 15 seconds**\n")

                    #Starting a new thread to countdown the 15 seconds.
                    flush = threading.Thread(target=flushPasswordThread, args=())
                    flush.daemon = True
                    flush.start()
                    print("Press any key to go back to Dashboard...")
                    getch()
                    clear()
                    break  # Breaks to go back to dashboard.

                #If record entered not found, an error is displayed.
                else:
                    print( recordName + " record not found!")
                    print("Press any key to try again...")
                    getch()
                    clear()
                    continue

        #Handling unexpected behavior.
        except Exception:
            print("\nInvalid Input.")
            print("Press any key to try again...")
            getch()
            clear()


# Function allows user to add a new record to their account. Users can also call the password generator from this
# function in order to create secure passwords.
def addRecord(userId):
    while True:
        try:
            while True:
                clear()
                print("--------------Add Record------------------\n[Enter '0' if you wish to go back to the dashboard]")
                print("\nEnter the name of the record (You will use this name to retrieve the record).")
                recordName = input("\nRecord Name: ")

                if recordName == '0':# Return to the previous screen.
                    return '0'

                if recordName.isspace() or recordName == "": # If input is empty.
                    print("\nRecord name cannot be empty.")
                    print("Press any key to try again...")
                    getch()
                    clear()
                    continue

                if recordName.isnumeric(): #If input is numeric.
                    print("\nRecord name cannot be composed of only numbers.\nPress any key to try again...")
                    getch()
                    continue

                recordName = validateRecordName(recordName) #Validating user input according to type.

                if recordName == '1': #If input is less than 3 characters.
                    print("\nRecord name must be at least 3 characters long.\nPress any key to try again...")
                    getch()
                    continue

                if recordName == '2': #If input is longer than 35 characters long.
                    print("\nRecord name must be less than 35 characters long.\nPress any key to try again...")
                    getch()
                    continue

                if recordName == '3': #If input does not follow the correct format.
                    print("\nRecord names must contain letters. Numbers and special characters are optional."
                          "\nSpecial characters allowed: Underscores (_), spaces ( ), and periods (.)"
                          "\nPress any key to try again...")
                    getch()
                    continue


                if checkDuplicateRecName(userId, recordName): #Checking for duplicate records.
                    print("\nRecord name taken. Please choose another record name.")
                    print("Press any key to try again...")
                    getch()
                    clear()
                    continue

                else:   #Continue if no errors found in name
                    break

            # Asks user to enter an email for their record
            while True:
                clear()
                print("--------------Add Record------------------\n[Enter '0' if you wish to go back to the dashboard]")
                print("\nEnter the Email for your " + recordName + " account. (Leave blank and press enter if no email"
                                                                   " was linked to the account)")
                recordEmail = input("\nAccount/Record Email: ")

                if recordEmail == '0': #Return to previous screen.
                    return '0'


                if recordEmail.isnumeric(): #If input is numeric only.
                    print("\nRecord email cannot be composed of only numbers.\nPress any key to try again...")
                    getch()
                    continue

                if recordEmail.isspace() or recordEmail == "": #If email is empty continue to the next step.
                    break                                       #Records can have empty emails.

                recordEmail = validateEmail(recordEmail) #Validating the input according to type.

                if recordEmail == 1: #If input is shorter than 6 characters.
                    print("\nRecord email must be at least 6 characters long.\nPress any key to try again...")
                    getch()
                    continue

                if recordEmail == 2: #If input is more than 35 characters.
                    print("\nRecord email must be less than 35 characters long.\nPress any key to try again...")
                    getch()
                    continue

                if recordEmail == 3: #If input does not follow format.
                    print("\nRecord email must contain letters, the '@' symbol, and a period (.)."
                          "\nPress any key to try again...")
                    getch()
                    continue

                break #If no errors continue to next step


            #Asking for username
            while True:
                clear()
                print("--------------Add Record------------------\n[Enter '0' if you wish to go back to the dashboard]")
                print("\nEnter the Username for your " + recordName + " account. (Leave blank and press enter if no "
                                                                      "username was linked to the account)")
                recordUser = input("\nAccount/Record Username: ")

                if recordUser == '0': #Return to previous screen.
                    return '0'

                if recordUser.isnumeric(): #If input is numeric.
                    print("\nRecord username cannot be composed of only numbers.\nPress any key to try again...")
                    getch()
                    continue

                if recordUser.isspace() or recordUser == "": #If input is empty.
                    break                                    #Username can be empty.

                if len(recordUser) < 3: #If record name is less than 3 characters.
                    print("\nRecord username must be at least 3 characters long. \nPress any key to try again...")
                    getch()
                    continue

                recordUser = validateRecordUserPasswordAndEmail(recordUser) #Validate input.


                if recordUser == 2: #If input is longer than 35 characters.
                    print("\nRecord username must be less than 35 characters long.\nPress any key to try again...")
                    getch()
                    continue #Continue if no errors.

                if recordUser == 3: #If input does not follow format.
                    print("\nRecord username cannot be composed of only symbols and/or numbers.\nPress any key to try"
                          " again...")
                    getch()
                    continue

                break

            # Allows users the option to enter a randomly generated password for their account password
            while True:
                end = False
                clear()
                print("--------------Add Record------------------")
                print("\nWould you like to generate a random password for your " + recordName + " account?\n")
                print("[1] Yes")
                print("[2] No, I would like to create my own password")
                print("[0] Cancel and go back to dashboard")
                menuSelection = input("\nSelection: ")

                if menuSelection == '0': #Going back to previous screen.
                    return '0'

                if menuSelection != "1" and menuSelection != "2" and menuSelection != "": #Invalid selection
                    print("\nPlease select a number between 0 and 2.\nPress any key to try again...")
                    getch()
                    clear()

                if menuSelection == "": #If selection is empty.
                    print("\nSelection cannot be empty.\nPress any key to try again...")
                    getch()
                    clear()


                if menuSelection == '1': #If user wishes to generate a password.

                    recordpassword = generate_password_long() #Calling function to generate password.
                    moveOn = False #Variable used as flag to exit.
                    while moveOn == False:
                        clear()
                        print("--------------Add Record------------------")
                        print("\nThe random password generated was: " + recordpassword)
                        print("\nWould you like to use this password?\n")
                        print("[1] Yes")
                        print("[2] No")
                        print("[0] Cancel and go back to dashboard\n")
                        passSelect = input("\nSelection: ")

                        if passSelect == '0': #Go back to dashboard.
                            return '0'

                        if passSelect == '1': #Choosing the password generated ends the loop and record is created.
                            moveOn = True
                            end = True
                        elif passSelect == '2': #If user does not want to use password, they are taken back.
                            menuSelection == '2'
                            moveOn = True

                        elif passSelect == "": #If empty input.
                            print("\nSelection cannot be empty.\nPress any key to try again...")
                            getch()
                            clear()
                        elif passSelect != '1' or passSelect != '2': #If invalid numeric input.
                            print("\nPlease select a number between 0 and 2.\nPress any key to try again...")
                            getch()
                            clear()

                        else: #If other invalid input.
                            print("\nInvalid Input.\nPress any key to try again...")
                            getch()
                            clear()


                # If 2 user can enter their own password.
                if menuSelection == '2':
                    while True:
                        clear()
                        print("--------------Add Record------------------\n[Enter '0' if you wish to go back to the"
                              " dashboard]\n")
                        print("Please enter the following: ")
                        recordpassword = hideRecPassword() #Calls function to hide password.

                        if recordpassword == '0': #Go back to previous screen.
                            return '0'

                        if recordpassword.isspace() or recordpassword == "": #If empty input.
                            print("\nRecord password cannot be empty.")
                            print("Press any key to try again...")
                            getch()
                            continue

                        #validating password input. Has to be less strict than master password.
                        recordpassword = validateRecordPass(recordpassword)

                        if recordpassword == 2: #Password longer than 35 characters.
                            print("\nRecord password must be less than 35 characters long.\nPress any key to try"
                                  " again...")
                            getch()
                            continue

                        else: #If no errors, create record.
                            end = True
                            break


                if end == True: #Sends data to SQL database.
                    adding_new_enc_record(userId, recordName, recordEmail, recordUser, recordpassword)
                    print("\nRecord created!")
                    print("Press any key to go back to Dashboard...")
                    getch()
                    clear()
                    break

            break

        except Exception: #Catching unexpected exceptions.
            print("\nSomething went wrong. Please try again.")
            print("Press any key to try again...")
            getch()
            clear()


# Function allows users to update a previously created record.
def updateRecord(userId):
    while True:
        try:

            while True:
                try:

                    while True:
                        clear()
                        print("--------------Update Record------------------\n[Enter '0' if you wish to go back to the"
                              " previous screen]")

                        #Checking if the user has any records in the database.
                        if checkIfNoRecords(userId) == 0: #If no records in database, user cannot use this feature.
                            print("\n**No records in database**")
                            print("\nPress any key to go back to the Dashboard...")
                            getch()
                            clear()
                            return

                        print("\nEnter the name of the record you want to update")
                        oldRecordName = input("\nRecord name: ")

                        if oldRecordName == '0': #Go back to previous screen.
                            return '0'

                        if oldRecordName.isspace() or oldRecordName == "": #If input is empty.
                            print("\nRecord name cannot be empty.")
                            print("Press any key to try again...")
                            getch()
                            continue

                        if oldRecordName.isnumeric(): #If input is numeric only.
                            print("\nRecord name cannot be composed of only numbers.")
                            print("Press any key to try again...")
                            getch()
                            continue

                        oldRecordName = validateRecordName(oldRecordName) #Validating input by type.


                        if oldRecordName == '1': #If input is less than 3 characters.
                            print("\nRecord name must be at least 3 characters long.\nPress any key to try again...")
                            getch()
                            continue

                        if oldRecordName == '2': #If inputs is more than 35 characters.
                            print("\nRecord name must be less than 35 characters long.\nPress any key to try again...")
                            getch()
                            continue

                        if oldRecordName == '3': #If input does not follow the format.
                            print("\nRecord names must contain letters. Numbers and special characters are optional."
                                  "\nSpecial characters allowed: Underscores (_), spaces ( ), and periods (.)."
                                  "\nPress any key to try again...")
                            getch()
                            continue

                        #Fetching the record entered.
                        retrievedRecord = fetch_rec_by_id_gen(userId, oldRecordName, "Record_Name")

                        #If record entered is found, continue to the next step.
                        if oldRecordName == retrievedRecord[2]:
                            clear()
                            break

                        else: #If record not found, user cannot continue.
                            print("\nRecord not found!")
                            print("Press any key to try again...")
                            getch()
                            clear()

                    #If record found, what would you like to change?
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

                            #If invalid numeric input.
                            if menuSelection > 4 or menuSelection < 0 or menuSelection == "":
                                print("\nPlease enter a number between 0 and 4.")
                                print("Press any key to try again...")
                                getch()
                                clear()

                            #If Changing record name.
                            elif menuSelection == 1:
                                while True:
                                    clear()
                                    print("--------------Update Record Name------------------\n[Enter '0' if you wish"
                                          " to go back to the previous screen]\n")
                                    newRecordName = input("Enter the new record name: ")

                                    if newRecordName == '0': #Go back to previous screen.
                                        break

                                    #If input is empty.
                                    if newRecordName == "" or newRecordName.isspace():
                                        print("\nRecord name cannot be empty.")
                                        print("Press any key to try again...")
                                        getch()
                                        clear()
                                        continue

                                    if newRecordName.isnumeric(): #If input is numric only.
                                        print("\nRecord name cannot be composed of only numbers.")
                                        print("Press any key to try again...")
                                        getch()
                                        continue

                                    newRecordName = validateRecordName(newRecordName) #Validating input based on type.

                                    if newRecordName == '1': #If input is shorter than 3 characters.
                                        print("\nRecord name must be at least 3 characters long.\nPress any key to try "
                                              "again...")
                                        getch()
                                        continue

                                    if newRecordName == '2': #If input is longer than 35 characters.
                                        print(
                                            "\nRecord name must be less than 35 characters long.\nPress any key to try "
                                            "again...")
                                        getch()
                                        continue

                                    if newRecordName == '3': #If input does not follow the proper format.
                                        print(
                                            "\nRecord names must contain letters. Numbers and special characters are "
                                            "optional."
                                            "\nSpecial characters allowed: Underscores (_), spaces ( ), and "
                                            "periods (.)."
                                            "\nPress any key to try again...")
                                        getch()
                                        continue

                                    if checkDuplicateRecName(userId, newRecordName): #Checks for duplicate record name.
                                        print("\nRecord name taken, please choose another one.")
                                        print("Press any key to try again...")
                                        getch()
                                        clear()
                                        continue

                                    #Updates the record to the new name
                                    update_record_name(newRecordName, userId, oldRecordName)
                                    oldRecordName = newRecordName #Changing the value of the variable.
                                    print("\nRecord name updated!\nPress any key to continue...")
                                    getch()
                                    clear()
                                    break

                            elif menuSelection == 2: #If changing record email.
                                while True:
                                    clear()
                                    print("--------------Update Record Email------------------\n[Enter '0' if you wish "
                                          "to go back to the previous screen]\n")
                                    newEmail = input("Enter the new record email (Leave blank and press enter if no "
                                                     "email was linked to the account): ")

                                    if newEmail == '0': #Go back to previous screen.
                                        break

                                    if newEmail.isnumeric(): #If input is numeric only.
                                        print("\nRecord email cannot be composed of only numbers.")
                                        print("Press any key to try again...")
                                        getch()
                                        continue

                                    if newEmail.isspace() or newEmail == "": #If input is empty, the record is updated.
                                        update_record_email(newEmail, userId, oldRecordName)
                                        print("\nRecord email updated!\nPress any key to continue...")
                                        getch()
                                        clear()
                                        break


                                    newEmail = validateEmail(newEmail) #Valiating input by type.

                                    if newEmail == 1: #If input is less than 6 characters.
                                        print("\nRecord email must be at least 6 characters long.\nPress any key to try"
                                              " again...")
                                        getch()
                                        continue

                                    if newEmail == 2: #If inputs is more than 35 characters.
                                        print("\nRecord email must be less than 35 characters long.\nPress any key to "
                                              "try again...")
                                        getch()
                                        continue

                                    if newEmail == 3: #If input does not follow format.
                                        print("\nRecord email must contain letters, the '@' symbol, and a period (.)."
                                            "\nPress any key to try again...")
                                        getch()
                                        continue
                                    #Updates record email.
                                    update_record_email(newEmail, userId, oldRecordName)
                                    print("\nRecord email updated!\nPress any key to continue...")
                                    getch()
                                    clear()
                                    break

                            elif menuSelection == 3: #If changing record username.
                                while True:
                                    clear()
                                    print("--------------Update Record Username------------------\n[Enter '0' if you"
                                          " wish to go back to the previous screen]\n")
                                    newRecordUserName = input("Enter the new record username (Leave blank and press "
                                                              "enter if no username was linked to the account): ")

                                    if newRecordUserName == '0': #Go back to previous menu.
                                        break

                                    if newRecordUserName.isnumeric(): #If input is numeric only.
                                        print("\nRecord username cannot be composed of only numbers.")
                                        print("Press any key to try again...")
                                        getch()
                                        continue

                                    if newRecordUserName.isspace() or newRecordUserName == "": #If input is empty.
                                        #Empyt usernames are valid, and thus the record will be updated.
                                        update_record_username(newRecordUserName, userId, oldRecordName)
                                        print("\nRecord username updated!\nPress any key to continue...")
                                        getch()
                                        clear()
                                        break

                                    if len(newRecordUserName) < 3: #If input is less than 3 chracters.
                                        print("\nRecord username must be at least 3 characters long. \nPress any key to "
                                              "try again...")
                                        getch()
                                        continue

                                    #Validating input by type.
                                    newRecordUserName = validateRecordUserPasswordAndEmail(newRecordUserName)

                                    if newRecordUserName == 2: #If input is longer than 35 characters.
                                        print("\nRecord name must be less than 35 characters long.\nPress any key to"
                                              " try"
                                              " again...")
                                        getch()
                                        continue

                                    if newRecordUserName == 3: #If input does not follow the format.
                                        print("\nRecord username cannot be composed of only symbols and/or numbers."
                                              "\nPress any key to try again...")
                                        getch()
                                        continue

                                    #Updates record to input entered.
                                    update_record_username(newRecordUserName, userId, oldRecordName)
                                    print("\nRecord username updated!\nPress any key to continue...")
                                    getch()
                                    clear()
                                    break

                            elif menuSelection == 4: #If updating password.
                                while True:
                                    clear()
                                    print("--------------Update Record Password------------------\n[Enter '0' if you "
                                          "wish to go back to the previous screen]\n")
                                    #newRecordPassword = input("Enter the new record password: ")
                                    print("Enter the new record password:")
                                    newRecordPassword = hideRecPassword()

                                    if newRecordPassword == '0': #Go back to previous menu.
                                        break

                                    #If input is empty.
                                    if newRecordPassword == "" or newRecordPassword.isspace():
                                        print("\nRecord password cannot be empty.")
                                        print("Press any key to try again...")
                                        getch()
                                        clear()
                                        continue

                                    #Validating input by type.
                                    newRecordPassword = validateRecordPass(newRecordPassword)


                                    if newRecordPassword == 2:
                                        print("\nRecord password must be less than 35 characters long.\nPress any key "
                                              "to try again...")
                                        getch()
                                        continue

                                    #Updating record password.
                                    update_record_password(newRecordPassword, userId, oldRecordName)
                                    print("\nRecord password updated!\nPress any key to continue...")
                                    getch()
                                    clear()
                                    break

                            elif menuSelection == 0: #Go ba to previous menu.
                                clear()
                                return '0'


                            else: #If invalid input
                                print("\nInvalid input!\nPress any key to try again...")
                                clear()
                                getch()



                        except Exception: #If invalid input
                            print("\nInvalid input. Please enter a number between 0 and 4.\nPress any key to try "
                                  "again...")
                            getch()
                            clear()

                    break

                except Exception: #If invalid input
                    print("\nInvalid Input!")
                    print("Press any key to try again...")
                    getch()
                    clear()
                break
        except Exception: #If invalid input
            print("\nInvalid Input!")
            print("Press any key to try again...")
            getch()
            clear()

        break

#Fucntion allows users to display all of their records and the information within them.
def viewAll(userId):
    clear()
    print("--------------View All Record------------------\n")

    #If no records in user database, a message will be displayed.
    if checkIfNoRecords(userId) == 0:
        print("**No records in database**")

    else: #If there are records in the user's database, display all records.
        printAllRecsByID(userId)

    print("\nPress any key to go back to Dashboard...")
    getch()
    clear()


#Function allows users to display only the name of their records. This can be used in order to find out what records a
#user has. This is safer than using the view all option since it does not display passwords.
def recordNamesOnly(userId, value):
    clear()

    print("--------------View All Record Names------------------\n")
    # If no records in user database, a message will be displayed.
    if checkIfNoRecords(userId) == 0:
        print("**No records in database**")

    else:#If there are records in the user's database, display all record names.
        printAllRecsByID(userId, value)

    print("\nPress any key to go back to Dashboard...")
    getch()
    clear()

#Function that allows the user to safely log out of the application.
# This option will let the user sign out and go back to the login screen
def logout():
    while True:
        try:
            clear()
            print("--------------Logout------------------")
            print("\nAre you sure you want to logout?\n")
            print("[1] Yes")
            print("[2] No\n")
            end = int(input("Selection: "))

            if end == 1:  # If one the user will be logged out.
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

        except Exception: #Catching exceptions.
            print("\nInvalid Input! Please enter a number between 1 and 2.")
            print("Press any key to try again...")
            getch()
            clear()