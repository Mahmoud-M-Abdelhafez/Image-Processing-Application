import tkinter as tk
import cv2
import numpy as np
from tkinter import Scale, Button, Label, Tk, Checkbutton, filedialog, messagebox
from PIL import Image, ImageTk
import os

class ImageProcessingApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Page 1")
        self.master.geometry("900x900") 
        self.master.resizable(False, False)  
        self.master.configure(bg="Khaki")
        
        self.slider_row = 2
        
        self.image_label = Label(master)
        self.image_label.grid(row=0, column=0, columnspan=3, padx=10, pady=10, sticky="nsew")  # Image label at top
        
        self.load_image_button = Button(self.master, text="Load image", bg="Purple", fg="white", width=10, height=1, font=30, activebackground="red", cursor="bottom_side", command=self.load_image)
        self.load_image_button.grid(row=1, column=0, pady=10)  # Load image button below image
        
        self.save_image_button = Button(self.master, text="Save image", bg="Blue", fg="white", width=10, height=1, font=30, activebackground="green", cursor="bottom_side", command=self.save_image)
        self.save_image_button.grid(row=1, column=1, pady=10)  # Save image button next to Load image button
        
        self.Next_Page_button = Button(self.master, text="Next Page", bg="green", fg="white", width=12, height=1, font=30, cursor="sb_right_arrow", command=self.open_page2)
        self.Next_Page_button.grid(row=7, column=1, pady=10) 
        
        self.add_buttons_and_sliders()
        self.load_default_image()

    def load_default_image(self):
        path = "image.jpg"
        self.original_image = cv2.imread(path)
        if self.original_image is not None:
            self.update_image(self.original_image)
        else:
            messagebox.showerror("Error", "Default image not found or could not be loaded.")

    def load_image(self):
        file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg *.jpeg *.png")])
        if file_path:
            self.original_image = cv2.imread(file_path)
            if self.original_image is not None:
                self.update_image(self.original_image)
                self.Zero_Slider()
            else:
                messagebox.showerror("Error", "Selected image could not be loaded. Please choose a valid image file.")

    def save_image(self):
        if hasattr(self, 'edited_image'):
            file_path = filedialog.asksaveasfilename(defaultextension=".jpg", filetypes=[("JPEG files", "*.jpg"), ("PNG files", "*.png"), ("All files", "*.*")])
            if file_path:
                cv2.imwrite(file_path, cv2.cvtColor(np.array(self.edited_image), cv2.COLOR_RGB2BGR))
                messagebox.showinfo("Image Saved", f"Image successfully saved to {file_path}")
        else:
            messagebox.showwarning("No Image", "No edited image to save. Please load and edit an image first.")

    def update_image(self, image):
        if image is not None:
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            image = Image.fromarray(image)
            
            # Resize image to fit within a maximum size
            max_width = 800
            max_height =500
            image.thumbnail((max_width, max_height))
            
            self.edited_image = image  # Store the edited image
            image = ImageTk.PhotoImage(image)

            self.image_label.configure(image=image)
            self.image_label.image = image

    def add_buttons_and_sliders(self):
        self.add_button("LPF", self.apply_lpf, 1)
        self.add_slider(1, 100, 0, self.update_lpf)

        self.add_button("HPF", self.apply_hpf, 2)
        self.add_slider(1, 100, 0, self.update_hpf)

        self.add_button("Mean_Filter", self.apply_mean_filter, 3)
        self.add_slider(1, 100, 0, self.update_mean_filter)

        self.add_button("Median_Filter", self.apply_median_filter, 4)
        self.add_slider(1, 100, 0, self.update_median_filter)

    def add_button(self, text, command, row):
        button = Button(self.master, text=text, command=command, bg="yellow", fg="black", width=20, height=1, font=("verdana", 13, "bold"), cursor="hand2", activebackground="Green")
        button.grid(row=(row + 1), column=0, pady=10)  # Set the row parameter to position the button

    def add_slider(self, from_, to_, default, command):
        slider_label = Label(self.master)
        slider_label.grid(row=self.slider_row, column=0, pady=5, padx=10, sticky="w")
        slider = Scale(self.master, from_=from_, to_=to_, orient=tk.HORIZONTAL, fg="white", bg="brown", activebackground="yellow", borderwidth=2, cursor="sb_h_double_arrow")
        slider.set(default)
        slider.grid(row=self.slider_row, column=1, pady=5, padx=10, sticky="ew")
        slider.bind("<ButtonRelease-1>", lambda event, cmd=command: cmd(event))
        self.slider_row += 1
    
    def Zero_Slider(self):
        self.slider_row = 2
        self.add_slider(1, 100, 0, self.update_lpf)
        self.add_slider(1, 100, 0, self.update_hpf)
        self.add_slider(1, 100, 0, self.update_mean_filter)
        self.add_slider(1, 100, 0, self.update_median_filter)
        
    def apply_lpf(self):
        kernel_size = 25  
        lpf_image = cv2.GaussianBlur(self.original_image, (kernel_size, kernel_size), 0)
        self.update_image(lpf_image)
        self.Zero_Slider()
        self.slider_row = 2
        self.add_slider(1, 100, 25, self.update_lpf)

    def update_lpf(self, event):
        kernel_size = int(event.widget.get())
        if kernel_size % 2 == 0:
            kernel_size += 1
        lpf_image = cv2.GaussianBlur(self.original_image, (kernel_size, kernel_size), 0)
        self.update_image(lpf_image)
        self.Zero_Slider()
        self.slider_row = 2
        self.add_slider(1, 100, kernel_size, self.update_lpf)

    def apply_hpf(self):
        kernel_size = 11
        gray_image = cv2.cvtColor(self.original_image, cv2.COLOR_BGR2GRAY)
        blurred_image = cv2.GaussianBlur(gray_image, (kernel_size, kernel_size), 0)
        hpf_image = cv2.subtract(gray_image, blurred_image)
        self.update_image(cv2.cvtColor(hpf_image, cv2.COLOR_GRAY2BGR))
        self.Zero_Slider()
        self.slider_row = 3
        self.add_slider(1, 100, 11, self.update_hpf)

    def update_hpf(self, event):
        kernel_size = int(event.widget.get())
        if kernel_size % 2 == 0:
            kernel_size += 1
        gray_image = cv2.cvtColor(self.original_image, cv2.COLOR_BGR2GRAY)
        blurred_image = cv2.GaussianBlur(gray_image, (kernel_size, kernel_size), 0)
        hpf_image = cv2.subtract(gray_image, blurred_image)
        self.update_image(cv2.cvtColor(hpf_image, cv2.COLOR_GRAY2BGR))
        self.Zero_Slider()
        self.slider_row = 3
        self.add_slider(1, 100, kernel_size, self.update_hpf)

    def apply_mean_filter(self):
        kernel_size = 20
        mean_image = cv2.blur(self.original_image, (kernel_size, kernel_size))
        self.update_image(mean_image)
        self.Zero_Slider()
        self.slider_row = 4
        self.add_slider(1, 100, 20, self.update_mean_filter)
       
    def update_mean_filter(self, event):
        kernel_size = int(event.widget.get())
        mean_image = cv2.blur(self.original_image, (kernel_size, kernel_size))
        self.update_image(mean_image)
        self.Zero_Slider()
        self.slider_row = 4
        self.add_slider(1, 100, kernel_size, self.update_mean_filter)

    def apply_median_filter(self):
        kernel_size = 20
        if kernel_size % 2 == 0:
            kernel_size += 1
        median_image = cv2.medianBlur(self.original_image, kernel_size)
        self.update_image(median_image)
        self.Zero_Slider()
        self.slider_row = 5
        self.add_slider(1, 100, 20, self.update_median_filter)
        
    def update_median_filter(self, event):
        kernel_size = int(event.widget.get())
        if kernel_size % 2 == 0:
            kernel_size += 1
        median_image = cv2.medianBlur(self.original_image, kernel_size)
        self.update_image(median_image)
        self.Zero_Slider()
        self.slider_row = 5
        self.add_slider(1, 100, kernel_size, self.update_median_filter)

    def open_page2(self):
        root.withdraw()
        os.system("python Page2.py") 

root = Tk()
app = ImageProcessingApp(root)
root.mainloop()
