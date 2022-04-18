# Xecure Password Manager
# By Carlos Ocasio

#This module contains all of the functions and features that enable users to recover their accounts. Users can recover
#their username and reset their password through this module.

import socket #Used for email features and error handling.
from database import cursor #Used to connect module to the database.
from dbsetup import decrypt, update_master_email, update_user_ID, checkDuplicateEmail #Used for SQL queries.
from random_pwd_generator import generate_password #Used to generate random passwords.
import smtplib #Used to send emails.
from hashing import combHash #Used for hashing and authenticating.
import hashlib #Used to create hashing algorithm.
from msvcrt import getch #Prevents the command screen from continuing to the next screen until a key is pressed.
from clear import clear #Used to clear command screen.
from input_val import validatePassword, noleadingspace, validateEmail, validateRecordPass #Used for input validation.
from hidePassword import hidePassword #Used to hide passwords from the command screen.
import time #Used to create a timer for the password clipboard function.

#This function allows the program to send emails to the users in order to verify and authenticate the account.
def sendEmail(email, code, retreival=None):
    # creates SMTP session
    s = smtplib.SMTP('smtp.gmail.com', 587)

    # start TLS for security
    s.starttls()

    # Authentication
    s.login("xecureddb@gmail.com", "Xecured123") #User needs to change the two parameters to their email address and
                                                 #their password.

    #Explanation contains the message that will be sent to the user if someone attempts to authenticate into the app.
    explanation = "\n-------Xecure Password Manager-------\n\nSomeone has attempted to authenticate into your " \
                  "Xecure Password Manager account. " \
                  "If this was not you, it is recommended that you change your password. If this was you please" \
                  " follow the instructions below.\n\n" \
                  "\nPlease go back to the Xecure application and enter this code when prompted in order to " \
                  "set a new password:\n"

    #If someone is attempting to retrieve the username, this message will be sent as an email.
    if retreival is not None:
        explanation = f"\n-------Xecure Password Manager-------\n\nSomeone has requested your Xecure Password" \
                      f" Manager user name." \
                  "If this was not you, it is recommended that you change your password. If this was you please" \
                      " follow the instructions below.\n\n" \
                      f"\nYour {retreival} is:\n"

    #msg variable contains the explanation message along with the verification code.
    msg = explanation + code
    #Sending the mail.
    s.sendmail("sender_email_id", email, msg)

    #Terminating the session.
    s.quit()

#This function verifies that the email entered is an email that has been registered into the application. If the email
#entered has been registered it will return True, if the email entered has not been registered it will return False.
def verifyEmail(email):

    #Query to search for all the emails in the database.
    sql = ("select id, Email from Registered_Users ")
    cursor.execute(sql )
    results = cursor.fetchall()
    #Looks through the emails retireved and tried to find the email entered by the user. Returns true if they match.
    for rec in results:
        if decrypt(rec[0], rec[1]) == email:
            return True
    return False

#Function used to update the master password of a user. The password needs to be changed both in the database, and the
#local file, and a new userID needs to be created for the user.
def updateAcctPass(acctDataFile, origEmail, newData, forPass=True):
    #Opens accDataFile to look for the password passed.
    adf_r = open(acctDataFile, 'r')
    dataLines = adf_r.readlines()
    adf_r.close()
    #Looks for the location of the pasword in the file.
    place = 3
    if not forPass:
        place = 1
    #If the password is found, then the file will be opened once again in write mode
    adf_w = open(acctDataFile, 'w')
    modify = 0
    #Modifies the file according to the location of the password.
    for line in dataLines:
        if modify > 0:
            modify += 1
        if origEmail in line:
            modify = 1
        if modify < place:
            adf_w.write(line)
        else: #Adds new line character if done.
            adf_w.write(newData + "\n")
            modify = 0
    adf_w.close()

#Function used when a user forgets their password and cannot login to the application.
#It contains the menu and the commands in order to initiate the password reset process. It will ask user to verify
#their account through a code sent to their email.
def forgot_update_password():
    while True:
        try:
            clear()
            print("--------------Reset Password------------------\n[Enter '0' if you wish to go back to the previous"
                  " screen]")
            print("\n**Verification is needed in order to reset your password**")
            print("\nPlease enter the email associated with your account:\n")
            email = input("Email: ")

            if email == '0': #Command to go back to the previous screen.
                return

            if email == "" or email.isspace(): #If input is empty.
                print("\nEmail cannot be empty.")
                print("Press any key to try again...")
                getch()
                clear()
                continue

            if email.isnumeric(): #If input is numeric only.
                print("\nEmail cannot be composed of only numbers.\nPress any key to try again...")
                getch()
                clear()
                continue

            email = validateEmail(email) #Validates input according to type.

            if email == 1: #If input is less than 6 characters long.
                print("\nEmail must be at least 6 characters long.\nPress any key to try again...")
                getch()
                continue

            if email == 2: #If input is more than 35 characters long.
                print("\nEmail must be less than 35 characters long.\nPress any key to try again...")
                getch()
                continue

            if email == 3: #If input does not follow correct format.
                print("\nEmail must contain letters, the '@' symbol, and a period (.)."
                      "\nPress any key to try again...")
                getch()
                continue

            email = email.lower() #Converting input to lowercase.

            #If email is contained within the applications database, an email will be sent to that address.
            if verifyEmail(email):
                #Generates a verification code and emails it to user.
                code = generate_password()
                #Sending email with code.
                sendEmail(email, code)
                while True:
                    clear()
                    print("--------------Reset Password------------------\n[Enter '0' if you wish to go back to the "
                          "previous screen]")
                    print("\nPlease enter the code that was just sent to the email:\n")
                    answer = input("Code: ")
                    answer = noleadingspace(answer) #Removes any leading or trailing space from the user input.

                    if answer == '0': #Command to go back to the previous screen.
                        return 0

                    if answer == "" or answer.isspace(): #If input is empty.
                        print("\nCode cannot be empty.")
                        print("Press any key to try again...")
                        getch()
                        clear()
                        continue
                    #Validating input by type.
                    answer = validateRecordPass(answer)

                    if answer == 2:#If input is more than 35 characters.
                        print("\nCode must be less than 35 characters long.\nPress any key to try again...")
                        getch()
                        continue

                    break

                if code == answer: #If code entered by the user matches the code sent, user can change password.
                    hashEmail = hashlib.pbkdf2_hmac('sha256', email.encode("utf-8"), b'&%$#f^',182)
                    newEmail = hashEmail.hex()

                    while True:
                        clear()
                        print("--------------Reset Password------------------\n[Enter '0' if you wish to cancel the "
                              "password reset process]")
                        print("\nEmail verified! Please enter a new password:")
                        inputPass = hidePassword()

                        if inputPass == '0': #Command to go back to the previous screen.
                            print("\nPassword reset cancelled!\nPress any key to go back...")
                            getch()
                            return

                        if inputPass == "" or inputPass.isspace(): #If input is empty.
                            print("\nPassword cannot be empty.\nPress any key to try again...")
                            getch()
                            continue
                        #Validating input by type.
                        validatePass = validatePassword(inputPass)

                        if validatePass == 1:#If input is less than 8 characters.
                            print("\nPassword must be at least 8 characters long.\nPress any key to try again...")
                            getch()
                            continue

                        elif validatePass == 2:#If input is longer than 35 characters.
                            print("\nPassword must be less than 35 characters long.\nPress any key to try again...")
                            getch()
                            continue

                        elif validatePass == 3: #If input does not follow correct format.
                            print("\nYour password must contain at least one of the following symbols: ~!@#$%^&*_-+='|\("
                                "){}[]:;\"\'<>,.?/"
                                "\nYour password must also contain at least one number, one uppercaser letter, and one"
                                " lowercase letter."
                                "\nPress any key to try again...")
                            getch()
                            continue
                        else:#If incorrect input, it will not update database.
                            break
                    #Hashing, and encoding new password.
                    newPassword = hashlib.pbkdf2_hmac('sha256', inputPass.encode("utf-8"), b'*@#d2',182).hex()

                    #Retreive the username, and old Id from database.
                    uname = onlyRetrieveUsername(email)
                    oldID = onlyRetrieveID(email)
                    #Opening database.txt file to update userID.
                    f = open("database.txt", "r")
                    lines = f.readlines()
                    f.close()
                    f = open("database.txt", "w")
                    newID = None
                    #Searching for the correct user ID.
                    for line in lines:
                        if oldID in line:
                            #Hashing the new userID
                            newID = combHash(inputPass, uname)
                            line = newID + "\t" + line.split("\t")[1]
                        f.write(line)
                    f.close()
                    update_user_ID(newID, oldID)
                    #Replaces oldID with new ID in both the text file and the database. Password is also updated.

                    #Updates password in accdatabase db document.
                    updateAcctPass('accdatabase', newEmail, newPassword)
                    print("\nPassword has been updated!")

                else:#If codes do not match an error is given.
                    print('\nThe code entered does not match!')

            else:#If email is invalid.
                print(f"\nThe email {email} is invalid!")

            print("Press any key to go back...")
            getch()
            clear()
            break
        #Catching errors.
        except socket.gaierror: #Cannot connect to internet error.
            print("\nConnection error. Please check your internet connection.")
            print("Press any key to try again...")
            getch()
            clear()

        except TimeoutError:#Connection error exception.
            print("\nConnection error. Please check your internet connection.")
            print("Press any key to try again...")
            getch()
            clear()

        except Exception:#Other errors.
            print("\nInvalid input.")
            print("Press any key to try again...")
            getch()
            clear()

#Function that allows a user to update their master password. This can be done while the user is logged in.
#This is very similar to the forgot password function but the user has been authenticated previously.
def update_master_password(id):
    while True:
        try:
            clear()
            print("--------------Reset Password------------------\n[Enter '0' if you wish to go back to the Settings"
                  " screen]")
            print("\n**Verification is needed in order to reset your password**")
            print("\nPlease enter the email associated with your account:")
            email = input("\nEmail: ")

            if email == "0": #Command to go back to previous screen.
                return '0'

            if email == "" or email.isspace(): #If input is empty.
                print("\nEmail cannot be empty.")
                print("Press any key to go back...")
                getch()
                clear()
                continue

            if email.isnumeric(): #If input is composed of numbers only.
                print("\nEmail cannot be composed of only numbers.\nPress any key to try again...")
                getch()
                clear()
                continue

            email = validateEmail(email)#Validating input by type.

            if email == 1:#If input is less than 6 characters.
                print("\nEmail must be at least 6 characters long.\nPress any key to try again...")
                getch()
                continue

            if email == 2: #If input is more than 36 characters.
                print("\nEmail must be less than 35 characters long.\nPress any key to try again...")
                getch()
                continue

            if email == 3: #If input does not follow the format.
                print("\nEmail must contain letters, the '@' symbol, and a period (.)."
                      "\nPress any key to try again...")
                getch()
                continue

            email = email.lower()#Converting input to lowercase.

            #Verifying email to make sure it is within the database.
            if verifyEmail(email):
                idOfEnteredEmail = retrieveIDByEmail(email) #The user's signed in email is compared to the userID
                if id == str(idOfEnteredEmail):#If email entered is associated with userID, code is generated.
                    #Generates a verification code and emails it to user.
                    code = generate_password()#Generating code.
                    sendEmail(email, code)#Sending code to email entered.

                    while True:
                        clear()
                        print("--------------Reset Password------------------\n[Enter '0' if you wish to go back to the"
                              " Settings screen]")
                        print("\nPlease enter the code that was just sent to the email:")
                        answer = input("\nCode: ")
                        answer = noleadingspace(answer) #Removes leading an trailing spaces.

                        if answer == '0':#Command to go back to previous screen.
                            return '0'

                        if answer == "" or answer.isspace(): #If input is empty.
                            print("\nCode cannot be empty.")
                            print("Press any key to try again...")
                            getch()
                            clear()
                            continue

                        answer = validateRecordPass(answer) #Validating input by type.
                        if answer == 2:
                            print("\nCode must be less than 35 characters long.\nPress any key to try again...")
                            getch()
                            continue

                        break

                    if code == answer: #If entered code matches sent code.
                        #The entered emailed is hashed and encoded for comparison purposes.
                        hashEmail = hashlib.pbkdf2_hmac('sha256', email.encode("utf-8"), b'&%$#f^',182)
                        newEmail = hashEmail.hex()

                        while True:
                            clear()
                            print("--------------Reset Password------------------\n[Enter '0' if you wish to go back "
                                  "to the Settings screen]")
                            print("\nEmail verified! Please enter a new password:")
                            inputPass = hidePassword()#Password is hidden from the screen.

                            if inputPass == '0':#Command to go back to previous screen.
                                print("\nPassword reset cancelled!\nPress any key to go back...")
                                getch()
                                return '0'

                            if inputPass == "" or inputPass.isspace():#If input is empty.
                                print("\nPassword cannot be empty.\nPress any key to try again...")
                                getch()
                                continue

                            if inputPass.isnumeric():#If input is numeric only.
                                print("\nPassword cannot be composed of only numbers.\nPress any key to try again...")
                                getch()
                                clear()
                                continue

                            validatePass = validatePassword(inputPass)#Validating input by type.

                            if validatePass == 1:#If input is less than 8 characters.
                                print("\nPassword must be at least 8 characters long.\nPress any key to try again...")
                                getch()
                                continue

                            elif validatePass == 2:#If input is longer than 35 characters.
                                print("\nPassword must be less than 35 characters long.\nPress any key to try again...")
                                getch()
                                continue

                            elif validatePass == 3:#If input does not follow format.
                                print("\nYour password must contain at least one of the following symbols: ~!@#$%^&*_-+='"
                                    "|\(){}[]:;\"\'<>,.?/"
                                    "\nYour password must also contain at least one number, one uppercaser letter, and"
                                    " one lowercase letter"
                                    "\nPress any key to try again...")
                                getch()
                                continue

                            else:
                                break

                        #Hashing, salting and encoding new password.
                        newPassword = hashlib.pbkdf2_hmac('sha256', inputPass.encode("utf-8"), b'*@#d2',182).hex()

                        #Retreive the username, and old Id from database.
                        uname = onlyRetrieveUsername(email)
                        oldID = onlyRetrieveID(email)
                        f = open("database.txt", "r")
                        lines = f.readlines()
                        f.close()
                        f = open("database.txt", "w")
                        newID = None
                        #Searches through database to find matching userID and password.
                        for line in lines:
                            if oldID in line:
                                newID = combHash(inputPass, uname)
                                line = newID + "\t" + line.split("\t")[1]
                            f.write(line)
                        f.close()
                        update_user_ID(newID, oldID)
                        #Updates password in accdatabase db document.
                        updateAcctPass('accdatabase', newEmail, newPassword)
                        print("\nPassword has been updated!")
                        print("Press any key to go back to the dashboard...")
                        getch()
                        clear()
                        return True


                    else:#If code does not match.
                        print('\nThe code entered does not match. The account could not be verified!')

                else:#If invalid email.
                    print(f"\nThe {email} is not valid!")

            else:#If invalid email.
                print(f"\nThe {email} is not valid!")

            print("Press any key to go back...")
            getch()
            clear()
            continue


        except socket.gaierror:#If connection error.
            print("\nConnection error. Please check your internet connection.")
            print("Press any key to try again...")
            getch()
            clear()

        except TimeoutError:#Connection error exception.
            print("\nConnection error. Please check your internet connection.")
            print("Press any key to try again...")
            getch()
            clear()

        except Exception:#Other errors.
            print("\nInvalid Input.")
            print("Press any key to try again...")
            getch()
            clear()

#Function allows users to change their master email address. This is done after the user has logged into the application
#and verification is still required. User will be sent a code to email in order to verify and authenticate account.
def changeMasterEmail(id):
    try:
        while True:
            clear()
            print("--------------Change Account Email------------------\n[Enter '0' if you wish to go back to the"
                  " Settings screen]")
            print("\n**Verification is needed in order to change your email**")

            print("\nPlease enter the email associated with your account: ")
            email = input("\nEmail: ")

            if email == '0':#Command to go back to previous screen.
                return '0'

            if email == "" or email.isspace(): #If input is empty.
                print("\nEmail cannot be empty!")
                print("Press any key to try again...")
                getch()
                clear()
                continue

            if email.isnumeric():#If input is numeric only.
                print("\nEmail cannot be composed of only numbers.\nPress any key to try again...")
                getch()
                clear()
                continue

            email = validateEmail(email)#Validation input by type.

            if email == 1:#If input is less than 6 characters.
                print("\nEmail must be at least 6 characters long.\nPress any key to try again...")
                getch()
                continue

            if email == 2:#If input is more than 35 characters.
                print("\nEmail must be less than 35 characters long.\nPress any key to try again...")
                getch()
                continue

            if email == 3:#If input does not follow format.
                print("\nEmail must contain letters, the '@' symbol, and a period (.)."
                      "\nPress any key to try again...")
                getch()
                continue

            email = email.lower()#Converting input to lowercase.

            if verifyEmail(email):#Verifying if email is within database.
                idOfEnteredEmail = retrieveIDByEmail(email)
                #If userID matches userID associated with email address, a code is generated.
                if id == str (idOfEnteredEmail):
                    #Generate the code and email it to user
                    code = generate_password()#Code generate function.
                    sendEmail(email, code)#Sending code to email address.
                    while True:
                        clear()
                        print("--------------Change Account Email------------------\n[Enter '0' if you wish to go back"
                              " to the Settings screen]")
                        print("\nPlease enter the code that was just sent to the email: " + email)
                        answer = input("\nCode :")
                        answer = noleadingspace(answer)#Removing leading and trailing spaces from input.

                        if answer == '0':#Command to go back to previous screen.
                            return '0'

                        if answer == "" or answer.isspace():#If input is empty.
                            print("\nCode cannot be empty!")
                            print("Press any key to try again...")
                            getch()
                            clear()
                            continue

                        answer = validateRecordPass(answer)#Validating input by type.
                        if answer == 2:#If input is more than 35 characters.
                            print("\nCode must be less than 35 characters long.\nPress any key to try again...")
                            getch()
                            continue
                        break
                    #If entered code matcher code sent, the user can change password.
                    if code == answer:
                            #Hashing and encoding email for comparing.
                            hashEmail = hashlib.pbkdf2_hmac('sha256', email.encode("utf-8"), b'&%$#f^',182).hex()
                            while True:
                                clear()
                                print("--------------Change Account Email------------------\n[Enter '0' if you wish "
                                      "to go back to the Settings screen]")
                                print("\nCode verified! Please enter your new email: ")
                                inputEmail = input("\nNew Email: ")

                                if inputEmail == '0':#Command to go back to previous screen.
                                    print("\nEmail reset has been cancelled!\nPress any key to go back...")
                                    getch()
                                    return '0'

                                if inputEmail == "" or inputEmail.isspace():#If input is empty.
                                    print("\nEmail cannot be empty.\nPress any key to try again...")
                                    getch()
                                    continue

                                if inputEmail.isnumeric():#If input is numeric only.
                                    print("\nEmail cannot be composed of only numbers.\nPress any key to try again...")
                                    getch()
                                    clear()
                                    continue

                                inputEmail = inputEmail.lower()#Coverting input to lower case.

                                while checkDuplicateEmail(inputEmail):#If input email corresponds to a duplicate email.
                                    inputEmail = input("\nEmail Taken. Please enter another email for your account: ")
                                    if inputEmail == '0':#Command to go back to previous screen.
                                        return '0'
                                    inputEmail = inputEmail.lower()#Converting input to lowercase.

                                email = validateEmail(inputEmail)#Validating input by type.

                                if email == 1:#If input is less than 6 characters.
                                    print("\nEmail must be at least 6 characters long.\nPress any key to try again...")
                                    getch()
                                    continue

                                if email == 2:#If input is more than 35 characters.
                                    print("\nEmail must be less than 35 characters long.\nPress any key to try "
                                          "again...")
                                    getch()
                                    continue

                                if email == 3:#If input does not match format.
                                    print("\nEmail must contain letters, the '@' symbol, and a period (.)."
                                          "\nPress any key to try again...")
                                    getch()
                                    continue
                                email = email.lower()#Converting email to lowercase.
                                break

                            #Hashing and encoding new email for comparing.
                            newEmail = hashlib.pbkdf2_hmac('sha256', inputEmail.encode("utf-8"), b'&%$#f^',182).hex()
                            #Update password in acc database.
                            updateAcctPass('accdatabase', hashEmail, newEmail, False)

                            print("\nEmail has been updated to " + inputEmail)
                            if id is not None:
                                update_master_email(inputEmail, id)
                                return False
                    else:#If code does not match, error will be displayed.
                        print('\nThe entered code does not match. The account could not be verified!')
                        print("Press any key to go back...")
                        getch()
                        clear()
                        return
                else:#If email is invalid.
                    print(f"\nThe {email} email is not valid!")
                    print("Press any key to try again...")
                    getch()
                    clear()
                    continue

            else:#If email is not valid
                print(f"\nThe {email} email is not valid!")
                print("Press any key to try again...")
                getch()
                clear()
                continue

    except socket.gaierror:#Connection error exception.
        print("\nConnection error. Please check your internet connection.")
        print("Press any key to try again...")
        getch()
        clear()

    except TimeoutError:  # Connection error exception.
        print("\nConnection error. Please check your internet connection.")
        print("Press any key to try again...")
        getch()
        clear()

    except Exception:#Other errors.
        print("\nInvalid Input.")
        print("Press any key to try again...")
        getch()
        clear()

#Functionused to retrieve username and send email by using the email associated with the account.
# Sends an email after retrieval.
def retrieveUsername(email):
    sql = ("select * from Registered_Users ")
    cursor.execute(sql )
    results = cursor.fetchall()
    #Searching through results for entered email
    for rec in results:
        if decrypt(rec[0], rec[2]) == email:#If email found sends a message to the entered email.
            sendEmail(email, decrypt(rec[0], rec[1]), "username")
    return False#If email not found, returns false.

#Function used to only retrieve the user email. Does not send email to the account.
def onlyRetrieveUsername(email):
    sql = ("select * from Registered_Users ")
    cursor.execute(sql )
    results = cursor.fetchall()
    # Searching through results for entered email
    for rec in results:
        if decrypt(rec[0], rec[2]) == email:
            return decrypt(rec[0], rec[1])
    return False#If email not found, returns false.

#Function used to retrieve the userID. This will send an email to the user if the userID matcher the email entered.
def retrieveID(email):
    sql = ("select * from Registered_Users ")
    cursor.execute(sql )
    results = cursor.fetchall()
    # Searching through results for entered email
    for rec in results:
        if decrypt(rec[0], rec[2]) == email:#If email found sends a message to the entered email.
            sendEmail(email, str(rec[0]), "ID")
    return False#If email not found, returns false.

#Function only retrieves the userID. No email is sent out in this function. Used for verification purposes.
def onlyRetrieveID(email):
    sql = ("select * from Registered_Users ")
    cursor.execute(sql )
    results = cursor.fetchall()
    # Searching through results for entered email.
    for rec in results:
        if decrypt(rec[0], rec[2]) == email:
            return rec[0]
    return False#If email not found, returns false.

#Function used to retrieve userID by using the username. Used for verification purposes.
def retrieveIDByName(usrName):
    sql = ("select * from Registered_Users ")
    cursor.execute(sql )
    results = cursor.fetchall()
    # Searching through results for entered email.
    for rec in results:
        if decrypt(rec[0], rec[1]) == usrName:
            return rec[0]
    return False#If email not found, returns false.

#Function used to retrieve userID by using the email address. Used for verification purposes.
def retrieveIDByEmail(email):
    sql = ("select * from Registered_Users ")
    cursor.execute(sql )
    results = cursor.fetchall()
    # Searching through results for entered email.
    for rec in results:
        if decrypt(rec[0], rec[2]) == email:
            return rec[0]
    return False#If email not found, returns false.

#This functions contains the controls and menu for the username recovery option. It allows users to receive an email
#with their username. This option can be accessed before loggin into the application.
def usernameRecovery():
    while True:
        try:
            clear()
            print("--------------Username Recovery------------------\n[Enter '0' if you wish to go back to the"
                  " previous screen]")
            print("\nPlease enter the email associated with your account:\n")
            email = input("Email: ")

            if email == '0':#Command to go back to previous screen.
                return 0

            if email == "" or email.isspace():#If input is empty.
                print("\nEmail cannot be empty!")
                print("Press any key to go back...")
                getch()
                clear()
                continue

            if email.isnumeric():#If input is numeric only.
                print("\nEmail cannot be composed of only numbers.\nPress any key to try again...")
                getch()
                clear()
                continue

            email = validateEmail(email)#Validating input by type.

            if email == 1:#If input is less than 6 characters.
                print("\nEmail must be at least 6 characters long.\nPress any key to try again...")
                getch()
                continue

            if email == 2:#If input is more than 35 characters.
                print("\nEmail must be less than 35 characters long.\nPress any key to try again...")
                getch()
                continue

            if email == 3:#If input does not follow format.
                print("\nEmail must contain letters, the '@' symbol, and a period (.)."
                      "\nPress any key to try again...")
                getch()
                continue

            email = email.lower()#Coverting input to lowercase.

            if verifyEmail(email):#Checks if entered email is within the database,
                retrieveUsername(email)#If email is within the app, an email is sent to the address entered.
                print("\nIf account exists, an email will be sent to the entered email. Please check your email.")
            else:#If email is not within database, no email will be sent.
                time.sleep(2)
                print(f"\nIf account exists, an email will be sent to the entered email. Please check your email.")

            print("Press any key to go back...")
            getch()
            clear()
            break

        except socket.gaierror:#Connection error exception.
            print("\nConnection error. Please check your internet connection.")
            print("Press any key to try again...")
            getch()
            clear()

        except TimeoutError:#Connection error exception.
            print("\nConnection error. Please check your internet connection.")
            print("Press any key to try again...")
            getch()
            clear()

        except Exception:#Other exceptions.
            print("\nInvalid Input.")
            print("Press any key to try again...")
            getch()
            clear()