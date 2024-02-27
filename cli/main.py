# FBl337
# Programming Code Golf Language
# Created: 21 February 2024
# Version: 21 February 2024 12:00PM
# Copyright: James Leibert 2024
# Licence: Available for use under the GPL3 Licence https://www.gnu.org/licenses/gpl-3.0.txt

# __main__.py
# Command Line Interpreter


import os
import sys

from fb1337.fb1337 import run, run_annotated, run_interactive, test

sys.setrecursionlimit(10000)

if __name__ == "__main__":

	arguments = sys.argv[1:]

	if arguments[0] in ('-h', '-H', '?', 'help', '-help'):
		print("fb1337 a Programming Golf Language")
		print("version 1.0")
		print("Usage:")
		print("fb1337 -h                print this help information")
		print("fb1337 -t [name]         perform examples in a test file")
		print("                         Rows should contain: ")
		print("                             [name] in text")
		print("                             [program] as a python string")
		print("                             [parameters] as a python list")
		print("                             [result] as a python list")
		print("fb1337 (-d)(-i) (-c [code] | [filename]) ([parameter ...])")
		print("                         -d provide program annotations")
		print("                         -i run in interactive mode")
		print("                         -c provide program code as a python string")

	elif arguments[0] == '-t':
		# Run a test suite from a file
		program_name = arguments[2]
		test_suite = dict()
		with open(program_name, 'r') as file:
			if file is None:
				print("File not found", program_name)
				exit()
			tests = file.readlines()
			for test in tests:
				items = test.split(' ')
				items = [t.strip("/n/r/t ") for t in items]
				if len(items) > 2:
					test_suite[items[0]] = {'code': items[1], 'parameters': items[2], 'expected': items[3]}
				else:
					print("test_suite not in correct format")
					exit()
			test(test_suite)

	else:
		# Run a program

		debug = False
		interactive = False
		program = None
		name: str = None
		parameters = []

		# Parse options and parameters
		while len(arguments) > 0:
			arg, arguments = arguments[0], arguments[1:]
			if len(arg) > 1 and arg[0] == '-':
				# options
				option = arg[1:]
				if option == 'd':
					# Run in annotated mode
					debug = True
				elif option == 'i':
					# Run in interactive mode
					interactive = True
				elif option == 'c' and len(arguments) > 0:
					# Run a program directly from the command line
					program, arguments = arguments[0], arguments[1:]
					name = None
			else:
				if program is None:
					# If we receive a filename before getting a -c argument, we read the code from a file
					if not os.path.isfile(arg):
						print('File not found', arg)
						exit()
					else:
						with open(arg, 'r') as file:
							program = file.read()
							name = arg
				else:
					# Any other non-option values are assumed to be arguments
					parameters.append(arg)

		if not debug and not interactive:
			# Run in quiet mode
			result = run(commented_code=program, parameters=parameters, name=name)
		elif not interactive:
			# Run in annotated mode
			result = run_annotated(commented_code=program, parameters=parameters, name=name, title=name, expected=None)
		else:
			# Run in interactive mode
			result = run_interactive(commented_code=program, parameters=parameters)
		print(result)
