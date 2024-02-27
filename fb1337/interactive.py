# FBl337
# Programming Code Golf Language
# Created: 21 February 2024
# Version: 21 February 2024 12:00PM
# Copyright: James Leibert 2024
# Licence: Available for use under the GPL3 Licence https://www.gnu.org/licenses/gpl-3.0.txt

# interactive.py
# Interactive debugger for the fb1337 interpreter


from PyQt5.Qt import QFont
from PyQt5.QtCore import QSize
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMainWindow, QApplication, QVBoxLayout, QHBoxLayout, QWidget, QPlainTextEdit, QPushButton, \
	QInputDialog, QMessageBox

from fb1337.execute import Program
from fb1337.syntax import SyntaxTree


class NotifyWindow(QMainWindow):

	def __init__(self):
		super().__init__()

		self.app = None
		self.debugger = None

		self.env = None
		self.info_dictionary = None

		self.code_area = None
		self.notify_area = None
		self.stack_area = None
		self.env_area = None

		self.set_up_window()

	def set_up_window(self):

		self.setWindowTitle("fb1337 Interactive Mode")

		code_area = QPlainTextEdit()
		code_area.setReadOnly(True)
		code_area.setLineWrapMode(QPlainTextEdit.NoWrap)
		code_area.setFont(QFont('Courier New'))
		self.code_area = code_area

		notify_area = QPlainTextEdit()
		notify_area.setReadOnly(True)
		notify_area.setLineWrapMode(QPlainTextEdit.NoWrap)
		self.notify_area = notify_area

		stack_area = QPlainTextEdit()
		stack_area.setReadOnly(True)
		stack_area.setLineWrapMode(QPlainTextEdit.NoWrap)
		self.stack_area = stack_area

		env_area = QPlainTextEdit()
		env_area.setReadOnly(True)
		env_area.setLineWrapMode(QPlainTextEdit.NoWrap)
		self.env_area = env_area

		next_button = QPushButton("Next")
		next_button.clicked.connect(self.next)

		go_button = QPushButton("Go")
		go_button.clicked.connect(self.go)

		quit_button = QPushButton("Quit")
		quit_button.clicked.connect(self.quit)

		breakpoint_button = QPushButton("Set Breakpoint")
		breakpoint_button.clicked.connect(self.set_breakpoint)

		clear_button = QPushButton("Clear Breakpoints")
		clear_button.clicked.connect(self.clear_breakpoints)

		execute_button = QPushButton("Execute Code")
		execute_button.clicked.connect(self.execute_code)

		layout1 = QVBoxLayout()
		layout1.addWidget(code_area)

		layout2 = QHBoxLayout()
		layout3 = QVBoxLayout()
		layout3.addWidget(notify_area)
		layout3.addWidget(env_area)
		layout2.addLayout(layout3)
		layout2.addWidget(stack_area)
		layout1.addLayout(layout2)
		layout4 = QHBoxLayout()
		layout4.addWidget(next_button)
		layout4.addWidget(go_button)
		layout4.addWidget(breakpoint_button)
		layout4.addWidget(clear_button)
		layout4.addWidget(execute_button)
		layout4.addWidget(quit_button)
		layout1.addLayout(layout4)

		container = QWidget()
		container.setLayout(layout1)
		self.setCentralWidget(container)

	def update(self, env, info_dictionary):
		"""Display the notification information in the window"""

		# Store the information provided so we can update the window again after taking action
		self.env = env
		self.info_dictionary = info_dictionary

		# Code Window Text
		line_length = 50
		token_list = []
		location = 0
		for token in self.debugger.tree.tokens:
			v = str(token.value) if token.value != '' else 'Ø'
			token_list.append((location, v, token.index))
			location += len(v)
		remaining = token_list
		token_lines = []
		while len(remaining) > 0:
			remaining, token_lines = remaining[line_length:], token_lines + [remaining[:line_length]]
		code_text = ''
		for token_line in token_lines:
			tens, units, breakpoints, code, position = '', '', '', '', ''
			for (l, v, i) in token_line:
				tens += (str((i // 10) % 10) if (i % 10 == 0) else ' ') + ' ' * len(v)
				units += str(i % 10) + ' ' * len(v)
				breakpoints += ('B' if i in self.debugger.breakpoints else ' ') + ' ' * len(v)
				code += v + ' '
				position += ('^' if i == info_dictionary['token'].index else ' ') + ' ' * len(v)
			code_text += tens + '\n' + units + '\n' + (
				(breakpoints + '\n') if 'B' in breakpoints else '') + code + '\n' + position + '\n'
		if len(info_dictionary['token'].comments) > 0:
			code_text += '\n# ' + info_dictionary['token'].comments + '\n'

		self.code_area.setPlainText(code_text)

		# Current Token Notification Text
		notify_text = 'Current Token\n'
		if 'symbol' in info_dictionary:
			notify_text += str(info_dictionary['symbol']) + ' ' + str(info_dictionary['alias']) + ' ' + str(
				info_dictionary['signature']) + '\n'
			notify_text += str(info_dictionary['description']) + '\n\n'
			parameters = info_dictionary['s-params'] + info_dictionary['c-params'] + info_dictionary['f-params'] + \
			             info_dictionary['b-params']
			parameter_list = '\n'.join([(str(p) if p != '' else 'Ø') + ": " + str(t) for p, t in
			                            zip(parameters, info_dictionary['type signature'])])
			notify_text += "Parameters\n" + parameter_list + ('\n' if len(parameter_list) > 0 else '')
			if 'value' in info_dictionary and info_dictionary['value'] is not None:
				notify_text += '\nValue ' + str(info_dictionary['value']) + '\n'
		else:
			notify_text += str(info_dictionary['token'].value) + '\n'
		self.notify_area.setPlainText(notify_text)

		# Stack Text
		if env is not None:
			stack_text = "Stack\n"
			for i, s in enumerate(env.get_stack()[::-1]):
				stack_text += str(len(env.get_stack()) - i - 1) + ': ' + str(s) + '\n'
			self.stack_area.setPlainText(stack_text)

		# Environment and Program Argument Text
		if env is not None:
			env_stack = []
			e = env
			while e is not None:
				env_stack.append("Implicit " + (
					str(e.implicit()) if e.implicit_object is not None else '-') + "    \tNamespace " + str(
					e.namespace))
				e = e.parent
			env_text = "Environment\n" + '\n'.join(
				[str(len(env_stack) - i - 1) + ': ' + text for i, text in enumerate(env_stack)])
			env_text += '\nProgram: ' + str({i: p for i, p in enumerate(self.debugger.program.parameters)}) + '\n'
			self.env_area.setPlainText(env_text)

	# Button Actions
	def next(self):
		self.debugger.interrupt = True
		self.app.exit()

	def go(self):
		self.debugger.interrupt = False
		self.app.exit()

	# noinspection PyCallByClass
	def set_breakpoint(self):
		bp, ok = QInputDialog.getInt(self, "Breakpoint", "Location", 0, 0, self.debugger.tree.tokens[-1].index)
		if ok and bp:
			self.debugger.breakpoints.add(bp)
			self.update(self.env, self.info_dictionary)

	def clear_breakpoints(self):
		self.debugger.breakpoints = set()
		self.update(self.env, self.info_dictionary)

	# noinspection PyCallByClass
	def execute_code(self):
		code, ok = QInputDialog.getText(self, "Execute", "Code", )
		if ok and code:
			tree = SyntaxTree(code)
			self.debugger.program.eval_context(self.env, tree)
			self.update(self.env, self.info_dictionary)

	@staticmethod
	def quit():
		exit()

	# Overridden Window Methods
	def resizeEvent(self, q_resize_event):
		self.debugger.window_size = q_resize_event.size()

	def keyPressEvent(self, event):
		if event.key() == Qt.Key_Return or event.key() == Qt.Key_N:
			self.next()
		if event.key() == Qt.Key_G:
			self.go()
		if event.key() == Qt.Key_B:
			self.set_breakpoint()
		if event.key() == Qt.Key_C:
			self.clear_breakpoints()
		if event.key() == Qt.Key_X:
			self.execute_code()
		if event.key() == Qt.Key_Q:
			self.quit()


class Interactive:

	def __init__(self, commented_code, program_parameters, path=None):

		self.tree = SyntaxTree(commented_code)
		self.program = Program(self.tree, parameters=program_parameters, debugger=self, logging=False)
		self.path = path

		self.interrupt = True
		self.breakpoints = set()

		self.window = None
		self.window_size = QSize(1200, 600)

		self.exit_code = None
		self.app = None

	def start(self):
		result = self.program.run(path=self.path)
		self.complete(result)

	@staticmethod
	def complete(result):
		app = QApplication([])
		result_text = "Program Complete\n\n" + str(result)
		dlg = QMessageBox(text=result_text)
		dlg.setStandardButtons(QMessageBox.Ok)
		dlg.exec_()
		app = None
		dlg = None

	def notify(self, env, info_dictionary):
		if self.interrupt or info_dictionary['token'].index in self.breakpoints:
			app = QApplication([])
			self.window = NotifyWindow()
			self.window.app = app
			self.window.debugger = self
			if self.window_size is not None:
				self.window.resize(self.window_size)
			self.window.update(env, info_dictionary)
			self.window.show()
			self.exit_code = app.exec_()
			self.app = None
			self.window = None
