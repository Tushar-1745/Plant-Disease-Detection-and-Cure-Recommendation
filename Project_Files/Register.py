import os
import tkinter as tk
from tkinter import messagebox as ms
from PIL import Image, ImageTk # type: ignore
import re
import mysql.connector # type: ignore

# Function to validate mobile number
def validate_mobile_number():
    mobile_number = Phoneno.get()
    if not mobile_number.isdigit() or len(mobile_number) != 10:
        validation_label_mobile.config(text="Mobile number is not valid.", fg="red")
    else:
        validation_label_mobile.config(text="")

# Function to validate email
def validate_email():
    email = Email.get()
    if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
        validation_label_email.config(text="Email is not valid.", fg="red")
    else:
        validation_label_email.config(text="")

# Function to validate password
def validate_password():
    password = password_var.get()
    if len(password) < 6:
        validation_label_password.config(text="Password should be at least 6 characters long.", fg="red")
    elif not re.search(r"[A-Z]", password):
        validation_label_password.config(text="Password should contain at least one uppercase letter.", fg="red")
    elif not re.search(r"\d", password):
        validation_label_password.config(text="Password should contain at least one digit (0-9).", fg="red")
    elif not re.search(r"[!@#$%^&*()_+=\-{}\[\]:;\"'|\\<,>.?/]", password):
        validation_label_password.config(text="Password should contain at least one special character.", fg="red")
    else:
        validation_label_password.config(text="")

# Function to check if email or mobile number already exists in database
def check_existing_user(email, mobile_number):
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="Tushar@1745",
            database="be_project_db"
        )
        cursor = connection.cursor()

        # Check if email exists
        cursor.execute("SELECT * FROM Users WHERE Email = %s", (email,))
        result = cursor.fetchone()
        if result:
            ms.showerror("Error", "An account with this email already exists.")
            return False

        # Check if mobile number exists
        cursor.execute("SELECT * FROM Users WHERE Mobile_Number = %s", (mobile_number,))
        result = cursor.fetchone()
        if result:
            ms.showerror("Error", "An account with this mobile number already exists.")
            return False

        return True

    except mysql.connector.Error as error:
        ms.showerror("Error", f"Database error: {error}")
        return False

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

# Function to validate all fields and register user
def validate_fields():
    name = Fullname.get()
    email = Email.get()
    mobile_number = Phoneno.get()
    password = password_var.get()
    confirm_password = confirm_password_var.get()

    # Reset validation labels
    validation_label_name.config(text="")
    validation_label_email.config(text="")
    validation_label_mobile.config(text="")
    validation_label_password.config(text="")
    validation_label_confirm_password.config(text="")

    # Validate each field
    if not name:
        validation_label_name.config(text="Name is not entered.", fg="red")
        
    if not email:
        validation_label_email.config(text="Email is not entered.", fg="red")
    if not mobile_number:
        validation_label_mobile.config(text="Mobile number is not entered.", fg="red")
    if not password:
        validation_label_password.config(text="Password is not entered.", fg="red")
        
    if not confirm_password:
        validation_label_confirm_password.config(text="Password is not entered.", fg="red")
        
    # Validate mobile number
    if mobile_number and (not mobile_number.isdigit() or len(mobile_number) != 10):
        validation_label_mobile.config(text="Mobile number is not valid.", fg="red")

    # Validate email
    if email and (not re.match(r"[^@]+@[^@]+\.[^@]+", email)):
        validation_label_email.config(text="Email is not valid.", fg="red")

    # Validate password
    if password:
        if len(password) < 6:
            validation_label_password.config(text="Password should be at least 6 characters long.", fg="red")
        elif not re.search(r"[A-Z]", password):
            validation_label_password.config(text="Password should contain at least one uppercase letter.", fg="red")
        elif not re.search(r"\d", password):
            validation_label_password.config(text="Password should contain at least one digit (0-9).", fg="red")
        elif not re.search(r"[!@#$%^&*()_+=\-{}\[\]:;\"'|\\<,>.?/]", password):
            validation_label_password.config(text="Password should contain at least one special character.", fg="red")
            
    
    # Validate confirm password
    if password != confirm_password:
        validation_label_confirm_password.config(text="Confirm password should match password", fg="red")
            
    # Check if all fields are valid
    if (validation_label_name.cget("text") == "" and
        validation_label_email.cget("text") == "" and
        validation_label_mobile.cget("text") == "" and
        validation_label_password.cget("text") == "" and
        validation_label_confirm_password.cget("text") == ""):
        
        # Check if email or mobile number already exists
        if email and mobile_number:
            if check_existing_user(email, mobile_number):
                register_user(name, email, mobile_number, password)

# Function to register user and save data to database
def register_user(name, email, mobile_number, password):
    try:
        # Connect to the database
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="Tushar@1745",
            database="be_project_db"
        )

        cursor = connection.cursor()

        # Insert user data into the database
        query = "INSERT INTO Users (Name, Email, Mobile_Number, Password) VALUES (%s, %s, %s, %s)"
        cursor.execute(query, (name, email, mobile_number, password))
        connection.commit()

        ms.showinfo("Success", "Account created successfully!")
        os.system('python Operation.py')

    except mysql.connector.Error as error:
        ms.showerror("Error", f"Database error: {error}")

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

# Initialize Tkinter window
window = tk.Tk()
window.geometry("1600x1450")
window.title("REGISTRATION FORM")
window.configure(background="grey")

# Define StringVar variables
Fullname = tk.StringVar()
Email = tk.StringVar()
Phoneno = tk.StringVar()
password_var = tk.StringVar()
confirm_password_var = tk.StringVar()

#background image
img = Image.open('../Images/register_bg.webp')
img = img.resize((1600, 1450))
background_image = ImageTk.PhotoImage(img)
background_label = tk.Label(window, image=background_image)
background_label.image = background_image
background_label.place(x=0, y=0, relwidth=1, relheight=1, anchor='nw')

# Heading Label
heading_label = tk.Label(window, text="Plant Disease Detection and Cure Recommendation using Machine Learning", font=("san serif", 20, "italic", "bold"), fg="black")
heading_label.place(x=250, y=50)

# Registration form Label
RegForm_label = tk.Label(window, text="Registration Form", font=("Times new roman", 30, "bold"), bg="#192841", fg="white")
RegForm_label.place(x=570, y=150)

#Name Label
l1 = tk.Label(window, text="Name :", width=12, font=("Times new roman", 15, "bold"), bg="snow")
l1.place(x=500, y=250)
t1 = tk.Entry(window, textvar=Fullname, width=20, font=('', 15))
t1.place(x=700, y=250)
validation_label_name = tk.Label(window, text="", font=("Times new roman", 12), fg="red")
validation_label_name.place(x=930, y=250)  # Validation message label

#Email Label
l5 = tk.Label(window, text="E-mail :", width=12, font=("Times new roman", 15, "bold"), bg="snow")
l5.place(x=500, y=300)
t4 = tk.Entry(window, textvar=Email, width=20, font=('', 15))
t4.place(x=700, y=300)
validation_label_email = tk.Label(window, text="", font=("Times new roman", 12), fg="red")
validation_label_email.place(x=930, y=300)  # Validation message label

#Mobile Number Label
l6 = tk.Label(window, text="Mobile number :", width=12, font=("Times new roman", 15, "bold"))
l6.place(x=500, y=350)
t5 = tk.Entry(window, textvar=Phoneno, width=20, font=('', 15))
t5.place(x=700, y=350)
validation_label_mobile = tk.Label(window, text="", font=("Times new roman", 12), fg="red")
validation_label_mobile.place(x=930, y=350)  # Validation message label

#Password Label
l9 = tk.Label(window, text="Password :", width=12, font=("Times new roman", 15, "bold"), bg="snow")
l9.place(x=500, y=400)
t9 = tk.Entry(window, textvariable=password_var, width=20, font=('', 15), show="*")
t9.place(x=700, y=400)
validation_label_password = tk.Label(window, text="", font=("Times new roman", 12), fg="red")
validation_label_password.place(x=930, y=400)  # Validation message label

#Confirm password Label
l10 = tk.Label(window, text="Confirm Password:", width=13, font=("Times new roman", 15, "bold"), bg="snow")
l10.place(x=500, y=450)
t10 = tk.Entry(window, textvar=confirm_password_var, width=20, font=('', 15), show="*")
t10.place(x=700, y=450)
validation_label_confirm_password = tk.Label(window, text="", font=("Times new roman", 12), fg="red")
validation_label_confirm_password.place(x=930, y=450)  # Validation message label

#Register button Label
btn = tk.Button(window, text="Register", bg="#192841",font=("",15),fg="white", width=19, height=0, command=validate_fields)
btn.place(x=600, y=520)

# Label for Login redirection
def open_login_page():
    #os.system('python Project_Files/Login.py')
    current_directory = os.path.dirname(os.path.abspath(__file__))
    # Navigate to the Project_Files directory and open Login.py
    login_file_path = os.path.join(current_directory, "Login.py")
    # Check if the file exists before opening it
    if os.path.exists(login_file_path):
        os.system(f'python "{login_file_path}"')
    else:
        print("Error: Login.py file not found.")

login_label1 = tk.Label(window, text="Already have an account? Login", font=("Times new roman", 12), fg="black", cursor="hand2")
login_label1.place(x=610, y=580)
login_label1.bind("<Button-1>",  lambda event: open_login_page())

window.mainloop()


