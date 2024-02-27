# Interpreter Internals

Below is a brief overview of how the fb1337 interpreter works. References to the appropriate code file are also provided as well as code snippets to make it easier to follow the logic.

The files are structured as follows:
```
Running Programs
    fbleet.py               functions to run programs
    FBLInteractive.py       the GUI interactive debugger
Interpreter
    FBLParser.py            Parses input code into parser tokens
    FBLSyntax.py            Builds the program's Syntax Tree
    FBLExecute.py           The eval / apply loop which runs a Syntax Tree
    FBLCommands.py          The command table
    FBLEnvironment.py       Local namespaces and the global stack
Types
    FBLArray.py             Array types: FlatArray, Coordinate, StructuredArray and MatrixArray
    FBLDictionary.py        Dictionary type
    FBLMatrix.py            Matrix specialisation of Array
    FBLIterators.py         Iterator types, ListIterator and Slice
    FBLLambda.py            Lambda functions and Combinators
Type Conversions
    TypeUtilities.py        Type coercion and type matching

```

Index
- [The Parser](#the-parser)
- [Syntax Tree Generation](#syntax-tree-generation)
- [Syntax Tree Evaluation](#syntax-tree-evaluation)
- [Evaluation of Operators](#evaluation-of-operators)
- [Type Transformations and Parameter Matching](#type-transformations-and-parameter-matching)
- [Return Values](#return-values)
- [The Environment](#the-environment)


## The Parser

The code is tokenised by the [Reader](FBLParser.py) using a simple set of regex patterns. See [Parser Documentation](fbl1337%20parser%20documentation.md) for more details on how the parser interprets code.

A typical token produced is of the following form:
```
('symbol',                      # The type of token
'|',                            # The token data
    {                           # Token meta data
    'comments': 'divides',          # Comments associated with this token
     'token_code': '|',             # Original text that was parsed to produce this token
     'code location': (15, 16)      # Where in the text (excluding comments and ignored text) the token was read from
     }
)
```

## Syntax Tree Generation

The tokens are arranged into a Syntax Tree by the [Tree Generator](FBLSyntax.py). The code tokens are read very much as they would be run, in a eval/apply loop. The resulting tree is structured as follows:
- Tokens that are evaluated in turn are placed in a list
- Parameters taken from the code are child-nodes of the operator token
- Block parameters are turned into sub-trees and become child-nodes of the operator token

For the program
```fb1337
ḣ:				for i in range(1, 101):
_‰3?FizzØ			'Fizz' if (i % 3 == 0) else ''
_‰5?BuzzØ			'Buzz' if (i % 5 == 0) else ''
⊕					concatenate strings
_∨					if string is '' then i else string
```

The Syntax Tree has the following structure. Intentation levels are used to indicate child-nodes
```
100
: 'iterate' (1) {    # for i in range(1, 101): #
  _ 'implicit'
  ‰ 'divisible by' (1) [
    3 ]
  ? 'if' (1) [
    Fizz
    Ø     # 'Fizz' if (i % 3 == 0) else '' # ]
  _ 'implicit'
  ‰ 'divisible by' (1) [
    5 ]
  ? 'if' (1) [
    Buzz
    Ø     # 'Buzz' if (i % 5 == 0) else '' # ]
  ⊕ 'join' (2)     # concatenate strings #
  _ 'implicit'
  ∨ 'or' (2)     # if string is '' then i else string # }
```

For example the ':' token has the following contents:

```
token_type: 'fn'        # 'fn' indicates a valid operator
token.value ':'         # ':' is the operator symbol
stack_values: 1         # number of operator parameters to be taken from the stack
code_tokens: []         # tokens taken from the code to be evaluated and used as parameters
fn_tokens: []           # tokens taken from the code to be evaluated as functions and used as parameters
sub_tree:               # sub-tree for operators that control blocks
    SyntaxTree([<2 fn _ - - - ->, <3 fn ‰ 1 [3] - ->, <5 fn ? 1 - ['Fizz', ''] ->, <8 fn _ - - - ->, <9 fn ‰ 1 [5] - ->, <11 fn ? 1 - ['Buzz', ''] ->, <14 fn ⊕ 2 - - ->, <15 fn _ - - - ->, <16 fn ∨ 2 - - ->])
location: (1,)          # Location in the syntax tree where the token can be found
index: 1                # Index of the token in the internal array (execution order)
parse_token: ('symbol', ':', {'comments': 'for i in range(1, 101):', 'token_code': ':', 'code location': (1, 2)})
```

## Syntax Tree Evaluation

Evaluation of the syntax tree takes place in the [Eval / Apply Loop](FBLExecute.py) and consists of a typical Lisp-like eval / apply loop. Tokens are evaluated in 'eval_token' one-by-one. When an operator is identified it is passed to 'apply' for evaluation. 'Apply' looks up the operator in the [Command Dictionary](FBLCommands.py) and gathers all the parameters required by the operator. It then passes each of these in turn to eval before running the operator function.

The exception is function parameters, which are wrapped to delay execution. An operator which takes function parameters, must explicitly run the resulting functions.

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
	self.apply(env, token)
```

Apply gathers parameters in the following order:
- stack parameters are popped off the stack and their order reversed so that the deepest stack value becomes the first parameter, and the top stack value becomes the last stack parameter. If insufficient values are available on the stack, null values are provided as parameters.
```python
for _ in range(token.stack_values):
	stack_parameters.append(env.pop())
stack_parameters = stack_parameters[::-1]
```
- code parameters are taken from the syntax tree and evaluated before being added to the list of parameters
```python
for code_token in token.code_tokens:
	self.eval_context(env, code_token)
	code_parameters.append(env.pop())
```
- function tokens are wrapped to defer execution and passed as lambdas to the operator function. Note that two different types of function could be passed in - operator tokens, or Lambda objects. Python's rather odd implementation of closures necessitates that we provide the code to be evaluated into the wrapper as a parameter (see the note in the code for details as to why).
```python
for fn_token in token.fn_tokens:
	if fn_token.token_type == 'fn' and fn_token.value in 'λµ(κ$':
		def wrapper(t):
			def f(e):
				self.eval_context(env, t)
				run_object(e, e.pop())
			return f
		new_lambda = wrapper(fn_token)
	else:
		new_lambda = (lambda t: (lambda e: self.eval_context(env, t)))(fn_token)
	fn_parameters.append(new_lambda)
```
- blocks are provided as a Lambda object that will evaluate the code in the block when run by the iterator object
```python
if token.sub_tree is not None:
	block_parameters.append(lambda e: self.eval_context(e, token.sub_tree))
```

Finally, the operator can be matched with the appropriate type variant (if one exists) given the types of the parameters that have been found, run and the result pushed back to the stack.
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

As seen above, before the function is run, the parameters and functions undergo a type transformations to coerce values. This takes place in [Type Utilities](FBLTypeUtilities.py).

The following are valid type substitutions and the following type transformations are made:
- ('int',) can be replaced by ('Array',). In this case the function is replaced by a map over the array
- ('Array', 'int') can replace ('int', 'int'). In this case the function is replaced by a map over the array with the integer value partially applied
- ('Array', 'Array') can replace ('int', 'int'). In this case the function is replaced by an element-wise binary operator
- 'int' will cast null, boolean, float, single-value matrices and strings that represent integer values to an integer value
- 'List' will cast 'Matrix' and 'StructuredArray' objects to flat lists
- 'Matrix' will cast a structured array containing integers into a Matrix

## Return Values

The return value of the program is a representation of the state of the stack on completion of the program. However the stack is not returned as-is. This is also handled by [Type Utilities](FBLTypeUtilities.py).

- If the stack is empty, None is returned
- null values remaining on the stack are ignored
- When number, tuple or string remains on the stack, this value is returned unaltered.
- When only a flat array is on the stack, the values are returned as a list
- When a structured array is the only object on the stack, a nested list is returned
- Matrices are rounded to 2dp before being returned; single-valued matrices are returned as float values
- List values are returned as a Python list of values (each value is subject to the above transformations also)

| Final Stack                      | Returned           |
|----------------------------------|--------------------|
| ['']                             | None               |
| [42]                             | 42                 |
| ["123"]                          | 123                |
| [List< 3 4 5>]                   | [3 4 5]            |
| [Matrix<1.1415 2.71828 3.14159>] | [1.14, 2.72, 3.14] |
| [1 3 5]                          | [[1 3 5]]          |
| [1 List< List<1 2> List<3 4>>]   | [1 [[1 2] [3 4]]]  |

## The Environment

At all times there is an active environment variable. This is found in [Environment](FBLEnvironment.py). When a program is executed, [Execute](FMLExecute.py) will create a base environment, which will contain the global stack and populate it's namespace dictionary with the program parameters (including the name of the program).

This base environment also contains the file path and active file handles for file input and output.

When a block is created, it will be created with a new local environment object that will maintain a link to its parent and to the base environment.

The active environment contains all local names, stored in a dictionary. When a variable is looked up, the search starts in the dictionary of the local environment, and a reference to the 'implicit object', which is the iterator or Lambda object that created the environment and which can be asked for an implicit local variable.

When a named lookup is performed, the local environment will check its local namespace dictionary first, if the name is not found it will make the lookup request to its parent. If it is not found in the base environment, null is returned. Thus when local variables are assigned, they will shadow objects in outer scope. It is not possible to write into the namespace of an outer scope, so these variables are effectively immutable.

Blocks do not usually provide closure, since the local environment is passed to the block when executed, not the time it was created.