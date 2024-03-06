# Some simple programs in fb1337

Please feel free to add examples to this page, including:

- the shortest code golf solution

- the most beautiful solution

- the most expressive solution

- an interesting alternative solution

## Hello World!

```fb1337
Hello` World`!						⍝ shortest
```

## FizzBuzz

```fb1337
ḣ:Fizz‿Buzz3‿5_|⊃'_∨				⍝ shortest
ḣ:_‰3⁈Fizz_‰5⁈Buzz⊕_∨				⍝ clearest
ḣ⍳𝔰∨∘⊸(3‿5)⊚|⋮∘⊸(Fizz‿Buzz)⊃'		⍝ point-free combinator
```

## First 100 Primes

```fb1337
ḣ𝜋									⍝ built-in
ḣ⍳↓1𝒮⟈𝒲⊚×							⍝ shortest
ḣ⍳∂∂⩔!~«%1=⊃						⍝ using number theory
Ø‿Øḣ⩔⍳⩓⊕∂:_ḣ√>?⌁@{(_²)Ø_Ø			⍝ fastest: Sieve of Eratosthenes
```

## Is it prime?

```fb1337
ℸ#1=								⍝ built-in
∂√⍳↓1𝒞|⊐¬							⍝ shortest
```

## Shortest Infinite Loop

```fb1337
:									⍝ shortest
⍣⊢Ø									⍝ shortest non-trivial
```

## Separate A List into Odd and Even Values

```fb1337
∂2%⊆								⍝ shortest
```