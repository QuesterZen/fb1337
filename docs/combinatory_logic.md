# Combinatory Logic

The origin of combinatory logic is found in the work of early pioneers in the logical foundations of functions. The idea is to combine combinators (ie. functions that take functions as inputs and produce functions as output) to describe any algorithm, or process imaginable. While the origins are relatively esoteric, their use in computing comes from the fact that it is often useful to inject behaviours into existing algorithms to specialise them (high level functions), compose functions using common patterns or algorithms and to build complex functions from simpler components that are easier to reason about.

The names of combinators are often taken, somewhat whimsically, from Raymond Smullyan's book To Mock a Mockingbird, which introduces combinatory logic through the metaphor of bird calls. However, functional languages such as Haskell and array languages such as APL make signficant use of some combinators as primary mechanisms for composition. For example, the Starling is the basis for Haskell's monadic chains, while the Phoenix and Starling are made use of in APL's forks (three-trains) and hooks (two trains). APL also makes use of the Psi combinator (over), Warbler (join) and Cardinal (flip) adverbs. Below is a table of the most useful combinators for programming and their implementation in fb1337.

Combinators
https://combinatorylogic.com/table.html
https://www.angelfire.com/tx4/cus/combinator/birds.html

Implementation
| Combinator | Bird     | Name     | Function           | Name      | Symbol | Outcome                   	| Implementation |
|------------|----------|----------|--------------------|-----------|--------|------------------------------|----------------|
| I          | Idiot    | Identity | λa.a               | Identity  | ℐ  	 | ℐf -> f                    	| f              |
| K          | Kestrel  | Constant | λab.a              | Constant  | 𝒦 	 | x𝒦y -> y                 	| ◌         	 |
| W          | Warbler  | Join     | λab.abb            | Join      | 𝒲 	 | x𝒲f -> f(x,x)            	| ∂ f     		 |
| C          | Cardinal | Flip     | λabc.acb           | Flip      | 𝒞 	 | xy𝒞f -> f(y,x)            	| « f     		 |
| B          | Bluebird | Compose  | λabc.a(bc..)       | Compose   | ∘  	 | #∘fg -> f(g(#))            	| g f     		 |
| S          | Starling | Compare  | λabc.ac(bc)        | S-Comb    | 𝒮 	 | x𝒮fg -> f(x,g(x))         	| ∂ g f    		 |
| Σ          | Violet S | Compare' | λabc.a(bc)c        | S'-Comb   | 𝔰 		 | x𝔰fg -> 	f(g(x),x)         	| ∂ ⊚ g f   	 |
| Ψ          | Psi      | On       | λabcd.a(bc)(bd)    | Psi-Comb  | Ψ  	 | xyΨfg -> g(f(x),f(y))      	| f ⊚ f g   	 |
| D2         | Dove     | Fork     | λabcde.a(bc)(de)   | D-Comb    | 𝒟  	 | xy𝒟fgh -> h(f(x),g(y))    	| g ⊚ f h   	 |
| Φ          | Phoenix  | Fork     | λabcd.a(bd)(cd)    | Phi-Comb  | 𝛷    	 | x𝛷fgh -> h(f(x),g(x))      	| ∂ g ⊚ f h 	 |
| Φ₁         | Pheasant | Fork     | λabcde.a(bde)(cde) | Phi2-Comb | 𝜙    	 | xy𝜙fgh -> h(f(x,y),g(x,y))	| ð g ⊚ f h 	 |
