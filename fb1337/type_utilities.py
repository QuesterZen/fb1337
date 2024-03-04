# FBl337
# Programming Code Golf Language
# Created: 21 February 2024
# Version: 21 February 2024 12:00PM
# Copyright: James Leibert 2024
# Licence: Available for use under the GPL3 Licence https://www.gnu.org/licenses/gpl-3.0.txt

# type_utilities.py
# This module contains various utilities that depend on knowledge of specific types
# or which can make use of more than one type. By placing these methods here, it means
# that no part of the program needs to have knowledge of multiple types, and types do not
# need knowledge of each other


import numpy as np

from fb1337.array import Array, FlatList, Matrix, Coordinate, StructuredArray
from fb1337.dictionary import Dictionary
from fb1337.iterators import Iterator
from fb1337.slice import Slice
from fb1337.lambda_fn import Lambda, fc2fn


def truthy_object(obj):
    """Interpret any value as True or False"""
    if obj is None: return False
    if type(obj) is bool: return obj is True
    if type(obj) is np.bool_: return obj is np.True_
    if type(obj) is int: return obj != 0
    if type(obj) is float or type(obj) is np.float_: return obj != 0
    if type(obj) is str: return obj != ''
    if isinstance(obj, FlatList): return len(obj.all_values()) != 0
    if type(obj) is list or type(obj) is tuple: return len(obj) != 0
    return True


def int_value(obj):
    """Attempt to interpret the value as an integer value"""
    if type(obj) is int or type(obj) is float or type(obj) is Matrix.data_type or type(obj) is np.float_:
        return obj
    elif obj is None or obj == '' or obj is False:
        return 0
    elif obj is True:
        return 1
    elif is_num_collection(obj) and len(obj.values) == 1:
        return obj.values[0]
    elif type(obj) is str:
        try:
            return int(obj)
        except ValueError:
            pass
    return None


number_aliases = {'h': 100, 'k': 1000, 'm': 1000000, 't': 10, 'l': 50, 'f': 15, 'F': 255}


def to_char(value):
    if type(value) is str and len(value) == 1:
        return value
    elif is_number(value):
        return chr(int(value))
    else:
        return str(value)[0] if len(str(value)) > 0 else ''


def is_null(obj):
    return obj == '' or obj == 'Ø' or obj is None


def is_num_collection(obj):
    """Identify types that consist of a list of values"""
    if isinstance(obj, Array): return all([is_number(x) for x in obj.all_values()])
    if isinstance(obj, Matrix): return True
    return False


def is_list_or_tuple(obj):
    """Identify parameters passed in as Python lists or tuples"""
    return type(obj) is list or type(obj) is tuple


def is_number(obj):
    """Identify number-like values"""
    return type(obj) in (int, float, bool, np.float_, np.int_)


def is_lambda(obj):
    """Identify Lambda objects or similar that can be run with .go(env)"""
    return isinstance(obj, Lambda)


def is_function(obj):
    """Identify runnable objects"""
    return is_lambda(obj) or type(obj).__name__ == 'function'


def parse_program_parameter(parameter):
    """Interprets program parameters into valid program types"""

    if type(parameter) is int:
        return parameter

    if type(parameter) is bool:
        # Boolean values are 0 and 1 in fb1337
        return int(parameter)

    if type(parameter) is str:
        # Null can be entered as a symbol, otherwise a string is a literal
        if object == 'Ø':
            return ''
        elif parameter in number_aliases:
            return number_aliases[parameter]
        else:
            return parameter

    if type(parameter) is float:
        # Floats are not an allowed type except as components of a matrix
        new_object = Matrix([parameter])
        return new_object

    if type(parameter) is dict:
        # Python dictionaries are converted into Dictionary types
        new_object = Dictionary()
        for k, v in parameter.items():
            new_object.set(k, parse_program_parameter(v))
        return new_object

    if is_list_or_tuple(parameter) and \
            len(parameter) > 0 and \
            all([is_list_or_tuple(x) for x in parameter]) and \
            len(parameter[0]) > 0 and \
            all([len(x) == len(parameter[0]) for x in parameter]) and \
            all([is_number(x) for row in parameter for x in row]):
        new_object = Matrix(parameter)
        return new_object

    if is_list_or_tuple(parameter) and \
            len(parameter) > 0 and \
            all([is_list_or_tuple(x) for x in parameter]):
        # A list of lists
        return FlatList([FlatList(p) for p in parameter])

    if is_list_or_tuple(parameter) and \
            all([is_number(x) for x in parameter]) and \
            not all([type(x) is int for x in parameter]):
        # A list of numbers including at least one float is assumed to be a vector not a list
        new_object = Matrix(parameter)
        return new_object

    if is_list_or_tuple(parameter) and \
            all([is_number(x) for x in parameter]):
        # A list of numbers that is not a Matrix is assumed to be a list of integers
        new_object = FlatList([int(x) for x in parameter])
        return new_object

    if is_list_or_tuple(parameter):
        # Any other list is assumed to be a list of objects
        new_object = FlatList([parse_program_parameter(x) for x in parameter])
        return new_object

    if is_function(parameter) and \
            parameter.__code__.co_argcount == 1:
        # Lambda functions can be used a parameters and are valid stack values
        # They should take the current environment as their only parameter
        return parameter

    # Anything else is simply used as is in the hope the program can make sense of it
    return parameter


def return_value(stack_dump):
    def return_value_rec(final, remove_null=True):
        if final == '' or final is None:
            return None
        elif type(final) is tuple or is_number(final) or type(final) is str:
            return final
        elif isinstance(final, Array):
            if isinstance(final, Matrix):
                if len(final.all_values()) == 1:
                    return round(final.all_values()[0], 2)
                else:
                    return final.structured_values().round(2).tolist()
            elif not final.is_structured():
                if len(final.all_values()) == 1:
                    return final.all_values()[0]
                elif isinstance(final, FlatList) and remove_null:
                    return [return_value_rec(x, False) for x in final.all_values() if x != '']
                else:
                    return [return_value_rec(x, False) for x in final.all_values()]
            else:
                if len(final.all_values()) == 1:
                    return final.all_values()[0]
                else:
                    return [return_value_rec(x, False) for x in final.structured_values()]
        else:
            return final

    if type(stack_dump) is list or type(stack_dump) is tuple:
        if len(stack_dump) == 1:
            return return_value_rec(stack_dump[0], True)
        else:
            return [return_value_rec(x, False) for x in stack_dump if x != '' and x is not None]


def parameter_match(parameters, type_signature):
    """Determines whether a given list of parameters complies with the type_signature"""

    # Length based comparison
    if len(parameters) != len(type_signature):
        return False
    if len(type_signature) == 0:
        return True

    # Allow number unary and binary functions to be extended to lists and matrices
    if type_signature == ('int',) and isinstance(parameters[0], Array):
        return True
    if type_signature == ('int', 'int',) and isinstance(parameters[0], Array) and (
            isinstance(parameters[1], Array) or is_number(parameters[1])):
        return True

    # Otherwise we check type compliance parameter by parameter
    match_list = []
    for t, v in zip(type_signature, parameters):
        if t == 'any':
            match_list.append(True)
        elif t == 'int':
            match_list.append(is_number(v) or int_value(v) is not None)
        elif t == 'Iterator':
            match_list.append(isinstance(v, Iterator))
        elif t == 'List' or t == 'FlatList':
            match_list.append(isinstance(v, FlatList))
        elif t == 'Matrix':
            match_list.append(isinstance(v, Matrix) or isinstance(v, Matrix))
        elif t == 'Array':
            match_list.append(isinstance(v, Array))
        elif t == 'Slice':
            match_list.append(isinstance(v, Slice))
        elif t == 'Coordinate':
            match_list.append(isinstance(v, Coordinate))
        elif t == 'None':
            match_list.append(is_null(v))
        elif t == 'str':
            match_list.append(type(v) is str)
        elif t == 'Lambda':
            match_list.append(is_lambda(v))
        elif t == 'fn':
            match_list.append(is_function(v))
        elif t == 'block':
            match_list.append(type(v).__name__ == 'function')
        else:
            match_list.append(type(v).__name__ == t)
    return all(match_list)


def apply_type_transformations(parameters, type_signature, fn):
    """Assuming parameter match succeeded, this will alter the type of the parameters to
    conform to the type signature"""

    # Allow int unary and binary functions to be extended to lists and matrices
    if type_signature == ('int',) and isinstance(parameters[0], Array):
        if isinstance(parameters[0], Array):
            return parameters, lambda e, m: m.map(fc2fn(e, fn))
        else:
            raise TypeError
    if type_signature == ('int', 'int',) and isinstance(parameters[0], Array) and is_number(parameters[1]):
        if isinstance(parameters[0], Array):
            return parameters, lambda e, m, a: m.map(lambda x: fn(e, x, a))
        else:
            raise TypeError
    if type_signature == ('int', 'int',) and isinstance(parameters[0], Array) and isinstance(parameters[1], Array):
        return parameters, lambda e, m, n: m.bi_map(n, fc2fn(e, fn))

    # Otherwise there are only a small number of other type coercions that are accepted
    new_parameters = []
    for t, v in zip(type_signature, parameters):
        if t == 'int' and int_value(v) is not None:
            new_parameters.append(int_value(v))
        elif t == 'None' and is_null(v):
            new_parameters.append('')
        elif (t == 'List' or t == 'FlatList') and isinstance(v, Matrix):
            new_parameters.append(FlatList(v.values))
        elif t == 'Matrix' and is_num_collection(v) and isinstance(v, StructuredArray):
            new_parameters.append(Matrix(v.structured_values()))
        else:
            new_parameters.append(v)
    return new_parameters, fn


def convert_collection(obj, new_type):
    """Takes a python list, int, float, FlatList, Dictionary or Matrix and converts it to another type"""
    if (isinstance(obj, FlatList) or isinstance(obj, StructuredArray) or isinstance(obj,
                                                                                    Coordinate)) and new_type == 'List':
        values = [round(float(y)) if is_number(y) else y for y in obj.all_values()]
        return FlatList(values).reshape(obj.get_shape())

    if isinstance(obj, StructuredArray) and new_type == 'Matrix':
        values = obj.all_values()
        return Matrix(values).reshape(obj.get_shape())

    if type(obj) is list or type(obj) is tuple:
        values = list(obj)
    elif isinstance(obj, FlatList):
        values = obj.values
    elif isinstance(obj, Matrix):
        values = obj.values
    elif isinstance(obj, Dictionary):
        values = obj.dictionary.keys()
    elif type(obj) is str:
        values = [ord(ch) for ch in obj]
    else:
        values = [obj]
    if new_type == 'List':
        return FlatList([round(x) if type(x) is float or type(x) is Matrix.data_type else x for x in values])
    elif new_type == 'CList':
        return FlatList([to_char(x) for x in values])
    elif new_type == 'Matrix' or new_type == 'Vector':
        return Matrix([Matrix.data_type(x) for x in values])
    elif new_type == 'Dictionary':
        new_object = Dictionary()
        new_object.dictionary = {k: '' for k in values}
    elif new_type == 'str':
        ''.join([chr(x) for x in values if type(x) is int])
    else:
        return values
