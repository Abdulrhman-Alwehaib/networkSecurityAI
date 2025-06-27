import sys
from networksecurity.logging import logger
class NetworkSecurityException(Exception):
    def __init__(self,error_message,error_details:sys):
        self.error_message = error_message
        _,_,exc_tb = error_details.exc_info()

        self.lineno = exc_tb.tb_lineno
        self.file_name = exc_tb.tb_frame.f_code.co_filename

    def __str__(self):
        return "\n\n\n\n \033[91mError occured in file named: [{0}], line number: [{1}], error message [{2}]\033[0m\n\n".format(
            self.file_name,self.lineno,self.error_message
        )
