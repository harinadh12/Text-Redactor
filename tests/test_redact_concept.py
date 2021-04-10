mport pytest

def test_redact_concept():
    files = [['*.txt']]
    data= handle_input_files(files)
    concept = ['court','state']
    mask_data  = redactor.redact_concept(data, concept)
    assert isinstance(mask_data,list)
