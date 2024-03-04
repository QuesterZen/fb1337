# FBl337
# Programming Code Golf Language
# Created: 21 February 2024
# Version: 21 February 2024 12:00PM
# Copyright: James Leibert 2024
# Licence: Available for use under the GPL3 Licence https://www.gnu.org/licenses/gpl-3.0.txt

# slice.py
# Defines a slice object, similar to a python slice

class Slice:
    """Slice objects allow you to access regularly spaced values in a list to alter all at once, or
    to create a new list. They operate similarly to Python slices"""

    DEFAULT_MAX = 1000000000

    def __init__(self, s, f, a):
        def clean_value(x):
            if type(x) is None:
                return None
            if type(x) is int:
                return x
            if type(x) is str and len(x) == 0 or x is False:
                return None
            if type(x) is str:
                try:
                    x = int(x)
                except ValueError:
                    return None
                return x
            return None

        self.start_param, self.stop_param, self.step_param = [clean_value(x) for x in [s, f, a]]

        self.start_value = self.start_param if self.start_param is not None else (
            1 if self.stop_param is None or self.stop_param > 0 else -1)
        self.stop_value = self.stop_param if self.stop_param is not None else (
            Slice.DEFAULT_MAX if self.step_param is None or self.step_param > 0 else -Slice.DEFAULT_MAX)
        self.ascending = self.stop_value > self.start_value
        self.step_value = self.step_param if self.step_param is not None else (1 if self.ascending else -1)

    def slice_string(self, string):
        return string[self.start_value:self.stop_value:self.step_value]

    def __repr__(self):
        return "<Slice [" + str(self.start_param) + ":" + str(self.stop_param) + ":" + str(self.step_param) + "]>"
