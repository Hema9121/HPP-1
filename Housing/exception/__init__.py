import os
import sys

class HousingException(Exception):
    def __init__(self,error_message:Exception,error_detail:sys):
        super().__init__(error_message)
        self.error_message=HousingException.get_detailed_error_message(error=error_message,error_detail=error_detail)
    
    @staticmethod
    def get_detailed_error_message(error:Exception,error_detail:sys):
        _,_,exec_tb=error_detail.exc_info()
        exception_block_lineno=exec_tb.tb_frame.f_lineno
        try_block_lineno=exec_tb.tb_lineno
        file_name=exec_tb.tb_frame.f_code.co_filename
        
        error_message=f"""error occure in the script : [{file_name}]
        at try block line number : [{try_block_lineno}]
        and exception_block line number : [{exception_block_lineno}]
        error message : [{str(error)}].
        """
        return error_message
    
    def __str__(self) -> str:
        return self.error_message
    
    def repr__(self):
        return HousingException.__name__.str()
    
