# Xecure Password Manager
# By Carlos Ocasio

#This module contains all of the SQL queries used to communicate with the database. Prepared statements where used to
#prevent users from making their own statements.

from database import cursor, db #Used to connect to the database.
from mysql.connector import errorcode #Used to connect to the database.
from cryptography.fernet import Fernet #Used to encrypt.
import mysql.connector #Used to connect to database.

###################################################MAKE IT xecureddb########################################
DB_NAME = "xecureddb" #This will be the name of the database.

#This code will tell the program what database to use.
def use_database(DB_NAME):
    cursor.execute("USE {}".format(DB_NAME))

#This function will be used to create the database. It checks to see if the database has been created,
# if not it will create it
def create_database():
    cursor.execute("CREATE DATABASE IF NOT EXISTS {} DEFAULT CHARACTER SET 'utf8'".format(DB_NAME))
    db.commit()
    use_database(DB_NAME)

create_database()#creates a database with the name entered

TABLES = {} #Used to contain the queries to create tables.

#This variable will contain the query to create the registered users table. This table contains all of the users that
# have registered an account.
TABLES['test'] = (
    "CREATE TABLE IF NOT EXISTS Registered_Users (id varchar(250),"
    " Account_Name varchar(250) NOT NULL, Email varchar(250) NOT NULL, PRIMARY KEY (id))"
)

#This function will use the TABLES var to create the registered users table.
def create_tables():
    cursor.execute("USE {}".format(DB_NAME))
    for table_name in TABLES:
        table_description = TABLES[table_name]
        try:
            cursor.execute(table_description)
        except mysql.connector.Error as err:
                print(err.msg)
    db.commit()
create_tables()

#This function is used to add a log into the registered users database.
def add_log(id, Account_Name, Email):
    sql = ("INSERT INTO Registered_Users(id, Account_Name, Email) VALUES (%s, %s, %s)")
    cursor.execute(sql, (id, Account_Name, Email))
    db.commit()
    log_id = cursor.lastrowid

#Tables2 will contain the query to create the user records table.
TABLES2 = {}

#Contains query that creates the user records table. This will contain all the record information from every user.
TABLES2['test'] = (
    "CREATE TABLE IF NOT EXISTS User_Records ("
    " recordId int(11) NOT NULL AUTO_INCREMENT, userId varchar(250), FOREIGN KEY(userId) REFERENCES"
    " Registered_Users(id) ON UPDATE CASCADE,"
    " Record_Name varchar(250) NOT NULL, Email varchar(250) NOT NULL, User_Name varchar(250), "
    "Account_Password varchar(250) NOT NULL, PRIMARY KEY (recordId)"
    ", UNIQUE KEY `Unique Records` (`userId`,`Record_Name`))"
)

#This function creates the user records table.
def create_tables2():
    cursor.execute("USE {}".format(DB_NAME))
    for table_name in TABLES2:
        table_description = TABLES2[table_name]
        try:
            cursor.execute(table_description)
        except mysql.connector.Error as err:
                print(err.msg)
    db.commit()
    sql = "ALTER TABLE user_records AUTO_INCREMENT=100000;"#Record id will start at 100000
    cursor.execute(sql)
    db.commit()
create_tables2()

#This function is used to add a log into the user records database.
def add_log2(userId, Record_Name, Email, User_Name, Account_Password):
    sql = ("INSERT INTO User_Records(userId, Record_Name, Email, User_Name, Account_Password)"
           " VALUES (%s, %s, %s, %s, %s)")
    cursor.execute(sql, (userId, Record_Name, Email, User_Name, Account_Password))
    db.commit()
    log_id = cursor.lastrowid

#################################################Setup Ends Here######################################################
#Function used to update the name of a record.
def update_record_name(newRecord, id, oldrcName):
    oldCiphRecName = fetch_cipher_by_id_gen(id, oldrcName, "Record_Name") #Contains current record name.
    newRecord, rcName = encryptAll(id, [newRecord, oldrcName]) #encrypts both the old and new recordnames to compare.
    sql = ("UPDATE User_Records SET Record_Name = %s WHERE userId = %s AND Record_Name = %s")
    # Uses the the current/old record name and Id, to change the record name to the newly encrypted newRecord.
    cursor.execute(sql, (newRecord, id, oldCiphRecName))
    db.commit()

#Function used to updated the userID of a user. This is needed because the user ID will change based on the password,
# and username of the user. If a password is changed the user's ID will change aswell.
#This function requires us to change the foreign key check.
def update_user_ID(newID, oldID):
    alterOff = "SET FOREIGN_KEY_CHECKS = 0;"
    cursor.execute(alterOff)#Turning off the key check
    sql = ("UPDATE User_Records SET userId = %s WHERE userId = %s")#Updating all entried with the userID
    cursor.execute(sql, (newID, oldID))
    sql = ("UPDATE Registered_Users SET id = %s WHERE id = %s")#Updating all entried with the userID
    cursor.execute(sql, (newID, oldID))
    alterOn = "SET FOREIGN_KEY_CHECKS = 1;"
    cursor.execute(alterOn)#Turning on the key check again.
    db.commit()

#Function that updates the email of a record.
def update_record_email(newEmail, id, recName):
    oldCiphRecEmail = fetch_cipher_by_id_gen(id, recName, "Email")
    newCipherEmail = encryptAll(id, [newEmail])[0]
    sql = ("UPDATE User_Records SET Email = %s WHERE userId = %s AND Email = %s")
    cursor.execute(sql, (newCipherEmail, id, oldCiphRecEmail))
    db.commit()

#Function that updates the username of a record.
def update_record_username(name, id, rcName):
    oldCiphRecEmail = fetch_cipher_by_id_gen(id, rcName, "User_Name")
    newCipherEmail = encryptAll(id, [name])[0]
    sql = ("UPDATE User_Records SET User_Name = %s WHERE userId = %s AND User_Name = %s")
    cursor.execute(sql, (newCipherEmail, id, oldCiphRecEmail))
    db.commit()

#Function that updates the password of a record.
def update_record_password(passwd, id, rcName):
    oldCiphRecEmail = fetch_cipher_by_id_gen(id, rcName, "Account_Password")
    newCipherEmail = encryptAll(id, [passwd])[0]
    sql = ("UPDATE User_Records SET Account_Password = %s WHERE userId = %s AND Account_Password = %s")
    cursor.execute(sql, (newCipherEmail, id, oldCiphRecEmail))
    db.commit()

#Function that allows users to delete a record.
def delete_record(rec, id):
    oldCiphRecName = fetch_cipher_by_id_gen(id, rec, "Record_Name") #Contains current record name
    sql = ("DELETE FROM User_Records WHERE userId = %s AND Record_Name = %s")
    cursor.execute(sql, (id, oldCiphRecName))
    db.commit()

#Function that allows users to update the master email.
def update_master_email(inputEmail, id):
    encryptedEmail = encrypt(id, inputEmail)
    sql = ("UPDATE Registered_Users SET Email = %s WHERE Id = %s")
    cursor.execute(sql, (encryptedEmail, id))
    db.commit()

#Function that allows users to delete all of the records within their account.
def delete_all_records(id):
    sql = ("DELETE FROM User_Records WHERE userId = %s")
    cursor.execute(sql, (id,))
    db.commit()
    print("\nAll records have been deleted!")


#####################################  Encryption Decryption Starts################################################

#Function encrypts a given plain_text
def encrypt( id,  plain_text):
    #Ensuring the parameter is a string.
    if type(id) != str:
        id = str(id)
    if type(plain_text) != str:
        plain_text = str(plain_text)

    #Making sure id is not already present in database file.
    key = retrieveKey(id)

    if key is None: #If key has not been used
        #Create the key and fernet object to be used for encryption process.
        key = Fernet.generate_key()
        #Open a file with name *id*.
        f = open("database.txt", "a") # open file in append mode.

        # Write the PLAIN TEXT key into the file.
        f.write(id + "\t" + key.decode() + "\n")
        f.close()

    cipher_suite = Fernet(key) #Encryting.

    #Converting to bytes.
    plain_bytes_text = bytes(plain_text,'ascii')

    #Generate the cipher from the "plain bytes text".
    cipher_text = cipher_suite.encrypt(plain_bytes_text)

    # return the bytes (cipher text).
    return cipher_text.decode()

#Function that retrieves the encryption/decryption keys.
def retrieveKey(id):
    key = None
    #Ensuring it is a string.
    if type(id) != str:
        id = str(id)
    try:
        f = open("database.txt", "r")

        # Read the plain text key from the file and separating key from username.
        database_lines = f.readlines()
        for record in database_lines:
            record_fields = record.split('\t')
            if record_fields[0] == id:
                key = record_fields[1].strip("\n")
                key = key.encode()
        f.close()
    except: #if key not found.
        print("database.txt not found")
    return key

#Function is used to decrypt cipher.
def decrypt(id, cipher_text):
    #Retireve the key and create fernet object.
    key = retrieveKey(id)
    if key is None: #If the key is not found in the database.
        print("ERROR!  ID NOT IN DATABASE.TXT")
        return
    cipher_suite = Fernet(key) #Encryption.

    # Get  the "plain bytes text" from the cipher text.
    plain_bytes_text_2 = cipher_suite.decrypt(cipher_text.encode())

    # Get back the plain text from the plain bytes text.
    plain_text_2 = str(plain_bytes_text_2)

    #Return the decrypted plain text.
    return plain_bytes_text_2.decode()

#This function is used to encrypt the list of strings that are composed of user information.
def encryptAll(id, list_2_enc):
    enc_list = [] #Contains user information
    for ele in list_2_enc:#Iterate through list and ecrypt all of the entries.
        enc_list.append(encrypt(id, ele))
    return tuple(enc_list)

#Function is used to print all of the records given a specific ID.
def printAllRecsByID(id, nameOnly = False):
    sql = ("select * from User_Records ")
    cursor.execute(sql )
    results = cursor.fetchall()
    #If nameonly is true, that means the record exists and the information for that record will be printed.
    if nameOnly:
        print("Record Names:\n")
    #Iterates through the records and prints the information.
    for rec in results:
        if rec[1] == id:
            usrID = rec[1]
            recID = rec[0]
            recName = decrypt(usrID, rec[2])
            email = decrypt(usrID, rec[3])
            usr_name  = decrypt(usrID, rec[4])
            acct_pass  = decrypt(usrID, rec[5])
            #This will be the format it is displayed to the screen.
            if not nameOnly:
                print(f"Record Name: {recName}\nRecord Email: {email}\nRecord Username: {usr_name}\nRecord "
                      f"Password: {acct_pass}\n\n--------------------------\n")
            else:#If nameonly is false no record will be printed.
                print(f"\t-{recName}")


#Function adds a new encrypted record to the database.
def adding_new_enc_record(userId, recordName, recordEmail, recordUser, recordpassword):
    userId = userId
    Record_Name = recordName
    Email = recordEmail
    User_Name = recordUser
    Account_Password = recordpassword
    #Calling encryption all function to encrypt all information given by user.
    Record_Name, Email, User_Name, Account_Password =  encryptAll(userId, [ Record_Name, Email, User_Name,
                                                                            Account_Password])
    add_log2(userId, Record_Name, Email, User_Name, Account_Password)#Adding the information to the database.

#Function retrieves record based on a given id. Function determines where every value is located based on table column.
def fetch_rec_by_id_gen(id, gen_value, gen_cat):
    sql0 = ("select * from INFORMATION_SCHEMA.COLUMNS where TABLE_NAME='User_Records' ")
    cursor.execute(sql0)
    columns = cursor.fetchall()
    #Checking the location of the record within the columns.
    col_i = [tup[4] for tup in columns if tup[1] == "xecureddb" and tup[2] == "user_records" and tup[3] == gen_cat][0] - 1
    sql = ("SELECT * FROM User_Records WHERE userId = %s")
    cursor.execute(sql, (id,))
    results = cursor.fetchall()
    j = 0
    #Iterates through all records found.
    for rec in results:
        if decrypt(id, rec[col_i]) == gen_value:
            # Now decrypt everything else.
            req_rec = [rec[0], rec[1] ]
            #Iterates through records found.
            for i in range(2, len(rec)):
                req_rec.append(decrypt(id, rec[i]))
            return req_rec #If record found returns record.
    return "Record not Found..."

#Function retrieves encrypted text based on a given id. Function determines where every value is located
# based on table column.
def fetch_cipher_by_id_gen(id, recName, gen_cat):
    sql0 = ("select * from INFORMATION_SCHEMA.COLUMNS where TABLE_NAME='User_Records' ")
    cursor.execute(sql0)
    columns = cursor.fetchall()
    #Checking the location of the record within the columns.
    ret_i = [tup[4] for tup in columns if tup[1] == "xecureddb" and tup[2] == "user_records" and tup[3] == gen_cat][0] - 1
    name_i = col_i = [tup[4] for tup in columns if tup[1] == "xecureddb" and tup[2] == "user_records" and tup[3] == "Record_Name"][0] - 1
    #Using userID to retrieve all of their records.
    sql = ("SELECT * FROM User_Records WHERE userId = %s")
    cursor.execute(sql, (id,))
    results = cursor.fetchall()
    j = 0
    for rec in results:
        if decrypt(id, rec[name_i]) == recName:
            return rec[ret_i] #If record could not be found.
    print("Couldn't find record matching id and " + gen_cat)
    return None

#Checks to see if there are any records in the database.
def checkIfNoRecords(userId):
    sql = ("SELECT * FROM User_Records where userId = %s ")
    cursor.execute(sql, (userId,))
    results = cursor.fetchall()
    return len(results) #Returns the length of the entries in the database.

#Function checks the record name entered to see if it already has been registered within the application.
def checkDuplicateRecName(usr_id, newName):
    sql = ("select * from User_Records where userId = %s")
    cursor.execute(sql, (usr_id,) )
    results = cursor.fetchall()
    # Decrypts all of the data and stores it in the curNames variable.
    curNames = [decrypt(usr_id, rec[2]) for rec in results]
    return newName in curNames

#Function checks the email entered to see if it already has been registered within the application.
def checkDuplicateEmail(newEmail):
    sql = ("select * from Registered_Users")
    cursor.execute(sql )
    results = cursor.fetchall()
    #Decrypts all of the data and stores it in the curEmails variable.
    curEmails = [decrypt(rec[0], rec[2]) for rec in results]
    return newEmail in curEmails #Returns the email if it was found within the database.