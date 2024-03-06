# A Short Potted History of Code Golf

## What is Code Golf?

[Code golf](https://en.wikipedia.org/wiki/Code_golf) a form of recreational computing where the goal is to write the shortest possible program to accomplish a given task. The name is a whimsical reference to conventional golf, where the lowest score wins.

## Relationship to Information Theory

In Mathematics, the concept of the 'information content' of a message is the minimal number of binary digits required to convey the message in an optimal encoding. It relates closely to the concept of entropy - the more 'order' in a system, the better the opportunity to describe the order concisely. 

> For example, consider the two 'messages': `CTVJKQRAVIOXDLG` and `ABCABCABCABCABC`, both of 15 characters. A typical approach to text compression is [LZSS encoding](https://en.wikipedia.org/wiki/Lempel–Ziv–Storer–Szymanski), which looks for repetitions in the text and replaces the repetition with a reference to its first occurrence in the original. It would render `ABCABCABCABCABC` as `ABC030603`. Meanwhile, in information theory, it is possible to show that for independent symbols of known probability distributions, [Huffman Codes](https://en.wikipedia.org/wiki/Huffman_coding) provide an optimal encoding. A combination of these two techniques leads to extremely efficient compression of texts. A simple implementation of these two algorithms encodes the first message into 108 bits and the second into 40, indicating that the first message contains almost 3 times the information content of the second. 

In programming, this translates to [**Kolmogorov complexity**](https://en.wikipedia.org/wiki/Kolmogorov_complexity), which is the shortest possible computer program in a given language that produces a given output. For mathematical proofs, the language used is often that of [Turing Machines](https://en.wikipedia.org/wiki/Turing_machine), which is not a practical programming language.

> If you want a flavour if this try programming in [Brainfuck](https://en.wikipedia.org/wiki/Brainfuck) or read [Turing's paper](https://www.amazon.com.au/dp/0470229055) which originally introduced his [Turing Machine](https://en.wikipedia.org/wiki/Turing_machine).

## The History of Code Golf

The theory of Kolmogorov complexity was developed in the 1960s in parallel with the development of the earliest high level computer languages. [Ken Iverson](https://en.wikipedia.org/wiki/Kenneth_E._Iverson), the creator of [APL](https://en.wikipedia.org/wiki/APL_(programming_language)), which was first described as a notational system in 1962 and first released as a programming language in 1966, seems to have been aware of this concept. Ken Iverson is known to have been proud of particularly short examples of algorithms and was keen to show he could out-do other practitioners in the brevity of his programs. In the MIT programming community that developed around the PDP-11 in the 1970s, there were also informal competitions to find neat binary hacks to shorten programs and find extremely terse if cryptic algorithms.

> For example, see the MIT [HACKMEM](https://en.wikipedia.org/wiki/HAKMEM) document among others.

The term **code golf** first appeared much later in the context of [Perl](https://en.wikipedia.org/wiki/Perl) programming. In around 1999 a Perl forum held an informal competition to code golf the RSA algorithm. Perl's infamous terseness and shortcuts provided an excellent playground for such competitive pursuits, particularly given its reputations as a 'Hacker' language.

## Code Golfing Languages

The first languages specifically designed for code golfing appeared around 2005, and include [**GolfScript**](http://www.golfscript.com/golfscript/), which is particularly notable for having a very small vocabulary. In common with many dedicated code golfing languages, it is a stack-based language. This leads to very short programs, but can make them extremely hard to read. For example, a program to print the first 1000 digits of pi in GolfScript is:

```golfscript
;''
6666,-2%{2+.2/@*\/10.3??2*+}*
`1000<~\;
```

More recently, a popular code golfing language is [**Jelly**](https://github.com/DennisMitchell/jellylanguage) (around 2015) which is strongly influenced by APL-variant J, rather than GolfScript and is notable for its encoding into 250 unicode glyphs, making extremely unreadable even for a code golfing language. In addition to its complicated vocabulary, it also uses a dictionary to compress strings, resulting in this 'Hello World' program:

```jelly
3ḅaė;œ»
```

## For more information

A number of online forums and competition sites now exist for code golfing, including [Code Golf](https://code.golf) and the [StackExchange Code Golf forum](https://codegolf.stackexchange.com).
