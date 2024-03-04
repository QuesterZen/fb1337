# FBl337
# Programming Code Golf Language
# Created: 21 February 2024
# Version: 21 February 2024 12:00PM
# Copyright: James Leibert 2024
# Licence: Available for use under the GPL3 Licence https://www.gnu.org/licenses/gpl-3.0.txt

# iterators.py
# Iterator class - turns (almost) anything into an iterable and iterates over it.

import numpy as np


from fb1337.array import Array
from fb1337.environment import Environment
from fb1337.lambda_fn import run_object, runnable
from fb1337.slice import Slice


class Iterator:
	"""Iterators express generic loop logic. They allow blocks of code to be run in a for-type loop.
	The current value of the loop variable can be accessed via the context-specific _ implicit variable."""

	def __init__(self):

		self.implicit = None
		self.previous = None

		self.init = None
		self.cond = None
		self.update = None

		self.pointer = None
		self.array = None

		self.exit_now = False

	def next(self):
		if self.pointer is not None and self.array is not None:
			if self.pointer < len(self.array):
				self.pointer += 1
			while self.pointer < len(self.array) and self.array[self.pointer] == '':
				self.pointer += 1
		return self.pointer

	def value_at_pointer(self):
		if self.pointer is not None and self.array is not None and 0 <= self.pointer < len(self.array):
			return self.array[self.pointer]
		else:
			return ''

	@classmethod
	def from_object(cls, obj):
		new_iterator = Iterator()
		if type(obj) in (int, bool, float, np.float_):
			new_iterator.array = None
			new_iterator.pointer = None
			if obj < 0:
				new_iterator.init = lambda e: -round(obj)
				new_iterator.cond = lambda e: new_iterator.implicit > 0
				new_iterator.update = lambda e: new_iterator.implicit - 1
			elif obj > 0:
				new_iterator.init = lambda e: 1
				new_iterator.cond = lambda e: new_iterator.implicit <= round(obj)
				new_iterator.update = lambda e: new_iterator.implicit + 1
			else:
				new_iterator.init = lambda e: 0
				new_iterator.cond = lambda e: False
				new_iterator.update = lambda e: 0
		elif type(obj) is str:
			new_iterator.array = obj
			new_iterator.pointer = 0
			if len(obj) > 0:
				new_iterator.init = lambda e: new_iterator.array[new_iterator.pointer]
				new_iterator.cond = lambda e: new_iterator.pointer < len(new_iterator.array)
				new_iterator.update = lambda e: [new_iterator.next(), new_iterator.value_at_pointer()][1]
			else:
				new_iterator.init = lambda e: ''
				new_iterator.cond = lambda e: False
				new_iterator.update = lambda e: ''
		elif isinstance(obj, Array):
			if obj.is_structured() and len(obj.get_shape()) > 1:
				new_iterator.array = [obj.build(x) for x in obj.structured_values()]
				new_iterator.pointer = 0
			else:
				new_iterator.array = obj.values
				new_iterator.pointer = 0
				while new_iterator.pointer < len(new_iterator.array) and new_iterator.array[new_iterator.pointer] == '':
					new_iterator.pointer += 1
			if len(new_iterator.array) > 0:
				new_iterator.init = lambda e: new_iterator.array[new_iterator.pointer]
				new_iterator.cond = lambda e: new_iterator.pointer < len(new_iterator.array)
				new_iterator.update = lambda e: [new_iterator.next(), new_iterator.value_at_pointer()][1]
			else:
				new_iterator.init = lambda e: 0 if obj.is_structured() else ''
				new_iterator.cond = lambda e: False
				new_iterator.update = lambda e: 0 if obj.is_structured() else ''
		elif isinstance(obj, Slice):
			new_iterator.init = lambda e: obj.start_value
			new_iterator.cond = lambda e: (new_iterator.implicit < obj.stop_value) if obj.ascending \
				else (new_iterator.implicit > obj.stop_value)
			new_iterator.update = lambda e: new_iterator.implicit + obj.step_value
		elif type(obj) in (tuple, list, np.ndarray) and len(obj) > 0:
			new_iterator.array = list(obj)
			new_iterator.pointer = 0
			new_iterator.init = lambda e: new_iterator.array[new_iterator.pointer]
			new_iterator.cond = lambda e: new_iterator.pointer < len(new_iterator.array)
			new_iterator.update = lambda e: new_iterator.array[new_iterator.next()]
		else:
			raise TypeError("Cannot iterate over", obj)
		return new_iterator

	@classmethod
	def from_functions(cls, start_block, cond_block, step_block):
		new_iterator = cls()
		if runnable(start_block):
			new_iterator.init = start_block
		else:
			new_iterator.init = lambda e: start_block
		if runnable(cond_block):
			new_iterator.cond = cond_block
		elif not runnable(step_block) and type(step_block) is int:
			if step_block < 0:
				new_iterator.cond = lambda e: new_iterator.implicit > cond_block
			else:
				new_iterator.cond = lambda e: new_iterator.implicit < cond_block
		else:
			new_iterator.cond = lambda e: new_iterator.implicit != cond_block
		if runnable(step_block):
			new_iterator.update = step_block
		else:
			new_iterator.update = lambda e: new_iterator.implicit + step_block
		return new_iterator

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
