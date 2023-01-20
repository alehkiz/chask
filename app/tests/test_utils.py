import pytest
from app.utils.kernel import validate_password, strip_accents, only_letters, url_in_host, order_dict

def test_validate_password_only_numbers():
    password = '123'
    test = validate_password(password)
    valid = {'length': False,
            'digit': True,
            'uppercase': False,
            'lowercase': False,
            'ok': False}
    assert test == valid

def test_validate_password_only_letters():
    password = 'abc'
    test = validate_password(password)
    valid = {'length': False,
            'digit': False,
            'uppercase': False,
            'lowercase': True,
            'ok': False}
    assert test == valid

def test_validate_password_only_letters_and_one_upper():
    password = 'Abc'
    test = validate_password(password)
    valid = {'length': False,
            'digit': False,
            'uppercase': True,
            'lowercase': True,
            'ok': False}
    assert test == valid

def test_validate_password_only_letters_six_length():
    password = 'abcdef'
    test = validate_password(password)
    valid = {'length': True,
            'digit': False,
            'uppercase': False,
            'lowercase': True,
            'ok': False}
    assert test == valid

def test_validate_password_only_letters_six_length_upper():
    password = 'Abcdef'
    test = validate_password(password)
    valid = {'length': True,
            'digit': False,
            'uppercase': True,
            'lowercase': True,
            'ok': False}
    assert test == valid

def test_validate_password_only_letters_six_length_upper_number():
    password = 'Abcde1'
    test = validate_password(password)
    valid = {'length': True,
            'digit': True,
            'uppercase': True,
            'lowercase': True,
            'ok': True}
    assert test == valid


def strip_accents_without_accents():
        value = 'Teste se acento nenhum'
        test = strip_accents(value)
        assert value == test