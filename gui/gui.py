# gui.py
import tkinter as tk
from tkinter import filedialog, StringVar
from settings.settings import Settings
from generators.space import Space
import os

class GUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.geometry('500x300')  # sets the window size
        self.root.title('WP Generator')  # sets the window title
        self.settings = Settings()

        self.width_var = StringVar(self.root, value=str(self.settings.width))
        self.height_var = StringVar(self.root, value=str(self.settings.height))
        self.save_path_var = StringVar(self.root, value=self.settings.save_path)

        self.create_widgets()

    def create_widgets(self):
        # Resolution settings
        resolution_label = tk.Label(self.root, text='Resolution:')
        resolution_label.grid(row=0, column=0)

        width_entry = tk.Entry(self.root, textvariable=self.width_var)
        width_entry.grid(row=0, column=1)

        height_entry = tk.Entry(self.root, textvariable=self.height_var)
        height_entry.grid(row=0, column=2)

        # Save path setting
        save_path_label = tk.Label(self.root, text='Save path:')
        save_path_label.grid(row=1, column=0)

        save_path_entry = tk.Entry(self.root, textvariable=self.save_path_var)
        save_path_entry.grid(row=1, column=1)

        browse_button = tk.Button(self.root, text='Browse', command=self.browse)
        browse_button.grid(row=1, column=2)

        # Generate button
        generate_button = tk.Button(self.root, text='Generate', command=self.generate)
        generate_button.grid(row=2, column=0)

        # Output screen
        self.output_text = tk.Text(self.root, state='disabled', width=60, height=10)
        self.output_text.grid(row=3, column=0, columnspan=3)

    def browse(self):
        self.save_path_var.set(filedialog.askdirectory())

    def generate(self):
        self.output_text.config(state='normal')
        self.output_text.insert('end', 'Generating...\n')
        self.output_text.config(state='disabled')
        self.root.update()

        # Save the settings
        self.settings.width = int(self.width_var.get())
        self.settings.height = int(self.height_var.get())
        self.settings.save_path = self.save_path_var.get()
        self.settings.save_settings(self.settings.__dict__)

        # Create a Space instance
        space_gen = Space(self.settings)

        # Generate the image
        image = space_gen.generate()

        # Construct the absolute path for saving the image
        img_path = os.path.join(self.settings.save_path, 'background.jpeg')
        abs_img_path = os.path.abspath(img_path)

        # Save the image
        image.save(abs_img_path)

        self.output_text.config(state='normal')
        self.output_text.insert('end', f'Generation complete! Image saved at {img_path}\n')
        self.output_text.config(state='disabled')
        self.root.update()

    def run(self):
        self.root.mainloop()


if __name__ == '__main__':
    gui = GUI()
    gui.run()