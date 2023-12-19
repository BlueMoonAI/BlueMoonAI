import os

from logly import Logly

logly = Logly()
logly.start_logging()

logly.set_default_max_file_size(50)
logger = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../log.txt")
logly.set_default_file_path(logger)