from random import randint
import subprocess

special = "&€$%@-+=^!?"

def check_has_numbers(password):
    return any(char.isdigit() for char in password)

def check_has_special(password):
    global special
    for char in special:
        if (char in password):
            return True
    return False     

def copy_to_clipboard(password):
   return subprocess.run("clip", text=True, input=password)

def gen_pass():
    global special
    word = ""
    letters = "abcdefghijklmnopqrstuvwxyz"
    while(len(word) < 24):
        dice = randint(1, 10) 
        if (dice <= 5):
            if (randint(0, 1) == 0):
                word += letters[randint(0, len(letters)-1)]
            else:
                word += letters[randint(0, len(letters)-1)].upper()
        elif (dice > 5 and dice <= 7):
            special[randint(0, len(special)-1)]
            word += special[randint(0, len(special)-1)]
        else:
           word += str(randint(0, 9))
    return word

def main():
    password = gen_pass()
    if (check_has_numbers(password) and check_has_special(password)):
        copy_to_clipboard(password)
        print(password)
        print("\nCopied to clipboard")
        input()
    else: 
        main()
main()