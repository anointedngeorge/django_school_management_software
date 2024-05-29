import logging
import os

error_file_path =  os.path.realpath('error/error.log')
logging.basicConfig(
    level=logging.DEBUG,  # Set the minimum log level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler(error_file_path),
        logging.StreamHandler(),
    ]
)

def CreateErrorLog(error):
    return logging.error("An error occurred: %s", error)