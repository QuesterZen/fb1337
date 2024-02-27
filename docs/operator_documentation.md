# Operators

Operators are listed as follows:

`name    symbol  signature (# stack parameters, # code parameters, # function parameters, # block parameters)`

The parameters are taken in the order listed in the signature:
- stack parameters are taken from the stack. When multiple stack parameters are taken they are provided to the operator in the order they appear on the stack (deepest first)
- code parameters are single tokens appearing directly after the symbol in the code. Values are taken as is. Parenthesised blocks are evaluated and the top value remaining on the stack is taken as the value). Lambdas can be passed in, but are not evaluated. The stack identity symbol `⊢` converts the code parameter into another stack parameter.
- function parameters can be lambdas, built-in operators (which are converted to lambdas) or combinators.
- block parameters - there is only a maximum of one block parameter, all code after the evaluation of the other parameters is taken until a block completion symbol `)` or `;`

Index
- [Math Operators](#math-operators)
- [Stack Operators](#stack-operators)
- [Lookup Operators](#lookup-operators)
- [Blocks, Iteration and Control Flow Operators](#blocks-iteration-and-control-flow-operators)
- [Array and List Operators](#array-and-list-operators)
- [Other Objects: Strings, Dictionaries and Slices](#other-objects-strings-dictionaries-and-slices)
- [Higher level functions and Combinators](#higher-level-functions-and-combinators)
- [File Handling](#file-handling)


## Math Operators

The majority of math operators take two integer values from the stack and perform an integer calculation. When the right, or both values are arrays, the operator is applied element-wise and returns an array.

Note that multiply is `×` while power is `*`.

```
neg 	 '~'	 (1, 0, 0, 0)
		 ('int',) "negate"
add 	 '+'	 (2, 0, 0, 0)
		 ('int', 'int') "addition"
		 ('None', 'any') "addition"
		 ('Coordinate', 'Coordinate') "addition"
mul 	 '×'	 (2, 0, 0, 0)
		 ('int', 'int') "multiply"
		 ('None', 'int') "multiply"
		 ('str', 'int') "string repeat"
		 ('Coordinate', 'int') "scalar multiply"
sub 	 '-'	 (2, 0, 0, 0)
		 ('int', 'int') "subtract"
div 	 '÷'	 (2, 0, 0, 0)
		 ('Matrix', 'int') "divide"
		 ('Matrix', 'Matrix') "divide"
		 ('int', 'int') "integer divide"
mod 	 '%'	 (2, 0, 0, 0)
		 ('int', 'int') "modulo division"
divisible by 	 '‰'	 (1, 1, 0, 0)
		 ('int', 'int') "is divisible by"
divisible 	 '‱'	 (2, 0, 0, 0)
		 ('int', 'int') "is divisible by"
divides 	 '|'	 (2, 0, 0, 0)
		 ('int', 'int') "a divides b"
abs 	 '⩲'	 (1, 0, 0, 0)
		 ('int',) "absolute value"
sqr 	 '²'	 (1, 0, 0, 0)
		 ('int',) "square"
sqrt 	 '√'	 (1, 0, 0, 0)
		 ('int',) "integer square root"
		 ('Matrix',) "square root"
log2 	 '⊛'	 (1, 0, 0, 0)
		 ('int',) "integer log base 2"
sign 	 '±'	 (1, 0, 0, 0)
		 ('int',) "sign of value as -1, 0 or 1"
		 ('Coordinate',) "grid (Manhattan) distance from origin"
pow 	 '*'	 (2, 0, 0, 0)
		 ('int', 'int') "power x^n"
gcd 	 '⨸'	 (2, 0, 0, 0)
		 ('int', 'int') "greatest common divisor"
inc 	 '⩓'	 (1, 0, 0, 0)
		 ('int',) "increment by 1"
dec 	 '⩔'	 (1, 0, 0, 0)
		 ('int',) "decrement by 1"
factorial 	 '!'	 (1, 0, 0, 0)
		 ('int',) "factorial n!"
binomial 	 '‼'	 (2, 0, 0, 0)
		 ('int', 'int') "nCr binomial coefficient"
max 	 '⌈'	 (2, 0, 0, 0)
		 ('int', 'int') "maximum value"
		 ('Matrix', 'Matrix') "element-wise maximum"
min 	 '⌊'	 (2, 0, 0, 0)
		 ('int', 'int') "minimum value"
eq 	     '='	 (2, 0, 0, 0)
		 ('int', 'int') "equal?"
		 ('str', 'str') "string equal?"
		 ('any', 'any') "equal?"
neq 	 '≠'	 (2, 0, 0, 0)
		 ('int', 'int') "not equal?"
		 ('str', 'str') "string not equal?"
		 ('any', 'any') "not equal?"
lt 	     '<'	 (2, 0, 0, 0)
		 ('int', 'int') "less than?"
lte 	 '≤'	 (2, 0, 0, 0)
		 ('int', 'int') "less than or equal?"
gt 	     '>'	 (2, 0, 0, 0)
		 ('int', 'int') "greater than?"
gte 	 '≥'	 (2, 0, 0, 0)
		 ('int', 'int') "greater than or equal?"
not 	 '¬'	 (1, 0, 0, 0)
		 ('Matrix',) "logical not"
		 ('Array',) "logical not"
		 ('int',) "logical not"
		 ('any',) "logical not"
and 	 '∧'	 (2, 0, 0, 0)
		 ('Matrix', 'Matrix') "logical and"
		 ('int', 'int') "logical and"
		 ('any', 'any') "logical and"
or 	     '∨'	 (2, 0, 0, 0)
		 ('Matrix', 'Matrix') "logical or"
		 ('int', 'int') "logical or"
		 ('any', 'any') "logical or"
binary 	 '⟘'	 (2, 0, 0, 0)
		 ('int', 'int') "binary value as list of length n"
from binary 	 '⊤'	 (1, 0, 0, 0)
		 ('str',) "string binary number to integer"
		 ('Array',) "boolean list binary representation to integer"
```

## Stack Operators

Stack operators manipulate the first few values on the stack. Typically, the same outcome can be performed with Combinators also during a calculation, but it is often useful to leave the stack in a specific order, for example at the end of a block.

The identity and left operators may seem unncessary, but they are very useful in combinators and operators that take code parameters, in which case they can convert the parameter to a stack parameter.

drop 	 '◌'	 (1, 0, 0, 0)
		 ('any',) "discard the top stack value"
identity 	 '⊢'	 (1, 0, 0, 0)
		 ('any',) "use the top stack value"
left 	 '⊣'	 (2, 0, 0, 0)
		 ('any', 'any') "use the second stack value"
copy 	 '⊩'	 (1, 0, 0, 0)
		 ('any',) "use and retain the top stack value (dup)"
copy left 	 '⫣'	 (2, 0, 0, 0)
		 ('any', 'any') "use and retain the second stack value (under)"
deep 	 '⫤'	 (0, 1, 0, 0)
		 ('int',) "use and drop stack value n-back to top of stack"
dup 	 '∂'	 (1, 0, 0, 0)
		 ('any',) "duplicate top stack value a -> aa"
dup2 	 'ð'	 (2, 0, 0, 0)
		 ('any', 'any') "duplicate top two stack values ab -> abab"
swap 	 '«'	 (2, 0, 0, 0)
		 ('any', 'any') "swap top two stack values ab -> ba"
under 	 '⨩'	 (2, 0, 0, 0)
		 ('any', 'any') "duplicate second stack value to the top ab->aba"
dup under 	 'ḋ'	 (2, 0, 0, 0)
		 ('any', 'any') "duplicate second stack value in place ab->aab"
rot 	 '®'	 (3, 0, 0, 0)
		 ('any', 'any', 'any') "rotate the top three stack values abc -> bca"


## Lookup Operators

The majority of lookup operators apply to the local environment. Each new block, iterator-controlled block and higher-level function creates a sub-environment. These have access to variables in their outer environments if not shadowed locally. It is not possible to directly change outer environments, but mutable operators can alter the objects they refer to.

Program parameters can be accessed as `$n` where n is an integer value and $0 is the program name; or through the following short-cuts for the 1st, 2nd, 3rd, 4th and 5th program parameters: `➊ ➋ ➌ ➍ ➎`

The current iteration parameter is accessed via:
```
implicit 	 '_'	 (0, 0, 0, 0)
		 () "current iterator value"
previous 	 '⍛'	 (0, 0, 0, 0)
		 () "the previous iterator value"
```
There are also shortcuts available to access iterators in outer scopes (as well as the local scope). `⓪` is another way to express the current iterators, `①` accesses the iterator one-scope above the current, `② ③ ④ ⑤` access iterators in higher scopes. There is no way to access iterators with greater levels of nesting directly.

Values can be added to- and accessed in- the local namespace with the following operators:
```
assign 	 '→'	 (1, 1, 0, 0)
		 ('any', 'str') "assign a name to a value or function"
lookup 	 '$'	 (0, 1, 0, 0)
		 ('str',) "lookup name"
		 ('int',) "lookup program parameter"
```
In addition lambdas with names can be run directly with the following operator which is a pseudonym for `$name⏎`.
```
execute 	 '£'	 (0, 1, 0, 0)
		 ('str',) "execute function by name"
		 ('int',) "execute function provided as a program parameter"
```

Stack parameters can be converted into local variables (somewhat akin to function parameters using 'pin' and accessed via the 'local' operator.
```
pin 	 '⇶'	 (0, 1, 0, 0)
		 ('int',) "removes n values from the stack and makes them accessible via local lookups"
local 	 '⇴'	 (0, 1, 0, 0)
		 ('int',) "accesses the nth local value"
```
Shortcuts are available for the first 5 local values: `⑴ ⑵ ⑶ ⑷ ⑸`.

## Blocks, Iteration and Control Flow Operators

The following operators create blocks of code for subsequent evaluation.
- `(...)` blocks are evaluated immediately.
- The simplest functions are created with `µ...)` which provides a code block that can be passed around as a value and run at a later time. `λ...)` and `κ...)` blocks are extensions of this.
- `λ`-blocks push the current iterator value to the stack before running, this makes them especially useful in higher-level functions and iterators.
- `κ`-blocks cache the top stack value at the time they are first run in a dictionary together with the top value on the stack on exit. Subsequent runs will check whether the stack value is in the dictionary and return the associated value and run no code.

```
paren 	 '('	 (0, 0, 0, 1)
		 ('block',) "start of a code block that will run immediately"
lambda 	 'λ'	 (0, 0, 0, 1)
		 ('block',) "lambda block (takes a single value)"
thunk 	 'µ'	 (0, 0, 0, 1)
		 ('block',) "mu block (takes no values)"
memo 	 'κ'	 (0, 0, 0, 1)
		 ('block',) "kappa block (takes a single value and caches it)"
run 	 '⏎'	 (1, 0, 0, 0)
		 ('fn',) "run a block or function"
end 	 ')'	 (0, 0, 0, 0)
		 () "end block"
```

All iteration uses iterator objects. These are either created
- implicitly by `:` 'iterate', which will convert arrays, slice objects, integers or strings into iterators, or
- explitly using the `Ω` 'for' operator. This takes three arguments:
    - an initial value or function that produces a value
    - a value to indicate the number of times to run, or alternatively a function that is called prior to running the block and should return True if the block should be run, or False to terminate iteration and jump to the end of the block
    - a value that will be added to the current value, or a function that will update the iterator at the end of each execution of the block

The iterator will run the subsequent code up to the `;` 'return' symbol. The loop can be terminated early with `⌁` 'break' which can appear in the iterator update function, or in the block. If it appears in the block, the loop will terminate at the end of this iteration through the block.

```
for 	 'Ω'	 (0, 3, 0, 0)
		 ('any', 'any', 'any') "create an iterator by providing an initial value or function, a 'while' value or function, and an 'update' value or function"
iterate  ':'	 (1, 0, 0, 1)
		 ('Iterator', 'block') "start an iterator and apply to the following block"
		 ('Array', 'block') "iterate through the values of an array"
		 ('Slice', 'block') "iterate over a slice range"
		 ('int', 'block') "iterate over the values 1 to n"
		 ('str', 'block') "iterate over the characters in a string"
break 	 '⌁'	 (0, 0, 0, 0)
		 () "stop iteration and jump to the end of the block"
return 	 ';'	 (0, 0, 0, 0)
		 () "end of iteration block symbol"
```

In addition, list iterators (created by iterating a list, or creating a new list) also manage a pointer to an item in the list. If the list is being iterated, the pointer points to the current value of the list and it is advanced to the next non-null value after each loop, the implicit value in the local environment will be the value pointed to by this pointer. It can also be manipulated directly via the following commands, which can be a useful way to keep track of a position in a list.
```
current 	 '◇'	 (1, 0, 0, 0)
		 ('List',) "returns the current value"
first 	 '⇤'	 (1, 0, 0, 0)
		 ('List',) "moves the list pointer to the first non-null value"
		 ('str',) "returns the first character of string"
last 	 '⇥'	 (1, 0, 0, 0)
		 ('List',) "moves the list pointer to the end of the list"
		 ('str',) "returns the last character of string"
next 	 '⪼'	 (1, 0, 0, 0)
		 ('List',) "moves the list pointer to the next non-null value"
prev 	 '⪻'	 (1, 0, 0, 0)
		 ('List',) "moves the list pointer to previous non-null value"
move 	 '≻'	 (2, 0, 0, 0)
		 ('List', 'int') "moves the list pointer to a specified index"
```

The following selective control operators are provided.
```if 	 '?'	 (1, 0, 2, 0)
		 ('any', 'any', 'any') "if predicate ? true_fn false_fn"
case 	 '₡'	 (0, 0, 3, 0)
		 ('any', 'any', 'any') "case predicate true_fn false_fn"
else 	 '€'	 (0, 0, 1, 0)
		 ('any',) "else action_fn"
```

Note that 'else' is not actually necessary, but can make the code easier to read in a nested case function such as the following code example:
```
100⍳¨µ
    ₡ µ∂ ‰15) µFizzBuzz)
    ₡ µ∂ ‰5)  µBuzz)
    ₡ µ∂ ‰3)  µFizz)
    €  ∂      ⊢
    ⍮◌
    )
```

## Array and List Operators

The following operators are conveniences for constructing lists:
```
pair 	 '‿'	 (1, 1, 0, 0)
		 ('Array', 'Array') "join two lists together side by side"
		 ('Array', 'any') "add a value to a list"
		 ('any', 'any') "pair two values into a list"
extend 	 '⁔'	 (2, 0, 0, 0)
		 ('Array', 'Array') "add list as a member"
		 ('Array', 'int') "list append"
		 ('int', 'Array') "list prepend"
		 ('Array', 'any') "list append"
		 ('any', 'Array') "list prepend"
		 ('any', 'any') "pair values into a list"
gather 	 '⏍'	 (0, 0, 0, 0)
		 () "put all values on the stack stack (from last null) into a list"
gather n 	 '☐'	 (0, 1, 0, 0)
		 ('int',) "put the top n items on the stack into a list"
scatter 	 '☆'	 (1, 0, 0, 0)
		 ('Array',) "put each item in the list onto the stack"
		 ('any',) "ungroup items and place each on the stack"
enlist 	 '⊟'	 (1, 0, 0, 0)
		 ('Coordinate',) "wrap a coordinate into a list"
		 ('Array',) "convert a structured array into a flat list"
		 ('int',) "wrap a value into a list"
		 ('any',) "wrap a value into a list"
iota 	 '⍳'	 (1, 0, 0, 0)
		 ('int',) "list of integer values from 1 to n"
range 	 '‥'	 (2, 0, 0, 0)
		 ('int', 'int') "list of integer values in the range m to n"
copies 	 '⧉'	 (2, 0, 0, 0)
		 ('any', 'int') "create a list containing n copies of v"
digits 	 'ⁿ'	 (1, 0, 0, 0)
		 ('int',) "list the digits of an integer value"
		 ('str',) "convert a string into a list of character code points"
```

Lists are mutable and a few operators allow the contents of the list to be altered in place:
```
replace  '@'	 (1, 2, 0, 0)
		 ('List', 'int', 'any') "replace the value at an index in a list"
		 ('List', 'Slice', 'any') "replace values in a list given by slice"
		 ('Array', 'Array', 'any') "replace all values at the given indices"
		 ('Array', 'int', 'any') "replace the value at an index in a list"
		 ('Dictionary', 'any', 'any') "set the value for a key"
```

The following commands are specific to lists and take part of the list to create a new list.
```
skip 	 '٪'	 (1, 1, 0, 0)
		 ('List', 'int') "take every nth item in a list"
slice 	 '['	 (1, 3, 0, 0)
		 ('List', 'any', 'any', 'any') "create a new list by taking a slice from the list [start : stop : step]"
		 ('str', 'any', 'any', 'any') "create a new string by taking a slice from the string [start : stop : step]"
```

Coordinates are similar to lists in that they are one-dimensional flat arrays. However, they can only contain integer values and do not get integrated into the structure when a list is promoted. They are useful as vectors and used as the data structure for indexing into a structured array or matrix. The following commands are specific to coordinates:
```
coordinate 	 '¢'	 (1, 0, 0, 0)
		 ('Array',) "create a coordinate using values from a list"
index list 	 'ɨ'	 (1, 0, 0, 0)
		 ('Coordinate',) "convert a coordinate to a list of values"
```

Structured arrays are rectangular multi-dimensional arrays (ie. all of their sub-arrays are the same dimension)
The following commands apply mainly to structured arrays:
```
set coord 	 '⌘'	 (1, 3, 0, 0)
		 ('Array', 'int', 'int', 'any') "set a matrix element value"
row 	 '𝖗'	 (2, 0, 0, 0)
		 ('Array', 'int') "select a row of an array"
col 	 '𝖈'	 (2, 0, 0, 0)
		 ('Array', 'int') "select a column of an array"
reshape 	 '⍴'	 (3, 0, 0, 0)
		 ('Array', 'int', 'int') "reshape an 2-dimensional structured array"
transpose 	 '⦰'	 (1, 0, 0, 0)
		 ('Array',) "transpose the rows and columns of a structured array"
reflect 	 '⎅'	 (1, 0, 0, 0)
		 ('List',) "reverse a list"
		 ('Array',) "reverse a structured array on its last axis (reverse each row)"
		 ('str',) "reverse a string"
flip 	 '⏛'	 (1, 0, 0, 0)
		 ('Array',) "reverse a structured array on its first axis (reverse each column)"
rotate 	 '⏀'	 (2, 0, 0, 0)
		 ('Array', 'int') "rotate a structured array on its last axis (cycle the row values)"
rotate up 	 '⦵'	 (2, 0, 0, 0)
		 ('Array', 'int') "rotate a structured array on its first axis (cycle the column values)"
shr 	 '↦'	 (1, 0, 0, 0)
		 ('Array',) "shift the values in an array 1 to the right, filling the gap with a default value"
shl 	 '↤'	 (1, 0, 0, 0)
		 ('Array',) "shift the values in an array 1 to the left, filling the gap with a default value"
shu 	 '↥'	 (1, 0, 0, 0)
		 ('Array',) "shift the values in a structured array 1 up, filling the gap with 0s"
shd 	 '↧'	 (1, 0, 0, 0)
		 ('Array',) "shift the values in a structured array 1 down, filling the gap with 0s"
stack 	 '⊜'	 (2, 0, 0, 0)
		 ('Array', 'Array') "stack two structured arrays on top of each other"
full reduce 	 '⥸'	 (1, 0, 1, 0)
		 ('Array', 'fn') "apply the function between all values in a structured array"
equivalent 	 '≡'	 (2, 0, 0, 0)
		 ('Array', 'Array') "equivalence of all values and shapes of two arrays"
not equivalent 	 '≢'	 (2, 0, 0, 0)
		 ('Array', 'Array') "non-equivalence of values and shapes of two arrays"
matrix binary 	 '⊙'	 (2, 0, 1, 0)
		 ('Array', 'Array', 'fn') "apply a binary function to the values in two arrays element-wise"
```

Matrices are a specialisation of structured arrays that can take floating point values and have some additional operations specific to their type. The following construct matrices:
```
identity matrix 	 '𝚰'	 (1, 0, 0, 0)
		 ('int',) "creates a new n x n identity matrix"
matrix fill 	 '𝕄'	 (3, 0, 0, 0)
		 ('int', 'int', 'int') "creates a matrix size n x m filled with a given value"
diagonal matrix 	 '⧅'	 (1, 0, 0, 0)
		 ('List',) "creates an n x n matrix, whose diagonal elements are taken from a list"
stack2mat 	 '⌸'	 (0, 0, 0, 0)
		 () "convert values on the stack (from the last null) to a matrix"
list2mat 	 '⊡'	 (1, 0, 0, 0)
		 ('List',) "convert a structured list to a matrix"
```

The following commands are specific to matrices, but structured arrays may be coerced to matrices in some cases.
```
matmul 	 '⊠'	 (2, 0, 0, 0)
		 ('Array', 'Array') "matrix multiplication"
inverse 	 '⌹'	 (1, 0, 0, 0)
		 ('Matrix',) "matrix inverse"
determinant 	 '𝚲'	 (1, 0, 0, 0)
		 ('Matrix',) "matrix determinant "
diagonalize 	 'ℰ'	 (1, 0, 0, 0)
		 ('Matrix',) "return an n x n diagonal eigenvalue matrix and an n x n eigenvector matrix"
```

A set is a list of unique values in no specific order. Any array can be provided to the following set operations, however after the following set operations, duplicates and nulls will be removed and the order is not guaranteed to remain the same.
```
exclusion 	 '⟈'	 (2, 0, 0, 0)
		 ('Array', 'Array') "set of elements in the first list not in the second"
		 ('List', 'int') "the set of elements in the list excluding the given element"
		 ('str', 'str') "remove all characters from the first string that appear in the second string"
intersection 	 '∩'	 (2, 0, 0, 0)
		 ('Array', 'Array') "all elements in both lists"
		 ('str', 'str') "remove all characters from the first string that do not appear in the second string"
union 	 '∪'	 (2, 0, 0, 0)
		 ('Array', 'Array') "all unique elements from both lists"
		 ('List', 'str') "join strings in the list using the given string as a separator"
unique 	 'ṵ'	 (1, 0, 0, 0)
		 ('Array',) "the set of all unique items in an array"
pop 	 '⬇'	 (1, 0, 0, 0)
		 ('Array',) "removes one (unspecified) value from a set"
add 	 '⬆'	 (2, 0, 0, 0)
		 ('Array', 'any') "adds a value to a set if not already present"
```

It is possible to convert from flat arrays (lists and coordinates) to structured arrays, and from structured arrays and matrices back to flat arrays (note that matrix values may be converted to integers). The following operators make these conversions.
```
promote 	 '⇑'	 (1, 0, 0, 0)
		 ('Array',) "convert a flat list of lists to a structured array"
demote 	 '⇓'	 (1, 0, 0, 0)
		 ('Array',) "demote a structured array to a flat list of lists"
```

The following operators are applicable to all kinds of array, but may have different meanings for structured and flat arrays.
```
count 	 '#'	 (1, 0, 0, 0)
		 ('str',) "string length"
		 ('List',) "the length of a flat list"
		 ('Coordinate',) "the dimension of a coordinate index"
		 ('Array',) "the size of the first axis of a structured array"
split 	 '⤲'	 (2, 0, 0, 0)
		 ('str', 'str') "split a string using characters from the second string"
		 ('Array', 'any') "split a list using an element or list of elements"
flatten 	 '▭'	 (1, 0, 0, 0)
		 ('Array',) "flatten a structured list into a 1 x n list"
join 	 '⊕'	 (2, 0, 0, 0)
		 ('Matrix', 'Array') "join structured arrays side-by-side"
		 ('Array', 'Array') "join lists side=by-side"
		 ('str', 'str') "concatenate strings"
		 ('None', 'str') "concatenate strings"
replace? 	 'ⓐ'	 (1, 2, 0, 0)
		 ('Array', 'Array', 'any') "set list values indicated by boolean list of the same shape"
take 	 '↑'	 (1, 1, 0, 0)
		 ('Array', 'int') "take the first n values"
drop 	 '↓'	 (1, 1, 0, 0)
		 ('Array', 'int') "drop the first n values"
sort 	 '↗'	 (1, 0, 0, 0)
		 ('Array',) "sort the list from smallest to largest"
		 ('str',) "sort the characters in a string from smallest to largest"
r sort 	 '↘'	 (1, 0, 0, 0)
		 ('Array',) "sort the list from largest to smallest"
		 ('str',) "sort the characters in a string from largest to smallest"
grade 	 '⍋'	 (1, 0, 0, 0)
		 ('Array',) "indices of elements of the list in ascending sort order"
r grade 	 '⍒'	 (1, 0, 0, 0)
		 ('Array',) "indices of elements of the list in descending sort order"
select? 	 '⊃'	 (2, 0, 0, 0)
		 ('Array', 'Array') "select items using a boolean list"
		 ('str', 'Array') "select characters of a string using a boolean list"
select 	 '⊇'	 (2, 0, 0, 0)
		 ('str', 'Array') "select characters of a string using a list of indices"
		 ('Matrix', 'Coordinate') "select an element of a matrix using a coordinate"
		 ('Array', 'Array') "select items using a list of indices"
		 ('Array', 'int') "select an item from a list at a given index"
		 ('str', 'int') "select a character from a string at a given index"
		 ('Coordinate', 'int') "select the nth dimension value in a coordinate"
		 ('Coordinate', 'Coordinate') "permute one coordinate using another"
		 ('Dictionary', 'List') "fetch values from a dictionary using a list of keys"
		 ('Dictionary', 'any') "fetch a value from a dictionary by key"
partition 	 '⊂'	 (2, 0, 0, 0)
		 ('Array', 'Array') "partition a list using a list to indicate which partition to assign each value"
		 ('str', 'Array') "partition a string using a list to indicate which partition to assign each character"
group 	 '⊆'	 (2, 0, 0, 0)
		 ('Array', 'Array') "group elements of an array using an array as a selector"
		 ('str', 'Array') "group characters in a string using an array as a selector"
member of? 	 '∈'	 (2, 0, 0, 0)
		 ('Array', 'Array') "returns a boolean list indicating which items are members of the second list"
		 ('str', 'str') "is the string contained in the second string"
		 ('any', 'Array') "is the item in the list"
find all 	 '⋸'	 (2, 0, 0, 0)
		 ('Array', 'Array') "returns the index of the first match of any item in the first list in the second list"
		 ('str', 'str') "returns the index of matches of items in the second string in the first string"
		 ('Array', 'any') "returns the first index where the item is found in the list"
find all? 	 '∊'	 (2, 0, 0, 0)
		 ('Array', 'Array') "returns a boolean list indicating where a member of the second list appears in the first list"
		 ('str', 'str') "returns a boolean list indicating where in the first string any character in the second appears"
		 ('Array', 'any') "returns a boolean list indicating where the value appears in the list"
bool list 	 '⋥'	 (2, 0, 0, 0)
		 ('Array', 'Array') "converts a list of indices to a boolean mask given a template list"
		 ('Array', 'int') "converts a list of indices to a boolean mask given a length"
indices 	 '⊒'	 (1, 0, 0, 0)
		 ('Array',) "converts a boolean mask into a list of indices"
first index 	 '⊐'	 (1, 0, 0, 0)
		 ('Array',) "index of the first 1 in a boolean list"
classify 	 '⊏'	 (1, 0, 0, 0)
		 ('Array',) "return array containing the indices of the first of each unique value in the list"
```


## Other Objects: Strings, Dictionaries and Slices

Slices are constructed with `{` 'make slice'
```
make slice 	 '{'	 (0, 3, 0, 0)
		 ('any', 'any', 'any') "create a slice object [start : stop : step]"
```

Strings can make use of a number of array functions, but the following are specific to strings.
```
str 	 '''	 (1, 0, 0, 0)
		 ('Array',) "join the elements of a list as strings"
		 ('any',) "convert to a string"
decode 	 '¦'	 (1, 0, 0, 0)
		 ('Array',) "convert a list of ascii code points to a string"
		 ('int',) "convert an ascii code point to a string character"
integer 	 'ℤ'	 (1, 0, 0, 0)
		 ('str',) "convert a string to an integer value"
		 ('any',) "convert object to an integer"
```

Dictionaries can be constructed with.
```
dictionary 	 'Δ'	 (0, 1, 0, 0)
		 ('str',) "create a new dictionary and assign a name"
```
They are respectively set and read with the following array commands.
```
select 	 '⊇'	 (2, 0, 0, 0)
		 ('Dictionary', 'List') "fetch values from a dictionary using a list of keys"
		 ('Dictionary', 'any') "fetch a value from a dictionary by key"
replace  '@'	 (1, 2, 0, 0)
		 ('Dictionary', 'any', 'any') "set the value for a key"
```

## Higher Level Functions and Combinators

Functional programming languages typically provide primives for map, filter and reduce that take functions and alter a list, array, stream, iterator or similar structure of values. They are also available in fbleet. While they are simple for lists, in the case of structured arrays, care is required to ensure the correct axis is being applied - for the most part operators behave similarly to their APL counterparts.
```
map 	 '¨'	 (1, 0, 1, 0)
		 ('Array', 'fn') "apply the function to each value of the array and return a new array of the same shape"
		 ('str', 'fn') "apply the function to each character in the string and return the result in a list"
filter 	 '}'	 (1, 0, 1, 0)
		 ('Array', 'fn') "remove values for which the function returns a falsy value"
reduce 	 '/'	 (1, 0, 1, 0)
		 ('List', 'fn') "apply the function between each value in a flat list"
		 ('Array', 'fn') "apply the function between each sub-array on the last axis of a structured array"
window 	 '⧈'	 (1, 1, 1, 0)
		 ('Array', 'int', 'fn') "perform a reduction on an n x n... window around each cell"
stencil 	 '⌺'	 (1, 1, 1, 0)
		 ('Array', 'int', 'fn') "perform a reduction on an n x n... window around each cell, including edge cells"
fold r 	 '⥆'	 (1, 0, 1, 0)
		 ('Array', 'fn') "apply the function between each value and the remaining list"
scan 	 '∖'	 (1, 0, 1, 0)
		 ('Array', 'fn') "provide the partial sums of a reduction"
scan r 	 '⥶'	 (1, 0, 1, 0)
		 ('Array', 'fn') "provide the partial sums of a right fold reduction"
col reduce 	 '⌿'	 (1, 0, 1, 0)
		 ('Array', 'fn') "reduce on first axis (apply the reduction to each column)"
row map 	 '⋯'	 (1, 0, 1, 0)
		 ('Array', 'fn') "apply a function to each row of an array and return the results as a list"
col map 	 '⋮'	 (1, 0, 1, 0)
		 ('Array', 'fn') "apply a function to each column of an array and return the results as a list"
outer-product 	 '⊚'	 (2, 0, 1, 0)
		 ('Array', 'str', 'fn') "table given by applying the function to all pairings of items in the list and characters in the string"
		 ('str', 'List', 'fn') "table given by applying the function to all pairings of items in the list and characters in the string"
		 ('Array', 'Array', 'fn') "table given by applying the function to all pairings of items in the two lists"
		 ('str', 'str', 'fn') "table given by applying the function to all pairings of characters in the two strings"
inner-product 	 '•'	 (2, 0, 2, 0)
		 ('Array', 'Array', 'fn', 'fn') "inner product of two arrays formed by applying the first function to the results of the product of the rows from the first array and columns of the second"
```

A separate document is provided on [Combinatory Logic](Combinatory%20Logic.md). The concept is that programs are more easily understood when state is not a part of the construction of the program. A program composed of pure functions is structured using combinators, which combine functions together to create complex behaviours. While the ideal of a purely functional program can be realised theoretically, in practice it is used for relatively small parts of programs that follow common structural patterns. The S, Phi and Psi combinators are sufficiently common that they form an integral part of APL syntax, but in fb1337 they must be explicitly invoked. The following combinators are provided.

```
identity 	 'ℐ'	 (0, 0, 1, 0)
		 ('fn',) "identity combinator (returns its input untouched) *Pf -> f(*)"
constant 	 '𝒦'	 (1, 1, 0, 0)
		 ('any', 'any') "constant combinator (returns x for any input) Kx -> x"
join combinator 	 '𝒲'	 (0, 0, 1, 0)
		 ('fn',) "join combinator (uses its input twice) xPf -> f(x,x)"
flip combinator 	 '𝒞'	 (0, 0, 1, 0)
		 ('fn',) "flip combinator (reverses its inputs) xyPf -> f(y,x)"
compose 	 '∘'	 (0, 0, 2, 0)
		 ('fn', 'fn') "compose combinator (applies one function after another) *Pfg -> g(f(*))"
compare combinator 	 '𝒮'	 (0, 0, 2, 0)
		 ('fn', 'fn') "compare combinator (applies a function to its input and a processed version of its input) xPfg -> f(x,g(x))"
compare flipped combinator 	 '𝔰'	 (0, 0, 2, 0)
		 ('fn', 'fn') "compare combinator (applies a function to a processed version of its input, and its input) xPfg -> f(g(x), x)"
on combinator 	 '𝚿'	 (0, 0, 2, 0)
		 ('fn', 'fn') "on combinator (processes both inputs before applying a function) xyPfg -> f(g(x),g(y))"
D fork 	 '𝒟'	 (0, 0, 3, 0)
		 ('fn', 'fn', 'fn') "D fork (applies different functions to its inputs and then combines them) xyPfgh -> f(g(x),h(y))"
phi fork 	 '𝚽'	 (0, 0, 3, 0)
		 ('fn', 'fn', 'fn') "fork (applies two different functions to the same input before combining them) xPfgh -> f(g(x),h(x))"
phi dyad fork 	 '𝛗'	 (0, 0, 3, 0)
		 ('fn', 'fn', 'fn') "fork (applies two different functions to the same inputs before combining them) xyPfgh -> f(g(x,y),h(x,y))"
repeat until 	 '⍣'	 (0, 0, 2, 0)
		 ('fn', 'fn') "repeatedly apply a function until the condition is false ⍣fg f.f... until not g"
repeat 	 '…'	 (1, 0, 1, 0)
		 ('int', 'fn') "Apply a function n times to the same input"
bind left 	 '⊸'	 (0, 1, 1, 0)
		 ('any', 'fn') "Bind left (partially apply the function with its first input) xPf -> λy.f(x,y)"
bind right 	 '⟜'	 (0, 1, 1, 0)
		 ('any', 'fn') "Bind right (partially apply the function with its second input) xPf -> λy.f(y,x)"
dip 	 '⍮'	 (0, 0, 1, 0)
		 ('fn',) "Dip (apply the function to the second stack value) xyPf -> f(x),y"
defer 	 '⩣'	 (0, 0, 1, 0)
		 ('fn',) "Defer execution and create a function object"
```


## File Handling

Programs can access files to write values and read values and arrays. It should be noted that they can only access one file for input and one file for output. The input file is in the same directory the program is being run from and is named '[name].in' where name is the name of the program provided to the Environment by the run functions in fbleet.py, or is provided as the 0th parameter variable. Output is directed to the file '[name].out' also in the same directory as the file the program is being run from.

```
load 	 '∫'	 (0, 0, 0, 0)
		 () "load a value from file"
save 	 '⨋'	 (1, 0, 0, 0)
		 ('any',) "save a value to file"
load list 	 '∮'	 (0, 0, 0, 0)
		 () "create a list with values from a file"
load array 	 '⨖'	 (0, 0, 0, 0)
		 () "crete a structured array using values from a file"
```