import tkinter as tk
from gui import RecursiveDiagram 

if __name__ == "__main__":

	c3 = [2, 0, 0, 0, 0, 0, 5, 7]
	c4 = [1, 7, 0, 3, 2]

	root = tk.Tk()
	root.title('Recursive Diagram')
	root.geometry('600x600')
	root.rowconfigure(0, weight=1)
	root.columnconfigure(0, weight=1)
	rd = RecursiveDiagram(root)
	rd.fft(c3, c4)
	rd.tree.grid(row=0, column=0, sticky='nsew')

	# what does this do?
	root.mainloop()