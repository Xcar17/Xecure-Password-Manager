# Xecure-Password-Manager

The project is a password manager application for Windows computers used to securely store and manage log in information for various accounts. It uses a “master” password to provide access into the user’s account with all the passwords. The application can also copy a record’s password into the computer’s clipboard. This password will then be wiped from the clipboard after fifteen seconds or if the user closes the application. The application has connectivity to a MYSQL database that is used to securely store the user’s information. In order to protect the information in the database the application uses the well-established AES encryption and SHA256 hashing algorithms. Additionally, the users have the option to generate unique and complex passwords for every record entered. Users will also have the option of entering their own passwords and the application will guide them every step of the way. Lastly, the program has features that allows users to reset their “master” password and email if they forget it or wish to change it.

The application is called Xecure Password Manager and it was inspired by applications like KeePass, and LastPass and it contains all of the major features that these application have. All of the previously mentioned features are the standard in the password manager market, and they will be included in the Xecure Password Manager application at no cost to the users. In addition to being a free application, Xecure Password Manager will not contain any ads, there are no password or account limits, and it will not store or use user data for any other purpose. This is what separates Xecure Password Manager from the competition.


Proposed Implementation Languages
The password manager application was developed on a Windows computer by using the latest versions of Python 3 (version 3.9.7) and MySQL (version 8).
Libraries, packages, development kits
The password manager application will use the following libraries:
•	Hashlib – Used for hashing.
•	cryptography.fernet – Used to encrypt.
•	msvcrt – Used to prevent the command screen from continuing until a key is pressed.
•	mysql.connector – Used to connect to the database.
•	os – Used to change the title of the command line screen.
•	Sys – Used alongside getpass to hide passwords in the command line screen.
•	getpass – Used to hide password in the command line screen. 
•	random – Used to generate random passwords and codes.
•	smtplib – Used for emailing capabilities.
•	socket – Used alongside smtplib to send emails, and email error handling.
•	time – Used alongside pyperclip to determine when to wipe clipboard.
•	pyperclip – Used to save record’s password into the computer’s clipboard.
•	threading – Used to wipe the clipboard while the user continues to use the application.


Additional Software/Equipment Needed
A Windows operating system is required, as well as Python (version 3.9.7) and a MySQL (version 8) database. See below for instructions on how to download and setup both Python and MySQL.
MySQL Installation Guide: 
These steps will guide you through the installation and setup of the MySQL Community Server for the required database of this application.
1.	Visit https://dev.mysql.com/downloads/mysql/
2.	Look for the “MySQL (MSI) Installer for Windows” and click on the “Go to Download Page” button (You can also use this link: https://dev.mysql.com/downloads/windows/installer/8.0.html)
3.	There will be two Windows MSI Installer options here. Please find the “(mysql-installer-community-8.0.27.0.msi)” option and press the download button.
4.	You will be redirected to a screen that asks you to login or sign up, but this is not needed. Scroll down to the bottom of the page and click on the “No thanks, just start my download.” link.  
5.	A download prompt will be displayed. Click on the “Save File” button. This will start the download of the file.
6.	Wait for the download to finish.
7.	Once it has downloaded, look for the “mysql-installer-community-8.0.26.0” (version number might change) file and run it. The file is typically located in your downloads folder.
8.	After double clicking the file, it will begin preparing the installation and it will then ask you for permission to install the application. Click the “yes” button.
9.	It may ask you “Do you want to allow this app to make changes to your pc?”. Click on the “yes” button. (Skip this step if you did not see this alert)
10.	The MySQL installation windows will now be displayed, and it will ask you to read over the License Agreement. After doing so, press the “I accept the license terms” check box and press the “Next” button.
11.	On the “Choosing a Setup Type” screen select the “Developer Default” option and press next.
12.	A screen may alert you that some product requirements have not been satisfied and it will ask you if you wish to continue. Select yes. (Skip this step if you did not see this alert)
13.	On this installation screen you can see all of the products that will be installed. When you are ready select the “Execute” button. This will begin installing all of the products.
14.	Wait for the Installation to finish.
15.	After the download has finished you will see a green checkmark on all of the products downloaded. If everything downloaded successfully press the “Next” button.
16.	On the “Product Configuration” screen you will be able to see the configuration for all of your downloaded products. Once you have reviewed this information press the “Next” button.
17.	On the “Type and Networking” screen select the “Standalone MySQL Server/Classic MySQL Replication” option and press the “Next” button.
18.	On this screen leave the “Config Type” as “Development Machine”. Make sure that the “TCP/IP” checkbox and “Open Firewall port for network access” checkbox are selected. Lastly, the “Port Number” is 3306. After confirming these options press the “Next” button.
19.	On the Accounts and Roles screen enter a strong password on the “MySQL Root Password” fields (make sure you remember this password). Then press the “Add User” button to create a user account. 
20.	A screen will appear and ask you for username information. Enter a username for your account (make sure you remember this username). Then enter a strong password for your account (make sure you remember this password). Once this is done press the “Ok” button. After creating your user account press on the “Next” button.
21.	On the “Windows Service” screen leave all settings as default and press on the “Next” button.
22.	On the “Plugins and Extensions” screen leave all settings as default and press on the “Next” button.
23.	On the “Apply Configuration” screen you will see an overview of the configurations. Once you are ready press the “Execute” button and the listed changes will be applied. Once this is done press the “Finish” button.
24.	On the “Product Configuration” Screen you will see that the MySQL Server is completed. Press the “Next” button to continue.
25.	On the “MySQL Router Configuration” screen you will leave all settings as default and press on the “Next” button.
26.	On the “Product Configuration” screen you will review the configuration and press on the “Next” button.
27.	On the Connect To Server screen, select the “MySQL Server 8.0.27.0 (version may be different for you) text. Then enter press the “Check” button to test the connection. Once the connection is established and you see a “Connection Successful” message press the “Next” button.
28.	On the apply configurations, press the “Execute” button. Once all the configurations are finished press the “Finish” button.
29.	On the “Product Configuration” screen you will review the configuration and press on the “Next” button.
30.	You will see the installation complete screen. Press the “Finish” button.
31.	You have successfully installed the MySQL database.


To use with MySQL Workbench:
1.	Go to start and search for “workbench”
2.	Open the MySQL Workbench
3.	Once the application opens, double click the “Local instance” below the “MySQL Connections”.
4.	A screen will appear, and you will be prompted to enter the password for the database. After entering the password, press the “OK” button.
5.	This is your database serve.
