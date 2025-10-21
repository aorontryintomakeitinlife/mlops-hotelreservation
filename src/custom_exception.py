import sys
import traceback

class CustomException(Exception):
    def __init__(self, error_message):
        super().__init__(error_message)
        self.error_message = self.get_detailed_error_message(error_message)

    @staticmethod
    def get_detailed_error_message(error_message):
        exc_type, exc_obj, exc_tb = sys.exc_info()
        if exc_tb:
            file_name = exc_tb.tb_frame.f_code.co_filename
            line_number = exc_tb.tb_lineno
            return f"Error [{exc_type.__name__}] in ({file_name}), line ({line_number}): {error_message}"
        else:
            return f"Error: {error_message}"

    def __str__(self):
        return self.error_message
