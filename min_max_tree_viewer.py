import tkinter as tk


class MinMaxTreeViewer:
	def __init__(self, mmt):
		self.mmt = mmt
		self.root = tk.Tk()
		self.root.geometry('800x600')

	def view(self):
		a = tk.Label(self.root, text='asdf')
		a.grid()
		self.root.mainloop()
