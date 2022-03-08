#must contain both @ and . characters
def validateEmail(name):
    ERROR_CODE, minLen, maxLen, minLenErr, maxLenErr, formatErr = None, 6,35, 1, 2, 3
    name = str(name)

    if minLen > len(name):
        return minLenErr

    if maxLen < len(name):
        return maxLenErr

    #req 2 (contains letters, numbers, symbols)
    alpha = False
    for c in name:
        if c.isalpha():
            alpha = True
            break
    if not alpha:
        return formatErr

    special = False
    special2 = False
    for c in name:
        if c in "@":
            special = True
        if c in ".":
            special2 = True

    if not special or not special2:
        return formatErr


    return name

#print(validateEmail("@@@@.1"))


#min lenght 8, max length20, must include lowercase, uppercase, number, and special char
def validatePassword(pwd):
    ERROR_CODE, minLen, maxLen, minLenErr, maxLenErr, formatErr = None, 8,35, 1, 2, 3
    pwd = str(pwd)
    #pwd = pwd.strip()

    #req 1 (length min and max)
    if minLen > len(pwd):
        return minLenErr

    if maxLen < len(pwd):
        return maxLenErr

    #req 2 (contains letters, numbers, symbols)
    alpha = False
    for c in pwd:
        if c.isalpha():
            alpha = True
            break
    if not alpha:
        return formatErr

    hasCap = False
    for c in pwd:
        if c.isupper():
            hasCap = True
            break
    if not hasCap:
        return formatErr

    numerical = False
    for c in pwd:
        if c.isnumeric():
            numerical = True
            break
    if not numerical:
        return formatErr

    special = False
    for c in pwd:
        if c in "~!@#$%^&*_-+='|\(){}[]:;\"\'<>,.?/":
            special = True
            break
    if not special:
        return formatErr

    else:
        return pwd


#print(validatePassword("!!!!!!!!!!!!!!!!!!!"))


def noleadingspace(userIn):
    stripping = str(userIn)
    stripped = str.strip(stripping)
    return stripped

#print(validatePassword("Password1!"))



#Usernames should only be at least 3 chars, should have no symbols (no spaces). It should only be letters and numbers.
def validateUsername(name):
    ERROR_CODE, minLen, maxLen, minLenErr, maxLenErr, formatErr = None, 3,35, 1, 2, 3#todo might not need these many vars
    name = str(name)

    if minLen > len(name):
        return minLenErr

    if maxLen < len(name):
        return maxLenErr

    #req 2 (contains letters, numbers, symbols)
    alpha = False
    for c in name:
        if c.isalpha():
            alpha = True
            break
    if not alpha:
        return formatErr

    special = False
    for c in name:
        if c in "~!@#$%^&*_-+=`'|\(){}[]:;\"\'<>,.?/ ":
            special = True
            break
    if not special:
        return name

    else:
        return formatErr

#print(validateUsername("ssdsdwe1"))



#allow spaces, underscores and periods. min length 3,, max length 35
def validateRecordName(name):
    ERROR_CODE, minLen, maxLen, minLenErr, maxLenErr, formatErr = None, 3,35, '1', '2', '3'#todo might not need these many vars
    name = str(name)

    if minLen > len(name):
        return minLenErr

    if maxLen < len(name):
        return maxLenErr

    #req 2 (contains letters, numbers, symbols)
    alpha = False
    for c in name:
        if c.isalpha():
            alpha = True
            break
    if not alpha:
        return formatErr

    special = False
    for c in name:
        if c in "~`!@#$%^&*-+='|\(){}[]:;?\"\'<>,/":
            special = True
            break
    if not special:
        return name

    else:
        return formatErr

#print(validateRecordName(".. a._"))



########################DID NOT USE THIS ONE!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
#validate recordusername: no min length, 20 max length, only special symbols (!@#&), space, numbers
#allow spaces, underscores, hyphen, and periods
def validateRecordUserName(name):
    ERROR_CODE, minLen, maxLen, minLenErr, maxLenErr, formatErr = None, 8,35, 1, 2, 3#todo might not need these many vars
    name = str(name)

    if maxLen < len(name):
        return maxLenErr

    #req 2 (contains letters, numbers, symbols)
    alpha = False
    for c in name:
        if c.isalpha():
            alpha = True
            break
    if not alpha:
        return formatErr


    special = False
    for c in name:
        if c in "~$%^*_-+=`'|\(){}[]:;\"\'<>,.?/":
            special = True
            break
    if not special:
        return name

    else:
        return formatErr

#print(validateRecordUserName("   h!@#&"))



#
def validateRecordPasswordAndEmail(name):
    maxLen, maxLenErr, formatErr = 35, 2, 3 #todo might not need these many vars
    name = str(name)

    alpha = False
    for c in name:
        if c.isalpha():
            alpha = True
            break
    if not alpha:
        return formatErr

    if maxLen < len(name):
        return maxLenErr

    else:
        return name


def validateRecordPass(name):
    maxLen, maxLenErr = 35, 2 #
    name = str(name)

    if maxLen < len(name):
        return maxLenErr

    else:
        return name

#print(validateRecordPasswordAndEmail("paaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"))


