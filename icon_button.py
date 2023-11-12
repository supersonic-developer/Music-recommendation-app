from tkinter import ttk
from tkinter import PhotoImage

class IconButton:
    def __init__(self, root, off_image_path, on_image_path, command):
        self.off_image = PhotoImage(file=off_image_path)
        self.on_image = PhotoImage(file=on_image_path)
        self.button = ttk.Button(root, image=self.off_image, command=command)
        self.button.image = self.off_image  # Keep a reference to the image

    def grid(self, **options):
        self.button.grid(**options)

    def toggle(self):
        if self.button.image == self.off_image:
            self.button.configure(image=self.on_image)
            self.button.image = self.on_image
        else:
            self.button.configure(image=self.off_image)
            self.button.image = self.off_image