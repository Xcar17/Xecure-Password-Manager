#Xecure Password Manager
#By Carlos Ocasio

#This module is uses the random library to generate random passwords. This function will be used to create unique
#passwords for user records. It is also used to send a verification code to the user in the event that they need to
#verify their email/account.

import random #Used to generate random passwords.

#This will be used as the pool of characters to used for the random password generator
GENKEY = "qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM1234567890!&@#%$?" #Pool of characters for code.
GENKEYLONG = "qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM1234567890!&@#%$?*=+-_()" #Pool of chars for password.
PASSLEN = 10 #Determines the length of the password'
PASSLENLONG = 15 #Determines the length of the password'

def generate_password():
    password = ''#Declaring my password variable that will hold the randomly generated pswd

    #Loop is determined by the password leght. Each itertion of the loop will add a random character from the GENKEY var
    #and this character will be added to the password until the pasworld lenght has been met
    for x in range(0, PASSLEN):
        generating_pswd = random.choice(GENKEY)
        password = password + generating_pswd
    return  password

def generate_password_long():
    password = ''#Declaring my password variable that will hold the randomly generated pswd

    #Loop is determined by the password leght. Each itertion of the loop will add a random character from the GENKEY var
    #and this character will be added to the password until the pasworld lenght has been met
    for x in range(0, PASSLENLONG):
        generating_pswd = random.choice(GENKEYLONG)
        password = password + generating_pswd
    return  password
