from tkinter import *
from frontend import Window

def main():
	window = Tk()
	window_class = Window(window)
	window.mainloop()

if __name__ == '__main__':
	main()