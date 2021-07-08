import sqlite3
import os
from xlsxwriter.workbook import Workbook
from datetime import date

class Database:


	def __init__(self, database):
		self.database = database
		self.today = date.today()
		self.display_date = self.today.strftime("%B %d, %Y")
		self.connection = sqlite3.connect(self.database)
		self.cursor = self.connection.cursor()
		self.cursor.execute("CREATE TABLE IF NOT EXISTS store (id INTEGER PRIMARY KEY, product TEXT, price INTEGER, date TEXT, quantity INTEGER)")
		self.connection.commit()


	#Adds transaction records to the data base.
	def add_product(self,product, price, quantity):
		self.cursor.execute("INSERT INTO store VALUES (NULL,?,?,?,?)", (product, price, self.display_date, quantity))
		self.connection.commit()


	#Returns all the existing data into a list of tuples.
	def	view_all(self):
		self.cursor.execute("SELECT * FROM store")
		rows = self.cursor.fetchall()
		return rows


	#Calculates the sum of all the price data. Returns the sum/profit integer.
	def get_profit(self):
		self.cursor.execute("SELECT price FROM store")
		rows = self.cursor.fetchall()
		price = [price[0] for price in rows]
		profit = 0
		for item in price:
			profit += item
		return profit


	#Deletes a product from the database through its ID.
	def delete_product(self,id):
		self.cursor.execute("DELETE FROM store WHERE id=?", (id,))
		self.connection.commit()


	#Searches the database for either the product or price. Returns the a list of tuples of data.
	def search(self,product="",price="", quantity=""):
		self.cursor.execute("SELECT * FROM store WHERE product=? OR price=? OR quantity=?", (product,price,quantity))
		rows = self.cursor.fetchall()
		return rows


	#Updates or changes an existing product through its ID.
	def update_product(self,id, product, price, quantity):
		self.cursor.execute("UPDATE store SET product=?, price=?, quantity=? WHERE id=?", (product, price, quantity, id))
		self.connection.commit()


	#Deletes all existing data in the database
	def delete_all(self):
		self.cursor.execute("DELETE FROM store;")
		self.connection.commit()


	#Exports everything to an excel file. It generates a new file if the file doesn't exists.
	def export_excel(self):
		homepath = os.path.join(os.environ["HOMEPATH"], "Desktop")
		workbook = Workbook(f'{homepath}\\store {self.display_date}.xlsx')
		worksheet = workbook.add_worksheet()
		data = self.view_all()
		for i, row in enumerate(data):
			for j, value in enumerate(row):
				worksheet.write(i, j, value)
		profit = self.get_profit()
		worksheet.write(0, 5, f"The profit is: {profit} pesos")
		workbook.close()


	#Closes the connection once the program is finished
	def __del__(self):
		self.connection.close()