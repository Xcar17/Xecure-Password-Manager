#Xecure Password Manager
#By Carlos Ocasio

#This module contains the Login/Register menu that allows users to create an account in order to use the program.


import os #Used to change the title of the command line screen.
import hashlib #Used for hashing.
from msvcrt import getch #Prevents the command screen from continuing to the next screen until a key is pressed.
from clear import myExit, clear #Used to clear and properly exit the application.
from dashboard import dashBoard #Used to call the dashboard function which contains the user features.
from dbsetup import encryptAll, checkDuplicateEmail, add_log #Used to query the database.
from passwordRecovery import usernameRecovery, forgot_update_password #Used to assist users in recovering account.
from hashing import combHash #Used to call hashing algorithm.
from input_val import validatePassword, validateRecordPass, validateEmail, validateUsername #Used for input validation.
from hidePassword import hidePassword #Used to hide password from the screen.
from logo import shield #Used to display logo.


#Called when a new user wants to register. Checks inside the db to see if the username entered is already in the db
#If the username is already in the db the user must use another name to register
#Returns true if username is taken and false if it's available
def checkStringDatabase(file, string):
    with open(file, 'r') as read:     #Opens file and checks every line for user name
        for line in read:
            if string in line:
                return True
    return False

#Opens file that contains Master Account info in order to compare login info (Login procedure).
def getPsswd():
    global pwdToCheck
    writeFile = open("accdatabase", "r")
    rL = lookingFor + 1
    ltr = [rL]
    for position, line in enumerate(writeFile):
        if position in ltr:
            pwdToCheck = line

#Function checks inside of database for a particular username/password. Used to authenticate users.
def checkLogin(file, string):
    global lookingFor
    with open(file, 'r') as read:
        for (lookingFor, line) in enumerate(read):
            if string in line:
                return True
    return False

#First screen the user will be greeted with. Contains the login, register, and exit controls.
def mainMenu():
    os.system("title Xecure Password Manager")#Changes title of screen.
    shield()
    print("                                         Press any key to continue...")
    getch()

    while True:
        try:
                clear()
                print("--------------Main Menu------------------")
                print("\nPlease select between the following options:\n")
                print("[1] Login")
                print("[2] Register")
                print("[3] Forgot Login")
                print("[4] Exit\n")
                menuSelection = int(input("Selection: "))

                if menuSelection == 1: #Calls the login function.
                    login()
                if menuSelection == 2: #Calls the register function.
                    register()
                if menuSelection == 3: #Calls the forgot login function.
                    forgotLogin()
                if menuSelection == 4: #Calls the exit function.
                    myExit()
                if menuSelection > 4 or menuSelection < 1: #Invalid numeric input.
                    print("\nPlease enter a number between 1 and 4.")
                    print("Press any key to try again...")
                    getch()
                    clear()

        except Exception: #Catching other invalid input.
            print("\nInvalid Input. Please enter a number between 1 and 4.")
            print("Press any key to try again...")
            getch()
            clear()

#Function for logging in to the appliaction. Asks for user credentials, verifies credentials and allows users into the
#application. If the user fails to login 6 times the application will close.
def login():
    while True:
        try:
            clear()
            print("--------------Login Screen------------------\n[Enter '0' if you wish to go back to the previous "
                  "screen]")

            #If the database is empty, no user can log into the application, so an error is displayed to let users know.
            if os.path.getsize("accdatabase") == 0:#If accdatabase file is empty, clear screen and print message.
                clear()
                print("--------------Login Screen------------------\n")
                print("Database is empty! Please register to use the application.\n")
                print("Press any key to go back to the login screen...")
                getch()
                clear()
                break
                #The application will loop back to the log in menu after the error message is displayed


            #If the database is not empty the program will allow the user to enter their login information
            else:

                #The errorCount variable will keep count of how many failed login attempts have occurred
                #After 6 failed login attempts the program will close (The idea is to disable that account later on or
                # reset the user's password)
                errorCount = 6 #todo implement lockout account feature
                while True:
                    clear()
                    print("--------------Login Screen------------------\n[Enter '0' if you wish to go back to the"
                          " previous screen]\n\nPlease enter the following:")

                    #Gives a warning to the user if they have only one attempt left.
                    if errorCount == 1:
                        print("\nThe application will close after another failed login attempt.")

                    username = input("\nAccount Username: ")

                    if username == '0': #Command to go back to previous screen.
                        return '0'

                    if username.isspace() or username == "": #If input is empty.
                        errorCount -= 1
                        print("\nUser name cannot be empty.")
                        if errorCount == 0:
                            print("The application will now close...")
                            getch()
                            exit(0)

                        print("Press any key to try again...")
                        getch()
                        clear()
                        continue

                    username = validateRecordPass(username) #Validates input by type

                    if username == 2: #If input is bigger than 35 characters.
                        errorCount -= 1
                        if errorCount == 0:
                            print("\nUsername must be less than 35 characters long.")
                            print("\nThe application will now close...")
                            getch()
                            exit(0)

                        print("\nUsername must be less than 35 characters long.\nPress any key to try again...")
                        getch()
                        continue

                    #A hash object is created and the username is encoded using utf8.
                    #A salt of (*!@#s', 823) is stored as byte and it is used to salt the hash.
                    h = hashlib.pbkdf2_hmac('sha256', username.encode("utf-8"), b'(*!@#s', 823)

                    #UserInput is used to convert the hash object as a hex-text, this is how it is saved in the database
                    #It is needed in the login function to compare what the user entered with what is stored in the db
                    #If there is an entry in the db that matches the userInput, then the user is allowed to continue
                    userInput = h.hex()

                    #Hidepassword function is called and it saves the password inside the userPassword variable.
                    userPassword = hidePassword()

                    if userPassword == '0': #Command to go back to previous screen.
                        return '0'


                    if userPassword.isspace() or userPassword == "": #If input is empty.
                        errorCount -= 1
                        print("\nPassword cannot be empty.")
                        if errorCount == 0:
                            print("The application will now close...")
                            getch()
                            exit(0)

                        print("Press any key to try again...")
                        getch()
                        clear()
                        continue

                    userPassword = validateRecordPass(userPassword) #Validating input by type.

                    if userPassword == 2: #If input is longer than 35 characters.
                        errorCount -= 1

                        if errorCount == 0:
                            print("\nPassword must be less than 35 characters long.")
                            print("The application will now close...")
                            getch()
                            exit(0)

                        print("\nPassword must be less than 35 characters long.\nPress any key to try again...")
                        getch()
                        continue


                    #A hash object h is created and it is used to encoded, and hash the password to be validated
                    h = hashlib.pbkdf2_hmac('sha256', userPassword.encode("utf-8"), b'*@#d2', 182)

                    #The hash object h with the password is converted into hex. This is how the database stores the
                    #passwords and this is how it will be compared to see if the password the user entered matches a
                    #password in the database.
                    passInput = h.hex()


                    #Checking login credentials.
                    if checkLogin('accdatabase', userInput):
                        getPsswd()  # Opens file to read entries and compare passwords later on
                        myPtct = pwdToCheck.replace("Password: ", '')
                        myCmpr = myPtct.rstrip("\n")
                        if passInput == myCmpr:
                            currentUser = username
                            usrId = combHash(username, userPassword) #UserId is passed on to other functions.
                            clear()
                            usrLoggedIn = ("title Xecure Password Manager (logged in as " + currentUser + ")")
                            os.system(usrLoggedIn)
                            break

                        else: #If invalid login attempt.
                            errorCount -= 1
                            print("\nInvalid Login.")
                            if errorCount == 0:
                                print("The application will now close...")
                                getch()
                                exit(0)
                            print("Press any key to try again...")
                            getch()
                            clear()
                            continue

                    #If the user input does not match anything in the database then an error will be displayed and the
                    #errorCount var will count the number of failed login attemptempts.
                    else:
                        #Used to count failed login attempts
                        errorCount -= 1
                        print("\nInvalid Login.")
                        if errorCount == 0:
                            print("The application will now close...")
                            getch()
                            exit(0)
                        print("Press any key to try again...")
                        getch()
                        clear()


                #This code will run if the user is fully authenticated
                clear()
                print("--------------Logged In-----------------")
                print("\nThank you for logging in " + username + ".\nPress any key to go to the Dashboard...")
                getch()
                dashBoard(currentUser)
                break

        except Exception:
            print("\nInvalid Input.")
            print("Press any key to try again...")
            getch()
            clear()


#Prompts the user to type in their email. Email will be used to reset account when needed. Returns the user's email
# after verification.
def getEmail():
    while True:
        try:
            clear()
            print("--------------Register------------------\n[Enter '0' if you wish to go back to the previous screen]")
            useremail = input("\nPlease enter the email for your account: ")

            if useremail == '0': #Command to go back to previous screen.
                return '0'

            if useremail.isnumeric(): #If input is numeric only.
                print("\nEmail cannot be composed of only numbers.\nPress any key to try again...")
                getch()
                clear()
                continue

            if useremail.isspace() or useremail == "": #If input is empty.
                print("\nEmail cannot be empty.\nPress any key to try again...")
                getch()
                clear()
                continue

            useremail = useremail.lower() #Converts the email to lowercase.

            while checkDuplicateEmail(useremail): #Checks input for duplicate (Email must be unique).
                useremail = input("\nEmail Taken. Please enter another email for your account: ")
                if useremail == '0':
                    return '0'
                useremail = useremail.lower()


            useremail = validateEmail(useremail) #Validates input by type.

            if useremail == 1: #If input is less than 6 characters.
                print("\nEmail must be at least 6 characters long.\nPress any key to try again...")
                getch()
                continue

            if useremail == 2: #If input is more than 35 characters.
                print("\nEmail must be less than 35 characters long.\nPress any key to try again...")
                getch()
                continue

            if useremail == 3: #If input format is incorrect.
                print("\nEmail must contain letters, the '@' symbol, and a period (.)."
                      "\nPress any key to try again...")
                getch()
                continue


            else:
                break

        except Exception: #Catching other invalid input.
            print("\nInvalid Input.")
            print("Press any key to try again...")
            getch()
            clear()
    return useremail




#Functions allows users to create a new account.
def register():
     clear()
     escape = 1 #flag used to make sure email is not called again after it has been approved.
     while True:
         try:
                while True:
                    if escape == 1:#Makes sure email only gets called once.
                        usrEmail = getEmail()


                        if usrEmail == '0': #Command to go back to previous screen.
                            return '0'

                        usrEmail = usrEmail.lower() #Converting email to lower case.

                        escape += 1 #Flag used to escape.
                        #Creating a hash of the email.
                        hashEmail = hashlib.pbkdf2_hmac('sha256', usrEmail.encode("utf-8"), b'&%$#f^',182)
                        newEmail = hashEmail.hex() #Converting hash to hex format. This is how it is stored in DB.

                    username = ""#Creating username variable to be used later.
                    while True:
                        clear()
                        print("--------------Register------------------\n[Enter '0' if you wish to go back to the "
                              "previous screen]")
                        #The user is asked to enter his Master Username
                        username = input("\nPlease enter a username for your account: ")

                        if username == '0':#Command to go back to previous screen.
                            return '0'

                        if username.isspace() or username == "":#If input is empty.
                            print("\nUsername cannot be empty.\nPress any key to try again...")
                            getch()
                            continue

                        if username.isnumeric():#If input is numeric only.
                            print("\nUsername cannot be composed of only numbers.\nPress any key to try again...")
                            getch()
                            continue

                        username = validateUsername(username)#Validating input by type.

                        if username == 1:#If input is less than 3 characters.
                            print("\nUsername must be at least 3 characters long.\nPress any key to try again...")
                            getch()
                            continue

                        if username == 2:#If input is longer than 35 characters.
                            print("\nUsername must be less than 35 characters long.\nPress any key to try again...")
                            getch()
                            continue

                        if username == 3:#If input does not follow the correct format.
                            print("\nUsernames must be composed of only letters and numbers. No spaces or special "
                                  "characters allowed."
                                  "\nPress any key to try again...")
                            getch()
                            continue

                        else:
                            break


                    #The entered username is encoded, salted and hashed inside the h hash object
                    h = hashlib.pbkdf2_hmac('sha256', username.encode("utf-8"), b'(*!@#s', 823)

                    #A newUser variable holds the hex value of the hashed username
                    newUser = h.hex()


                    #The function check is called in order to see if the entered username is already a registered user.
                    #This function will check if the input entered matches a value in the database
                    #If it check() returns true it means that username is already taken. An error mssg will be displayed
                    if checkStringDatabase('accdatabase', newUser):
                        print("\nUser already exists! Please choose another username.")
                        print("Press any key to try again...")
                        getch()
                        clear()
                        continue


                    else:
                        break
                        #If the username is not already taken the program will continue and the user can enter  psswd

                #The hidepassword() is called and it will ask the user for the password
                while True:
                        clear()
                        print("--------------Register------------------\n[Enter '0' if you wish to go back to the "
                              "previous screen]")
                        print("\nPlease enter a password for your Xecure Password Manager Account. You will use this to"
                              " log into the application.")

                        secretPass = hidePassword() #Asks for password and hides it from the screen.

                        if secretPass == '0':#Command to go back to previous screen.
                            return '0'

                        if secretPass == "" or secretPass.isspace(): #if input is empty.
                            print("\nPassword cannot be empty.\nPress any key to try again...")
                            getch()
                            continue

                        if secretPass.isnumeric(): #If input is numeric only.
                            print("\nPassword cannot be composed of only numbers.\nPress any key to try again...")
                            getch()
                            continue

                        validatePass = validatePassword(secretPass) #Validating input by type.

                        if validatePass == 1: #If input is less than 8 characters.
                            print("\nPassword must be at least 8 characters long.\nPress any key to try again...")
                            getch()
                            continue

                        elif validatePass == 2: #If input is longer than 35 characters.
                            print("\nPassword must be less than 35 characters long.\nPress any key to try again...")
                            getch()
                            continue

                        elif validatePass == 3: #If input does not follow proper format.
                            print("\nYour password must contain at least one of the following symbols: ~!@#$%^&*_-+='|"
                            "(){}[]:;\"\'<>,.?/"
                                  "\nYour password must also contain at least one number, one uppercaser letter, and "
                                  "one lowercase letter."
                                  "\nPress any key to try again...")
                            getch()
                            continue

                        else:
                          break


                # The entered password is encoded, salted and hashed inside the h hash object.
                h = hashlib.pbkdf2_hmac('sha256', secretPass.encode("utf-8"), b'*@#d2', 182)

                # A newpass variable holds the hex value of the hashed password.
                newPass = h.hex()

                #Opens the database.txt in append mode to add the new user account.
                users = open("accdatabase", "a")

                # Writes to the text database.txt the new user information in the specified format.
                users.write( newEmail + "\n" + newUser + "\n" + newPass + "\n\n")

                #Closes the file.
                users.close()
                clear()

                #  get  next user id.
                usrID = combHash(username, secretPass)

                topUser = username
                # use newID to encrypt username and usrEmail
                username, usrEmail = encryptAll(usrID, [username, usrEmail])

                add_log(usrID, username, usrEmail) #Adds user to the database.

                #User is registered and confirmation message printed to screen
                print("--------------Register------------------")
                print("\nThank you for registering!")
                print("Press any key to go back to the main menu...")
                getch()
                clear()
                break

         except Exception: #Catching exceptions
             print("\nInvalid Input.")
             print("Press any key to try again...")
             getch()
             clear()

#Function can be used if user cannot remember their login information. It will allow the users to recover their userID
# or it will let them reset their account password.
def forgotLogin():
    while True:
        try:
            clear()
            print("--------------Login Help------------------\n")
            if os.path.getsize("accdatabase") == 0: #If accdatabase file is empty, clear screen and print message
                print("Database is empty! Please register to use this feature.\n")
                print("Press any key to go back to the login screen...")
                getch()
                clear()
                break
                #The application will loop back to the log in menu after the error message is displayed

            #If there are records present the feature will work.
            print("Please select between the following options:\n")
            print("[1] Forgot Username")
            print("[2] Forgot Password")
            print("[0] Back to login screen\n")
            menuSelection = int(input("Selection: "))

            if menuSelection == 1: #Calls function to recover username ID.
                usernameRecovery()
            if menuSelection == 2: #Calls function to reset master password.
                forgot_update_password()
            if menuSelection == 0: #Command to go back to the previous screen.
                break
            if menuSelection > 2 or menuSelection < 0:  # If input is invalid numeric only.
                print("\nPlease enter a number between 0 and 2.")
                print("Press any key to try again...")
                getch()
                clear()

        except Exception: #Catching other exceptions.
            print("\nInvalid Input. Please select a number between 0 and 2.")
            print("Press any key to try again...")
            getch()
            clear()