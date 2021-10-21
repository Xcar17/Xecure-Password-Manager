from msvcrt import getch
import os
import getpass
import sys
import hashlib







#Promt to ask user for password this will be the setup before the hashin (need to understand this code a little more)
def mpass(prompt='\nPlease enter your password: '):
    if sys.stdin is not sys.__stdin__:
        pwd = getpass.getpass(prompt)
        return pwd
    else:
        pwd = ""
        sys.stdout.write(prompt)
        sys.stdout.flush()
        while True:
            key = ord(getch())
            if key == 13:
                sys.stdout.write('\n')
                return pwd
                break

            if key == 8:
                if len(pwd) > 0:
                    sys.stdout.write('\b' + ' ' + '\b')
                    sys.stdout.flush()
                    pwd = pwd[:-1]
            else:
                char = chr(key)
                sys.stdout.write('*')
                sys.stdout.flush()
                pwd = pwd + char



#Called when a new user wants to register
#Checks inside the database to see if the username entered is already in the database
#If the username is already in the database the user must use another name to register
#Returns true if username is taken and false if it's available
def check(file, string):
    #Opens file and checks every line for user name
    with open(file, 'r') as read:
        for line in read:
            if string in line:
                return True
    return False





def grabpass():
    global ptc
    writef = open("accdatabase", "r")
    cl = lf + 1
    ltr = [cl]
    for position, line in enumerate(writef):
        if position in ltr:
            ptc = line




def checklogin(file, string):
    global lf
    with open(file, 'r') as read:
        for (lf, line) in enumerate(read):
            if string in line:
                return True
    return False










#Used to clear the cmd screen
def clear():
    os.system("cls")


def mainMenu():
    os.system("title Xecure Password Manager")
    while True:
        try:
                print("--------------Main Menu------------------")
                #Presents user's with all options available
                print("\nPlease select between the following options.\n")
                print("[1] Login")
                print("[2] Register")
                print("[3] Exit\n")
                menuSelection = int(input("Selection: "))

                if menuSelection == 1:
                    login()
                    #break#jumps to return/exit might not need this!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

                if menuSelection == 2:
                    clear()
                    register()
                    #clear()
                    #break#jumps to return/exit might not need this!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

                if menuSelection ==  3:
                    clear()
                    myExit()

                if menuSelection > 3 or menuSelection < 1:
                    print("\nPlease enter a number between 1 and 3.")
                    print("\nPress any key to try again...")
                    getch()
                    clear()


        except Exception:
            print("\nInvalid Input.")
            print("Press any key to try again...")
            getch()
            clear()
    #End of function
   # return menuSelection









def login():
    while True:
        try:
            clear()
            print("--------------Login Screen------------------")
            #If the database is empty, no user can log into the application, so an error is displayed to let users know
            if os.path.getsize("accdatabase") == 0:#If accdatabase file is empty, clear screen and print message
                clear()
                print("Database is empty!\n")
                print("Press any key to go back to the login screen...")
                getch()
                clear()
                #The application will loop back to the log in menu after the error message is displayed


            #If the database is not empty the program will allow the user to enter their login information
            else:

                #The errorCount variable will keep count of how many failed login attempts have occurred
                #After 5 failed login attempts the program will close (The idea is to disable that account later on or
                # reset the user's password)
                errorCount = 5
                while True:

                    #username var will contain the user's entered password
                    username = input("\nPlease enter your username: ")


                    #A hash object is created and the username is encoded using utf8
                    #A salt of (*!@#s', 823) is stored as byte and it is used to salt the hash
                    h = hashlib.pbkdf2_hmac('sha256', username.encode("utf-8"), b'(*!@#s', 823)#todo random salt test

                    #userInput is used to convert the hash object as a hex-text, this is how it is saved in the database
                    #It is needed in the login function to compare what the user entered with what is stored in the db
                    #If there is an entry in the db that matches the userInput, then the user is allowed to continue
                    userInput = h.hex()
                    if checklogin('accdatabase', userInput):
                        clear()
                        print("--------------Login Screen------------------")
                        print("\nWelcome " + username + "!")
                        break #If checklogin is true then the user will be asked to enter his/her password

                    #If the user input does not match anything in the database then an error will be displayed and the
                    #errorCount var will count the number of failed login attemptempts
                    else:

                        #Used to count failed login attempts
                        errorCount -= 1

                        if username == "":
                            print("\nA username must be entered.")
                        else:
                            print("\nInvalid username.")

                        #After 4 failed login attempts the user will be warned that the program will close after another
                        if errorCount == 1:
                            print("\nThe application will close after another failed login attempt")
                        if errorCount == 0:
                            exit(0)

                #The user will be asked to enter their password and their input will be verified with the db
                while True:

                    #mpass function is called and it saves the password inside the userPassword variable
                    userPassword = mpass()

                    #A hash object h is created and it is used to encoded, and hash the password to be validated
                    h = hashlib.pbkdf2_hmac('sha256', userPassword.encode("utf-8"), b'*@#d2', 182)#todo random salt test

                    #The hash object h with the password is converted into hex. This is how the database stores the
                    #passwords and this is how it will be compared to see if the password the user entered matches a
                    #password in the database.
                    passInput = h.hex()



                    #Need more information on this function
                    grabpass()
                    ptct = ptc.replace("Password: ", '')
                    ptcr = ptct.rstrip("\n")
                    if passInput == ptcr:
                        currentuser = username
                        clear()
                        print("Successfully logged in as " + currentuser + "!\n")
                        usrtitle = ("title Xecure Password Manager (logged in as " + currentuser + ")")
                        os.system(usrtitle)
                        break



                    #If password is incorrect an error will be displayed and after 5 failed login attempts the program
                    #Will close (later it will lock/reset the account/password)
                    else:

                        errorCount -= 1
                        if userPassword == "":
                            print("\nA password is required.")
                        else:
                            print("\nInvalid Password.")

                        if errorCount == 1:
                            print("The application will close after another failed login attempt")
                        if errorCount == 0:
                            exit(0)

                #This code will run if the user is authenticated (THIS MIGHT BE THE END OF THIS FUNCTION & ANOTHER ONE
                #MIGHT BE TAKING OVER)
                clear()
                print("--------------Logged In-----------------")
                print("Thank you for loging in " + username)
                #FUNCTION EITHER ENDS HERE OR ANOTHER IS CALLED TO CONTINUE THE PROGRAM
                print("Press any key to go to the Dashboard...")
                getch()
                clear()
                dashBoard()
                break
        except Exception:
            print("\nInvalid Input.")
            print("Press any key to try again...")
            getch()
            clear()











def register():
     while True:
         try:#If the user enters 2 in the login menu they are able to create an account to use the application

                while True:
                    print("--------------Register Screen------------------")
                    username = ""
                    while username.isspace() or len(username) < 5 or username.isnumeric():

                        #The user is asked to enter his Master Username
                        username = input("\nPlease enter a username for your account: ")#todo implement username validation function or find a way to remove prevent spaces from being entered
                                                                    #todo fond how to make the username not take in a password that is all numbers and spaces
                                                                    #todo better user input validation can be implemented
                        if username.isspace() or username == "":
                            print("\nUsername cannot be empty.")
                        elif len(username) < 5:
                            print("\nUsername must be at least 8 characters long.")
                        elif username.isnumeric():
                            print("\nUsername cannot be composed of only numbers.")
                        else:
                            print("\nYour username will be " + username + ".")

                    #The entered username is encoded, salted and hashed inside the h hash object
                    h = hashlib.pbkdf2_hmac('sha256', username.encode("utf-8"), b'(*!@#s', 823)#todo random salt test needed

                    #A newUser variable holds the hex value of the hashed username
                    newUser = h.hex()


                    #The function check is called in order to see if the entered username is already a registered user.
                    #This function will check if the input entered matches a value in the database
                    #If it check() returns true it means that username is already taken. An error message will be displayed
                    if check('accdatabase', newUser):
                        print("\nUser already exists! Please choose another username.")
                        print("\nPress any key to try again...")
                        getch()
                        clear()
                        #If the user already exists the user will be forced to enter a new name
                        #todo need to implement a way to exit this if the user wants to back out################################################
                    else:
                        break
                        #If the username is not already taken the program will continue and the user can enter their psswd

                #The mpass() is called and it will ask the user for the password
                b = mpass()              #todo need to implement a way to exit this if the user wants to back out################################################

                # The entered password is encoded, salted and hashed inside the h hash object
                h = hashlib.pbkdf2_hmac('sha256', b.encode("utf-8"), b'*@#d2', 182)#todo random salt test need to be done

                # A newpass variable holds the hex value of the hashed password
                newPass = h.hex()

                #Opens the database.txt in append mode to add the new user account
                users = open("accdatabase", "a")

                #Writes to the text database.txt the new user information in the specified format
                users.write("Username: " + newUser + "\nPassword: " + newPass + "\n\n")

                #Closes the file
                users.close()
                clear()
                print("Thank you for registering " + username + "!\n")
                print("Press any key to go back to login menu...")
                getch()
                clear()
                break

         except Exception:
             print("\nInvalid Input.")
             print("Press any key to try again...")
             getch()
             clear()





def myExit():
    while True:
        try:

            print("\nAre you sure you want to exit?\n")
            print("[1] Yes")
            print("[2] No\n")
            end = int(input("Selection: "))


            if end == 1:
                print("\nThank you for using Xecure Password Manager. \nPress any key to exit the application...")
                getch()
                exit(0)
            elif end == 2:
                clear()
                break
            else:
                print("\nPlease enter a number between 1 and 2.")
                print("\nPress any key to try again...")
                getch()
                clear()

        except Exception:
            print("\nInvalid Input.")
            print("Press any key to try again...")
            getch()
            clear()





def dashBoard():
    while True:
        try:
            print("--------------Dash Board------------------")
            # Presents user's with all options available
            print("\nPlease select between the following options.\n")
            print("[1] Retrieve a Record")
            print("[2] Add a New Record")
            print("[3] View All Records")
            print("[4] User Settings")
            print("[5] Logout")
            print("[6] Exit\n")
            menuSelection = int(input("Selection: "))

            if menuSelection == 1:
                getRecord()


                #break  # jumps to return/exit might not need this!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

            if menuSelection == 2:
                print("\nThis will call function that lets users add a record")
                # break#jumps to return/exit might not need this!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
                print("Press any key to continue...")
                getch()
                clear()

            if menuSelection == 3:
                print("\nThis will call function lets user see all records")
                print("Press any key to continue...")
                getch()
                clear()

            if menuSelection == 4:
                clear()
                settings()
                clear()

            if menuSelection == 5:

                print("\nAre you sure you want to logout?\n")
                print("[1] Yes")
                print("[2] No\n")
                end = int(input("Selection: "))

                if end == 1:
                    clear()
                    print("\nThank you for using Xecure Password Manager. \nPress any key to logout...")
                    getch()
                    usrtitle = ("title Xecure Password Manager")
                    os.system(usrtitle)
                    clear()
                    break

                elif end == 2:
                    clear()

                else:
                    print("\nPlease enter a number between 1 and 2.")
                    print("\nPress any key to try again...")
                    getch()
                    clear()

            if menuSelection == 6:
                clear()
                myExit()


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
    # End of function




def settings():
    while True:
        try:
            print("--------------Settings------------------")
            # Presents user's with all options available
            print("\nWhat would you like to do?.\n")
            print("[1] Delete a Record")
            print("[2] Delete All Records")
            print("[3] Reset Account Password")
            print("[4] Change Security Questions (FEATURE IS TENTATIVE)")
            print("[5] Back to Dashboard\n")
            menuSelection = int(input("Selection: "))

            if menuSelection == 1:
                print("\nThis will call function that delete records")
                print("Press any key to continue...")
                getch()
                clear()

                #break  # jumps to return/exit might not need this!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

            if menuSelection == 2:
                print("\nThis will call function that deletes all records")
                # break#jumps to return/exit might not need this!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
                print("Press any key to continue...")
                getch()
                clear()

            if menuSelection == 3:
                print("\nThis will call function lets user reset their master account password")
                print("Press any key to continue...")
                getch()
                clear()

            if menuSelection == 4:
                print("\nThis will call function lets user change Security Questions (FEATURE TENTATIVE)")
                print("Press any key to continue...")
                getch()
                clear()

            if menuSelection == 5:
                clear()
                break

            if menuSelection > 5 or menuSelection < 1:
                print("\nPlease enter a number between 1 and 5.")
                print("\nPress any key to try again...")
                getch()
                clear()
        except Exception:
            print("\nInvalid Input.")
            print("Press any key to try again...")
            getch()
            clear()
    # End of function



def getRecord():
    clear()
    while True:
        try:
            print("--------------Retrieve Record------------------")
            print("\nEnter the name of the service/platform of the record you wish to retrieve: ")
            recordName = input("\nPlatform/Service Name: ")
            if recordName.isspace() or recordName == "":
                print("\nService/Platform name cannot be empty.")
                print("Press any key to try again...")
                getch()
                clear()
            elif recordName.isnumeric():
                print("\nService/Platform cannot be composed of only numbers.")
                print("Press any key to try again...")
                getch()
                clear()
            else:
                print("Program will search for record.\n")

                if recordName == "Facebook": #todo this is temporary code and it should be replaced with function to detect record
                    print(recordName + " Record found.\n")
                    print(recordName + " User Account/Email: " + "THE USERS RECORD WILL BE RETRIEVED AND DISPLAYED HERE")
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


def addRecord():
    clear()
    while True:
        try:
            print("--------------Add Record------------------")
            print("\nEnter the name of the service/platform of the record you wish to create: ")
            recordName = input("\nPlatform/Service Name: ")
            if recordName.isspace() or recordName == "":
                print("\nService/Platform name cannot be empty.")
                print("Press any key to try again...")
                getch()
                clear()
            # todo implement function to detect if this user already has an account with this name.

            elif recordName.isnumeric():
                print("\nService/Platform cannot be composed of only numbers.")
                print("Press any key to try again...")
                getch()
                clear()
            else:


                print("\nEnter the username/email for your " + recordName + "account.")
                recordUser = input("\nAcount username/email: \n")

                while True:
                    print("Would you like to generate a random password for your account?")
                    print("[1] Yes")
                    print("[2] No")
                    menuSelection = int(input("Selection: "))

                    if menuSelection == 1:
                        print("A function to genearate a random password will be called here.")
                        break
                    if menuSelection == 2:
                        print("You may enter your own password.")
                        break

                while True:
                    print("Enter the name for your " + recordName + " account.")
                    recordpassword = input("\nAcount password (has to be fixed to only display ****): \n")

                    if recordpassword.isspace() or recordpassword == "":
                        print("\nService/Platform name cannot be empty.")
                        print("Press any key to try again...")
                        getch()
                        clear()
                    # todo implement function to detect if this user already has an account with this name.

                    elif recordpassword.isnumeric():
                        print("\nService/Platform cannot be composed of only numbers.")
                        print("Press any key to try again...")
                        getch()
                        clear()
                    else:
                        print("Record created!")
                        print("Press any key to go back to Dashboard...")
                        getch()
                        clear()


        except Exception:
            print("\nInvalid Input.")
            print("Press any key to try again...")
            getch()
            clear()





#print(mainMenu())
#print("Press any key to try again...")
#getch()

mainMenu()
#login()
#myExit()
#dashBoard()
#settings()
#getRecord()
