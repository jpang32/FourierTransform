import math
import cmath
import numpy as np

## Concepts understood from video on Fast Fourier Transform at
## https://www.youtube.com/watch?v=h7apO7q16V0&t=1234s


def evaluation(coeffs, inverse=False):

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

	ye = evaluation(even_coeffs, inverse=inv)
	yo = evaluation(odd_coeffs, inverse=inv)
	
	for j in range(int(n / 2)):

		y1 = ye[j] + w * yo[j]

		y2 = ye[j] - w * yo[j]

		pts[j] = y1
		pts[j + int(n/2)] = y2

		w = w * wk

	return pts


def inverse_evaluation(pts):

	coeffs = evaluation(pts, inverse=True)

	n  = len(coeffs)

	coeffs = [int((1.0 / n) * round(item.real)) for item in coeffs]

	while(True):

		if int(coeffs[-1]) == 0 and len(coeffs) > 0:
			del coeffs[-1]
		else:
			return coeffs


def FFT(p1, p2):

	k = max(len(p1) - 1 + len(p2), len(p2) - 1 + len(p1))

	n = 1<<k.bit_length()

	p1 += [0] * (n - len(p1))
	p2 += [0] * (n - len(p2))

	p1_y = evaluation(p1)
	p2_y = evaluation(p2)

	pts = []

	for i in range(n):

		pts.append(p1_y[i] * p2_y[i])

	return inverse_evaluation(pts)


if __name__ == '__main__':

	coeffs1 = [2, 3, 1]
	coeffs2 = [1, 0, 2]

	c3 = [2, 0, 0, 0, 0, 0, 5, 7]
	c4 = [1, 7, 0, 3, 2]

	print(FFT(coeffs1, coeffs2))

	print(FFT(c3, c4))

