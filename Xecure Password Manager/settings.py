#Xecure Password Manager
#By Carlos Ocasio
#Password Manager lets users create an account and allows them to safely store all of their login credentials for
#various sites. Login credentials can only be accessed by the root user. Application uses SHA256 to hash login
#credentials and encrypts the records of the user inside a secure MySQL database.

#This module contains the settings controls that give users control over their data.

from clear import clear
from msvcrt import getch
from dbsetup import delete_record, delete_all_records, fetch_rec_by_id_gen
from passwordRecovery import update_master_password, changeMasterEmail

#This function is the settings menu that contains the controls of delete a record, delete all records, change email,
#change password, change security question (Tentative Feature), and Back to dashboard.
#Gives users control over their data
def settings(currentUser):
    clear()
    while True:
        try:
            userId = input("enter User Id: ") #get_id(currentUser)
            print("--------------Settings------------------")
            # Presents user's with all options available
            print("\nWhat would you like to do?.\n")
            print("[1] Delete a Record")
            print("[2] Delete All Records")
            print("[3] Change Master Account Email")
            print("[4] Change Master Account Password")
            #print("[5] Change Security Questions (FEATURE IS TENTATIVE)")
            print("[5] Back to Dashboard\n")

            menuSelection = int(input("Selection: "))

            if menuSelection == 1:
                deleteRecord(userId)

            if menuSelection == 2:
                deleteAllRecords(userId)

            if menuSelection == 3:
                changeEmail(userId)

            if menuSelection == 4:
                update_master_password()

            # if menuSelection == 5:
            #     print("\nThis will call function lets user change Security Questions (FEATURE TENTATIVE)")
            #     print("Press any key to continue...")
            #     getch()
            #     clear()

            if menuSelection == 5:
                clear()
                break

            if menuSelection > 6 or menuSelection < 1:
                print("\nPlease enter a number between 1 and 6.")
                print("\nPress any key to try again...")
                getch()
                clear()

        except Exception:
            print("\nInvalid Input.")
            print("Press any key to try again...")
            getch()
            clear()


#Function allows users to delete a specified record
def deleteRecord(userId):
    clear()
    ready = 1 #flag used to exit loop
    while True:
        try:
            print("--------------Delete Record------------------")
            #todo implement better input val
            print("\nPlease enter the name of the record you wish to delete.")
            recordSelected = input("\nRecord Name: ")

            if recordSelected.isspace() or recordSelected == "":
                print("\nRecord name cannot be empty.\nPress any key to continue...")
                getch()
                clear()

            elif recordSelected.isnumeric():
                print("\nRecord name cannot be composed of only numbers.\nPress any key to continue...")
                getch()
                clear()


            #todo implement function to find a specific record
            else:
                test = fetch_rec_by_id_gen(userId, recordSelected, "Record_Name")
                if recordSelected == test[2]:
                    print("\nRecord found!\nPress any key to continue...")
                    getch()
                    clear()

                    confirmation = "0"#Ensures user wants to delete this record
                    #todo implement better input val
                    while confirmation != "1" or confirmation != "2" or confirmation == "0":
                        print("--------------Delete Record------------------")
                        print("\nAre you sure you want to delete the " + recordSelected + " record?")
                        print("[1] Yes")
                        print("[2] No")
                        confirmation = input("\nSelection: ")

                        if confirmation == "1":#If 1 user wants record deleted
                            ready = 2#Flag is set to exit function
                            delete_record(recordSelected, userId)
                            print("\nRecord " + recordSelected + " was deleted!")
                            #todo implement record deletion
                            break

                        elif confirmation == "2":#Record will not be deleted if 2
                            ready = 2#Flag set to exit function
                            print("\nRecord was not deleted.")
                            break

                        else:#Invalid input
                            print("\nInvalid Input!\nPress any key to try again...")
                            getch()
                            clear()

                else:#If record not fund
                    print("\nRecord not found!\nPress any key to continue...")
                    getch()
                    clear()

            if ready == 2:#Function ready to break
                print("\nPress any key to go back to Settings...")
                getch()
                clear()
                break

        except Exception:
            print("\nInvalid Input.")
            print("Press any key to try again...")
            getch()
            clear()


#Function deletes all record after prompting the user to confirm action
def deleteAllRecords(userId):
    clear()
    confirmation = "0"
    #todo implement input val
    while confirmation != "1" or confirmation != "2" or confirmation == "0":#Asks user to confirm action of delete all
        print("--------------Delete Record------------------")
        print("\nAre you sure you want to delete all the records? (This action cannot be undone)")
        print("[1] Yes (Deletes All Records)")
        print("[2] No (Does Not Delete Records)")
        confirmation = input("\nSelection: ")

        if confirmation == "1":
            #todo implement function that validates user password
            print("***Function will be called that ask user for password and if it matches records will be deleted.***")
            #password = input("\nPlease enter master account password: ")
            #todo implement input val

            #if password == "found":#if password correct delete all records
            delete_all_records(userId)
            break
                #print("All records were deleted!************PASSWORD MATCHING FEATURE NEEDS TO BE IMPLEMENTED. ONLY WORK WITH 'found' PASSWORD")
                # todo implement record deletion

            #else:#invalid rinput
                #print("\nIncorrect Password.\nPress any key to go back...")
                #getch()
                #clear()

        elif confirmation == "2":#If no then records will not be deleted
            print("\nNo record will be deleted.")
            break

        else:#if invalid input
            print("\nInvalid Input!\nPress any key to try again...")
            getch()
            clear()

    print("\nPress any key to go back...")
    getch()
    clear()


#Function allows user to change their email after confirming their password
def changeEmail(userId):
    clear()
    ready = 0#flag used to exit loop
    while True:
        try:

            exit = changeMasterEmail(userId)
            if exit == False:
                break

            else:
                print("Something went wrong...****create a confirm/exit function*****")

        except Exception:
            print("\nInvalid Input. Error 6010")
            print("Press any key to try again...")
            getch()
            clear()


#Function used to change the user's master account password
def changePassword():
    clear()
    while True:
        try:

            update_master_password()


        except Exception:
            print("\nInvalid Input.")
            print("Press any key to try again...")
            getch()
            clear()