import tkinter as tk
from tkinter import filedialog, StringVar
from settings.settings import Settings
from logger.logger import Logger
from generators.space import Space
from settings.validators import validate_resolution, validate_save_path
import os


class GUI:
    def __init__(self, logger):
        self.root = tk.Tk()
        self.root.geometry('500x300')  # sets the window size
        self.root.title('WP Generator')  # sets the window title
        self.settings = Settings()
        self.logger = logger

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
        self.generate_button = tk.Button(self.root, text='Generate', command=self.generate, state='disabled')
        self.generate_button.grid(row=2, column=0)

        # Output screen
        self.output_text = tk.Text(self.root, state='disabled', width=60, height=10)
        self.output_text.grid(row=3, column=0, columnspan=3)

        # Set up input validation
        validate_resolution_cmd = self.root.register(self.validate_resolution_callback)
        width_entry.config(validate='key', validatecommand=(validate_resolution_cmd, '%P', '%s'))
        height_entry.config(validate='key', validatecommand=(validate_resolution_cmd, '%P', '%s'))

        validate_save_path_cmd = self.root.register(self.validate_save_path_callback)
        save_path_entry.config(validate='key', validatecommand=(validate_save_path_cmd, '%P', '%s'))

        # Validate initial values and enable Generate button if valid
        is_resolution_valid = validate_resolution(self.width_var.get(), self.height_var.get())
        is_save_path_valid = validate_save_path(self.save_path_var.get())

        if is_resolution_valid and is_save_path_valid:
            self.generate_button.config(state='normal')

    def browse(self):
        self.save_path_var.set(filedialog.askdirectory())

    def generate(self):
        self.output_text.config(state='normal')
        self.output_text.insert('end', 'Generating...\n')
        self.output_text.config(state='disabled')
        self.root.update()

        try:
            # Validate user input
            width = self.width_var.get()
            height = self.height_var.get()
            save_path = self.save_path_var.get()

            if not validate_resolution(width, height):
                self.logger.log_warning('Invalid resolution entered')
                self.output_text.config(state='normal')
                self.output_text.insert('end', 'Invalid resolution entered\n')
                self.output_text.config(state='disabled')
                self.root.update()
                return

            if not validate_save_path(save_path):
                self.logger.log_warning('Invalid save path entered')
                self.output_text.config(state='normal')
                self.output_text.insert('end', 'Invalid save path entered\n')
                self.output_text.config(state='disabled')
                self.root.update()
                return

            # Save the settings
            self.settings.width = int(width)
            self.settings.height = int(height)
            self.settings.save_path = save_path
            self.settings.save_settings(self.settings.__dict__)

            # Create a Space instance
            space_gen = Space(self.logger, self.settings)

            # Generate the image
            image = space_gen.generate()

            # Construct the absolute path for saving the image
            img_path = os.path.join(self.settings.save_path, 'background.jpeg')
            abs_img_path = os.path.abspath(img_path)

            # Save the image
            image.save(abs_img_path)

            self.output_text.config(state='normal')
            self.output_text.insert('end', f'Generation complete! Image saved at {img_path}\n')
            self.logger.log_info('Image generated and saved')
        except Exception as e:
            error_message = f"An error occurred while generating the image: {str(e)}"
            self.logger.log_exception(error_message)
            self.output_text.config(state='normal')
            self.output_text.insert('end', f'Error occurred: {str(e)}\n')
        finally:
            self.output_text.config(state='disabled')
            self.root.update()

    def run(self):
        self.logger.log_info('Application started')
        self.root.mainloop()
        self.logger.log_info('Application finished')

    def validate_resolution_callback(self, new_value, current_value):
        if validate_resolution(new_value, self.height_var.get()):
            self.generate_button.config(state='normal')
        else:
            self.generate_button.config(state='disabled')
        return True

    def validate_save_path_callback(self, new_value, current_value):
        if validate_save_path(new_value):
            self.generate_button.config(state='normal')
        else:
            self.generate_button.config(state='disabled')
        return True
