#Xecure Password Manager
#By Carlos Ocasio
#Password Manager lets users create an account and allows them to safely store all of their login credentials for
#various sites. Login credentials can only be accessed by the root user. Application uses SHA256 to hash login
#credentials and encrypts the records of the user inside a secure MySQL database.

#This module is the driver of the code

from mainMenu import mainMenu
from dbsetup import create_database

create_database()#creates a database with the name entered

#Calling program
mainMenu()