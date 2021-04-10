import pytest

def test_phone():
    files = [['*.txt']]
    data= handle_input_files(files)
    mask_data  = redactor.redact_phones(data)
    assert isinstance(mask_data,list)
