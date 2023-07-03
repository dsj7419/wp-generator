from gui.gui import GUI
from logger.logger import Logger


def main():
    # Create an instance of the Logger class
    logger = Logger()
    logger.configure_logging()
    logger.log_info('Application started')

    try:
        # Run the GUI
        gui = GUI(logger)
        gui.run()
    except Exception as e:
        logger.log_exception('An error occurred: {}'.format(str(e)))

    logger.log_info('Application finished')


if __name__ == "__main__":
    main()
