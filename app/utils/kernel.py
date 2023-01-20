import enum
from re import search, sub

from functools import wraps
from unicodedata import normalize, category
from werkzeug.urls import url_parse
from flask import request

from flask import url_for, g, session, request


ALPHABET = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz_123456789'
def validate_password(password):
    '''
    Valida uma senha com a regra:
    Senha deve conter mais que 6 caracteres;
    Senha deve conter um número
    Senha deve conter uma letra maiúscula
    Senha deve conter uma letra minúscula
    retorna um dicionário onde `ok` terá o resultado da validação com `True` se vaidado ou `False` se conter alguma inconsistêcnia
    '''

    valid_pass = {}
    valid_pass['length'] = len(password) >= 6
    valid_pass['digit'] = not search(r'\d', password) is None
    valid_pass['uppercase'] = not search(r'[A-Z]', password) is None
    valid_pass['lowercase'] = not search(r'[a-z]', password) is None
    # valid_pass['special_char'] = search(r"[ !#$%&'()*+,-./[\\\]^_`{|}~"+r'"]', password) is not None
    valid_pass['ok'] = all(valid_pass.values())
    return valid_pass


def strip_accents(string:str):
    '''Remove acentos da string'''
    return ''.join(c for c in normalize('NFD', string)
                    if category(c)  != 'Mn')

def only_letters(string:str, lower:bool=True) -> str:
    """Return only letter of a given `string` 

    Args:
        string (str): The string that will be processes
        lower (bool, optional): if is `False` return the case of given string, else will lower case. Defaults to True.

    Returns:
        str: Return the string with only letters
    """    
    text = strip_accents(string)
    text = text.replace(' ', '_')
    text = ''.join([x for x in text if x in ALPHABET])
    if lower is True:
        return text.lower()
    return text

def only_numbers(string:str) -> str:
    """return only number in string

    Args:
        string (str): string to be processed

    Returns:
        str: string with only numbers
    """    
    return sub("[^0-9]", "", string)
def url_in_host(url):
    if url_parse(url).netloc == url_parse(request.base_url).netloc:
        return True
    return False


def order_dict(dictionary: dict, size:int =5, summarize=False,other_key:str='Outros', extra_size:bool=False):
    '''
    Ordena um dicionário recebido pelos valores, recorda de acordo com o `size` informado.
    insere os valores restantes em uma chave `other_key`
    '''

    _nd = dict(sorted(dictionary.items(), key= lambda item: item[1], reverse=True))
    agg = 0
    if summarize:
        if not extra_size:
            size = size-1
        for i, _d in enumerate(list(_nd.items())):
            if i >= size:
                agg += dictionary[_d[0]]
                _nd.pop(_d[0], None)

        if other_key in _nd.keys():
            agg += _nd[other_key]
            _nd[other_key] = agg
        else:
            _nd[other_key] = agg
        _nd = dict(sorted(_nd.items(), key= lambda item: item[1], reverse=True))
        return _nd

    for i, _d in enumerate(list(_nd.items())):
        if i >= size:
            _nd.pop(_d[0], None)
    return _nd


def format_number_as_thousand(number: int):
    '''formata um número como milhar com ponto (.)'''
    return f'{number:,d}'.replace(',','.')


def validate_cpf(value:str) -> bool:
    """Validate a given string and validate as CPF

    Args:
        value (str): CPF, can be formated as 000.000.000-00 or only numbers

    Returns:
        str: True if given value is a valid CPF or false
    """    
    cpf = only_numbers(value)
    if len(cpf) != 11 or len(set(cpf)) == 1:
        return False
    sum_of_products = sum(int(a)*int(b) for a, b in zip(cpf[0:9], range(10, 1, -1)))
    expected_digit = (sum_of_products * 10 % 11) % 10
    if int(cpf[9]) != expected_digit:
        return False
    
    sum_of_products = sum(int(a)*int(b) for a, b in zip(cpf[0:10], range(11, 1, -1)))
    expected_digit = (sum_of_products * 10 % 11) % 10
    if int(cpf[10]) != expected_digit:
        return False
    return True
