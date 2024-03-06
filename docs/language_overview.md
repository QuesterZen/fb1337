# fb1337 Language Overview

fb1337 is an experimental, highly expressive, stack- and array- based code golfing language written in Python.

Its goal is to explore the limits of expressiveness and brevity in translating algorithms into runnable code.

FizzBuzz in fb1337 is a mere 20 characters long!

```fb1337
ḣ:Fizz‿Buzz3‿5_|⊃'_∨
```

## Language Features

### Values

Values are automatically pushed onto the stack when evaluated.

fb1337 has a small number of types

1. **number** Numbers are integer values. Type in `137` and get the value 137. For negative numbers, place a `~` sign in front of them, so `~42` becomes -42. Floating point numbers are only allowed when they are in a Matrix (see below). If you use a floating point value as a program parameter, it will be converted to a 1x1 Matrix.
   Some values have shortcut glyphs, for example `ṫ` means 10, : `ḣ` means 100 and `ḳ` means 1000.

2. **string literal**. Strings of alphabet characters are turned into string literals. These can be treated as string values, or used as variable names. It is possible to include non-alphabet characters by escaping them with a back-tick character. So we can write the hello_world program in fb1337 as  ```Hello` World`!```, where the space and exclamation mark need to be escaped. 
   When used as variable names, the sigils `$` and `£` are used to access the value. `$` is an operator which pushes the value to the stack, `£` is an operator that evaluates or runs the value.

3. **null**. The special value `Ø` is the null character. It can represent the value 0 when used in place of an integer, an empty string '' when used in place of a string, and the value 'False' when used in place of a boolean value. 
   When used as a value in a FlatList, this item is skipped when the list is iterated over, and it is removed when the FlatList is output by the program. 
   It also has special meaning as a stack-marker when pushed onto the stack.

4. **Array**. There are 4 array types. Arrays are the main type in fb1337 and the majority of operators primarily act on arrays or can be coerced into acting on arrays; for example, any operator that works on integers, will apply to an array of numbers by acting element-wise.
   
   1. **FlatList** is a flat array that can contain any objects, including other arrays or any size or type. 
      There are several easy ways to create FlatLists
      
      - `‿` 'pair' joins values into lists, so `3‿4‿5` evaluates to the array `[3 4 5]`;
      
      - `☐` 'gather' takes n values from the stack and puts them in a list so `3 4 5 ☐3` also creates the list `[3 4 5]`
      
      - `⍳` 'iota' creates a list of values. For example, `5⍳` evaluates to `[1 2 3 4 5]`. Using a negative value creates a descending list so `~5⍳` creates the list `[5 4 3 2 1]`
      
      - `‥` 'range' is similar, but can start at any value, so `3 5‥` evaluates to the list `[3 4 5]`.
   
   2. **StructuredArray** is a rectangular, nested array of any dimension. Generally they act like Matrices, but like FlatLists, they can contain values of any kind.
      They can be created by promoting a FlatList using `⇑` 'promote' or with `⍴` 'reshape'. StructuredArrays can be converted back into a FlatList using `⇓` 'demote' or `▭` 'flatten'.
   
   3. **Coordinate** is lists of integers. They are the type used for creating indices to items in StructuredArrays. They are also useful as 1-D vectors.
      They are treated as single values by most structure-related operators. 
      They are created from FlatLists by `¢` 'coordinate' and turned back into FlatLists by `ɨ` 'index list'.
   
   4. **Matrix** is similar to a StructuredArray but all of its values are 64-bit floating point numbers. Matrices can make use of Python numpy library functions and are often much faster than using StructuredArrays or FlatLists. They also have their own set of specific matrix functions.
      Matrices are created most easily in the following ways:
      
      - from a FlatList or StructuredArray with `⊡` 'list2mat'
      
      - by creating one a new matrix with on of the following:  `𝚰` 'matrix id', an `nxn` identity matrix; `𝕄` 'matrix fill', a shaped matrix of a single value; or `⧅` 'matrix diagonal' which converts a FlatList of length n into an `nxn` diagonal matrix.

5. **Slice** is a special type that can represent a range of values, much like a Python slice object. For example the slice `{2 10 3` represents the FlatList indices [2 5 8], i.e. the slice starts at 2, ends at 10 and takes every 3rd value. null can be provided in one or more of the inputs. For example `{3ØØ` will start at position 3, continue to the end with increment 1. 
   Slices are useful for extracting or value-setting a range of elements in a FlatList. A slice is created with the operator `{` 'make slice'.

### Operators

fb1337 uses single-character unicode glyphs to represent built-in operations. For example the glyph `⊃` represents the operation 'select', which takes two stack variables and returns the values in the first list that correspond to 'truthy' values in the second.
For example, if the stack contains the lists [1 2 3 4] and [0 3 "hello" ""] then after applying `⊃`, the stack will contain the list [2 3]. (The values 0 and "" are considered 'falsy').

Each glyph has a common signature, meaning that it will take a fixed number of values from the stack, or from the code following it. But each glyph will have many different behaviours depending on the types of the values passed to it.

For example, the glyph `⊚` 'outer product'. Creates a table from two arrays.
Its signature is `(2, 0, 1, 0)`, meaning that it takes:

- 2 parameters from the stack

- 0 parameters from the code ahead

- 1 functional parameter

- 0 block parameters

A typical use would be ⊚×, applied to a stack containing the arrays [1 2] and [3 4 5]. It will produce a multiplication table of pairs of values one in each list. The result will be the StructuredArray [[3 4 5], [6 8 10]].

There are several type specialisations of 'outer product' including:

- ('Array', 'Array', 'fn') as we have seen

- ('str', 'str', 'fn') which turns each of the strings into arrays of characters before applying a binary function, fn to the pairs of characters

The full list of operations and their type-specialisations can be obtained by typing `?` into the [Command Assistant](#tools-to-aid-programming-in-fb1337).

### The Stack

When values are evaluated, they are pushed onto the stack. Most operations take their parameters from the stack. As a result, the evaluation order, and hence the way to read programs, is dictated by the stack. This is sometimes referred to as Reverse Polish order or post-fix, which may be familiar from stack-based languages such as Forth, or calculators like the HP15C.

The program ```5 3 + 7 ×``` evaluates as `(5 + 3) × 7` in more familiar mathematical in-fix notation. We can read the program as follows:

| Evaluate | Meaning          | Stack |
|----------|------------------|-------|
| 5        | push the value 5 | 5     |
| 3        | push the value 3 | 5 3   |
| +        | apply 'add' (2)  | 8     |
| 7        | push the value 7 | 8 7   |
| ×        | apply 'mul' (2)  | 56    |

When reading and reasoning about programs, it is important to understand the state of the stack. 
A range of operators are provided for managing the stack. The most useful are:

- `◌` 'drop' removes the top value from the stack
- `∂` 'dup' copies the top value on the stack
- `«` 'swap' swaps the top two values on the stack
- `⨩` 'under' copies the second value to the top of the stack
- `®` 'rot' removes the third value from the stack and brings it to the top

## Variables

Values and code blocks can be assigned names in the local environment using `→`'assign'. You can recover the value using `$`'lookup' and the name. For example,

```fb1337
3 4 + →seven, 8 $seven ×
```

returns `56`.

Variables can also be used with code blocks. `⏎`'run' will run a block. If a block is named, it can also be run using `£`'execute'. Since the environment is resolved when the block is executed, not when it is defined, we can easily create recursive functions.

```fb1337
µ∂1= ? ⊢ µ∂ ⩔£factorial ×))→factorial, 5 £factorial
```

## A Sample Program

An example of a complete fb1337 program is the 20-character implementation of the game FizzBuzz:

```fb1337
ḣ:Fizz‿Buzz3‿5_|⊃'_∨
```

This uses the following glyphs

- `ḣ` is the value 100
- `: 'iterate' (1, 0, 0, 1) ('Iterator', 'block')`
    Converts the value 100 to an iterator producing the values 1 to 100 inclusive
- `‿ 'pair' (1, 1, 0, 0) ('any', 'any')`
    Creates the arrays ['Fizz' 'Buzz'] and [3 5]
- `| 'divides' (2, 0, 0, 0) ('int', 'int')`
    Returns 1 if first value divides the second, or 0 otherwise. Given a stack containing `[3 5] 6`, it returns the array `[1 0]`. This also demonstrates that integer operators can be coerced into maps over arrays.
- `⊃ 'select?' (2, 0, 0, 0) ('Array', 'Array')`
    Selects items in the first array if the corresponding value in the second is 'truthy'. For example, with ['Fizz' 'Buzz'] and [1 0] on the stack, it will return ['Fizz']
- `' 'str' (1, 0, 0, 0) ('Array',)`
    Stringifies any object. When given an array, it will turn each value into a string and concatenate them without spaces.
- `_ 'implicit' (0, 0, 0, 0) ()`
    Returns the current value of the active iterator, in this case the loop value
- `∨ 'or' (2, 0, 0, 0) ('int', 'int')`
    As in Lisp and Python, 'or' in fb1337 returns the first value if it is truthy (in this case, a non-empty string), or else the second value (in this case the value provided by 'implicit')

The code block is executed as follows when the iterator has the value 6:

| Command   | Effect                             | Stack                     |
|-----------|------------------------------------|---------------------------|
| Fizz‿Buzz | push ['Fizz' 'Buzz']               | ['Fizz' 'Buzz']           |
| 3‿5       | push [3 5]                         | ['Fizz' 'Buzz'], [3 5]    |
| _         | push implicit value 6              | ['Fizz' 'Buzz'], [3 5], 6 |
| \|        | pop two values and apply 'div'     | ['Fizz' 'Buzz'], [1 0]    |
| ⊃         | pop two values and apply 'select?' | ['Fizz']                  |
| '         | pop one value and apply 'str'      | 'Fizz'                    |
| _         | push implicit value 6              | 'Fizz', 6                 |
| ∨         | pop two values and apply 'or'      | 'Fizz'                    |

At the end of the iteration, 'Fizz' is left on the stack. At the conclusion of the program, all the values remaining on the stack (1 2 'Fizz' 4 'Buzz' ...) are returned as a list.

## A Few More Program Examples

The following are a selection of shorter solutions from Project Euler and LeetCode challenges.

### Project Euler 6

Problem: Find the difference between the square of the sum and the sum of the squares of the first 100 natural numbers

Solution:

```fb1337
➊⍳ 𝚽-∘/+²∘²/+
```

parameters: [100]

- `➊ 'p1' (0, 0, 0, 0)`
    Return the first parameter value (100)
- `⍳ 'iota' (1, 0, 0, 0) ('int',)`
    Create a list of integers 1..100
- `𝚽 'fork' (0, 0, 3, 0) ('fn', 'fn', 'fn')`
    A combinator which applies two different functions to the same input value and combines them with the third. Here we apply `-` to the result of `∘/+²` and `∘²/+` each applied to the list. This is similar to the fork in APL.
- `- 'sub' (2, 0, 0, 0) ('int', 'int')`
    Subtract the second value from the first
- `∘ 'compose' (0, 0, 2, 0) ('fn', 'fn')`
    Another combinator, in this case it composes the functions `/+` and `²` into a single function
- `/ 'reduce' (1, 0, 1, 0) ('List', 'fn')`
    Apply the following function between each value in the list, here `/+` means sum the values in the list
- `+ 'add' (2, 0, 0, 0) ('int', 'int')`
    Add two values
- `² 'sqr' (1, 0, 0, 0) ('int',)`
     Square a value

Note that it is slightly shorter to write this using the stack and repeating the input list, rather than using combinators as:

```fb1337
➊⍳/+² ➊⍳²/+ -
```

### Project Euler 15

Problem. In a 20x20 grid, how many routes consisting of only down and right (and staying on the grid) can be taken between the top left and bottom right of the grid?

Solution:

```fb1337
1➊⩓⧉➊…∖+➊⊇
```

parameters: [20]

- `1` 
    Push the value 1 to the stack
- `➊ 'p1' (0, 0, 0, 0)`
    Push the first parameter value, 20 to the stack
- `⩓ 'inc' (1, 0, 0, 0) ('int',)`
    Add one to the value. The stack now contains the value 21
- `⧉ 'copies' (2, 0, 0, 0) ('any', 'int')`
    Creates a list of n copies of a value. Here, a list with 21 1s
- `… 'repeat' (1, 0, 1, 0) ('int', 'fn')`
    Apply a function n times. In this case we apply `\+` 20 times
- `\ 'scan' (1, 0, 1, 0) ('Array', 'fn')`
    Create a list containing the partial sums at each step in a reduction
- `+ 'add' (2, 0, 0, 0) ('int', 'int')`
    Add two values
- `⊇ 'select' (2, 0, 0, 0) ('List', 'int')`
    Select the nth value in the list

The program builds up the diagonals of a Pascal Triangle, starting with the 1s diagonal using 'scan' to create the next diagonal. 

The idea is that the number of routes to the grid square `(n m)` is the value at `(2n m)` in Pascal's triangle. The calculation makes use of a mathematical identity: the values at `(n r)` in Pascal's Triangle are equal to the sum of the values on the diagonal `(n-1 r-1), (n-2 r-1) ... (r-1 r-1)`. 

An even shorter solution is to use the built-in `‼` 'binom' operator.

```fb1337
➊𝔰‼⟜2×
```

- `𝔰 'flipped compare combinator' (0, 0, 2, 0) ('fn', 'fn')`
     A combinator which applies a function to two copies of an input, one of which has had a second function applied. Here ‼ is applied to 20 after applying double (`⟜2×`), and to 20 unchanged
- `⟜ 'bind right' (0, 1, 1, 0) ('any', 'fn')`
    Bind a value to a function. It partially applies its value (2) to the function (`×`). The result is a new function of one integer variable that doubles any value it is given
- `× 'mul' (2, 0, 0, 0) ('int', 'int')`
    Multiply two values

Again, manipulating the stack makes the program slightly shorter.

```fb1337
➊∂+➊‼
```

## LeetCode 1614

Problem: What is the maximum nesting depth of parentheses in a mathematical expression given as a string

Solution:

```fb1337
➊ `(`) ⊚= ⇑ /- ∖+ /⌈
```

parameters: ["(1+(2×3)+((8)/4))+1"]

- `➊ 'p1' (0, 0, 0, 0)`
    Push the string to the stack
- \`\(\`\)
    Push the string "()" to the stack
- `⊚ 'outer product' (2, 0, 1, 0) ('str', 'str', 'fn')`
    Create a table using the characters from each string, applying the function to every pair
- `= 'equal' (2, 0, 0, 0) ('str', 'str')`
    Test whether two strings are the same
- `⇑ 'promote' (1, 0, 0, 0) ('Array')`
    Promotes the resulting table into a StructuredArray
- `/ 'reduce' (1, 0, 1, 0) ('Matrix', 'fn')`
    Perform a reduction on the columns of the array, resulting in a list of values, one for each column
- `- 'sub' (2, 0, 0, 0) ('int', 'int')`
    Subtract the second value from the first
- `\ 'scan' (1, 0, 1, 0) ('List', 'fn')`
    Produce a row scan consisting of the partial sums of a reduction
- `= 'add' (2, 0, 0, 0) ('int', 'int')`
    Add two values
- `⌈ 'max' (2, 0, 0, 0) ('int', 'int')`
    Take the maximum of two values

The idea is that we produce a table indicating where the '(' and ')' characters are in the string and use it to calculate the maximum nesting depth at each point as follows:

```
➊
   ( 1 + ( 2 × 3 ) + ( ( 8 ) / 4 ) ) + 1

`(`) ⊚=
 [[1 0 0 1 0 0 0 0 0 1 1 0 0 0 0 0 0 0 0]
  [0 0 0 0 0 0 0 1 0 0 0 0 1 0 0 1 1 0 0]]

/-
  [1 0 0 1 0 0 0-1 0 1 1 0-1 0 0-1-1 0 0]

\+
  [1 1 1 2 2 2 2 1 1 2 3 3 2 2 2 1 0 0 0]

/⌈
  3
```

### LeetCode 801

Problem: What is the fewest number of same-position swaps to make two lists both strictly increasing?

```fb1337
➊#→n ➊⧈2< ➋⧈2< ∧¬$n× ➊➋↓1< ➋➊↓1< ∧¬$n× 0 1
$n⩔: ⇶4 ⑴↓1  ⑵↓1  ⑶⑴0⊇+⑷⑵0⊇+⌊ ⑷⑴0⊇+⑶⑵0⊇+⌊⩓;
⇶4 ⑶⑷⌊
```

Parameters: [[1, 3, 5, 4], [1, 2, 3, 7]]

This is a much harder problem than the others and the solution is more involved, but illustrative of some useful idioms in fb1337 programming, typical in longer programs. I will only explain the outline of the program.

`➊#→n` assigns the length of the first list to the variable `n` as we will be using it a couple of times further along in the program.

- `# 'count' (1, 0, 0, 0) ('List',)` The length of a list
- `→ 'assign' (1, 1, 0, 0) ('any', 'str')` Create a local variable accessible in the current environment and child environments using the string literal as a name

`➋⧈2<` pair-wise `<` on a sliding 2-length window on the list. The effect is to place a 1 whenever the value is greater than the one preceding it. For [1 3 5 4] it yields [1 1 0]

- `➋ 'p2' (0, 0, 0, 0)` Push the second program parameter to the stack
- `⧈ 'window' (1, 1, 1, 0) ('Array', 'int', 'fn')` Apply a reduction on all values within a given distance of each cell of an array.
- `< 'lt' (2, 0, 0, 0) ('int', 'int')` Less than

`∧¬$n×` performs a 'NAND' operation on the values in a list and multiplies the result by the value associated with the variable 'n'

- `∧ 'and' (2, 0, 0, 0) ('int', 'int')` Logical and
- `¬ 'not' (1, 0, 0, 0) ('int',)` Return 0 if the value is truthy, 1 otherwise
- `$ 'lookup' (0, 1, 0, 0) ('str',)` Look up the name in the local environment

`➊➋↓1<` compares each value in the first list with next value in the other list. For [1 3 5 4] and [1 2 3 7] we get [1 0 1] because 1 < 2, 3 !< 3 and 5 < 7.

- `↓ 'drop' (1, 1, 0, 0) ('Array', 'int')` Return the list without its first n values

`$n⩔:` iterates over the values `1..(n-1)`

- `⩔ 'dec' (1, 0, 0, 0) ('int',)` Decrement the value by 1

`⇶4` pops four values off the stack: the list indicating whether not swapping is OK, the list indicating whether swapping is OK, and the values 0 and 1 which will represent the minimum number of swaps required to make both lists strictly increasing if you finish on an un-swapped value (0), or a swapped value (1). We will iteratively solve the problem for progressively longer versions of the input lists. 0 and 1 are the solutions for the 1-length sub-lists.

- `⇶ 'pin' (0, 1, 0, 0) ('int',)` Take n values from the stack and make them available as local variables, accessible as `⑴`, `⑵`, `⑶` and `⑷`.

`⑴↓1` removes the first value from each list

`⑶⑴0⊇+⑷⑵0⊇+⌊` determines the number of swaps required to maintain strictly increasing order ending on an un-swapped value (the other similar terms does the same for ending on a swapped value)

- `⊇ 'select' (2, 0, 0, 0) ('List', 'int')` Pick the nth value from a list. In this case the first value from the list that indicates whether no swap or swap allows the list to remain in strictly increasing order.
- `⌊ 'min' (2, 0, 0, 0) ('int', 'int')` Select the smallest value
- `; 'return' (0, 0, 0, 0)` End a block. In this case it ends the iteration block and starts the next iteration as well as providing a point to jump to when iteration is complete

## Tools to aid programming in fb1337

1. **The Command Assistant**. Programming in fb1337 requires a little help. The glyphs are unicode characters that mostly have no easy way to enter on the keyboard. It is useful to keep a copy of the Code Assistant running while programming, so you can look up commands and copy their glyphs. If you can remember the name of the operator, you can simply type in its name to get a full description of the operator and its various type-specialisations.
   
   ```
   Command: mul
   mul      '×'     (2, 0, 0, 0)
         ('int', 'int') "multiply"
         ('None', 'int') "multiply"
         ('str', 'int') "string repeat"
         ('Coordinate', 'int') "scalar multiply"
   ```
   
   If not, you can search in the description by adding `?` to the end of the query.
   
   ```
   Command: set ?
   replace      '@'     (1, 2, 0, 0) ('Dictionary', 'any', 'any') "set the value for a key"
   exclusion    '⟈'    (2, 0, 0, 0) ('Array', 'Array') "set of elements in the first list not in the second"
   exclusion    '⟈'    (2, 0, 0, 0) ('List', 'int') "the set of elements in the list excluding the given element"
   unique       'ṵ'     (1, 0, 0, 0) ('Array',) "the set of all unique items in an array"
   add          '⬆'     (2, 0, 0, 0) ('Array', 'any') "adds a value to a set if not already present"
   replace?     'ⓐ'    (1, 2, 0, 0) ('Array', 'Array', 'any') "set list values indicated by boolean list of the same shape"
   set coord    '⌘'     (1, 3, 0, 0) ('Array', 'int', 'int', 'any') "set a matrix element value"
   ```

2. **The Interactive Debugger** can be started by running a program with `run_interactive` from the `fbleet.py` module or with the `-i` flag on the command line. This is a simple GUI interface what allows you to step through code token-by-token; see which type-specialisation the interpreter has chosen; which parameters it picked up; what the local and external environments contain; and a listing of all values on the stack.
   
   ![Interactive Debugger](./InteractiveDebuggerImage.jpg)

3. **Code Annotation** The fb1337 parser allows the user to annotate the code and provide some level of code formatting to make programs more readable.
   
    Whitespace characters space ' ' and newline '\n' are simply ignored as is comma ','. This makes it easier to lay out code and make it more readable. These characters also serve to separate values. `3 4` will return the values `3` and `4` and not  `34`.
   
    Parentheses work more or less as expected. They actually produce a block with a new local environment, which is run immediately, but the effect is to prioritise execution of the code between the brackets and provide the resulting value to the code
   
    Line comments start with a '\t' or `⍝` 'comment' character and last until the next newline. Comments are stored with the code token immediately preceding them and displayed in the Interactive Debugger when that token is being evaluated.
   
   ```fb1337
   ḣ:                    for i in range(1, 101):
   Fizz‿Buzz                {Fizz, Buzz} list of strings to select from
   3‿5_|                    {i divides 3?, i divides 5?} boolean selector list
   ⊃                        pick elements of string list based on whether 1/True in selector list
   '                        turn the resulting list of 0 or more strings into a single string
   _∨                        if string is '' then i else string
   ```

(Someday, I hope to get around to creating a fully interactive GUI programming sandbox, somewhat in the spirit of [BQN Pad](https://bqnpad.mechanize.systems).)

## Glyphs

If you are learning to experiment for the first time in fb1337, I would recommend restricting yourself to a smaller sub-set of the language. I would suggest the following subset of 50 glyphs, which is already sufficient to solve a very large range of problems and gives a good understanding of programming in fb1337.

```
Math
    ~ (neg) + (add) × (mul) - (sub) ÷ (div)
    % (mod) ⩲ (abs) ⌈ (max) ⌊ (min) 
    = (eq) < (lt) ≤ (lte) > (gt) ≥ (gte)
    ¬ (not) ∧ (and) ∨ (or)
Stack
    ◌ (drop) ∂ (dup) « (swap)
Control
    ? (if) : (iterate) ; (return)
    ( (paren) µ (mu) ⏎ (run) ) (end)
Lookup
    _ (implicit) $ (lookup) → (assign)
Arrays
    ‿ (pair) ⍳ (iota) ⁿ (digits) @ (replace) [ (slice)
    # (count) ⊕ (join) ↑ (take) ↓ (drop) ↗ (sort)
    ⊃ (select?) ⊇ (select) ⟈ (exclude) ∈ (member of?)
String
    ' (str)
Higher Level Functions / Combinators
    ¨ (map) } (filter) / (reduce) 
    ∘ (compose) ⟜ (bind r) ⍮ (dip)
```

The full set of glyphs can be found by typing ?? or all?? into the Command Assistant.

```
parser shortcuts and special symbols
	 ḣ ḳ Ḳ ṁ ḃ ṫ Ḷ ḟ Ḟ 
	 Ø ⍝
integer math
	 ~ + × - ÷ % ‰ ‱ | ℸ 𝜋 ⩲ ² √ ⊛ ± * ⨸ ⩓ ⩔
	 ! ‼ ⌈ ⌊ = ≠ < ≤ > ≥ ¬ ∧ ∨ ⟘ ⊤
array types
	 ‿ ⁔ ⏍ ☐ ☆ ⊟ ⍳ ‥ ⧉ ⁿ @ ٪ [ {
	 ⌘ 𝖗 𝖈 ⍴ ῤ ⦰ ⎅ ⏛ ⏀ ⦵ ↦ ↤ ↥ ↧ ⊜ ⥸ ≡ ≢ ⊙
	 𝚰 𝕄 ⧅ ⌸ ⊡ ⊠ ⌹ 𝚲 ¢ ɨ
	 ⟈ ∩ ∪ ṵ ⬇ ⬆
	 ⇑ ⇓ # ⤲ ▭ ⊕ ⓐ ↑ ↓ ↗ ↘ ⍋ ⍒ ⊃ ⊇ ⊂ ⊆ ∈ ⋸ ∊
	 ⋥ ⊒ ⊐ ⊏
strings and dictionaries
	 ' ¦ ℤ
	 Δ
high level functions and combinators
	 ¨ } / ⧈ ⌺ ⥆ ∖ ⥶ ⌿ ⋯ ⋮ ⊚ •
	 ℐ 𝒦 𝒲 𝒞 ∘ 𝒮 𝔰 𝚿 𝒟 𝚽 𝛗 ⍣ … ⊸ ⟜ ⍮ ⩣
environment variables
	 _ ⍛ $ £ → ⇶ ⇴
	 ➊ ➋ ➌ ➍ ➎ ⓪ ① ② ③ ④ ⑤ ⑴ ⑵ ⑶ ⑷ ⑸
stack management
	 ◌ ⊢ ⊣ ⊩ ⫣ ⫤ ∂ ð « ⨩ ḋ ®
control flow, iteration and function blocks
	 ? ⁈ ₡ €
	 Ω : ⌁ ;
	 ( λ µ κ ⏎ )
file handling
	 ∫ ⨋ ∮ ⨖
```

## Exercises

If you want to practice with the language, try solving the following problems, using the Interactive Debugger

1. Given the Lists [1 2 3 4 5 6 7]  and [3 2 1 6 5 4 7], return all the numbers that are the same value in the same place in both Lists. For example, 2 is the second value in both lists.

2. Given the List [5 6 8 9 3 2 10 8 4], return all the values that are between 3 and 7 inclusive.

3. Return the highest of the average values of the Lists [2 3 5 7] and [2 4 6 8].

4. For each value in the List [2 3 5 7 8 11 12 13], for the even values halve the value, for the odd values multiply by 3 and add 1. Repeat this 10 times.

5. Generate a list of all prime numbers up to 30

## Possible Solutions

The following solutions all use only the 50 glyph subset of the language indicated above.

1. `1‿2‿3‿4‿5‿6‿7 ∂ 3‿2‿1‿6‿5‿4‿7 =⊃`

2. `5‿6‿8‿9‿3‿2‿10‿8‿4 } µ∂ 3≥ « 7≤ ∧)`

3. `µ∂/+«#÷)→avg, 2‿3‿5‿7 £avg 2‿4‿6‿8 £avg ⌈`

4. `2‿3‿5‿7‿8‿11‿12‿13 10:¨µ∂ 2%0= ? µ2÷) µ3×1+))`

5. `µ∂ #0= ? ◌ µ∂ 0⊇→p } µ $p% 0>) $p« £prime))→prime, 30⍳↓1 £prime`
