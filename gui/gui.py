import os
from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QLabel,
    QLineEdit,
    QPushButton,
    QTextEdit,
    QMessageBox,
    QFileDialog,
    QVBoxLayout,
    QWidget,
    QHBoxLayout,
)
from PyQt5.QtGui import QFont, QIcon, QPixmap
from PyQt5.QtCore import Qt
from settings.settings import Settings
from logger.logger import Logger
from generators.space import Space
from settings.validators import validate_resolution, validate_save_path


class GUI(QMainWindow):
    def __init__(self, logger):
        super().__init__()

        self.setWindowTitle("WP Generator")
        self.setWindowIcon(QIcon("assets/icon.png"))
        self.settings = Settings()
        self.logger = logger

        # Main Widget
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        main_layout = QVBoxLayout()
        main_widget.setLayout(main_layout)

        # Logo
        logo_label = QLabel()
        logo_label.setAlignment(Qt.AlignCenter)
        pixmap = QPixmap("assets/logo.png")
        logo_label.setPixmap(pixmap.scaled(200, 200, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        main_layout.addWidget(logo_label)

        # Title
        title_label = QLabel("WP Generator")
        title_label.setAlignment(Qt.AlignCenter)
        title_font = QFont("Arial", 18, QFont.Bold)
        title_label.setFont(title_font)
        main_layout.addWidget(title_label)

        # Resolution settings
        resolution_label = QLabel("Resolution:")
        main_layout.addWidget(resolution_label)

        resolution_layout = QHBoxLayout()
        main_layout.addLayout(resolution_layout)

        self.width_line_edit = QLineEdit(str(self.settings.width))
        self.width_line_edit.setFixedWidth(60)
        resolution_layout.addWidget(self.width_line_edit)

        x_label = QLabel("x")
        x_label.setAlignment(Qt.AlignCenter)
        x_label.setFixedWidth(20)
        resolution_layout.addWidget(x_label)

        self.height_line_edit = QLineEdit(str(self.settings.height))
        self.height_line_edit.setFixedWidth(60)
        resolution_layout.addWidget(self.height_line_edit)

        # Save path setting
        save_path_label = QLabel("Save path:")
        main_layout.addWidget(save_path_label)

        save_path_layout = QHBoxLayout()
        main_layout.addLayout(save_path_layout)

        self.save_path_line_edit = QLineEdit(self.settings.save_path)
        save_path_layout.addWidget(self.save_path_line_edit)

        browse_button = QPushButton("Browse")
        browse_button.clicked.connect(self.browse)
        save_path_layout.addWidget(browse_button)

        # Generate button
        generate_button = QPushButton("Generate")
        generate_button.setEnabled(False)
        generate_button.clicked.connect(self.generate)
        main_layout.addWidget(generate_button)
        self.generate_button = generate_button

        # Output screen
        self.output_text = QTextEdit()
        self.output_text.setReadOnly(True)
        main_layout.addWidget(self.output_text)

        # Set up input validation
        self.width_line_edit.textChanged.connect(self.validate_input)
        self.height_line_edit.textChanged.connect(self.validate_input)
        self.save_path_line_edit.textChanged.connect(self.validate_input)

        # Validate initial values and enable Generate button if valid
        self.validate_input()

    def browse(self):
        save_path = QFileDialog.getExistingDirectory(self, "Select Save Path")
        if save_path:
            self.save_path_line_edit.setText(save_path)

    def generate(self):
        self.output_text.append("Generating...")

        try:
            width = int(self.width_line_edit.text())
            height = int(self.height_line_edit.text())
            save_path = self.save_path_line_edit.text()

            self.settings.width = width
            self.settings.height = height
            self.settings.save_path = save_path
            self.settings.save_settings(self.settings.__dict__)

            space_gen = Space(self.logger, self.settings)
            image = space_gen.generate()

            img_path = os.path.join(save_path, "background.jpeg")
            abs_img_path = os.path.abspath(img_path)
            image.save(abs_img_path)

            self.output_text.append(f"Generation complete! Image saved at {img_path}")
            self.logger.log_info("Image generated and saved")
        except Exception as e:
            error_message = f"An error occurred while generating the image: {str(e)}"
            self.logger.log_exception(error_message)
            self.output_text.append(f"Error occurred: {str(e)}")

    def validate_input(self):
        width = self.width_line_edit.text()
        height = self.height_line_edit.text()
        save_path = self.save_path_line_edit.text()

        is_resolution_valid = validate_resolution(width, height)
        is_save_path_valid = validate_save_path(save_path)

        self.generate_button.setEnabled(is_resolution_valid and is_save_path_valid)

    def closeEvent(self, event):
        self.logger.log_info("Application finished")
        event.accept()
