import tkinter as tk
from tkinter import ttk

class RecursiveDiagram(tk.Frame):

	def __init__(self, parent, *args, **kwargs):
		super().__init__(parent, *args, **kwargs)
		self.parent = parent
		self.tree = ttk.Treeview(parent)
		self.tree.heading('#0', text="Recursive Diagram". anchor="w")


	# Need to make it so that when evaluate runs, it adds 
	def populate(p1, p2):





