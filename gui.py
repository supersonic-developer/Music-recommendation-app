import tkinter as tk
from tkinter import ttk
from ttkthemes import ThemedTk
from spotify_api import SpotifyAPI
from icon_entry import IconEntry
from icon_combobox import IconCombobox
from icon_button import IconButton  
from concurrent.futures import ThreadPoolExecutor

class GUI:
    def __init__(self):
        self.spotify_api = SpotifyAPI()

        # Create the main window
        self.root = ThemedTk(theme="breeze")
        self.root.title("Music recommendation system")
        self.root.iconbitmap('assets/main-icon.ico')

        # Create the song input widget
        self.search_entry = IconEntry(self.root, "assets/search.png", "Get recommendations for specific song")
        self.search_entry.grid(row=0, column=0, sticky='w')
        self.search_entry.entry.bind("<Return>", self.on_enter_pressed)

        # Create the genre selection widgets
        self.genre_combobox = IconCombobox(self.root, "assets/genre.png", self.spotify_api.available_genres, "Get recommendations for specific genre")
        self.genre_combobox.grid(row=1, column=0, sticky='w')
        self.genre_combobox.combobox.bind("<<ComboboxSelected>>", self.on_genre_selected)

        # Create the liked songs widgets
        self.liked_songs_label = ttk.Label(self.root, text="Use liked songs:")
        self.liked_songs_label.grid(row=0, column=1, sticky='w')
        self.liked_songs_button = IconButton(self.root, "assets/like-off.png", "assets/like-on.png", self.toggle_like)
        self.liked_songs_button.grid(row=0, column=2, sticky='w')

        # Create the number of songs selection widget
        self.num_songs_label = ttk.Label(self.root, text="Number of songs:")
        self.num_songs_label.grid(row=1, column=1, sticky='w')
        self.last_valid_num_songs = "5"
        self.num_songs_spinbox = tk.Spinbox(self.root, from_=1, to=100, width=4, command=self.on_spinbox_value_changed)
        self.num_songs_spinbox.grid(row=1, column=2, sticky='w')
        self.num_songs_spinbox.delete(0, "end")
        self.num_songs_spinbox.insert(0, 5)
        self.num_songs_spinbox.bind("<Return>", self.on_spinbox_value_changed)

        # Create the recommendations output widgets
        self.recommendations_label = ttk.Label(self.root, text="Recommendations:")
        self.recommendations_label.grid(row=3, column=0, sticky='w')
        self.recommendations_text = tk.Text(self.root, height=15, width=70, wrap=tk.WORD)
        self.recommendations_text.config(state=tk.DISABLED) # Make the text widget read-only
        self.recommendations_text.grid(row=4, column=0, columnspan=3)

        # Create the progress bar widget
        self.progressbar = ttk.Progressbar(self.root, mode='indeterminate')
        self.progressbar.grid(row=5, column=0, columnspan=3, sticky='ew')

        self.executor = ThreadPoolExecutor(max_workers=1)
        
        # Start the event loop
        self.root.mainloop()

    def on_spinbox_value_changed(self, event=None):
        self.num_songs_spinbox.master.focus()
        user_input = self.num_songs_spinbox.get()
        try:
            user_input = int(user_input)
            if user_input < 1:
                num_of_recommendations = 1
                self.num_songs_spinbox.delete(0, "end")
                self.num_songs_spinbox.insert(0, 1)
            elif user_input > 100:
                num_of_recommendations = 100
                self.num_songs_spinbox.delete(0, "end")
                self.num_songs_spinbox.insert(0, 100)
            else:
                num_of_recommendations = user_input
            self.last_valid_num_songs = str(num_of_recommendations)
            self.spotify_api.num_of_recommendations = num_of_recommendations
        except ValueError:
            self.num_songs_spinbox.delete(0, "end")
            self.num_songs_spinbox.insert(0, self.last_valid_num_songs)
            self.recommendations_text.config(state=tk.NORMAL)
            self.recommendations_text.delete(1.0, tk.END)
            self.recommendations_text.insert(tk.END, "Warning: Invalid input. Please enter a number.")
            self.recommendations_text.config(state=tk.DISABLED)

    def toggle_like(self):
        self.liked_songs_button.toggle()
        # Reset other inputs
        self.search_entry.entry.delete(0, tk.END)
        self.genre_combobox.combobox.delete(0, tk.END)
        self.genre_combobox.set_placeholder(None)
        self.search_entry.entry.add_placeholder(None)   

    def on_enter_pressed(self, event):
        # Reset other inputs
        if self.liked_songs_button.button.image == self.liked_songs_button.on_image:
            self.liked_songs_button.toggle()
        self.genre_combobox.combobox.delete(0, tk.END)
        self.genre_combobox.set_placeholder(None)

        # Get the song name from the entry
        self.search_entry.master.focus()
        song_name = self.search_entry.get()
        song_id, warning = self.spotify_api.get_song_id(song_name)

        # Clear the listbox
        self.recommendations_text.config(state=tk.NORMAL)
        self.recommendations_text.delete('1.0', tk.END)

        # If there's a warning, insert it into the listbox
        if warning:
            self.recommendations_text.insert(tk.END, warning + '\n')

        self.recommendations_text.config(state=tk.DISABLED)

        if song_id is None:
            return

        future = self.executor.submit(self.spotify_api.get_recommendations_based_on_song, song_id)
        self.progressbar.start()
        self.root.after(100, self.check_future, future)  

    def on_genre_selected(self, event):
        # Reset other inputs
        if self.liked_songs_button.button.image == self.liked_songs_button.on_image:
            self.liked_songs_button.toggle()
        self.search_entry.entry.delete(0, tk.END)
        self.search_entry.entry.add_placeholder(None)

        # Get the genre from the combobox
        self.genre_combobox.master.focus()
        genre = self.genre_combobox.get()

        # Clear the listbox
        self.recommendations_text.config(state=tk.NORMAL)
        self.recommendations_text.delete('1.0', tk.END)

        future = self.executor.submit(self.spotify_api.get_recommendations_based_on_genre, genre)
        self.progressbar.start()
        self.root.after(100, self.check_future, future)

    def check_future(self, future):
        if future.done():
            recommendations = future.result()
            self.recommendations_text.config(state=tk.NORMAL)
            # Add the recommendations to the listbox
            for recommendation in recommendations:
                self.recommendations_text.insert(tk.END, recommendation + '\n')
            self.recommendations_text.config(state=tk.DISABLED)
            self.progressbar.stop()
        else:
            # Check again after 100 ms
            self.root.after(100, self.check_future, future)