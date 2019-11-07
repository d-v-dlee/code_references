import logging
import string
import numpy as np

def get_logger(name):
    """
    creates a logger object to help report progress/problems in code.
    
    logger.setLevel is set to logging.Info (20) meaning it will show all 
    warning (30), error(40) and critical(50)

    inputs
    ------
    name: str, whatever you want to to name logger
    
    returns
    ------
    logger: logger object
    """
    console = logging.StreamHandler()
    logger = logging.getLogger(name)
    logger.addHandler(console)
    logger.setLevel(logging.INFO)
    return logger


def generate_random_list(size):
    """
    function for generating random list of floats and str for example.
    """
    letters = string.ascii_letters
    
    ints = list(np.random.choice(100, size=size))
    floats = [float(x + np.random.rand()) for x in ints]
    
    random = np.random.randint(0, 100)
    if random > 65:
        cutoff = np.random.randint(5, 10)
    else:
        cutoff = 0
    
    output_list = []
    for i in range(len(floats)):
        if cutoff > i:
            string_char = letters[np.random.randint(0, 52)]
            output_list.append(string_char)
        else:
            output_list.append(floats[i])
            
    return output_list


#### get_split_logger_code ####

class LessThanFilter(logging.Filter):
    def __init__(self, exclusive_maximum, name=""):
        super(LessThanFilter, self).__init__(name)
        self.max_level = exclusive_maximum

    def filter(self, record):
        #non-zero return means we log this message
        return 1 if record.levelno < self.max_level else 0


def get_split_logger(name):
    """
    creates a logger object that will write everything less than WARNING level
    to stdout and everything else to sterr.
    """
    #Get the root logger
    logger = logging.getLogger(name)
    #Have to set the root logger level, it defaults to logging.WARNING
    logger.setLevel(logging.NOTSET)

    logging_handler_out = logging.StreamHandler(sys.stdout)
    logging_handler_out.setLevel(logging.DEBUG)
    logging_handler_out.addFilter(LessThanFilter(logging.WARNING))
    logger.addHandler(logging_handler_out)

    logging_handler_err = logging.StreamHandler(sys.stderr)
    logging_handler_err.setLevel(logging.WARNING)
    logger.addHandler(logging_handler_err)
    return logger