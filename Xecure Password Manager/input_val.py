

def validatePassword(pwd):
    ERROR_CODE, minLen, maxLen, minLenErr, maxLenErr, formatErr = None, 8,20, 1, 2, 3
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


#Need symbols in order to have a strong password

#Maybe Limit complicated record names

#In records emails and password should have lesser password restrictions

# Use for record names:         !?@.#&
# Dont use:    ;-'*=\+|:()



#Usernames should only be at least 3 chars, should have no symbols (no spaces). It should only be letters and numbers.
def validateUsername(name):
    ERROR_CODE, minLen, maxLen, minLenErr, maxLenErr, formatErr = None, 8,20, 1, 2, 3#todo might not need these many vars
    name = str(name)

    special = False
    for c in name:
        if c in "~!@#$%^&*_-+=`'|\(){}[]:;\"\'<>,.?/ ":
            special = True
            break
    if not special:
        return name

    else:
        return formatErr

#print(validateUsername("Carlos"))

#allow spaces, underscores and periods
def validateRecordName(name):
    ERROR_CODE, minLen, maxLen, minLenErr, maxLenErr, formatErr = None, 8,20, 1, 2, 3#todo might not need these many vars
    name = str(name)

    special = False
    for c in name:
        if c in "~`!@#$%^&*-+='|\(){}[]:;?\"\'<>,/":
            special = True
            break
    if not special:
        return name

    else:
        return formatErr

print(validateRecordName("Carlos_Test.123. Extra"))

################ALL OF THESE NEED TO BE LESS STRICT

#validate recordusername: 3 letters, only special symbols, numbers
#allow spaces, underscores, hyphen, and periods
def validateRecordUserName(name):
    ERROR_CODE, minLen, maxLen, minLenErr, maxLenErr, formatErr = None, 8,20, 1, 2, 3#todo might not need these many vars
    name = str(name)

    special = False
    for c in name:
        if c in "~`!@#$%^&*+='|\(){}[]:;?\"\'<>,/":
            special = True
            break
    if not special:
        return name

    else:
        return formatErr

print(validateRecordUserName("Test this_12.hi-bye"))


#validate recordpassword
#validate recordemail