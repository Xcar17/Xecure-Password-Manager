#Xecure Password Manager
#By Carlos Ocasio

#This module is used to hide the input entered to the screen. This is used to hide the password as the user types it.

import sys #Used to hide the password in the command screen.
import getpass #Used to display and prompt a message.
from msvcrt import getch #Used to prevent the command screen from moving to the next screen.

#Function replaces input text as '*' in the cmd as the user enters their password. This is used so that the password is
#not displayed to the screen for others to see.
def hidePassword(prompt='\nAccount password: '):
    if sys.stdin is not sys.__stdin__:
        usrPsswd = getpass.getpass(prompt) #Asking for the user input
        return usrPsswd #Returns password.
    else:
        usrPsswd = ""
        sys.stdout.write(prompt) #Writing to prompt
        sys.stdout.flush()
        while True: #Writing new line.
            myKey = ord(getch())
            if myKey == 13:
                sys.stdout.write('\n')
                return usrPsswd
            if myKey == 8:
                if len(usrPsswd) > 0:
                    sys.stdout.write('\b' + ' ' + '\b')
                    sys.stdout.flush()
                    usrPsswd = usrPsswd[:-1]
            else:   #Ensuring the password is not displayed to the screen.
                char = chr(myKey)
                sys.stdout.write('*')
                sys.stdout.flush()
                usrPsswd = usrPsswd + char

#Function serves a similar purpose to the function above, but it is used for hiding passwords for records.
def hideRecPassword(prompt='\nRecord password: '):
    if sys.stdin is not sys.__stdin__:
        usrPsswd = getpass.getpass(prompt) #Returns password.
        return usrPsswd #Return user password.
    else:
        usrPsswd = ""
        sys.stdout.write(prompt)    #Writing & flushing prompt input
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
                sys.stdout.write('*')   #Writing * instead of user input.
                sys.stdout.flush()
                usrPsswd = usrPsswd + char
