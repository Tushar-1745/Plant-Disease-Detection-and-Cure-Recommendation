import os
import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk, ImageSequence  # type: ignore
import numpy as np  # type: ignore
import cv2  # type: ignore
from Diseases import diseases

global leaf
leaf = ""
Plant = ""

def resize_image(event):
    global resized_image, resized_photo
    window_width = event.width
    window_height = event.height
    resized_image = original_image.resize((window_width, window_height))  # type: ignore
    resized_photo = ImageTk.PhotoImage(resized_image)
    background_label.config(image=resized_photo)

def upload_image():
    global leaf
    file_path = filedialog.askopenfilename(
        initialdir="C:/Users/MTS/Downloads/BE_Project/testing_dataset",
        title="Select Image File",
        filetypes=(("Image files", "*.jpg *.jpeg *.png *.gif"), ("all files", "*.*"))
    )
    if file_path:
        print("Selected file:", file_path)
        selected_image = Image.open(file_path)
        leaf = file_path
        target_width_pixels = int(5 * 37.79)
        target_height_pixels = int(5 * 37.79)
        selected_image = selected_image.resize((target_width_pixels, target_height_pixels))
        selected_image_photo = ImageTk.PhotoImage(selected_image)
        selected_image_label.config(image=selected_image_photo)
        selected_image_label.image = selected_image_photo
        selected_image_name_label.config(text=file_path.split("/")[-1], fg="black")
        analyze_button.place(relx=0.5, rely=0.7, anchor="center")
        upload_button.config(bg='white', fg='purple', bd=1, relief='raised')

def update_completed_message(str_T):
    result_label = tk.Label(root, text=str_T, font=("bold", 18), fg='black', justify="center")
    result_label.place(relx=0.5, rely=0.65, anchor="center")

def update_result_message(str_T):
    result_label = tk.Label(root, text=str_T, font=("bold", 18), fg='black', justify="left")
    result_label.place(relx=0.5, rely=0.77, anchor="center")

def test_model_proc(leaf):
    from tensorflow.keras.models import load_model  # type: ignore

    IMAGE_SIZE = 64

    if leaf != "":
        model = load_model('C:/Users/MTS/Desktop/Final_Project/plant_model.h5')
        img = Image.open(leaf)
        img = img.resize((IMAGE_SIZE, IMAGE_SIZE))
        img = np.array(img)
        img = img.reshape(1, IMAGE_SIZE, IMAGE_SIZE, 3)
        img = img.astype('float32')
        img = img / 255.0
        prediction = model.predict(img)
        predicted_class_index = np.argmax(prediction)

        if predicted_class_index < len(diseases):
            Plant = diseases[predicted_class_index][0]
            Diseased = diseases[predicted_class_index][1]
            Disease_Name = diseases[predicted_class_index][2]
            Solution = diseases[predicted_class_index][3]
            Direction = diseases[predicted_class_index][4]
        else:
            Plant = "Unknown"
            Diseased = "Unknown"
            Disease_Name = "Unknown"
            Solution = "No specific solution available."
            Direction = ""

        result = f"Plant: {Plant}\nDiseased: {Diseased}\nDisease Name: {Disease_Name}\nSolution: {Solution}\nDirection to use: {Direction}"
        return result

def display_images_and_result():
    global leaf

    original_image = Image.open(leaf)
    original_image = original_image.resize((200, 200))
    original_photo = ImageTk.PhotoImage(original_image)
    original_label = tk.Label(root, text="Original Image", font=("bold", 16), bg='white')
    original_label.place(x=380, y=280)
    original_image_label = tk.Label(root, image=original_photo)
    original_image_label.image = original_photo
    original_image_label.place(x=350, y=320)

    greyscale_image = cv2.cvtColor(cv2.imread(leaf, 1), cv2.COLOR_RGB2GRAY)
    greyscale_image = cv2.resize(greyscale_image, (200, 200))
    greyscale_photo = Image.fromarray(greyscale_image)
    greyscale_photo = ImageTk.PhotoImage(greyscale_photo)
    greyscale_label = tk.Label(root, text="Greyscale Image", font=("bold", 16), bg='white')
    greyscale_label.place(x=690, y=280)
    greyscale_image_label = tk.Label(root, image=greyscale_photo)
    greyscale_image_label.image = greyscale_photo
    greyscale_image_label.place(x=670, y=320)

    _, binary_image = cv2.threshold(greyscale_image, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
    binary_photo = Image.fromarray(binary_image)
    binary_photo = ImageTk.PhotoImage(binary_photo)
    binary_label = tk.Label(root, text="Binary Image", font=("bold", 16), bg='white')
    binary_label.place(x=1020, y=280)
    binary_image_label = tk.Label(root, image=binary_photo)
    binary_image_label.image = binary_photo
    binary_image_label.place(x=980, y=320)

    result = test_model_proc(leaf)
    update_result_message(result)
    msg = "Image testing completed.."
    update_completed_message(msg)

    analyze_button.place_forget()
    done_button.place(relx=0.5, rely=0.9, anchor="center")

def analyze_image():
    print("Analyze")
    analyze_button.config(bg='white', fg='purple', bd=1, relief='raised')
    upload_button.config(bg='purple', fg='white', bd=5, relief='sunken')

    global leaf
    if leaf != "":
        gif_path = "processing_file.gif"
        gif = Image.open(gif_path)
        gif_frames = [ImageTk.PhotoImage(frame.resize((200, 200))) for frame in ImageSequence.Iterator(gif)]
        gif_label = tk.Label(root)
        gif_label.place(relx=0.5, rely=0.5, anchor="center")

        def animate(index):
            gif_label.config(image=gif_frames[index])
            root.after(50, animate, (index + 1) % len(gif_frames))

        def run_processing():
            display_images_and_result()
            gif_label.destroy()

        root.after(0, animate, 0)
        root.after(2000, run_processing)

def on_upload_enter(event):
    upload_button.config(bg='purple', fg='white', bd=5, relief='sunken')

def on_upload_leave(event):
    upload_button.config(bg='white', fg='purple', bd=1, relief='raised')

def on_analyze_enter(event):
    analyze_button.config(bg='purple', fg='white', bd=5, relief='sunken')

def on_analyze_leave(event):
    analyze_button.config(bg='white', fg='purple', bd=1, relief='raised')

def on_done_enter(event):
    done_button.config(bg='purple', fg='white', bd=5, relief='sunken')

def on_done_leave(event):
    done_button.config(bg='white', fg='purple', bd=1, relief='raised')

def on_back_enter(event):
    back_button.config(bg='white', fg='black', bd=5, relief='sunken')

def on_back_leave(event):
    back_button.config(bg='black', fg='purple', bd=1, relief='raised')

def back_to_login():
    current_directory = os.path.dirname(os.path.abspath(__file__))
    login_file_path = os.path.join(current_directory, "Login.py")
    if os.path.exists(login_file_path):
        os.system(f'python "{login_file_path}"')
    else:
        print("Error: Login.py file not found.")

def back_to_operation():
    current_directory = os.path.dirname(os.path.abspath(__file__))
    operation_file_path = os.path.join(current_directory, "Operation.py")
    if os.path.exists(operation_file_path):
        os.system(f'python "{operation_file_path}"')
    else:
        print("Error: Operation.py file not found.")

root = tk.Tk()
root.title("Plant Disease Detection and Cure Recommendation using Machine Learning")
window_width = root.winfo_screenwidth()
window_height = root.winfo_screenheight()
root.geometry(f"{window_width}x{window_height}")
background_image = Image.open("../Images/operation_bg.jpg")
resized_image = background_image.resize((window_width, window_height))
resized_photo = ImageTk.PhotoImage(resized_image)
background_label = tk.Label(root, image=resized_photo)
background_label.place(x=0, y=0, relwidth=1, relheight=1)
heading_font = ("Helvetica", 24, "italic")
heading_label = tk.Label(root, text="Plant Disease Detection and Cure Recommendation using Machine Learning", font=heading_font, bg=root.cget("bg"))
heading_label.place(relx=0.5, rely=0.1, anchor="center")
upload_button = tk.Button(root, text="Upload Image", command=upload_image, font=('Helvetica', 16), bg='white', fg='purple', bd=1, relief='raised')
upload_button.place(relx=0.5, rely=0.25, anchor="center", width=200, height=50)
upload_button.bind("<Enter>", on_upload_enter)
upload_button.bind("<Leave>", on_upload_leave)
back_button = tk.Button(root, text="back", command=back_to_login, font=('Helvetica', 16), bg='black', fg='purple', bd=1, relief='raised')
back_button.place(x=80, y=150, width=150, height=40)
back_button.bind("<Enter>", on_back_enter)
back_button.bind("<Leave>", on_back_leave)
selected_image_label = tk.Label(root, bg='white')
selected_image_label.place(relx=0.5, rely=0.5, anchor="center")
gif_label = tk.Label(root, bg='white')
gif_label.place(relx=0.5, rely=0.5, anchor="center")
selected_image_name_label = tk.Label(root, bg='white', anchor="w", justify="left")
selected_image_name_label.place(relx=0.57, rely=0.26, anchor="w")
analyze_button = tk.Button(root, text="Analyze", command=analyze_image, font=('Helvetica', 16), bg='white', fg='purple', bd=1, relief='raised')
analyze_button.bind("<Enter>", on_analyze_enter)
analyze_button.bind("<Leave>", on_analyze_leave)
done_button = tk.Button(root, text="Done", command=back_to_operation, font=('Helvetica', 16), bg='white', fg='purple', bd=1, relief='raised')
done_button.bind("<Enter>", on_done_enter)
done_button.bind("<Leave>", on_done_leave)

root.mainloop()