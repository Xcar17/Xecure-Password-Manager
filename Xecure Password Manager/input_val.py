#Xecure Password Manager
#By Carlos Ocasio

#This module contains all of the input validation functions and rules.

#Function used to validate emails. Emails must contain both @ and . characters.
def validateEmail(email):
    #Variables used for error codes.
    ERROR_CODE, minLen, maxLen, minLenErr, maxLenErr, formatErr = None, 6,35, 1, 2, 3
    email = str(email)

    if minLen > len(email):
        return minLenErr #Return 1 if less than 6 characters.

    if maxLen < len(email):
        return maxLenErr #Return 2 if more than 35 characters.

    #req 2 (contains letters, numbers, symbols).
    alpha = False
    for c in email:
        if c.isalpha():
            alpha = True
            break
    if not alpha:
        return formatErr #Return 3 if no letters are used.

    special = False #Used to ensure @ is used.
    special2 = False #Used to ensure . is used.
    for c in email:
        if c in "@":
            special = True
        if c in ".":
            special2 = True

    #If @ or . not used return error.
    if not special or not special2:
        return formatErr

    return email #If email format correct, return full email string.


#Function used to validate master password.
#Min lenght 8, max length20, must include lowercase, uppercase, number, and special char.
def validatePassword(pwd):
    # Variables used for error codes.
    ERROR_CODE, minLen, maxLen, minLenErr, maxLenErr, formatErr = None, 8,35, 1, 2, 3
    pwd = str(pwd)


    #req 1 (length min and max)
    if minLen > len(pwd):
        return minLenErr #Return 1 if less than 8 characters.

    if maxLen < len(pwd):
        return maxLenErr #Return 2 if more than 35 characters.

    #req 2 (contains letters, numbers, symbols)
    alpha = False
    for c in pwd: #Looks for letters in string.
        if c.isalpha():
            alpha = True
            break
    if not alpha:
        return formatErr #Return 3 if no letters are used.

    hasCap = False
    for c in pwd:
        if c.isupper(): #Looks for uppercase letters.
            hasCap = True
            break
    if not hasCap:
        return formatErr #Returns 3 if no uppercase letters used.


    haslowCap = False
    for c in pwd:
        if c.islower(): #Looks for lowercase letters.
            haslowCap = True
            break
    if not haslowCap:
        return formatErr #Returns 3 if no lowercase letters are used.

    numerical = False
    for c in pwd:
        if c.isnumeric(): #Looks for numbers.
            numerical = True
            break
    if not numerical:
        return formatErr #Returns 3 if no numbers are used.

    special = False
    for c in pwd:
        if c in "~!@#$%^&*_-+='|\(){}[]:;\"\'<>,.?/": #Looks for the symbols listed.
            special = True
            break
    if not special:
        return formatErr #Returns 3 if a symbol is not used.

    else:
        return pwd

#Function that removes leading spaces from input.
def noleadingspace(userIn):
    stripping = str(userIn)
    stripped = str.strip(stripping)
    return stripped

#Function that validates record usernames.
#Usernames should only be at least 3 chars, should have no symbols (no spaces). It should only be letters and numbers.
def validateUsername(name):
    #Variables used for error codes.
    ERROR_CODE, minLen, maxLen, minLenErr, maxLenErr, formatErr = None, 3,35, 1, 2, 3
    name = str(name)

    if minLen > len(name):
        return minLenErr #Return 1 if less than 3 characters.

    if maxLen < len(name):
        return maxLenErr #Return 2 if more than 35 characters.

    #req 2 (contains letters, numbers, symbols)
    alpha = False
    for c in name:
        if c.isalpha(): #Looks for letters in string.
            alpha = True
            break
    if not alpha:
        return formatErr #If no letters used returns 3.

    special = False
    for c in name:
        if c in "~!@#$%^&*_-+=`'|\(){}[]:;\"\'<>,.?/ ": #Looks for these symbols.
            special = True
            break
    if not special:
        return name #If a symbol is not used, returns 3. Else return name passed.

    else:
        return formatErr #Returns 3 if wrong format.


#Function used to validate record names.
#Allow spaces, underscores and periods. min length 3, max length 35.
def validateRecordName(name):
    #Variables needed to display error codes.
    ERROR_CODE, minLen, maxLen, minLenErr, maxLenErr, formatErr = None, 3,35, '1', '2', '3'
    name = str(name)

    if minLen > len(name):
        return minLenErr #Return 1 if less than 3 characters.

    if maxLen < len(name):
        return maxLenErr #Return 2 if more than 35 characters.

    #req 2 (contains letters, numbers, symbols).
    alpha = False
    for c in name:
        if c.isalpha(): #Looks for letters.
            alpha = True
            break
    if not alpha:
        return formatErr #If letters not used returns '1'.

    special = False
    for c in name:
        if c in "~`!@#$%^&*-+='|\(){}[]:;?\"\'<>,/": #Looks for these symbols.
            special = True
            break
    if not special:
        return name #Returns name if a symbol is not present.

    else:
        return formatErr #Returns '3' if wrong format.

#Function used to validate record information.
#checks if the input is alphabetic, checks that the legth is less tha 35
def validateRecordUserPasswordAndEmail(name):
    #Variables needed to display error codes.
    maxLen, maxLenErr, formatErr = 35, 2, 3
    name = str(name)

    alpha = False
    for c in name:
        if c.isalpha(): #Looks for letters.
            alpha = True
            break
    if not alpha:
        return formatErr #Returns 3 if no letters found.

    if maxLen < len(name):
        return maxLenErr #Return 2 if more than 35 characters.

    else:
        return name #Returns entered input.

#Function used to validate record password only. Record password cannot be strict because users already have their
#passwords set most of the time.
def validateRecordPass(psswd):
    #Variables needed to display errors.
    maxLen, maxLenErr = 35, 2
    psswd = str(psswd)

    if maxLen < len(psswd):
        return maxLenErr #Return 2 if more than 35 characters.
    else:
        return psswd #Returns password if no error found.
