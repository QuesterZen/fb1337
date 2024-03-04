# The Story Behind fb1337

## Origin story

The project was initially conceived in response to a simple question my son asked me. What is the shortest possible implementation of FizzBuzz?

Python has a reputation as quite a terse language, and after a few attempts I eventually produced the following Python one-liner consisting of 66 characters, making use of a few minor Python quirks.

```python
for i in range(1, 101):print('Fizz'*(i%3==0)+"Buzz"*(i%5==0) or i)
```

After searching on the internet, I found an improved version, saving 7 characters. It requires some clever number-hackery to get there and it is much less easy to understand.

```python
for i in range(100):print(i%3//2*'Fizz'+i%5//4*'Buzz'or-~i)
```

However, it occured to me that one might be able to do even better in another language. The two most famously terse languages I could think of are Perl and APL (although both also have a reputation as write-once languages and that their code looks like 'line noise').

In Perl, it takes 48 characters and it is not too unreadable.

```perl
print+(Fizz)[$_%3].(Buzz)[$_%5]||$_,$/for 1..1e2
```

APL is better at 38, but good luck making sense of it if you don't know APL.

```apl
{∊(3↑(0=3 5|⍵)∪1)/'Fizz' 'Buzz'⍵}¨⍳100
```

For what it's worth, we can replace the glyphs with their names and read it backwards to get something fairly readable. 

```
100 iota map 
{['Fizz' 'Buzz' right-arg] replicate 
(1 union ([3 5] residue right-arg equal 0) take 3) 
enlist}
```

Converting to more familiar Perl / Python -ish notation, we can finally understand how it works.

```
1..100 map (['Fizz', 'Buzz', $_] * (($_ % [3, 5] == 0).union(1))[:3]) list)
```

Note that APL is exploiting some unexpected behaviour too:  `∪1` 'union 1' adds a `1` to the selection list if it doesn't already contain one; and `3↑`'take 3' will provide an additional `0` by default otherwise.

Perhaps one could conceive of a language that combines the best of all worlds: as terse as APL, as expressive as APL, but as clear as Python? Perhaps we can invent a language in which FizzBuzz can be written in 23 characters as:

```
1..100:3|?Fizz+5|?Buzz∨
```

Somehow this seems like a significant improvement over the Python, Perl and APL solutions, but it is hard to pin down precisely what is better about it. Here is my thought process:

1. The hypothetical program is even shorter than APL, but is arguably the clearest expression of the algorithm - there is a direct correspondence between every character in the code and the algorithm. There is no hackery or language-imposed 'accidental complexity'.

2. I think `1..100:` is the best way to say iterate over the values from 1 to 100 inclusive. Python's `for i in range(1, 101):` is pretty ugly by comparison, especially the fact that the number 100 isn't even used. Perl's `for 1..1e2` is better, but I'm not sure I understand why it doesn't use 100. APLs `¨⍳100` is nice, but only if you know what iota and the diaeresis glyphs mean. Ruby has `1..100` and it seems more than sufficient.

3. Perl and APL do not use an explicit variable for the iteration. It seems pointless to have to name the loop variable and Perl's `$_` is a reasonable choice for an anonymous loop variable. APL can have two 'implicit' variables called `⍺` and `⍵` for the left and right arguments. The hypothetical version simply asks whether a function has enough arguments and if not substitutes the implicit variable automatically. This `3|` is immediately translated into `3|_`, `?Fizz` into `? Fizz _` and `...∨` into `...∨_`. As far as I know, this would be a unique feature.

4. I think for a terse scripting language, the final value of a function or program should automatically be used as the return value. Rust and Lisp both use this convention, and it seems more sensible than having an explicit print statement, which is not actually part of the algorithm.

5. In common with most languages, all three of our languages use modulo arithmetic to test for divisibility. Thus we must explicitly say `i%3==0` in Python for example. While it divisibility is a narrower use case, I think it is sufficiently common that it warrants having an extra primitive for it. I have stuck with the theme of using the mathematical symbol and opted to use `|` in my hypothetical language and `∨` for or.

6. In all three languages, we use some unexpected language behaviours to determine whether to select 'Fizz' and 'Buzz'. In Python we multiply a string by 1 or 0, in Perl we index a length 1 list, and in APL we 'replicate' our string 1 or 0 times. In Python and APL, we make use of the unexpected behaviour, inherited from C which had no boolean type, that False is equivalent to integer 0 and True is equivalent to integer 1. I think it would be nice to instead be able to express the idea of taking or not taking an object more clearly. I have opted to use the `?` to mean `if` and if no `else` option is provided, then a null is returned instead.

7. Personally I am a fan of Rust's Option type, I think it is the best way to propagate an error, or non-value through a program. Especially helpful is if functions can treat the null as if it were an appropriate value of the same type. Here I am envisaging null to be equivalent to an empty string, but it could also represent the number 0, False or an empty list. APL is the most type-sensitive of the three languages we looked at, but all three have some issue with returning null values.

8. Python and Perl use `or` / `||` to mean something slightly different from 'logical or'. Like Lisp before them, both treat or as a shortcut operator: it returns the first argument if it is 'truthy', and otherwise the second argument. This "Hello" or 5 returns "Hello", while "" or 0 returns 0. Despite the fact that it is slightly unexpected, it is sufficiently common in programming languages at this point that I think it is an acceptable choice, given the additional power it provides.

The question is, could our hypothetical program actually be expanded into a working functional language that would be practical for everyday use?

Could we do even better? Is it conceivable to express FizzBuzz in fewer than 20 characters? Would it still be intelligible? Is there a way to express the FizzBuzz algorithm even more clearly or more elegantly without making it significantly longer or adding more language-specific complexity?

Additionally, if the hypothetical code is part of the language, what limitations will it place on how well it handles other kinds of code challenges? Is this a good language for these challenges? Would it allow new, elegant solutions to some of the problems? Would it struggle with certain kinds of problem?

I was keen to find out!

## The goals of fb1337

fb1337 was my attempt to convert the above code snippet into a functional all-purpose language. I set myself three goals for the project:

1. Express FizzBuzz a tersely and clearly as possible. Ideally as close as possible to 20 characters without sacrificing readability. Is the hypothetical example above practical? What limitations will it impose on the language as a whole?

2. Code a wide variety of code challenge problems in the language to demonstrate the universal applicability of the language for these kinds of problems. (I chose the first 20 problems from [Project Euler](https://forum.projecteuler.net/about), and a selection of 40 [LeetCode](https://leetcode.com) challenge problems from Conor Hoekstra's YouTube channel).

3. To write a personal code golfing language to use for my own enjoyment!

## Research and inspiration

I looked to a number of places for inspiration.

1. *Code_Report* I found a great deal of inspiration in Conor Hoekstra's [code_report YouTube channel](https://www.youtube.com/c/codereport). On this channel, Conor has looked to find short, expressive solutions to coding challenge problems. In particular, he has a fascination for functional languages such as Haskell and array languages such as APL and its derivatives. Along the way he has made a study of combinators.

2. *APL* Following Hoekstra's lead, I looked more deeply into the [APL](https://www.dyalog.com) language to try to understand how APL manages to do so much with so few glyphs. I also dug out my old, battered (and largely unread) copy of Ken Iverson's book ["A Programming Language"](https://a.co/d/eGQ7kLV).

3. *Combinators* Also following a lead from Hoekstra, I explored the world of combinatory logic, reading [Raymond Smullyan's "To Mock a Mockingbird"](https://a.co/d/91w8NSg) and researching some of the mathematical history of [combinatory logic](https://en.wikipedia.org/wiki/Combinatory_logic).

4. *Code Golf* I looked at three languages that were created for competitive [code golf](https://en.wikipedia.org/wiki/Code_golf#Dedicated_golfing_languages). I had come across Brian Chen (Betaveros)'s  [Paradoc](https://github.com/betaveros/paradoc) a few years ago and had resolved to look more closely at it (He has also written an interesting [Introduction to Code Golf](https://blog.vero.site/post/golf). [GolfScript](http://www.golfscript.com/golfscript/) is one of the very first code golf language and its sheer simplicity was a revelation given how powerful it is. Finally, I looked at one of the most recent code golf languages, [Jelly](https://github.com/DennisMitchell/jellylanguage?tab=readme-ov-file) which is a good deal more complicated. For more on code golf, see [A Short Potted History of Code Golf](code_golf.md).

5. *Stack-Based Byte Code* I brought some previous experience to the project having previously written a stack-based byte code interpreter for Scheme, [4Scheme](https://gitlab.com/QuesterZen/4Scheme). For that project I had done some reading on the [Java Virtual Machine Byte Code](https://en.wikipedia.org/wiki/Java_bytecode) which is predominantly stack-based, and on the stack language [Forth](https://amzn.asia/d/i8Gi9Ut). The project was also invaluable for my design for the interpreter eval / apply loop and the implementation of the local naming environment.

6. *Elixir* Of all the functional languages, [Elixir](https://elixir-lang.org) seems to be the best designed from the perspective of readability and practical programming. While Elixir wasn't a direct inspiration for any of the features of the final language, I had Elixir in mind as a benchmark for clarity of expression and readability of code.
