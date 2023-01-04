from importlib import import_module
from pkgutil import iter_modules
from sqlalchemy.sql.schema import Table
from sys import modules
from inspect import isclass, getmembers
from sqlalchemy.sql.schema import Table

def get_class_models(return_str = True):
    '''
    Retur a dictionary with class that is a `DefaultMeta` and not `abstract` class
    '''
    from app.models.base import BaseModel
    class_models = {}
    for model_info, name, ispkg in iter_modules(__path__):
        module = import_module(f'{__name__}.{name}')
        for class_name, obj in getmembers(modules[module.__name__], isclass):
            if (issubclass(obj, BaseModel) and obj.__abstract__ is False) or isinstance(obj, Table):
                if class_models.get(class_name, False) is False:
                    class_models[class_name] = obj
    return class_models

def import_class():
    dic = get_class_models()
