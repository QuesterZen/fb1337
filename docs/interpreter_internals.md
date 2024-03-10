# Interpreter Internals

Below is a brief overview of how the fb1337 interpreter works. References to the appropriate code file are also provided as well as code snippets to make it easier to follow the logic.

The files in the directory `/fb1337` are structured as follows:
```
Running Programs
	fbleet.py				run programs in normal, annotation or interactive modes
Interpreter
	lexer.py				parses input code into lexical tokens
	parser.py				builds the program's Abstract Syntax Tree
	execute.py				eval / apply loop which runs the Abstract Syntax Tree
	commands.py				table of commands
	environment.py			global stack and local namespaces
Types
	array					array types: FlatArray, Coordinate, StructuredArray and MatrixArray
	dictionary.py			Dictionary type
	iterators.py			Iterator type
	slice.py				Slice type
	lambda_fn.py			Lambda anonymous function objects and Combinators
Type Conversions
	type_utilities.py		type coercion and type matching
```

Index
- [The Parser](#the-parser)
- [Syntax Tree Generation](#syntax-tree-generation)
- [Syntax Tree Evaluation](#syntax-tree-evaluation)
  - [Evaluation of Values](#evaluation-of-values)
  - [Evaluation of Operators](#evaluation-of-operators)
  - [Type Transformations and Parameter Matching](#type-transformations-and-parameter-matching)
- [Return Values](#return-values)
- [The Environment](#the-environment)


## The Parser

The code is tokenised by the [Reader object](../fb1337/lexer.py) using a simple set of regex patterns. See [Parser Documentation](./interpreting_input) for more details on how the parser interprets code.

A typical token produced by the parser is of the following form:
```
('symbol',						# The type of token
'|',							# The token data
	{							# Token meta data
	'comments': 'divides',		# Comments associated with this token
	'token_code': '|',				# Original text that was parsed to produce this token
	'code location': (15, 16)		# Location of original text in the (processed) code
									  after removal of comments, whitespace and 
									  the expansion of short cuts 
	}
)
```

## Syntax Tree Generation

The tokens are arranged into a Syntax Tree by the [Syntax Tree object](../fb1337/parser.py). The code tokens are read very much as they will be run, in the eval / apply loop. The resulting tree is structured as follows:
- Tokens to be are evaluated consecutively are placed in a list
- Parameters taken from the code become child-nodes of the operator token in the syntax tree
- Block parameters are turned into subtrees and also become child-nodes of the operator token

For the following program:
```fb1337

ḣ:				for i in range(1, 101):
_‰3⁈Fizz			'Fizz' if (i % 3 == 0) else ''
_‰5⁈Buzz			'Buzz' if (i % 5 == 0) else ''
⊕					concatenate strings
_∨					if string is '' then i else string
```

The Syntax Tree has the following structure (indentation indicates child-nodes)
```
100
: 'iterate' (1) {	# for i in range(1, 101): #
  _ 'implicit'
  ‰ 'divisible by' (1) [
    3 ]
  ⁈ 'if or null' (1) [
    Fizz			# 'Fizz' if (i % 3 == 0) else '' # ]
  _ 'implicit'
  ‰ 'divisible by' (1) [
    5 ]
  ⁈ 'if or null' (1) [
    Buzz			# 'Buzz' if (i % 5 == 0) else '' # ]
  ⊕ 'join' (2)		# concatenate strings #
  _ 'implicit'
  ∨ 'or' (2)		# if string is '' then i else string # }
```

For example the ':' token has the following contents:

```
token_type: 'fn'        # 'fn' indicates a valid operator
token.value ':'         # ':' is the operator symbol
stack_values: 1         # number of operator parameters to be taken from the stack
code_tokens: []         # tokens taken from the code to be evaluated and used as parameters
fn_tokens: []           # tokens taken from the code to be evaluated as functions and used as parameters
sub_tree:               # the block argument
    SyntaxTree([<2 fn _ - - - ->, <3 fn ‰ 1 [3] - ->, <5 fn ⁈?? 1 - ['Fizz'] ->, <8 fn _ - - - ->, <9 fn ‰ 1 [5] - ->, <11 fn ⁈ 1 - ['Buzz'] ->, <14 fn ⊕ 2 - - ->, <15 fn _ - - - ->, <16 fn ∨ 2 - - ->])
location: (1,)          # Location in the syntax tree where the token can be found
index: 1                # Index of the token in the internal array (execution order)
```

## Syntax Tree Evaluation

Evaluation of the syntax tree takes place in the [Execute Module](../fb1337/execute.py) and consists of a typical Lisp-like eval / apply loop. Tokens are evaluated one-by-one in the method 'eval_token'. When an operator is identified it is passed to 'apply'. 'Apply' looks up the operator in the [Command Dictionary](../fb1337/commands.py) and gathers all the parameters required by the operator. It then passes each of these in turn to eval before looking up the appropriate type-variant of the operator in the [Command Dictionary](../fb1337/commands.py), which may require type coercion in [Type Utilities](../fb1337/type_utilities.py), and running the associated function.


### Evaluation of Values

When value tokens are evaluated, the token value is simply pushed onto the stack.

```python
if token_type == "value":
	env.push(token.value)
```

### Evaluation of Operators

Operator tokens are passed to apply

```python
if token_type == 'fn':
  self._apply(env, token)
```

Apply gathers its parameters in the following order:

1. **stack parameters** are popped off the stack and their order reversed so that the deepest stack value becomes the first parameter, and the top stack value becomes the last parameter. If insufficient values are available on the stack, null values are provided as parameters.
```python
for _ in range(token.stack_values):
	stack_parameters.append(env.pop())
stack_parameters = stack_parameters[::-1]
```
2. **code parameters** are taken from the syntax tree and evaluated before being added to the list of parameters

```python
for code_token in token.code_tokens:
  self._eval_context(env, code_token)
  code_parameters.append(env.pop())
```
3. **function parameters** are wrapped to defer execution and passed as lambdas to the operator function. Note that two different types of function could be passed in - operator tokens, or Lambda objects. Python's implementation of closures necessitates that we provide the code to be evaluated into the wrapper as a parameter (see the note in the code for details as to why).

```python
for fn_token in token.fn_tokens:
  if fn_token.token_type == 'fn' and fn_token.value in 'λµ(κ$':
    def wrapper(t):
      def f(e):
        self._eval_context(env, t)
        run_object(e, e.pop())

      return f


    new_lambda = wrapper(fn_token)
  else:
    new_lambda = (lambda t: (lambda e: self._eval_context(env, t)))(fn_token)
  fn_parameters.append(new_lambda)
```
4. **block parameters** are also wrapped to be run by the block's owner.

```python
if token.sub_tree is not None:
  block_parameters.append(lambda e: self._eval_context(e, token.sub_tree))
```

Finally, the operator can be matched with the appropriate type-variant (if one exists) given the types of the parameters that have been found, run and the result is pushed back to the stack.
```python
match = self.commands.match_command(symbol, stack_parameters, code_parameters, fn_parameters, block_parameters)
all_parameters = stack_parameters + code_parameters + fn_parameters + block_parameters
type_signature = match['type signature']
used_fn = match['function']
transformed_parameters, transformed_fn = apply_type_transformations(all_parameters, type_signature, used_fn)
value = transformed_fn(env, *transformed_parameters)
if value is not None:
    env.push(value)
```

### Type Transformations and Parameter Matching

As seen above, before the function is run, the parameters and functions undergo a type transformations to coerce values. This takes place in [Type Utilities](../fb1337/type_utilities.py).

The following are valid type substitutions and the following type transformations are made:
- ('int',) can be replaced by ('Array',). In this case the function is replaced by a map over the array
- ('Array', 'int') can replace ('int', 'int'). In this case the function is replaced by a map over the array with the integer value partially applied to the operator
- ('Array', 'Array') can replace ('int', 'int'). In this case the function is replaced by an element-wise binary operation
- 'int' will cast null, boolean, float, single-value matrices and strings that represent integer values to an integer value
- 'List' will cast 'MatrixArray' and 'StructuredArray' objects to 'FlatList' 
- 'Matrix' will cast StructuredArray containing integers into 'MatrixArray'

## Return Values

The return value of the program is a representation of the state of the stack on completion of the program. However, the stack is not returned as-is. This is also handled by [Type Utilities](../fb1337/type_utilities.py).

- If the stack is empty, None is returned
- null values remaining on the stack are ignored
- When a single number or string remains on the stack, this value is returned unaltered.
- When only a FlatList is on the stack, the values are returned as a list
- When only a StructuredArray is on the stack, a nested list is returned
- Matrices are rounded to 2 decimal places before being returned; single-valued matrices are returned as float values, other shapes as nested lists
- When multiple values remain on the stack, they are each transformed as above and returned in a list

| Final Stack                               | Returned              |
|-------------------------------------------|-----------------------|
| ['']                                      | None                  |
| [42]                                      | 42                    |
| ["123"]                                   | 123                   |
| [FlatList<3 4 5>]                         | [3, 4, 5]             |
| [Matrix<1.1415 2.71828 3.14159>]          | [1.14, 2.72, 3.14]    |
| [1 3 5]                                   | [1, 3, 5]             |
| [1 FlatList<FlatList<1 2> FlatList<3 4>>] | [1, [[1, 2], [3, 4]]] |

## The Environment

At all times there is an active environment variable. This is described in [Environment](../fb1337/environment.py). When a program is executed, [Execute](../fb1337/execute.py) will create a base environment, which will contain the global stack and populate its namespace dictionary with the program parameters (including the name of the program).

This base environment also contains the file path and active file handles for file input and output.

When a block is run, it will receive a new local environment object that will maintain a link to its parent and to the base environment.

The active environment contains all local names, stored in a dictionary. When a variable is looked up, the search starts in the dictionary of the local environment. If it is not found there, the search will move to its parent. If it is not found in the parent environment, the value `null` is returned. Similarly, when the implicit variable is looked up, the search for an 'implicit object' starts in the local environment and moves up the chain until it is found.

When local variables are assigned, they shadow objects in outer scope. It is not possible to write into the namespace of an outer scope, so variables in outer scopes are effectively immutable.

Blocks do not usually provide closure over variables active in the scope where they are defined, since the local environment that is passed to them is created at the time the block is executed, not the time it was created.