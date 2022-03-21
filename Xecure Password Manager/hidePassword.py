import sys
import getpass
from msvcrt import getch

#Function replaces input text as * in the cmd as the user enters their password. This is used so that the password is
#not displayed to the screen for others to see.
def hidePassword(prompt='\nAccount password: '):
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

def hideRecPassword(prompt='\nRecord password: '):
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
