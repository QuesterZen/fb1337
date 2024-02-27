# fb1337 The Parser

## Parsing Input Parameters

When entering values as program parameters, the following transformations are applied:
- (int) or (bool) -> number value
- (str)'' or (str)'Ø' -> 'null' value
- (str) + number shortcut symbol -> number value
- (str) otherwise -> string literal
- (float) -> Matrix object consisting of a single value and shape (1,)
- (dict) -> Dictionary object consisting of key, value pairs which are also parsed into fb1337 objects
- (list) or (tuple) containing equal-length lists of floats -> Matrix
- (list) or (tuple) containing (list)s or (tuple)s of varying lengths -> List of Lists
- (list) or (tuple) otherwise -> List object, the values of which are also parsed into fb1337 objects
- (lambda) with 1 argument -> Lambda object

For example, the parameters
```
[3, "hello", [[1,2,3],[4,5,6],[7,8,9]], {'a': 7, 'b':'Ø', 'c':False}, ['ape', '', 'banana', [1, 2, 3]]]
```
Is translated into the parameters:
```
1. <value 3>
2. <value "hello">
3. Matrix<[[1., 2., 3.], [4., 5., 6.], [7., 8., 9.]]>
4. Dictionary<{<value 'a'>: <value 7>, <value 'b'>: <value ''>, <value 'c'>: <value 0>}>
5. ListIterator< <<value "ape">> <value ''> <value "banana"> <ListIterator<<value 1>>> <value 2> <value 3> >
```


## Parsing Program Code Strings

The parser reads the text and breaks it into tokens using regex patterns. The following tokens are defined:

- 'noop' consisting of ` ` and `,`. These characters are not tokenised, but can be used a separators for example "3 4,5" will be read as three tokens: `<number 3> <number 4> <number 5>` and not `<number 345>`

- 'null' is entered as the character `Ø` to create the token `<null>`. Internally null is translated into the token `<value ''>`, which will be interpreted as a stack mark, empty string, 0, or empty list as required.

- 'number' consists of any of the following patterns, which are converted into a value token containing an integer value
    - `0`
    - a string of digits starting with a non-zero value eg. `123`
    - a string of digits starting with a non-zero value and preceded by `~` eg. `~99` which will be read as a negative number
    - one of the number shortcut symbols (see below) when not followed by a string literal character

- 'newline' consists of the sequence '\`nl' which will translate to the token `<value "\n">`, it can be used in strings and file output when a newline character is required.

- 'string literal' consists of a sequence of one or more characters in a-zA-Z. They are translated into value tokens containing a string. Other characters can be included by prefixing them with a back-tick escape character eg. 'Hello\` World\`!', which produces the token `<value "Hello World!">`.

- 'block end' specifies the end point of a lambda or iteration block and is one of the symbols `)` or `;`. By convention `)` is used to end lambda blocks and `;` to end iteration blocks. It produces the token `<end block>`

- 'symbol' any unicode character not recognised by one of the patterns above is considered a single character operator. These are translated into the symbol tokens eg. `<symbol '!'>`

Comments are patterns that are preceded by any number of '\t' or `⍝` characters and last until the next '\n' character. These are included in the metadata for the token immediately preceding the comment.


For example, for the following program
```fb1337
ḣ:					for i in range(1, 101):
Fizz‿Buzz				{Fizz, Buzz} list of strings to select from
3‿5_|					{i divides 3?, i divides 5?} boolean selector list
⊃						pick elements of string list based on whether 1/True in selector list
'						turn the resulting list of 0 or more strings into a single string
_∨						if string is '' then i else string
```

The following tokens are produced
```
('value', 100, {'comments': '', 'token_code': 'ḣ', 'code location': (0, 1)})
('symbol', ':', {'comments': 'for i in range(1, 101):', 'token_code': ':', 'code location': (1, 2)})
('value', 'Fizz', {'comments': '', 'token_code': 'Fizz', 'code location': (2, 6)})
('symbol', '‿', {'comments': '', 'token_code': '‿', 'code location': (6, 7)})
('value', 'Buzz', {'comments': '{Fizz, Buzz} list of strings to select from', 'token_code': 'Buzz',
    'code location': (7, 11)})
('value', 3, {'comments': '', 'token_code': '3', 'code location': (11, 12)})
('symbol', '‿', {'comments': '', 'token_code': '‿', 'code location': (12, 13)})
('value', 5, {'comments': '', 'token_code': '5', 'code location': (13, 14)})
('symbol', '_', {'comments': '', 'token_code': '_', 'code location': (14, 15)})
('symbol', '|', {'comments': '{i divides 3?, i divides 5?} boolean selector list', 'token_code': '|',
    'code location': (15, 16)})
('symbol', '⊃', {'comments': 'pick elements of string list based on whether 1/True in selector list', 'token_code': '⊃',
    'code location': (16, 17)})
('symbol', "'", {'comments': 'turn the resulting list of 0 or more strings into a single string', 'token_code': "'",
    'code location': (17, 18)})
('symbol', '_', {'comments': '', 'token_code': '_', 'code location': (18, 19)})
('symbol', '∨', {'comments': "if string is '' then i else string", 'token_code': '∨', 'code location': (19, 20)})
```

## Shortcut Symbols

The following shortcut symbols are currently defined. All of these produce integer values.

| Symbol | Meaning  | Token                   |
|--------|----------|-------------------------|
| ṫ      | ten      | `<value 10>`            |
| ḟ      | F        | `<value 15>`            |
| Ḷ      | fifty    | `<value 50>`            |
| Ḟ      | FF       | `<value 255>`           |
| ḣ      | hundred  | `<value 100>`           |
| ḳ      | thousand | `<value 1000>`          |
| Ḳ      | kilo     | `<value 1024>`          |
| ṁ      | million  | `<value 1_000_000>`     |
| ḃ      | billion  | `<value 1_000_000_000>` |
