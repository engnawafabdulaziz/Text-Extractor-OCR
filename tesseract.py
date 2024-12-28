import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk  
import pytesseract
from pdf2image import convert_from_path
import easyocr
import os
import time
import threading


root = tk.Tk()
root.geometry("6000x5000")
root.title("تطبيق OCR")

# خلفية داكنة
bg_color = 'black'
font_main = ("Simplified Arabic", 20, "bold")
font_sub = ("Simplified Arabic", 16)
font_button = ("Simplified Arabic", 14)

root.overrideredirect(1)

screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

x = (screen_width // 2) - (600 // 2)
y = (screen_height // 2) - (700 // 2)
root.geometry(f"450x500+{x}+{y}")

bg_image = Image.open(os.path.join(os.path.dirname(__file__), "background.png"))
bg_image = bg_image.resize((600, 700), Image.Resampling.LANCZOS)
bg_photo = ImageTk.PhotoImage(bg_image)

bg_label = tk.Label(root, image=bg_photo)  
bg_label.place(x=0, y=0, relwidth=1, relheight=1)

elapsed_time = 0
timer_running = False

def move_window(event):
    root.geometry(f'+{event.x_root}+{event.y_root}')

root.bind("<B1-Motion>", move_window)

def update_timer(label):
    global elapsed_time, timer_running
    if timer_running:
        elapsed_time += 1
        label.config(text=f"Time spent: {elapsed_time} seconds")
        label.after(1000, lambda: update_timer(label))

def extract_text_from_image(image_path, label):
    global timer_running, elapsed_time
    try:
        timer_running = True
        elapsed_time = 0
        update_timer(label)

        file_name = os.path.splitext(os.path.basename(image_path))[0]
        directory = os.path.dirname(image_path)

        image = Image.open(image_path)
        text = pytesseract.image_to_string(image, lang='ara+eng')

        text_file_path = os.path.join(directory, f"{file_name}.txt")
        with open(text_file_path, 'w', encoding='utf-8') as f:
            f.write(text)

        timer_running = False
        messagebox.showinfo("Success", f"Text extracted and saved in {text_file_path}\nTime spent: {elapsed_time} seconds")
    except Exception as e:
        timer_running = False
        messagebox.showerror("Error", f"Failed to process the image: {str(e)}")

def extract_text_from_pdf(pdf_path, label):
    global timer_running, elapsed_time
    try:
        timer_running = True
        elapsed_time = 0
        update_timer(label)

        file_name = os.path.splitext(os.path.basename(pdf_path))[0]
        directory = os.path.dirname(pdf_path)

        pages = convert_from_path(pdf_path)
        text_file_path = os.path.join(directory, f"{file_name}.txt")
        with open(text_file_path, 'w', encoding='utf-8') as f:
            for page_number, page in enumerate(pages, start=1):
                text = pytesseract.image_to_string(page, lang='ara+eng')
                f.write(f"--- Page {page_number} ---\n")
                f.write(text)
                f.write("\n\n")

        timer_running = False
        messagebox.showinfo("Success", f"Text extracted and saved in {text_file_path}\nTime spent: {elapsed_time} seconds")
    except Exception as e:
        timer_running = False
        messagebox.showerror("Error", f"Failed to process the PDF file: {str(e)}")

def extract_text_easyocr(image_path, label):
    global timer_running, elapsed_time
    try:
        timer_running = True
        elapsed_time = 0
        update_timer(label)

        file_name = os.path.splitext(os.path.basename(image_path))[0]
        directory = os.path.dirname(image_path)

        reader = easyocr.Reader(['ar', 'en'])
        result = reader.readtext(image_path, detail=0)
        text = '\n'.join(result)

        text_file_path = os.path.join(directory, f"{file_name}_easyocr.txt")
        with open(text_file_path, 'w', encoding='utf-8') as f:
            f.write(text)

        timer_running = False
        messagebox.showinfo("Success", f"Text extracted and saved in {text_file_path}\nTime spent: {elapsed_time} seconds")
    except Exception as e:
        timer_running = False
        messagebox.showerror("Error", f"Failed to process the image: {str(e)}")

def select_image(label):
    image_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png;*.jpg;*.jpeg")])
    if image_path:
        threading.Thread(target=extract_text_from_image, args=(image_path, label)).start()

def select_pdf(label):
    pdf_path = filedialog.askopenfilename(filetypes=[("PDF Files", "*.pdf")])
    if pdf_path:
        threading.Thread(target=extract_text_from_pdf, args=(pdf_path, label)).start()

def select_image_easyocr(label):
    image_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png;*.jpg;*.jpeg")])
    if image_path:
        threading.Thread(target=extract_text_easyocr, args=(image_path, label)).start()

def switch_to_main():
    welcome_frame.pack_forget() 
    pdf_frame.pack_forget()
    image_frame.pack_forget()
    easyocr_frame.pack_forget()
    main_frame.pack()

def switch_to_image_frame():
    main_frame.pack_forget()
    image_frame.pack()

def switch_to_pdf_frame():
    main_frame.pack_forget()
    pdf_frame.pack()

def switch_to_easyocr_frame():
    main_frame.pack_forget()
    easyocr_frame.pack()

# Create welcome frame
welcome_frame = tk.Frame(root, bg=bg_color)
welcome_label = tk.Label(welcome_frame, text="Welcome to the OCR Application", font=font_main, bg=bg_color, fg='#f0f4ef')
welcome_label.pack(pady=40) 

app_name_label = tk.Label(welcome_frame, text="The OCR Text Extraction Application is an innovative tool for converting visual content such as images and PDF files into editable text. The application supports both Arabic and English, and uses advanced techniques like Tesseract and EasyOCR to improve text extraction accuracy.", font=font_sub, bg=bg_color, fg='#f0f4ef', wraplength=400)
app_name_label.pack(pady=20) 


button_frame = tk.Frame(welcome_frame, bg=bg_color)
start_button = tk.Button(button_frame, text="Start Using", font=font_button, bg='#66bb6a', fg='#ffffff', width=15, height=2, relief="raised", bd=4, command=switch_to_main)
start_button.pack(side=tk.LEFT, padx=7)

exit_button = tk.Button(button_frame, text="Exit", font=font_button, bg='#d32f2f', fg='#ffffff', width=15, height=2, relief="raised", bd=4, command=root.quit)  # تكبير الأزرار
exit_button.pack(side=tk.LEFT, padx=7)

button_frame.pack(pady=20)
welcome_frame.pack(expand=True, fill='both')

# Create main frame for file selection
main_frame = tk.Frame(root, bg=bg_color)
main_label = tk.Label(main_frame, text="Choose File Type", font=("Simplified Arabic", 18), fg='#ffffff', bg=bg_color)
main_label.pack(pady=20)

pdf_button = tk.Button(main_frame, text="PDF File", font=font_button, bg='#66bb6a', fg='#ffffff', width=25, height=1, relief="raised", bd=2, command=switch_to_pdf_frame)
pdf_button.pack(pady=10)

image_button = tk.Button(main_frame, text="Image", font=font_button, bg='#66bb6a', fg='#ffffff', width=25, height=1, relief="raised", bd=2, command=switch_to_image_frame)
image_button.pack(pady=10)

easyocr_button = tk.Button(main_frame, text="Use EasyOCR", font=font_button, bg='#66bb6a', fg='#ffffff', width=25, height=1, relief="raised", bd=2, command=switch_to_easyocr_frame)
easyocr_button.pack(pady=10)

# Create PDF file selection frame
pdf_frame = tk.Frame(root, bg=bg_color)
pdf_label = tk.Label(pdf_frame, text="Choose a PDF file to convert to text:", font=font_sub, bg=bg_color, fg='#f0f4ef')
pdf_label.pack(pady=10)

pdf_extract_button = tk.Button(pdf_frame, text="Choose PDF File", font=font_button, bg='#66bb6a', fg='#ffffff', width=25, height=1, relief="raised", bd=2, command=lambda: select_pdf(pdf_label))
pdf_extract_button.pack(pady=10)

pdf_back_button = tk.Button(pdf_frame, text="Back", font=font_button, bg='#ff9800', fg='#ffffff', width=25, height=1, relief="raised", bd=2, command=switch_to_main)
pdf_back_button.pack(pady=10)

# Create image file selection frame
image_frame = tk.Frame(root, bg=bg_color)
image_label = tk.Label(image_frame, text="Choose an image to convert to text:", font=font_sub, bg=bg_color, fg='#f0f4ef')
image_label.pack(pady=10)

image_extract_button = tk.Button(image_frame, text="Choose Image", font=font_button, bg='#66bb6a', fg='#ffffff', width=25, height=1, relief="raised", bd=2, command=lambda: select_image(image_label))
image_extract_button.pack(pady=10)

image_back_button = tk.Button(image_frame, text="Back", font=font_button, bg='#ff9800', fg='#ffffff', width=25, height=1, relief="raised", bd=2, command=switch_to_main)
image_back_button.pack(pady=10)

# Create EasyOCR frame for handwritten text
easyocr_frame = tk.Frame(root, bg=bg_color)
easyocr_label = tk.Label(easyocr_frame, text="Choose a handwritten image", font=font_sub, bg=bg_color, fg='#f0f4ef')
easyocr_label.pack(pady=10)

easyocr_extract_button = tk.Button(easyocr_frame, text="Choose Image", font=font_button, bg='#66bb6a', fg='#ffffff', width=25, height=1, relief="raised", bd=2, command=lambda: select_image_easyocr(easyocr_label))
easyocr_extract_button.pack(pady=10)

easyocr_back_button = tk.Button(easyocr_frame, text="Back", font=font_button, bg='#ff9800', fg='#ffffff', width=25, height=1, relief="raised", bd=2, command=switch_to_main)
easyocr_back_button.pack(pady=10)

# Display the welcome frame initially
welcome_frame.pack(expand=True, fill='both')

# Run the application
root.mainloop()
