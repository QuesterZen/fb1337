# FBl337
# Programming Code Golf Language
# Created: 21 February 2024
# Version: 21 February 2024 12:00PM
# Copyright: James Leibert 2024
# Licence: Available for use under the GPL3 Licence https://www.gnu.org/licenses/gpl-3.0.txt

# tests.py
# Test programs


import sys

from fb1337 import test, interactive_from_test_suite

sys.setrecursionlimit(10000)

tests = [
    # Basic Program Operation
    {'name': 'hello world', 'code': "Hello` World`!", 'parameters': [], 'result': "Hello World!"},
    {'name': 'context', 'code': "x; 3,3+", 'parameters': [], 'result': ['x', 6]},
    {'name': 'parameters', 'code': "$1$2+$3", 'parameters': [1, 2, 3], 'result': [3, 3]},
    {'name': 'interpret params', 'code': "1$1+ $2:_+; $3+ $4", 'parameters': ["1", [5, 10], '', False],
     'result': [17, 0]},
    {'name': 'return list', 'code': "3⍳@1Ø", 'parameters': [], 'result': [1, 3]},

    # Maths Functions
    {'name': 'simple math', 'code': "3,4,5++~10+,~6-2÷2×", 'parameters': [], 'result': 8},
    {'name': 'special math', 'code': "125,4%²36√×3÷4*", 'parameters': [], 'result': 16},
    {'name': 'comparisons', 'code': "3,3=3,2≠+ 4,3⌈+ 5,6≤+ 0¬1¬++ 3,5∧2∨+", 'parameters': [], 'result': 13},
    {'name': 'max', 'code': "$1$2⌈;$2$1⌈", 'parameters': [29, 31], 'result': [31, 31]},
    {'name': 'gcd', 'code': "84,105⨸", 'parameters': [], 'result': 21},

    # Control flow
    {'name': 'parens', 'code': "3(4,5+)× (3,4+)5×", 'parameters': [], 'result': [27, 35]},
    {'name': 'if divisible', 'code': "5‰3?1,0 6‰3?2,5+", 'parameters': [], 'result': 2},
    {'name': 'query', 'code': "1?µ3)4;0?µ3)4", 'parameters': [], 'result': [3, 4]},
    {'name': 'query id', 'code': "1⍳:1?_⊢;2⍳:0?_⊢;3⍳:_‰2?_⊢", 'parameters': [], 'result': [1, 2]},
    {'name': 'order', 'code': "µð>?µ⊢)µ«))→a945,285$a⏎;285,945$a⏎", 'parameters': [], 'result': [945, 285, 945, 285]},
    {'name': 'case 1', 'code': "₡1,1₡0,2₡0,3€4", 'parameters': [], 'result': 1},
    {'name': 'case 2', 'code': "₡0,1₡1,2₡1,3€4", 'parameters': [], 'result': 2},
    {'name': 'case 3', 'code': "₡0,1₡0,2₡1,3€4", 'parameters': [], 'result': 3},
    {'name': 'case 4', 'code': "₡0,1₡0,2₡0,3€4", 'parameters': [], 'result': 4},
    {'name': 'case fn', 'code': "4₡µ∂2<)µ1)₡µ∂4<)µ2)₡µ∂6<)µ3)€µ4)⍮◌", 'parameters': [], 'result': 3},

    # Basic Loops and iteration
    {'name': 'loop up', 'code': "3:_", 'parameters': [], 'result': [1, 2, 3]},
    {'name': 'loop down', 'code': "~3:_", 'parameters': [], 'result': [3, 2, 1]},
    {'name': 'count down', 'code': "$1:_;$1~:_", 'parameters': [3], 'result': [1, 2, 3, 3, 2, 1]},
    {'name': 'add loop', 'code': "0,5:_+", 'parameters': [], 'result': 15},
    {'name': 'oddfact', 'code': "1$1:_2×1-×", 'parameters': [5], 'result': 945},
    {'name': 'double loop', 'code': "3:_3:∂_×«;◌", 'parameters': [], 'result': [1, 2, 3, 2, 4, 6, 3, 6, 9]},
    {'name': 'double named', 'code': "5:_→a,5:_→b,($a$b+)", 'parameters': [],
     'result': [2, 3, 4, 5, 6, 3, 4, 5, 6, 7, 4, 5, 6, 7, 8, 5, 6, 7, 8, 9, 6, 7, 8, 9, 10]},
    {'name': 'str loop', 'code': "hello:_; $1:_", 'parameters': ["help"],
     'result': ['h', 'e', 'l', 'l', 'o', 'h', 'e', 'l', 'p']},
    {'name': 'list loop', 'code': "Ø3,1,4,1,5,9⏍:_;3⍳:_", 'parameters': [], 'result': [3, 1, 4, 1, 5, 9, 1, 2, 3]},
    {'name': 'slice.py loop', 'code': "{3,11,2:_", 'parameters': [], 'result': [3, 5, 7, 9]},

    # For Loops
    {'name': 'basic for', 'code': "Ω2,9,3:_2×1+", 'parameters': [], 'result': [5, 11, 17]},
    {'name': 'lambda for', 'code': "Ωµ2)λ9≤)λ3+):_2×1+", 'parameters': [], 'result': [5, 11, 17]},
    {'name': 'double for', 'code': "ØΩ16,18,1:◌_Ω19,21,1:∂_×«;;◌", 'parameters': [], 'result': [304, 320, 323, 340]},
    {'name': 'gcd', 'code': "945,285Ω1λ0≠)µ∂®«%∂):;◌", 'parameters': [], 'result': 15},

    # Power Loop / Repeat
    {'name': 'repeat loops', 'code': "5,3…µ2×) 5⍣µ2×)µ∂40=)", 'parameters': [], 'result': [40, 40]},

    # Lists, Slices and List Iteration
    {'name': 'list', 'code': "3⍳:_", 'parameters': [], 'result': [1, 2, 3]},
    {'name': 'pair', 'code': "1‿2‿3‿4‿5:_", 'parameters': [], 'result': [1, 2, 3, 4, 5]},
    {'name': 'pair with list', 'code': "2‿(3⍳)‿(3⍳)‿2", 'parameters': [], 'result': [2, 1, 2, 3, 1, 2, 3, 2]},
    {'name': 'slice.py', 'code': "9⍳[2Ø3:_2×1+", 'parameters': [], 'result': [7, 13, 19]},
    {'name': 'extend list', 'code': "1⍳$1∂+:∂0⁔0®⁔+;$1⊇", 'parameters': [20], 'result': 137846528820},
    {'name': 'stack list', 'code': "3,4,0Ø1,2,3,4⏍:_+", 'parameters': [], 'result': [3, 4, 10]},
    {'name': 'list length', 'code': "1,2,3,4⏍↓1#", 'parameters': [], 'result': 3},
    {'name': 'list join', 'code': "3⍳Ø4,5,6⏍⊕", 'parameters': [], 'result': [1, 2, 3, 4, 5, 6]},
    {'name': 'char lists', 'code': "123ⁿ bobⁿ ⊕", 'parameters': [], 'result': [1, 2, 3, 98, 111, 98]},
    {'name': 'roll list', 'code': "3⍳↦ 3⍳↤⊕", 'parameters': [], 'result': [0, 1, 2, 2, 3, 0]},
    {'name': 'include exclude', 'code': "5⍳Ø4,2,4⏍⟈ Ø4,2,4⏍3⍳∩ ⊕", 'parameters': [], 'result': [1, 3, 5, 2]},
    {'name': 'take drop', 'code': "5⍳ ↑4 ↓2", 'parameters': [], 'result': [3, 4]},
    {'name': 'copies', 'code': "5,3⧉ hi2⧉ ⊕", 'parameters': [], 'result': [5, 5, 5, 'hi', 'hi']},
    {'name': 'set slice.py', 'code': "Ø3,1,4,1,5,9⏍@{2,4Ø9", 'parameters': [], 'result': [3, 1, 9, 9, 5, 9]},
    {'name': 'slice.py alt', 'code': "Ø3,1,4,1,5,9⏍[1Ø2", 'parameters': [], 'result': [1, 1, 9]},
    {'name': 'at location', 'code': "Ø3,1,4,1,5,9⏍∂2⊇«5⊇", 'parameters': [], 'result': [4, 9]},
    {'name': 'set', 'code': "Ø3,1,4,1,5,9⏍@2,1@{4,6Ø1", 'parameters': [], 'result': [3, 1, 1, 1, 1, 1]},
    {'name': 'set list', 'code': "$1√→a$1⍳∂→s@0Ø$a«:_", 'parameters': [10], 'result': [3, 2, 3, 4, 5, 6, 7, 8, 9, 10]},
    {'name': 'outer product', 'code': "Ø1,2,3⏍Ø3,4,5⏍⊚×▭", 'parameters': [], 'result': [3, 4, 5, 6, 8, 10, 9, 12, 15]},
    {'name': 'list binary 1', 'code': "Ø1,2,3,4⏍Ø4,1,7,~8⏍⌈", 'parameters': [], 'result': [4, 2, 7, 4]},
    {'name': 'list binary 2', 'code': "Ø1,2,3,4⏍Ø4,1,7,~8⏍µ⌈)⏎", 'parameters': [], 'result': [4, 2, 7, 4]},
    {'name': 'list binary 3', 'code': "Ø1,2,3,4⏍Ø4,1,7,~8⏍µ×)⏎", 'parameters': [], 'result': [4, 2, 21, -32]},
    {'name': 'list binary 4', 'code': "Ø1,2,3,4⏍Ø4,1,7,~8⏍µ²-)⏎", 'parameters': [], 'result': [-15, 1, -46, -60]},
    {'name': 'implicit binary', 'code': "3⍳∂⎅¨!×; 3⍳∂⎅¨!«µ²-)⏎+", 'parameters': [], 'result': [11, 2, -5]},
    {'name': 'implicit map 1', 'code': "Ø1,2,3,4⏍²", 'parameters': [], 'result': [1, 4, 9, 16]},
    {'name': 'implicit map 2', 'code': "Ø1,2,3,4⏍!", 'parameters': [], 'result': [1, 2, 6, 24]},
    {'name': 'implicit map 3', 'code': "Ø1,2,3,4⏍µ!)⏎", 'parameters': [], 'result': [1, 2, 6, 24]},
    {'name': 'implicit map 4', 'code': "3,4Ø1,2,3,4⏍!:_", 'parameters': [], 'result': [3, 4, 1, 2, 6, 24]},
    {'name': 'list set ops', 'code': "1‿2‿3,2‿3‿4∩1‿2‿3,2‿3‿4∪⊕3‿3‿2‿2‿3‿1ṵ⊕", 'parameters': [],
     'result': [2, 3, 1, 2, 3, 4, 3, 2, 1]},
    {'name': 'sort', 'code': "5‿2‿3‿1‿4‿0↗∂↘⊕", 'parameters': [], 'result': [0, 1, 2, 3, 4, 5, 5, 4, 3, 2, 1, 0]},
    {'name': 'grade', 'code': "5‿3‿2‿6‿0‿1∂⍋«⍒⊕", 'parameters': [], 'result': [4, 5, 2, 1, 0, 3, 3, 0, 1, 2, 5, 4]},
    {'name': 'select bool', 'code': "5‿3‿2‿6‿0‿1,0‿0‿1‿1‿0‿1⊃:_;Hello0‿0‿1‿1‿0⊃", 'parameters': [],
     'result': [2, 6, 1, 'll']},
    {'name': 'select index', 'code': "5‿3‿2‿6‿0‿1∂3⊇«2‿3⊇Hellopr«⊇", 'parameters': [], 'result': [6, 'lr']},
    {'name': 'dictionary select', 'code': "Δa@1,2@2,3@3,4@4,5,2‿3‿4⊇", 'parameters': [], 'result': [3, 4, 5]},
    {'name': 'group', 'code': "5‿3‿2‿6‿0‿1,0‿1‿0‿1‿0‿2⊆", 'parameters': [], 'result': [[5, 2, 0], [3, 6], [1]]},
    {'name': 'group str', 'code': "splunk0‿1‿0‿1‿0‿2⊆", 'parameters': [], 'result': ['sln', 'pu', 'k']},
    {'name': 'member', 'code': "3,5‿3‿2‿6‿0‿1∈9,5‿3‿2‿6‿0‿1∈5‿7‿3‿2,5‿3‿2‿6‿0‿1∈:_", 'parameters': [],
     'result': [1, 0, 1, 0, 1, 1]},
    {'name': 'member str', 'code': "vera,severality∈, very,severality∈", 'parameters': [], 'result': [1, 0]},
    {'name': 'find all', 'code': "5‿3‿2‿6‿0‿1→a $a6⋸ $a9⋸ $a2‿1‿7⋸:_; hello,elx⋸:_", 'parameters': [],
     'result': [3, 2, 5, 1, 2, 3]},
    {'name': 'find all?', 'code': "5‿3‿2‿6→a $a6∊:_; $a9∊:_; $a2‿1‿7∊:_; hello,elx∊:_;", 'parameters': [],
     'result': [0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 1, 1, 0]},
    {'name': 'index conversion', 'code': "2‿6‿3,8⋥:_; 0‿0‿1‿1‿1⊒:_; 0‿0‿1‿1‿1⊐", 'parameters': [],
     'result': [0, 0, 1, 1, 0, 0, 1, 0, 2, 3, 4, 2]},
    {'name': 'window', 'code': "5‿3‿2‿6‿0‿2‿6‿3⧈3+", 'parameters': [],
     'result': [10, 11, 8, 8, 8, 11]},
    {'name': 'window 2', 'code': "1‿2‿3,4‿5‿6⁔7‿8‿9⁔⧈2+", 'parameters': [],
     'result': [[12, 16], [24, 28]]},
    {'name': 'window 3', 'code': "1,2,3,2,3,4,3,4,5⌸3,3⍴⧈3+9÷", 'parameters': [],
     'result': 3.},
    {'name': 'stencil', 'code': "5‿3‿2‿6‿0‿2‿6‿3⌺3+", 'parameters': [],
     'result': [8, 10, 11, 8, 8, 8, 11, 9]},
    {'name': 'stencil 2', 'code': "1‿2‿3,4‿5‿6⁔7‿8‿9⁔⌺2+", 'parameters': [],
     'result': [[12, 16, 9], [24, 28, 15], [15, 17, 9]]},
    {'name': 'stencil 3', 'code': "1,2,3,2,3,4,3,4,5⌸3,3⍴⌺3+", 'parameters': [],
     'result': [[8, 15, 12], [15, 27, 21], [12, 21, 16]]},
    {'name': 'array size', 'code': "1‿2‿3‿4,4‿5‿6‿7⁔7‿8‿9‿10⁔#", 'parameters': [], 'result': 3},
    {'name': 'array flatten', 'code': "1‿2‿3‿4,4‿5‿6‿7⁔7‿8‿9‿10⁔▭", 'parameters': [],
     'result': [1, 2, 3, 4, 4, 5, 6, 7, 7, 8, 9, 10]},
    {'name': 'array join', 'code': "1‿2,3‿4⁔7‿8,9‿10⁔⊕▭", 'parameters': [], 'result': [1, 2, 7, 8, 3, 4, 9, 10]},
    {'name': 'array set', 'code': "1‿2,3‿4⁔7‿8⁔9‿10⁔ⓐ(0‿0,1‿0⁔0‿1⁔1‿1⁔)9▭", 'parameters': [],
     'result': [1, 2, 9, 4, 7, 9, 9, 9]},
    {'name': 'array set fns', 'code': "1‿2‿3,4‿5‿6⁔▭→a 2‿4‿7→b $a$b∪ $a$b∩ ⊕ $a$b⟈ ⊕", 'parameters': [],
     'result': [1, 2, 3, 4, 5, 6, 7, 2, 4, 1, 3, 5, 6]},
    {'name': 'array bool select', 'code': "1‿2,3‿4⁔∂ 8| ⊃", 'parameters': [], 'result': [1, 2, 4]},
    {'name': 'array return value', 'code': "1‿2,3‿4⁔", 'parameters': [], 'result': [[1, 2], [3, 4]]},
    {'name': 'array implicit map', 'code': "1‿2,3‿4⁔ 2+", 'parameters': [], 'result': [[3, 4], [5, 6]]},
    {'name': 'array implicit binary', 'code': "1‿2,3‿4⁔ 1‿2,3‿4⁔+", 'parameters': [], 'result': [[2, 4], [6, 8]]},
    {'name': 'array return value', 'code': "1‿2,3‿4⁔", 'parameters': [], 'result': [[1, 2], [3, 4]]},
    {'name': 'array size 2', 'code': "1‿2,3‿4⁔#", 'parameters': [], 'result': 2},
    {'name': 'array set 2', 'code': "1‿2,3‿4⁔ ⌘1,1,0", 'parameters': [], 'result': [[1, 2], [3, 0]]},
    {'name': 'array row col', 'code': "1‿2,3‿4⁔∂ 1𝖗« 0𝖈 +", 'parameters': [], 'result': [4, 7]},
    {'name': 'array shape', 'code': "1‿2‿3,3‿4‿5‿6⁔⇑2,4⍴", 'parameters': [], 'result': [[1, 2, 3, 3], [4, 5, 6, 0]]},
    {'name': 'array transpose', 'code': "1‿2‿3,4‿5‿6⁔⦰", 'parameters': [], 'result': [[1, 4], [2, 5], [3, 6]]},
    {'name': 'array reflect', 'code': "1‿2‿3,4‿5‿6⁔ ⎅", 'parameters': [], 'result': [[3, 2, 1], [6, 5, 4]]},
    {'name': 'array flip', 'code': "1‿2‿3,4‿5‿6⁔ ⏛", 'parameters': [], 'result': [[4, 5, 6], [1, 2, 3]]},

    # Additional list functions
    {'name': 'partition str', 'code': "hello1‿0‿1‿1‿0⊂", 'parameters': [],
     'result': ["h", "ll"]},
    {'name': 'partition list', 'code': "5‿8‿2‿1‿0‿2‿6‿3,5‿8‿2‿1‿0‿2‿6‿3,3%⊂", 'parameters': [],
     'result': [[5, 8, 2], [1], [2]]},
    {'name': 'partition harder', 'code': "5‿3‿2,6‿0‿2⁔6‿3‿1⁔,1‿1‿1‿2‿1‿0‿2‿2‿3⊂", 'parameters': [],
     'result': [[5, 3, 2], [6], [0], [6, 3], [1]]},
    {'name': 'classify', 'code': "5‿3‿2‿6‿0‿2‿6‿3∂ṵ«⊏", 'parameters': [],
     'result': [[5, 3, 2, 6, 0], [[0], [1, 7], [2, 5], [3, 6], [4]]]},

    # Inner and outer products
    {'name': 'list inner product', 'code': "1‿2‿3,3‿4‿5•+×", 'parameters': [], 'result': 26},
    {'name': 'list inner different', 'code': "1‿2‿3,5‿4‿2•⌈⌊", 'parameters': [], 'result': 2},
    {'name': 'lol inner product', 'code': "2‿3,2‿3⁔2‿3⁔,1‿2‿1,2‿1‿2⁔•+×", 'parameters': [],
     'result': [[8, 7, 8], [8, 7, 8], [8, 7, 8]]},
    {'name': 'matrix inner product', 'code': "1,2,3,4,5,6⌸2,3⍴→aØ4,3,2⌸3,1⍴→b $a$b•+× $a$b⊠ ≡", 'parameters': [],
     'result': 1},
    {'name': 'list outer product', 'code': "1‿2‿3,3‿4‿5⊚×▭", 'parameters': [],
     'result': [3, 4, 5, 6, 8, 10, 9, 12, 15]},
    {'name': 'lol outer product', 'code': "1‿2,1‿2⁔▭ 1‿2 ⊚×▭", 'parameters': [], 'result': [1, 2, 2, 4, 1, 2, 2, 4]},
    {'name': 'matrix outer product', 'code': "2,2,2𝕄2𝚰+2𝚰⎅⊚-", 'parameters': [],
     'result': [[3, 2, 2, 3], [2, 1, 1, 2], [2, 1, 1, 2], [3, 2, 2, 3]]},

    # Higher Level List Functions
    {'name': 'map', 'code': "3,4Ø1,2,3,4⏍¨!:_", 'parameters': [], 'result': [3, 4, 1, 2, 6, 24]},
    {'name': 'map mu', 'code': "3,4Ø1,2,3,4⏍¨µ⩔!):_", 'parameters': [], 'result': [3, 4, 1, 1, 2, 6]},
    {'name': 'map b-comb', 'code': "1,2,3,4⏍¨∘⩔!", 'parameters': [], 'result': [1, 1, 2, 6]},
    {'name': 'map w-comb', 'code': "1,2,3,4⏍¨𝒲+", 'parameters': [], 'result': [2, 4, 6, 8]},
    {'name': 'map bind', 'code': "1,2,3,4⏍¨⟜2×", 'parameters': [], 'result': [2, 4, 6, 8]},
    {'name': 'filter', 'code': "1,2,3,4⏍}‰2", 'parameters': [], 'result': [2, 4]},
    {'name': 'reduce', 'code': "3,4Ø1,2,3,4⏍/+", 'parameters': [], 'result': [3, 4, 10]},
    {'name': 'reduce mu', 'code': "3,4Ø1,2,3,4⏍/µ×)", 'parameters': [], 'result': [3, 4, 24]},
    {'name': 'reduce comb', 'code': "3,4Ø1,2,3,4⏍/𝚿+⩔", 'parameters': [], 'result': [3, 4, 4]},
    {'name': 'filter reduce', 'code': "10⍳}‰3∂/µ²+)«#÷", 'parameters': [], 'result': 40},
    {'name': 'reduce 2', 'code': "1,2,3,4⏍/µ²+)", 'parameters': [], 'result': 30},
    {'name': 'foldr', 'code': "1,2,3,4⏍⥆µ²+)", 'parameters': [], 'result': 131770},
    {'name': 'scan', 'code': "1,2,3,4⏍∖+", 'parameters': [], 'result': [1, 3, 6, 10]},
    {'name': 'scanr', 'code': "1,2,3,4⏍⥶+", 'parameters': [], 'result': [10, 9, 7, 4]},

    # Matrices
    {'name': 'matrix input', 'code': "➊3𝚰-", 'parameters': [[[1, 2, 3], [4, 5, 6], [7, 8, 9]]],
     'result': [[0, 2, 3], [4, 4, 6], [7, 8, 8]]},
    {'name': 'list - matrix', 'code': "Ø3,1,4,1,5,9,2,6,5⏍⊡3,3⍴Ø1,2,3,4,5,6,7,8,9⌸3,3⍴⊠▭", 'parameters': [],
     'result': [35, 43, 51, 84, 99, 114, 61, 74, 87]},
    {'name': 'matrix reflect', 'code': "3𝚰3𝚰⎅+1+", 'parameters': [], 'result': [[2, 1, 2], [1, 3, 1], [2, 1, 2]]},
    {'name': 'matrix transpose', 'code': "Ø3,1,4,1,5,9,2,6,5⌸3,3⍴Ø1,2,3,4,5,6⌸2,3⍴⎅⦰⊠", 'parameters': [],
     'result': [[15, 39], [22, 67], [23, 62]]},
    {'name': 'matrix implicit', 'code': "Ø3,1,4,1,5,9,2,6,5⌸3,3⍴→s $s4× $s+ 3𝚰×", 'parameters': [],
     'result': [[15, 0, 0], [0, 25, 0], [0, 0, 25]]},
    {'name': 'matrix implicit 2', 'code': "Ø3,1,4,1,5,9,2,6,5⌸3,3⍴→s $sµ4×)⏎ $sµ+)⏎ 3𝚰µ×)⏎", 'parameters': [],
     'result': [[15, 0, 0], [0, 25, 0], [0, 0, 25]]},
    {'name': 'matrix set', 'code': "3𝚰⌘1,2,8", 'parameters': [], 'result': [[1, 0, 0], [0, 1, 8], [0, 0, 1]]},
    {'name': 'matrix roll', 'code': "Ø1,2,3,4,5,6,7,8,9⌸3,3⍴↧▭", 'parameters': [3],
     'result': [0, 0, 0, 1, 2, 3, 4, 5, 6]},
    {'name': 'matrix shifts', 'code': "3𝚰↦3𝚰↤+ 3𝚰↥3𝚰↧- ×", 'parameters': [],
     'result': [[0, 1, 0], [-1, 0, 1], [0, -1, 0]]},
    {'name': 'matrix rotate', 'code': "1‿2‿3,4‿5‿6⁔7‿8‿9⁔→s $s1⏀$s~1⏀+ $s1⦵$s~1⦵- ×", 'parameters': [],
     'result': [[15, 12, 9], [-66, -60, -54], [51, 48, 45]]},
    {'name': 'matrix inverse', 'code': "1,2,0,0,2,1,1,0,1⌸3,3⍴⌹4×", 'parameters': [],
     'result': [[2, -2, 2], [1, 1, -1], [-2, 2, 2]]},
    {'name': 'matrix inverse 2', 'code': "1,2,0,0,2,1,1,0,1⌸3,3⍴∂⌹⊠", 'parameters': [],
     'result': [[1, 0, 0], [0, 1, 0], [0, 0, 1]]},
    {'name': 'matrix determinant', 'code': "1,2,0,0,2,1,1,0,1⌸3,3⍴∂⌹«𝚲×", 'parameters': [],
     'result': [[2, -2, 2], [1, 1, -1], [-2, 2, 2]]},
    {'name': 'matrix equivalent', 'code': "3𝚰3×3𝚰5×↦+∂ Ø3,5,0,0,3,5,0,0,3⌸3,3⍴≡ «3𝚰≡ 3𝚰3𝚰9,1⍴≡", 'parameters': [],
     'result': [1, 0, 0]},
    {'name': 'matrix outer product 2', 'code': "1,2,3⌸Ø2,4,3⌸⊚+", 'parameters': [],
     'result': [[3, 5, 4], [4, 6, 5], [5, 7, 6]]},
    {'name': 'matrix outer product 3', 'code': "1,2,3,4⌸2,2⍴Ø5,7⌸⊚+", 'parameters': [],
     'result': [[6, 8], [7, 9], [8, 10], [9, 11]]},
    {'name': 'to matrix', 'code': "Ø1,2,3,4,5,6⏍⊡Ø3,4,5,6,7,8,9⏍⊡+⊟:_", 'parameters': [],
     'result': [4, 6, 8, 10, 12, 14]},
    {'name': 'reshape', 'code': "Ø1,2,3,4,5,6⌸3,2⍴∂+▭", 'parameters': [], 'result': [2, 4, 6, 8, 10, 12]},
    {'name': 'matrix solve', 'code': "Ø3,5,~7,1,0,3,1,~1,~1⌸3,3⍴→aØ2,4,~3⌸⦰→x$a⌹$x⊠16×", 'parameters': [],
     'result': [4, 32, 20]},
    {'name': 'x-matrix', 'code': "$1∂0≠«#𝚰∂⎅∨≡",
     'parameters': [[[2, 0, 0, 6], [0, 3, -1, 0], [0, -2, 7, 0], [1, 0, 0, 2]]], 'result': 1},
    {'name': 'x-matrix f', 'code': "$1∂0≠«#𝚰∂⎅∨≡", 'parameters': [[[2, 0, 6], [3, 0, 0], [1, 0, 2]]],
     'result': 0},
    {'name': 'x-matrix comb', 'code': "$1𝚽≡µ0≠)µ#𝚰𝒮∨⎅)",
     'parameters': [[[2, 0, 0, 6], [0, 3, -1, 0], [0, -2, 7, 0], [1, 0, 0, 2]]], 'result': 1},
    {'name': 'matrix binary', 'code': "3𝚰3𝚰⎅∨", 'parameters': [], 'result': [[1, 0, 1], [0, 1, 0], [1, 0, 1]]},
    {'name': 'matrix binary 2', 'code': "3𝚰3𝚰⎅µ∨)⏎", 'parameters': [], 'result': [[1, 0, 1], [0, 1, 0], [1, 0, 1]]},
    {'name': 'matrix binary 3', 'code': "2𝚰2𝚰⎅⊚µ∨)", 'parameters': [],
     'result': [[1, 1, 1, 1], [0, 1, 1, 0], [0, 1, 1, 0], [1, 1, 1, 1]]},
    {'name': 'matrix binary 4', 'code': "3𝚰3𝚰⎅⊙µ∨)", 'parameters': [], 'result': [[1, 0, 1], [0, 1, 0], [1, 0, 1]]},
    {'name': 'matrix map', 'code': "3𝚰¨µ1+)", 'parameters': [], 'result': [[2, 1, 1], [1, 2, 1], [1, 1, 2]]},
    {'name': 'matrix select', 'code': "3𝚰∂2𝖗«0𝖈-", 'parameters': [], 'result': [-1, 0, 1]},
    {'name': 'matrix reduction', 'code': "Ø1,2,3,4,5,6⌸2,3⍴∂⍮/+⌿×⊚-", 'parameters': [],
     'result': [[2, -4, -12], [11, 5, -3]]},
    {'name': 'matrix map vector', 'code': "Ø1,2,3,4,5,6⌸2,3⍴∂⋯µ/+)«⋮µ/+)", 'parameters': [],
     'result': [[6, 15], [5, 7, 9]]},

    # Stack manipulation
    {'name': 'duplicate', 'code': "1,2,3⨩-ð×+∂×--", 'parameters': [], 'result': 8},
    {'name': 'drop', 'code': "3:_;◌◌3,4◌5,6◌7", 'parameters': [], 'result': [1, 3, 5, 7]},
    {'name': 'swap', 'code': "⊢1«2«⊢-", 'parameters': [], 'result': 1},
    {'name': 'stack manipulation', 'code': "1,2,3⨩+®+ð+®∂+÷-", 'parameters': [], 'result': 4},
    {'name': 'lcm', 'code': "945,285,15,®®×«÷", 'parameters': [], 'result': 17955},

    # Strings
    {'name': 'palindrome', 'code': "$1'∂⎅=;$2'∂⎅=", 'parameters': [906609, 90608], 'result': [True, False]},
    {'name': 'count', 'code': "`1`2`3⎅ℤ1-", 'parameters': [], 'result': 320},
    {'name': 'join', 'code': "`1`2,`3⊕⎅ℤ1-", 'parameters': [], 'result': 320},
    {'name': 'join strings', 'code': "abc‿def‿ghi→x $x/⊕ $x,`@⊕ $x'", 'parameters': [],
     'result': ["abcdefghi", "abc@def@ghi", "abcdefghi"]},

    # Dictionary
    {'name': 'dictionary', 'code': "Δa@3,5@4,9,3⊇$a4⊇$a5⊇", 'parameters': [], 'result': [5, 9]},

    # Binary
    {'name': 'binary', 'code': "13,4⟘ ¬⊤ `0`1`0`1⊤ ×", 'parameters': [], 'result': 10},

    # Namespaces
    {'name': 'assign', 'code': "6→s12$s÷", 'parameters': [], 'result': 2},
    {'name': 'assign local', 'code': "3→s µ5→s2$s×)⏎ 3$s×", 'parameters': [], 'result': [10, 9]},
    {'name': 'assign late', 'code': "(1,2+)→s2$s$s+-", 'parameters': [], 'result': -4},
    {'name': 'assign long', 'code': "µ10,6-)→birthday $birthday⏎", 'parameters': [], 'result': 4},
    {'name': 'local pin', 'code': "1,2,3,4⇶2 + ⇴2⇴1-× ⇶2 ⑴", 'parameters': [], 'result': 3},

    # Lookups
    {'name': 'num refs', 'code': "Ø2⏍:Ø8⏍:Ø1⏍:Ø8⏍:Ø9⏍:_⓪①②③④⑤;➋➍➌➊➎", 'parameters': [3, 1, 4, 1, 5],
     'result': [9, 9, 8, 1, 8, 2, 1, 1, 4, 3, 5]},
    {'name': 'lookup run', 'code': "µ3×)→x 2£x 4£1", 'parameters': [lambda e: e.pop() * 5], 'result': [6, 20]},

    # Blocks
    {'name': 'block', 'code': "3(4,5+)⍳:_+", 'parameters': [], 'result': 48},
    {'name': 'mu', 'code': "µ3)→s$s⏎$s⏎+", 'parameters': [], 'result': 6},
    {'name': 'lambda', 'code': "03:λ²)⏎+", 'parameters': [], 'result': 14},
    {'name': 'kappa', 'code': "κ2×1+,1«)→a3$a⏎4$a⏎5$a⏎3$a⏎5$a⏎", 'parameters': [],
     'result': [1, 7, 1, 9, 1, 11, 7, 11]},

    # Higher Level Functions
    {'name': 'defer', 'code': "⩣+1,2®⏎", 'parameters': [], 'result': 3},
    {'name': 'bind', 'code': '4⊸3- 4⟜3-', 'parameters': [], 'result': [-1, 1]},
    {'name': 'bind in map 1', 'code': '3⍳¨µ2=)', 'parameters': [], 'result': [0, 1, 0]},
    {'name': 'bind in map 2', 'code': '3⍳¨⊸2=', 'parameters': [], 'result': [0, 1, 0]},
    {'name': 'bind in map 3', 'code': '⩣⊸2=→s 3⍳¨$s', 'parameters': [], 'result': [0, 1, 0]},
    {'name': 'dip', 'code': '3,4⍮²', 'parameters': [], 'result': [9, 4]},
    {'name': 'dip stack', 'code': '3,4⍮∂ ⍮µ3+) « ⍮« ⍮◌', 'parameters': [], 'result': [4, 6]},
    {'name': 'repeat', 'code': "3,4,5,6,3…+ 2,4…² 1,3…µ3×1+)", 'parameters': [], 'result': [18, 65536, 40]},

    # Combinators
    {'name': 'comb i', 'code': '3,4ℐ+ 3,4ℐµ+) ⩣+→a 3,4ℐ$a µ+)→b 3,4ℐ$b', 'parameters': [], 'result': [7, 7, 7, 7]},
    {'name': 'comb k', 'code': '7𝒦1', 'parameters': [], 'result': 1},
    {'name': 'comb w', 'code': '3𝒲+ 3𝒲µ+) ⩣+→a 3𝒲$a', 'parameters': [], 'result': [6, 6, 6]},
    {'name': 'comb c', 'code': '3,4𝒞- 3,4𝒞µ-) ⩣-→a 3,4𝒞$a', 'parameters': [], 'result': [1, 1, 1]},
    {'name': 'comb wi', 'code': '3𝒲ℐ+', 'parameters': [], 'result': 6},
    {'name': 'comb b', 'code': '3,4∘²+ ⩣∘²+→a 3,4$a⏎', 'parameters': [], 'result': [19, 19]},
    {'name': 'comb s s-prime', 'code': '⩣𝒮-µ²)→a ⩣𝔰-µ²)→b 3$a⏎ 3$b⏎', 'parameters': [], 'result': [-6, 6]},
    {'name': 'comb psi', 'code': '4,3𝚿-² ⩣-→a ⩣²→b 4,3𝚿$a$b 4,3𝚿+⊢', 'parameters': [], 'result': [7, 7, 7]},
    {'name': 'comb d', 'code': '3,4𝒟+²√ 3,4𝒟+²⊢ 3,4𝒟+⊢²', 'parameters': [], 'result': [11, 13, 19]},
    {'name': 'comb phi phi-prime', 'code': '4𝚽+²√ 4𝚽-𝒲×𝔰-² 4,3𝛗×+-', 'parameters': [], 'result': [18, 4, 7]},
    {'name': 'combinator defer', 'code': '⩣𝒲×3«⏎', 'parameters': [], 'result': 9},
    {'name': 'combinators', 'code': '⩣+→a µ×1-)→b ⩣²→x µ3×1+)→y 3,4𝛗×$a$b 3∘$x$y 3𝚽+𝒲$b𝔰×$x', 'parameters': [],
     'result': [77, 28, 35]},
    {'name': 'comb lambda', 'code': '3𝒲+ 3𝒲µ+) ⩣+→a 3𝒲$a', 'parameters': [], 'result': [6, 6, 6]},

    # Complex Example Programs
    {'name': 'FizzBuzz long', 'code': "$1:_‰3?FizzØ_‰5?BuzzØ⊕_∨", 'parameters': [10],
     'result': [1, 2, 'Fizz', 4, 'Buzz', 'Fizz', 7, 8, 'Fizz', 'Buzz']},
    {'name': 'FizzBuzz short', 'code': "$1:Fizz‿Buzz3‿5_|⊃'_∨", 'parameters': [10],
     'result': [1, 2, 'Fizz', 4, 'Buzz', 'Fizz', 7, 8, 'Fizz', 'Buzz']},
    {'name': 'Eratosthenes Fast', 'code': "Ø‿Ø➊⩔⍳⩓⊕∂:_➊√>?⌁@{(_²)Ø_Ø", 'parameters': [30],
     'result': [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]},
    {'name': 'Eratosthenes Short', 'code': "2➊⍳↓1⍣µ}⟜⫣%∂⍮⬇)µ⨩➊√>)☆", 'parameters': [30],
     'result': [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]},
    {'name': 'Iverson Primes', 'code': "$1⍳↓1𝒮⟈𝒲⊚×", 'parameters': [30],
     'result': [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]},
    {'name': 'Wilson Primes', 'code': "$1⍳∂∂⩔!~«%1=⊃", 'parameters': [30],
     'result': [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]},
    {'name': 'Wilson Primes Comb', 'code': "$1⍳↓1 𝒮⊃𝔰‱∘⩔∘!⩓", 'parameters': [30],
     'result': [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]},
    {'name': 'pascal matrix', 'code': "$1$1,0𝕄⌘0,0,1∂$1,2×µ∂1=?◌µ«∂↧«↦+∂®1-$s⏎+))→s$s⏎ +▭:◌_", 'parameters': [21],
     'result': 137846528820},
    {'name': 'combuzz', 'code': "ḟ:_𝔰∨𝚽⊕µ‰3?FizzØ)µ‰5?BuzzØ)", 'parameters': [],
     'result': [1, 2, 'Fizz', 4, 'Buzz', 'Fizz', 7, 8, 'Fizz', 'Buzz', 11, 'Fizz', 13, 14, 'FizzBuzz']},
    {'name': 'triangle divisors', 'code': "0Ω1µ$1<)1:_+→a$a⍳}µ$a«‱)#$a«", 'parameters': [12], 'result': 120},

    {'name': 'loadtest', 'code': "1⨋2⨋3⨋∫ℤ∫ℤ∫ℤ", 'parameters': [], 'result': [1, 2, 3]},
    {'name': 'loadlist', 'code': "~3⍳:_⨋;7⨋9⨋;∮", 'parameters': [], 'result': [3, 2, 1, 7, 9]},
    {'name': 'loadarray', 'code': "`1` `2` `3⨋`4` `5` `6⨋`7` `8` `9⨋⨖", 'parameters': [],
     'result': [[1, 2, 3], [4, 5, 6], [7, 8, 9]]},
]

if __name__ == "__main__":
    debug_single_test = None
    if debug_single_test is not None and debug_single_test in [t['name'] for t in tests]:
        interactive_from_test_suite(tests, debug_single_test)
    else:
        test(tests, verbose=True, path=__file__)
