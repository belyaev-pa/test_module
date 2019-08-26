# -*- coding: utf-8 -*-
__all__ = []

import pkgutil
import inspect
from collections import namedtuple


module_dict = dict()
DInstance = namedtuple('DInstance', ['link', 'description', 'status'])

for loader, name, is_pkg in pkgutil.walk_packages(__path__):
    module = loader.find_module(name).load_module(name)

    status, description, main = None, None, None

    for def_name, value in inspect.getmembers(module):
        if name.startswith('__'):
            continue

        globals()[def_name] = value
        if def_name == 'main':
            main = value
        elif def_name == 'DESCRIPTION':
            description = value
        elif def_name == 'status':
            status = value()
    if main is not None and description is not None and status is not None:
        module_dict[name] = DInstance(main, description, status)
    else:
        exit('Один из модулей имеет неверную архитектуру')

__all__.append(module_dict)