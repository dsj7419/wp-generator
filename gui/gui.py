import os
import tkinter as tk
from tkinter import filedialog, messagebox
from settings.settings import Settings
from generators.space import Space

class GUI:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("WP Generator")
        self.settings = Settings()
        self.space = Space(self.settings)

        self.width_entry = tk.Entry(self.window)
        self.height_entry = tk.Entry(self.window)
        self.browse_button = tk.Button(self.window, text="Browse", command=self.browse)
        self.generate_button = tk.Button(self.window, text="Generate", command=self.generate)
        self.progress_label = tk.Label(self.window, text="Ready")

        self.width_entry.pack()
        self.height_entry.pack()
        self.browse_button.pack()
        self.generate_button.pack()
        self.progress_label.pack()

    def browse(self):
        directory = filedialog.askdirectory()
        self.settings.directory = directory

    def generate(self):
        self.settings.width = int(self.width_entry.get())
        self.settings.height = int(self.height_entry.get())
        self.space.generate()
        self.progress_label.config(text="Image generated")

    def run(self):
        self.window.mainloop()
