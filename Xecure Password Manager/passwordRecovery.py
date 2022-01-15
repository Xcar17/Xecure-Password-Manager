from database import cursor, db
from mysql.connector import errorcode
from cryptography.fernet import Fernet
import mysql.connector
from dbsetup import decrypt, update_master_email
from random_pwd_generator import generate_password
import smtplib
import hashlib
from msvcrt import getch
from clear import myExit, clear

def sendEmail(email, code, retreival=None):
    # creates SMTP session
    s = smtplib.SMTP('smtp.gmail.com', 587)

    # start TLS for security
    s.starttls()

    # Authentication
    s.login("xecureddb@gmail.com", "Xecured123")

    explanation = "\nPlease go back to the App and enter this code when prompted in order to set a new password:\n"
    if retreival is not None:
        explanation = f"\nYour {retreival} is:\n"

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

def update_master_password():
    email = input("Please enter the email associated with your account:")
    if verifyEmail(email):
        #generate the code and email it to user
        code = generate_password()
        sendEmail(email, code)
        answer = input("Please enter the code that was just sent to the email: " + email + "\n")
        if code == answer:

            hashEmail = hashlib.pbkdf2_hmac('sha256', email.encode("utf-8"), b'&%$#f^',
                                            182)  # todo implement random salt test
            newEmail = hashEmail.hex()

            inputPass = input("Please enter new Password")
            newPassword = hashlib.pbkdf2_hmac('sha256', inputPass.encode("utf-8"), b'*@#d2',
                                            182).hex()
            #update password in acc databae
            updateAcctPass('accdatabase', newEmail, newPassword)
            print("Password has been updated!")


        else:
            print('Code does not match')

    else:
        print(f"Email: {email} was not found.")

    print("\nPress any key to go back...")
    getch()
    clear()


def changeMasterEmail(id=None): #':+()6\\zx!illp}}(N~'
    email = input("Please enter the email associated with your account:")
    if verifyEmail(email):
        #generate the code and email it to user
        code = generate_password()
        #code = '+()6\\zx!illp}}(N~' #test code to see if it breaks. found that : breaks emails
        sendEmail(email, code)
        answer = input("Please enter the code that was just sent to the email: " + email + "\n")
        if code == answer:
            print("Recovered!!  Here is where we would redirect to updating email ")

            hashEmail = hashlib.pbkdf2_hmac('sha256', email.encode("utf-8"), b'&%$#f^',
                                            182).hex()  # todo implement random salt test
            #newEmail = hashEmail.hex()

            inputEmail = input("Pleae enter new Email")
            newEmail = hashlib.pbkdf2_hmac('sha256', inputEmail.encode("utf-8"), b'&%$#f^',
                                            182).hex()
            #update password in acc databae
            updateAcctPass('accdatabase', hashEmail, newEmail, False)

            print("Email has been updated to " + inputEmail)
            if id is not None:
                update_master_email(inputEmail, id)
                return False
        else:
            print('Code does not match')

    else:
        print(f"Email: {email} was not found.")

def retrieveUsername(email):
    # try:
    sql = ("select * from Registered_Users ")
    cursor.execute(sql )
    results = cursor.fetchall()

    for rec in results:
        if decrypt(rec[0], rec[2]) == email:
            sendEmail(email, decrypt(rec[0], rec[1]), "username")
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

def verifyIDByName(usrName):
    # try:
    sql = ("select * from Registered_Users ")
    cursor.execute(sql )
    results = cursor.fetchall()

    for rec in results:
        if decrypt(rec[0], rec[1]) == usrName:
            return rec[0]
    return False

def verifyIDByEmail(usrName):
    # try:
    sql = ("select * from Registered_Users ")
    cursor.execute(sql )
    results = cursor.fetchall()

    for rec in results:
        if decrypt(rec[0], rec[2]) == usrName:
            return rec[0]
    return False

def usernameRecovery():
    email = input("Please enter the email associated with your account:")
    if verifyEmail(email):
        #generate the code and email it to user
        #code = generate_password()
        retrieveUsername(email)
        print("Username has been sent to the Email associated with the account.")
    else:
        print(f"Email: {email} was not found.")

    print("\nPress any key to go back...")
    getch()
    clear()


def idRecovery():
    email = input("Please enter the email associated with your account:")
    if verifyEmail(email):
        #generate the code and email it to user
        #code = generate_password()
        retrieveID(email)
        print("ID has been sent to the Email associated with the account.")
    else:
        print(f"Email: {email} was not found.")

    print("\nPress any key to go back...")
    getch()
    clear()

print(verifyIDByName("Xecured"))
print(verifyIDByEmail("xecureddb@gmail.com"))

#if __name__ == "__main__":

