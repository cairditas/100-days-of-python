from tkinter import *
from tkinter import messagebox

import os
import pyperclip
import secrets
import string

TAUPE = "#0C0C0C"
BLUE = "#FFF2CC"
BLACK = "black"

window = Tk()
window.title("Password Manager")
# window.minsize(width=300, height=300)
window.config(padx=20, pady=20, bg=BLUE)

canvas = Canvas(width=200, height=200, bg=BLUE, highlightthickness=0)
image = PhotoImage(file="logo.png")
canvas.create_image(100, 105, image=image)
canvas.grid(row=0, column=1)

# ---------------------------- PASSWORD GENERATOR ------------------------------- #
def generate():
    letters = string.ascii_letters + string.digits + "!@#$%^&*"
    password = ''.join(secrets.choice(letters) for _ in range(16))

    password_entry.delete(0, END)  # Clear the entry
    password_entry.insert(0, password)  # Insert the password
    password_entry.config(fg="black")
    
    # Copy password to clipboard
    pyperclip.copy(password)

# ---------------------------- SAVE PASSWORD ------------------------------- #
def add_entry():
    filename = "passwords.txt"
    
    # Get entry data
    website = website_entry.get()
    email = email_entry.get()
    password = password_entry.get()

    # Validate inputs
    if not website or not email or not password:
        messagebox.showerror(message="Missing details!")
        print("Please fill in all fields")
        return
    
    messagebox.askokcancel(
        title=website, 
        message=f"Are you sure you want to save this entry?\nWebsite: {website}\nEmail: {email}\nPassword: {password}"
    )

    # Create file if it doesn't exist
    if not os.path.exists(filename):
        with open(filename, "w") as file:
            file.write("Website | Email | Password\n")
    
    # Append the new entry
    with open(filename, "a") as file:
        file.write(f"{website} | {email} | {password}\n")

    
    # Clear the website and password fields
    website_entry.delete(0, END)
    email_entry.delete(0, END)
    password_entry.delete(0, END)

    new_entry_created = Label(text=f"Entry for {website} created!", bg=BLUE, fg=TAUPE)
    new_entry_created.grid(column=1, row=6)

# ---------------------------- UI SETUP ------------------------------- #
website = Label(text="Website: ", bg=BLUE, fg=TAUPE)
website.grid(column=0, row=1, sticky="e")
 
email = Label(text="Email / Username: ", bg=BLUE, fg=TAUPE)
email.grid(column=0, row=2, sticky="e")

password = Label(text="Password: ", bg=BLUE, fg=TAUPE)
password.grid(column=0, row=3, sticky="e")



website_entry = Entry(width=35, bg=BLUE, fg=BLACK, highlightthickness=0)
website_entry.grid(column=1, row=1, columnspan=2)

email_entry = Entry(width=35, bg=BLUE, fg=BLACK, highlightthickness=0)   
email_entry.grid(column=1, row=2, columnspan=2)

password_entry = Entry(width=25, bg=BLUE, fg=BLACK, highlightthickness=0)
password_entry.grid(column=1, row=3)


generate_password_button = Button(text="Generate", command=generate)
generate_password_button.grid(column=2, row=3, columnspan=1)
generate_password_button.config(highlightbackground=BLUE)


add_button = Button(text="Add to Password Manager", command=add_entry)
add_button.grid(column=1, row=5, columnspan=2)
add_button.config( 
    relief="solid",
    highlightbackground=BLUE)

window.mainloop()