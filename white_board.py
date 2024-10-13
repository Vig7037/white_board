import customtkinter as ctk
from tkinter.colorchooser import askcolor
from tkinter import filedialog
from PIL import ImageGrab, Image, ImageTk
import os

def start_drawing(event):
    global is_drawing, prev_x, prev_y
    is_drawing = True
    prev_x, prev_y = event.x, event.y

def draw(event):
    global is_drawing, prev_x, prev_y
    if is_drawing:
        current_x, current_y = event.x, event.y
        canvas.create_line(prev_x, prev_y, current_x, current_y, fill=drawing_color, width=line_width, capstyle=ctk.ROUND, smooth=True)
        prev_x, prev_y = current_x, current_y

def stop_drawing(event):
    global is_drawing
    is_drawing = False

def change_pen_color():
    global drawing_color
    color = askcolor()[1]
    if color:
        drawing_color = color

def change_line_width(value):
    global line_width
    line_width = int(value)

def save_canvas():
    # Save the canvas content as an image
    file_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png"), ("All files", "*.*")])
    if file_path:
        # Save the current canvas as an image
        x = root.winfo_rootx() + canvas.winfo_x()
        y = root.winfo_rooty() + canvas.winfo_y()
        x1 = x + canvas.winfo_width()
        y1 = y + canvas.winfo_height()
        ImageGrab.grab().crop((x, y, x1, y1)).save(file_path)

def open_image():
    # Open an existing image file and load it onto the canvas
    file_path = filedialog.askopenfilename(filetypes=[("PNG files", "*.png"), ("All files", "*.*")])
    if file_path:
        image = Image.open(file_path)
        image = image.resize((canvas.winfo_width(), canvas.winfo_height()), Image.ANTIALIAS)
        image_tk = ImageTk.PhotoImage(image)
        canvas.create_image(0, 0, anchor='nw', image=image_tk)
        canvas.image_tk = image_tk  # Keep reference to prevent garbage collection

def reset_canvas():
    # Clear the canvas completely
    canvas.delete("all")

def undo_last_action():
    # Optional undo feature: undo the last action on the canvas
    items = canvas.find_all()
    if items:
        canvas.delete(items[-1])

# Initialize the customtkinter application
ctk.set_appearance_mode("System")  # Modes: "System" (default), "Dark", "Light"
ctk.set_default_color_theme("blue")  # Themes: "blue" (default), "dark-blue", "green"

root = ctk.CTk()
root.title("Whiteboard App")

canvas = ctk.CTkCanvas(root, bg="white")
canvas.pack(fill="both", expand=True)

is_drawing = False
drawing_color = "black"
line_width = 2

root.geometry("800x600")

# Controls frame using CTkFrame
controls_frame = ctk.CTkFrame(root)
controls_frame.pack(side="top", fill="x")

# Color change button using CTkButton
color_button = ctk.CTkButton(controls_frame, text="Change Color", command=change_pen_color)
clear_button = ctk.CTkButton(controls_frame, text="Clear Canvas", command=reset_canvas)
undo_button = ctk.CTkButton(controls_frame, text="Undo", command=undo_last_action)

# Save and open file buttons
save_button = ctk.CTkButton(controls_frame, text="Save", command=save_canvas)
open_button = ctk.CTkButton(controls_frame, text="Open", command=open_image)

color_button.pack(side="left", padx=5, pady=5)
clear_button.pack(side="left", padx=5, pady=5)
undo_button.pack(side="left", padx=5, pady=5)
save_button.pack(side="left", padx=5, pady=5)
open_button.pack(side="left", padx=5, pady=5)

# Line width label and slider
line_width_label = ctk.CTkLabel(controls_frame, text="Line Width:")
line_width_label.pack(side="left", padx=5, pady=5)

line_width_slider = ctk.CTkSlider(controls_frame, from_=1, to=10, orientation="horizontal", command=change_line_width)
line_width_slider.set(line_width)
line_width_slider.pack(side="left", padx=5, pady=5)

# Bind the canvas events for drawing
canvas.bind("<Button-1>", start_drawing)
canvas.bind("<B1-Motion>", draw)
canvas.bind("<ButtonRelease-1>", stop_drawing)

root.mainloop()
