from tkinter import ttk
from tkinter import PhotoImage

class IconCombobox(ttk.Frame):
    def __init__(self, master, icon_path, values, placeholder, **kwargs):
        super().__init__(master, **kwargs)

        # Load the icon
        self.icon = PhotoImage(file=icon_path)

        # Create the icon label
        self.icon_label = ttk.Label(self, image=self.icon)
        self.icon_label.grid(row=0, column=0)

        # Create the combobox
        self.placeholder = placeholder
        self.combobox = ttk.Combobox(self, values=[placeholder] + values, width=33, **kwargs)
        self.combobox.grid(row=0, column=1, sticky='ew')
        self.combobox.set(placeholder)
        self.combobox.bind("<FocusIn>", self.clear_placeholder)
        self.combobox.bind("<FocusOut>", self.set_placeholder)
        self.combobox.configure(foreground="grey")
    
    def clear_placeholder(self, event):
        if self.combobox.get() == self.placeholder:  # If the current value is the placeholder
            self.combobox.set('')  # Clear it
            self.combobox.configure(foreground="black")

    def set_placeholder(self, event):
        if self.combobox.get() == '':  # If the combobox is empty
            self.combobox.set(self.placeholder)  # Set the placeholder
            self.combobox.configure(foreground="grey")

    def get(self):
        return self.combobox.get()
    
    def grid(self, **options):
        super().grid(**options)