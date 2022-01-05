from database import cursor, db
from mysql.connector import errorcode
from cryptography.fernet import Fernet
import mysql.connector
from dbsetup import decrypt
from random_pwd_generator import generate_password
from mainMenu import checkStringDatabase
import smtplib
import hashlib

def sendEmail(email, code):
    # creates SMTP session
    s = smtplib.SMTP('smtp.gmail.com', 587)

    # start TLS for security
    s.starttls()

    # Authentication
    s.login("xecureddb@gmail.com", "Xecured123")

    explanation = "Please go back to the App and enter this code when prompted in order to set a new password:\n"

    # sending the mail
    s.sendmail("sender_email_id", email, explanation + code)

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

def updateAcctPass(acctDataFile, newEmail, newPassword):
    adf_r = open(acctDataFile, 'r')
    dataLines = adf_r.readlines()
    adf_r.close()

    adf_w = open(acctDataFile, 'w')
    modify = 0
    for line in dataLines:
        if modify > 0:
            modify += 1

        if newEmail in line:
            modify = 1
        if modify < 3:
            adf_w.write(line)
        else:
            adf_w.write(newPassword)
            print("Writing new password: " + newPassword)
            modify = 0
    adf_w.close()

def passwordRecovery():
    email = input("Please enter the email associated with your account:")
    if verifyEmail(email):
        #generate the code and email it to user
        code = generate_password()
        sendEmail(email, code)
        answer = input("Please enter the code that was just sent to the email: " + email + "\n")
        if code == answer:
            print("Recovered!!  Here is where we would redirect to updating password code ")

            #todo implement code that finds the value of our email variable in the accdatabase and then replaces the password with a new one
            hashEmail = hashlib.pbkdf2_hmac('sha256', email.encode("utf-8"), b'&%$#f^',
                                            182)  # todo implement random salt test
            newEmail = hashEmail.hex()

            inputPass = input("Pleae enter new Password")
            newPassword = hashlib.pbkdf2_hmac('sha256', inputPass.encode("utf-8"), b'*@#d2',
                                            182).hex()
            #update password in acc databae
            updateAcctPass('accdatabase', newEmail, newPassword)

            #if checkStringDatabase('accdatabase', newEmail):
            #    print('The email is in the database')

            #else:
            #    print('The email is not in the database')



    else:
        print(f"Email: {email} does not exist")


#todo implement function like passwordRecovery() that uses the email to find the username in accdatabase (after the email verification process)


if __name__ == "__main__":
    passwordRecovery()