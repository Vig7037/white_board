import customtkinter as ctk
from tkinter.colorchooser import askcolor

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

ctk.set_appearance_mode("System")  
ctk.set_default_color_theme("dark-blue")

root = ctk.CTk()
root.title("Whiteboard App")

canvas = ctk.CTkCanvas(root, bg="white")
canvas.pack(fill="both", expand=True)

is_drawing = False
drawing_color = "black"
line_width = 2

root.geometry("800x600")

+controls_frame = ctk.CTkFrame(root)
controls_frame.pack(side="top", fill="x")

color_button = ctk.CTkButton(controls_frame, text="Change Color", command=change_pen_color)
clear_button = ctk.CTkButton(controls_frame, text="Clear Canvas", command=lambda: canvas.delete("all"))

color_button.pack(side="left", padx=5, pady=5)
clear_button.pack(side="left", padx=5, pady=5)

line_width_label = ctk.CTkLabel(controls_frame, text="Line Width:")
line_width_label.pack(side="left", padx=5, pady=5)

line_width_slider = ctk.CTkSlider(controls_frame, from_=1, to=10, orientation="horizontal", command=change_line_width)
line_width_slider.set(line_width)
line_width_slider.pack(side="left", padx=5, pady=5)

canvas.bind("<Button-1>", start_drawing)
canvas.bind("<B1-Motion>", draw)
canvas.bind("<ButtonRelease-1>", stop_drawing)

root.mainloop()
