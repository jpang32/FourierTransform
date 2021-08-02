import math
import cmath
import numpy as np
import pprint
from typing import List

import tkinter as tk
from tkinter import ttk

class RecursiveDiagram(tk.Frame):

	def __init__(self, parent, *args, **kwargs):
		super().__init__(parent, *args, **kwargs)
		self.parent = parent
		self.tree = ttk.Treeview(parent)
		self.tree.heading('#0', text="Recursive Diagram", anchor="w")


	# Need to make it so that when evaluate runs, it adds function call
	def _populate(func):

		rec_level = 1
		item_id = 1

		def coeffs_to_string(coeffs):

			operations = {
				(True, True): '-',
		        (True, False): '',
		        (False, True): ' - ',
		        (False, False): ' + '
			}

			expression = []

			for power, val in enumerate(coeffs):

				if val == 0:
					continue

				op = operations[(not expression, val < 0)]

				val = abs(val)

				if val == 1 and power != 0:
					val = ''

				f = {0: '{}{}', 1: '{}{}x'}.get(power, '{}{}x^{}')

				expression.append(f.format(op, val, power))


			return ''.join(expression) or '0'


		def wrapper(self, *args, **kwargs):

			if (kwargs and kwargs['inverse']):
				return func(self, *args, **kwargs)

			nonlocal rec_level
			nonlocal item_id

			coeff_str = coeffs_to_string(args[0])

			fn_str = f"eval({coeff_str}) ({item_id})" 

			whitespace = "   " * (rec_level - 1)

			print(f"{whitespace} -> {fn_str}")

			self.tree.insert('', tk.END, iid=item_id, text=fn_str, open=True)

			item_id += 1

			rec_level += 1

			result = func(self, *args, **kwargs)

			rec_level -= 1

			return result

		return wrapper


	def _organize(func):

		def place_children(self, parent_id, k):

			if k == 1:
				return

			print(f"parent: {parent_id}")
			print(k)

			self.tree.move(parent_id + 1, parent_id, 2)
			self.tree.move(parent_id + k, parent_id, 2)

			place_children(self, parent_id + 1, (int)(k / 2.0))
			place_children(self, parent_id + k, (int)(k / 2.0))

		def wrapper(self, *args, **kwargs):

			result = func(self, *args, **kwargs)

			assert len(args[0]) == len(args[1])
			k = len(args[0])

			place_children(self, 1, k)
			#place_children(self, k, k)

			return result

		return wrapper


	@_populate
	def evaluation(self, coeffs: List[int], inverse=False) -> List[complex]:

		""" 
		Create pts that define the polynomial by finding nth roots of unity

		:param coeffs: list of coeffs [p0, p1, ..., pn] defining polynomial
		:param inverse: when true, performs inverse operation

		:return: list of complex numbers representing the polynomial
		"""

		n = 1<<(len(coeffs) - 1).bit_length()

		coeffs += [0] * (n - len(coeffs))

		pts = [None]*n

		if n == 1:
			return [coeffs[-1]]

		wk = cmath.exp(complex(0, (2 * math.pi) / n))
		inv = False

		if inverse:
			wk = cmath.exp(complex(0, (-2 * math.pi) / n)) 
			inv = True

		w = 1

		even_coeffs = coeffs[0::2]
		odd_coeffs = coeffs[1::2]

		ye = self.evaluation(even_coeffs, inverse=inv)
		yo = self.evaluation(odd_coeffs, inverse=inv)

		for j in range(int(n / 2)):

			y1 = ye[j] + w * yo[j]

			y2 = ye[j] - w * yo[j]

			pts[j] = y1
			pts[j + int(n/2)] = y2

			w = w * wk

		return pts


	def inverse_evaluation(self, pts: List[complex]) -> List[int]:

		"""
		Calls inverse operation of evaliation, then formats the output

		:param pts: list of complex numbers representing the polynomial

		:return: list of coeffs [p0, p1, ..., pn] defining polynomial
		"""

		coeffs = self.evaluation(pts, inverse=True)

		n  = len(coeffs)

		coeffs = [int((1.0 / n) * round(item.real)) for item in coeffs]

		while(True):

			if int(coeffs[-1]) == 0 and len(coeffs) > 0:
				del coeffs[-1]
			else:
				return coeffs


	@_organize
	def fft(self, p1: List[int], p2: List[int]) -> List[int]:

		"""
		Perform the actuall fft using the helper functions.
		This function multiplies two polynomials in O(nlogn) time

		:param p1: list of coeffs [p0, p1, ..., pn] defining first polynomial
		:param p2: list of coeffs [p0, p1, ..., pn] defining second polynomial

		:return: list of coefficients representing the polynomial that
		results from the multiplication of p1 and p2
		"""

		k = max(len(p1) - 1 + len(p2), len(p2) - 1 + len(p1))

		n = 1<<k.bit_length()

		p1 += [0] * (n - len(p1))
		p2 += [0] * (n - len(p2))

		p1_y = self.evaluation(p1)
		p2_y = self.evaluation(p2)

		pts = []

		for i in range(n):

			pts.append(p1_y[i] * p2_y[i])

		return self.inverse_evaluation(pts)





