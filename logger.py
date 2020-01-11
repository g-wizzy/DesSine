class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def error(prefix, line, message):
    """
    Prints the message with specific format for error

    Args:
        prefix: Will prefix the log entry
        line: Info about the line where the error occured
        message: Message to display
    """
    print(f"{bcolors.FAIL}[{prefix}] {bcolors.ENDC}{bcolors.BOLD}Line {line}{bcolors.ENDC} : {message}")

def warning(prefix, message):
    """
    Prints the message with specific format for warning

    Args:
        prefix: Will prefix the log entry
        message: Message to display
    """
    print(f"{bcolors.WARNING}[{prefix}] {bcolors.ENDC}{message}")

def info(prefix, message):
    """
    Prints the message with specific format for information

    Args:
        prefix: Will prefix the log entry
        message: Message to display
    """
    print(f"{bcolors.OKGREEN}[{prefix}] {bcolors.ENDC}{message}")