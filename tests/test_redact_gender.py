import pytest

def test_redact_gender():
    files = [['*.txt']]
    data= handle_input_files(files)
    mask_data  = redactor.redact_gender(data)
    assert isinstance(mask_data,list)
