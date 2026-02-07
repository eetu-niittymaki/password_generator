#!/usr/bin/env python3

from random import randint
from sys import platform
import subprocess
import customtkinter as ct
from CTkMessagebox import CTkMessagebox

special = "&€$%@-+=^!?"
password_length = 24
use_special = True
use_numbers = True
use_uppercase = True

def check_has_numbers(password):
    if use_numbers:
        return any(char.isdigit() for char in password)
    return True

def check_has_special(password):
    if use_special:
        for char in special:
            if (char in password):
                return True
        return False    
    return True

def copy_to_clipboard(password):
    if platform == "win32": # Windows
        subprocess.run("clip", text=True, input=password)
    elif platform == "linux": # Linux, tested on Fedora
        subprocess.run(
		["wl-copy"],
		input=password.encode(),
		check=True
	)

def generate_password():
    word = ""
    letters = "abcdefghijklmnopqrstuvwxyz"
    length_letters = len(letters) - 1
    length_special = len(special) - 1
     
    while(len(word) < password_length):
        dice = randint(1, 10) 
        if (dice <= 5):
            word += letters[randint(0, length_letters)].upper() if randint(0, 6) < 2 and use_uppercase else letters[randint(0, length_letters)]
        elif (dice > 5 and dice <= 7):
            if use_special:
                word += special[randint(0, length_special)]
        else:
           if use_numbers:
            word += str(randint(0, 9))
    return word

def GUI():
    # Helper functions
    def generate_and_update():
        while True:
            password = generate_password()
            if check_has_numbers(password) and check_has_special(password):
                break

        copy_to_clipboard(password)

        textbox.configure(state="normal")
        textbox.delete("0.0", "end")
        textbox.insert("0.0", password + "\n\nCopied to clipboard")
        textbox.configure(state="disabled")

    def numberbox_event():
        global use_numbers
        use_numbers = numberbox_state.get()


    def specialbox_event():
        global use_special
        use_special = specialbox_state.get()

    def uppercasebox_event():
        global use_uppercase
        use_uppercase = uppercasebox_state.get()

    def button_event():
        global password_length
        new_length = entry_password_length.get()
        if (new_length.isdigit()):
            password_length = int(new_length)
            if password_length > 150:
                CTkMessagebox(title="Error!", message="Max Length Is 150!", icon="cancel")
                return
            elif password_length < 4:
                CTkMessagebox(title="Error!", message="Minimum Length Is 4!", icon="cancel")
                return
            generate_and_update()
        else:
            CTkMessagebox(title="Error!", message="Field Must Contain Only Numbers!", icon="cancel")


    width = 500
    height = 400
    app = ct.CTk()
    ct.set_appearance_mode("dark")
    app.title("Password Generator")

    screen_width = app.winfo_screenwidth()
    screen_height = app.winfo_screenheight()
    position_top = int(screen_height / 2 - height / 2)
    position_right = int(screen_width / 2 - width / 2)

    app.geometry(f"{width}x{height}+{position_right}+{position_top}")
    app.grid_columnconfigure(0, weight=1)
    app.grid_columnconfigure(1, weight=1)
    app.grid_rowconfigure(0, weight=1)
    app.grid_rowconfigure(1, weight=1)
    app.grid_rowconfigure(2, weight=1)
    app.grid_rowconfigure(3, weight=1)

    # Password textbox
    textbox = ct.CTkTextbox(app)
    textbox.grid(row=0, column=0, columnspan=3, padx=10, pady=10, sticky="nsew")
    textbox.configure(state="disabled")

    # Password length entry box
    entry_label = ct.CTkLabel(app, text="Password Length")
    entry_label.grid(row=1, column=0, padx=0, pady=10, sticky="e")
    entry_password_length = ct.CTkEntry(app, placeholder_text=str(password_length), textvariable=ct.StringVar(value=str(password_length)))
    entry_password_length.grid(row=1, column=1, padx=0, pady=10, sticky="e")
    
    # Checkboxes
    numberbox_state = ct.BooleanVar(value=use_numbers)
    specialbox_state = ct.BooleanVar(value=use_special)
    uppercasebox_state = ct.BooleanVar(value=use_uppercase)

    checkbox_numbers = ct.CTkCheckBox(app, text="Use Numbers", variable=numberbox_state, command=numberbox_event)
    checkbox_numbers.grid(row=2, column=0, padx=10, pady=10, sticky="nsew")

    checkbox_special = ct.CTkCheckBox(app, text="Use Special", variable=specialbox_state, command=specialbox_event)
    checkbox_special.grid(row=2, column=1, padx=10, pady=10, sticky="nsew")

    checkbox_uppercase = ct.CTkCheckBox(app, text="Use Uppercase", variable=uppercasebox_state, command=uppercasebox_event)
    checkbox_uppercase.grid(row=2, column=2, padx=10, pady=10, sticky="nsew")

    # Button
    button = ct.CTkButton(app, text="Generate New", command=button_event)
    button.grid(row=3, column=0, columnspan=2, padx=40, pady=10, sticky="se")

    generate_and_update() # Generate initial password

    app.mainloop()

if __name__ == "__main__":
    GUI()