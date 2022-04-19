#Xecure Password Manager
#By Carlos Ocasio


#This module contains the settings options that give users control over their data. Users can delete records, and
#change their master email and password.

import socket #Used to catch email exceptions.
from clear import clear #Used to clear the screen.
from msvcrt import getch #Used to prevent the screen from moving to the next screen until the user is ready.
from dbsetup import delete_record, delete_all_records, fetch_rec_by_id_gen, checkIfNoRecords #Used for SQL queries.
from passwordRecovery import update_master_password, changeMasterEmail #Used for account help.
from input_val import validateRecordName #Used to validate input.


#This function is the settings menu that contains the controls of delete a record, delete all records, change email,
#change password, change security question (Tentative Feature), and Back to dashboard.
#Gives users control over their data
def settings(userId):
    while True:
        try:
            clear()
            print("--------------Settings & Delete Records------------------")
            print("\nPlease select one of the following options\n")
            print("[1] Delete a Record")
            print("[2] Delete All Records")
            print("[3] Change Master Account Email")
            print("[4] Change Master Account Password")
            print("[0] Back to Dashboard\n")
            menuSelection = int(input("Selection: "))

            if menuSelection == 1: #Calling function that deletes a record.
                deleteRecord(userId)

            if menuSelection == 2: #Calling function that deletes all records.
                deleteAllRecords(userId)

            if menuSelection == 3: #Calling function that changes master email.
                changeEmail(userId)

            if menuSelection == 4: #Calling function that updates master password.
                result = update_master_password(userId)

                if result == True: #Used to determine when to go back to dashboard in order to retrieve new userID.
                    break

            if menuSelection == 0: #Go back to previous screen.
                clear()
                break

            if menuSelection > 4 or menuSelection < 0: #Invalid numeric input.
                print("\nPlease enter a number between 0 and 4.")
                print("Press any key to try again...")
                getch()
                clear()

        except Exception: #Catching exceptions.
            print("\nInvalid Input. Please enter a number between 0 and 4.")
            print("Press any key to try again...")
            getch()
            clear()


#Function allows users to delete a specified record.
def deleteRecord(userId):
    clear()
    ready = 1 #flag used to exit loop
    while True:
        try:
            clear()
            print("--------------Delete Record------------------\n[Enter '0' if you wish to go back to "
                  "the previous screen]")
            #Checks database for records. If no records found message will be displayed letting the user know.
            if checkIfNoRecords(userId) == 0:
                print("\n**No records in database**")
                print("Press any key to go back to Settings...")
                getch()
                clear()
                break

            else: #If the user has records in the database, program will continue.
                print("\nPlease enter the name of the record you wish to delete:")
                recordSelected = input("\nRecord Name: ")

                if recordSelected == '0': #Go back to previous screen.
                    return '0'

                if recordSelected.isspace() or recordSelected == "": #If input is empty.
                    print("\nRecord name cannot be empty.\nPress any key to continue...")
                    getch()
                    clear()
                    continue

                if recordSelected.isnumeric(): #If input is numeric only.
                    print("\nRecord name cannot be composed of only numbers.\nPress any key to continue...")
                    getch()
                    clear()
                    continue

                recordSelected = validateRecordName(recordSelected) #Validates input by type.

                if recordSelected == '1': #If input is less than 3 characters.
                    print("\nRecord name must be at least 3 characters long.\nPress any key to try again...")
                    getch()
                    continue

                if recordSelected == '2': #If input is more than 35 characters.
                    print("\nRecord name must be less than 35 characters long.\nPress any key to try again...")
                    getch()
                    continue

                if recordSelected == '3': #If input does not follow format.
                    print("\nRecord names must contain letters. Numbers and special characters are optional."
                          "\nSpecial characters allowed: Underscores (_), spaces ( ), and periods (.)"
                          "\nPress any key to try again...")
                    getch()
                    continue


                else: #If no errors program will continue.

                    #Searching for record entered.
                    recordRetrieved = fetch_rec_by_id_gen(userId, recordSelected, "Record_Name")

                    #If record entered found.
                    if recordSelected == recordRetrieved[2]:
                        print("\nRecord found!\nPress any key to continue...")
                        getch()
                        clear()

                        confirmation = "0"#Ensures user wants to delete this record.
                        while confirmation != "1" or confirmation != "2" or confirmation == "0":
                            print("--------------Delete Record------------------")
                            print("\nAre you sure you want to delete the " + recordSelected + " record?")
                            print("[1] Yes")
                            print("[2] No, cancel and go back to Settings")
                            confirmation = input("\nSelection: ")

                            if confirmation == "1":#If 1 user wants record deleted.
                                ready = 2#Flag is set to exit function.
                                delete_record(recordSelected, userId) #Deleting record selected.
                                print("\nRecord " + recordSelected + " was deleted!")
                                break

                            elif confirmation == "2":#Record will not be deleted if 2.
                                ready = 2#Flag set to exit function.
                                print("\nRecord was not deleted!")
                                break

                            else:#Invalid input.
                                print("\nInvalid Input. Please enter a number between 1 and 2.\nPress any key"
                                      " to try again...")
                                getch()
                                clear()

                    else:#If record not found.
                        print("\nRecord not found!\nPress any key to try again...")
                        getch()
                        clear()
                        continue

            if ready == 2:#Function ready to break.
                print("Press any key to go back to Settings...")
                getch()
                clear()
                break

        except Exception: #Catching other exceptions.
            print("\nInvalid Input.")
            print("Press any key to try again...")
            getch()
            clear()


#Function deletes all record after prompting the user to confirm action.
def deleteAllRecords(userId):
    try:
        confirmation = "0"
        while confirmation != "1" or confirmation != "2" or confirmation == "0":#User confirm action of delete all.
            clear()
            print("--------------Delete All Records------------------\n[Enter '0' if you wish to go back to "
                  "the previous screen]")

            #Checking if users has records in database. Error message will be displayed if no records.
            if checkIfNoRecords(userId) == 0:
                print("\n**No records in database**\nPress any key to go back to Settings...")
                getch()
                return

            else: #If records found.
                print("\nAre you sure you want to delete all the records? (This action cannot be undone)\n")
                print("[1] Yes")
                print("[2] No, cancel and go back to Settings")
                confirmation = input("\nSelection: ")

                if confirmation == "" or confirmation.isspace(): #If input is empty.
                    print("\nSelection cannot be blank.\nPress any key to try again...")
                    getch()
                    continue

                if confirmation == "1": #If 1, all records will be deleted for the logged in user.
                    delete_all_records(userId)
                    print("Press any key to go back to Settings...")
                    getch()
                    return

                elif confirmation == "2":#If 2 then records will not be deleted.
                    print("\nNo records erased!\nPress any key to go back to Settings...")
                    getch()
                    return

                else:#if invalid input.
                    print("\nInvalid Input. Please enter a number between 1 and 2.\nPress any key to try again...")
                    getch()
                    continue

    except Exception: #Catching exceptions.
        print("\nInvalid Input.")
        print("Press any key to try again...")
        getch()
        clear()

#Function allows user to change their email after confirming their password
def changeEmail(userId):
    clear()
    while True:
        try:
            #Calling functions that allows user to change password.
            usrEmail = changeMasterEmail(userId)

            if usrEmail == '0': #Command to go back to previous screen.
                return

            if usrEmail == False: #If error, user will be taken back
                print("Press any key to go back...")
                getch()
                clear()
                break

            else:
                if usrEmail == None: #If none, loop will start over.
                    continue

                clear()
                break


        except socket.gaierror: #Error is displayed if a connection cannot be established.
            print("\nConnection error. Please check your internet connection.")
            print("Press any key to try again...")
            getch()
            clear()
            continue


        except Exception: #Catching other errors.
            print("\nInvalid Input.")
            print("Press any key to try again...")
            getch()
            clear()
            continue