from database import cursor
from dbsetup import decrypt, update_master_email, update_user_ID
from random_pwd_generator import generate_password
import smtplib
from hashing import combHash
import hashlib
from msvcrt import getch
from clear import myExit, clear
from input_val import validatePassword, noleadingspace


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
                break

            if email == "":
                print("\nEmail cannot be blank.")
                print("Press any key to go back...")
                getch()
                clear()
                break


            if verifyEmail(email):
                #generates a verification code and emails it to user
                code = generate_password()
                sendEmail(email, code)
                clear()
                print("--------------Reset Password------------------\n[Enter '0' if you wish to go back to the previous screen]")
                print("\nPlease enter the code that was just sent to the email:\n")
                answer = input("Code: ")
                answer = noleadingspace(answer)

                if answer == '0':
                    break

                if code == answer:
                    hashEmail = hashlib.pbkdf2_hmac('sha256', email.encode("utf-8"), b'&%$#f^',182)# todo implement random salt test
                    newEmail = hashEmail.hex()

                    while True:
                        clear()
                        print("--------------Reset Password------------------\n[Enter '0' if you wish to cancel the password reset process]")
                        print("\nEmail verified! Please enter a new password:")
                        inputPass = input("New Password: ")

                        if inputPass == '0':
                            print("\nPassword reset cancelled\nPress any key to go back...")
                            getch()
                            break

                        if inputPass == "":
                            print("\nPassword cannot be empty\nPress any key to try again...")
                            getch()
                            continue

                        validatePass = validatePassword(inputPass)

                        if validatePass == 1:
                            print("\nPassword must be at least 8 characters long\nPress any key to try again...")
                            getch()
                            continue

                        elif validatePass == 2:
                            print("\nPassword must be less than 20 characters long\nPress any key to try again...")
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

                else:
                    print('\nThe code entered does not match.')

            else:
                print(f"\nThe {email} email was not found.")

            print("Press any key to go back...")
            getch()
            clear()
            break

        except Exception:
            print("\nInvalid Input.")
            print("Press any key to try again...")
            getch()
            clear()

#todo need to figure out how to go to settings if email is left blank (or if its invalid)
def update_master_password(id):
    while True:
        try:
            clear()
            print("--------------Reset Password------------------\n[Enter '0' if you wish to go back to the Settings screen]")
            print("\n**Verification is needed in order to reset your password**")
            print("\nPlease enter the email associated with your account:")
            email = input("Email: ")

            if email == "0":
                return '0'

            if email == "":
                print("\nEmail cannot be blank.")
                print("Press any key to go back...")
                getch()
                clear()
                break

            if email == "0":
                clear()
                break

            if verifyEmail(email):
                idOfEnteredEmail = retrieveIDByEmail(email)
                if id == str(idOfEnteredEmail):
                    #generates a verification code and emails it to user
                    code = generate_password()
                    sendEmail(email, code)
                    clear()
                    print("--------------Reset Password------------------\n[Enter '0' if you wish to go back to the Settings screen]")
                    print("\nPlease enter the code that was just sent to the email:")
                    answer = input("Code: ")
                    answer = noleadingspace(answer)

                    if answer == '0':
                        return '0'

                    if code == answer:
                        hashEmail = hashlib.pbkdf2_hmac('sha256', email.encode("utf-8"), b'&%$#f^',182)# todo implement random salt test
                        newEmail = hashEmail.hex()

                        while True:

                            clear()
                            print("--------------Reset Password------------------\n[Enter '0' if you wish to go back to the Settings screen]")
                            print("\nEmail verified! Please enter a new password:")
                            inputPass = input("New Password: ")

                            if inputPass == '0':
                                return '0'

                            if inputPass == "":
                                print("\nPassword cannot be empty\nPress any key to try again...")
                                getch()
                                continue

                            validatePass = validatePassword(inputPass)

                            if validatePass == 1:
                                print("\nPassword must be at least 8 characters long\nPress any key to try again...")
                                getch()
                                continue

                            elif validatePass == 2:
                                print("\nPassword must be less than 20 characters long\nPress any key to try again...")
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
                        print('\nThe code entered does not match.')

                else:
                    print(f"\nThe {email} is not valid")

            else:
                print(f"\nThe {email} is not valid")

            print("Press any key to go back...")
            getch()
            clear()
            break

        except Exception as e:
            print(e)
            print("\nInvalid Input.")
            print("Press any key to try again...")
            getch()
            clear()



#
# def changeMasterEmail(id):
#     print("--------------Change Account Email------------------")
#     email = input("\nPlease enter the email associated with your account: ")
#     if verifyEmail(email):
#         idOfEnteredEmail = retrieveIDByEmail(email)
#         if id == str (idOfEnteredEmail):
#             #generate the code and email it to user
#             code = generate_password()
#             sendEmail(email, code)
#             print("Please enter the code that was just sent to the email: " + email)
#             answer = input("Code :")
#             if code == answer:
#                     hashEmail = hashlib.pbkdf2_hmac('sha256', email.encode("utf-8"), b'&%$#f^',182).hex()  # todo implement random salt test
#                     clear()
#                     print("--------------Change Account Email------------------")
#
#                     print("\nCode verified. Please enter your new email: ")
#                     inputEmail = input("New Email: ")
#                     newEmail = hashlib.pbkdf2_hmac('sha256', inputEmail.encode("utf-8"), b'&%$#f^',
#                                                     182).hex()
#                     #update password in acc databae
#                     updateAcctPass('accdatabase', hashEmail, newEmail, False)
#
#                     print("\nEmail has been updated to " + inputEmail)
#                     if id is not None:
#                         update_master_email(inputEmail, id)
#                         return False
#             else:
#                 print('\nCode does not match')
#         else:
#             print(f"\nThe {email} email is not valid.")
#
#     else:
#         print(f"\nThe {email} email is not valid.")



def changeMasterEmail(id):
    print("--------------Change Account Email------------------\n[Enter '0' if you wish to go back to the Settings screen]")
    print("\n**Verification is needed in order to change your email**")
    email = input("\nPlease enter the email associated with your account: ")

    if email == '0':
        return '0'

    if email == "":
        print("\nEmail cannot be blank.")
        return

    if verifyEmail(email):
        idOfEnteredEmail = retrieveIDByEmail(email)
        if id == str (idOfEnteredEmail):
            #generate the code and email it to user
            code = generate_password()
            sendEmail(email, code)
            clear()
            print("--------------Change Account Email------------------\n[Enter '0' if you wish to go back to the Settings screen]")
            print("\nPlease enter the code that was just sent to the email: " + email)
            answer = input("Code :")

            if answer == '0':
                return  '0'

            if code == answer:
                    hashEmail = hashlib.pbkdf2_hmac('sha256', email.encode("utf-8"), b'&%$#f^',182).hex()  # todo implement random salt test
                    clear()
                    print("--------------Change Account Email------------------\n[Enter '0' if you wish to go back to the Settings screen]")
                    print("\nCode verified! Please enter your new email: ")
                    inputEmail = input("New Email: ")

                    if inputEmail == '0':
                        return '0'

                    newEmail = hashlib.pbkdf2_hmac('sha256', inputEmail.encode("utf-8"), b'&%$#f^',
                                                    182).hex()
                    #update password in acc databae
                    updateAcctPass('accdatabase', hashEmail, newEmail, False)

                    print("\nEmail has been updated to " + inputEmail)
                    if id is not None:
                        update_master_email(inputEmail, id)
                        return False
            else:
                print('\nCode does not match')
        else:
            print(f"\nThe {email} email is not valid.")

    else:
        print(f"\nThe {email} email is not valid.")



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
                break

            if verifyEmail(email):
                retrieveUsername(email)
                print("\nUsername has been sent to the Email associated with the account.")
            else:
                print(f"\nThe {email} email was not found.")

            print("Press any key to go back...")
            getch()
            clear()
            break

        except Exception:
            print("\nInvalid Input.")
            print("Press any key to try again...")
            getch()
            clear()

def idRecovery():
    while True:
        try:
            clear()
            print("--------------Id Recovery------------------")
            print("\nPlease enter the email associated with your account:\n")
            email = input("Email: ")

            if verifyEmail(email):
                retrieveID(email)
                print("\nID has been sent to the Email associated with the account.")
            else:
                print(f"\nThe {email} email was not found.")

            print("Press any key to go back...")
            getch()
            clear()
            break

        except Exception:
            print("\nInvalid Input.")
            print("Press any key to try again...")
            getch()
            clear()
