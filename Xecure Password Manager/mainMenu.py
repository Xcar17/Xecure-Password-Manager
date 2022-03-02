#Xecure Password Manager
#By Carlos Ocasio
#Password Manager lets users create an account and allows them to safely store all of their login credentials for
#various sites. Login credentials can only be accessed by the root user. Application uses SHA256 to hash login
#credentials and encrypts the records of the user inside a secure MySQL database.

#This module contai1ns the Login/Register menu that gives users access to the application and records.

import os
import sys
import getpass
import hashlib
from msvcrt import getch
from clear import myExit, clear
from dashboard import dashBoard
from dbsetup import add_log
from dbsetup import encryptAll, add_log3, adding_new_enc_sec_answers, checkDuplicateEmail
from passwordRecovery import usernameRecovery, idRecovery, forgot_update_password, retrieveIDByName, retrieveIDByEmail
from hashing import combHash
from input_val import validatePassword

#Function replaces input text as * in the cmd as the user enters their password. This is used so that the password is
#not displayed to the screen for others to see.
def hidePassword(prompt='\nPlease enter your password: '): #todo Pwd needs validation
    if sys.stdin is not sys.__stdin__:
        usrPsswd = getpass.getpass(prompt)
        return usrPsswd
    else:
        usrPsswd = ""
        sys.stdout.write(prompt)
        sys.stdout.flush()
        while True:
            myKey = ord(getch())
            if myKey == 13:
                sys.stdout.write('\n')
                return usrPsswd

            if myKey == 8:
                if len(usrPsswd) > 0:
                    sys.stdout.write('\b' + ' ' + '\b')
                    sys.stdout.flush()
                    usrPsswd = usrPsswd[:-1]
            else:
                char = chr(myKey)
                sys.stdout.write('*')
                sys.stdout.flush()
                usrPsswd = usrPsswd + char


#Called when a new user wants to register. Checks inside the db to see if the username entered is already in the db
#If the username is already in the db the user must use another name to register
#Returns true if username is taken and false if it's available
def checkStringDatabase(file, string):
    with open(file, 'r') as read:     #Opens file and checks every line for user name
        for line in read:
            if string in line:
                return True
    return False

#Opens file that contains Master Account info in order to compare login info (Login procedure)
def getPsswd():
    global pwdToCheck
    writeFile = open("accdatabase", "r")
    rL = lookingFor + 1
    ltr = [rL]
    for position, line in enumerate(writeFile):
        if position in ltr:
            pwdToCheck = line

#Function checks inside of database for a particular username/password
def checkLogin(file, string):
    global lookingFor
    with open(file, 'r') as read:
        for (lookingFor, line) in enumerate(read):
            if string in line:
                return True
    return False




#First screen the user will be greeted with. Contains the login, register, and exit controls.
def mainMenu():
    os.system("title Xecure Password Manager")#Changes title of screen
    while True:
        try:
                clear()
                print("--------------Main Menu------------------")
                print("\nPlease select between the following options:\n")#Presents user's with all options available
                print("[1] Login")
                print("[2] Register")
                print("[3] Forgot Login")
                print("[4] Exit\n")
                menuSelection = int(input("Selection: "))

                if menuSelection == 1:
                    login()
                if menuSelection == 2:
                    register()
                if menuSelection == 3:
                    forgotLogin()
                if menuSelection == 4:
                    myExit()
                if menuSelection > 4 or menuSelection < 1: #numbers higher or lower than valid cases
                    print("\nPlease enter a number between 1 and 4.")
                    print("Press any key to try again...")
                    getch()
                    clear()

        except Exception:
            print("\nInvalid Input.")
            print("Press any key to try again...")
            getch()
            clear()





#Function for logging in to the appliaction. Asks for
def login():
    while True:
        try:
            clear()
            print("--------------Login Screen------------------\n[Enter '0' if you wish to go back to the previous screen]")
            #If the database is empty, no user can log into the application, so an error is displayed to let users know
            if os.path.getsize("accdatabase") == 0:#If accdatabase file is empty, clear screen and print message
                clear()
                print("Database is empty!\n")
                print("Press any key to go back to the login screen...")
                getch()
                clear()
                break
                #The application will loop back to the log in menu after the error message is displayed


            #If the database is not empty the program will allow the user to enter their login information
            else:

                #The errorCount variable will keep count of how many failed login attempts have occurred
                #After 5 failed login attempts the program will close (The idea is to disable that account later on or
                # reset the user's password)
                errorCount = 5 #todo implement lockout account feature (Do i want to lockout after username or psswd)
                while True:

                    #username var will contain the user's entered password
                    username = input("\nPlease enter your username: ")

                    if username == '0':
                        return '0'

                    #A hash object is created and the username is encoded using utf8
                    #A salt of (*!@#s', 823) is stored as byte and it is used to salt the hash
                    h = hashlib.pbkdf2_hmac('sha256', username.encode("utf-8"), b'(*!@#s', 823)#todo random salt test

                    #userInput is used to convert the hash object as a hex-text, this is how it is saved in the database
                    #It is needed in the login function to compare what the user entered with what is stored in the db
                    #If there is an entry in the db that matches the userInput, then the user is allowed to continue
                    userInput = h.hex()



                    #mpass function is called and it saves the password inside the userPassword variable
                    userPassword = hidePassword()

                    if userPassword == '0':
                        return '0'

                    #A hash object h is created and it is used to encoded, and hash the password to be validated
                    h = hashlib.pbkdf2_hmac('sha256', userPassword.encode("utf-8"), b'*@#d2', 182)#todo random salt test

                    #The hash object h with the password is converted into hex. This is how the database stores the
                    #passwords and this is how it will be compared to see if the password the user entered matches a
                    #password in the database.
                    passInput = h.hex()



                    if checkLogin('accdatabase', userInput):
                        getPsswd()  # Opens file to read entries and compare passwords later on
                        myPtct = pwdToCheck.replace("Password: ", '')
                        myCmpr = myPtct.rstrip("\n")
                        if passInput == myCmpr:
                            currentUser = username
                            usrId = combHash(username, userPassword)
                            # lastCMPR = retrieveIDByName(username)
                            clear()
                            usrLoggedIn = ("title Xecure Password Manager (logged in as " + currentUser + ")")
                            os.system(usrLoggedIn)
                            break

                        else:
                            print("\nInvalid Login")
                            print("Press any key to try again...")
                            getch()
                            clear()
                            print("--------------Login Screen------------------\n[Enter '0' if you wish to go back to the previous screen]")




                    #If the user input does not match anything in the database then an error will be displayed and the
                    #errorCount var will count the number of failed login attemptempts
                    else:
                        #Used to count failed login attempts
                        errorCount -= 1

                        if username == "":
                            print("\nA username and password must be entered.\nPress any key to try again...")
                            getch()
                            clear()
                            print("--------------Login Screen------------------\n[Enter '0' if you wish to go back to the previous screen]")
                        else:
                            print("\nInvalid Login")
                            print("Press any key to try again...")
                            getch()
                            clear()
                            print("--------------Login Screen------------------\n[Enter '0' if you wish to go back to the previous screen]")

                        #After 4 failed login attempts the user will be warned that the program will close after another
                        if errorCount == 1:
                            print("\nThe application will close after another failed login attempt")
                        if errorCount == 0:
                            exit(0)






                #This code will run if the user is fully authenticated
                clear()
                print("--------------Logged In-----------------")
                print("\nThank you for logging in " + username + "\nPress any key to go to the Dashboard...")
                getch()
                dashBoard(currentUser)
                break

        except Exception:
            print("\nInvalid Input")
            print("Press any key to try again...")
            getch()
            clear()







#Prompts the user to type in their email. Email will be used to reset account when needed (Future Implementation)
#Returns the user's email
def getEmail(): #todo Needs validation to make sure no repeat emails accepted
    while True:
        try:
            clear()
            print("--------------Register------------------\n[Enter '0' if you wish to go back to the previous screen]")
            #todo implement input validation
            useremail = input("\nPlease enter the email for your account: ")

            if useremail == '0':
                return '0'

            while checkDuplicateEmail(useremail):
                useremail = input("\nEmail Taken. Please enter another email for your account: ")


            if useremail.isspace() or useremail == "":
                print("\nEmail cannot be empty\nPress any key to try again...")
                getch()
                clear()
                continue

            elif len(useremail) < 5:
                print("\nEmail cannot be less than 5 characters\nPress any key to try again...")
                getch()
                clear()
                continue

            elif useremail.isnumeric():
                print("\nEmail cannot be composed of only numbers.\nPress any key to try again...")
                getch()
                clear()
                continue
            else:
                break

        except Exception:
            print("\nInvalid Input")
            print("Press any key to try again...")
            getch()
            clear()
    return useremail





#Functions allows new users to create a new account
def register():
     clear()
     escape = 1 #flag used to make sure email is not called again after it has been approved.
     while True:
         try:
                while True:
                    if escape == 1:#Makes sure email only gets called once
                        usrEmail = getEmail()

                        if usrEmail == '0':
                            return '0'

                        escape += 1
                        hashEmail = hashlib.pbkdf2_hmac('sha256', usrEmail.encode("utf-8"), b'&%$#f^',
                                                        182)  # todo implement random salt test
                        newEmail = hashEmail.hex()

                    username = ""
                    while True:
                        clear()
                        print("--------------Register------------------\n[Enter '0' if you wish to go back to the previous screen]")
                        #The user is asked to enter his Master Username
                        username = input("\nPlease enter a username for your account: ")

                        if username == '0':
                            return '0'

                        if username.isspace() or username == "":
                            print("\nUsername cannot be empty.\nPress any key to try again...")
                            getch()

                        elif len(username) < 3:
                            print("\nUsername must be at least 3 characters long.\nPress any key to try again...")
                            getch()

                        elif username.isnumeric():
                            print("\nUsername cannot be composed of only numbers.\nPress any key to try again...")
                            getch()

                        else:
                            break


                    #The entered username is encoded, salted and hashed inside the h hash object
                    h = hashlib.pbkdf2_hmac('sha256', username.encode("utf-8"), b'(*!@#s', 823)#todo random salt test needed

                    #A newUser variable holds the hex value of the hashed username
                    newUser = h.hex()


                    #The function check is called in order to see if the entered username is already a registered user.
                    #This function will check if the input entered matches a value in the database
                    #If it check() returns true it means that username is already taken. An error message will be displayed
                    if checkStringDatabase('accdatabase', newUser):
                        print("\nUser already exists! Please choose another username.")
                        print("Press any key to try again...")
                        getch()
                        clear()
                        #If the user already exists the user will be forced to enter a new name
                        #todo need to implement a way to exit this if the user wants to back out
                    else:
                        break
                        #If the username is not already taken the program will continue and the user can enter their psswd

                #The mpass() is called and it will ask the user for the password
                while True:
                        clear()
                        print("--------------Register------------------\n[Enter '0' if you wish to go back to the previous screen]")
                        secretPass = hidePassword()              #todo needs input verification and password protocols

                        if secretPass == '0':
                            return '0'

                        if secretPass == "":
                            print("\nPassword cannot be empty\nPress any key to try again...")
                            getch()
                            continue


                        validatePass = validatePassword(secretPass)

                        if validatePass == 1:
                            print("\nPassword must be at least 8 characters long\nPress any key to try again...")
                            getch()
                            continue

                        elif validatePass == 2:
                            print("\nPassword must be less than 20 characters long\nPress any key to try again...")
                            getch()
                            continue

                        elif validatePass == 3:
                            print("\nYour password must contain at least one of the following symbols: ~!@#$%^&*_-+='|\(){}[]:;\"\'<>,.?/"
                                  "\nYour password must also contain at least one number, one uppercaser letter, and one lowercase letter"
                                  "\nPress any key to try again...")
                            getch()
                            continue


                        else:
                          break



                # The entered password is encoded, salted and hashed inside the h hash object
                h = hashlib.pbkdf2_hmac('sha256', secretPass.encode("utf-8"), b'*@#d2', 182)#todo implement random salt test

                # A newpass variable holds the hex value of the hashed password
                newPass = h.hex()

                #Opens the database.txt in append mode to add the new user account
                users = open("accdatabase", "a")

                # Writes to the text database.txt the new user information in the specified format
                users.write("Email: " + newEmail + "\nUsername: " + newUser + "\nPassword: " + newPass + "\n\n")

                #Closes the file
                users.close()
                clear()


                #  get  next user id
                usrID = combHash(username, secretPass)

                topUser = username
                # use newID to encrypt username and usrEmail
                username, usrEmail = encryptAll(usrID, [username, usrEmail])


                add_log(usrID, username, usrEmail)#todo make sure username and usrEmail are sanitized

                #User is registered and confirmation message printed to screen
                print("--------------Register------------------")
                print("\nThank you for registering")
                print("Press any key to go back to the main menu...")
                getch()
                clear()
                break

         except Exception:
             exc_type, exc_obj, exc_tb = sys.exc_info()
             fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
             print(exc_type, fname, exc_tb.tb_lineno)
             print("\nInvalid Input")
             print("Press any key to try again...")
             getch()
             clear()


def forgotLogin():
    while True:
        try:
            clear()
            print("--------------Login Help------------------")
            print("\nPlease select between the following options:\n")  # Presents user's with all options available
            print("[1] Forgot Username")
            print("[2] Forgot Password")
            print("[0] Back to login screen\n")
            menuSelection = int(input("Selection: "))

            if menuSelection == 1:
                usernameRecovery()
            if menuSelection == 2:
                forgot_update_password()
            if menuSelection == 0:
                break
            if menuSelection > 2 or menuSelection < 0:  # numbers higher or lower than valid cases
                print("\nPlease enter a number between 0 and 2.")
                print("Press any key to try again...")
                getch()
                clear()

        except Exception:
            print("\nInvalid Input.")
            print("Press any key to try again...")
            getch()
            clear()