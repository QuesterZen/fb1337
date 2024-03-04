# FBl337
# Programming Code Golf Language
# Created: 21 February 2024
# Version: 21 February 2024 12:00PM
# Copyright: James Leibert 2024
# Licence: Available for use under the GPL3 Licence https://www.gnu.org/licenses/gpl-3.0.txt

# FizzPrimes.py
# FB1337 code golf examples.


import sys

sys.setrecursionlimit(10000)

from fb1337 import run, run_annotated, run_interactive

# Code Golf Program Challenges

# Fizz Buzz
# Print the numbers from 1 to 100, but whenever the number is divisible by 3 replace with Fizz and when divisible by 5 Buzz
# If a number is divisible by both, then replace it with FizzBuzz
fizzbuzz_commented = """
ḣ:				for i in range(1, 101):
_‰3?FizzØ			'Fizz' if (i % 3 == 0) else ''
_‰5?BuzzØ			'Buzz' if (i % 5 == 0) else ''
⊕					concatenate strings
_∨					if string is '' then i else string
"""

fizzbuzz_title = "FizzBuzz"
fizzbuzz_name = 'fizzbuzz'
fizzbuzz_parameters = []
fizzbuzz_output = [1, 2, 'Fizz', 4, 'Buzz', 'Fizz', 7, 8, 'Fizz', 'Buzz', 11, 'Fizz', 13, 14, 'FizzBuzz', 16, 17,
                   'Fizz', 19, 'Buzz', 'Fizz', 22, 23, 'Fizz', 'Buzz', 26, 'Fizz', 28, 29, 'FizzBuzz', 31, 32, 'Fizz',
                   34, 'Buzz', 'Fizz', 37, 38, 'Fizz', 'Buzz', 41, 'Fizz', 43, 44, 'FizzBuzz', 46, 47, 'Fizz', 49,
                   'Buzz', 'Fizz', 52, 53, 'Fizz', 'Buzz', 56, 'Fizz', 58, 59, 'FizzBuzz', 61, 62, 'Fizz', 64, 'Buzz',
                   'Fizz', 67, 68, 'Fizz', 'Buzz', 71, 'Fizz', 73, 74, 'FizzBuzz', 76, 77, 'Fizz', 79, 'Buzz', 'Fizz',
                   82, 83, 'Fizz', 'Buzz', 86, 'Fizz', 88, 89, 'FizzBuzz', 91, 92, 'Fizz', 94, 'Buzz', 'Fizz', 97, 98,
                   'Fizz', 'Buzz']

# Fizz Buzz in 20 characters
golfbuzz_commented = """
ḣ:					for i in range(1, 101):
Fizz‿Buzz				{Fizz, Buzz} list of strings to select from
3‿5_|					{i divides 3?, i divides 5?} boolean selector list
⊃						pick elements of string list based on whether 1/True in selector list
'						turn the resulting list of 0 or more strings into a single string
_∨						if string is '' then i else string
"""

golfbuzz_title = "CodeGolf FizzBuzz"
golfbuzz_name = 'golfbuzz'
golfbuzz_parameters = []
golfbuzz_output = [1, 2, 'Fizz', 4, 'Buzz', 'Fizz', 7, 8, 'Fizz', 'Buzz', 11, 'Fizz', 13, 14, 'FizzBuzz', 16, 17,
                   'Fizz', 19, 'Buzz', 'Fizz', 22, 23, 'Fizz', 'Buzz', 26, 'Fizz', 28, 29, 'FizzBuzz', 31, 32, 'Fizz',
                   34, 'Buzz', 'Fizz', 37, 38, 'Fizz', 'Buzz', 41, 'Fizz', 43, 44, 'FizzBuzz', 46, 47, 'Fizz', 49,
                   'Buzz', 'Fizz', 52, 53, 'Fizz', 'Buzz', 56, 'Fizz', 58, 59, 'FizzBuzz', 61, 62, 'Fizz', 64, 'Buzz',
                   'Fizz', 67, 68, 'Fizz', 'Buzz', 71, 'Fizz', 73, 74, 'FizzBuzz', 76, 77, 'Fizz', 79, 'Buzz', 'Fizz',
                   82, 83, 'Fizz', 'Buzz', 86, 'Fizz', 88, 89, 'FizzBuzz', 91, 92, 'Fizz', 94, 'Buzz', 'Fizz', 97, 98,
                   'Fizz', 'Buzz']

# Fizz Buzz with Point-Free Combinators (27 characters)
combuzz_commented = """
ḣ:_				for i in range(1, 101):
𝔰∨					or x, f(x):
𝚽⊕					concatenate g(x), h(x):           
µ‰3?FizzØ)			'Fizz' if (i % 3 == 0) else ''
µ‰5?BuzzØ)			'Buzz' if (i % 5 == 0) else ''
"""

combuzz_title = "Combinator FizzBuzz"
combuzz_name = 'combuzz'
combuzz_parameters = []
combuzz_output = [1, 2, 'Fizz', 4, 'Buzz', 'Fizz', 7, 8, 'Fizz', 'Buzz', 11, 'Fizz', 13, 14, 'FizzBuzz', 16, 17, 'Fizz',
                  19, 'Buzz', 'Fizz', 22, 23, 'Fizz', 'Buzz', 26, 'Fizz', 28, 29, 'FizzBuzz', 31, 32, 'Fizz', 34,
                  'Buzz', 'Fizz', 37, 38, 'Fizz', 'Buzz', 41, 'Fizz', 43, 44, 'FizzBuzz', 46, 47, 'Fizz', 49, 'Buzz',
                  'Fizz', 52, 53, 'Fizz', 'Buzz', 56, 'Fizz', 58, 59, 'FizzBuzz', 61, 62, 'Fizz', 64, 'Buzz', 'Fizz',
                  67, 68, 'Fizz', 'Buzz', 71, 'Fizz', 73, 74, 'FizzBuzz', 76, 77, 'Fizz', 79, 'Buzz', 'Fizz', 82, 83,
                  'Fizz', 'Buzz', 86, 'Fizz', 88, 89, 'FizzBuzz', 91, 92, 'Fizz', 94, 'Buzz', 'Fizz', 97, 98, 'Fizz',
                  'Buzz']

# Fizz Buzz with no iteration (29 characters)
arraybuzz_commented = """
ḣ⍳					1..100
𝔰∨						or (reversed arguments)
∘⊸(3‿5)⊚|					outer-product divides 1..100 with [3 5], then
 ⋮							map columns
  ∘⊸(Fizz‿Buzz)⊃				select [Fizz Buzz], then
   '							stringify
"""

arraybuzz_title = "No Iteration FizzBuzz"
arraybuzz_name = 'arraybuzz'
arraybuzz_parameters = []
arraybuzz_output = [1, 2, 'Fizz', 4, 'Buzz', 'Fizz', 7, 8, 'Fizz', 'Buzz', 11, 'Fizz', 13, 14, 'FizzBuzz', 16, 17, 'Fizz',
                  19, 'Buzz', 'Fizz', 22, 23, 'Fizz', 'Buzz', 26, 'Fizz', 28, 29, 'FizzBuzz', 31, 32, 'Fizz', 34,
                  'Buzz', 'Fizz', 37, 38, 'Fizz', 'Buzz', 41, 'Fizz', 43, 44, 'FizzBuzz', 46, 47, 'Fizz', 49, 'Buzz',
                  'Fizz', 52, 53, 'Fizz', 'Buzz', 56, 'Fizz', 58, 59, 'FizzBuzz', 61, 62, 'Fizz', 64, 'Buzz', 'Fizz',
                  67, 68, 'Fizz', 'Buzz', 71, 'Fizz', 73, 74, 'FizzBuzz', 76, 77, 'Fizz', 79, 'Buzz', 'Fizz', 82, 83,
                  'Fizz', 'Buzz', 86, 'Fizz', 88, 89, 'FizzBuzz', 91, 92, 'Fizz', 94, 'Buzz', 'Fizz', 97, 98, 'Fizz',
                  'Buzz']


# The Sieve of Eratosthenes in 25 characters
# Find all primes up to some number n, by eliminating all multiples of smaller primes
eratosthenes_commented = """
Ø‿Ø➊⩔⍳⩓⊕			s = [Ø, Ø] + list(range(2, n+1))
∂:					for i in s:
_➊√>?⌁					if i > sqrt(n): break
@{(_²)Ø_Ø				else: s[i*i::i] = ''
"""

eratosthenes_title = "The Sieve of Eratosthenes"
eratosthenes_name = "eratosthenes"
eratosthenes_parameters = [50]
eratosthenes_output = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47]


# The Sieve of Eratosthenes in 22 characters
# Find all primes up to some number n, by eliminating all multiples of smaller primes
# Uses a filter instead of iteration.

eratos_filter_commented = """
2➊⍳↓1				i = 2; s = list(range(2, n+1)) 
⍣µ					repeat:
}⟜⫣%					s.filter(x -> not i divides x)
∂⍮⬇)					stack.append(i); i = s[0]; s = s[1:]
µ⨩➊√>)				until: i > isqrt(n)
☆					stack += s
"""

eratos_filter_title = "The Sieve of Eratosthenes"
eratos_filter_name = "eratosthenes"
eratos_filter_parameters = [50]
eratos_filter_output = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47]


# Iverson Primes in 9 characters
# Less efficient, but more concise way to find the primes by removing multiples
# Less efficient because all nxn products are calculated explictly and removed individually
# The concision comes from using whole-of-array functions, rather than having to create loops and slices
# The program is also point-free (ignoring the initial parameter)

iverson_commented = """
➊
⍳↓1				    list 2..n
𝒮					Apply S combinator to the following functions so xSfg -> f(x, g(x))
⟈						f = remove these values from the original list
𝒲⊚×					    g = use outer-product multiply to create a list of all products: 2..n x 2..n
"""

iverson_title = "Iverson Array Primes"
iverson_name = "iverson"
iverson_parameters = [50]
iverson_output = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47]


# Built-in Primes 2 characters
built_in_primes_commented = """
➊𝜋					Use built-in function for fast prime generation using numpy
"""

built_in_primes_title = "Built-in Primes"
built_in_primes_name = 'built-in'
built_in_primes_parameters = [50]
built_in_primes_output = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47]


# HOW TO RUN CODE

# 1. Run raw code
result = run(name=fizzbuzz_name, commented_code=fizzbuzz_commented, parameters=fizzbuzz_parameters)
print(result)
result = run(name=golfbuzz_name, commented_code=golfbuzz_commented, parameters=golfbuzz_parameters)
print(result)
result = run(name=combuzz_name, commented_code=combuzz_commented, parameters=combuzz_parameters)
print(result)
result = run(name=arraybuzz_name, commented_code=arraybuzz_commented, parameters=arraybuzz_parameters)
print(result)
result = run(name=eratosthenes_name, commented_code=eratosthenes_commented, parameters=eratosthenes_parameters)
print(result)
result = run(name=eratos_filter_name, commented_code=eratos_filter_commented, parameters=eratos_filter_parameters)
print(result)
result = run(name=iverson_name, commented_code=iverson_commented, parameters=iverson_parameters)
print(result)
result = run(name=built_in_primes_name, commented_code=built_in_primes_commented, parameters=built_in_primes_parameters)
print(result)
print()

# 2. Run with extra information
run_annotated(title=golfbuzz_title, name=golfbuzz_name, commented_code=golfbuzz_commented,
              parameters=golfbuzz_parameters, expected=golfbuzz_output)


# 3. Run in interactive_mode with code comments
# run_interactive(name=fizzbuzz_name, commented_code=fizzbuzz_commented, parameters=fizzbuzz_parameters)
