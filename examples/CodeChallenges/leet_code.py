# FBl337
# Programming Code Golf Language
# Created: 21 February 2024
# Version: 21 February 2024 12:00PM
# Copyright: James Leibert 2024
# Licence: Available for use under the GPL3 Licence https://www.gnu.org/licenses/gpl-3.0.txt

# LeetCode.py
# FB1337 solutions for challenges from LeetCode


import sys

from fb1337 import test, interactive_from_test_suite

sys.setrecursionlimit(10000000)

# Code Challenges Challenges
# Taken from code_report channel on youtube; playlist Leetcode
# Series of https://leetcode.com challenges solved in APL/J/BQN/Uiua
# See https://www.youtube.com/playlist?list=PLVFrD1dmDdvd_rChH0L1jeMVZpJ8ZIivE

# 1. Sum the squares of the values in a list whose index divides the length of the list
# 2. Is the given matrix an x-matrix ie. has non-zero values on the diagonals and zeros elsewhere
# 3. Given a list of words and a string, does the string comprise the initial characters of the words in order (ie is it an acronym)
# 4. Given a list of integers, what is the greatest number of positive values in its partial sums for all permutations of the values
# 5. Given a list of integers, create a list consisting of the abs(sum of items to the left - sum of items to right)
# 6. Given a sorted (non-decreasing) array return the maximum between the number of positive and number of negative integers
# 7. Given a grid of 1s and 0s, create a new grid whose i,jth entry is #1s in ith row - #0s in ith row +  #1s in ith col - #0s in ith col
# 8. Given an integer array, move all the even integers to the start of the array, followed by the odd integers
# 9. Given an unsorted integer array, return the smallest positive integer (1, 2...) not in the list; must run in o(n) time and o(1) space
# 10. Given a list containing '++x', 'x++', 'x--' and '--x' commands, find the final value of x when it starts at 0
# 11. Find the greatest common divisor of the maximum and minimum values in a list
# 12. Find the longest common prefix of a list of strings
# 13. Given an index permutation (0-based) use it to permute the permutation list ie. res[i] = num[num[i]]
# 14. Given a list of words, can the letters be re-arranged into the same number of identical words?
# 15. What is the sign of the product of a list of numbers: 1 if positive, -1 if negative, 0 if 0
# 16. Find the maximum nesting depth of parentheses in an expression
# 17. Truncate a sentence (sequence of alpha character words separated by spaces) to return only the first n words
# 18. After replacing all non-numeric characters in a string with spaces, how many unique integers (separated by spaces) are left?
# 19. Given a grid of values, find the maximum row sum
# 20. Count the number of negative values in an ordered grid
# 21. Given an array of integers, how many of them have an even number of digits
# 22. Find all words that follow a given pair of words eg. for "have you" , "how HAVE YOU been today" will return "been"
# 23. Given a permutation, find the largest permutation (dictionary order) less than the original you can obtain with a single swap
# 24. Given a list of values, count how many are not in the correct order
# 25. Remove the outer parentheses on every first level group of parentheses
# 26. In a 2D binary array there are two 'islands' of 1s connected NSEW. Find the fewest 0s to flip to connect the islands.
# 27. Find the minimum sum of values in a grid that take one value from each row, so that each value's column differs by at most 1 from the one above.
# 28. How many ways are there to write N as a sum of consecutive positive integers
# 29. Given a list of 'bus routes' (connected clusters), what is the fewest number of routes (not stops) we need to take to go from S to D?
# 30. Split a list of values into two lists with equal average
# 31. How many characters in string 2 are in string 1?
# 32. Start with 0 on row 1. On the next row replace 0 -> 01 and 1->10. What symbol is at kth column of row n?
# 33. Given a 3x2 sliding number puzzle, either find the shortest solution or return -1
# 34. In a non-decreasing list of numbers count the negative values and the number of positive values and take the maximum
# 35. Given a Binary Search Tree and a target value; split the tree into a tree with values <= and values > preserving the tree structure
# 36. Find how many equivalence classes of strings there are: a~b if the even characters are permutations and the odd characters are permutations
# 37. Given a directed graph, how many nodes have all possible exit paths leading to a terminal node
# 38. Given a list of integers, count the number of contiguous subarrays whose maximum is between L and R inclusive.
# 39. Given points on a number line, add k extra points to minimise the maximum distance between two points. Find this new minimum.
# 40. Given an array, find the path from top left to bottom right with the smallest maximum grid value
# 41. Given a list of coprime numbers, find the kth smallest fraction a/b where a, b are distinct values on the list
# 42. How many tilings of a 2xN board are there using domino (I covering 2 squares) and triomino (L covering 3 squares)?
# 43. What is the fewest number of same-position swaps to make two lists both strictly increasing?

leet_code_solutions = [
	{'name': 'challenge 1.1', 'code': "➊𝚽⊃¨²∘#𝔰|⍳/+", 'parameters': [[2, 7, 1, 19, 18, 3]], 'result': 63},
	{'name': 'challenge 1.2', 'code': "➊𝚽⊃¨²∘#𝔰|⍳/+", 'parameters': [[1, 2, 3, 4]], 'result': 21},
	{'name': 'challenge 2.1', 'code': "➊∂#𝚰∂⎅∨«0≠≡",
	 'parameters': [[[2, 0, 0, 1], [0, 3, 1, 0], [0, 5, 2, 0], [4, 0, 0, 2]]], 'result': 1},
	{'name': 'challenge 2.2', 'code': "➊∂#𝚰∂⎅∨«0≠≡", 'parameters': [[[5, 7, 0], [0, 3, 1], [0, 5, 0]]], 'result': 0},
	{'name': 'challenge 3.1', 'code': "➋➊¨⇤'=", 'parameters': [['alice', 'bob', 'charlie'], 'abc'], 'result': 1},
	{'name': 'challenge 3.2', 'code': "➋➊¨⇤'=", 'parameters': [['an', 'apple'], 'a'], 'result': 0},
	{'name': 'challenge 4.1', 'code': "➊↘∖+0>/+", 'parameters': [[2, -1, 0, 1, -3, 3, -3]], 'result': 6},
	{'name': 'challenge 4.2', 'code': "➊↘∖+0>/+", 'parameters': [[0, -3, -2]], 'result': 0},
	{'name': 'challenge 5.1', 'code': "➊∂∖+↦«⥶+↤-⩲", 'parameters': [[10, 4, 8, 3]], 'result': [15, 1, 11, 22]},
	{'name': 'challenge 5.2', 'code': "➊∂∖+↦«⥶+↤-⩲", 'parameters': [[1]], 'result': 0},
	{'name': 'challenge 6.1', 'code': "➊0𝛗𝚿⌈/+><", 'parameters': [[-2, -1, -1, 1, 2, 3]], 'result': 3},
	{'name': 'challenge 6.2', 'code': "➊0𝛗𝚿⌈/+><", 'parameters': [[-3, -2, -1, 0, 0, 1, 2]], 'result': 3},
	{'name': 'challenge 6.3', 'code': "➊0𝛗𝚿⌈/+><", 'parameters': [[5, 20, 66, 1314]], 'result': 4},
	{'name': 'challenge 7.1', 'code': "➊2×⩔𝚽⊚+/+⌿+", 'parameters': [[[0, 1, 1], [1, 0, 1], [0, 0, 1]]],
	 'result': [[0, 0, 4], [0, 0, 4], [-2, -2, 2]]},
	{'name': 'challenge 7a.1', 'code': "➊𝒮𝚿-𝚽⊚+/+⌿+¬", 'parameters': [[[0, 1, 1], [1, 0, 1], [0, 0, 1]]],
	 'result': [[0, 0, 4], [0, 0, 4], [-2, -2, 2]]},
	{'name': 'challenge 8.1', 'code': "➊∂}‰2𝒮⊕⟈", 'parameters': [[3, 1, 2, 4]], 'result': [2, 4, 1, 3]},
	{'name': 'challenge 8a.1', 'code': "➊∂}‰2∂®«⟈⊕", 'parameters': [[3, 1, 2, 4]], 'result': [2, 4, 1, 3]},
	{'name': 'challenge 8b.1', 'code': "➊𝒮𝛗⊕⊃∘¬⊃‰2", 'parameters': [[3, 1, 2, 4]], 'result': [2, 4, 3, 1]},
	{'name': 'challenge 8.2', 'code': "➊∂}‰2𝒮⊕𝒞⟈", 'parameters': [[0]], 'result': 0},
	{'name': 'challenge 9.1', 'code': "➊∂/⌈⩓⍳«⟈/⌊", 'parameters': [[3, 7, 1, 4, 6, 2]], 'result': 5},
	{'name': 'challenge 9.2', 'code': "➊∂/⌈⩓⍳«⟈/⌊", 'parameters': [[1, 2, 0]], 'result': 3},
	{'name': 'challenge 9.3', 'code': "➊∂/⌈⩓⍳«⟈/⌊", 'parameters': [[3, 4, -1, 1]], 'result': 2},
	{'name': 'challenge 9.4', 'code': "➊∂/⌈⩓⍳«⟈/⌊", 'parameters': [[7, 8, 9, 11, 12]], 'result': 1},
	{'name': 'challenge 10.1', 'code': "➊0«:_1⊇`+=?⩓⩔", 'parameters': [['--X', 'X--', 'X++']], 'result': -1},
	{'name': 'challenge 10a.1', 'code': "➊`+`-⊚𝒞∈/+⌿-", 'parameters': [['--X', 'X--', 'X++']], 'result': -1},
	{'name': 'challenge 10b.1', 'code': "➊¨∘⊸`-∈⊸~1*/+", 'parameters': [['--X', 'X--', 'X++']], 'result': -1},
	{'name': 'challenge 10.2', 'code': "0➊:_1⊇`+=?⩓⩔",
	 'parameters': [
		 ['X++', '--X', '++X', '++X', 'X--', 'X++', '--X', '++X', '++X', '--X', 'X++', '--X', '++X', '++X', '--X',
		  'X--', 'X++', '++X', '--X', ]],
	 'result': 3},
	{'name': 'challenge 10.2', 'code': "0➊:_1⊇`+=?⩓⩔", 'parameters': [[]], 'result': 0},
	{'name': 'challenge 11.1', 'code': "➊𝚽⨸/⌊/⌈", 'parameters': [[36, 156, 84, 24, 132, 36]], 'result': 12},
	{'name': 'challenge 11a.1', 'code': "µ∂0=?◌𝛗$g⍮◌%)→g ➊∂/⌊«/⌈$g⏎", 'parameters': [[36, 156, 84, 24, 132, 36]],
	 'result': 12},
	{'name': 'challenge 11.2', 'code': "➊𝚽⨸/⌊/⌈", 'parameters': [[134, 7]], 'result': 1},
	{'name': 'challenge 11.3', 'code': "➊𝚽⨸/⌊/⌈", 'parameters': [[3]], 'result': 3},
	{'name': 'challenge 11.4', 'code': "➊𝚽⨸/⌊/⌈", 'parameters': [[2, 5, 6, 8, 10]], 'result': 2},
	{'name': 'challenge 11.5', 'code': "➊𝚽⨸/⌊/⌈", 'parameters': [[7, 5, 6, 8, 3]], 'result': 1},
	{'name': 'challenge 11.6', 'code': "➊𝚽⨸/⌊/⌈", 'parameters': [[3, 3]], 'result': 3},
	{'name': 'challenge 12.1', 'code': "➊/𝒮∘∖∧⊃𝚿=ⁿ", 'parameters': [["flow", "flower", "flight"]], 'result': "fl"},
	{'name': 'challenge 12.2', 'code': "➊/𝒮∘∖∧⊃𝚿=ⁿ", 'parameters': [["castle", "cattle", "cart"]], 'result': "ca"},
	{'name': 'challenge 12.3', 'code': "➊/𝒮∘∖∧⊃𝚿=ⁿ", 'parameters': [["dog", "racecar", "car"]], 'result': None},
	{'name': 'challenge 12.4', 'code': "➊/𝒮∘∖∧⊃𝚿=ⁿ", 'parameters': [["indigo"]], 'result': "indigo"},
	{'name': 'challenge 13.1', 'code': "➊𝒲⊇", 'parameters': [[0, 2, 1, 5, 3, 4]], 'result': [0, 1, 2, 4, 5, 3]},
	{'name': 'challenge 13.2', 'code': "➊𝒲⊇", 'parameters': [[5, 0, 1, 2, 3, 4]], 'result': [4, 5, 0, 1, 2, 3]},
	{'name': 'challenge 14.1', 'code': "➊∂ /⊕ⁿ↗ ⇑«#∂⍴ 𝒮=⟜1⏀ ⥸∧", 'parameters': [['abc', 'aabc', 'bc']],
	 'result': True},
	{'name': 'challenge 14.2', 'code': "➊∂ /⊕ⁿ↗ ⇑«#∂⍴ 𝒮=⟜1⏀ ⥸∧", 'parameters': [['abc', 'babc', 'bc']],
	 'result': False},
	{'name': 'challenge 14.3', 'code': "➊∂ /⊕ⁿ↗ ⇑«#∂⍴ 𝒮=⟜1⏀ ⥸∧", 'parameters': [['abc', 'babc', 'b']],
	 'result': False},
	{'name': 'challenge 14.4', 'code': "➊∂ /⊕ⁿ↗ ⇑«#∂⍴ 𝒮=⟜1⏀ ⥸∧", 'parameters': [['abc', 'abc', 'bc']],
	 'result': False},
	{'name': 'challenge 15.1', 'code': "➊±/×", 'parameters': [[-1, -2, -3, -4, 3, 2, 1]], 'result': 1},
	{'name': 'challenge 15.2', 'code': "➊±/×", 'parameters': [[1, 5, 0, 2, -3]], 'result': 0},
	{'name': 'challenge 15.3', 'code': "➊±/×", 'parameters': [[-1, 1, -1, 1, -1]], 'result': -1},
	{'name': 'challenge 15.4', 'code': "➊±/×", 'parameters': [[-17]], 'result': -1},
	{'name': 'challenge 16.1', 'code': "➊`(`)⊚=⇑/-∖+/⌈", 'parameters': ["(1+(2×3)+((8)/4))+1"], 'result': 3},
	{'name': 'challenge 16a.1', 'code': "➊ⁿ∂40=«41=-∖+/⌈", 'parameters': ["(1+(2*3)+((8)/4))+1"], 'result': 3},
	{'name': 'challenge 16c.1', 'code': "➊`(`)∩ⁿ~2×81+∖+/⌈", 'parameters': ["(1+(2*3)+((8)/4))+1"], 'result': 3},
	{'name': 'challenge 16.2', 'code': "➊ⁿ∂40=«41=-∖+/⌈", 'parameters': [""], 'result': 0},
	{'name': 'challenge 16a.2', 'code': "➊`(`)⊚=/-∖+/⌈", 'parameters': [" "], 'result': 0},
	{'name': 'challenge 17.1', 'code': "➊` ⤲↑➋` ∪", 'parameters': ["What is the solution to this problem", 4],
	 'result': "What is the solution"},
	{'name': 'challenge 17a.1', 'code': "➊∂¨⟜` =∖+➋<⊃", 'parameters': ["What is the solution to this problem", 4],
	 'result': "What is the solution"},
	{'name': 'challenge 17.2', 'code': "➊` ⤲↑➋` ∪", 'parameters': ["Hello how are you Contestant", 4],
	 'result': "Hello how are you"},
	{'name': 'challenge 18.1', 'code': "➊ⁿ∂47>×∂58<× 0⤲⋯∘¦ℤ ṵ", 'parameters': ["a123bc34d8ef034"],
	 'result': [8, 34, 123]},
	{'name': 'challenge 19.1', 'code': "➊/+⌿⌈", 'parameters': [[[1, 2, 3], [5, 5, 5], [3, 1, 4]]],
	 'result': 15},
	{'name': 'challenge 20.1', 'code': "➊0<⥸+", 'parameters': [[[-2, -1, 0], [-1, 1, 3], [-1, 2, 4]]],
	 'result': 4},
	{'name': 'challenge 21.1', 'code': "➊:_'#‰2+", 'parameters': [[12, 345, 2, 6, 7896]],
	 'result': 2},
	{'name': 'challenge 21a.1', 'code': "➊¨∘'#}‰2#", 'parameters': [[12, 345, 2, 6, 7896]],
	 'result': 2},
	{'name': 'challenge 22.1', 'code': "➊` ⤲∂↦∂↦¨⊸➋=⍮¨⊸➌=×⊃",
	 'parameters': ["alice is a good girl she is a good student", "a", "good"], 'result': ["girl", "student"]},
	{'name': 'challenge 22a.1', 'code': "➊` ⤲𝒮⊃∘↦𝚽×∘↦¨⊸➋=¨⊸➌=",
	 'parameters': ["alice is a good girl she is a good student", "a", "good"], 'result': ["girl", "student"]},
	{'name': 'challenge 22b.1', 'code': "➊` ⤲∂↦∂↦⏍⦰}µ∂2⊇➋=«1⊇➌=∧)⋯⟜0⊇",
	 'parameters': ["alice is a good girl she is a good student", "a", "good"], 'result': ["girl", "student"]},
	{'name': 'challenge 22.2', 'code': "➊` ⤲∂↦∂↦¨⊸➋=⍮¨⊸➌=×⊃",
	 'parameters': ["we will we will rock you", "we", "will"], 'result': ["we", "rock"]},
	{'name': 'challenge 23.1', 'code':
		"µ∂#⍳×/⌈⩔0⌈)→b➊➊↦<⥶∨↤∂$b⏎∂➊«⊇®¬➊×«<➊➊↦≠×$b⏎ð𝚿⊢µ➊«⊇)⍮®➊@(«⊢)(⊢)@(«⊢)(⊢)",
	 'parameters': [[1, 9, 4, 6, 7]], 'result': [1, 7, 4, 6, 9]},
	{'name': 'challenge 23.2', 'code':
		"µ∂#⍳×/⌈⩔0⌈)→b➊➊↦<⥶∨↤∂$b⏎∂➊«⊇®¬➊×«<➊➊↦≠×$b⏎ð𝚿⊢µ➊«⊇)⍮®➊@(«⊢)(⊢)@(«⊢)(⊢)",
	 'parameters': [[1, 1, 5]], 'result': [1, 1, 5]},
	{'name': 'challenge 23.3', 'code':
		"µ∂#⍳×/⌈⩔0⌈)→b"  # finds the index of the rightmost 1 in a mask
		"➊➊↦<⥶∨↤"  # creates a mask where the rightmost non-descending value is the rightmost 1
		"∂$b⏎∂➊«⊇"  # get the index and the target value at that index
		"®¬➊×«<➊➊↦≠×$b⏎"  # get the last value less than our target value after removing duplicates
		"ð𝚿⊢µ➊«⊇)⍮®➊@(«⊢)(⊢)@(«⊢)(⊢)",  # swap the values at these indices
	 'parameters': [[3, 2, 1]], 'result': [3, 1, 2]},
	{'name': 'challenge 23.4', 'code':
		"µ∂#⍳×/⌈⩔0⌈)→b➊➊↦<⥶∨↤∂$b⏎∂➊«⊇®¬➊×«<➊➊↦≠×$b⏎ð𝚿⊢µ➊«⊇)⍮®➊@(«⊢)(⊢)@(«⊢)(⊢)",
	 'parameters': [[3, 1, 1, 3]], 'result': [1, 3, 1, 3]},
	{'name': 'challenge 24.1', 'code': "➊∂↗=/+", 'parameters': [[1, 1, 4, 2, 1, 3]], 'result': 3},
	{'name': 'challenge 25.1', 'code': "➊ⁿ∂∂ 𝚽-⟜40=⟜41=∖+ 𝛗∨𝒟∧⟜40=⟜1=𝒟∧⟜41=⟜0= ¬⊃¦",
	 'parameters': ["(())(()())((())())"], 'result': "()()()(())()"},
	{'name': 'challenge 25a.1', 'code': "➊ⁿ∂ 40=2×1- ∖+ḣ×+ 41⤲⋯∘↓1∘⟜ḣ%¦'", 'parameters': ["(())(()())((())())"],
	 'result': "()()()(())()"},
	{'name': 'challenge 25.2', 'code': "➊ⁿ∂∂ 𝚽-⟜40=⟜41=∖+ 𝛗∨𝒟∧⟜40=⟜1=𝒟∧⟜41=⟜0= ¬⊃¦",
	 'parameters': ["(()())(())"], 'result': "()()()"},
	{'name': 'challenge 25.3', 'code': "➊ⁿ∂∂ 𝚽-⟜40=⟜41=∖+ 𝛗∨𝒟∧⟜40=⟜1=𝒟∧⟜41=⟜0= ¬⊃¦",
	 'parameters': ["(()())(())(()(()))"], 'result': "()()()()(())"},
	{'name': 'challenge 25.4', 'code': "➊ⁿ∂∂ 𝚽-⟜40=⟜41=∖+ 𝛗∨𝒟∧⟜40=⟜1=𝒟∧⟜41=⟜0= ¬⊃¦",
	 'parameters': ["()()"], 'result': None},
	{'name': 'challenge 26.1', 'code': "➊∂⍮⊒ ⊐Ø«⏍ ⍣µ∂➊⋥∂↦⨩↤∨⨩↥∨⨩↧∨∨⊒⍮⨩∩)µ«⨩≡) «⨩⟈ ⊚µ-⩲/+)1-⥸⌊",
	 'parameters': [[[0, 1], [1, 0]]],
	 'result': 1},
	{'name': 'challenge 26.2', 'code': "➊∂⍮⊒ ⊐Ø«⏍ ⍣µ∂➊⋥∂↦⨩↤∨⨩↥∨⨩↧∨∨⊒⍮⨩∩)µ«⨩≡) «⨩⟈ ⊚µ⍮ɨɨ-⩲/+)1-⥸⌊",
	 'parameters': [[[0, 1, 0], [0, 0, 0], [0, 0, 1]]],
	 'result': 2},
	{'name': 'challenge 26.3', 'code': "➊∂⍮⊒ ⊐Ø«⏍ ⍣µ∂➊⋥∂↦⨩↤∨⨩↥∨⨩↧∨∨⊒⍮⨩∩)µ«⨩≡) «⨩⟈ ⊚µ⍮ɨɨ-⩲/+)1-⥸⌊",
	 'parameters': [[[1, 1, 1, 1, 1], [1, 0, 0, 0, 1], [1, 0, 1, 0, 1], [1, 0, 0, 0, 1], [1, 1, 1, 1, 1]]],
	 'result': 1},
	{'name': 'challenge 26.4', 'code': "➊∂⍮⊒ ⊐Ø«⏍ ⍣µ∂➊⋥∂↦⨩↤∨⨩↥∨⨩↧∨∨⊒⍮⨩∩)µ«⨩≡) «⨩⟈ ⊚µ⍮ɨɨ-⩲/+)1-⥸⌊",
	 'parameters': [[[0, 0, 0, 0, 0], [0, 1, 1, 1, 0], [0, 0, 0, 0, 0], [1, 0, 0, 0, 0], [1, 1, 1, 0, 0]]],
	 'result': 2},
	{'name': 'challenge 27.1', 'code': "➊⦰⥆µḳ-∂∂↦⍮↤⌊⌊ḳ++)/⌊",
	 'parameters': [[[1, 2, 3], [4, 5, 6], [7, 8, 9]]],
	 'result': 12},
	{'name': 'challenge 27.2', 'code': "➊⦰⥆µḳ-∂∂↦⍮↤⌊⌊ḳ++)/⌊",
	 'parameters': [[[1, 2, 3, 4], [4, -1, 3, -2], [-2, 5, -3, 2], [7, -6, 9, 8]]],
	 'result': -9},
	{'name': 'challenge 28.1', 'code': "➊2×√⍳}µ𝚽|⟜2×µ∂⩔×~➊2×+))#",
	 'parameters': [5],
	 'result': 2},
	{'name': 'challenge 28.2', 'code': "➊2×√⍳}µ𝚽|⟜2×µ∂⩔×~➊2×+))#",
	 'parameters': [9],
	 'result': 3},
	{'name': 'challenge 28.3', 'code': "➊2×√⍳}µ𝚽|⟜2×µ∂⩔×~➊2×+))#",
	 'parameters': [15],
	 'result': 4},
	{'name': 'challenge 28.4', 'code': "➊2×√⍳}µ𝚽|⟜2×µ∂⩔×~➊2×+))#",
	 'parameters': [24],
	 'result': 2},
	{'name': 'challenge 29.1', 'code': "0 ➊∂⊚µ∩#0>)⊡ 0➊#⩔⩔⧉‿1‿0⊡ ⍣µḋ⊠⍮⍮⩓)µ∂➊#⩔⊇) ◌◌⩔",
	 'parameters': [[[0, 1, 2], [0, 3, 4], [2, 5, 6], [4, 7, 6], [0], [7]]],
	 'result': 2},
	{'name': 'challenge 30.1', 'code': "➊/+→s ➊#→n 0 2$n*⩔⩔:➊_$n⟘⊃𝚽=µ#$s×)µ/+$n×)∨∂?⌁⊢",
	 'parameters': [[2, 4, 5, 7, 10, 14]],
	 'result': 1},
	{'name': 'challenge 30.2', 'code': "➊/+→s ➊#→n 0 2$n*⩔⩔:➊_$n⟘⊃𝚽=µ#$s×)µ/+$n×)∨∂?⌁⊢",
	 'parameters': [[2, 3, 3, 4, 5, 5, 49]],
	 'result': 0},
	{'name': 'challenge 31.1', 'code': "➋➊∊/+",
	 'parameters': ["aA", "aAAbbbb"],
	 'result': 3},
	{'name': 'challenge 31.2', 'code': "➋➊∊/+",
	 'parameters': ["z", "ZZ"],
	 'result': 0},
	{'name': 'challenge 32.1', 'code': "0⊟➊⩔:∂¬⁔⦰▭;➋⩔⊇", 'parameters': [4, 5], 'result': 1},
	{'name': 'challenge 32a.1', 'code': "0⊟➊⩔:∂¬⊕;➋⩔⊇", 'parameters': [4, 5], 'result': 1},
	{'name': 'challenge 33.1', 'code':
		("Ø 1‿0‿2‿3‿4‿5¢ 3‿1‿2‿0‿4‿5¢ ⏍\n"
		 "Ø 1‿0‿2‿3‿4‿5¢ 0‿2‿1‿3‿4‿5¢ 0‿4‿2‿3‿1‿5¢ ⏍\n"
		 "Ø 0‿2‿1‿3‿4‿5¢ 0‿1‿5‿3‿4‿2¢ ⏍\n"
		 "Ø 3‿1‿2‿0‿4‿5¢ 0‿1‿2‿4‿3‿5¢ ⏍\n"
		 "Ø 0‿4‿2‿3‿1‿5¢ 0‿1‿2‿4‿3‿5¢ 0‿1‿2‿3‿5‿4¢ ⏍\n"
		 "Ø 0‿1‿5‿3‿4‿2¢ 0‿1‿2‿3‿5‿4¢ ⏍⏍→table   ⍝All valid moves as permutations\n"
		 "\n"
		 "➊¢→start\n"
		 "➋¢→final\n"
		 "$start⊟→unchecked                      ⍝Store of positions yet to test\n"
		 "Δdistance @$start1◌                    ⍝Shortest distance of each position\n"
		 "\n"
		 "⍣ µ\n"
		 "$unchecked⬇\n"
		 "∂ $distance « ⊇ ⩓ «\n"
		 "\n"
		 "∂ 0 ⋸ $table « 𝖗\n"
		 "¨ µ ḋ ⊇\n"
		 "\n"
		 "∂ $distance «⊇\n"
		 "𝚽∨⟜⫤3>⟜Ø= ? µ∂$distance@⊢⫤2◌ $unchecked«⬆) ⊢\n"
		 ")\n"
		 "◌◌◌\n"
		 ")\n"
		 "µ $unchecked # 0 =)\n"
		 "\n"
		 "$distance $final⊇ 0∨ ⩔\n"),
	 'parameters': [(4, 1, 3, 2, 0, 5), (1, 2, 3, 4, 5, 0)], 'result': 5},
	{'name': 'challenge 33.2',
	 'code': "Ø1‿0‿2‿3‿4‿5¢3‿1‿2‿0‿4‿5¢⏍Ø1‿0‿2‿3‿4‿5¢0‿2‿1‿3‿4‿5¢0‿4‿2‿3‿1‿5¢⏍Ø0‿2‿1‿3‿4‿5¢0‿1‿5‿3‿4‿2¢⏍Ø3‿1‿2‿0‿4‿5¢0‿1‿2‿4‿3‿5¢⏍Ø0‿4‿2‿3‿1‿5¢0‿1‿2‿4‿3‿5¢0‿1‿2‿3‿5‿4¢⏍Ø0‿1‿5‿3‿4‿2¢0‿1‿2‿3‿5‿4¢⏍⏍→t➊¢→s$s⊟→uΔd@$s1◌⍣µ$u⬇∂$d«⊇⩓«∂0⋸$t«𝖗¨µḋ⊇∂$d«⊇𝚽∨⟜⫤3>⟜Ø=?µ∂$d@⊢⫤2◌$u«⬆)⊢)◌◌◌)µ$u#0=)$d➋¢⊇0∨⩔",
	 'parameters': [(0, 1, 2, 4, 5, 3), (1, 2, 3, 4, 5, 0)], 'result': 3},
	{'name': 'challenge 34.1', 'code': "➊0𝛗𝚿⌈/+<>", 'parameters': [[-2, -1, -1, 1, 2, 3]], 'result': 3},
	{'name': 'challenge 34.2', 'code': "➊0𝛗𝚿⌈/+<>", 'parameters': [[-3, -2, -1, 0, 0, 1, 2]], 'result': 3},
	{'name': 'challenge 34.3', 'code': "➊0𝛗𝚿⌈/+<>", 'parameters': [[5, 20, 66, 1314]], 'result': 4},
	{'name': 'challenge 35.1', 'code':
		"µ"
		"⇶3 ⑵Ø=⑶Ø=∧ ?"
		"µ ⑴➋> ? µ Ø ⑴ ) µ ⑴ Ø ) )"
		"µ ⑴➋> ? µ ⑵☆ £split ⑴ « ⑶ ☐3 ) µ ⑶☆ £split « ⑴ ⑵ ® ☐3 « ) )"
		")→split"
		"➊☆£split",
	 'parameters': [[4, [2, 1, 3], [6, 5, 7]], 2], 'result': [[2, 1, None], [4, 3, [6, 5, 7]]]},
	{'name': 'challenge 35.2', 'code': "µ⇶3⑵Ø=⑶Ø=∧?µ⑴➋>?µØ⑴)µ⑴Ø))µ⑴➋>?µ⑵☆£s⑴«⑶☐3)µ⑶☆£s«⑴⑵®☐3«)))→s➊☆£s",
	 'parameters': [[5, [4, 1, ''], [9, [8, 7, ''], [12, '', 13]]], 9],
	 'result': [[5, [4, 1, None], [9, [8, 7, None], None]], [12, None, 13]]},
	{'name': 'challenge 36.1', 'code': "➊¨𝚽𝚿⊕↘[0Ø2[1Ø2ṵ#", 'parameters': [['abc', 'cba', 'acb', 'bca', 'cab', 'bac']],
	 'result': 3},
	{'name': 'challenge 37.1', 'code':
		"⏍→safe"
		"➊#⍳1-→unchecked"
		"⏍→checked"
		"⍣"
		"µ $unchecked⬇∂ ➊ 𝒞⊇ ∂#0=?µ◌1)µ$safe ∊ ∂#0=?µ◌0)µ/∧)) ? µ $safe 𝒞⬆◌ ⍣µ$checked⬇$unchecked𝒞⬆◌)µ$checked#0=)) µ$checked𝒞⬆◌))"
		"µ$unchecked#0=)"
		"$safe"
		, 'parameters': [[[1, 2], [2, 3], [5], [0], [5], [], []]],
     'result': [2, 4, 5, 6]},
	{'name': 'challenge 38.1', 'code':
		"➊∂➌≤⊂"
		"➊∂➋<⊂"
		"𝚿-µ⋯µ#∂⩓×2÷)/+)",
	 'parameters': [[9, 4, 5, 6, 2, 3, 9, 5, 6, 3, 2, 5, 3, 1], 5, 8],
	 'result': 33},
	{'name': 'challenge 38.2', 'code':
		"➊∂➌≤⊂➊∂➋<⊂𝚿-µ⋯µ#∂⩓×2÷)/+)",
	 'parameters': [[0, 3, 1, 2, 0, 5, 1, 2], 2, 4], 'result': 14},
	{'name': 'challenge 39.1', 'code':
		"➊↓1➊-⊡"
		"∂∂÷"
		"➋: ð÷ ∂/⌈ ∊ +;"
		"÷/⌈"
		,
     'parameters': [[2, 5, 6, 16], 5], 'result': 2.0},
	{'name': 'challenge 40.1', 'code':
		"0‿0¢→start"
		"➊#→size"
		"$size⩔∂⏍¢→end"
		"$start⊟→unchecked"
		"Δlevel @ $start 0◌"
		"µ 0‿1⊇∂ 0≥ « $size< ∧ /∧)→valid"
		"µ ∂0‿1¢+« ∂0‿~1¢+« ∂1‿0¢+« ~1‿0¢+« ☐4 }$valid )→neighbours"
		"⍣"
		"µ $unchecked⬇ ∂$level«⊇«"
		"£neighbours ¨ µ"
		"ḋ∂ $level«⊇ ⨩ ➊«⊇ ⇶4   ⍝ (1)current level, (2)newloc, (3)newloc best level, (4)newloc grid value\n"
		"⑶Ø= ? µ$level @ ⑵ (⑴⑷⌈) $unchecked⑵⬆◌◌Ø)  ⍝ if not in dict add max of current level and grid level\n"
		"µ ⑴⑶< ? µ$level @ ⑵ (⑴⑷⌈) $unchecked⑵⬆◌◌) µ) Ø) ⍝ otherwise only update if better\n"
		"    )  ⍝ neighbour map\n"
		"◌◌◌)   ⍝ repeat (one unchecked value) \n"
		"µ $unchecked # 0=) ⍝ until no more unchecked values\n"
		"$level $end ⊇"
		,
     'parameters': [[[0, 2, 2, 5], [3, 2, 4, 1], [1, 2, 1, 0], [2, 2, 4, 0]]], 'result': 2},
	{'name': 'challenge 40.2', 'code':
		"0‿0¢→start"
		"➊#→size"
		"$size⩔∂⏍¢→end"
		"$start⊟→unchecked"
		"Δlevel @ $start 0◌"
		"µ 0‿1⊇∂ 0≥ « $size< ∧ /∧)→valid"
		"µ ∂0‿1¢+« ∂0‿~1¢+« ∂1‿0¢+« ~1‿0¢+« ☐4 }$valid )→neighbours"
		"⍣"
		"µ $unchecked⬇ ∂$level«⊇«"
		"£neighbours ¨ µ"
		"ḋ∂ $level«⊇ ⨩ ➊«⊇ ⇶4   ⍝ (1)current level, (2)newloc, (3)newloc best level, (4)newloc grid value\n"
		"⑶Ø= ? µ$level @ ⑵ (⑴⑷⌈) $unchecked⑵⬆◌◌Ø)  ⍝ if not in dict add max of current level and grid level\n"
		"µ ⑴⑶< ⑶⑷> ∧? µ$level @ ⑵ (⑴⑷⌈) $unchecked⑵⬆◌◌) µ) Ø) ⍝ otherwise only update if better\n"
		"    )  ⍝ neighbour map\n"
		"◌◌◌)   ⍝ repeat (one unchecked value) \n"
		"µ $unchecked # 0=) ⍝ until no more unchecked values\n"
		"$level $end ⊇"
		,
     'parameters': [
	     [[0, 1, 2, 3, 4], [99, 99, 99, 99, 5], [12, 13, 14, 15, 16], [11, 99, 99, 99, 99], [10, 9, 8, 7, 0]]],
     'result': 16},
	{'name': 'challenge 41.1', 'code':
		"µ➊⎅0⊇ ➊¨µḋ⊢‿⊢¢)⍮◌)→build                              ⍝ build the initial coordinate list ()->list\n"
		"µ⇶1 ⑴0⊇ ⑴↓1)→pop                                      ⍝ pop the first value off the list (list)->val,list\n"
		"µ⇶1 ⑴☆ ➊«⋸⩔➊«⊇ ☐2¢)→gen                               ⍝ generate the next fraction (frac)->frac\n"
		"µ⇶2 ⑴0⊇⑵1⊇× ⑴1⊇⑵0⊇× <)→lt                            ⍝ frac1 < frac2 (frac1, frac2)->bool\n"
		"µ⇶2 ⑴∂#→l 1‿~1 0$l⍴ ⑵⩔…↦ $l⍳1-+ ⊇)→swap               ⍝ swap adjacent values (list, 2nd pos)->list\n"
		"µ⇶2 ⑴⑵⁔ ⑴#⩔~: ∂∂_⊇« _⩔⊇ £lt ? µ_£swap) ⌁;)→insert    ⍝ insert a value into an ordered list (list, frac)->list\n"
		"0 £build ➋: ⍮◌ £pop ḋ« £gen £insert; ◌",
	 'parameters': [[1, 3, 7, 11, 31], 4], 'result': [1, 7]},
	{'name': 'challenge 42.1', 'code': "1 1 2 ➊2-: ®⨩∂++; «◌«◌ ḃ7+%"
		, 'parameters': [100], 'result': 190242381},
	{'name': 'challenge 43.1', 'code':
		"➊#→n ➊⧈2< ➋⧈2< ∧¬$n× ➊➋↓1< ➋➊↓1< ∧¬$n× 0 1"
		"$n⩔: ⇶4 ⑴↓1  ⑵↓1  ⑶⑴0⊇+⑷⑵0⊇+⌊ ⑷⑴0⊇+⑶⑵0⊇+⌊⩓;"
		"⇶4 ⑶⑷⌊"
		, 'parameters': [[1, 3, 5, 4], [1, 2, 3, 7]], 'result': 1},
	{'name': 'challenge 43.2', 'code':
		"➊#→n ➊⧈2< ➋⧈2< ∧¬$n× ➊➋↓1< ➋➊↓1< ∧¬$n× 0 1  ⍝ A no swap ok; B swap ok; min swaps with last same; last swapped\n"
		"$n⩔: ⇶4 ⑴↓1  ⑵↓1  ⑶⑴0⊇+⑷⑵0⊇+⌊ ⑷⑴0⊇+⑶⑵0⊇+⌊⩓; ⍝ Pick best option allowed for unswapped, swapped ith items\n"
		"⇶4 ⑶⑷⌊"
		, 'parameters': [[1, 3, 3, 5, 6, 9, 9], [2, 2, 4, 5, 7, 8, 10]], 'result': 2},
	{'name': 'challenge 43a.2', 'code':
		"0 1 ➊#→n ➊⧈2< ➋⧈2< ∧¬$n× ➊➋↓1< ➋➊↓1< ∧¬$n× ⁔⦰: _☆⇶4 ⑴⑶+⑵⑷+⌊ ⑵⑶+⑴⑷+⌊⩓; ⌊"
		, 'parameters': [[1, 3, 3, 5, 6, 9, 9], [2, 2, 4, 5, 7, 8, 10]], 'result': 2},
]

if __name__ == "__main__":
	debug_single_test = None
	if debug_single_test is not None and debug_single_test in [t['name'] for t in leet_code_solutions]:
		interactive_from_test_suite(leet_code_solutions, debug_single_test)
	else:
		test(leet_code_solutions, verbose=True, path=__file__)
