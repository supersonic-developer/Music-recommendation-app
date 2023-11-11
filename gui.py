import tkinter as tk
from tkinter import ttk
from ttkthemes import ThemedTk
from spotify_api import SpotifyAPI
from tkinter import PhotoImage


class GUI:
    def __init__(self):
        self.spotify_api = SpotifyAPI()

        # Create the main window
        self.root = ThemedTk(theme="breeze")
        self.root.geometry("800x600")
        self.root.title("Music recommendation system")
        self.root.iconbitmap('assets/main-icon.ico')

        # Create the song input widgets
        self.search_entry = IconEntry(self.root, "assets/search.png", "Get recommendations for specific song", width=35)
        self.search_entry.grid(row=0, column=0, columnspan=2)

        # Create the genre selection widgets
        self.genre_label = ttk.Label(self.root, text="Select genre:", width=30)
        self.genre_label.grid(row=1, column=0)
        self.genre_combobox = ttk.Combobox(self.root, width=30)
        self.genre_combobox.grid(row=1, column=1)

        # Create the liked songs widgets
        self.liked_songs_label = ttk.Label(self.root, text="Use liked songs:")
        self.liked_songs_label.grid(row=2, column=0)
        self.liked_songs_checkbutton = ttk.Checkbutton(self.root)
        self.liked_songs_checkbutton.grid(row=2, column=1)

        # Create the submit button
        self.submit_button = ttk.Button(self.root, text="Get recommendations", command=self.get_recommendations)
        self.submit_button.grid(row=3, column=0, columnspan=2)

        # Create the recommendations output widgets
        self.recommendations_label = ttk.Label(self.root, text="Recommendations:")
        self.recommendations_label.grid(row=4, column=0)
        self.recommendations_listbox = tk.Listbox(self.root, height=15, width=50)
        self.recommendations_listbox.grid(row=5, column=0, columnspan=2)

        # Start the event loop
        self.root.mainloop()

    def get_recommendations(self):
        # This function will be called when the submit button is clicked
        genre = self.genre_combobox.get()
        song = self.song_entry.get()
        use_liked_songs = self.liked_songs_checkbutton.instate(['selected'])

        # Get the recommendations from the Spotify API
        recommendations = self.spotify_api.get_recommendations(genre, song, use_liked_songs)

        # Clear the listbox
        self.recommendations_listbox.delete(0, tk.END)

        # Add the recommendations to the listbox
        for recommendation in recommendations:
            self.recommendations_listbox.insert(tk.END, recommendation)


class IconEntry(ttk.Frame):
    def __init__(self, parent, icon_path, placeholder, **kwargs):
        super().__init__(parent)

        # Load the icon
        self.icon = PhotoImage(file=icon_path)

        # Create the icon label
        self.icon_label = ttk.Label(self, image=self.icon)
        self.icon_label.pack(side="left")

        # Create the entry
        self.entry = PlaceholderEntry(self, placeholder, **kwargs)
        self.entry.pack(side="left", fill="x", expand=True)

    def get(self):
        return self.entry.get()
    

class PlaceholderEntry(ttk.Entry):
    def __init__(self, parent, placeholder, **kwargs):
        super().__init__(parent, **kwargs)

        self.placeholder = placeholder
        self.placeholder_color = 'grey'
        self.default_fg_color = self['foreground']

        self.bind("<FocusIn>", self._clear_placeholder)
        self.bind("<FocusOut>", self._add_placeholder)

        self._add_placeholder(None)

    def _add_placeholder(self, event):
        if self.get() == '':
            self['foreground'] = self.placeholder_color
            self.insert(0, self.placeholder)

    def _clear_placeholder(self, event):
        if self['foreground'] == self.placeholder_color:
            self.delete(0, "end")
            self['foreground'] = self.default_fg_color
            self.icursor(0)