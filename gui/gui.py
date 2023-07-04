import os
from generators.space import Space
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
    QComboBox,
    QFormLayout,
    QCheckBox,
)
from PyQt5.QtGui import QFont, QIcon, QPixmap
from PyQt5.QtCore import Qt
from settings.settings import Settings
from logger.logger import Logger
from settings.validators import validate_resolution, validate_save_path


class GUI(QMainWindow):
    def __init__(self, logger):
        super().__init__()

        self.setWindowTitle("WP Generator")
        self.setWindowIcon(QIcon("assets/icon.png"))
        self.settings = Settings()
        self.logger = logger
        self.space_gen = Space(self.logger, self.settings)

        # Main Widget
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        main_layout = QVBoxLayout()
        main_widget.setLayout(main_layout)

        # Logo
        logo_label = QLabel()
        logo_label.setAlignment(Qt.AlignCenter)
        pixmap = QPixmap("assets/logo.png")
        logo_label.setPixmap(
            pixmap.scaled(200, 200, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        )
        main_layout.addWidget(logo_label)

        # Title
        title_label = QLabel("WP Generator")
        title_label.setAlignment(Qt.AlignCenter)
        title_font = QFont("Arial", 18, QFont.Bold)
        title_label.setFont(title_font)
        main_layout.addWidget(title_label)

        # Generator selection
        generator_label = QLabel("Generator:")
        main_layout.addWidget(generator_label)

        self.generator_combo_box = QComboBox()
        self.generator_combo_box.addItem("Please select the generator")
        self.generator_combo_box.addItems(["Space"])  # Add more generators as needed
        self.generator_combo_box.currentIndexChanged.connect(self.generate_settings_menu)
        main_layout.addWidget(self.generator_combo_box)

        # Settings layout
        self.settings_layout = QFormLayout()
        main_layout.addLayout(self.settings_layout)

        # Resolution settings
        self.width_line_edit = QLineEdit(str(self.settings.width))
        self.width_line_edit.setFixedWidth(60)
        self.settings_layout.addRow("Width:", self.width_line_edit)

        self.height_line_edit = QLineEdit(str(self.settings.height))
        self.height_line_edit.setFixedWidth(60)
        self.settings_layout.addRow("Height:", self.height_line_edit)

        # Save path setting
        self.save_path_line_edit = QLineEdit(self.settings.save_path)
        self.settings_layout.addRow("Save path:", self.save_path_line_edit)

        browse_button = QPushButton("Browse")
        browse_button.clicked.connect(self.browse)
        self.settings_layout.addRow("", browse_button)

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

        # Connect generator combo box signal
        self.generator_combo_box.currentIndexChanged.connect(self.generate_settings_menu)

        # Generate settings menu for the default generator
        self.generate_settings_menu()

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

            generator = self.generator_combo_box.currentText()
            if generator == "Space":
                image = self.space_gen.generate()
            else:
                # Handle other generators here
                self.logger.log_warning(f"Generator '{generator}' is not implemented.")

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

    def generate_settings_menu(self):
        generator = self.generator_combo_box.currentText()

        while self.settings_layout.count():
            item = self.settings_layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.setParent(None)

        if generator == "Space":
            # Add Space generator settings outline
            label = QLabel("Space Generator Settings:")
            self.settings_layout.addRow(label)

            # Resolution settings
            self.width_line_edit = QLineEdit(str(self.settings.width))
            self.width_line_edit.setFixedWidth(60)
            self.settings_layout.addRow("Width:", self.width_line_edit)

            self.height_line_edit = QLineEdit(str(self.settings.height))
            self.height_line_edit.setFixedWidth(60)
            self.settings_layout.addRow("Height:", self.height_line_edit)

            # Save path setting
            self.save_path_line_edit = QLineEdit(self.settings.save_path)
            self.settings_layout.addRow("Save path:", self.save_path_line_edit)

            browse_button = QPushButton("Browse")
            browse_button.clicked.connect(self.browse)
            self.settings_layout.addRow("", browse_button)

            # Enable Galaxies
            galaxies_checkbox = QCheckBox("Enable Galaxies")
            galaxies_checkbox.setChecked(self.space_gen.is_space_setting_enabled("galaxies"))
            galaxies_checkbox.stateChanged.connect(
                lambda state: self.toggle_category_settings(state, "galaxies")
            )
            self.settings_layout.addRow(galaxies_checkbox)

            if self.space_gen.is_space_setting_enabled("galaxies"):
                # Number of Galaxies
                self.num_galaxies_line_edit = QLineEdit(str(self.space_gen.settings.num_galaxies))
                self.num_galaxies_line_edit.setFixedWidth(60)
                self.settings_layout.addRow("Number of Galaxies:", self.num_galaxies_line_edit)

                # Minimum Galaxy Diameter
                self.min_galaxy_diameter_line_edit = QLineEdit(str(self.space_gen.settings.min_galaxy_diameter))
                self.min_galaxy_diameter_line_edit.setFixedWidth(60)
                self.settings_layout.addRow("Minimum Galaxy Diameter:", self.min_galaxy_diameter_line_edit)

                # Maximum Galaxy Diameter
                self.max_galaxy_diameter_line_edit = QLineEdit(str(self.space_gen.settings.max_galaxy_diameter))
                self.max_galaxy_diameter_line_edit.setFixedWidth(60)
                self.settings_layout.addRow("Maximum Galaxy Diameter:", self.max_galaxy_diameter_line_edit)

                # Colors
                self.colors_line_edit = QLineEdit(str(self.space_gen.settings.colors))
                self.colors_line_edit.setFixedWidth(200)
                self.settings_layout.addRow("Colors:", self.colors_line_edit)

            # Enable Shooting Stars
            shooting_stars_checkbox = QCheckBox("Enable Shooting Stars")
            shooting_stars_checkbox.setChecked(self.space_gen.is_space_setting_enabled("shooting_stars"))
            shooting_stars_checkbox.stateChanged.connect(
                lambda state: self.toggle_category_settings(state, "shooting_stars")
            )
            self.settings_layout.addRow(shooting_stars_checkbox)

            if self.space_gen.is_space_setting_enabled("shooting_stars"):
                # Number of Shooting Stars
                self.num_shooting_stars_line_edit = QLineEdit(str(self.space_gen.settings.num_shooting_stars))
                self.num_shooting_stars_line_edit.setFixedWidth(60)
                self.settings_layout.addRow("Number of Shooting Stars:", self.num_shooting_stars_line_edit)

                # Shooting Star Length
                self.shooting_star_length_line_edit = QLineEdit(str(self.space_gen.settings.shooting_star_length))
                self.shooting_star_length_line_edit.setFixedWidth(60)
                self.settings_layout.addRow("Shooting Star Length:", self.shooting_star_length_line_edit)

            # Enable Perlin Noise
            perlin_noise_checkbox = QCheckBox("Enable Perlin Noise")
            perlin_noise_checkbox.setChecked(self.space_gen.is_space_setting_enabled("perlin_noise"))
            perlin_noise_checkbox.stateChanged.connect(
                lambda state: self.toggle_category_settings(state, "perlin_noise")
            )
            self.settings_layout.addRow(perlin_noise_checkbox)

            if self.space_gen.is_space_setting_enabled("perlin_noise"):
                # Perlin Octaves
                self.perlin_octaves_line_edit = QLineEdit(str(self.space_gen.settings.perlin_octaves))
                self.perlin_octaves_line_edit.setFixedWidth(60)
                self.settings_layout.addRow("Perlin Octaves:", self.perlin_octaves_line_edit)

                # Perlin Persistence
                self.perlin_persistence_line_edit = QLineEdit(str(self.space_gen.settings.perlin_persistence))
                self.perlin_persistence_line_edit.setFixedWidth(60)
                self.settings_layout.addRow("Perlin Persistence:", self.perlin_persistence_line_edit)

                # Perlin Scale
                self.perlin_scale_line_edit = QLineEdit(str(self.space_gen.settings.perlin_scale))
                self.perlin_scale_line_edit.setFixedWidth(60)
                self.settings_layout.addRow("Perlin Scale:", self.perlin_scale_line_edit)

        else:
            # Handle other generators here
            self.logger.log_warning(f"Generator '{generator}' is not implemented.")

    def toggle_category_settings(self, state, category):
        if state == Qt.Checked:
            if category == "galaxies":
                self.space_gen.enable_space_setting("galaxies")
            elif category == "shooting_stars":
                self.space_gen.enable_space_setting("shooting_stars")
            elif category == "perlin_noise":
                self.space_gen.enable_space_setting("perlin_noise")
        else:
            if category == "galaxies":
                self.space_gen.disable_space_setting("galaxies")
            elif category == "shooting_stars":
                self.space_gen.disable_space_setting("shooting_stars")
            elif category == "perlin_noise":
                self.space_gen.disable_space_setting("perlin_noise")

        self.generate_settings_menu()
