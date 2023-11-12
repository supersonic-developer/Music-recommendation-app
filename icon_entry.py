from tkinter import ttk
from tkinter import PhotoImage

class IconEntry(ttk.Frame):
    def __init__(self, parent, icon_path, placeholder, **kwargs):
        super().__init__(parent, **kwargs)

        # Load the icon
        self.icon = PhotoImage(file=icon_path)

        # Create the icon label
        self.icon_label = ttk.Label(self, image=self.icon)
        self.icon_label.grid(row=0, column=0)

        # Create the entry
        self.entry = PlaceholderEntry(self, placeholder, width=35, **kwargs)
        self.entry.grid(row=0, column=1, sticky='ew')

    def get(self):
        return self.entry.get()
    
    def grid(self, **options):
        super().grid(**options)
    

class PlaceholderEntry(ttk.Entry):
    def __init__(self, parent, placeholder, **kwargs):
        super().__init__(parent, **kwargs)

        self.placeholder = placeholder
        self.placeholder_color = 'grey'
        self.default_fg_color = self['foreground']

        self.bind("<FocusIn>", self.clear_placeholder)
        self.bind("<FocusOut>", self.add_placeholder)

        self.add_placeholder(None)

    def add_placeholder(self, event):
        if self.get() == '':
            self.delete(0, "end")
            self['foreground'] = self.placeholder_color
            self.insert(0, self.placeholder)

    def clear_placeholder(self, event):
        if self.get() == self.placeholder:
            self.delete(0, "end")
            self['foreground'] = self.default_fg_color
            self.icursor(0)