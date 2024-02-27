# FBl337
# Programming Code Golf Language
# Created: 21 February 2024
# Version: 21 February 2024 12:00PM
# Copyright: James Leibert 2024
# Licence: Available for use under the GPL3 Licence https://www.gnu.org/licenses/gpl-3.0.txt

# fb1337.py
# Module contains various functions for running programs


from time import perf_counter_ns

from fb1337.execute import Program
from fb1337.interactive import Interactive
from fb1337.syntax import SyntaxTree
from fb1337.type_utilities import parse_program_parameter


def _strip_comments(commented_code):
	code_lines = [x.strip(' \n\t\r') for x in commented_code.split('\n')]
	code_lines = [line.split('\t')[0] for line in code_lines if len(line.split('\t')[0]) > 0]
	code = ''.join(code_lines)
	return code


def _create_parameter_list(name, parameters):
	return [name] + [parse_program_parameter(parameter) for parameter in parameters]


def run(commented_code, parameters=list(), name=None, path=None):
	"""Run an fb1337 program in quiet mode.
	Outputs contents of the stack at the end of the program (as a list if more than one item).
	Parameters provided as a list/tuple of integers are assumed to be Lists; as a list/tuple of floats as a Matrix
	integers and strings are imported as integers and strings
	for a null parameter, use an empty string
	If no name is provided, the default files for input and output are f.in and f.out"""
	tree = SyntaxTree(commented_code)
	program_parameters = _create_parameter_list(name, parameters)
	program = Program(tree, program_parameters)

	result = program.run(path=path)
	return result


def run_annotated(commented_code, parameters=list(), name=None, title=None, expected=list(), path=None):
	"""Run an fb1337 program in annotated mode.
	Outputs contents of the stack at the end of the program (as a list if more than one item).
	Parameters provided as a list/tuple of integers are assumed to be Lists; as a list/tuple of floats as a Matrix
	integers and strings are imported as integers and strings
	for a null parameter, use an empty string
	If no name is provided, the default files for input and output are f.in and f.ou
	Additional information on the program and its execution as well as a listing of its syntax tree and comments are printed."""
	# Print program information
	tree = SyntaxTree(commented_code)
	program_parameters = _create_parameter_list(name, parameters)
	program = Program(tree, program_parameters)

	code = _strip_comments(commented_code)

	print(title)
	print()
	tree.pretty_print()
	print()
	print(code, 'length', len(code))
	print('parameters', program_parameters)
	print()

	start_time = perf_counter_ns()
	result = program.run(path=path)
	end_time = perf_counter_ns()

	print('run time', round((end_time - start_time) / 1000000, 2), "ms")
	print()
	print('result', result)
	if result == expected or expected is None or expected == []:
		print('ok')
	else:
		print('expected', expected)
	print()

	return result


def run_interactive(commented_code, parameters=list(), name=None, path=None):
	"""Run a program in interactive debugging mode
	The user can step through the program, set breakpoints and interact with the stack
	The current stack, environment stack and namespace are visible as well as details of each command"""
	program_parameters = _create_parameter_list(name, parameters)
	interactive_debugger = Interactive(commented_code=commented_code, program_parameters=program_parameters, path=path)
	interactive_debugger.start()


def test(test_suite, verbose=False, path=None):
	"""Run a complete test suite. The test suite should consist of a dictionary of examples, indexed by name
	Each entry provides a dictionary containing the following keys:
	- code: the fb1337 program which may contain comments
	- parameters: the program parameters
	- result: the expected result as a list of values expected to be on the stack on completion (from bottom to top)
	"""
	if path is not None:
		file_path = path
	else:
		file_path = __file__
	failures = []
	for i, test_info in enumerate(test_suite):
		code = test_info['code']
		parameters = test_info['parameters']
		name = test_info['name']
		expected = test_info['result']
		start_time, end_time, result = None, None, None
		try:
			start_time = perf_counter_ns()
			result = run(code, parameters, name=name, path=file_path)
			end_time = perf_counter_ns()

			if expected != result:
				failures.append((i, name, result, expected))
		except Exception as e:
			failures.append((i, name, "Error: " + "'" + str(e) + "'", expected))
		if verbose:
			print(i + 1, name, (parameters if len(parameters) > 0 else ''), '"' + str(code) + '" length',
			      len(_strip_comments(code)))
			if end_time is not None:
				print('run time', round((end_time - start_time) / 1000000, 2), "ms")
			print('result', result)
			if result == expected:
				print('ok')
			else:
				print('expected', expected)
			print("-----")
			print()
	print('Tests:', len(test_suite) - len(failures), 'of', len(test_suite), 'ok')
	if len(failures) > 0:
		print("Failed:")
		for i, name, result, expected in failures:
			print(i + 1, name, 'result', result, 'expected', expected)

def interactive_from_test_suite(test_suite, name, path=None):
	if path is None: path = __file__
	for t in test_suite:
		if t['name'] == name:
			Interactive(t['code'], [name] + t['parameters'], path).start()
			return

