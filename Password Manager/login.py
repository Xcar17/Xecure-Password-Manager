# Written by TilasTech
# Channel: https://www.youtube.com/channel/UC7xQkF7kX2rCz672OVwcCYw
# Video: https://youtu.be/GXZKSk4c9cc
# Hope this helps you out!

def main():
    import hashlib
    from msvcrt import getch
    import os
    import getpass
    import sys

    def mpass(prompt='Password: '):
        if sys.stdin is not sys.__stdin__:
            pwd = getpass.getpass(prompt)
            return pwd
        else:
            pwd = ""
            sys.stdout.write(prompt)
            sys.stdout.flush()
            while True:
                key = ord(getch())
                if key == 13:
                    sys.stdout.write('\n')
                    return pwd
                    break

                if key == 8:
                    if len(pwd) > 0:
                        sys.stdout.write('\b' + ' ' + '\b')
                        sys.stdout.flush()
                        pwd = pwd[:-1]
                else:
                    char = chr(key)
                    sys.stdout.write('*')
                    sys.stdout.flush()
                    pwd = pwd + char


    #Called when a new user wants to register
    #Checks inside the database to see if the username entered is already in the database
    #If the username is already in the database the user must use another name to register
    #Returns true if username is taken and false if it's available
    def check(file, string):
        with open(file, 'r') as read:
            for line in read:
                if string in line:
                    return True
        return False




    def grabpass():
        global ptc
        writef = open("accdatabase", "r")
        cl = lf + 1
        ltr = [cl]
        for position, line in enumerate(writef):
            if position in ltr:
                ptc = line




    def checklogin(file, string):
        global lf
        with open(file, 'r') as read:
            for (lf, line) in enumerate(read):
                if string in line:
                    return True
        return False



    def clear():
        os.system("cls")







    #Program main starts here
    print("Welcome to Xecure Password Manager\n")
    os.system("title Xecure Password Manager")
    while True:
        print("What would you like to do?\n")
        print("[1] Register new user.")
        print("[2] View user database.")
        print("[3] Wipe user database.")
        print("[4] Login as user.")
        print("[5] Exit\n")
        a = input("Selection: ")
        if a == "1":
            while True:
                a = input("Username: ")
                h = hashlib.pbkdf2_hmac('sha256', a.encode("utf-8"), b'(*!@#s', 823)
                newuser = h.hex()
                if check('accdatabase', newuser):
                    print("User already exists!")
                else:
                    break
            b = mpass()
            h = hashlib.pbkdf2_hmac('sha256', b.encode("utf-8"), b'*@#d2', 182)
            newpass = h.hex()
            users = open("accdatabase", "a")
            users.write("Username: " + newuser + "\nPassword: " + newpass + "\n\n")
            users.close()
            clear()
            print("The following has been saved to the user database...\n")
            print("Username: " + newuser + "\nPassword: " + newpass + "\n")
            print("Press any key to continue...")
            getch()
            clear()
        elif a == "2":
            if os.path.getsize("accdatabase") == 0:
                clear()
                print("Database is empty!\n")
            else:
                clear()
                print("User Database:\n")
                reader = open("accdatabase", "r")
                print(reader.read())
                reader.close()
                print("Press any key to continue...")
                getch()
                clear()
        elif a == "3":
            if os.path.getsize("accdatabase") == 0:
                clear()
                print("Database is already empty!\n")
            else:
                while True:
                    a = input("Are you sure you want to wipe the user database [y/n]? ")
                    if a == "y":
                        datab = open("accdatabase", "w")
                        datab.write("")
                        datab.close()
                        clear()
                        print("Database wiped!\n")
                        break
                    elif a == "n":
                        clear()
                        print("Database will not be wiped!\n")
                        break
                    else:
                        print("Invalid selection.")
        elif a == "4":
            if os.path.getsize("accdatabase") == 0:
                clear()
                print("Database is empty!\n")
            else:
                count = 5
                while True:
                    a = input("Username: ")
                    h = hashlib.pbkdf2_hmac('sha256', a.encode("utf-8"), b'(*!@#s', 823)
                    userinput = h.hex()
                    if checklogin('accdatabase', userinput):
                        print("Welcome " + a + "!\n")
                        break
                    else:
                        count -= 1
                        print("Invalid username.")
                        if count == 1:
                            print("The application will close after another failed login attempt")
                        if count == 0:
                            exit(0)

                while True:
                    b = mpass()
                    h = hashlib.pbkdf2_hmac('sha256', b.encode("utf-8"), b'*@#d2', 182)
                    passinput = h.hex()
                    grabpass()
                    ptct = ptc.replace("Password: ", '')
                    ptcr = ptct.rstrip("\n")
                    if passinput == ptcr:
                        currentuser = a
                        clear()
                        print("Successfully logged in as " + currentuser + "!\n")
                        usrtitle = ("title Secure Login System (logged in as " + currentuser + ")")
                        os.system(usrtitle)
                        break
                    else:
                        count -= 1
                        print("Invalid Password.")
                        if count == 1:
                            print("The application will close after another failed login attempt")
                        if count == 0:
                            exit(0)
        elif a == "5":
            print("Press any key to exit...")
            getch()
            exit(0)
        else:
            clear()
            print("Invalid Selection!\n")


if __name__ == '__main__':
    main()