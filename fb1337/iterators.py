# FBl337
# Programming Code Golf Language
# Created: 21 February 2024
# Version: 21 February 2024 12:00PM
# Copyright: James Leibert 2024
# Licence: Available for use under the GPL3 Licence https://www.gnu.org/licenses/gpl-3.0.txt

# iterators.py
# Iterator abstract base class. Iterable flat list class. List slice class.


from fb1337.array import Array, FlatList, Coordinate
from fb1337.environment import Environment
from fb1337.lambda_fn import run_object


class Iterator:
	"""Iterators express generic loop logic. They allow blocks of code to be run in a for-type loop.
	The current value of the loop variable can be accessed via the context-specific _ implicit variable."""

	def __init__(self, init_block, cond_block, update_block):

		self.implicit = None
		self.previous = None

		self.init = init_block
		self.cond = cond_block
		self.update = update_block

		if type(init_block) is int:
			self.init = lambda e: init_block
		if type(cond_block) is int:
			if type(update_block) is int and update_block < 0:
				self.cond = lambda e: self.implicit > cond_block
			else:
				self.cond = lambda e: self.implicit < cond_block
		if type(update_block) is int:
			self.update = lambda e: self.implicit + update_block

		self.exit_now = False

	def start(self, env, body):

		env.implicit_object = self

		run_object(env, self.init)
		self.previous = self.implicit
		self.implicit = env.pop()

		while not self.exit_now:

			run_object(env, self.cond)
			run_block = Array.truthy(env.pop())

			if run_block:
				block_env = Environment(env)
				block_env.implicit_obj = self
				body(block_env)

			else:

				break

			run_object(env, self.update)
			self.previous = self.implicit
			self.implicit = env.pop()

		env.implicit_object = None

		return None

	def exit_iteration(self):
		self.exit_now = True

	def __repr__(self):
		return "<Iterator implicit=" + str(self.implicit) + ">"


class LoopIterator(Iterator):
	"""Loop iterators are a specialisation of iterator that runs a simple loop from 1 to n.
	They are initialised with range specifiers: start, stop, step"""

	def __init__(self, n, base):
		super().__init__(None, None, None)

		self.n = abs(n)
		self.base = base
		ascending = n > 0

		self.start_value = self.base if ascending else self.n - 1 + base
		self.stop_value = self.n + self.base if ascending else base - 1
		self.step_value = 1 if ascending else - 1

		self.implicit = self.start_value

		self.init = lambda e: self.start_value
		self.cond = lambda e: (self.implicit < self.stop_value) if ascending else (self.implicit > self.stop_value)
		self.update = lambda e: self.implicit + self.step_value

	def __repr__(self):
		s = "<Loop Iterator"
		s += " implicit=" + str(self.implicit)
		s += " base " + str(self.base) + " n " + str(self.n) + " step " + str(self.step_value)
		s += ">"
		return s


class ListIterator(Iterator, FlatList):
	"""A list iterator holds a list that can be modified, and can be iterated over.
	There are three special list types that are recognised and treated differently by some commands:
	1. Nulled Lists. These are excluded from iteration and creating new lists from a nulled list usually
	excludes these elements
	2. Number lists. A list that contains only numbers can sometimes act like a matrix and conversions to / from matrices
	are sometimes automatic. Character lists are included as characters are translated into unicode code points and treated
	as integers. Note that lists do not contain floating point values so these conversions are not lossless.
	3. Lists of Lists. Lists containing lists can use some additional matrix modification commands such as row-reduce and
	transpose (zip).
	"""

	def __init__(self, structured_values):

		Iterator.__init__(self, None, None, None)
		FlatList.__init__(self, structured_values, 0)

		self.index = 0

		self.implicit = self.move_to(0)

		self.init = lambda e: self.move_to(0)
		self.cond = lambda e: 0 <= self.index < len(self.flat_list())
		self.update = lambda e: self.next(1)

	def build(self, structured_list):
		new_list = ListIterator(structured_list)
		return new_list

	# Ways to create new 1D lists

	@classmethod
	def pair(cls, a, b):
		"""Create a list by pairing up values or appending them to a list"""
		new_values = (a.values if isinstance(a, ListIterator) else [a]) + (
			b.values if isinstance(b, ListIterator) else [b])
		return cls(new_values)

	@classmethod
	def stack_to_list(cls, env):
		"""Convert all objects on the stack from the last null into a list"""
		values = []
		more = True
		while more:
			value = env.pop()
			if value is not None and value != '':
				if isinstance(value, Array) and not isinstance(value, Coordinate):
					values.append(value.structured_values())
				else:
					values.append(value)
			else:
				more = False
		return cls(values[::-1])

	@classmethod
	def int_list(cls, a, b=None):
		"""Create a list of integers from a..b or b..a.
		If only one value is provided, the list starts/ends at 1."""
		if b is None and a > 0:
			return cls(list(range(1, a + 1, 1)))
		elif b is None and a < 0:
			return cls(list(range(-a, 0, -1)))
		elif a > b:
			return cls(list(range(a, b - 1, -1)))
		else:
			return cls(list(range(a, b + 1, 1)))

	# Ways to modify a flat list

	def slice(self, slice_object):
		"""Create a new list using values in this list indicated by a slice object (ie a range indicator)"""
		s = slice_object.start_param - 1 if slice_object.start_param is not None else 0
		f = slice_object.stop_param if slice_object.stop_param is not None else len(self.values)
		a = slice_object.step_param if slice_object.step_param is not None else (1 if f > s else -1)
		new_values = self.all_values()[s: f: a]
		return ListIterator(new_values)

	def skip(self, n):
		"""Return a list containing every nth non-null value in the current list"""
		new_values = [x for x in self.all_values() if x != ''][::n]
		return ListIterator(new_values)

	def insert(self, other, loc=None):
		"""Insert a values into the current list to create a new list"""
		s_flat = self.all_values()

		if loc is None or loc > len(s_flat):
			insertion_point = len(s_flat)
		elif loc < 0:
			insertion_point = max(0, len(s_flat) + loc)
		else:
			insertion_point = loc

		if isinstance(other, ListIterator):
			o_flat = other.all_values()
		elif Array.container(other):
			o_flat = list(other)
		else:
			o_flat = [other]

		new_values = s_flat[:insertion_point] + o_flat + s_flat[insertion_point:]

		return ListIterator(new_values)

	# Non-destructive mutation

	def set_location(self, i, value):
		values = self.flat_list()
		if 0 <= i < len(values):
			values[i] = value
		self.values = values
		self.next(0)
		return self

	def set_slice(self, slice_object, value):
		values = self.values
		s = slice_object.start_param if slice_object.start_param is not None else 0
		f = slice_object.stop_param + 1 if slice_object.stop_param is not None else len(values) + 1
		a = slice_object.step_param if slice_object.step_param is not None else (1 if f >= s else -1)
		for i in range(s, f, a):
			if 0 <= i - 1 < len(values):
				values[i - 1] = value
		self.values = values
		self.next(0)
		return self

	def return_mutated(self, new_struc):
		self.values = new_struc
		self.next(0)
		return self

	# Moving the list pointer

	def move_to(self, i):
		"""Move the list pointer to the first non-null position at or after i"""
		values = self.values
		lenvals = len(values)
		if 0 <= i < lenvals:
			self.index = i
		elif -lenvals <= i < 0:
			self.index = lenvals - i
		elif i < -lenvals:
			self.index = 0
		elif i > lenvals:
			self.index = lenvals - 1
		return self.next(0)

	def next(self, advance=1):
		"""Advance the list pointer by advance non-null positions."""
		values = self.values
		lenvals = len(values)
		if advance == 0:
			while 0 <= self.index < lenvals and values[self.index] in [None, '']:
				self.index += 1
		elif advance > 0:
			for _ in range(advance):
				self.index = min(self.index + 1, lenvals)
				while 0 <= self.index < lenvals and values[self.index] in [None, '']:
					self.index += 1
		elif advance < 0:
			for _ in range(-advance):
				self.index = min(self.index - 1, lenvals)
				while 0 <= self.index < lenvals and values[self.index] in [None, '']:
					self.index -= 1
		return values[self.index] if 0 <= self.index < lenvals else ''

	# Character list functions

	@classmethod
	def to_ch_list(cls, x):
		"""Convert a string into a list of character code points. Or an integer into a list of digits."""
		if type(x) is str:
			values = [ord(ch) for ch in x]
		elif type(x) is int:
			values = [int(ch) for ch in str(x)]
		else:
			values = [ord(ch) for ch in str(x)]
		return cls(values)

	def __repr__(self):
		shape = self.get_shape()
		index_coord = Array.coordinates_for_flat_index(self.index, shape)
		struc = self.structured_values()

		def struc_str(remaining, i_coord, active_index=True):
			if not type(remaining) is list and not type(remaining) is tuple:
				return str(remaining) if (i_coord[0] != 0 or not active_index) else '<' + str(remaining) + '>'
			elif len(i_coord) == 1:
				return ', '.join(
					[(str(x) if (i_coord[0] != i or not active_index) else "<" + str(x) + ">") for i, x in
					 enumerate(remaining)])
			else:
				return '[' + '], ['.join(
					[struc_str(l, i_coord[1:], i_coord[0] == i) for i, l in enumerate(remaining)]) + ']'

		s = "<List Iterator "
		s += struc_str(struc, index_coord)
		s += ">"
		return s


class Slice(Iterator):
	"""Slice objects allow you to access regularly spaced values in a list to alter all at once, or
	to create a new list. They operate similarly to Python slices"""

	DEFAULT_MAX = 1000000000

	def __init__(self, s, f, a):
		def clean_value(x):
			if type(x) is None: return None
			if type(x) is int: return x
			if type(x) is str and len(x) == 0 or x is False: return None
			if type(x) is str:
				try:
					x = int(x)
				except ValueError:
					return None
				return x
			return None

		super().__init__(None, None, None)

		self.start_param, self.stop_param, self.step_param = [clean_value(x) for x in [s, f, a]]

		self.start_value = self.start_param if self.start_param is not None else (
			1 if self.stop_param is None or self.stop_param > 0 else -1)
		self.stop_value = self.stop_param if self.stop_param is not None else (
			Slice.DEFAULT_MAX if self.step_param is None or self.step_param > 0 else -Slice.DEFAULT_MAX)
		ascending = self.stop_value > self.start_value
		self.step_value = self.step_param if self.step_param is not None else (1 if ascending else -1)

		self.implicit = self.start_value

		self.init = lambda e: self.start_value
		self.cond = lambda e: (self.implicit < self.stop_value) if ascending else (self.implicit > self.stop_value)
		self.update = lambda e: self.implicit + self.step_value

	def slice_string(self, string):
		return string[self.start_value:self.stop_value:self.step_value]

	def __repr__(self):
		return "<Slice [" + str(self.start_param) + ":" + str(self.stop_param) + ":" + str(self.step_param) + "]>"
