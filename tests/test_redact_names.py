import pytest
from project1 import redactor

def test_redact_names():
    count = 0
    files = [['*.txt']]
    data = redactor.handle_input_files(files)
    mask_data = redactor.redact_names(data)
    if isinstance(mask_data,list):
        mask_str = ''.join(mask_data)
    
    if '\u2588' in mask_str:
        count += 1

    assert count >= 1

    

