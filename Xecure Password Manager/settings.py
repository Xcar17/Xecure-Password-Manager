#Xecure Password Manager
#By Carlos Ocasio
#Password Manager lets users create an account and allows them to safely store all of their login credentials for
#various sites. Login credentials can only be accessed by the root user. Application uses SHA256 to hash login
#credentials and encrypts the records of the user inside a secure MySQL database.

#This module contains the settings controls that give users control over their data.
import socket

from clear import clear
from msvcrt import getch
from dbsetup import delete_record, delete_all_records, fetch_rec_by_id_gen, checkIfNoRecords
from passwordRecovery import update_master_password, changeMasterEmail
from input_val import validateRecordName, validateEmail, validatePassword
import smtplib

#This function is the settings menu that contains the controls of delete a record, delete all records, change email,
#change password, change security question (Tentative Feature), and Back to dashboard.
#Gives users control over their data
def settings(userId):
    while True:
        try:
            clear()
            print("--------------Settings------------------")
            # Presents user's with all options available
            print("\nPlease select one of the following options\n")
            print("[1] Delete a Record")
            print("[2] Delete All Records")
            print("[3] Change Master Account Email")
            print("[4] Change Master Account Password")
            print("[0] Back to Dashboard\n")

            menuSelection = int(input("Selection: "))

            if menuSelection == 1:
                deleteRecord(userId)

            if menuSelection == 2:
                deleteAllRecords(userId)

            if menuSelection == 3:
                changeEmail(userId)

            if menuSelection == 4:
                result = update_master_password(userId)

                if result == True:
                    break

            if menuSelection == 0:
                clear()
                break

            if menuSelection > 4 or menuSelection < 0:
                print("\nPlease enter a number between 0 and 4")
                print("Press any key to try again...")
                getch()
                clear()

        except Exception:
            print("\nInvalid Input")
            print("Press any key to try again...")
            getch()
            clear()


#Function allows users to delete a specified record
def deleteRecord(userId):
    clear()
    ready = 1 #flag used to exit loop
    while True:
        try:
            clear()
            print("--------------Delete Record------------------\n[Enter '0' if you wish to go back to the previous screen]")

            if checkIfNoRecords(userId) == 0:
                print("\n**No records in database**")
                print("Press any key to go back to Settings...")
                getch()
                clear()
                break

            else:
                print("\nPlease enter the name of the record you wish to delete:")
                recordSelected = input("\nRecord Name: ")

                if recordSelected == '0':
                    return '0'

                if recordSelected.isspace() or recordSelected == "":
                    print("\nRecord name cannot be empty\nPress any key to continue...")
                    getch()
                    clear()
                    continue

                if recordSelected.isnumeric():
                    print("\nRecord name cannot be composed of only numbers\nPress any key to continue...")
                    getch()
                    clear()
                    continue

                recordSelected = validateRecordName(recordSelected)

                if recordSelected == '1':
                    print("\nRecord name must be at least 3 characters long\nPress any key to try again...")
                    getch()
                    continue

                if recordSelected == '2':
                    print("\nRecord name must be less than 35 characters long\nPress any key to try again...")
                    getch()
                    continue

                if recordSelected == '3':
                    print("\nRecord names must contain letters. Numbers and special characters are optional"
                          "\nSpecial characters allowed: Underscores (_), spaces ( ), and periods (.)"
                          "\nPress any key to try again...")
                    getch()
                    continue


                else:
                    test = fetch_rec_by_id_gen(userId, recordSelected, "Record_Name")
                    if recordSelected == test[2]:
                        print("\nRecord found!\nPress any key to continue...")
                        getch()
                        clear()

                        confirmation = "0"#Ensures user wants to delete this record
                        while confirmation != "1" or confirmation != "2" or confirmation == "0":
                            print("--------------Delete Record------------------")
                            print("\nAre you sure you want to delete the " + recordSelected + " record?")
                            print("[1] Yes")
                            print("[2] No, cancel and go back to Settings")
                            confirmation = input("\nSelection: ")

                            if confirmation == "1":#If 1 user wants record deleted
                                ready = 2#Flag is set to exit function
                                delete_record(recordSelected, userId)
                                print("\nRecord " + recordSelected + " was deleted!")
                                break

                            elif confirmation == "2":#Record will not be deleted if 2
                                ready = 2#Flag set to exit function
                                print("\nRecord was not deleted")
                                break

                            else:#Invalid input
                                print("\nInvalid Input\nPress any key to try again...")
                                getch()
                                clear()

                    else:#If record not fund
                        print("\nRecord not found!\nPress any key to try again...")
                        getch()
                        clear()
                        continue

            if ready == 2:#Function ready to break
                print("Press any key to go back to Settings...")
                getch()
                clear()
                break

        except Exception:
            print("\nInvalid Input")
            print("Press any key to try again...")
            getch()
            clear()


#Function deletes all record after prompting the user to confirm action
def deleteAllRecords(userId):
    try:
        confirmation = "0"
        while confirmation != "1" or confirmation != "2" or confirmation == "0":#Asks user to confirm action of delete all
            clear()
            print("--------------Delete All Records------------------")
            if checkIfNoRecords(userId) == 0:
                print("\n**No records in database**\nPress any key to go back to Settings...")
                getch()
                return

            else:
                print("\nAre you sure you want to delete all the records? (This action cannot be undone)\n")
                print("[1] Yes")
                print("[2] No, cancel and go back to Settings")
                confirmation = input("\nSelection: ")

                if confirmation == "" or confirmation.isspace():
                    print("\nSelection cannot be blank\nPress any key to try again...")
                    getch()
                    continue

                if confirmation == "1":
                    delete_all_records(userId)
                    print("Press any key to go back to Settings...")
                    getch()
                    return

                elif confirmation == "2":#If no then records will not be deleted
                    print("\nNo records erased\nPress any key to go back to Settings...")
                    getch()
                    return

                else:#if invalid input
                    print("\nInvalid Input! Please select a number between 1-2\nPress any key to try again...")
                    getch()
                    continue

    except Exception:
        print("\nInvalid Input")
        print("Press any key to try again...")
        getch()
        clear()

#Function allows user to change their email after confirming their password
def changeEmail(userId):
    clear()
    while True:
        try:
            usrEmail = changeMasterEmail(userId)

            if usrEmail == '0':
                return

            if usrEmail == False:
                print("Press any key to go back...")
                getch()
                clear()
                break

            else:
                if usrEmail == None:
                    continue


                clear()
                break


        except socket.gaierror:
            print("\nConnection error. Please check your internet connection.")
            print("Press any key to try again...")
            getch()
            clear()
            continue


        except Exception:
            print("\nInvalid Input")
            print("Press any key to try again...")
            getch()
            clear()
            continue