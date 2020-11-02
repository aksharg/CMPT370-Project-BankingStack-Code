import pytest
from institutions import checkInstitutionSupport

def test_canadianInstitutes():
    """
    Tests the function with Canadian Bank Inputs.
    """
    assert checkInstitutionSupport("RBC") == True
    assert checkInstitutionSupport("Scotia") == True
    assert checkInstitutionSupport("TD Canada") == True
    assert checkInstitutionSupport("CIBC") == True

def test_americanInstitutes():
    """
    Tests the function with American Bank Inputs.
    """
    with pytest.raises(Exception):
        checkInstitutionSupport("wells fargo")
        checkInstitutionSupport("chase")

def test_invalidInput():
    """
    Tests the function with random string Inputs.
    """
    with pytest.raises(Exception):
        checkInstitutionSupport("a3s75y")
        checkInstitutionSupport("hello")