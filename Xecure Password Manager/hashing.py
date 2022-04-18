import hashlib #Used to created hashes.

#Function used to create a hash from the password and username.
def combHash(pwd, uname):
    plain_result = ""
    plen = len(pwd)
    ulen = len(uname)

    #Iterating through the lenght of each input to create a hash.
    for i in range(max(plen, ulen)):    #Gets Max of both strings and sets as range
        o1 = ord(pwd[i % len(pwd)])     #Grabs one character of pwd at a time and converts to scii val
        o2 = ord(uname[i % len(uname)]) #Grabs one character of una at a time and converts to scii val
        plain_result += str( (o1 + o2)%95 + 31 ) #Adds results together then result % 95, then adds 31
                                                 #After adding 31 the result will be appended to the plain_result var
                                                 #and this will keep happening until the range has finished

    # Hashing plain_result and adding a salt.
    plain_result_hash= hashlib.pbkdf2_hmac('sha256', plain_result.encode("utf-8"), b'(*!@#s', 823)
    plain_result_hash_hex = plain_result_hash.hex()

    return plain_result_hash_hex
