import os
import subprocess
import tkinter as tk
from tkinter import messagebox as ms
from PIL import Image, ImageTk # type: ignore
import mysql.connector # type: ignore

def open_register_page():
    current_directory = os.path.dirname(os.path.abspath(__file__))
    # Navigate to the Project_Files directory and open Login.py
    login_file_path = os.path.join(current_directory, "Register.py")
    # Check if the file exists before opening it
    if os.path.exists(login_file_path):
        os.system(f'python "{login_file_path}"')
    else:
        print("Error: Login.py file not found.")
    #os.system('python Project_Files/Register.py')

def validate_credentials():
    try:
        # Connect to the database
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="Tushar@1745",
            database="be_project_db"
        )

        cursor = connection.cursor()

        # Get the username (email) and password entered by the user
        entered_username = username.get()
        entered_password = password.get()

        # Query to fetch user data
        query = "SELECT * FROM Users WHERE Email = %s AND Password = %s"
        cursor.execute(query, (entered_username, entered_password))
        result = cursor.fetchone()

        # If user exists, show success message and redirect to operation page
        if result:
            ms.showinfo("Success", "Login successful!")
            current_directory = os.path.dirname(os.path.abspath(__file__))
            # Navigate to the Project_Files directory and open Login.py
            operation_file_path = os.path.join(current_directory, "Operation.py")
            # Check if the file exists before opening it
            if os.path.exists(operation_file_path):
                os.system(f'python "{operation_file_path}"')
            else:
                print("Error: Operation.py file not found.")
            # Redirect to operation page
            # Note: You may want to pass user information to the operation page
            #os.system('python Project_Files/Operation.py')
            # subprocess.Popen(['python', 'Operation.py'])
        else:
            ms.showerror("Error", "Invalid username or password")

    except mysql.connector.Error as error:
        ms.showerror("Error", f"Database error: {error}")

    finally:
        # Close database connection
        if 'connection' in locals() and connection.is_connected():
            cursor.close()
            connection.close()

root = tk.Tk()
root.configure(background="black")
w, h = root.winfo_screenwidth(), root.winfo_screenheight()
root.geometry("1600x1450")
root.title("Login Form")

username = tk.StringVar()
password = tk.StringVar()

img = Image.open('../Images/login_bg.png')
img = img.resize((w, h))
background_image = ImageTk.PhotoImage(img)
background_label = tk.Label(root, image=background_image)
background_label.image = background_image
background_label.place(x=0, y=0)

# Heading Label
heading_label = tk.Label(text="Plant Disease Detection and Cure Recommendation using Machine Learning", font=("san serif", 20, "italic", "bold"), fg="black")
heading_label.place(x=250, y=50)

title = tk.Label(root, text="Login Here", font=("Algerian", 30, "bold", "italic"), bd=5, bg="black", fg="white")
title.place(x=600, y=150, width=250)

frame = tk.Frame(root, height=800, bg="white")
frame.place(x=520, y=240)
logolbl = tk.Label(frame, bd=0).grid(row=0, columnspan=2, pady=20)

# Username
lbluser = tk.Label(frame, text="Username", compound=tk.LEFT, font=("Times new roman", 20, "bold"), bg="white")
lbluser.grid(row=1, column=0, padx=5, pady=10)
txtuser = tk.Entry(frame, bd=5, border=0, textvariable=username, font=("", 15))
txtuser.grid(row=1, column=1, padx=15)
tk.Frame(frame, width=250, height=2, bg='black').place(x=180, y=100)

# Password
lblpass = tk.Label(frame, text="Password", compound=tk.LEFT, font=("Times new roman", 20, "bold"), bg="white")
lblpass.grid(row=2, column=0, padx=5, pady=10)
txtpass = tk.Entry(frame, bd=5, border=0, textvariable=password, show="*", font=("", 15))
txtpass.grid(row=2, column=1, padx=15)
tk.Frame(frame, width=250, height=2, bg='black').place(x=180, y=150)

# Login Button
btn_log = tk.Button(frame, text="Login", width=30, font=("Times new roman", 14, "bold"), bg="Green", fg="black", cursor="hand2", command=validate_credentials)
btn_log.grid(row=3, column=0, columnspan=2, pady=(20, 10), padx=50)

# Line "Don't have an account? Sign Up"
signup_label1 = tk.Label(frame, text="Don't have an account? Sign Up", font=("Times new roman", 12), bg="white", fg="black", cursor="hand2")
signup_label1.grid(row=4, column=1, pady=10, padx=(10, 0))
signup_label1.bind("<Button-1>", lambda event: open_register_page())

root.mainloop()

