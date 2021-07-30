import tkinter as tk
from gui import RecursiveDiagram 

if __name__ == "__main__":

	c3 = [2, 0, 0, 0, 0, 0, 5, 7]
	c4 = [1, 7, 0, 3, 2]

	root = tk.Tk()
	RecursiveDiagram(root)

	# what does this do?
	root.mainloop()