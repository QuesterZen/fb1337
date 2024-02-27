# FBl337
# Programming Code Golf Language
# Created: 21 February 2024
# Version: 21 February 2024 12:00PM
# Copyright: James Leibert 2024
# Licence: Available for use under the GPL3 Licence https://www.gnu.org/licenses/gpl-3.0.txt

# matrix.py
# Matrix array subclass definition


import numpy as np

from fb1337.array import MatrixArray


class Matrix(MatrixArray):
	"""Matrix class consists of a 2D array of floats"""

	def __init__(self, structured_values):
		MatrixArray.__init__(self, structured_values)

	# Create new matrices

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
		if len(shape) != 2 or shape[0] != shape[1]:
			raise ValueError('Matrix is not square ' + str(shape))
		new_matrix = np.linalg.inv(self.structured_values())
		return Matrix(new_matrix)

	def __invert__(self):
		return self.inverse()

	def matrix_multiply(self, other):
		s_arr = self.structured_values()
		o_arr = other.structured_values()
		new_struc = np.matmul(s_arr, o_arr)
		return self.build(new_struc)

	def eigen_matrices(self):
		eigenvalues, eigenvectors = np.linalg.eig(self.structured_values())
		eigenvalue_matrix = Matrix.diagonal(list(eigenvalues.flatten()))
		eigenvector_matrix = Matrix(eigenvectors)
		return eigenvalue_matrix, eigenvector_matrix

	# Array Overrides

	def build(self, structured_values):
		return Matrix(structured_values)

	# All types

	def __repr__(self):
		flat_rep = str(self.values).replace('\n', ', ')
		return '<Matrix ' + flat_rep + '>'
