import mysql.connector
from cryptography.fernet import Fernet

# construct the cipher suite
# we will use this to construct and deconstruct
#key = Fernet.generate_key()
#cipher_suite = Fernet(key)

# encrypt a given plain_text
def encrypt( id,  plain_text):
    #create the key and fernet object to be used for encryption process
    key = Fernet.generate_key()

    #open a file with name *id*
    f = open(id + ".txt", "w")

    # write the PLAIN TEXT key into the file
    f.write(key.decode())
    f.close()
    cipher_suite = Fernet(key)

    #convert to bytes
    plain_bytes_text = bytes(plain_text,'ascii')

    # now generate the cipher from the "plain bytes text"
    cipher_text = cipher_suite.encrypt(plain_bytes_text)

    # return the bytes (cipher text)
    return cipher_text.decode()


def decrypt(id, cipher_text):
    #retireve the key and create fernet objct
    f = open(id + ".txt", "r")

    #read the plain text key from the file
    key = f.read()
    key = key.encode()

    cipher_suite = Fernet(key)

    # get  the "plain bytes text" from the cipher text
    plain_bytes_text_2 = cipher_suite.decrypt(cipher_text.encode())

    # finally get back the plain text from the plain bytes text
    plain_text_2 = str(plain_bytes_text_2)

    #return the decrypted plain text
    return plain_bytes_text_2.decode()

#myTest = encrypt("test")
# send to databae , then tretireve





# getting the values from the database

mydb = mysql.connector.connect (
    host ="localhost",
    user="root",
    password="12345",
    database = "students_db"
)

# fetching the data
cursor = mydb.cursor()

#
insert_sql = "INSERT INTO students (name, email, password) VALUES "
name = "bobbyyyyyy"
email = "Siva.Jastfesfsdfdsfhi@ymail.com"
pwd = "Random"

#insert_sql = insert_sql + '("' + name + '","' + email + '","' + encrypt(name, pwd) + '")'
#print (insert_sql)
#cursor.execute(insert_sql)
#mydb.commit()


#result = cursor.fetchall()
insert_sql = "Select name, password From students"
cursor.execute(insert_sql)
records = cursor.fetchall()
for record in records:
    #print(record, type(record))
    if record[0] == name:
        print(record[1], decrypt(name, record[1]))
#print(cursor.fetchall())




#print(decrypt(myTest))