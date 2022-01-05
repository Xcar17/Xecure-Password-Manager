#Module contains function that copies password into the clipboard and resets the clipboard after 30 seconds
import time

import pyperclip

def clipboard(password):
    pyperclip.copy(password)


password = input("Enter your password: ")
clipboard(password)
print("Your password will be saved to your clipboard for just 30 seconds....")
time.sleep(30)
clipboard('Password has been sanitized')
print('Thanks for using Xecured Password')
time.sleep (3)

#Maybe add loading bar