**<h1>WP Generator</h1>**

WP Generator is a program that allows you to generate custom wallpapers with various patterns and designs. It provides a user-friendly interface to customize the resolution and save path of the generated wallpapers. Please note that WP Generator is still a work in progress, and additional features, such as AI generative art, will be incorporated in the future.

**<h2>Installation</h2>**

To run WP Generator, you need to have the following dependencies installed:

    Python 3.7 or above
    PyQt5
    NumPy
    Pillow

You can install the dependencies by running the following command:<br>
```pip freeze > requirements.txt```<br>
```pip install -r requirements.txt```

**<h2>Usage</h2>**
<h3>Running from Shell</h3><br>
To run WP Generator from the shell, navigate to the project directory and execute the following command:<br>

```python main.py```

This will launch the application, and you can interact with the graphical user interface to generate wallpapers.
Building Executable

WP Generator can also be converted into a standalone executable file using the provided build.bat file. Follow the steps below to create the executable:

    Ensure you have the necessary dependencies installed as mentioned in the installation section.

    Open the command prompt and navigate to the project directory.

    Run the following command: build.bat

    This will check for the required Python packages and create a standalone executable using PyInstaller.

    After successful execution, you will find the generated executable in the dist folder.

**<h2>Contributing</h2>**
We welcome contributions to enhance WP Generator and make it even more powerful. If you have any suggestions, bug reports, or feature requests, please feel free to open an issue or submit a pull request on the GitHub repository.
License

*WP Generator is released under the MIT License.*

**<h2>Acknowledgements</h2>**
We would like to thank the open-source community for their valuable contributions and the creators of the dependencies used in this project.
