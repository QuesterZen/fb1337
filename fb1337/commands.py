# FBl337
# Programming Code Golf Language
# Created: 21 February 2024
# Version: 21 February 2024 12:00PM
# Copyright: James Leibert 2024
# Licence: Available for use under the GPL3 Licence https://www.gnu.org/licenses/gpl-3.0.txt

# commands.py
# Functions provided by FBl337


import math

import numpy as np
from scipy.special import comb

from fb1337.array import Array, Coordinate, Matrix, FlatList
from fb1337.dictionary import Dictionary
from fb1337.iterators import Iterator
from fb1337.slice import Slice
from fb1337.lambda_fn import Lambda, run_object, fp2fn
from fb1337.parser import add_command_signature
from fb1337.type_utilities import convert_collection, truthy_object, int_value
from fb1337.type_utilities import parameter_match

# fb1337 language commands
FBLeet_language = [

    # Maths and Logic Functions
    {'symbol': '~', 'signature': (1, 0, 0, 0), 'alias': 'neg', 'group': 'math', 'patterns': [
        {'signature': ('int',), 'description': 'negate', 'function': lambda e, a: -a},
    ]},
    {'symbol': '+', 'signature': (2, 0, 0, 0), 'alias': 'add', 'group': 'math', 'patterns': [
        {'signature': ('int', 'int',), 'description': 'addition', 'function': lambda e, a, b: a + b},
        {'signature': ('None', 'any',), 'description': 'addition', 'function': lambda e, a, b: b},
        {'signature': ('Coordinate', 'Coordinate',), 'description': 'addition',
         'function': lambda e, a, b: a + b},

    ]},
    {'symbol': '×', 'signature': (2, 0, 0, 0), 'alias': 'mul', 'group': 'math', 'patterns': [
        {'signature': ('int', 'int',), 'description': 'multiply', 'function': lambda e, a, b: a * b},
        {'signature': ('None', 'int',), 'description': 'multiply', 'function': lambda e, a, b: b},
        {'signature': ('str', 'int',), 'description': 'string repeat', 'function': lambda e, a, b: a * b},
        {'signature': ('Coordinate', 'int',), 'description': 'scalar multiply',
         'function': lambda e, a, b: a * b},
    ]},
    {'symbol': '-', 'signature': (2, 0, 0, 0), 'alias': 'sub', 'group': 'math', 'patterns': [
        {'signature': ('int', 'int',), 'description': 'subtract', 'function': lambda e, a, b: a - b},
    ]},
    {'symbol': '÷', 'signature': (2, 0, 0, 0), 'alias': 'div', 'group': 'math', 'patterns': [
        {'signature': ('Matrix', 'int',), 'description': 'divide', 'function': lambda e, a, b: a.map(lambda x: x / b)},
        {'signature': ('Matrix', 'Matrix',), 'description': 'divide',
         'function': lambda e, a, b: a.matrix_binary(b, lambda x, y: x / y)},
        {'signature': ('int', 'int',), 'description': 'integer divide', 'function': lambda e, a, b: a // b},
    ]},
    {'symbol': '%', 'signature': (2, 0, 0, 0), 'alias': 'mod', 'group': 'math', 'patterns': [
        {'signature': ('int', 'int',), 'description': 'modulo division', 'function': lambda e, a, b: a % b},
    ]},
    {'symbol': '‰', 'signature': (1, 1, 0, 0), 'alias': 'divisible by', 'group': 'math', 'patterns': [
        {'signature': ('int', 'int',), 'description': 'is divisible by', 'function': lambda e, a, b: (a % b == 0)},
    ]},
    {'symbol': '‱', 'signature': (2, 0, 0, 0), 'alias': 'divisible', 'group': 'math', 'patterns': [
        {'signature': ('int', 'int',), 'description': 'is divisible by', 'function': lambda e, a, b: (a % b == 0)},
    ]},
    {'symbol': '|', 'signature': (2, 0, 0, 0), 'alias': 'divides', 'group': 'math', 'patterns': [
        {'signature': ('int', 'int',), 'description': 'a divides b', 'function': lambda e, a, b: (b % a == 0)},
    ]},
    {'symbol': 'ℸ', 'signature': (1, 0, 0, 0), 'alias': 'prime factors', 'group': 'math', 'patterns': [
        {'signature': ('int',), 'description': 'returns a list of prime factors',
         'function': lambda e, x: FlatList.prime_factors(x)},
    ]},
    {'symbol': '𝜋', 'signature': (1, 0, 0, 0), 'alias': 'primes', 'group': 'math', 'patterns': [
        {'signature': ('Array',), 'description': 'returns nth primes for integers in the array',
         'function': lambda e, m: FlatList.primes_nth_list(m)},
        {'signature': ('int',), 'description': 'returns a list of primes up to n',
         'function': lambda e, m: FlatList.primes_up_to(m)},
    ]},
    {'symbol': '⩲', 'signature': (1, 0, 0, 0), 'alias': 'abs', 'group': 'math', 'patterns': [
        {'signature': ('int',), 'description': 'absolute value', 'function': lambda e, x: abs(x)},
    ]},
    {'symbol': '²', 'signature': (1, 0, 0, 0), 'alias': 'sqr', 'group': 'math', 'patterns': [
        {'signature': ('int',), 'description': 'square', 'function': lambda e, x: x * x},
    ]},
    {'symbol': '√', 'signature': (1, 0, 0, 0), 'alias': 'sqrt', 'group': 'math', 'patterns': [
        {'signature': ('int',), 'description': 'integer square root', 'function': lambda e, a: int(math.sqrt(a))},
        {'signature': ('Matrix',), 'description': 'square root', 'function': lambda e, a: np.sqrt(a)},
    ]},
    {'symbol': '⊛', 'signature': (1, 0, 0, 0), 'alias': 'log2', 'group': 'math', 'patterns': [
        {'signature': ('int',), 'description': 'integer log base 2', 'function': lambda e, a: int(math.log(a, 2))},
    ]},
    {'symbol': '±', 'signature': (1, 0, 0, 0), 'alias': 'sign', 'group': 'math', 'patterns': [
        {'signature': ('int',), 'description': 'sign of value as -1, 0 or 1',
         'function': lambda e, a: int((a > 0) - (a < 0))},
        {'signature': ('Coordinate',), 'description': 'grid (Manhattan) distance from origin',
         'function': lambda e, c: c.grid_len()},
    ]},
    {'symbol': '*', 'signature': (2, 0, 0, 0), 'alias': 'pow', 'group': 'math', 'patterns': [
        {'signature': ('int', 'int',), 'description': 'power x^n', 'function': lambda e, x, y: x ** y},
    ]},
    {'symbol': '⨸', 'signature': (2, 0, 0, 0), 'alias': 'gcd', 'group': 'math', 'patterns': [
        {'signature': ('int', 'int',), 'description': 'greatest common divisor',
         'function': lambda e, x, y: math.gcd(x, y)},
    ]},
    {'symbol': '⩓', 'signature': (1, 0, 0, 0), 'alias': 'inc', 'group': 'math', 'patterns': [
        {'signature': ('int',), 'description': 'increment by 1', 'function': lambda e, x: x + 1},
    ]},
    {'symbol': '⩔', 'signature': (1, 0, 0, 0), 'alias': 'dec', 'group': 'math', 'patterns': [
        {'signature': ('int',), 'description': 'decrement by 1', 'function': lambda e, x: x - 1},
    ]},
    {'symbol': '!', 'signature': (1, 0, 0, 0), 'alias': 'factorial', 'group': 'math', 'patterns': [
        {'signature': ('int',), 'description': 'factorial n!',
         'function': lambda e, x: math.factorial(x)},
    ]},
    {'symbol': '‼', 'signature': (2, 0, 0, 0), 'alias': 'binomial', 'group': 'math', 'patterns': [
        {'signature': ('int', 'int'), 'description': 'nCr binomial coefficient',
         'function': lambda e, n, r: comb(n, r, exact=True)},
    ]},
    {'symbol': '⌈', 'signature': (2, 0, 0, 0), 'alias': 'max', 'group': 'math', 'patterns': [
        {'signature': ('int', 'int'), 'description': 'maximum value',
         'function': lambda e, a, b: max(int_value(a), int_value(b))},
        {'signature': ('Matrix', 'Matrix'), 'description': 'element-wise maximum',
         'function': lambda e, a, b: Matrix.maximum(a, b)},
    ]},
    {'symbol': '⌊', 'signature': (2, 0, 0, 0), 'alias': 'min', 'group': 'math', 'patterns': [
        {'signature': ('int', 'int'), 'description': 'minimum value',
         'function': lambda e, a, b: min(int_value(a), int_value(b))},
    ]},
    {'symbol': '=', 'signature': (2, 0, 0, 0), 'alias': 'eq', 'group': 'math', 'patterns': [
        {'signature': ('int', 'int'), 'description': 'equal?', 'function': lambda e, a, b: a == b},
        {'signature': ('str', 'str'), 'description': 'string equal?', 'function': lambda e, a, b: a == b},
        {'signature': ('any', 'any'), 'description': 'equal?', 'function': lambda e, a, b: a == b},
    ]},
    {'symbol': '≠', 'signature': (2, 0, 0, 0), 'alias': 'neq', 'group': 'math', 'patterns': [
        {'signature': ('int', 'int'), 'description': 'not equal?', 'function': lambda e, a, b: a != b},
        {'signature': ('str', 'str'), 'description': 'string not equal?', 'function': lambda e, a, b: a != b},
        {'signature': ('any', 'any'), 'description': 'not equal?', 'function': lambda e, a, b: a != b},
    ]},
    {'symbol': '<', 'signature': (2, 0, 0, 0), 'alias': 'lt', 'group': 'math', 'patterns': [
        {'signature': ('int', 'int'), 'description': 'less than?', 'function': lambda e, a, b: a < b},
    ]},
    {'symbol': '≤', 'signature': (2, 0, 0, 0), 'alias': 'lte', 'group': 'math', 'patterns': [
        {'signature': ('int', 'int'), 'description': 'less than or equal?', 'function': lambda e, a, b: a <= b},
    ]},
    {'symbol': '>', 'signature': (2, 0, 0, 0), 'alias': 'gt', 'group': 'math', 'patterns': [
        {'signature': ('int', 'int'), 'description': 'greater than?', 'function': lambda e, a, b: a > b},
    ]},
    {'symbol': '≥', 'signature': (2, 0, 0, 0), 'alias': 'gte', 'group': 'math', 'patterns': [
        {'signature': ('int', 'int'), 'description': 'greater than or equal?', 'function': lambda e, a, b: a >= b},
    ]},
    {'symbol': '¬', 'signature': (1, 0, 0, 0), 'alias': 'not', 'group': 'math', 'patterns': [
        {'signature': ('Matrix',), 'description': 'logical not',
         'function': lambda e, m: m.build(np.logical_not(m.structured_values()))},
        {'signature': ('Array',), 'description': 'logical not',
         'function': lambda e, m: m.map(lambda x: int(not x))},
        {'signature': ('int',), 'description': 'logical not', 'function': lambda e, a: not a},
        {'signature': ('any',), 'description': 'logical not', 'function': lambda e, a: not truthy_object(a)},
    ]},
    {'symbol': '∧', 'signature': (2, 0, 0, 0), 'alias': 'and', 'group': 'math', 'patterns': [
        {'signature': ('Matrix', 'Matrix'), 'description': 'logical and',
         'function': lambda e, a, b: a.matrix_binary(b, lambda x, y: x and y)},
        {'signature': ('int', 'int'), 'description': 'logical and', 'function': lambda e, a, b: a and b},
        {'signature': ('any', 'any'), 'description': 'logical and', 'function': lambda e, a, b:
            b if truthy_object(a) else a},
    ]},
    {'symbol': '∨', 'signature': (2, 0, 0, 0), 'alias': 'or', 'group': 'math', 'patterns': [
        {'signature': ('Matrix', 'Matrix'), 'description': 'logical or',
         'function': lambda e, a, b: a.matrix_binary(b, lambda x, y: x or y)},
        {'signature': ('int', 'int'), 'description': 'logical or', 'function': lambda e, a, b: a or b},
        {'signature': ('any', 'any'), 'description': 'logical or',
         'function': lambda e, a, b: a if truthy_object(a) else b},
    ]},

    # Binary representation
    {'symbol': '⟘', 'signature': (2, 0, 0, 0), 'alias': 'binary', 'group': 'math', 'patterns': [
        {'signature': ('int', 'int'), 'description': 'binary value as list of length n',
         'function': lambda e, x, n: FlatList(([0] * n + [int(ch) for ch in bin(x)[2:]])[-n:])},
    ]},
    {'symbol': '⊤', 'signature': (1, 0, 0, 0), 'alias': 'from binary', 'group': 'math', 'patterns': [
        {'signature': ('str',), 'description': 'string binary number to integer',
         'function': lambda e, x: int("0b" + ''.join([ch for ch in str(x) if ch in "01"]), 2)},
        {'signature': ('Array',), 'description': 'boolean list binary representation to integer',
         'function': lambda e, x: int("0b" + ''.join(['1' if truthy_object(x) else '0' for x in x.all_values()]), 2)},
    ]},

    # Control Flow and Conditional Expressions
    {'symbol': '?', 'signature': (1, 0, 2, 0), 'alias': 'if', 'group': 'control', 'patterns': [
        {'signature': ('any', 'any', 'any'), 'description': 'if predicate ? true_fn false_fn',
         'function': lambda e, q, t, f: Lambda.late_eval(e, t if q else f)},
    ]},
    {'symbol': '⁈', 'signature': (1, 0, 1, 0), 'alias': 'if or null', 'group': 'control', 'patterns': [
        {'signature': ('any', 'any',), 'description': 'if predicate ? true_fn null',
         'function': lambda e, q, t: Lambda.late_eval(e, t if q else lambda e_: '')},
    ]},
    {'symbol': '₡', 'signature': (0, 0, 3, 0), 'alias': 'case', 'group': 'control', 'patterns': [
        {'signature': ('any', 'any', 'any'), 'description': 'case predicate true_fn false_fn',
         'function': lambda e, q, t, f: Lambda.late_eval(e, t) if [run_object(e, q), e.pop()][1] else Lambda.late_eval(
             e, f)},
    ]},
    {'symbol': '€', 'signature': (0, 0, 1, 0), 'alias': 'else', 'group': 'control', 'patterns': [
        {'signature': ('any',), 'description': 'else action_fn',
         'function': lambda e, f: run_object(e, f)},
    ]},

    # Stack Management
    {'symbol': '◌', 'signature': (1, 0, 0, 0), 'alias': 'drop', 'group': 'stack', 'patterns': [
        {'signature': ('any',), 'description': 'discard the top stack value', 'function': lambda e, _: None},
    ]},
    {'symbol': '⊢', 'signature': (1, 0, 0, 0), 'alias': 'identity', 'group': 'stack', 'patterns': [
        {'signature': ('any',), 'description': 'use the top stack value', 'function': lambda e, x: x},
    ]},
    {'symbol': '⊣', 'signature': (2, 0, 0, 0), 'alias': 'left', 'group': 'stack', 'patterns': [
        {'signature': ('any', 'any'), 'description': 'use the second stack value',
         'function': lambda e, x, y: [e.push(y), x][1]},
    ]},
    {'symbol': '⊩', 'signature': (1, 0, 0, 0), 'alias': 'copy', 'group': 'stack', 'patterns': [
        {'signature': ('any',), 'description': 'use and retain the top stack value (dup)',
         'function': lambda e, x: [e.push(x), x][1]},
    ]},
    {'symbol': '⫣', 'signature': (2, 0, 0, 0), 'alias': 'copy left', 'group': 'stack', 'patterns': [
        {'signature': ('any', 'any'), 'description': 'use and retain the second stack value (under)',
         'function': lambda e, x, y: [e.push(x), e.push(y), x][2]},
    ]},
    {'symbol': '⫤', 'signature': (0, 1, 0, 0), 'alias': 'deep', 'group': 'stack', 'patterns': [
        {'signature': ('int',), 'description': 'use and drop stack value n-back to top of stack',
         'function': lambda e, n: e.deep(n)},
    ]},
    {'symbol': '∂', 'signature': (1, 0, 0, 0), 'alias': 'dup', 'group': 'stack', 'patterns': [
        {'signature': ('any',), 'description': 'duplicate top stack value a -> aa', 'function': lambda e, x: e.dup(x)},
    ]},
    {'symbol': 'ð', 'signature': (2, 0, 0, 0), 'alias': 'dup2', 'group': 'stack', 'patterns': [
        {'signature': ('any', 'any'), 'description': 'duplicate top two stack values ab -> abab',
         'function': lambda e, x, y: e.dup2(x, y)},
    ]},
    {'symbol': '«', 'signature': (2, 0, 0, 0), 'alias': 'swap', 'group': 'stack', 'patterns': [
        {'signature': ('any', 'any'), 'description': 'swap top two stack values ab -> ba',
         'function': lambda e, x, y: e.swap(x, y)},
    ]},
    {'symbol': '⨩', 'signature': (2, 0, 0, 0), 'alias': 'under', 'group': 'stack', 'patterns': [
        {'signature': ('any', 'any'), 'description': 'duplicate second stack value to the top ab->aba',
         'function': lambda e, a, b: e.under(a, b)},
    ]},
    {'symbol': 'ḋ', 'signature': (2, 0, 0, 0), 'alias': 'dup under', 'group': 'stack', 'patterns': [
        {'signature': ('any', 'any'), 'description': 'duplicate second stack value in place ab->aab',
         'function': lambda e, a, b: e.dup_under(a, b)},
    ]},
    {'symbol': '®', 'signature': (3, 0, 0, 0), 'alias': 'rot', 'group': 'stack', 'patterns': [
        {'signature': ('any', 'any', 'any'), 'description': 'rotate the top three stack values abc -> bca',
         'function': lambda e, a, b, c: e.rotate(a, b, c)},
    ]},

    # String Functions
    {'symbol': "'", 'signature': (1, 0, 0, 0), 'alias': 'str', 'group': 'string', 'patterns': [
        {'signature': ('Array',), 'description': 'join the elements of a list as strings',
         'function': lambda e, l: l.stringify(False)},
        {'signature': ('int',), 'description': 'convert to a string', 'function': lambda e, x: str(x)},
        {'signature': ('any',), 'description': 'convert to a string', 'function': lambda e, x: str(x)},
    ]},
    {'symbol': '¦', 'signature': (1, 0, 0, 0), 'alias': 'decode', 'group': 'string', 'patterns': [
        {'signature': ('Array',), 'description': 'convert a list of ascii code points to a string',
         'function': lambda e, l: l.stringify(True)},
        {'signature': ('int',), 'description': 'convert an ascii code point to a string character',
         'function': lambda e, l: FlatList([l]).stringify(True)},
    ]},
    {'symbol': 'ℤ', 'signature': (1, 0, 0, 0), 'alias': 'integer', 'group': 'string', 'patterns': [
        {'signature': ('str',), 'description': 'convert a string to an integer value',
         'function': lambda e, x: int_value(x)},
        {'signature': ('any',), 'description': 'convert object to an integer',
         'function': lambda e, x: int_value(str(x))},
    ]},

    # List Functions
    {'symbol': '‿', 'signature': (1, 1, 0, 0), 'alias': 'pair', 'group': 'list', 'patterns': [
        {'signature': ('Array', 'Array'), 'description': 'join two lists together side by side',
         'function': lambda e, a, b: a.join_on_axis(b)},
        {'signature': ('Array', 'any'), 'description': 'add a value to a list',
         'function': lambda e, a, b: a.insert(b)},
        {'signature': ('any', 'any'), 'description': 'pair two values into a list',
         'function': lambda e, a, b: FlatList.pair(a, b)},
    ]},
    {'symbol': '⁔', 'signature': (2, 0, 0, 0), 'alias': 'extend', 'group': 'list', 'patterns': [
        {'signature': ('Array', 'Array'), 'description': 'add list as a member',
         'function': lambda e, a, b: a.extend(b)},
        {'signature': ('Array', 'int'), 'description': 'list append', 'function': lambda e, a, b: a.insert(b)},
        {'signature': ('int', 'Array'), 'description': 'list prepend', 'function': lambda e, a, b: b.insert(a, loc=0)},
        {'signature': ('Array', 'any'), 'description': 'list append', 'function': lambda e, a, b: a.insert(b)},
        {'signature': ('any', 'Array'), 'description': 'list prepend', 'function': lambda e, a, b: b.insert(a, loc=0)},
        {'signature': ('any', 'any'), 'description': 'pair values into a list',
         'function': lambda e, a, b: FlatList.pair(a, b)},
    ]},
    {'symbol': '⏍', 'signature': (0, 0, 0, 0), 'alias': 'gather', 'group': 'list', 'patterns': [
        {'signature': (), 'description': 'put all values on the stack stack (from last null) into a list',
         'function': lambda e: FlatList.stack_to_list(e)},
    ]},
    {'symbol': '☐', 'signature': (0, 1, 0, 0), 'alias': 'gather n', 'group': 'list', 'patterns': [
        {'signature': ('int',), 'description': 'put the top n items on the stack into a list',
         'function': lambda e, n: FlatList([e.pop() for _ in range(n)][::-1])},
    ]},
    {'symbol': '☆', 'signature': (1, 0, 0, 0), 'alias': 'scatter', 'group': 'list', 'patterns': [
        {'signature': ('Array',), 'description': 'put each item in the list onto the stack',
         'function': lambda e, l: [[e.push(x) for x in l.iterable()], None][1]},
        {'signature': ('any',), 'description': 'ungroup items and place each on the stack',
         'function': lambda e, l:
         [[e.push(x) for x in l] if (type(l) is list or type(l) is tuple) else [e.push(l) for _ in [1]], None][1]},
    ]},
    {'symbol': '⊟', 'signature': (1, 0, 0, 0), 'alias': 'enlist', 'group': 'list', 'patterns': [
        {'signature': ('Coordinate',), 'description': 'wrap a coordinate into a list',
         'function': lambda e, a: FlatList([a])},
        {'signature': ('Array',), 'description': 'convert a structured array into a flat list',
         'function': lambda e, a: FlatList(a.all_values())},
        {'signature': ('int',), 'description': 'wrap a value into a list',
         'function': lambda e, x: FlatList([int(x)])},
        {'signature': ('any',), 'description': 'wrap a value into a list', 'function': lambda e, x: FlatList([x])},
    ]},
    {'symbol': '⍳', 'signature': (1, 0, 0, 0), 'alias': 'iota', 'group': 'list', 'patterns': [
        {'signature': ('int',), 'description': 'list of integer values from 1 to n',
         'function': lambda e, t: FlatList.int_list(t)},
    ]},
    {'symbol': '‥', 'signature': (2, 0, 0, 0), 'alias': 'range', 'group': 'list', 'patterns': [
        {'signature': ('int', 'int'), 'description': 'list of integer values in the range m to n',
         'function': lambda e, m, n: FlatList.int_list(m, n)},
    ]},
    {'symbol': '⧉', 'signature': (2, 0, 0, 0), 'alias': 'copies', 'group': 'list', 'patterns': [
        {'signature': ('List', 'int'), 'description': 'cycle through a list n times',
         'function': lambda e, a, n: FlatList(a.iterable() * n)},
        {'signature': ('any', 'int'), 'description': 'create a list containing n copies of v',
         'function': lambda e, v, n: FlatList([v for _ in range(n)])},
    ]},
    {'symbol': 'ⁿ', 'signature': (1, 0, 0, 0), 'alias': 'digits', 'group': 'list', 'patterns': [
        {'signature': ('int',), 'description': 'list the digits of an integer value',
         'function': lambda e, x: FlatList.to_ch_list(x)},
        {'signature': ('str',), 'description': 'convert a string into a list of character code points',
         'function': lambda e, x: convert_collection(x, 'List')},
    ]},
    {'symbol': '@', 'signature': (1, 2, 0, 0), 'alias': 'replace', 'group': 'list', 'patterns': [
        {'signature': ('Array', 'any', 'any'), 'description': 'replace values in a list given by indices',
         'function': lambda e, l, s, v: l.set_indices(s, v)},
        {'signature': ('Dictionary', 'any', 'any'), 'description': 'set the value for a key',
         'function': lambda e, d, k, v: d.set(k, v)},
    ]},
    {'symbol': '٪', 'signature': (1, 1, 0, 0), 'alias': 'skip', 'group': 'list', 'patterns': [
        {'signature': ('List', 'int',), 'description': 'take every nth item in a list',
         'function': lambda e, l, n: l.skip(n)},
    ]},
    {'symbol': '[', 'signature': (1, 3, 0, 0), 'alias': 'slice.py', 'group': 'list', 'patterns': [
        {'signature': ('List', 'any', 'any', 'any'),
         'description': 'create a new list by taking a slice.py from the list [start : stop : step]',
         'function': lambda e, l, s, f, a: l.slice(Slice(s, f, a))},
        {'signature': ('str', 'any', 'any', 'any'),
         'description': 'create a new string by taking a slice.py from the string [start : stop : step]',
         'function': lambda e, l, s, f, a: Slice(s, f, a).slice_string(l)},
    ]},
    {'symbol': '{', 'signature': (0, 3, 0, 0), 'alias': 'make slice.py', 'group': 'list', 'patterns': [
        {'signature': ('any', 'any', 'any'), 'description': 'create a slice.py object [start : stop : step]',
         'function': lambda e, s, f, a: Slice(s, f, a)},
    ]},

    # Matrix Functions

    {'symbol': '𝚰', 'signature': (1, 0, 0, 0), 'alias': 'identity matrix', 'group': 'matrix', 'patterns': [
        {'signature': ('int',), 'description': 'creates a new n x n identity matrix',
         'function': lambda e, s: Matrix.identity(s)},
    ]},
    {'symbol': '𝕄', 'signature': (3, 0, 0, 0), 'alias': 'matrix fill', 'group': 'matrix', 'patterns': [
        {'signature': ('int', 'int', 'int'),
         'description': 'creates a matrix size n x m filled with a given value',
         'function': lambda e, r, c, v: Matrix.single_value_matrix(value=v, shape=(r, c))},
    ]},
    {'symbol': '⧅', 'signature': (1, 0, 0, 0), 'alias': 'diagonal matrix', 'group': 'matrix', 'patterns': [
        {'signature': ('List',),
         'description': 'creates an n x n matrix, whose diagonal elements are taken from a list',
         'function': lambda e, l: Matrix.diagonal(l.values)},
    ]},
    {'symbol': '⌸', 'signature': (0, 0, 0, 0), 'alias': 'stack2mat', 'group': 'matrix', 'patterns': [
        {'signature': (), 'description': 'convert values on the stack (from the last null) to a matrix',
         'function': lambda e: convert_collection(FlatList.stack_to_list(e).values, 'Matrix')},
    ]},
    {'symbol': '⊡', 'signature': (1, 0, 0, 0), 'alias': 'list2mat', 'group': 'matrix', 'patterns': [
        {'signature': ('List',), 'description': 'convert a flat list to a matrix',
         'function': lambda e, s: convert_collection(s, 'Matrix')},
        {'signature': ('Coordinate',), 'description': 'convert a coordinate to a matrix',
         'function': lambda e, s: convert_collection(s, 'Matrix')},
        {'signature': ('Array',), 'description': 'convert a structured array to a matrix',
         'function': lambda e, s: convert_collection(s, 'Matrix')},
    ]},
    {'symbol': '⊠', 'signature': (2, 0, 0, 0), 'alias': 'matmul', 'group': 'matrix', 'patterns': [
        {'signature': ('Array', 'Array'), 'description': 'matrix multiplication',
         'function': lambda e, a, b: a.matrix_multiply(b)},
    ]},
    {'symbol': '⌹', 'signature': (1, 0, 0, 0), 'alias': 'inverse', 'group': 'matrix', 'patterns': [
        {'signature': ('Matrix',), 'description': 'matrix inverse', 'function': lambda e, m: m.inverse()},
    ]},
    {'symbol': '𝚲', 'signature': (1, 0, 0, 0), 'alias': 'determinant', 'group': 'matrix', 'patterns': [
        {'signature': ('Matrix',), 'description': 'matrix determinant ', 'function': lambda e, m: m.determinant()},
    ]},

    # Dictionary Functions
    {'symbol': 'Δ', 'signature': (0, 1, 0, 0), 'alias': 'dictionary', 'group': 'dictionary', 'patterns': [
        {'signature': ('str',), 'description': 'create a new dictionary and assign a name',
         'function': lambda e, s: [e.assign(s, Dictionary()), e.lookup(s)][-1]},
    ]},

    # Index Functions
    {'symbol': '¢', 'signature': (1, 0, 0, 0), 'alias': 'coordinate', 'group': 'coordinate', 'patterns': [
        {'signature': ('Array',), 'description': 'create a coordinate using values from a list',
         'function': lambda e, l: Coordinate(l.iterable())},
    ]},
    {'symbol': 'ɨ', 'signature': (1, 0, 0, 0), 'alias': 'index list', 'group': 'coordinate', 'patterns': [
        {'signature': ('Coordinate',), 'description': 'convert a coordinate to a list of values',
         'function': lambda e, l: Array.demote(l)},
    ]},

    # Set Functions

    {'symbol': '⟈', 'signature': (2, 0, 0, 0), 'alias': 'exclusion', 'group': 'set', 'patterns': [
        {'signature': ('Array', 'Array'), 'description': 'set of elements in the first list not in the second',
         'function': lambda e, a, b: a.set_exclude(b)},
        {'signature': ('List', 'int'), 'description': 'the set of elements in the list excluding the given element',
         'function': lambda e, a, b: a.set_exclude(b)},
        {'signature': ('str', 'str'),
         'description': 'remove all characters from the first string that appear in the second string',
         'function': lambda e, a, b: ''.join(ch for ch in a if ch not in b)},
    ]},
    {'symbol': '∩', 'signature': (2, 0, 0, 0), 'alias': 'intersection', 'group': 'set', 'patterns': [
        {'signature': ('Array', 'Array'), 'description': 'all elements in both lists',
         'function': lambda e, a, b: a.set_intersection(b)},
        {'signature': ('str', 'str'),
         'description': 'remove all characters from the first string that do not appear in the second string',
         'function': lambda e, a, b: ''.join(ch for ch in a if ch in b)},
    ]},
    {'symbol': '∪', 'signature': (2, 0, 0, 0), 'alias': 'union', 'group': 'set', 'patterns': [
        {'signature': ('Array', 'Array'), 'description': 'all unique elements from both lists',
         'function': lambda e, l, m: l.set_union(m)},
    ]},
    {'symbol': 'ṵ', 'signature': (1, 0, 0, 0), 'alias': 'unique', 'group': 'set', 'patterns': [
        {'signature': ('Array',), 'description': 'the set of all unique items in an array',
         'function': lambda e, l: l.set_unique()},
    ]},
    {'symbol': '⬇', 'signature': (1, 0, 0, 0), 'alias': 'pop', 'group': 'set', 'patterns': [
        {'signature': ('Array',), 'description': 'removes one (unspecified) value from a set',
         'function': lambda e, l: l.pop()},
    ]},
    {'symbol': '⬆', 'signature': (2, 0, 0, 0), 'alias': 'add', 'group': 'set', 'patterns': [
        {'signature': ('Array', 'any'), 'description': 'adds a value to a set if not already present',
         'function': lambda e, l, v: l.add_value(v)},
    ]},

    # Array Conversion

    {'symbol': '⇑', 'signature': (1, 0, 0, 0), 'alias': 'promote', 'group': 'array', 'patterns': [
        {'signature': ('Array',), 'description': 'convert a flat list of lists to a structured array',
         'function': lambda e, l: Array.promote(l)},
    ]},
    {'symbol': '⇓', 'signature': (1, 0, 0, 0), 'alias': 'demote', 'group': 'array', 'patterns': [
        {'signature': ('Array',), 'description': 'demote a structured array to a flat list of lists',
         'function': lambda e, l: Array.demote(l)},
    ]},

    # Array Functions

    {'symbol': '#', 'signature': (1, 0, 0, 0), 'alias': 'count', 'group': 'array', 'patterns': [
        {'signature': ('str',), 'description': 'string length', 'function': lambda e, x: len(str(x))},
        {'signature': ('List',), 'description': 'the length of a flat list',
         'function': lambda e, l: len(l.iterable())},
        {'signature': ('Coordinate',), 'description': 'the dimension of a coordinate index',
         'function': lambda e, l: len(l.iterable())},
        {'signature': ('Array',), 'description': 'the size of the first axis of a structured array',
         'function': lambda e, l: l.count(0)},
    ]},
    {'symbol': '⤲', 'signature': (2, 0, 0, 0), 'alias': 'split', 'group': 'array', 'patterns': [
        {'signature': ('str', 'str'), 'description': 'split a string using characters from the second string',
         'function': lambda e, a, b: FlatList(str(a).split(str(b)))},
        {'signature': ('Array', 'any'), 'description': 'split a list using an element or list of elements',
         'function': lambda e, a, b: a.split(b)},
    ]},
    {'symbol': '▭', 'signature': (1, 0, 0, 0), 'alias': 'flatten', 'group': 'array', 'patterns': [
        {'signature': ('Array',), 'description': 'flatten a structured list into a 1 x n list',
         'function': lambda e, l: l.flatten()},
    ]},
    {'symbol': '⊕', 'signature': (2, 0, 0, 0), 'alias': 'join', 'group': 'array', 'patterns': [
        {'signature': ('Matrix', 'Array'), 'description': 'join structured arrays side-by-side',
         'function': lambda e, l, m: l.join_on_axis(Matrix(m.structured_values()), axis=-1)},
        {'signature': ('Array', 'Array'), 'description': 'join lists side=by-side',
         'function': lambda e, l, m: l.join_on_axis(m, axis=-1)},
        {'signature': ('str', 'str',), 'description': 'concatenate strings', 'function': lambda e, a, b: a + b},
        {'signature': ('None', 'str',), 'description': 'concatenate strings', 'function': lambda e, a, b: b},
        {'signature': ('FlatList', 'str'),
         'description': 'join strings in the list using the given string as a separator',
         'function': lambda e, a, b: b.join([str(x) for x in a.values if len(str(x)) > 0])},
    ]},
    {'symbol': 'ⓐ', 'signature': (1, 2, 0, 0), 'alias': 'replace?', 'group': 'array', 'patterns': [
        {'signature': ('Array', 'Array', 'any'),
         'description': 'set list values indicated by boolean list of the same shape',
         'function': lambda e, l, m, v: l.set_bool(m, v)},
    ]},
    {'symbol': '↑', 'signature': (1, 1, 0, 0), 'alias': 'take', 'group': 'array', 'patterns': [
        {'signature': ('Array', 'int'), 'description': 'take the first n values',
         'function': lambda e, l, i: l.take(i)},
    ]},
    {'symbol': '↓', 'signature': (1, 1, 0, 0), 'alias': 'drop', 'group': 'array', 'patterns': [
        {'signature': ('Array', 'int'), 'description': 'drop the first n values',
         'function': lambda e, l, i: l.drop(i)},
    ]},
    {'symbol': '↗', 'signature': (1, 0, 0, 0), 'alias': 'sort', 'group': 'array', 'patterns': [
        {'signature': ('Array',), 'description': 'sort the list from smallest to largest',
         'function': lambda e, l: l.sort(reverse=False)},
        {'signature': ('str',), 'description': 'sort the characters in a string from smallest to largest',
         'function': lambda e, l: ''.join(sorted([ch for ch in l], reverse=False))},
    ]},
    {'symbol': '↘', 'signature': (1, 0, 0, 0), 'alias': 'r sort', 'group': 'array', 'patterns': [
        {'signature': ('Array',), 'description': 'sort the list from largest to smallest',
         'function': lambda e, l: l.sort(reverse=True)},
        {'signature': ('str',), 'description': 'sort the characters in a string from largest to smallest',
         'function': lambda e, l: ''.join(sorted([ch for ch in l], reverse=True))},
    ]},
    {'symbol': '⍋', 'signature': (1, 0, 0, 0), 'alias': 'grade', 'group': 'array', 'patterns': [
        {'signature': ('Array',), 'description': 'indices of elements of the list in ascending sort order',
         'function': lambda e, l: l.grade()},
    ]},
    {'symbol': '⍒', 'signature': (1, 0, 0, 0), 'alias': 'r grade', 'group': 'array', 'patterns': [
        {'signature': ('Array',), 'description': 'indices of elements of the list in descending sort order',
         'function': lambda e, l: l.grade(reverse=True)},
    ]},
    {'symbol': '⊃', 'signature': (2, 0, 0, 0), 'alias': 'select?', 'group': 'array', 'patterns': [
        {'signature': ('Array', 'Array'), 'description': 'select items using a boolean list',
         'function': lambda e, l, s: l.select_bool(s)},
        {'signature': ('str', 'Array'), 'description': 'select characters of a string using a boolean list',
         'function': lambda e, st, sl: ''.join([ch for (ch, i) in zip(st, sl.all_values()) if truthy_object(i)])},
    ]},
    {'symbol': '⊇', 'signature': (2, 0, 0, 0), 'alias': 'select', 'group': 'array', 'patterns': [
        {'signature': ('str', 'Array'),
         'description': 'select characters of a string using a list of indices',
         'function': lambda e, t, s: s.select_string(t)},
        {'signature': ('Matrix', 'Coordinate'), 'description': 'select an element of a matrix using a coordinate',
         'function': lambda e, l, s: l.select_index(s)},
        {'signature': ('Array', 'Array'), 'description': 'select items using a list of indices',
         'function': lambda e, l, s: l.select_indices(s)},
        {'signature': ('Array', 'int'), 'description': "select an item from a list at a given index",
         'function': lambda e, l, i: l.select_index(i)},
        {'signature': ('str', 'int'), 'description': 'select a character from a string at a given index',
         'function': lambda e, s, i: s[i] if len(s) > i else ''},
        {'signature': ('Coordinate', 'int'), 'description': 'select the nth dimension value in a coordinate',
         'function': lambda e, c, i: c.index[i] if 0 <= i < len(c.index) else ''},
        {'signature': ('Coordinate', 'Coordinate'), 'description': 'permute one coordinate using another',
         'function': lambda e, c, s: Coordinate([c.values[i] for i in s.values])},
        {'signature': ('Dictionary', 'List'), 'description': 'fetch values from a dictionary using a list of keys',
         'function': lambda e, d, l: FlatList([d.fetch(i) for i in l.values])},
        {'signature': ('Dictionary', 'any'), 'description': 'fetch a value from a dictionary by key',
         'function': lambda e, d, i: d.fetch(i)},
    ]},
    {'symbol': '⊂', 'signature': (2, 0, 0, 0), 'alias': 'partition', 'group': 'array', 'patterns': [
        {'signature': ('Array', 'Array'),
         'description': 'partition a list using a list to indicate which partition to assign each value',
         'function': lambda e, l, s: s.partition(l)},
        {'signature': ('str', 'Array'),
         'description': 'partition a string using a list to indicate which partition to assign each character',
         'function': lambda e, t, s: s.partition(t)},
    ]},
    {'symbol': '⊆', 'signature': (2, 0, 0, 0), 'alias': 'group', 'group': 'array', 'patterns': [
        {'signature': ('Array', 'Array'), 'description': 'group elements of an array using an array as a selector',
         'function': lambda e, l, s: s.group(l)},
        {'signature': ('str', 'Array'), 'description': 'group characters in a string using an array as a selector',
         'function': lambda e, t, s: s.group(t)},
    ]},
    {'symbol': '∈', 'signature': (2, 0, 0, 0), 'alias': 'member of?', 'group': 'array', 'patterns': [
        {'signature': ('Array', 'Array'),
         'description': 'returns a boolean list indicating which items are members of the second list',
         'function': lambda e, l, m: l.member(m, method='bool')},
        {'signature': ('str', 'str'), 'description': 'is the string contained in the second string',
         'function': lambda e, a, b: a in b},
        {'signature': ('any', 'Array'), 'description': 'is the item in the list',
         'function': lambda e, a, l: a in l.unique_values()},
    ]},
    {'symbol': '⋸', 'signature': (2, 0, 0, 0), 'alias': 'find all', 'group': 'array', 'patterns': [
        {'signature': ('Array', 'Array'),
         'description': 'returns the index of the first match of any item in the first list in the second list',
         'function': lambda e, m, i: m.member(from_array=i, method='indices')},
        {'signature': ('str', 'str'),
         'description': 'returns the index of matches of items in the second string in the first string',
         'function': lambda e, s1, s2: FlatList([i for i, ch in enumerate(s1) if ch in s2])},
        {'signature': ('Array', 'any'),
         'description': 'returns the first index where the item is found in the list',
         'function': lambda e, m, i: m.member(from_array=i, method='indices')},
    ]},
    {'symbol': '∊', 'signature': (2, 0, 0, 0), 'alias': 'find all?', 'group': 'array', 'patterns': [
        {'signature': ('Array', 'Array'),
         'description': 'returns a boolean list indicating where a member of the second list appears in the first list',
         'function': lambda e, m, i: m.member(from_array=i, method='bool')},
        {'signature': ('str', 'str'),
         'description': 'returns a boolean list indicating where in the first string any character in the second appears',
         'function': lambda e, s1, s2: FlatList([ch in s2 for ch in s1])},
        {'signature': ('Array', 'any'),
         'description': 'returns a boolean list indicating where the value appears in the list',
         'function': lambda e, m, i: m.member(from_array=i, method='bool')},
    ]},
    {'symbol': '⋥', 'signature': (2, 0, 0, 0), 'alias': 'bool list', 'group': 'array', 'patterns': [
        {'signature': ('Array', 'Array'),
         'description': 'converts a list of indices to a boolean mask given a template list',
         'function': lambda e, il, t: il.bool_mask_from_indices(t)},
        {'signature': ('Array', 'int'),
         'description': 'converts a list of indices to a boolean mask given a length',
         'function': lambda e, il, t: il.bool_mask_from_indices(t)},
    ]},
    {'symbol': '⊒', 'signature': (1, 0, 0, 0), 'alias': 'indices', 'group': 'array', 'patterns': [
        {'signature': ('Array',),
         'description': 'converts a boolean mask into a list of indices',
         'function': lambda e, b: b.indices_from_bool_mask()},
    ]},
    {'symbol': '⊐', 'signature': (1, 0, 0, 0), 'alias': 'first index', 'group': 'array', 'patterns': [
        {'signature': ('Array',),
         'description': 'index of the first 1 in a boolean list',
         'function': lambda e, b: b.first_index_from_bool_mask()},
    ]},
    {'symbol': '⊏', 'signature': (1, 0, 0, 0), 'alias': 'classify', 'group': 'array', 'patterns': [
        {'signature': ('Array',),
         'description': 'return array containing the indices of the first of each unique value in the list',
         'function': lambda e, l: l.classify()},
    ]},

    # Higher Level Array Functions
    {'symbol': '¨', 'signature': (1, 0, 1, 0), 'alias': 'map', 'group': 'high level fns', 'patterns': [
        {'signature': ('Array', 'fn'),
         'description': 'apply the function to each value of the array and return a new array of the same shape',
         'function': lambda e, l, f: l.map(fp2fn(e, f, 1))},
        {'signature': ('str', 'fn'),
         'description': 'apply the function to each character in the string and return the result in a list',
         'function': lambda e, s, f: convert_collection(s, 'CList').map(fp2fn(e, f, 1))},
    ]},
    {'symbol': '}', 'signature': (1, 0, 1, 0), 'alias': 'filter', 'group': 'high level fns', 'patterns': [
        {'signature': ('Array', 'fn'), 'description': 'remove values for which the function returns a falsy value',
         'function': lambda e, l, f: l.filter(fp2fn(e, f, 1))},
    ]},
    {'symbol': '/', 'signature': (1, 0, 1, 0), 'alias': 'reduce', 'group': 'high level fns', 'patterns': [
        {'signature': ('List', 'fn'),
         'description': 'apply the function between each value in a flat list',
         'function': lambda e, l, f: l.reduce(fp2fn(e, f, 2), axis=-1)},
        {'signature': ('Array', 'fn'),
         'description': 'apply the function between each sub-array on the last axis of a structured array',
         'function': lambda e, l, f: l.reduce(fp2fn(e, f, 2), axis=-1)},
    ]},
    {'symbol': '⧈', 'signature': (1, 1, 1, 0), 'alias': 'window', 'group': 'high level fns', 'patterns': [
        {'signature': ('Array', 'int', 'fn'),
         'description': 'perform a reduction on an n x n... window around each cell',
         'function': lambda e, l, n, f: l.window(n, fp2fn(e, f, 2))},
    ]},
    {'symbol': '⌺', 'signature': (1, 1, 1, 0), 'alias': 'stencil', 'group': 'high level fns', 'patterns': [
        {'signature': ('Array', 'int', 'fn'),
         'description': 'perform a reduction on an n x n... window around each cell, including edge cells',
         'function': lambda e, l, n, f: l.window(n, fp2fn(e, f, 2), edges=True)},
    ]},
    {'symbol': '⥆', 'signature': (1, 0, 1, 0), 'alias': 'fold r', 'group': 'high level fns', 'patterns': [
        {'signature': ('Array', 'fn'), 'description': 'apply the function between each value and the remaining list',
         'function': lambda e, l, f: l.reduce(fp2fn(e, f, 2), axis=-1, reverse=True, partial_sums=False)},
    ]},
    {'symbol': '∖', 'signature': (1, 0, 1, 0), 'alias': 'scan', 'group': 'high level fns', 'patterns': [
        {'signature': ('Array', 'fn'), 'description': 'provide the partial sums of a reduction',
         'function': lambda e, l, f: l.reduce(fp2fn(e, f, 2), axis=0, partial_sums=True)},
    ]},
    {'symbol': '⥶', 'signature': (1, 0, 1, 0), 'alias': 'scan r', 'group': 'high level fns', 'patterns': [
        {'signature': ('Array', 'fn'), 'description': 'provide the partial sums of a right fold reduction',
         'function': lambda e, l, f: l.reduce(fp2fn(e, f, 2), axis=0, reverse=True, partial_sums=True)},
    ]},
    {'symbol': '⌿', 'signature': (1, 0, 1, 0), 'alias': 'col reduce', 'group': 'high level fns', 'patterns': [
        {'signature': ('Array', 'fn'), 'description': 'reduce on first axis (apply the reduction to each column)',
         'function': lambda e, l, f: l.reduce(fp2fn(e, f, 2), axis=0)},
    ]},
    {'symbol': '⋯', 'signature': (1, 0, 1, 0), 'alias': 'row map', 'group': 'high level fns', 'patterns': [
        {'signature': ('Array', 'fn'),
         'description': 'apply a function to each row of an array and return the results as a list',
         'function': lambda e, a, f: a.map_on_axis(fp2fn(e, f, 1), axis=0)},
    ]},
    {'symbol': '⋮', 'signature': (1, 0, 1, 0), 'alias': 'col map', 'group': 'high level fns', 'patterns': [
        {'signature': ('Array', 'fn'),
         'description': 'apply a function to each column of an array and return the results as a list',
         'function': lambda e, a, f: a.map_on_axis(fp2fn(e, f, 1), axis=-1)},
    ]},
    {'symbol': '⊚', 'signature': (2, 0, 1, 0), 'alias': 'outer-product', 'group': 'high level fns', 'patterns': [
        {'signature': ('Array', 'str', 'fn'),
         'description': 'table given by applying the function to all pairings of items in the list and characters in the string',
         'function': lambda e, a, b, f: a.outer_product(convert_collection(b, 'CList'), fp2fn(e, f, 2))},
        {'signature': ('str', 'List', 'fn'),
         'description': 'table given by applying the function to all pairings of items in the list and characters in the string',
         'function': lambda e, a, b, f: convert_collection(a, 'CList').outer_product(b, fp2fn(e, f, 2))},
        {'signature': ('Array', 'Array', 'fn'),
         'description': 'table given by applying the function to all pairings of items in the two lists',
         'function': lambda e, a, b, f: a.outer_product(b, fp2fn(e, f, 2))},
        {'signature': ('str', 'str', 'fn'),
         'description': 'table given by applying the function to all pairings of characters in the two strings',
         'function': lambda e, a, b, f: convert_collection(a, 'CList').outer_product(convert_collection(b, 'CList'),
                                                                                     fp2fn(e, f, 2))},
    ]},
    {'symbol': '•', 'signature': (2, 0, 2, 0), 'alias': 'inner-product', 'group': 'high level fns', 'patterns': [
        {'signature': ('Array', 'Array', 'fn', 'fn'),
         'description': 'inner product of two arrays formed by applying the first function to the results of the product of the rows from the first array and columns of the second',
         'function': lambda e, a, b, f, g: a.inner_product(b, fp2fn(e, f, 2), fp2fn(e, g, 2))},
    ]},

    # Structured Array Functions
    {'symbol': '⌘', 'signature': (1, 3, 0, 0), 'alias': 'set coord', 'group': 'structured array', 'patterns': [
        {'signature': ('Array', 'int', 'int', 'any'), 'description': 'set a matrix element value',
         'function': lambda e, l, x, y, v: l.set_index(Coordinate((x, y)), v)},
    ]},
    {'symbol': '𝖗', 'signature': (2, 0, 0, 0), 'alias': 'row', 'group': 'structured array', 'patterns': [
        {'signature': ('Array', 'int'), 'description': 'select a row of an array',
         'function': lambda e, l, n: l.choose_slice_on_axis(n=n, axis=0)},
    ]},
    {'symbol': '𝖈', 'signature': (2, 0, 0, 0), 'alias': 'col', 'group': 'structured array', 'patterns': [
        {'signature': ('Array', 'int'), 'description': 'select a column of an array',
         'function': lambda e, l, n: l.choose_slice_on_axis(n=n, axis=-1)},
    ]},
    {'symbol': '⍴', 'signature': (3, 0, 0, 0), 'alias': 'reshape', 'group': 'structured array', 'patterns': [
        {'signature': ('Array', 'int', 'int'), 'description': 'reshape an 2-dimensional structured array',
         'function': lambda e, a, r, c: a.reshape((r, c))},
    ]},
    {'symbol': 'ῤ', 'signature': (2, 0, 0, 0), 'alias': 'chunk', 'group': 'structured array', 'patterns': [
        {'signature': ('Array', 'int'), 'description': 'break an array into n-length chunks',
         'function': lambda e, a, c: a.reshape((0, c))},
    ]},
    {'symbol': '⦰', 'signature': (1, 0, 0, 0), 'alias': 'transpose', 'group': 'structured array', 'patterns': [
        {'signature': ('Array',), 'description': 'transpose the rows and columns of a structured array',
         'function': lambda e, l: l.transpose()},
    ]},
    {'symbol': '⎅', 'signature': (1, 0, 0, 0), 'alias': 'reflect', 'group': 'structured array', 'patterns': [
        {'signature': ('Array',), 'description': 'reverse a structured array on its last axis (reverse each row)',
         'function': lambda e, l: l.reverse_on_axis(-1)},
        {'signature': ('str',), 'description': 'reverse a string', 'function': lambda e, x: x[::-1]},
    ]},
    {'symbol': '⏛', 'signature': (1, 0, 0, 0), 'alias': 'flip', 'group': 'structured array', 'patterns': [
        {'signature': ('Array',), 'description': 'reverse a structured array on its first axis (reverse each column)',
         'function': lambda e, l: l.reverse_on_axis(0)},
    ]},
    {'symbol': '⏀', 'signature': (2, 0, 0, 0), 'alias': 'rotate', 'group': 'structured array', 'patterns': [
        {'signature': ('Array', 'int'),
         'description': 'rotate a structured array on its last axis (cycle the row values)',
         'function': lambda e, a, i: a.rotate_on_axis(axis=-1, n=i)},
    ]},
    {'symbol': '⦵', 'signature': (2, 0, 0, 0), 'alias': 'rotate up', 'group': 'structured array', 'patterns': [
        {'signature': ('Array', 'int'),
         'description': 'rotate a structured array on its first axis (cycle the column values)',
         'function': lambda e, m, i: m.rotate_on_axis(axis=0, n=i)},
    ]},
    {'symbol': '↦', 'signature': (1, 0, 0, 0), 'alias': 'shr', 'group': 'structured array', 'patterns': [
        {'signature': ('Array',),
         'description': 'shift the values in an array 1 to the right, filling the gap with a default value',
         'function': lambda e, a: a.shift_on_axis(axis=-1, n=1)},
        {'signature': ('str',), 'description': 'shift string 1 to the right', 'function': lambda e, s: (' ' + s)[:-1]},
    ]},
    {'symbol': '↤', 'signature': (1, 0, 0, 0), 'alias': 'shl', 'group': 'structured array', 'patterns': [
        {'signature': ('Array',),
         'description': 'shift the values in an array 1 to the left, filling the gap with a default value',
         'function': lambda e, a: a.shift_on_axis(axis=-1, n=-1)},
        {'signature': ('str',), 'description': 'shift string 1 to the left', 'function': lambda e, s: s[1:] + ' '},
    ]},
    {'symbol': '↥', 'signature': (1, 0, 0, 0), 'alias': 'shu', 'group': 'structured array', 'patterns': [
        {'signature': ('Array',), 'description': 'shift the values in a structured array 1 up, filling the gap with 0s',
         'function': lambda e, a: a.shift_on_axis(axis=0, n=-1)},
    ]},
    {'symbol': '↧', 'signature': (1, 0, 0, 0), 'alias': 'shd', 'group': 'structured array', 'patterns': [
        {'signature': ('Array',),
         'description': 'shift the values in a structured array 1 down, filling the gap with 0s',
         'function': lambda e, a: a.shift_on_axis(axis=0, n=1)},
    ]},
    {'symbol': '⊜', 'signature': (2, 0, 0, 0), 'alias': 'stack', 'group': 'structured array', 'patterns': [
        {'signature': ('Array', 'Array'), 'description': 'stack two structured arrays on top of each other',
         'function': lambda e, a, b: Matrix.join_on_axis(a, b, axis=0)},
    ]},
    {'symbol': '⥸', 'signature': (1, 0, 1, 0), 'alias': 'full reduce', 'group': 'structured array', 'patterns': [
        {'signature': ('Array', 'fn'), 'description': 'apply the function between all values in a structured array',
         'function': lambda e, m, f: m.reduce_all(fp2fn(e, f, 2))},
    ]},
    {'symbol': '≡', 'signature': (2, 0, 0, 0), 'alias': 'equivalent', 'group': 'structured array', 'patterns': [
        {'signature': ('Array', 'Array'), 'description': 'equivalence of all values and shapes of two arrays',
         'function': lambda e, a, b: a.equivalent(b)},
    ]},
    {'symbol': '≢', 'signature': (2, 0, 0, 0), 'alias': 'not equivalent', 'group': 'structured array', 'patterns': [
        {'signature': ('Array', 'Array'), 'description': 'non-equivalence of values and shapes of two arrays',
         'function': lambda e, a, b: not a.equivalent(b)},
    ]},
    {'symbol': '⊙', 'signature': (2, 0, 1, 0), 'alias': 'matrix binary', 'group': 'structured array', 'patterns': [
        {'signature': ('Array', 'Array', 'fn'),
         'description': 'apply a binary function to the values in two arrays element-wise',
         'function': lambda e, m1, m2, f: m1.bi_map(m2, fp2fn(e, f, 2))},
    ]},

    # Iteration
    {'symbol': 'Ω', 'signature': (0, 3, 0, 0), 'alias': 'for', 'group': 'iteration', 'patterns': [
        {'signature': ('any', 'any', 'any'),
         'description': "create an iterator by providing an initial value or function, a 'while' value or function, and an 'update' value or function",
         'function': lambda e, s, f, a: Iterator.from_functions(s, f, a)},
    ]},
    {'symbol': ':', 'signature': (1, 0, 0, 1), 'alias': 'iterate', 'group': 'iteration', 'patterns': [
        {'signature': ('Iterator', 'block'), 'description': 'start an iterator and apply to the following block',
         'function': lambda e, l, b: l.start(e, b)},
        {'signature': ('any', 'block'), 'description': 'iterate through a set of values',
         'function': lambda e, x, b: Iterator.from_object(x).start(e, b)},
    ]},
    {'symbol': '⌁', 'signature': (0, 0, 0, 0), 'alias': 'break', 'group': 'iteration', 'patterns': [
        {'signature': (), 'description': 'stop iteration and jump to the end of the block',
         'function': lambda e: e.exit_iteration()},
    ]},
    {'symbol': ';', 'signature': (0, 0, 0, 0), 'alias': 'return', 'group': 'iteration', 'patterns': [
        {'signature': (), 'description': 'end of iteration block symbol', 'function': lambda e: None},
    ]},

    # Lookup Functions
    {'symbol': '➊', 'signature': (0, 0, 0, 0), 'alias': 'p1', 'group': 'lookup', 'patterns': [
        {'signature': (), 'description': 'program parameter 1', 'function': lambda e: e.lookup('1')},
    ]},
    {'symbol': '➋', 'signature': (0, 0, 0, 0), 'alias': 'p2', 'group': 'lookup', 'patterns': [
        {'signature': (), 'description': 'program parameter 2', 'function': lambda e: e.lookup('2')},
    ]},
    {'symbol': '➌', 'signature': (0, 0, 0, 0), 'alias': 'p3', 'group': 'lookup', 'patterns': [
        {'signature': (), 'description': 'program parameter 3', 'function': lambda e: e.lookup('3')},
    ]},
    {'symbol': '➍', 'signature': (0, 0, 0, 0), 'alias': 'p4', 'group': 'lookup', 'patterns': [
        {'signature': (), 'description': 'program parameter 4', 'function': lambda e: e.lookup('4')},
    ]},
    {'symbol': '➎', 'signature': (0, 0, 0, 0), 'alias': 'p5', 'group': 'lookup', 'patterns': [
        {'signature': (), 'description': 'program parameter 5', 'function': lambda e: e.lookup('5')},
    ]},
    {'symbol': '⓪', 'signature': (0, 0, 0, 0), 'alias': 'i0', 'group': 'lookup', 'patterns': [
        {'signature': (), 'description': 'current iterator value', 'function': lambda e: e.implicit()},
    ]},
    {'symbol': '①', 'signature': (0, 0, 0, 0), 'alias': 'i1', 'group': 'lookup', 'patterns': [
        {'signature': (), 'description': 'value for iteration loop 1 above', 'function': lambda e: e.implicit(1)},
    ]},
    {'symbol': '②', 'signature': (0, 0, 0, 0), 'alias': 'i2', 'group': 'lookup', 'patterns': [
        {'signature': (), 'description': 'value for iteration loop 2 above', 'function': lambda e: e.implicit(2)},
    ]},
    {'symbol': '③', 'signature': (0, 0, 0, 0), 'alias': 'i3', 'group': 'lookup', 'patterns': [
        {'signature': (), 'description': 'value for iteration loop 3 above', 'function': lambda e: e.implicit(3)},
    ]},
    {'symbol': '④', 'signature': (0, 0, 0, 0), 'alias': 'i4', 'group': 'lookup', 'patterns': [
        {'signature': (), 'description': 'value for iteration loop 4 above', 'function': lambda e: e.implicit(4)},
    ]},
    {'symbol': '⑤', 'signature': (0, 0, 0, 0), 'alias': 'i5', 'group': 'lookup', 'patterns': [
        {'signature': (), 'description': 'value for iteration loop 5 above', 'function': lambda e: e.implicit(5)},
    ]},
    {'symbol': '_', 'signature': (0, 0, 0, 0), 'alias': 'implicit', 'group': 'lookup', 'patterns': [
        {'signature': (), 'description': 'current iterator value', 'function': lambda e: e.implicit()},
    ]},
    {'symbol': '⍛', 'signature': (0, 0, 0, 0), 'alias': 'previous', 'group': 'lookup', 'patterns': [
        {'signature': (), 'description': 'the previous iterator value',
         'function': lambda e: e.implicit(previous=True)},
    ]},
    {'symbol': '$', 'signature': (0, 1, 0, 0), 'alias': 'lookup', 'group': 'lookup', 'patterns': [
        {'signature': ('str',), 'description': 'lookup name', 'function': lambda e, s: e.lookup(s)},
        {'signature': ('int',), 'description': 'lookup program parameter', 'function': lambda e, s: e.lookup(str(s))},
    ]},
    {'symbol': '£', 'signature': (0, 1, 0, 0), 'alias': 'execute', 'group': 'lookup', 'patterns': [
        {'signature': ('str',), 'description': 'execute function by name',
         'function': lambda e, s: run_object(e, e.lookup(s))},
        {'signature': ('int',), 'description': 'execute function provided as a program parameter',
         'function': lambda e, s: run_object(e, e.lookup(str(s)))},
    ]},
    {'symbol': '→', 'signature': (1, 1, 0, 0), 'alias': 'assign', 'group': 'lookup', 'patterns': [
        {'signature': ('any', 'str'), 'description': 'assign a name to a value or function',
         'function': lambda e, v, s: e.assign(s, v)},
    ]},
    {'symbol': '⇶', 'signature': (0, 1, 0, 0), 'alias': 'pin', 'group': 'lookup', 'patterns': [
        {'signature': ('int',),
         'description': 'removes n values from the stack and makes them accessible via local lookups',
         'function': lambda e, i: e.pin(i)},
    ]},
    {'symbol': '⇴', 'signature': (0, 1, 0, 0), 'alias': 'local', 'group': 'lookup', 'patterns': [
        {'signature': ('int',), 'description': 'accesses the nth local value',
         'function': lambda e, i: e.local_lookup(i)},
    ]},
    {'symbol': '⑴', 'signature': (0, 0, 0, 0), 'alias': 'l1', 'group': 'lookup', 'patterns': [
        {'signature': (), 'description': 'pinned local value 1', 'function': lambda e: e.local_lookup('1')},
    ]},
    {'symbol': '⑵', 'signature': (0, 0, 0, 0), 'alias': 'l2', 'group': 'lookup', 'patterns': [
        {'signature': (), 'description': 'pinned local value 2', 'function': lambda e: e.local_lookup('2')},
    ]},
    {'symbol': '⑶', 'signature': (0, 0, 0, 0), 'alias': 'l3', 'group': 'lookup', 'patterns': [
        {'signature': (), 'description': 'pinned local value 3', 'function': lambda e: e.local_lookup('3')},
    ]},
    {'symbol': '⑷', 'signature': (0, 0, 0, 0), 'alias': 'l4', 'group': 'lookup', 'patterns': [
        {'signature': (), 'description': 'pinned local value 4', 'function': lambda e: e.local_lookup('4')},
    ]},
    {'symbol': '⑸', 'signature': (0, 0, 0, 0), 'alias': 'l5', 'group': 'lookup', 'patterns': [
        {'signature': (), 'description': 'pinned local value 5', 'function': lambda e: e.local_lookup('5')},
    ]},

    # Block Functions
    {'symbol': '(', 'signature': (0, 0, 0, 1), 'alias': 'paren', 'group': 'block', 'patterns': [
        {'signature': ('block',), 'description': 'start of a code block that will run immediately',
         'function': lambda e, b: Lambda(b).go(e)},
    ]},
    {'symbol': 'λ', 'signature': (0, 0, 0, 1), 'alias': 'lambda', 'group': 'block', 'patterns': [
        {'signature': ('block',), 'description': 'lambda block (takes a single value)',
         'function': lambda e, b: Lambda(b, use_implicit=True)},
    ]},
    {'symbol': 'µ', 'signature': (0, 0, 0, 1), 'alias': 'thunk', 'group': 'block', 'patterns': [
        {'signature': ('block',), 'description': 'mu block (takes no values)', 'function': lambda e, b: Lambda(b)},
    ]},
    {'symbol': 'κ', 'signature': (0, 0, 0, 1), 'alias': 'memo', 'group': 'block', 'patterns': [
        {'signature': ('block',), 'description': 'kappa block (takes a single value and caches it)',
         'function': lambda e, b: Lambda(b, caching=True)},
    ]},
    {'symbol': '⏎', 'signature': (1, 0, 0, 0), 'alias': 'run', 'group': 'block', 'patterns': [
        {'signature': ('fn',), 'description': 'run a block or function',
         'function': lambda e, l: run_object(e, l)},
    ]},
    {'symbol': ')', 'signature': (0, 0, 0, 0), 'alias': 'end', 'group': 'block', 'patterns': [
        {'signature': (), 'description': 'end block', 'function': lambda e: None},
    ]},

    # Combinators
    {'symbol': 'ℐ', 'signature': (0, 0, 1, 0), 'alias': 'identity', 'group': 'combinators', 'patterns': [
        {'signature': ('fn',), 'description': 'identity combinator (returns its input untouched) *Pf -> f(*)',
         'function': lambda e, f: Lambda.combinator('I', f)(e)},
    ]},
    {'symbol': '𝒦', 'signature': (1, 1, 0, 0), 'alias': 'constant', 'group': 'combinators', 'patterns': [
        {'signature': ('any', 'any'), 'description': 'constant combinator (returns x for any input) Kx -> x',
         'function': lambda e, x, y: y},
    ]},
    {'symbol': '𝒲', 'signature': (0, 0, 1, 0), 'alias': 'join combinator', 'group': 'combinators', 'patterns': [
        {'signature': ('fn',), 'description': 'join combinator (uses its input twice) xPf -> f(x,x)',
         'function': lambda e, f: Lambda.combinator('W', f)(e)},
    ]},
    {'symbol': '𝒞', 'signature': (0, 0, 1, 0), 'alias': 'flip combinator', 'group': 'combinators', 'patterns': [
        {'signature': ('fn',), 'description': 'flip combinator (reverses its inputs) xyPf -> f(y,x)',
         'function': lambda e, f: Lambda.combinator('C', f)(e)},
    ]},
    {'symbol': '∘', 'signature': (0, 0, 2, 0), 'alias': 'compose', 'group': 'combinators', 'patterns': [
        {'signature': ('fn', 'fn'),
         'description': 'compose combinator (applies one function after another) *Pfg -> g(f(*))',
         'function': lambda e, f, g: Lambda.combinator('B', g, f)(e)},
    ]},
    {'symbol': '𝒮', 'signature': (0, 0, 2, 0), 'alias': 'compare combinator', 'group': 'combinators', 'patterns': [
        {'signature': ('fn', 'fn'),
         'description': 'compare combinator (applies a function to its input and a processed version of its input) xPfg -> f(x,g(x))',
         'function': lambda e, f, g: Lambda.combinator("S", f, g)(e)},
    ]},
    {'symbol': '𝔰', 'signature': (0, 0, 2, 0), 'alias': 'compare flipped combinator', 'group': 'combinators',
     'patterns': [
         {'signature': ('fn', 'fn'),
          'description': 'compare combinator (applies a function to a processed version of its input, and its input) xPfg -> f(g(x), x)',
          'function': lambda e, f, g: Lambda.combinator("S'", f, g)(e)},
     ]},
    {'symbol': '𝚿', 'signature': (0, 0, 2, 0), 'alias': 'on combinator', 'group': 'combinators', 'patterns': [
        {'signature': ('fn', 'fn'),
         'description': 'on combinator (processes both inputs before applying a function) xyPfg -> f(g(x),g(y))',
         'function': lambda e, f, g: Lambda.combinator('Psi', f, g)(e)},
    ]},
    {'symbol': '𝒟', 'signature': (0, 0, 3, 0), 'alias': 'D fork', 'group': 'combinators', 'patterns': [
        {'signature': ('fn', 'fn', 'fn'),
         'description': 'D fork (applies different functions to its inputs and then combines them) xyPfgh -> f(g(x),h(y))',
         'function': lambda e, f, g, h: Lambda.combinator('D', f, g, h)(e)},
    ]},
    {'symbol': '𝚽', 'signature': (0, 0, 3, 0), 'alias': 'phi fork', 'group': 'combinators', 'patterns': [
        {'signature': ('fn', 'fn', 'fn'),
         'description': 'fork (applies two different functions to the same input before combining them) xPfgh -> f(g(x),h(x))',
         'function': lambda e, f, g, h: Lambda.combinator('Phi', f, g, h)(e)},
    ]},
    {'symbol': '𝛗', 'signature': (0, 0, 3, 0), 'alias': 'phi dyad fork', 'group': 'combinators', 'patterns': [
        {'signature': ('fn', 'fn', 'fn'),
         'description': 'fork (applies two different functions to the same inputs before combining them) xyPfgh -> f(g(x,y),h(x,y))',
         'function': lambda e, f, g, h: Lambda.combinator("Phi'", f, g, h)(e)},
    ]},
    {'symbol': '⍣', 'signature': (0, 0, 2, 0), 'alias': 'repeat until', 'group': 'combinators', 'patterns': [
        {'signature': ('fn', 'fn'),
         'description': 'repeatedly apply a function until the condition is false ⍣fg f.f... until not g',
         'function': lambda e, f, g: Lambda.repeat_until(e, f, g)},
    ]},
    {'symbol': '…', 'signature': (1, 0, 1, 0), 'alias': 'repeat', 'group': 'combinators', 'patterns': [
        {'signature': ('int', 'fn'), 'description': 'Apply a function n times to the same input',
         'function': lambda e, i, f: Lambda.repeat(e, f, i)},
    ]},
    {'symbol': '⊸', 'signature': (0, 1, 1, 0), 'alias': 'bind left', 'group': 'combinators', 'patterns': [
        {'signature': ('any', 'fn'),
         'description': 'Bind left (partially apply the function with its first input) xPf -> λy.f(x,y)',
         'function': lambda e, x, f: Lambda.bind('left', f, x)(e)},
    ]},
    {'symbol': '⟜', 'signature': (0, 1, 1, 0), 'alias': 'bind right', 'group': 'combinators', 'patterns': [
        {'signature': ('any', 'fn'),
         'description': 'Bind right (partially apply the function with its second input) xPf -> λy.f(y,x)',
         'function': lambda e, x, f: Lambda.bind('right', f, x)(e)},
    ]},
    {'symbol': '⍮', 'signature': (0, 0, 1, 0), 'alias': 'dip', 'group': 'combinators', 'patterns': [
        {'signature': ('fn',), 'description': 'Dip (apply the function to the second stack value) xyPf -> f(x),y',
         'function': lambda e, f: Lambda.dip(e, f)},
    ]},
    {'symbol': '⩣', 'signature': (0, 0, 1, 0), 'alias': 'defer', 'group': 'combinators', 'patterns': [
        {'signature': ('fn',), 'description': 'Defer execution and create a function object',
         'function': lambda e, f: Lambda(f)},
    ]},

    # Files
    {'symbol': '∫', 'signature': (0, 0, 0, 0), 'alias': 'load', 'group': 'files', 'patterns': [
        {'signature': (), 'description': 'load a value from file', 'function': lambda e: e.load_value()},
    ]},
    {'symbol': '⨋', 'signature': (1, 0, 0, 0), 'alias': 'save', 'group': 'files', 'patterns': [
        {'signature': ('any',), 'description': 'save a value to file', 'function': lambda e, x: e.save_value(x)},
    ]},
    {'symbol': '∮', 'signature': (0, 0, 0, 0), 'alias': 'load list', 'group': 'files', 'patterns': [
        {'signature': (), 'description': 'create a list with values from a file',
         'function': lambda e: FlatList(e.file_in(ints=True, cols=False))},
    ]},
    {'symbol': '⨖', 'signature': (0, 0, 0, 0), 'alias': 'load array', 'group': 'files', 'patterns': [
        {'signature': (), 'description': 'crete a structured array using values from a file',
         'function': lambda e: Matrix(e.file_in(ints=False, cols=True))},
    ]},

]

# On loading also provide the signatures to SyntaxTree so that it can create the program run tree
for _command in FBLeet_language:
    add_command_signature(_command['symbol'], _command['signature'], _command['alias'])


class Commands:
    """The command class encapsulates the above command list and exposes one method:
        match_command - finds the appropriate function for a given set of parameters (type dispatched)
        so the function can be applied to the parameters. It relies on parameter_match from the
        TypeUtilities module"""

    def __init__(self, command_list=None):
        """Load the commands and provide a symbol lookup table to simplify matching."""
        if command_list is None:
            self.commands = FBLeet_language
        else:
            self.commands = command_list

        self.symbol_lookup = dict()
        for command in self.commands:
            self.symbol_lookup[command['symbol']] = command
        return

    def match_command(self, symbol, stack_parameters, code_parameters, fn_parameters, block_parameters):
        if symbol in self.symbol_lookup:
            parameters = stack_parameters + code_parameters + fn_parameters + block_parameters
            patterns = self.symbol_lookup[symbol]['patterns']

            for pattern in patterns:
                pattern_signature = pattern['signature']

                if parameter_match(parameters, pattern_signature):
                    return {'symbol': symbol,
                            'signature': self.symbol_lookup[symbol]['signature'],
                            'type signature': pattern_signature,
                            'alias': self.symbol_lookup[symbol]['alias'],
                            'description': pattern['description'],
                            'function': pattern['function']}

        print("Function not found", symbol,
              [type(s) for s in stack_parameters],
              [type(c) for c in code_parameters],
              [type(f) for f in fn_parameters],
              [type(b) for b in block_parameters])
        raise KeyError


def print_commands():
    prev_group = ''
    for command in FBLeet_language:
        current_group = command['group']
        if current_group != prev_group:
            print('-----', current_group, '-----')
            prev_group = current_group
        print(command['symbol'], '\t', command['alias'], command['signature'], end=' ')
        if len(command['patterns']) > 1:
            print()
            prefix = '\t   -\t'
        else:
            prefix = ' - '
        for pattern in command['patterns']:
            print(prefix, pattern['signature'], pattern['description'])


def print_symbols(grouped=False):
    chunk_size = 20
    groups = dict()
    if not grouped:
        groups['functions'] = [command['symbol'] for command in FBLeet_language]
        group_names = groups.keys()
    else:
        group_names = set([command['group'] for command in FBLeet_language])
        for group in group_names:
            groups[group] = [command['symbol'] for command in FBLeet_language if command['group'] == group]
        group_names = sorted(group_names, key=lambda x: len(groups[x]), reverse=True)
    for group in group_names:
        print(group)
        symbols = groups[group]
        for i in range(0, len(symbols), chunk_size):
            chunk = ' '.join(symbols[i: i + chunk_size])
            print('\t', chunk)
