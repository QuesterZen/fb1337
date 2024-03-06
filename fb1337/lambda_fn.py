# FBl337
# Programming Code Golf Language
# Created: 21 February 2024
# Version: 21 February 2024 12:00PM
# Copyright: James Leibert 2024
# Licence: Available for use under the GPL3 Licence https://www.gnu.org/licenses/gpl-3.0.txt

# lambda_fn.py
# User defined functions and function combinators


from fb1337.environment import Environment


def runnable(obj):
	return isinstance(obj, Lambda) or type(obj).__name__ == 'function'


def run_object(env, obj):
	"""Determines what the object is and what the appropriate form of 'running' it would be:
	for Python functions, Python lambdas with one argument, blocks or delayed execution thunks these are simply run with the environment as a parameter
	for Python functions or lambdas with multiple arguments, these are taken from the stack and run
	for Lambda objects the object is run
	all other objects are ignored
	All runnable objects either return a value, or leave values on the stack. when run_object is run, the value is always left on the stack
	"""
	if obj is None:
		pass
	elif isinstance(obj, Lambda):
		obj.go(env)
	elif type(obj).__name__ == "function" and obj.__code__.co_argcount == 1:
		r = obj(env)
		if r is not None:
			env.push(r)
	elif type(obj).__name__ == "function":
		parameters = [env.pop() for _ in range(obj.__code__.co_argcount)]
		r = obj(*parameters)
		if r is not None:
			env.push(r)
	else:
		pass


def fp2fn(e, f, n):
	def new_fn(*args):
		if len(args) != n:
			raise ValueError("Warning: Number of arguments not consistent with prototype", len(args), n)
		for a in args:
			e.push(a)
		f(e)
		return e.pop()

	return new_fn


def fc2fn(e, f):
	return lambda *args: f(e, *args)


class Lambda:
	"""Lambdas hold blocks of code that can be run later.
	The block is represented as a Python lambda which takes an environment in which the lambda is to be run.
	The block does not return a value or take external parameters, but instead operates via the stack.
	This environment should have an outer environment as a child, but can also be run in isolation with a base environment
	with its own implicit values, namespace variables and stack.
	"""

	def __init__(self, block, use_implicit=False, caching=False):

		self.block = block
		self.use_implicit = use_implicit
		self.cache = dict() if caching else None

	def go(self, env):

		if self.use_implicit:
			i = env.implicit()
			env.push(i)

		param = env.peek()
		if self.cache is not None and param is not None and type(param).__hash__ and param in self.cache:
			env.pop()
			env.push(self.cache[param])
			return

		local_env = Environment(env)
		self.block(local_env)

		if self.cache is not None and param is not None and type(param).__hash__:
			self.cache[param] = local_env.peek()

	@staticmethod
	def combinator(comb, f, g=(lambda e: 0), h=(lambda e: 0)):
		""" Combinators are operators that take functions as parameters and return modified functions
		https://combinatorylogic.com/table.html
		https://www.angelfire.com/tx4/cus/combinator/birds.html

		Comb	Bird		Name		Function			Name		Symbol		Outcome						Implementation

		I 		Idiot		Identity	λa.a				Identity 	ℐ			ℐf -> f 						f
		W		Warbler		Join		λab.abb				Join 		𝒲 			x𝒲f -> f(x,x)					∂ f
		C		Cardinal	Flip		λabc.acb			Flip  		𝒞			xy𝒞f -> f(y,x)					« f

		B		Bluebird	Compose		λabc.a(bc)		    Compose 	∘			#∘fg -> f(g(#))					g f
		S		Starling	Compare		λabc.ac(bc)			S-Comb 		𝒮			x𝒮fg -> f(x,g(x))				∂ g f
		Σ		Violet S	Compare'	λabc.a(bc)c			S'-Comb		𝔰			x𝔰fg -> 	f(g(x),x) 				∂ ⍮g f
		Ψ		Psi			On			λabcd.a(bc)(bd)		Psi-Comb 	Ψ			xyΨfg -> g(f(x),f(y))			f ⍮f g

		D2		Dove		Fork		λabcde.a(bc)(de)	D-Comb 		𝒟 			xy𝒟fgh -> h(f(x),g(y))			g ⍮f h
		Φ		Phoenix		Fork		λabcd.a(bd)(cd)		Phi-Comb 	𝛷			x𝛷fgh -> h(f(x),g(x))			∂ g ⍮f h
		Φ₁		Pheasant	Fork		λabcde.a(bde)(cde)	Phi2-Comb 	𝜙			xy𝜙fgh -> h(f(x,y),g(x,y))		ð g ⍮f h
		"""
		if comb == 'I':
			def combinator(e):
				run_object(e, f)
				return e.pop()
		elif comb == 'W':
			def combinator(e):
				e.push(e.peek())
				run_object(e, f)
				return e.pop()
		elif comb == 'C':
			def combinator(e):
				y = e.pop()
				x = e.pop()
				e.push(y)
				e.push(x)
				run_object(e, f)
				return e.pop()
		elif comb == "B":
			def combinator(e):
				run_object(e, g)
				run_object(e, f)
				return e.pop()
		elif comb == "S":
			def combinator(e):
				x = e.peek()
				run_object(e, g)
				y = e.pop()
				e.push(x)
				e.push(y)
				run_object(e, f)
				return e.pop()
		elif comb == "S'":
			def combinator(e):
				x = e.peek()
				run_object(e, g)
				e.push(x)
				run_object(e, f)
				return e.pop()
		elif comb == "Psi":
			def combinator(e):
				run_object(e, g)
				x = e.pop()
				run_object(e, g)
				e.push(x)
				run_object(e, f)
				return e.pop()
		elif comb == "D":
			def combinator(e):
				run_object(e, h)
				x = e.pop()
				run_object(e, g)
				e.push(x)
				run_object(e, f)
				return e.pop()
		elif comb == "Phi":
			def combinator(e):
				e.push(e.peek())
				run_object(e, h)
				x = e.pop()
				run_object(e, g)
				e.push(x)
				run_object(e, f)
				return e.pop()
		elif comb == "Phi'":
			def combinator(e):
				y = e.pop()
				x = e.pop()
				e.push(x)
				e.push(y)
				e.push(x)
				e.push(y)
				run_object(e, h)
				x = e.pop()
				run_object(e, g)
				e.push(x)
				run_object(e, f)
				return e.pop()
		else:
			print("Unknown combinator", comb)
			raise TypeError
		return combinator

	@staticmethod
	def bind(direction, f, value):

		if direction == 'left':
			# xPf -> λy.f(x,y)
			def bind_left(e, x=value):
				y = e.pop()
				e.push(x)
				e.push(y)
				run_object(e, f)
				return e.pop()

			return bind_left

		elif direction == 'right':
			# xPf -> λy.f(y,x)
			def bind_right(e, x=value):
				y = e.pop()
				e.push(y)
				e.push(x)
				run_object(e, f)
				return e.pop()

			return bind_right

	@staticmethod
	def dip(e, f):
		y = e.pop()
		x = e.pop()
		e.push(x)
		run_object(e, f)
		e.push(y)
		return e.pop()

	@staticmethod
	def repeat(e, f, n):
		for i in range(n):
			run_object(e, f)
		return e.pop()

	@staticmethod
	def repeat_until(e, f, g):
		while True:
			run_object(e, f)
			run_object(e, g)
			if e.pop():
				break
		return e.pop()

	@staticmethod
	def late_eval(e, expr):
		return run_object(e, expr)
