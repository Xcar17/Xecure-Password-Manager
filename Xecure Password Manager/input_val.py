

def validatePassword(pwd):
    ERROR_CODE, minLen, lenErr, formatErr = None, 8, 0, 1
    pwd = str(pwd)
    pwd = pwd.strip()

    #req 1 (length)
    if minLen > len(pwd):
        return lenErr
    #req 2 (contains letters, numbers, symbols)
    alpha = False
    for c in pwd:
        if c.isalpha():
            alpha = True
            break
    if not alpha:
        return

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
        if c in "!@#$%^&*()":
            special = True
            break
    if not special:
        return formatErr

