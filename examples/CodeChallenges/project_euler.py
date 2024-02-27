# FBl337
# Programming Code Golf Language
# Created: 21 February 2024
# Version: 21 February 2024 12:00PM
# Copyright: James Leibert 2024
# Licence: Available for use under the GPL3 Licence https://www.gnu.org/licenses/gpl-3.0.txt

# ProjectEuler.py
# FB1337 solutions for challenges from Project Euler


import sys

from fb1337 import test, interactive_from_test_suite

sys.setrecursionlimit(10000000)

# Project Euler Code Challenges

# 1. Find the sum of all the multiples of 3 or 5 below 1000 [233168]
# 2. Find the sum of the even Fibonacci numbers not exceeding 4000000 [4613732]
# 3. Find the largest prime factor of 600851475143 [6857]
# 4. Find the largest palindromic number that is the product of two 3-digit numbers [906609]
# 5. Find the least common multiple of the numbers from 1 to 20 [232792560]
# 6. Find the difference between the square of the sums and the sum of the squares for the first 100 natural numbers [25164150]
# 7. Find the 10001st prime number [104743]
# 8. Find the 13 adjacent digits in the following 1000-digit number which have the greatest product. 
#    What is their product? [23514624000]
# 	 See below for the 1000 digit number
# 9. Find the pythagorean triple a^2 + b^2 = c^2 such that a + b + c = 1000. Find the product abc. [31875000]
# 10. Find the sum of the primes below 2 million [142913828922]
# 11. Find the greatest product of 4 numbers in a row in any direction (u, d, l, r, diagonally), in a 20x20 grid [70600674]
# see euler 11.in
# 12. What is the first triangle number with more than 500 divisors? [76576500]
# 13. First 10 digits of the sum of 100 50-digit numbers" [5537376230]
# see euler 13.in
# 14. Which start number under 1000000 leads to the longest Collatz chain? (x even -> x/2; x odd -> 3x+1 ... -> 1) [837799]
# 15. How many down-right routes are there from the top-left to bottom-right of a 20x20 grid? [137846528820]
# 16. Find the sum of the digits of 2^1000 [1366]
# 17. How many letters in total in the word form of the numbers from 1 to 1000 inclusive [21124]
# 18. Find the route down through the grid (moving down or left) that has the highest sum of points traversed [1074]
# 19. Given that 1/1/1900 was a Monday how many Sundays fell on the first of the month in the twentieth century? Note that leap years are every four years, except centuries that are not multiples of 400. []
# 20. Find the sum of the digits in 100! [648]


project_euler_solutions = [
	{'name': 'euler 1', 'code': "➊⍳}𝚽∨‰3‰5/+", 'parameters': [999], 'result': 233168},
	{'name': 'euler 2', 'code': "1Ω1λ➊≤)µð+):_;⏍}‰2/+", 'parameters': [4000001], 'result': 4613732},
	{'name': 'euler 3', 'code': "➊Ω2λ⨩<)µ∂‰_?λ÷_)λ⩓)):;", 'parameters': [600851475143], 'result': 6857},
	# Euler 4 is very slow
	{'name': 'euler 5', 'code': "µ∂0=?◌𝛗$g⍮◌%)→g $1⍳/𝛗÷×$g", 'parameters': [20], 'result': 232792560},
	{'name': 'euler 6', 'code': "➊⍳/+²➊⍳²/+-", 'parameters': [100], 'result': 25164150},
	{'name': 'euler 7', 'code': "➊∂⊛×→s $s√→v $s⍳∂@0ØΩ2λ$v≤)µ∂⪼◇):@{(_²)$s_Ø;◌}⊢ ➊⩔⊇", 'parameters': [10001],
	 'result': 104743},
	{'name': 'euler 8', 'code': "∫→n $nⁿ#➊-:$nⁿ[_(_➊+)1/×;⏍/⌈", 'parameters': [12], 'result': 23514624000},
	{'name': 'euler 9', 'code': "➊2÷√:_: Ø①²⓪²-,2①⓪××,①²⓪²+⏍∂ /+ḳ=?µ/×)µ◌)", 'parameters': [1000], 'result': 31875000},
	{'name': 'euler 10', 'code': "➊⍳∂@0Ø Ω2λ➊√≤)µ∂⪼◇): @{(_²)➊_Ø; ◌/+", 'parameters': [2000000],
	 'result': 142913828922},
	{'name': 'euler 11', 'code': "⨖∂0×⊜∂0×⊕⊟→v ➊²2×: Ø1➊2×∂∂⍮⩓⩔⏍: $v[①(①_3×+)_ /×;; ⏍/⌈", 'parameters': [20],
	 'result': 70600674},
	# Euler 12 is very slow
	{'name': 'euler 13', 'code': "∮/+ⁿ↑ṫ'ℤ", 'parameters': [], 'result': 5537376230},
	# Euler 14 is very slow
	{'name': 'euler 15', 'code': "1➊⩓⧉➊…∖+➊⊇", 'parameters': [20], 'result': 137846528820},
	{'name': 'euler 15a', 'code': "➊𝔰‼⟜2×", 'parameters': [20], 'result': 137846528820},
	{'name': 'euler 16', 'code': "2ḳ*ⁿ/+", 'parameters': [], 'result': 1366},
	{'name': 'euler 17',
	 'code': "0,3,3,5,4,4,3,5,5,4⏍→ones 3,6,6,8,8,7,7,9,8,8⏍→teens 0,3,6,6,5,5,5,7,6,6⏍→tens"
	         "999:"
	         "_99>?µ$ones _100÷⊇ 7+ _‰100?0,3+)0 +"
	         "_100%20<?µ_20%10<? µ$ones_10%⊇)"
	         "µ$teens_20%10-⊇))"
	         "µ$tens_100%10÷⊇ $ones_10%⊇+)+;"
	         "11+",
	 'parameters': [], 'result': 21124},
	{'name': 'euler 18', 'code': "1⌸➊➊⍴⏛⎅ ⨖ ➊:ð⊠ ∂↤⌈↥+ ⍮↥⍮↤; ⍮◌ ⊟0⊇", 'parameters': [15], 'result': 1074},
	{'name': 'euler 19', 'code': "31,28,31,30,31,30,31,31,30,31,30,31⏍→M"
	                             "λ⩔‰48?⩓⊢)→L"
	                             "0,2 Ω12,1212,1:"
	                             "∂‰7?⍮⩓⊢ $L⏎ $M_12%⊇+;"
	                             "◌",
	 'parameters': [], 'result': 171},
	{'name': 'euler 20', 'code': "ḣ!ⁿ/+", 'parameters': [], 'result': 648},

]

project_euler_slow = [
	{'name': 'euler 4', 'code': "➊ḣ-⍳ḣ+ ∂⊚× ▭}µ∂'⎅=)/⌈", 'parameters': [999], 'result': 906609},
	{'name': 'euler 7 short', 'code': "Ωµ➊∂⊛×⍳↓1)λ#)λ}λ◇‱¬)):_◇;⏍➊⩔⊇", 'parameters': [10001], 'result': 104743},
	{'name': 'euler 9 short', 'code': "ḳ:_:ḳ⓪-①-∂²⓪²-①²-?◌µ⓪①××)", 'parameters': [], 'result': 31875000},
	{'name': 'euler 12',
	 'code': "µ ₡µ∂$M>) µ◌◌×2×)"
	         "  ₡µð<)   µ◌◌×)"
	         "  ₡µð‱)   µ⍮⍮⩓∂⍮÷$P⏎)"
	         "  €       µ⍮⍮×1®®⩓$P⏎)"
	         ")→P"
	         "0,0Ω1µ➊≤)1:_+→T $T2×√√⩓→M"
	         "$T 1,1$T2$P⏎",
	 'parameters': [500], 'result': 76576500},
	{'name': 'euler 14',
	 'code': "κ ₡µ∂1=)  µ◌0)"
	         "  ₡µ∂‰2)  µ2÷$C⏎⩓)"
	         "  €       µ3×1+$C⏎⩓)"
	         ")→C"
	         "0,0➊:_$C⏎"
	         "ð<?µ⍮◌⍮◌_«)◌;"
	         "◌",
	 'parameters': [1000000], 'result': 837799},

]

if __name__ == "__main__":
	debug_single_test = None
	include_slow = False
	if debug_single_test is not None and debug_single_test in [t['name'] for t in project_euler_solutions]:
		interactive_from_test_suite(project_euler_solutions, debug_single_test)
	elif debug_single_test is not None and debug_single_test in [t['name'] for t in project_euler_slow]:
		interactive_from_test_suite(project_euler_slow, debug_single_test)
	else:
		test(project_euler_solutions, verbose=True, path=__file__)
		if include_slow:
			test(project_euler_slow, verbose=True, path=__file__)
