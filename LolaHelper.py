from tkinter import *
from tkinter import messagebox
from datetime import date
import backenddb as backend

#Takes the date of transaction.
today = date.today()
display_date = today.strftime("%B %d, %Y")


#Clears all the entry boxes.
def clear_boxes():
	product_box.delete(0,END)
	price_box.delete(0, END)
	quantity_box.delete(0, END)

#Selecting a row from the list_box and returns the tuple of the selected row.
def get_selected_row(event):
	global selected_row
	try:
		index = list_box.curselection()[0]
		selected_row = list_box.get(index)
		clear_boxes()
		product_box.insert(END, selected_row[1])
		price_box.insert(END, selected_row[2])
		return selected_row
	except IndexError:
		pass


#Updates the list box and displays all the data from the database in the list box.
def view_command():
	items = backend.view_all()
	list_box.delete(0, END)
	for item in items:
		list_box.insert(END, item)


#Adds a transaction data to the database
def add_command():
	backend.add_product(product_box.get(), price_box.get(), quantity_box.get())
	view_command()


#Deletes a selected row from the list and the database.
def delete_command():
	product_name_delete = product_box.get()
	delete_popup = messagebox.askquestion("Delete Product", f"Are you sure you want to delete {product_name_delete}?")
	if delete_popup == 'yes':
		backend.delete_product(selected_row[0])
		clear_boxes()
		view_command()
	else:
		pass


#Updates a selected product from the list box. The update also happens in the database.
def update_command():
	backend.update_product(selected_row[0], product_box.get(), price_box.get(), quantity_box.get())
	view_command()


#Searches for specific products by price, quantity, or name.
def search_command():
	products = backend.search(product_box.get(), price_box.get(), quantity_box.get())
	list_box.delete(0, END)
	for items in products:
		list_box.insert(END, items)


#Exports the data to an excel file.
def export_excel():
	backend.export_excel()


#Deletes everything from the database.
def clear_command():
	delete_popup = messagebox.askquestion("Delete Product", f"Are you sure you want to clear all?")
	if delete_popup == 'yes':
		backend.delete_all()
		view_command()
		clear_boxes()
	else:
		pass


#Computes the profits gained from all transactions.
def profit_command():
	profit = backend.get_profit()
	profit_box.delete(0, END)
	profit_box.insert(END, profit)


window = Tk()


#labels
name_product = StringVar()
name_product.set("Product Name")
product_name = Label(window, textvariable=name_product, height=2, width=11)
product_name.grid(row=0, column=0)

price_name = StringVar()
price_name.set("Price")
price = Label(window, textvariable=price_name, height=2, width=20)
price.grid(row=0, column=2)

date_name = StringVar()
date_name.set(f"Date:	{display_date}")
date_label = Label(window, textvariable=date_name, height=2, width=15)
date_label.grid(row=0, column=4)

quantity_name = StringVar()
quantity_name.set("Quantity: ")
quantity_label = Label(window, textvariable=quantity_name, height=2, width=10)
quantity_label.grid(row=0, column=6)

profit_name = StringVar()
profit_name.set("Profit")
profit_label = Label(window, textvariable=profit_name)
profit_label.grid(row=15, column=1)

	
#entry box
product_box = Entry(window)
product_box.grid(row=0, column=1)

price_box = Entry(window)
price_box.grid(row=0, column=3)

quantity_box = Entry(window)
quantity_box.grid(row=0, column=7)

profit_box = Entry(window)
profit_box.grid(row=15, column=2)


#listbox and scroll bar
list_box = Listbox(window, height=12, width=70)
list_box.grid(row=2,column=0,rowspan=12,columnspan=6)

scroll_bar = Scrollbar(window)
scroll_bar.grid(row=2, column=4, rowspan=7)

list_box.configure(yscrollcommand=scroll_bar.set)
scroll_bar.configure(command=list_box.yview)

list_box.bind('<<ListboxSelect>>', get_selected_row)

#buttons
view_all = Button(window, text="View All", height=1, width=20, command=view_command)
view_all.grid(row=2, column=7)

search_button = Button(window, text="Search", height=1, width=20, command=search_command)
search_button.grid(row=3, column=7)

add_button = Button(window, text="Add Entry", height=1, width=20, command=add_command)
add_button.grid(row=4, column=7)

update_button = Button(window, text="Update Selected", height=1, width=20, command=update_command)
update_button.grid(row=5, column=7)

delete_button = Button(window, text="Delete Selected", height=1, width=20, command=delete_command)
delete_button.grid(row=6, column=7)

sum_button = Button(window, text="Calculate Profit", height=1, width=20, command=profit_command)
sum_button.grid(row=7, column=7)

export_excel = Button(window, text="Export to Excel", height=1, width=20, command=export_excel)
export_excel.grid(row=8, column=7)

clear_all_button = Button(window, text="Clear All", height=1, width=20, command=clear_command)
clear_all_button.grid(row=9, column=7)


window.mainloop()