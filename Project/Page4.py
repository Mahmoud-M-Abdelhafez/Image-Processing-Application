import tkinter as tk
import cv2
import numpy as np
from tkinter import Scale, Button, Label, Tk, filedialog, messagebox
from PIL import Image, ImageTk
import os

class ImageProcessingApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Page 4")
        self.master.geometry("900x900") 
        self.master.resizable(False, False)  
        self.master.configure(bg="Khaki")
        self.slider_row = 2
        
        self.image_label = Label(master)
        self.image_label.grid(row=0, column=0, columnspan=3, padx=10, pady=10, sticky="nsew")  # Image label at top
        
        self.load_image_button = Button(self.master, text="Load image", bg="Purple", fg="white", width=10, height=1, font=30, activebackground="red", cursor="bottom_side", command=self.load_image)
        self.load_image_button.grid(row=1, column=0, pady=10)  # Load image button below image
        
        self.save_image_button = Button(self.master, text="Save image", bg="Blue", fg="white", width=10, height=1, font=30, activebackground="green", cursor="bottom_side", command=self.save_image)
        self.save_image_button.grid(row=1, column=1, pady=10)
        
        self.Last_Page_button = Button(self.master, text="Previous page", bg="red", fg="white", width=12, height=1, font=30, cursor="sb_left_arrow", command=self.open_page3)
        self.Last_Page_button.grid(row=7, column=0, pady=10)

        self.add_buttons_and_sliders()
        self.load_default_image()

    def load_default_image(self):
        path = "spiderman.jpg"
        self.original_image = cv2.imread(path)
        self.update_image(self.original_image)

    def load_image(self):
        file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.jpg;*.jpeg;*.png")])
        if file_path:
            self.original_image = cv2.imread(file_path)
            self.update_image(self.original_image)
            self.slider_row = 2
            self.add_slider(1, 250, 127, self.update_thresholding_segmentation)
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
        self.add_button("Thresholding Segmentation", self.apply_thresholding_segmentation, 1)
        self.add_slider(1, 250, 127, self.update_thresholding_segmentation)
        self.add_button("Hough Circle Transform", self.apply_hough_circle_transform, 2)

    def add_button(self, text, command, row):
        button = Button(self.master, text=text, command=command, bg="Coral", fg="white", width=20, height=1, font=("verdana", 13, "bold"), cursor="hand2", activebackground="Green")
        button.grid(row=(row+1), column=0, pady=10)  # Set the row parameter to position the button

    def add_slider(self, from_, to_, default, command):
        slider_label = Label(self.master)
        slider_label.grid(row=self.slider_row, column=0, pady=5, padx=10, sticky="w")
        slider = Scale(self.master, from_=from_, to=to_, orient=tk.HORIZONTAL, fg="white", bg="brown", activebackground="Coral", borderwidth=2, cursor="sb_h_double_arrow")
        slider.set(default)
        slider.grid(row=self.slider_row, column=1, pady=5, padx=10, sticky="ew")
        slider.bind("<ButtonRelease-1>", lambda event, cmd=command: cmd(event))
        self.slider_row += 1

    def apply_thresholding_segmentation(self):
        threshold_value = 127
        gray_image = cv2.cvtColor(self.original_image, cv2.COLOR_BGR2GRAY)
        _, threshold_image = cv2.threshold(gray_image, threshold_value, 255, cv2.THRESH_BINARY)
        self.update_image(cv2.cvtColor(threshold_image, cv2.COLOR_GRAY2BGR))
        self.slider_row = 2
        self.add_slider(1, 250, 127, self.update_thresholding_segmentation)

    def update_thresholding_segmentation(self, event):
        threshold_value = int(event.widget.get())
        gray_image = cv2.cvtColor(self.original_image, cv2.COLOR_BGR2GRAY)
        _, threshold_image = cv2.threshold(gray_image, threshold_value, 255, cv2.THRESH_BINARY)
        self.update_image(cv2.cvtColor(threshold_image, cv2.COLOR_GRAY2BGR))

    def apply_hough_circle_transform(self):
        # Convert the original image to grayscale
        gray_image = cv2.cvtColor(self.original_image, cv2.COLOR_BGR2GRAY)
        # Detect circles using Hough circle transform with specified parameters
        circles = cv2.HoughCircles(gray_image, cv2.HOUGH_GRADIENT, dp=1, minDist=50, param1=100, param2=50, minRadius=0, maxRadius=0)
        # Check if any circles are detected
        if circles is not None:
            # Convert the circle parameters to integer
            circles = np.uint16(np.around(circles))
            # Create a copy of the original image for drawing circles
            hough_image = self.original_image.copy()
            # Draw detected circles on the image
            for i in circles[0, :]:
                cv2.circle(hough_image, (i[0], i[1]), i[2], (0, 255, 0), 2)  # Draw the outer circle
                cv2.circle(hough_image, (i[0], i[1]), 2, (0, 0, 255), 3)       # Draw the center of the circle
            # Update the image display with the circles drawn
            self.update_image(hough_image)

    def open_page3(self):
        root.withdraw()
        os.system("python Page3.py")

root = Tk()
app = ImageProcessingApp(root)
root.mainloop()
