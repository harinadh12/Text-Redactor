import pytest

def test_phone():
    files = [['*.txt']]
    data= handle_input_files(files)
    mask_data  = redactor.redact_gender(data)
    assert isinstance(mask_data,list)
