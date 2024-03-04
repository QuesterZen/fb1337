# FBl337
# Programming Code Golf Language
# Created: 21 February 2024
# Version: 21 February 2024 12:00PM
# Copyright: James Leibert 2024
# Licence: Available for use under the GPL3 Licence https://www.gnu.org/licenses/gpl-3.0.txt

# array.py
# Array types: (flat) List, StructuredArray, Matrix and Coordinates

from functools import reduce
from itertools import accumulate, chain, count
from math import sqrt
from operator import add, mul

import numpy as np
from math import isqrt


class Array:

	def __init__(self):
		self.values = None
		self.default = None
		self.iterable_pointer = None

	# Must be implemented by all sub classes

	def get_shape(self):
		"""For structured arrays, return a tuple containing the shape of the array.
		For flat arrays return the length."""
		raise NotImplementedError

	def is_structured(self):
		"""Structured arrays return True, flat arrays return False"""
		raise NotImplementedError

	def structured_values(self):
		"""For structured arrays, return the array of values.
		For flat arrays, return the list of values."""
		raise NotImplementedError

	def iterable(self):
		"""Returns a list of items to iterate over for iteration, filter, map, reduce, outer and inner product etc.
		Structured arrays should return StructuredArray objects."""
		raise NotImplementedError

	def all_values(self):
		"""Flat Lists should include non-iterable values. Structured arrays should return flattened values."""
		raise NotImplementedError

	def mutate(self, structured_values):
		"""Should update the same object and return itself"""
		raise NotImplementedError

	def build(self, structured_values):
		"""Build a new object of the same type"""
		raise NotImplementedError

	# Class functions relating to types

	@staticmethod
	def truthy(x):
		if x is None: return False
		if type(x) is bool: return x
		if type(x) is int: return x != 0
		if type(x) is str: return x != ''
		if type(x) is float or type(x) is np.float_: return x != 0.
		return True

	@staticmethod
	def container(x):
		return type(x) in (list, tuple, np.ndarray)

	@staticmethod
	def number(x):
		return type(x) in (int, float, bool, np.float_)

	# Type Conversions

	@staticmethod
	def promote(array):
		if isinstance(array, FlatList):
			values = array.iterable()
			array_type = [isinstance(v, Array) for v in values]
			if all(array_type):
				return StructuredArray([x.structured_values() for x in values])
			elif all([not v for v in array_type]):
				return StructuredArray([0 if x == '' else x for x in values])
			else:
				return StructuredArray(values)
		elif isinstance(array, Coordinate):
			return StructuredArray([x for x in array.iterable()])
		else:
			return array

	@staticmethod
	def demote(array):
		if isinstance(array, Matrix):
			return FlatList(array.iterable().tolist())
		else:
			return FlatList(array.iterable())

	# Utility List Functions

	def unique_values(self):
		self_flat = self.iterable()
		seen = set()
		unique = []
		for x in self_flat:
			if x not in seen:
				unique.append(x)
				seen.add(x)
		return unique

	# Default Implementation of List Functions

	# Methods that do not alter the array

	def count(self, axis=-1):
		if self.is_structured():
			shape = self.get_shape()
			if -len(shape) <= axis < len(shape):
				return shape[axis]
			else:
				return 0
		else:
			return len(self.iterable())

	def equivalent(self, other):
		if not isinstance(other, Array):
			return False
		elif self.get_shape() != other.get_shape():
			return False
		elif not all([x == y for x, y in zip(self.all_values(), other.all_values())]):
			return False
		else:
			return True

	def grade(self, reverse=False):
		grades = [i for _, i in sorted([(v, i) for i, v in enumerate(self.all_values())], reverse=reverse)]
		if self.is_structured():
			structured = StructuredArray.shape_structured(grades, self.get_shape())
			return self.build(structured)
		else:
			return self.build(grades)

	# Methods that mutate the existing array

	def reshape(self, shape):
		all_values = self.all_values()
		size = reduce(mul, [x for x in shape if x != 0], 1)
		if shape[-1] == 0 and len(all_values) % size == 0:
			new_shape = [s for s in shape if s != 0]+[len(all_values) // size]
		elif shape[0] == 0 and len(all_values) % size == 0:
			new_shape = [len(all_values) // size] + [s for s in shape if s != 0]
		else:
			new_shape = [s for s in shape if s != 0]

		if len(new_shape) == 0 and len(all_values) == 0:
			new_struc = [self.default]
		elif len(new_shape) == 0:
			new_struc = [all_values[0]]
		elif len(new_shape) == 1 and new_shape[0] <= len(all_values):
			new_struc = [all_values[:new_shape[0]]]
		elif len(new_shape) == 1:
			new_struc = all_values + [self.default] * (new_shape[0] - len(all_values))
		else:
			new_struc = StructuredArray.shape_structured(all_values, new_shape, self.default)

		return Array.promote(self.mutate(new_struc))

	def flatten(self):
		new_struc = self.all_values()
		return self.mutate(new_struc)

	def set_bool(self, bool_array, new_value):
		s_flat = self.all_values()
		b_flat = bool_array.all_values()
		new_values = [new_value if Array.truthy(b) else s for s, b in zip(s_flat, b_flat)]
		if self.is_structured():
			new_values = StructuredArray.shape_structured(new_values, self.get_shape())
		return self.mutate(new_values)

	def set_index(self, index, new_value):
		values = self.all_values()
		if self.is_structured():
			shape = self.get_shape()
			flat_index = StructuredArray.flat_index_for_coordinate(index, shape)
			values[flat_index] = new_value
			values = StructuredArray.shape_structured(values, shape)
		else:
			values[index] = new_value
		return self.mutate(values)

	def set_indices(self, indices, new_value):
		values = self.all_values()
		if type(indices) is int:
			new_values = values
			new_values[indices] = new_value
		elif type(indices).__name__ == 'Slice':
			new_values = values
			stop = indices.stop_value
			if stop is None or stop > len(new_values):
				stop = len(new_values)
			for i in range(indices.start_value, stop, indices.step_value):
				new_values[i] = new_value
		elif isinstance(indices, Array):
			new_values = values
			for i in indices.all_values():
				new_values[i] = new_value
		else:
			new_values = values
		return self.mutate(new_values)

	def extend(self, obj, start=False):
		if self.is_structured() and isinstance(obj, Array) and obj.is_structured() and self.get_shape() == obj.get_shape():
			if start:
				return StructuredArray([obj.structured_values(), self.structured_values()])
			else:
				return StructuredArray([self.structured_values(), obj.structured_values()])
		elif self.is_structured() and len(self.structured_values()) > 0 and isinstance(obj, Array) and len(
				obj.iterable()) == len(self.structured_values()[0]):
			if start:
				self.mutate([obj.structured_values()] + self.structured_values())
				return self
			else:
				self.mutate(self.structured_values() + [obj.structured_values()])
				return self
		elif isinstance(obj, Array) and len(self.iterable()) == len(obj.iterable()):
			if start:
				return StructuredArray([obj.iterable(), self.iterable()])
			else:
				return StructuredArray([self.iterable(), obj.iterable()])
		elif isinstance(self, FlatList) and isinstance(obj, FlatList):
			return FlatList([self.iterable(), obj.iterable()])
		elif not self.is_structured() and isinstance(obj, Array) and not obj.is_structured():
			if start:
				return self.mutate([obj] + self.iterable())
			else:
				return self.mutate(self.iterable() + [obj])
		elif not self.is_structured() and isinstance(obj, Array):
			if start:
				return StructuredArray(obj.iterable() + self.iterable())
			else:
				return StructuredArray(self.iterable() + obj.iterable())
		else:
			return self.insert(obj, 0 if start else -1)

	def insert(self, obj, loc=-1, mutate=False):
		values = self.iterable()
		if loc < 0:
			loc = len(values) + loc + 1
		values = values[:loc] + [obj] + values[loc:]
		if mutate:
				return self.mutate(values)
		else:
			return self.build(values)

	# Methods that create new arrays by combining arrays

	def join_on_axis(self, other, axis=-1):
		if not self.is_structured() and not other.is_structured():
			return self.build(self.iterable() + other.iterable())

		s_struc = self.structured_values()
		o_struc = other.structured_values()
		u_axis = axis if axis >= 0 else len(self.get_shape()) + axis

		def join_rec(a1, a2, ax):
			if ax == 0:
				if type(a1) is not list: a1 = [a1]
				if type(a2) is not list: a2 = [a2]
				return a1 + a2
			else:
				return [join_rec(x, y, ax - 1) for x, y in zip(a1, a2)]

		return self.build(join_rec(s_struc, o_struc, u_axis))

	# Methods that return a new array, composed largely from the current array

	def take(self, n):
		if self.is_structured():
			struc = self.structured_values()
			new_values = struc[:n]
		else:
			new_values = self.iterable()[:n]
		return self.build(new_values)

	def drop(self, n):
		if self.is_structured():
			struc = self.structured_values()
			new_values = struc[n:]
		else:
			new_values = self.iterable()[n:]
		return self.build(new_values)

	def sort(self, reverse):
		if self.is_structured():
			return FlatList(sorted(self.iterable(), reverse=reverse))
		else:
			return self.build(sorted(self.iterable(), reverse=reverse))

	def transpose(self):
		if not self.is_structured():
			structured = Array.promote(self)
		else:
			structured = self
		return StructuredArray(StructuredArray.permute_axes(structured.structured_values()))

	def reverse_on_axis(self, axis):
		if not self.is_structured():
			return self.build(self.iterable()[::-1])

		if axis < 0:
			axis = len(self.get_shape()) + axis

		def rev_rec(struc, u_axis):
			if not Array.container(struc):
				return struc
			elif u_axis == 0:
				return struc[::-1]
			else:
				return [rev_rec(s, u_axis - 1) for s in struc]

		new_struc = rev_rec(self.structured_values(), axis)
		return self.build(new_struc)

	def rotate_on_axis(self, axis, n):
		if not self.is_structured():
			if axis == 0:
				values = self.iterable()
				return self.build(values[-n:] + values[:-n])
			else:
				return self.build(self.iterable())

		shape = self.get_shape()
		if axis < 0:
			used_axis = len(shape) + axis
		else:
			used_axis = axis
		original = list(range(len(shape)))
		permutation = [original[used_axis]] + original[:used_axis] + original[used_axis + 1:]
		inverse = original[1:used_axis + 1] + [original[0]] + original[used_axis + 1:]
		permuted = StructuredArray.permute_axes(self.structured_values(), permutation)
		permuted = permuted[-n:] + permuted[:-n]
		returned = StructuredArray.permute_axes(permuted, inverse)
		return self.build(returned).reshape(shape)

	def shift_on_axis(self, axis, n):

		if not self.is_structured():
			values = self.iterable()
			if n > 0:
				shifted = [(self.default * n)] + values[:-n]
			else:
				shifted = values[-n:] + [(self.default * -n)]
			return self.build(shifted)

		shape = self.get_shape()
		if axis < 0:
			used_axis = len(shape) + axis
		else:
			used_axis = axis
		original = list(range(len(shape)))
		permutation = [original[used_axis]] + original[:used_axis] + original[used_axis + 1:]
		inverse = original[1:used_axis + 1] + [original[0]] + original[used_axis + 1:]
		permuted = StructuredArray.permute_axes(self.structured_values(), permutation)
		default = StructuredArray.map_struc(permuted[0], lambda x: self.default)
		if n > 0:
			shifted = [(default * n)] + permuted[:-n]
		else:
			shifted = permuted[-n:] + [(default * -n)]
		returned = StructuredArray.permute_axes(shifted, inverse)
		return self.build(returned).reshape(shape)

	def select_bool(self, array_bool):
		boolean_values = array_bool.all_values()
		target = self.all_values()
		result = [t for t, b in zip(target, boolean_values) if Array.truthy(b)]
		return FlatList(result)

	def select_index(self, index):
		s_flat = self.all_values()
		flat_index = StructuredArray.flat_index_for_coordinate(index, self.get_shape())
		return s_flat[flat_index] if 0 <= flat_index < len(s_flat) else ''

	def select_indices(self, indices):
		return self.build([self.select_index(i) for i in indices.all_values()])

	def select_string(self, string):
		indices = self.all_values()
		return ''.join([string[i] for i in indices if 0 <= i < len(string)])

	def group(self, obj):
		if isinstance(obj, Array):
			target = obj.all_values()
		elif type(obj) is str:
			target = obj
		else:
			raise ValueError("Incompatible type for group", type(obj))
		groups = self.unique_values()
		if type(obj) is str:
			group_struc = [''.join([v for s, v in zip(self.all_values(), target) if s == g]) for g in groups]
		else:
			group_struc = [[v for s, v in zip(self.all_values(), target) if s == g] for g in groups]
		return StructuredArray(group_struc)


	def partition(self, obj):
		ranges = StructuredArray.make_ranges(self.all_values())
		return StructuredArray(StructuredArray.select_ranges(obj, ranges))

	def classify(self):
		shape = self.get_shape()
		classification = []
		for u in self.unique_values():
			group_indices = []
			for i, v in enumerate(self.all_values()):
				if v == u:
					if len(shape) == 1:
						group_indices.append(i)
					else:
						group_indices.append(StructuredArray.coordinates_for_flat_index(i, shape))
			classification.append(group_indices)
		return StructuredArray(classification)

	def member(self, from_array, method='all'):
		if not isinstance(from_array, Array) and not Array.container(from_array):
			target = [from_array]
			return_type = 'value'
		elif Array.container(from_array):
			target = from_array
			return_type = 'value' if len(from_array) > 1 else 'array'
		else:
			target = from_array.unique_values()
			return_type = 'array'
		values = self.all_values()
		if method == 'all':
			result = all([v in target for v in values])
		elif method == 'bool':
			return_type = 'array'
			bool_array = [v in target for v in values]
			result = StructuredArray.shape_structured(bool_array, self.get_shape())
		elif method == 'indices':
			flat_indices = [i for i, v in enumerate(values) if v in target]
			shape = self.get_shape()
			result = []
			for i in flat_indices:
				coordinate = StructuredArray.coordinates_for_flat_index(i, self.get_shape())
				if len(coordinate) == 1 or len(shape) == 1:
					result.append(coordinate[0])
				else:
					result.append(coordinate)
		else:
			raise ValueError("method " + method + " not valid")
		if return_type == 'array':
			return self.build(result)
		else:
			result = StructuredArray.flatten_structured(result)
			if len(result) > 0:
				return result[0]
			else:
				return None

	def window(self, window_size, reduce_fn, edges=False):
		shape = self.get_shape()

		window_shape = [window_size for _ in shape]
		window_relative = [win_rel_coord for win_rel_coord in StructuredArray.all_indices(window_shape)]
		valid_coordinates = [array_coord for array_coord in StructuredArray.all_indices(shape)]

		all_values = self.all_values()

		new_values = []
		for index in valid_coordinates:
			window_corner = [c - (w - 1) // 2 for c, w in zip(index, window_shape)]
			window_coordinates = [tuple([c + w for c, w in zip(window_corner, window_relative_coord)]) for window_relative_coord in window_relative]
			if not edges and all([w in valid_coordinates for w in window_coordinates]):
				values = [all_values[StructuredArray.flat_index_for_coordinate(c, shape)] for c in window_coordinates]
				new_values.append(StructuredArray.reduce_struc(values, reduce_fn)[-1])
			elif edges:
				valid_window_coordinates = [w for w in window_coordinates if w in valid_coordinates]
				values = [all_values[StructuredArray.flat_index_for_coordinate(c, shape)] for c in valid_window_coordinates]
				if len(values) == 0:
					new_values.append(self.default)
				else:
					new_values.append(StructuredArray.reduce_struc(values, reduce_fn)[-1])
			else:
				pass
		if self.is_structured():
			if not edges:
				new_shape = [s - w + 1 for w, s in zip(window_shape, shape) if s - w + 1 > 0]
			else:
				new_shape = shape
			return self.build(new_values).reshape(new_shape)
		else:
			return self.build(new_values)

	def choose_slice_on_axis(self, n, axis):
		if axis < 0: axis = len(self.get_shape()) + axis
		if axis == 0:
			return self.build(self.structured_values()[n])
		else:
			return self.build(StructuredArray.promote_axis(self.structured_values(), axis)[n])

	# Selection indices / boolean mask conversions

	def bool_mask_from_indices(self, template):
		mask_template = []
		if type(template) is int:
			mask_template = [0] * template
		elif type(template) is list:
			mask_template = StructuredArray.map_struc(template, lambda x: 0)
		elif isinstance(template, Array):
			mask_template = StructuredArray.map_struc(template.structured_values(), lambda x: 0)
		else:
			ValueError("Boolean mask template type not usable", type(template))
		template_shape = StructuredArray.shape_of_structured(mask_template)
		bool_mask = StructuredArray.indices_to_bool([StructuredArray.index_value(i) for i in self.structured_values()], template_shape)
		if isinstance(template, Array):
			return template.build(bool_mask).reshape(template_shape)
		elif Array.number(template):
			return FlatList((bool_mask + [self.default] * int(template))[:template])
		else:
			return StructuredArray(bool_mask).reshape(template_shape)

	def indices_from_bool_mask(self):
		indices = StructuredArray.bool_to_indices(self.structured_values())
		if all([type(i) is int for i in indices]):
			return FlatList([i for i in indices])
		elif all([(type(i) is list and len(i) == 1) for i in indices]):
			return FlatList([i[0] for i in indices])
		else:
			return FlatList([Coordinate(i) for i in indices])

	def first_index_from_bool_mask(self):
		index = StructuredArray.first_index(self.structured_values())
		if index == '':
			return ''
		elif type(index) is int:
			return index
		elif type(index) is list and len(index) == 0:
			return index[0]
		elif isinstance(index, Coordinate) and len(index.values) == 1:
			return index.values[0]
		else:
			return Coordinate(index) if index != '' else ''

	# Higher level functions - return a new array or structure

	def filter(self, fn):
		if isinstance(self, FlatList):
			return self.build([x for x in self.iterable() if fn(x)])
		elif isinstance(self, StructuredArray) and len(self.shape) < 2:
			return self.build([x for x in self.values if fn(x)])
		elif isinstance(self, StructuredArray):
			return self.build([x for x in self.values if fn(StructuredArray(x))])
		else:
			return self.build([x for x in self.iterable() if (fn(FlatList(x)) if Array.container(x) else fn(x))])

	def reduce(self, fn, axis, reverse=False, partial_sums=False):
		if not self.is_structured():
			return FlatList.flat_reduce(self.all_values(), fn, reverse, partial_sums)

		shape = self.get_shape()
		if axis < 0: axis = len(shape) + axis
		if self.is_structured():
			s_struc = StructuredArray.promote_axis(self.structured_values(), axis)
		else:
			s_struc = self.iterable()
		if len(shape) > 1 and self.is_structured():
			s_struc = [self.build(s) for s in s_struc]
		if reverse:
			new_array = StructuredArray.reduce_struc_r(s_struc, fn)
		else:
			new_array = StructuredArray.reduce_struc(s_struc, fn)
		if not Array.container(new_array):
			return new_array
		elif partial_sums:
			return self.build(new_array)
		elif not reverse and not Array.container(new_array[-1]):
			return new_array[-1]
		elif reverse and not Array.container(new_array[0]):
			return new_array[0]
		elif not reverse:
			return self.build(new_array[-1])
		else:
			return self.build(new_array[0])

	def reduce_all(self, fn, reverse=False, partial_sums=False):
		return FlatList.flat_reduce(self.all_values(), fn, reverse, partial_sums)

	def map(self, fn):
		if self.is_structured():
			return self.build(StructuredArray.map_struc(self.structured_values(), fn))
		else:
			return self.build([fn(x) for x in self.iterable()])

	def map_on_axis(self, fn, axis=-1):
		if self.is_structured():
			struc = self.structured_values()
		elif all([isinstance(x, Array) for x in self.values]):
			struc = [x.structured_values() for x in self.values]
		else:
			struc = self.structured_values()
		if axis < 0: axis = len(self.get_shape()) + axis
		if axis != 0:
			struc = StructuredArray.promote_axis(struc, axis)
		result_struc = []
		for x in struc:
			row_val = fn(self.build(x))
			if isinstance(row_val, Array):
				row_val = row_val.structured_values()
			result_struc.append(row_val)
		if self.is_structured():
			return self.build(result_struc)
		else:
			return self.build(result_struc)

	# Array as a set methods

	def set_exclude(self, other):
		self_flat = self.iterable()
		other_all = set(other.iterable())
		new_flat = [x for x in self_flat if x not in other_all and x != '']
		return FlatList(new_flat)

	def set_intersection(self, other):
		self_flat = self.iterable()
		other_all = set(other.iterable())
		new_flat = [x for x in self_flat if x in other_all]
		return FlatList(new_flat)

	def set_union(self, other):
		if not isinstance(other, Array):
			other_flat = [other]
		else:
			other_flat = other.iterable()
		self_flat = self.iterable()
		other_extra = list(set(other_flat) - set(self_flat))
		new_flat = self_flat + other_extra
		return FlatList(new_flat)

	def set_unique(self):
		return FlatList(self.unique_values())

	def pop(self):
		self_flat = self.iterable()
		if len(self_flat) > 0:
			first, rest = self_flat[0], self_flat[1:]
			self.mutate(rest)
			return first
		else:
			return ''

	def add_value(self, obj):
		self_flat = self.iterable()
		if obj not in self_flat:
			return self.mutate(self_flat + [obj])
		else:
			return self

	# Binary array product methods

	def bi_map(self, other, fn):
		if self.is_structured():
			return self.build(StructuredArray.bi_map_struc(self.structured_values(), other.structured_values(), fn))
		else:
			return self.build(StructuredArray.bi_map_struc(self.iterable(), other.iterable(), fn))

	def inner_product(self, other, reduce_fn, combine_fn):
		result = []
		s_struc = self.structured_values()
		o_struc = other.structured_values()
		s_shape = self.get_shape()
		o_shape = other.get_shape()
		if len(s_shape) == 1 and len(o_shape) == 1:
			combined = [combine_fn(x, y) for x, y in zip(s_struc, o_struc)]
			if len(combined) > 1:
				reduced = reduce(reduce_fn, combined[1:], combined[0])
			else:
				reduced = combined
			return reduced
		else:
			for s in StructuredArray.promote_axis(s_struc, 0):
				row = []
				for o in StructuredArray.promote_axis(o_struc, -1):
					combined = StructuredArray.bi_map_struc(s, o, combine_fn)
					reduced = StructuredArray.reduce_struc(combined, reduce_fn)[-1]
					row.append(reduced)
				result.append(row)
			return self.build(result)

	def outer_product(self, other, combine_fn):
		result = []
		rows = self.iterable()
		cols = other.iterable()
		return StructuredArray([[combine_fn(x, y) for y in cols] for x in rows])

	# String Functions

	def stringify(self, code_points=False):
		if code_points and all([type(i) is int for i in self.all_values()]):
			return ''.join([chr(int(i)) for i in self.all_values() if i not in ('', None, 0)])
		else:
			return ''.join([str(x) for x in self.all_values()])


class FlatList(Array):
	def __init__(self, values, default=0):

		super(FlatList, self).__init__()

		self.values = values
		self.default = default


	# Required implementations

	def get_shape(self):
		return len(self.values),

	def is_structured(self):
		return False

	def iterable(self):
		return self.values

	def structured_values(self):
		return self.values

	def all_values(self):
		return self.values

	def mutate(self, structured_values):
		self.values = structured_values
		return self

	def build(self, structured_values):
		return FlatList(StructuredArray.flatten_structured(structured_values))

	# Specific to this sub-class

	def slice(self, slice_obj):
		return self.build(self.values[slice_obj.start_value:slice_obj.stop_value:slice_obj.step_value])


	@classmethod
	def pair(cls, a, b):
		"""Create a list by pairing up values or appending them to a list"""
		new_values = (a.values if isinstance(a, Array) else [a]) + (
			b.values if isinstance(b, Array) else [b])
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

	@classmethod
	def primes_up_to(cls, maximum):
		sieve = np.ones(maximum+1, dtype=bool)
		sieve[0] = sieve[1] = False
		factor_limit = isqrt(maximum)
		prime = 2
		while prime <= factor_limit:
			while not sieve[prime]: prime += 1
			sieve[prime * prime::prime] = False
			prime += 1
		return cls([i for i, p in enumerate(sieve) if p])

	@classmethod
	def primes_nth_list(cls, array):
		all_n = array.all_values()
		max_n = max(*all_n) if len(all_n) > 2 else all_n[0]
		expected_maximum = int(100 + max_n * np.log2(max_n))
		primes = FlatList([2])
		while len(primes.values) < max_n:
			primes = FlatList.primes_up_to(expected_maximum)
			expected_maximum *= 2
		prime_values = [primes.values[i-1] for i in all_n]
		return cls(prime_values)

	@classmethod
	def prime_factors(cls, x):
		def prime_factors(n):
			for i in chain([2], count(3, 2)):
				if n <= 1:
					break
				while n % i == 0:
					n //= i
					yield i
		return cls(list(prime_factors(x)))

	@staticmethod
	def flat_reduce(values, fn, reverse, partial_sums):
		if len(values) < 2:
			accumulated = [values[0]]
		elif reverse:
			accumulated = FlatList.flat_reduce_r(values, fn)
		else:
			accumulated = []
			acc = values[0]
			accumulated.append(acc)
			for v in values[1:]:
				acc = fn(acc, v)
				accumulated.append(acc)
		if partial_sums:
			return StructuredArray(accumulated)
		elif len(accumulated) == 0:
			return 0
		elif reverse:
			return accumulated[0]
		else:
			return accumulated[-1]

	@staticmethod
	def flat_reduce_r(values, fn):
		if len(values) < 2:
			return values
		next_acc = FlatList.flat_reduce_r(values[1:], fn)
		return [fn(values[0], next_acc[0])] + next_acc


	def split(self, obj):
		values = self.all_values()
		if isinstance(obj, Array):
			ranges = StructuredArray.make_ranges([not x for x in StructuredArray.find_sequence_bool(values, obj.all_values())])
		else:
			ranges = StructuredArray.make_ranges([x != obj for x in values])
		return FlatList([FlatList(x) for x in StructuredArray.select_ranges(values, ranges)])


	# Method overrides

	def sort(self, reverse):
		values = [x for x in self.all_values() if x != '']
		return self.build(sorted(values, reverse=reverse))

	def __repr__(self):
		return '<FlatList | ' + ' | '.join([str(s) for s in self.values]) + ' | >'


class StructuredArray(Array):
	def __init__(self, structured_values, default=0):
		super(StructuredArray, self).__init__()

		self.values = structured_values
		self.shape = StructuredArray.shape_of_structured(structured_values)
		self.default = default

	# Required implementations

	def get_shape(self):
		return self.shape

	def is_structured(self):
		return True

	def structured_values(self):
		return self.values

	def iterable(self):
		return StructuredArray.flatten_structured(self.values)

	def all_values(self):
		return StructuredArray.flatten_structured(self.values)

	def mutate(self, structured_values):
		self.values = structured_values
		self.shape = StructuredArray.shape_of_structured(structured_values)
		return self

	def build(self, structured_values):
		return StructuredArray(structured_values, self.default)

	# Overrides of default implementation

	def reshape(self, shape):
		new_struc = StructuredArray.shape_structured([x for x in self.all_values() if x != ''], shape=shape, default=0)
		self.values = new_struc
		self.shape = shape
		self.default = 0
		return self

	def matrix_multiply(self, other):
		return self.inner_product(other, add, mul)

		# Class functions relating to structured arrays - utilities

	@staticmethod
	def flatten_structured(obj):
		if Array.container(obj):
			return sum([StructuredArray.flatten_structured(x) for x in obj], start=[])
		else:
			return [obj]

	@staticmethod
	def shape_of_structured(obj):
		if Array.container(obj) and len(obj) > 0:
			sub_shapes = sorted(tuple([StructuredArray.shape_of_structured(x) for x in obj]))
			return tuple([len(sub_shapes)] + list(sub_shapes[0]))
		else:
			return ()

	@staticmethod
	def all_indices(shape):
		if len(shape) == 1:
			for i in range(shape[0]):
				yield (i,)
		else:
			for i in range(shape[0]):
				for x in StructuredArray.all_indices(shape[1:]):
					yield tuple([i] + list(x))

	@staticmethod
	def shape_structured(values, shape, default=0):
		total_size = reduce(mul, shape, 1)
		if len(values) < total_size:
			values = values + [default] * (total_size - len(values))
		else:
			values = values

		def shape_rec(items, rec_shape):
			if len(rec_shape) == 1:
				return items
			chunk_shape = rec_shape[1:]
			chunk_size = reduce(mul, chunk_shape, 1)
			return [shape_rec(items[(i * chunk_size):((i + 1) * chunk_size)], rec_shape[1:]) for i in
					range(rec_shape[0])]

		return shape_rec(values, shape)

	@staticmethod
	def index_value(index):
		if type(index) is int:
			return index,
		elif type(index) in (float, np.float_):
			return int(index),
		elif isinstance(index, Coordinate):
			return index.values
		elif Array.container(index):
			return tuple(index)
		elif isinstance(index, Array):
			return tuple([int(x) for x in index.all_values()])
		elif type(index) is tuple:
			return index
		else:
			raise ValueError("Index type not usable", type(index))

	@staticmethod
	def flat_index_for_coordinate(coordinate, shape):
		used = (list(StructuredArray.index_value(coordinate)) + [0] * len(shape))[:len(shape)]
		offsets = list(accumulate((list(shape)[1:] + [1])[::-1], func=mul))[::-1]
		return sum([x * y for x, y in zip(used, offsets)])

	@staticmethod
	def coordinates_for_flat_index(index, shape):
		offsets = list(accumulate((list(shape)[1:] + [1])[::-1], func=mul))[::-1]

		def coord_rec(ix, sh):
			if len(sh) == 1:
				return [ix]
			else:
				chunk_number = ix // sh[0]
				chunk_index = ix % sh[0]
				remaining = coord_rec(chunk_index, sh[1:])
				return [chunk_number] + remaining

		return coord_rec(index, offsets)

	@staticmethod
	def indices_to_bool(indices_list, shape):
		size = reduce(mul, shape, 1)
		bool_array_flat = [0] * size
		for c in indices_list:
			i = StructuredArray.flat_index_for_coordinate(c, shape)
			bool_array_flat[int(i)] = 1
		bool_array = StructuredArray.shape_structured(bool_array_flat, shape, 0)
		return bool_array

	@staticmethod
	def bool_to_indices(bool_array):
		shape = StructuredArray.shape_of_structured(bool_array)
		indices = []
		for i, b in enumerate(StructuredArray.flatten_structured(bool_array)):
			if Array.truthy(b):
				index = StructuredArray.coordinates_for_flat_index(i, shape)
				if len(index) == 1:
					index = index[0]
				indices.append(index)
		return indices

	@staticmethod
	def first_index(bool_array):
		indices = StructuredArray.bool_to_indices(bool_array)
		if len(indices) == 0:
			return ''
		else:
			return indices[0]

	@staticmethod
	def permute_axes(struc, permutation=None):
		shape = StructuredArray.shape_of_structured(struc)
		size = reduce(mul, shape, 1)
		dimensions = len(shape)
		if permutation is None or len(permutation) != dimensions or sorted(permutation) != list(range(dimensions)):
			permutation = list(range(dimensions))[::-1]
		permuted_shape = [shape[i] for i in permutation]
		new_flat = [0] * size
		old_flat = StructuredArray.flatten_structured(struc)
		for i, x in enumerate(old_flat):
			old_coord = StructuredArray.coordinates_for_flat_index(i, shape)
			new_coord = [old_coord[i] for i in permutation]
			new_flat[StructuredArray.flat_index_for_coordinate(new_coord, permuted_shape)] = x
		new_struc = StructuredArray.shape_structured(new_flat, permuted_shape)
		return new_struc

	@staticmethod
	def promote_axis(struc, axis):
		if axis == 0:
			return struc
		shape = StructuredArray.shape_of_structured(struc)
		dim = len(shape)
		permutation = list(range(dim))
		permutation = [permutation[axis]] + permutation[:axis] + permutation[axis + 1:]
		return StructuredArray.permute_axes(struc, permutation)

	@staticmethod
	def map_struc(a, fn):
		def map_rec(a_struc):
			if Array.container(a_struc):
				return [map_rec(x) for x in a_struc]
			else:
				return fn(a_struc)

		return map_rec(a)

	@staticmethod
	def bi_map_struc(a, b, fn):
		def bi_rec(a_struc, b_struc):
			if Array.container(a_struc) and Array.container(b_struc):
				return [bi_rec(x, y) for x, y in zip(a_struc, b_struc)]
			elif not Array.container(a_struc) and not Array.container(b_struc):
				return fn(a_struc, b_struc)
			else:
				raise ValueError("Incompatible shapes", StructuredArray.shape_of_structured(a_struc),
								 StructuredArray.shape_of_structured(b_struc))

		return bi_rec(a, b)

	@staticmethod
	def reduce_struc(a, fn):
		if len(a) < 2: return a
		accumulated = []
		acc = a[0]
		accumulated.append(acc)
		for v in a[1:]:
			acc = StructuredArray.bi_map_struc(acc, v, fn)
			accumulated.append(acc)
		return accumulated

	@staticmethod
	def reduce_struc_r(a, fn):
		if not Array.container(a): return [a]
		if len(a) == 0: return a
		if len(a) == 1: return [a[0]]
		next_struc = StructuredArray.reduce_struc_r(a[1:], fn)
		return [StructuredArray.bi_map_struc(a[0], next_struc[0], fn)] + next_struc

	@staticmethod
	def select_ranges(obj, ranges):
		if isinstance(obj, Array):
			target = obj.all_values()
		elif Array.container(obj):
			target = obj
		elif isinstance(obj, str):
			target = obj
		else:
			raise ValueError("Incompatible type", type(obj))
		new_values = [target[b: e] for b, e in ranges]
		return new_values

	@staticmethod
	def make_ranges(values):
		range_list = []
		last = 0
		start = None
		for i, v in enumerate(values + [0]):
			if v != last or v == 0:
				if start is not None:
					range_list.append((start, i))
					start = None if v == 0 else i
				elif v != 0:
					start = i
				last = v
		return range_list

	@staticmethod
	def find_sequence_bool(sequence, sub_sequence):
		target = tuple(sub_sequence)
		target_length = len(target)
		return [tuple(sequence[i:i + target_length]) == target for i, _ in enumerate(sequence)]

	def __repr__(self):
		return "<Structured Array " + str(self.structured_values()) + '>'


class Matrix(Array):
	data_type = np.float64

	def __init__(self, structured_values, shape=None):

		super(Matrix, self).__init__()

		self.values = np.array(structured_values, dtype=Matrix.data_type)
		if shape is not None:
			self.values = self.values.reshape(shape)
		self.default = 0.

	# Required implementations

	def get_shape(self):
		return self.values.shape

	def is_structured(self):
		return True

	def structured_values(self):
		return self.values

	def iterable(self):
		return StructuredArray.flatten_structured(self.values)

	def all_values(self):
		return StructuredArray.flatten_structured(self.values)

	def mutate(self, struc):
		self.values = np.array(struc, dtype=Matrix.data_type)
		return self

	def build(self, structured_values):
		return Matrix(structured_values, None)

	# Overrides of default implementations

	def reshape(self, shape):
		all_values = self.all_values()
		used_shape = [s for s in shape if s != 0]
		if len(used_shape) == 0 and len(all_values) > 0:
			values = self.all_values()[0]
		elif len(used_shape) == 0:
			values = [self.default]
		else:
			current_size = len(all_values)
			new_size = reduce(mul, used_shape, 1)
			if new_size > current_size:
				values = all_values + [self.default] * (max(0, new_size - current_size))
			else:
				values = all_values[:new_size]
		values = np.array(values, dtype=self.data_type)
		self.values = values.reshape(used_shape)
		return self

	def join_on_axis(self, other, axis=-1):
		return self.build(np.concatenate((self.values, other.values), axis))

	def select_index(self, coordinate):
		if isinstance(coordinate, Coordinate):
			flat_index = StructuredArray.flat_index_for_coordinate(coordinate.values, self.get_shape())
		else:
			flat_index = coordinate
		return self.all_values()[flat_index]

	def select_indices(self, indices):
		return self.build([self.values[i] for i in indices.values])

	def transpose(self):
		new_matrix = Matrix(self.all_values(), self.get_shape())
		new_matrix.values.transpose()
		return Matrix(self.structured_values().transpose())

	@classmethod
	def promote_axis(cls, struc, axis):
		return np.moveaxis(struc, axis, 0)

	def return_mutated(self, new_struc):
		self.values = np.array(new_struc)
		return self

	def matrix_multiply(self, other):
		s_arr = self.structured_values()
		o_arr = other.structured_values()
		new_struc = np.matmul(s_arr, o_arr)
		return self.build(new_struc)


	# Specific to this subclass

	def matrix_binary(self, other, fn):
		s_struc = self.structured_values()
		o_struc = other.structured_values()
		s_flat = s_struc.flatten()
		o_flat = o_struc.flatten()
		r_flat = np.array([fn(s, o) for s, o in zip(s_flat, o_flat)], dtype=self.data_type)
		structured = r_flat.reshape(s_struc.shape)
		return self.build(structured)

	@classmethod
	def identity(cls, size):
		values = [1 if i == j else 0 for i in range(size) for j in range(size)]
		shape = (size, size)
		new_matrix = cls(values).reshape(shape)
		return new_matrix

	@classmethod
	def diagonal(cls, value_list):
		l = len(value_list)
		shape = [l, l]
		values = [value_list[i] if i == j else 0 for i in range(l) for j in range(l)]
		new_matrix = cls(values).reshape(shape)
		return new_matrix

	@classmethod
	def single_value_matrix(cls, value=0, shape=(1, 1)):
		return cls([value for _ in range(shape[0] * shape[1])]).reshape(shape)

	# Overridden Element-wise maths functions

	@staticmethod
	def maximum(m, n):
		"""element-wise maximum"""
		values = [max(i, j) for i, j in zip(m.all_values(), n.all_values())]
		return Matrix(values).reshape(m.get_shape())

	# Matrix Math operations

	def determinant(self):
		return np.linalg.det(self.structured_values())

	def inverse(self):
		shape = self.get_shape()
		new_matrix = np.linalg.inv(self.structured_values())
		return self.build(new_matrix)

	def __invert__(self):
		return self.inverse()

	def __repr__(self):
		return "<Matrix " + str(self.structured_values()).replace('\n', ', ') + ">"


# Coordinates are used for indexing into structured arrays
# When 1-dimensional, they generally produce integers when used

class Coordinate(Array):

	def __init__(self, coordinates):

		super(Coordinate, self).__init__()

		if type(coordinates) in (int, float, np.float_):
			self.values = (int(coordinates),)
		else:
			self.values = tuple([int(c) for c in coordinates])

	def get_shape(self):
		return len(self.values),

	def is_structured(self):
		return False

	def structured_values(self):
		return self.values

	def iterable(self):
		return list(self.values)

	def all_values(self):
		return list(self.values)

	def mutate(self, structured_list):
		self.values = StructuredArray.flatten_structured(structured_list)
		return self

	def build(self, structured_list):
		return Coordinate(StructuredArray.flatten_structured(structured_list))

	# Specific to this subclass

	def add_dimension(self, i, start=True):
		if start:
			self.values = tuple([int(i)] + list(self.values))
		else:
			self.values = tuple(list(self.values) + [int(i)])
		return self

	def __eq__(self, other):
		if isinstance(other, Coordinate):
			return self.values == other.values
		elif Array.container(other):
			return self.values == tuple(other)
		else:
			return self.values == other

	def __add__(self, other):
		return Coordinate([x + y for x, y in zip(self.values, other.values)])

	def __sub__(self, other):
		return Coordinate([x - y for x, y in zip(self.values, other.values)])

	def __mul__(self, other):
		return Coordinate([x * other for x in self.values])

	def __lt__(self, other):
		for i, j in zip(self.values, other.values):
			if i < j: return True
			if i > j: return False
		return False

	def grid_len(self):
		return sum([abs(x) for x in self.values])

	def vector_len(self):
		return sqrt(sum([x * x for x in self.values]))

	def __len__(self):
		return len(self.values)

	def __hash__(self):
		return self.values.__hash__()

	def __repr__(self):
		return '<Coordinate ' + str(self.values) + '>'
