from database import cursor, db
from mysql.connector import errorcode
from cryptography.fernet import Fernet
import mysql.connector

DB_NAME = "XecuredDB"

def use_database(DB_NAME):
    cursor.execute("USE {}".format(DB_NAME))
    #print("Welcome to the database " + DB_NAME )


def create_database():
    cursor.execute("CREATE DATABASE IF NOT EXISTS {} DEFAULT CHARACTER SET 'utf8'".format(DB_NAME))
    db.commit()
    #print("Database {} created!".format(DB_NAME))
    use_database(DB_NAME)

create_database()#creates a database with the name entered

TABLES = {}

TABLES['test'] = (
    "CREATE TABLE IF NOT EXISTS Registered_Users (id int(11) NOT NULL AUTO_INCREMENT,"
    " Account_Name varchar(250) NOT NULL, Email varchar(250) NOT NULL, PRIMARY KEY (id))"
)


def create_tables():
    cursor.execute("USE {}".format(DB_NAME))
    for table_name in TABLES:
        table_description = TABLES[table_name]
        try:
            #print("Creating table ({}) ".format(table_name), end="")
            cursor.execute(table_description)
        except mysql.connector.Error as err:
            #if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
               #print("Table Already Exists")
            #else:
                print(err.msg)
    db.commit()

create_tables()


def add_log(Account_Name, Email):
    sql = ("INSERT INTO Registered_Users(Account_Name, Email) VALUES (%s, %s)")
    cursor.execute(sql, (Account_Name, Email))
    db.commit()
    log_id = cursor.lastrowid
    #print ("Added log {}".format(log_id))


def prompt_user():
    AccountName = input("What is the name of the account: ")
    usrEmail = input("What is the user email for this account : ")
    add_log(AccountName, usrEmail)
#prompt_user()


TABLES2 = {}

TABLES2['test'] = (
    "CREATE TABLE IF NOT EXISTS User_Records ("
    " recordId int(11) NOT NULL AUTO_INCREMENT, userId int, FOREIGN KEY(userId) REFERENCES Registered_Users(id),"
    " Record_Name varchar(250) NOT NULL, Email varchar(250) NOT NULL, User_Name varchar(250), "
    "Account_Password varchar(250) NOT NULL, PRIMARY KEY (recordId))"
)


def create_tables2():
    cursor.execute("USE {}".format(DB_NAME))

    for table_name in TABLES2:
        table_description = TABLES2[table_name]
        try:
            #print("Creating table ({}) ".format(table_name), end="")
            cursor.execute(table_description)
        except mysql.connector.Error as err:
            #if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
                #print("Table Already Exists")
            #else:
                print(err.msg)
    db.commit()


create_tables2()


def add_log2(userId, Record_Name, Email, User_Name, Account_Password):
    sql = ("INSERT INTO User_Records(userId, Record_Name, Email, User_Name, Account_Password) VALUES (%s, %s, %s, %s, %s)")
    cursor.execute(sql, (userId, Record_Name, Email, User_Name, Account_Password))
    db.commit()
    log_id = cursor.lastrowid
    #print ("Added log {}".format(log_id))


def prompt_user2():
    id =  input("What is the userid for this account : ")
    recordName = input("What is the name of the account: ")
    recordEmail = input("What is the user email for this account : ")
    recordUserName = input("What is the user name for this account : ")
    recordPassword = input("What is the password for this account : ")
    add_log2(id, recordName, recordEmail, recordUserName, recordPassword)

#prompt_user2()


##################################################################

TABLES3 = {}

TABLES3['SecTab'] = (
    "CREATE TABLE IF NOT EXISTS Rec_Sec ("
    " recordId int(11) NOT NULL AUTO_INCREMENT, userId int, FOREIGN KEY(userId) REFERENCES Registered_Users(id),"
    " Answer1 varchar(250) NOT NULL, Answer2 varchar(250) NOT NULL, Answer3 varchar(250) NOT NULL, "
    "Answer4 varchar(250) NOT NULL,  Answer5 varchar(250) NOT NULL,PRIMARY KEY (recordId))"
)


def create_tables3():
    cursor.execute("USE {}".format(DB_NAME))

    for table_name in TABLES3:
        table_description = TABLES3[table_name]
        try:
            #print("Creating table ({}) ".format(table_name), end="")
            cursor.execute(table_description)
        except mysql.connector.Error as err:
            #if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
                #print("Table Already Exists")
            #else:
                print(err.msg)
    db.commit()


create_tables3()



def add_log3(userId, Answer1, Answer2, Answer3, Answer4, Answer5):
    sql = ("INSERT INTO Rec_Sec(userId, Answer1, Answer2, Answer3, Answer4, Answer5) VALUES (%s, %s, %s, %s, %s, %s)")
    cursor.execute(sql, (userId, Answer1, Answer2, Answer3, Answer4, Answer5))
    db.commit()
    log_id = cursor.lastrowid
    #print ("Added log {}".format(log_id))


#################################################Setup Ends Here##################################################################################################

def update_record_name(newRecord, id, rcName):
    oldCiphRecName = fetch_cipher_by_id_gen(id, rcName, "Record_Name") #Contains current record name
    newRecord, rcName = encryptAll(id, [newRecord, rcName]) #encrypts both the old and new recordnames to compare
    #try:
    sql = ("UPDATE User_Records SET Record_Name = %s WHERE userId = %s AND Record_Name = %s")
    cursor.execute(sql, (newRecord, id, oldCiphRecName)) #uses the the current/old record name and Id, to change the record name to the newly encrypted newRecord
    db.commit()
    #except:
    #    print("THAT RECEORD DOESN'T EXIST!")
    #print("Log updated!")


def update_record_email(newEmail, id, recName):
    oldCiphRecEmail = fetch_cipher_by_id_gen(id, recName, "Email")
    newCipherEmail = encryptAll(id, [newEmail])[0]
    #try:
    sql = ("UPDATE User_Records SET Email = %s WHERE userId = %s AND Email = %s")
    cursor.execute(sql, (newCipherEmail, id, oldCiphRecEmail))
    db.commit()
    #print("Log updated!")


def update_record_username(text, id, rcName):
    oldCiphRecEmail = fetch_cipher_by_id_gen(id, rcName, "User_Name")
    newCipherEmail = encryptAll(id, [text])[0]
    #try:
    sql = ("UPDATE User_Records SET User_Name = %s WHERE userId = %s AND User_Name = %s")
    cursor.execute(sql, (newCipherEmail, id, oldCiphRecEmail))
    db.commit()
    #print("Log updated!")


def update_record_password(text, id, rcName):
    oldCiphRecEmail = fetch_cipher_by_id_gen(id, rcName, "Account_Password")
    newCipherEmail = encryptAll(id, [text])[0]
    #try:
    sql = ("UPDATE User_Records SET Account_Password = %s WHERE userId = %s AND Account_Password = %s")
    cursor.execute(sql, (newCipherEmail, id, oldCiphRecEmail))
    db.commit()
    #print("Log updated!")


def delete_record(text, id):
    oldCiphRecName = fetch_cipher_by_id_gen(id, text, "Record_Name") #Contains current record name
    sql = ("DELETE FROM User_Records WHERE userId = %s AND Record_Name = %s")
    cursor.execute(sql, (id, oldCiphRecName))
    db.commit()

def update_master_email(inputEmail, id):
    encryptedEmail = encrypt(id, inputEmail)
    #todo finish updating email on DB
    sql = ("UPDATE Registered_Users SET Email = %s WHERE Id = %s")
    cursor.execute(sql, (encryptedEmail, id))
    db.commit()
    #print("Log updated!")

def delete_all_records(id):
    sql = ("DELETE FROM User_Records WHERE userId = %s")
    cursor.execute(sql, (id,))
    db.commit()
    print("\nAll records have been deleted!")



####################################################################################################todo This is where my tutoring code starts####################################################################################

# encrypt a given plain_text
def encrypt( id,  plain_text):
    if type(id) != str:
        id = str(id)
    if type(plain_text) != str:
        plain_text = str(plain_text)

    #make sure id is not already present in file
    key = retrieveKey(id)

    if key is None:
        #create the key and fernet object to be used for encryption process
        key = Fernet.generate_key()
        #open a file with name *id*
        f = open("database.txt", "a") # open file in append mode

        # write the PLAIN TEXT key into the file
        f.write(id + "\t" + key.decode() + "\n")
        f.close()

    cipher_suite = Fernet(key)

    #convert to bytes
    plain_bytes_text = bytes(plain_text,'ascii')

    # now generate the cipher from the "plain bytes text"
    cipher_text = cipher_suite.encrypt(plain_bytes_text)

    # return the bytes (cipher text)
    return cipher_text.decode()

def retrieveKey(id):
    key = None
    if type(id) != str:
        id = str(id)
    try:
        f = open("database.txt", "r")

        # read the plain text key from the file

        database_lines = f.readlines()
        for record in database_lines:
            record_fields = record.split('\t')
            if record_fields[0] == id:
                key = record_fields[1].strip("\n")
                key = key.encode()
        f.close()
    except:
        print("database.txt not found")
    return key

def decrypt(id, cipher_text):
    #retireve the key and create fernet objct

    key = retrieveKey(id)
    if key is None:
        print("ERROR!  ID NOT IN DATABASE.TXT")
        return

    cipher_suite = Fernet(key)

    # get  the "plain bytes text" from the cipher text
    plain_bytes_text_2 = cipher_suite.decrypt(cipher_text.encode())

    # finally get back the plain text from the plain bytes text
    plain_text_2 = str(plain_bytes_text_2)

    #return the decrypted plain text
    return plain_bytes_text_2.decode()


def encryptAll(id, list_2_enc):
    enc_list = []
    for ele in list_2_enc:
        enc_list.append(encrypt(id, ele))

    return tuple(enc_list)



################################################### DECRYPT/ENCRYPT ###################################################################
def printAllRecsByID(id, nameOnly = False):
    # todo implement code that displays "no records found for this account"

    if type(id) != int:
        id = int(id)

    sql = ("select * from User_Records ")
    cursor.execute(sql )
    results = cursor.fetchall()

    if nameOnly:
        print("Record Names:\n")
    for rec in results:
        if rec[1] == id:
            usrID = rec[1]
            recID = rec[0]
            recName = decrypt(usrID, rec[2])
            email = decrypt(usrID, rec[3])
            usr_name  = decrypt(usrID, rec[4])
            acct_pass  = decrypt(usrID, rec[5])
            if not nameOnly:
                print(f"Record Name:{recName}\nAccount Email:{email}\nUser Name:{usr_name}\nAccount Password:{acct_pass}\n\n--------------------------\n")
            else:
                print(f"\t-{recName}")



def adding_new_enc_record(userId, recordName, recordEmail, recordUser, recordpassword):
    userId = int(userId)
    Record_Name = recordName
    Email = recordEmail
    User_Name = recordUser
    Account_Password = recordpassword
    Record_Name, Email, User_Name, Account_Password =  encryptAll(userId, [ Record_Name, Email, User_Name, Account_Password])
    add_log2(userId, Record_Name, Email, User_Name, Account_Password)

def adding_new_enc_sec_answers(userId, Answer1, Answer2, Answer3, Answer4, Answer5):
    userId = int(userId)
    encAnswer1, encAnswer2, encAnswer3, encAnswer4, encAnswer5 = encryptAll(userId, [ Answer1, Answer2, Answer3, Answer4, Answer5])
    add_log3(userId, encAnswer1, encAnswer2, encAnswer3, encAnswer4, encAnswer5)



def fetch_rec_by_id_gen(id, gen_value, gen_cat):
    # try:
    sql0 = ("select * from INFORMATION_SCHEMA.COLUMNS where TABLE_NAME='User_Records' ")
    cursor.execute(sql0)
    columns = cursor.fetchall()
    col_i = [tup[4] for tup in columns if tup[1] == "xecureddb" and tup[2] == "user_records" and tup[3] == gen_cat][0] - 1
    sql = ("SELECT * FROM User_Records WHERE userId = %s")
    cursor.execute(sql, (id,))
    results = cursor.fetchall()
    j = 0
    for rec in results:
        if decrypt(id, rec[col_i]) == gen_value:
            # now decrypt everything else
            req_rec = [rec[0], rec[1] ]
            for i in range(2, len(rec)):
                req_rec.append(decrypt(id, rec[i]))
            return req_rec
    #print("Couldn't find record matching id and name")
    return "Record not Found..."

def fetch_cipher_by_id_gen(id, recName, gen_cat):
    # try:
    sql0 = ("select * from INFORMATION_SCHEMA.COLUMNS where TABLE_NAME='User_Records' ")
    cursor.execute(sql0)
    columns = cursor.fetchall()
    ret_i = [tup[4] for tup in columns if tup[1] == "xecureddb" and tup[2] == "user_records" and tup[3] == gen_cat][0] - 1
    name_i = col_i = [tup[4] for tup in columns if tup[1] == "xecureddb" and tup[2] == "user_records" and tup[3] == "Record_Name"][0] - 1

    sql = ("SELECT * FROM User_Records WHERE userId = %s")
    cursor.execute(sql, (id,))
    results = cursor.fetchall()
    j = 0
    for rec in results:
        if decrypt(id, rec[name_i]) == recName:
            return rec[ret_i]
    print("Couldn't find record matching id and " + gen_cat)
    return None

# gonna use this to fetch the next user id
def next_user_id():
    #try:
    #sql = ("SELECT * FROM User_Records WHERE userId = " + str(id) )
    sql = ("SELECT * FROM Registered_Users" )
    cursor.execute(sql)
    results = cursor.fetchall()
    if len(results) == 0:
        return 1

    lastRec = results[-1]
    return lastRec[0] + 1