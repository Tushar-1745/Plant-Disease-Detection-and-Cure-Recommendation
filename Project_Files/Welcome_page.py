import os
import tkinter as tk
from PIL import Image, ImageTk # type: ignore


root = tk.Tk()
root.title("Plant Disease Detection and Cure Recommendation using Machine Learning")

# Set window size to screen size
window_width = root.winfo_screenwidth()
window_height = root.winfo_screenheight()
root.geometry(f"{window_width}x{window_height}")

# Load original image
#background_image = Image.open("Images/s1.jpg")
background_image = Image.open("../Images/s1.jpg")
# Resize the image to fit the window
resized_image = background_image.resize((window_width, window_height))
resized_photo = ImageTk.PhotoImage(resized_image)

# Set background image
background_label = tk.Label(root, image=resized_photo)
background_label.place(x=0, y=0, relwidth=1, relheight=1)

# Add heading
heading_font = ("Helvetica", 24, "italic")  # Font family, size, and slant
heading_label = tk.Label(root, text="Plant Disease Detection and Cure Recommendation \nusing Machine Learning", font=heading_font, bg=root.cget("bg"), fg="black")

heading_label.place(relx=0.5, rely=0.1, anchor="center")



logo_label1 = tk.Label(text='System that capable \n to Detect And \n Identify the type of disease...', compound='bottom', font=("Times New Roman", 20, 'bold', 'italic'), width=35, bg="#cce6ff", fg="black")
logo_label1.place(x=480, y=600)

def open_login_page():
    current_directory = os.path.dirname(os.path.abspath(__file__))
    # Navigate to the Project_Files directory and open Login.py
    login_file_path = os.path.join(current_directory, "Login.py")
    # Check if the file exists before opening it
    if os.path.exists(login_file_path):
        os.system(f'python "{login_file_path}"')
    else:
        print("Error: Login.py file not found.")
   #os.system('python Project_Files/Login.py')

   
button1 = tk.Button(text=" START", command=open_login_page, width=15, height=1, font=('times', 15, ' bold '), bg="#3BB9FF", fg="black")
button1.place(x=650, y=500)

root.mainloop()

