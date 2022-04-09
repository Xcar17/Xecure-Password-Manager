#Xecure Password Manager
#By Carlos Ocasio

#This module is used to connect the application to the MySQL server.

import mysql.connector #Connects to database.

config = {
    'user': 'root', #Root is the username of the MySQL database.
    'passwd': '12345', #12345 is the password of the MySQL database.
}

db = mysql.connector.connect(**config) #Creating a database object.
cursor = db.cursor() #Creating a cursor for the database.