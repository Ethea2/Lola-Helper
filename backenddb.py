import sqlite3
from xlsxwriter.workbook import Workbook
from datetime import date

today = date.today()
display_date = today.strftime("%B %d, %Y")

def connect():
	connection = sqlite3.connect("store.db")
	cursor = connection.cursor()
	cursor.execute("CREATE TABLE IF NOT EXISTS store (id INTEGER PRIMARY KEY, product TEXT, price INTEGER, date TEXT)")
	connection.commit()
	connection.close()


def add_product(product, price):
	connection = sqlite3.connect("store.db")
	cursor = connection.cursor()
	cursor.execute("INSERT INTO store VALUES (NULL,?,?,?)", (product, price, display_date))
	connection.commit()
	connection.close()


def	view_all():
	connection = sqlite3.connect("store.db")
	cursor = connection.cursor()
	cursor.execute("SELECT * FROM store")
	rows = cursor.fetchall()
	connection.close()
	return rows


def get_price():
	connection = sqlite3.connect("store.db")
	cursor = connection.cursor()
	cursor.execute("SELECT price FROM store")
	rows = cursor.fetchall()
	price = [price[0] for price in rows]
	connection.close()
	return price


def get_profit():
	sold_items = get_price()
	profit = 0
	for item in sold_items:
		profit += item
	return profit


def delete_product(id):
	connection = sqlite3.connect("store.db")
	cursor = connection.cursor()
	cursor.execute("DELETE FROM store WHERE id=?", (id,))
	connection.commit()
	connection.close()


def search(product="",price=""):
	connection = sqlite3.connect("store.db")
	cursor = connection.cursor()
	cursor.execute("SELECT * FROM store WHERE product=? OR price=?", (product,price))
	rows = cursor.fetchall()
	connection.close()
	return rows


def update_product(id, product, price):
	connection = sqlite3.connect("store.db")
	cursor = connection.cursor()
	cursor.execute("UPDATE store SET product=?, price=? WHERE id=?", (product, price, id))
	connection.commit()
	connection.close()


def delete_all():
	connection = sqlite3.connect("store.db")
	cursor = connection.cursor()
	cursor.execute("DELETE FROM store;")
	connection.commit()
	connection.close()

def export_excel():
	workbook = Workbook(f'store {display_date}.xlsx')
	worksheet = workbook.add_worksheet()
	data = view_all()
	for i, row in enumerate(data):
		for j, value in enumerate(row):
			worksheet.write(i, j, value)
	workbook.close()


connect()
#insert_product("Lucky Me", 30)
#delete_product()
#update_product(1, 'Lays', 40)
#print(search(price=20))
#export_excel()
#print(get_profit())