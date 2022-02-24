import hashlib

def combHash(pwd, uname):
    plain_result = ""
    plen = len(pwd)
    ulen = len(uname)
    for i in range(max(plen, ulen)):
        o1 = ord(pwd[i % len(pwd)])
        o2 = ord(uname[i % len(uname)])
        plain_result += str( (o1 + o2)%95 + 31 )

    # now hash plain_result
    plain_result_hash= hashlib.pbkdf2_hmac('sha256', plain_result.encode("utf-8"), b'(*!@#s', 823)
    plain_result_hash_hex = plain_result_hash.hex()

    return plain_result_hash_hex

