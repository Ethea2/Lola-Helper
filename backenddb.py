import sqlite3
import os
from xlsxwriter.workbook import Workbook
from datetime import date

today = date.today()
display_date = today.strftime("%B %d, %Y")

def connect():
	connection = sqlite3.connect("store.db")
	cursor = connection.cursor()
	cursor.execute("CREATE TABLE IF NOT EXISTS store (id INTEGER PRIMARY KEY, product TEXT, price INTEGER, date TEXT, quantity INTEGER)")
	connection.commit()
	connection.close()


#Adds transaction records to the data base.
def add_product(product, price, quantity):
	connection = sqlite3.connect("store.db")
	cursor = connection.cursor()
	cursor.execute("INSERT INTO store VALUES (NULL,?,?,?,?)", (product, price, display_date, quantity))
	connection.commit()
	connection.close()


#Returns all the existing data into a list of tuples.
def	view_all():
	connection = sqlite3.connect("store.db")
	cursor = connection.cursor()
	cursor.execute("SELECT * FROM store")
	rows = cursor.fetchall()
	connection.close()
	return rows


#Only gets the price of all the products. Returns a list of the price data.
def get_price():
	connection = sqlite3.connect("store.db")
	cursor = connection.cursor()
	cursor.execute("SELECT price FROM store")
	rows = cursor.fetchall()
	price = [price[0] for price in rows]
	connection.close()
	return price


#Calculates the sum of all the price data. Returns the sum/profit integer.
def get_profit():
	sold_items = get_price()
	profit = 0
	for item in sold_items:
		profit += item
	return profit


#Deletes a product from the database through its ID.
def delete_product(id):
	connection = sqlite3.connect("store.db")
	cursor = connection.cursor()
	cursor.execute("DELETE FROM store WHERE id=?", (id,))
	connection.commit()
	connection.close()


#Searches the database for either the product or price. Returns the a list of tuples of data.
def search(product="",price="", quantity=""):
	connection = sqlite3.connect("store.db")
	cursor = connection.cursor()
	cursor.execute("SELECT * FROM store WHERE product=? OR price=? OR quantity=?", (product,price,quantity))
	rows = cursor.fetchall()
	connection.close()
	return rows


#Updates or changes an existing product through its ID.
def update_product(id, product, price, quantity):
	connection = sqlite3.connect("store.db")
	cursor = connection.cursor()
	cursor.execute("UPDATE store SET product=?, price=?, quantity=? WHERE id=?", (product, price, quantity, id))
	connection.commit()
	connection.close()


#Deletes all existing data in the database
def delete_all():
	connection = sqlite3.connect("store.db")
	cursor = connection.cursor()
	cursor.execute("DELETE FROM store;")
	connection.commit()
	connection.close()


#Exports everything to an excel file. It generates a new file if the file doesn't exists.
def export_excel():
	homepath = os.path.join(os.environ["HOMEPATH"], "Desktop")
	workbook = Workbook(f'{homepath}\\store {display_date}.xlsx')
	worksheet = workbook.add_worksheet()
	data = view_all()
	for i, row in enumerate(data):
		for j, value in enumerate(row):
			worksheet.write(i, j, value)
	workbook.close()


connect()