import os


def validate_resolution(width, height):
    try:
        width = int(width)
        height = int(height)

        # Specify the maximum resolution (two 8K monitors)
        max_width = 7680
        max_height = 4320

        if width > max_width or height > max_height:
            return False

        return True
    except ValueError:
        return False



def validate_save_path(save_path):
    """
    Validates the save path entered by the user.
    Returns True if the path is valid, False otherwise.
    """
    return os.path.isdir(save_path)
