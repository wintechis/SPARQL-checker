import logging as log
from typing import List

class Logger():
    """Wrapper class for logging functions
    """
    def __init__(self, output_file: str, handle_errors: bool) -> None:
        self.out = output_file
        self.use_log = handle_errors
        self.configure_log()
        self.start = self.get_current_log_lines()

    def configure_log(self) -> None:
        """set basic line format"""
        log.basicConfig(filename=self.out,
                            filemode='a',
                            level=log.INFO,
                            format='%(asctime)s : %(levelname)8s : %(message)s',
                            datefmt='%Y-%m-%d %H:%M:%S')

    def get_current_log_lines(self) -> int:
        """returns number of lines
        """
        return len(self.get_file_lines(self.out))

    def get_file_lines(self, file: str) -> List[str]:
        """Copy from file_handling to escape circular import
        """
        with open(file, 'r', encoding='utf8') as f:
            return [line.strip() for line in f.readlines() if not line.startswith('#')]

    def compare_lines(self) -> bool:
        """ Returns True if log file did not add lines during program execution
        """
        return self.start == self.get_current_log_lines()

    def log_msg(self, e: Exception, msg: str, level: int) -> None:
        """write to logfile
        """
        if not self.use_log: raise e
        log.log(level, msg)

