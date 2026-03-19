from tkinter import *
from tkinter import messagebox
from random import choice, randint, shuffle
import functools
from typing import Dict, Any

import json
import pyperclip

# ---------------------------- ERROR HANDLING ------------------------------- #

def handle_file_errors(operation_name: str):
    """Decorator to handle file operation errors consistently."""
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except FileNotFoundError:
                if operation_name == "load":
                    return {}  # Expected for first run
                messagebox.showerror(title="File Error", message=f"File not found during {operation_name}")
                return None
            except json.JSONDecodeError as e:
                messagebox.showerror(title="Corrupted File", message=f"Invalid JSON data: {e}")
                return {} if operation_name == "load" else None
            except (IOError, PermissionError) as e:
                messagebox.showerror(title="Access Error", message=f"File access error: {e}")
                return None
            except Exception as e:
                messagebox.showerror(title="Unexpected Error", message=f"Unexpected error: {e}")
                return None
        return wrapper
    return decorator   


# ---------------------------- PASSWORD GENERATOR ------------------------------- #

#Password Generator Project
def generate_password():
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    password_letters = [choice(letters) for _ in range(randint(8, 10))]
    password_symbols = [choice(symbols) for _ in range(randint(2, 4))]
    password_numbers = [choice(numbers) for _ in range(randint(2, 4))]

    password_list = password_letters + password_symbols + password_numbers
    shuffle(password_list)

    password = "".join(password_list)
    password_entry.insert(0, password)
    pyperclip.copy(password)

# ---------------------------- SAVE PASSWORD ------------------------------- #
def save():

    website = website_entry.get()
    email = email_entry.get()
    password = password_entry.get()

    # Validate inputs
    if not all([website, email, password]):
        messagebox.showinfo(title="Oops", message="Please make sure you haven't left any fields empty.")
        return
    
    # Load existing data / create empty dict if file doesn't exist
    data = load_password_data()
    
    # Check for existing entry
    if website in data:
        entry_exists = messagebox.askyesno(
            title="Entry Exists", 
            message=f"An entry for {website} already exists. Do you want to override it?")
        if not entry_exists:
            messagebox.showinfo(title="No new entry", message="Keeping existing entry.")
            return

     # Save the entry
    data[website] = {"email": email, "password": password}
    save_password_data(data)

    # Clear fields and confirm
    clear_entries()
    messagebox.showinfo(title="Success", message=f"Password for {website} saved successfully!")
 

@handle_file_errors("load")
def load_password_data() -> Dict[str, Any]:
    """Load password data from file."""
    with open("passwords.json", "r") as file:
        data = json.load(file)
        if not isinstance(data, dict):
            messagebox.showwarning(title="Invalid Data", message="Password file contains invalid data. Creating new file.")
            return {}
        
        # Validate the structure
        if not validate_password_data(data):
            messagebox.showwarning(title="Invalid Structure", message="Password file has invalid structure. Creating new file.")
            return {}
            
        return data
 
@handle_file_errors("save")
def save_password_data(data: Dict[str, Any]) -> bool:
    """Save password data to file."""
    with open("passwords.json", "w") as file:
        json.dump(data, file, indent=4)
    return True


def validate_password_data(data: Any) -> bool:
    """Validate that password data is properly formatted."""
    return isinstance(data, dict) and all(
        isinstance(v, dict) and "email" in v and "password" in v 
        for v in data.values()
    )

def clear_entries():
    """Clear all entry fields."""
    website_entry.delete(0, END)
    email_entry.delete(0, END)
    password_entry.delete(0, END)


# ---------------------------- SEARCH FOR EXISITNG ENTRIES ------------------------------- #

def search():
    website = website_entry.get()

    # Validate email
    if not website:
        messagebox.showinfo(title="Oops", message="Please enter a website!")
        return

    data = {}
    try:
        with open("passwords.json", "r") as data_file:
            data = json.load(data_file)
    except FileNotFoundError:
        messagebox.showerror(message="No password file exists!")
    except json.JSONDecodeError:
        messagebox.showerror(message="Password file unable to be read!")
    
    else:
        entry = data.get(website)
        if entry:
            messagebox.showinfo(title="Entry Found", message=f"Email: {entry['email']}\nPassword: {entry['password']}")
        else:
            # Offer to create new entry if not found
            result = messagebox.askyesno(
                title="Entry Not Found", 
                message=f"No entry found for {website}.\n\nWould you like to create one?")
            if result:
                # Focus on email field for new entry
                save()


# ---------------------------- UI SETUP ------------------------------- #

window = Tk()
window.title("Password Manager")
window.config(padx=50, pady=50)

canvas = Canvas(height=200, width=200)
logo_img = PhotoImage(file="logo.png")
canvas.create_image(100, 100, image=logo_img)
canvas.grid(row=0, column=1)

#Labels
website_label = Label(text="Website:")
website_label.grid(row=1, column=0, sticky="e")

email_label = Label(text="Email / Username:")
email_label.grid(row=2, column=0, sticky="e")

password_label = Label(text="Password:")
password_label.grid(row=3, column=0, sticky="e")

#Entries
website_entry = Entry(width=21)
website_entry.grid(row=1, column=1)
website_entry.focus()

email_entry = Entry(width=37)
email_entry.grid(row=2, column=1, columnspan=2)
email_entry.configure(justify="left")

password_entry = Entry(width=21)
password_entry.grid(row=3, column=1)

# Buttons
search_password_button = Button(text="Search", width=11, command=search)
search_password_button.grid(row=1, column=2)

generate_password_button = Button(text="Generate", command=generate_password, width=11)
generate_password_button.grid(row=3, column=2)

add_button = Button(text="Add", width=36, command=save)
add_button.grid(row=4, column=1, columnspan=2)

window.mainloop()