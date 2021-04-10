import pytest
from project1 import redactor

def test_redact_names():
    count = 0
    files = [['*.txt']]
    data = redactor.handle_input_files(files)
    mask_data = redactor.redact_names(data)
    
    assert mask_data is not None

    
    #if mask_data:
       # assert True
    #else:
       # assert False

