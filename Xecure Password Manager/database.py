import mysql.connector

config = {
    'user': 'root',
    'passwd': '12345',
}

db = mysql.connector.connect(**config)
cursor = db.cursor()