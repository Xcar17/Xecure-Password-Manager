import socket

from database import cursor
from dbsetup import decrypt, update_master_email, update_user_ID, checkDuplicateEmail
from random_pwd_generator import generate_password
import smtplib
from hashing import combHash
import hashlib
from msvcrt import getch
from clear import myExit, clear
from input_val import validatePassword, noleadingspace, validateEmail, validateRecordPass
from hidePassword import hidePassword
import time


def sendEmail(email, code, retreival=None):
    # creates SMTP session
    s = smtplib.SMTP('smtp.gmail.com', 587)

    # start TLS for security
    s.starttls()

    # Authentication
    s.login("xecureddb@gmail.com", "Xecured123")

    explanation = "\n-------Xecured Password Manager-------\n\nSomeone has attempted to authenticate into your Xecured Password Manager account. " \
                  "If this was not you, it is recommended that you change your password. If this was you please follow the instructions below.\n\n" \
                  "\nPlease go back to the Xecured application and enter this code when prompted in order to set a new password:\n"
    if retreival is not None:
        explanation = f"\n-------Xecured Password Manager-------\n\nSomeone has requested your Xecured Password Manager user name." \
                  "If this was not you, it is recommended that you change your password. If this was you please follow the instructions below.\n\n" \
                      f"\nYour {retreival} is:\n"

    msg = explanation + code
    # sending the mail
    s.sendmail("sender_email_id", email, msg)

    # terminating the session
    s.quit()


def verifyEmail(email):
    # try:
    sql = ("select id, Email from Registered_Users ")
    cursor.execute(sql )
    results = cursor.fetchall()

    for rec in results:
        if decrypt(rec[0], rec[1]) == email:
            return True
    return False

def updateAcctPass(acctDataFile, origEmail, newData, forPass=True):
    adf_r = open(acctDataFile, 'r')
    dataLines = adf_r.readlines()
    adf_r.close()

    place = 3
    if not forPass:
        place = 1

    adf_w = open(acctDataFile, 'w')
    modify = 0
    for line in dataLines:
        if modify > 0:
            modify += 1

        if origEmail in line:
            modify = 1
        if modify < place:
            adf_w.write(line)
        else:
            adf_w.write(newData + "\n")
            modify = 0
    adf_w.close()

def forgot_update_password():
    while True:
        try:
            clear()
            print("--------------Reset Password------------------\n[Enter '0' if you wish to go back to the previous screen]")
            print("\n**Verification is needed in order to reset your password**")
            print("Please enter the email associated with your account:\n")
            email = input("Email: ")

            if email == '0':
                return

            if email == "" or email.isspace():
                print("\nEmail cannot be empty.")
                print("Press any key to try again...")
                getch()
                clear()
                continue



            if email.isnumeric():
                print("\nEmail cannot be composed of only numbers.\nPress any key to try again...")
                getch()
                clear()
                continue

            email = validateEmail(email)


            if email == 1:
                print("\nEmail must be at least 6 characters long.\nPress any key to try again...")
                getch()
                continue

            if email == 2:
                print("\nEmail must be less than 35 characters long.\nPress any key to try again...")
                getch()
                continue

            if email == 3:
                print("\nEmail must contain letters, the '@' symbol, and a period (.)."
                      "\nPress any key to try again...")
                getch()
                continue



            if verifyEmail(email):
                #generates a verification code and emails it to user
                code = generate_password()
                sendEmail(email, code)
                while True:
                    clear()
                    print("--------------Reset Password------------------\n[Enter '0' if you wish to go back to the previous screen]")
                    print("\nPlease enter the code that was just sent to the email:\n")
                    answer = input("Code: ")
                    answer = noleadingspace(answer)

                    if answer == '0':
                        return 0

                    if answer == "" or answer.isspace():
                        print("\nCode cannot be empty.")
                        print("Press any key to try again...")
                        getch()
                        clear()
                        continue



                    answer = validateRecordPass(answer)
                    if answer == 2:
                        print("\nCode must be less than 35 characters long.\nPress any key to try again...")
                        getch()
                        continue

                    break

                if code == answer:
                    hashEmail = hashlib.pbkdf2_hmac('sha256', email.encode("utf-8"), b'&%$#f^',182)# todo implement random salt test
                    newEmail = hashEmail.hex()

                    while True:
                        clear()
                        print("--------------Reset Password------------------\n[Enter '0' if you wish to cancel the password reset process]")
                        print("\nEmail verified! Please enter a new password:")
                        #inputPass = input("New Password: ")
                        inputPass = hidePassword()

                        if inputPass == '0':
                            print("\nPassword reset cancelled!\nPress any key to go back...")
                            getch()
                            return

                        if inputPass == "" or inputPass.isspace():
                            print("\nPassword cannot be empty.\nPress any key to try again...")
                            getch()
                            continue

                        validatePass = validatePassword(inputPass)

                        if validatePass == 1:
                            print("\nPassword must be at least 8 characters long.\nPress any key to try again...")
                            getch()
                            continue

                        elif validatePass == 2:
                            print("\nPassword must be less than 35 characters long.\nPress any key to try again...")
                            getch()
                            continue

                        elif validatePass == 3:
                            print(
                                "\nYour password must contain at least one of the following symbols: ~!@#$%^&*_-+='|\(){}[]:;\"\'<>,.?/"
                                "\nYour password must also contain at least one number, one uppercaser letter, and one lowercase letter."
                                "\nPress any key to try again...")
                            getch()
                            continue


                        else:
                            break

                    newPassword = hashlib.pbkdf2_hmac('sha256', inputPass.encode("utf-8"), b'*@#d2',182).hex()

                    # retreive the username, and old Id from database
                    uname = onlyRetrieveUsername(email)
                    oldID = onlyRetrieveID(email)
                    f = open("database.txt", "r")
                    lines = f.readlines()
                    f.close()
                    f = open("database.txt", "w")
                    newID = None
                    for line in lines:
                        if oldID in line:
                            newID = combHash(inputPass, uname)
                            line = newID + "\t" + line.split("\t")[1]
                        f.write(line)
                    f.close()
                    update_user_ID(newID, oldID)

                    #updates password in accdatabase db document
                    updateAcctPass('accdatabase', newEmail, newPassword)
                    print("\nPassword has been updated!")

                else:
                    print('\nThe code entered does not match!')

            else:
                print(f"\nThe email {email} is invalid!")

            print("Press any key to go back...")
            getch()
            clear()
            break

        except socket.gaierror:
            print("\nConnection error. Please check your internet connection.")
            print("Press any key to try again...")
            getch()
            clear()
        except Exception:
            print("\nInvalid input.")
            print("Press any key to try again...")
            getch()
            clear()



def update_master_password(id):
    while True:
        try:
            clear()
            print("--------------Reset Password------------------\n[Enter '0' if you wish to go back to the Settings screen]")
            print("\n**Verification is needed in order to reset your password**")
            print("\nPlease enter the email associated with your account:")
            email = input("\nEmail: ")

            if email == "0":
                return '0'

            if email == "" or email.isspace():
                print("\nEmail cannot be empty.")
                print("Press any key to go back...")
                getch()
                clear()
                continue

            if email.isnumeric():
                print("\nEmail cannot be composed of only numbers.\nPress any key to try again...")
                getch()
                clear()
                continue

            email = validateEmail(email)

            if email == 1:
                print("\nEmail must be at least 6 characters long.\nPress any key to try again...")
                getch()
                continue

            if email == 2:
                print("\nEmail must be less than 35 characters long.\nPress any key to try again...")
                getch()
                continue

            if email == 3:
                print("\nEmail must contain letters, the '@' symbol, and a period (.)."
                      "\nPress any key to try again...")
                getch()
                continue

            if verifyEmail(email):
                idOfEnteredEmail = retrieveIDByEmail(email)
                if id == str(idOfEnteredEmail):
                    #generates a verification code and emails it to user
                    code = generate_password()
                    sendEmail(email, code)

                    while True:
                        clear()
                        print("--------------Reset Password------------------\n[Enter '0' if you wish to go back to the Settings screen]")
                        print("\nPlease enter the code that was just sent to the email:")
                        answer = input("\nCode: ")
                        answer = noleadingspace(answer)

                        if answer == '0':
                            return '0'

                        if answer == "" or answer.isspace():
                            print("\nCode cannot be empty.")
                            print("Press any key to try again...")
                            getch()
                            clear()
                            continue



                        answer = validateRecordPass(answer)
                        if answer == 2:
                            print("\nCode must be less than 35 characters long.\nPress any key to try again...")
                            getch()
                            continue

                        break





                    if code == answer:
                        hashEmail = hashlib.pbkdf2_hmac('sha256', email.encode("utf-8"), b'&%$#f^',182)# todo implement random salt test
                        newEmail = hashEmail.hex()

                        while True:

                            clear()
                            print("--------------Reset Password------------------\n[Enter '0' if you wish to go back to the Settings screen]")
                            print("\nEmail verified! Please enter a new password:")
                            #inputPass = input("New Password: ")
                            inputPass = hidePassword()

                            if inputPass == '0':
                                print("\nPassword reset cancelled!\nPress any key to go back...")
                                getch()
                                return '0'

                            if inputPass == "" or inputPass.isspace():
                                print("\nPassword cannot be empty.\nPress any key to try again...")
                                getch()
                                continue

                            if inputPass.isnumeric():
                                print("\nPassword cannot be composed of only numbers.\nPress any key to try again...")
                                getch()
                                clear()
                                continue


                            validatePass = validatePassword(inputPass)

                            if validatePass == 1:
                                print("\nPassword must be at least 8 characters long.\nPress any key to try again...")
                                getch()
                                continue

                            elif validatePass == 2:
                                print("\nPassword must be less than 35 characters long.\nPress any key to try again...")
                                getch()
                                continue

                            elif validatePass == 3:
                                print(
                                    "\nYour password must contain at least one of the following symbols: ~!@#$%^&*_-+='|\(){}[]:;\"\'<>,.?/"
                                    "\nYour password must also contain at least one number, one uppercaser letter, and one lowercase letter"
                                    "\nPress any key to try again...")
                                getch()
                                continue


                            else:
                                break

                        newPassword = hashlib.pbkdf2_hmac('sha256', inputPass.encode("utf-8"), b'*@#d2',182).hex()

                        # retreive the username, and old Id from database

                        uname = onlyRetrieveUsername(email)
                        oldID = onlyRetrieveID(email)
                        f = open("database.txt", "r")
                        lines = f.readlines()
                        f.close()
                        f = open("database.txt", "w")
                        newID = None
                        for line in lines:
                            if oldID in line:
                                newID = combHash(inputPass, uname)
                                line = newID + "\t" + line.split("\t")[1]
                            f.write(line)
                        f.close()
                        update_user_ID(newID, oldID)
                        #updates password in accdatabase db document
                        updateAcctPass('accdatabase', newEmail, newPassword)
                        print("\nPassword has been updated!")
                        print("Press any key to go back to the dashboard...")
                        getch()
                        clear()
                        return True


                    else:
                        print('\nThe code entered does not match. The account could not be verified!')

                else:
                    print(f"\nThe {email} is not valid!")

            else:
                print(f"\nThe {email} is not valid!")

            print("Press any key to go back...")
            getch()
            clear()
            break


        except socket.gaierror:
            print("\nConnection error. Please check your internet connection.")
            print("Press any key to try again...")
            getch()
            clear()

        except Exception as e:
            print("\nInvalid Input.")
            print("Press any key to try again...")
            getch()
            clear()


def changeMasterEmail(id):
    try:
        while True:
            clear()
            print("--------------Change Account Email------------------\n[Enter '0' if you wish to go back to the Settings screen]")
            print("\n**Verification is needed in order to change your email**")
            email = input("\nPlease enter the email associated with your account: ")

            if email == '0':
                return '0'

            if email == "" or email.isspace():
                print("\nEmail cannot be empty!")
                print("Press any key to try again...")
                getch()
                clear()
                continue

            if email.isnumeric():
                print("\nEmail cannot be composed of only numbers.\nPress any key to try again...")
                getch()
                clear()
                continue

            email = validateEmail(email)

            if email == 1:
                print("\nEmail must be at least 6 characters long.\nPress any key to try again...")
                getch()
                continue

            if email == 2:
                print("\nEmail must be less than 35 characters long.\nPress any key to try again...")
                getch()
                continue

            if email == 3:
                print("\nEmail must contain letters, the '@' symbol, and a period (.)."
                      "\nPress any key to try again...")
                getch()
                continue

            if verifyEmail(email):
                idOfEnteredEmail = retrieveIDByEmail(email)
                if id == str (idOfEnteredEmail):
                    #generate the code and email it to user
                    code = generate_password()
                    sendEmail(email, code)
                    while True:
                        clear()
                        print("--------------Change Account Email------------------\n[Enter '0' if you wish to go back to the Settings screen]")
                        print("\nPlease enter the code that was just sent to the email: " + email)
                        answer = input("\nCode :")
                        answer = noleadingspace(answer)

                        if answer == '0':
                            return '0'

                        if answer == "" or answer.isspace():
                            print("\nCode cannot be empty!")
                            print("Press any key to try again...")
                            getch()
                            clear()
                            continue

                        answer = validateRecordPass(answer)
                        if answer == 2:
                            print("\nCode must be less than 35 characters long.\nPress any key to try again...")
                            getch()
                            continue
                        break




                    if code == answer:
                            hashEmail = hashlib.pbkdf2_hmac('sha256', email.encode("utf-8"), b'&%$#f^',182).hex()  # todo implement random salt test
                            while True:
                                clear()
                                print("--------------Change Account Email------------------\n[Enter '0' if you wish to go back to the Settings screen]")
                                print("\nCode verified! Please enter your new email: ")
                                inputEmail = input("\nNew Email: ")

                                while checkDuplicateEmail(inputEmail):
                                    inputEmail = input("\nEmail Taken. Please enter another email for your account: ")

                                if inputEmail == '0':
                                    print("\nEmail reset has been cancelled!\nPress any key to go back...")
                                    getch()
                                    return '0'

                                if inputEmail == "" or inputEmail.isspace():
                                    print("\nEmail cannot be empty.\nPress any key to try again...")
                                    getch()
                                    continue

                                if inputEmail.isnumeric():
                                    print("\nEmail cannot be composed of only numbers.\nPress any key to try again...")
                                    getch()
                                    clear()
                                    continue

                                email = validateEmail(inputEmail)



                                if email == 1:
                                    print("\nEmail must be at least 6 characters long.\nPress any key to try again...")
                                    getch()
                                    continue

                                if email == 2:
                                    print("\nEmail must be less than 35 characters long.\nPress any key to try again...")
                                    getch()
                                    continue

                                if email == 3:
                                    print("\nEmail must contain letters, the '@' symbol, and a period (.)."
                                          "\nPress any key to try again...")
                                    getch()
                                    continue

                                break


                            newEmail = hashlib.pbkdf2_hmac('sha256', inputEmail.encode("utf-8"), b'&%$#f^',
                                                            182).hex()
                            #update password in acc databae
                            updateAcctPass('accdatabase', hashEmail, newEmail, False)

                            print("\nEmail has been updated to " + inputEmail)
                            if id is not None:
                                update_master_email(inputEmail, id)
                                return False
                    else:
                        print('\nThe entered code does not match. The account could not be verified!')
                        print("Press any key to go back...")
                        getch()
                        clear()
                        return
                else:
                    print(f"\nThe {email} email is not valid!")
                    print("Press any key to try again...")
                    getch()
                    clear()
                    continue

            else:
                print(f"\nThe {email} email is not valid!")
                print("Press any key to try again...")
                getch()
                clear()
                continue

    except socket.gaierror:
        print("\nConnection error. Please check your internet connection.")
        print("Press any key to try again...")
        getch()
        clear()

    except Exception:
        print("\nInvalid Input.")
        print("Press any key to try again...")
        getch()
        clear()



def retrieveUsername(email):
    # try:
    sql = ("select * from Registered_Users ")
    cursor.execute(sql )
    results = cursor.fetchall()

    for rec in results:
        if decrypt(rec[0], rec[2]) == email:
            sendEmail(email, decrypt(rec[0], rec[1]), "username")
    return False

def onlyRetrieveUsername(email):
    sql = ("select * from Registered_Users ")
    cursor.execute(sql )
    results = cursor.fetchall()

    for rec in results:
        if decrypt(rec[0], rec[2]) == email:
            return decrypt(rec[0], rec[1])
    return False


def retrieveID(email):
    # try:
    sql = ("select * from Registered_Users ")
    cursor.execute(sql )
    results = cursor.fetchall()

    for rec in results:
        if decrypt(rec[0], rec[2]) == email:
            sendEmail(email, str(rec[0]), "ID")
    return False

def onlyRetrieveID(email):
    sql = ("select * from Registered_Users ")
    cursor.execute(sql )
    results = cursor.fetchall()

    for rec in results:
        if decrypt(rec[0], rec[2]) == email:
            return rec[0]
    return False

def retrieveIDByName(usrName):


    # try:
    sql = ("select * from Registered_Users ")
    cursor.execute(sql )
    results = cursor.fetchall()

    for rec in results:
        if decrypt(rec[0], rec[1]) == usrName:
            return rec[0]
    return False

def retrieveIDByEmail(email):
    # try:
    sql = ("select * from Registered_Users ")
    cursor.execute(sql )
    results = cursor.fetchall()

    for rec in results:
        if decrypt(rec[0], rec[2]) == email:
            return rec[0]
    return False

def usernameRecovery():
    while True:
        try:
            clear()
            print("--------------Username Recovery------------------\n[Enter '0' if you wish to go back to the previous screen]")
            print("\nPlease enter the email associated with your account:\n")
            email = input("Email: ")

            if email == '0':
                return 0

            if email == "" or email.isspace():
                print("\nEmail cannot be empty!")
                print("Press any key to go back...")
                getch()
                clear()
                continue

            if email.isnumeric():
                print("\nEmail cannot be composed of only numbers.\nPress any key to try again...")
                getch()
                clear()
                continue

            email = validateEmail(email)

            if email == 1:
                print("\nEmail must be at least 6 characters long.\nPress any key to try again...")
                getch()
                continue

            if email == 2:
                print("\nEmail must be less than 35 characters long.\nPress any key to try again...")
                getch()
                continue

            if email == 3:
                print("\nEmail must contain letters, the '@' symbol, and a period (.)."
                      "\nPress any key to try again...")
                getch()
                continue


            if verifyEmail(email):
                retrieveUsername(email)
                print("\nIf account exists, an email will be sent to the entered email. Please check your email.")
            else:
                time.sleep(2)
                print(f"\nIf account exists, an email will be sent to the entered email. Please check your email.")

            print("Press any key to go back...")
            getch()
            clear()
            break


        except socket.gaierror:
            print("\nConnection error. Please check your internet connection.")
            print("Press any key to try again...")
            getch()
            clear()

        except Exception:
            print("\nInvalid Input.")
            print("Press any key to try again...")
            getch()
            clear()