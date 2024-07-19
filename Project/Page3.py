import tkinter as tk
import cv2
import numpy as np
from tkinter import Scale, Button, Label, Tk, filedialog, messagebox
from PIL import Image, ImageTk
import os

class ImageProcessingApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Page 3")
        self.master.geometry("900x900") 
        self.master.resizable(False, False)  
        self.master.configure(bg="Khaki")
        self.slider_row = 2
        
        self.image_label = Label(master)
        self.image_label.grid(row=0, column=0, columnspan=3, padx=10, pady=10, sticky="nsew")  # Image label at top
        
        self.load_image_button = Button(self.master, text="Load image", bg="Purple", fg="white", width=10, height=1, font=30, activebackground="red", cursor="bottom_side", command=self.load_image)
        self.load_image_button.grid(row=1, column=0, pady=10)

        self.save_image_button = Button(self.master, text="Save image", bg="Blue", fg="white", width=10, height=1, font=30, activebackground="green", cursor="bottom_side", command=self.save_image)
        self.save_image_button.grid(row=1, column=1, pady=10)

        self.Next_Page_button = Button(self.master, text="Next Page", bg="green", fg="white", width=12, height=1, font=30, cursor="sb_right_arrow", command=self.open_page4)
        self.Next_Page_button.grid(row=7, column=2, pady=10)

        self.Last_Page_button = Button(self.master, text="Previous page", bg="red", fg="white", width=12, height=1, font=30, cursor="sb_left_arrow", command=self.open_page2)
        self.Last_Page_button.grid(row=7, column=0, pady=10)

        self.add_buttons_and_sliders()
        self.load_default_image()

    def load_default_image(self):
        path = "image.jpg"
        self.original_image = cv2.imread(path)
        self.update_image(self.original_image)

    def load_image(self):
        file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.jpg;*.jpeg;*.png")])
        if file_path:
            self.original_image = cv2.imread(file_path)
            self.update_image(self.original_image)
            self.Zero_Slider()
        else:
            messagebox.showerror("Error", "Failed to load image.")

    def save_image(self):
            if hasattr(self, 'edited_image'):
                file_path = filedialog.asksaveasfilename(defaultextension=".jpg", filetypes=[("JPEG files", "*.jpg"), ("PNG files", "*.png"), ("All files", "*.*")])
                if file_path:
                    cv2.imwrite(file_path, cv2.cvtColor(np.array(self.edited_image), cv2.COLOR_RGB2BGR))
                    messagebox.showinfo("Image Saved", f"Image successfully saved to {file_path}")
            else:
                messagebox.showwarning("No Image", "No edited image to save. Please load and edit an image first.")
    def update_image(self, image):
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        image = Image.fromarray(image)
        
        # Resize image to fit within a maximum size
        max_width = 800
        max_height = 500
        image.thumbnail((max_width, max_height))
        
        self.edited_image = image
        image = ImageTk.PhotoImage(image)

        self.image_label.configure(image=image)
        self.image_label.image = image

    def add_buttons_and_sliders(self):
        self.add_button("Erosion", self.apply_erosion, 1)
        self.add_slider(1, 100, 0, self.update_erosion)

        self.add_button("Dilation", self.apply_dilation, 2)
        self.add_slider(1, 30, 0, self.update_dilation)

        self.add_button("Open", self.apply_open, 3)
        self.add_slider(1, 100, 0, self.update_open)

        self.add_button("Close", self.apply_close, 4)
        self.add_slider(1, 100, 0, self.update_close)

    def add_button(self, text, command, row):
        button = Button(self.master, text=text, command=command, bg="Pink", fg="Black", width=20, height=1, font=("verdana", 13, "bold"), cursor="hand2", activebackground="Green")
        button.grid(row=(row+1), column=0, pady=10)  # Set the row parameter to position the button

    def add_slider(self, from_, to_, default, command):
        slider_label = Label(self.master)
        slider_label.grid(row=self.slider_row, column=0, pady=5, padx=10, sticky="w")
        slider = Scale(self.master, from_=from_, to_=to_, fg="white", bg="brown", activebackground="Pink", borderwidth=2, orient=tk.HORIZONTAL, cursor="sb_h_double_arrow")
        slider.set(default)
        slider.grid(row=self.slider_row, column=1, pady=5, padx=10, sticky="ew")
        slider.bind("<ButtonRelease-1>", lambda event, cmd=command: cmd(event))
        self.slider_row += 1
    
    def Zero_Slider(self):
        self.slider_row = 2
        self.add_slider(1, 100, 0, self.update_erosion)
        self.add_slider(1, 30, 0, self.update_dilation)
        self.add_slider(1, 100, 0, self.update_open)
        self.add_slider(1, 100, 0, self.update_close)

    def apply_erosion(self):
        kernel_size = 10
        kernel = np.ones((kernel_size, kernel_size), np.uint8)
        erosion_image = cv2.erode(self.original_image, kernel, iterations=1)
        self.update_image(erosion_image)
        self.Zero_Slider()
        self.slider_row = 2
        self.add_slider(1, 100, 10, self.update_erosion)

    def update_erosion(self, event):
        kernel_size = int(event.widget.get())
        kernel = np.ones((kernel_size, kernel_size), np.uint8)
        erosion_image = cv2.erode(self.original_image, kernel, iterations=1)
        self.update_image(erosion_image)
        self.Zero_Slider()
        self.slider_row = 2
        self.add_slider(1, 100, kernel_size, self.update_erosion)

    def apply_dilation(self):
        kernel_size = 10
        kernel = np.ones((kernel_size, kernel_size), np.uint8)
        dilation_image = cv2.dilate(self.original_image, kernel, iterations=1)
        self.update_image(dilation_image)
        self.Zero_Slider()
        self.slider_row = 3
        self.add_slider(1, 100, 10, self.update_dilation)

    def update_dilation(self, event):
        kernel_size = int(event.widget.get())
        kernel = np.ones((kernel_size, kernel_size), np.uint8)
        dilation_image = cv2.dilate(self.original_image, kernel, iterations=1)
        self.update_image(dilation_image)
        self.Zero_Slider()
        self.slider_row = 3
        self.add_slider(1, 100, kernel_size, self.update_dilation)

    def apply_open(self):
        kernel_size = 10
        kernel = np.ones((kernel_size, kernel_size), np.uint8)
        open_image = cv2.morphologyEx(self.original_image, cv2.MORPH_OPEN, kernel)
        self.update_image(open_image)
        self.Zero_Slider()
        self.slider_row = 4
        self.add_slider(1, 100, 10, self.update_open)

    def update_open(self, event):
        kernel_size = int(event.widget.get())
        kernel = np.ones((kernel_size, kernel_size), np.uint8)
        open_image = cv2.morphologyEx(self.original_image, cv2.MORPH_OPEN, kernel)
        self.update_image(open_image)
        self.Zero_Slider()
        self.slider_row = 4
        self.add_slider(1, 100, kernel_size, self.update_open)

    def apply_close(self):
        kernel_size = 10
        kernel = np.ones((kernel_size, kernel_size), np.uint8)
        close_image = cv2.morphologyEx(self.original_image, cv2.MORPH_CLOSE, kernel)
        self.update_image(close_image)
        self.Zero_Slider()
        self.slider_row = 5
        self.add_slider(1, 100, 10, self.update_close)

    def update_close(self, event):
        kernel_size = int(event.widget.get())
        kernel = np.ones((kernel_size, kernel_size), np.uint8)
        close_image = cv2.morphologyEx(self.original_image, cv2.MORPH_CLOSE, kernel)
        self.update_image(close_image)
        self.Zero_Slider()
        self.slider_row = 5
        self.add_slider(1, 100, kernel_size, self.update_close)

    def open_page4(self):
        root.withdraw()
        os.system("python Page4.py") 

    def open_page2(self):
        root.withdraw()
        os.system("python Page2.py") 

root = Tk()
app = ImageProcessingApp(root)
root.mainloop()

