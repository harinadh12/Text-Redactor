import pytest
from project1 import redactor

def test_redact_names():
    count = 0
    files = [['*.txt']]
    data = redactor.handle_input_files(files)
    mask_data = redactor.redact_names(data)
    
    assert isinstance(mask_data,list)

    
    #if mask_data:
       # assert True
    #else:
       # assert False

