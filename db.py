#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sqlite3
from typing import List, Tuple


conn = sqlite3.connect("pizza1.db", check_same_thread=False)
cursor = conn.cursor()


# Создание таблицы
cursor.execute("""CREATE TABLE IF NOT EXISTS orders(
                tg_id INT PRIMARY KEY,
                pizza_id TEXT DEFAULT None,
                drink_name TEXT DEFAULT None,
                drink_id TEXT DEFAULT None,
                size TEXT,
                address TEXT,
                phone TEXT,
                time_ship TEXT,
                time_ship_conf TEXT,
                sum TEXT,
                status BOOL
                )""")


cursor.execute("""CREATE TABLE IF NOT EXISTS pizzes(
                id INTEGER,
                pizza_name TEXT,
                modifications TEXT,
                price TEXT
                )""")


cursor.execute("""CREATE TABLE IF NOT EXISTS drinks(
                id INTEGER,
                drink_name TEXT, 
                price TEXT
                )""")


# Добавляет юзера
def new_user(tg_id: int):
    try:
        cursor.execute(
            f"INSERT INTO orders (tg_id) VALUES ({tg_id})")
        conn.commit()
    except:
        print('Такой юзер уже есть')


# Обновляет запись
def update(column: str, value, tg_id: int):
    cursor.execute(
        f"UPDATE orders SET {column}=? WHERE tg_id={tg_id}", 
        (value,))
    conn.commit()


# Достает заказ юзера
def get_order(tg_id: int) -> Tuple:
    cursor.execute(
        f"SELECT * FROM orders WHERE tg_id={tg_id}")
    rows = cursor.fetchall()
    columns = ['tg_id', 'pizza_id', 'drink_name', 'drink_id', 'size', 'address', 'phone', 'time_ship', 'time_ship_conf', 'sum', 'status']
    dict_row = {}
    for row in rows:
        for index, column in enumerate(columns):
            dict_row[column] = row[index]
    return dict_row


# Добавляет пиццу
def insert_pizzes(p_id, pizza_name, mod, price):
    cursor.execute(
        "INSERT INTO pizzes (id, pizza_name, modifications, price) VALUES(?, ?, ?, ?)", (p_id, pizza_name, mod, price))
    conn.commit()


# Добавляет напиток
def insert_drinks(d_id, drink_name, price):
    cursor.execute(
        "INSERT INTO drinks (id, drink_name, price) VALUES(?, ?, ?)", (d_id, drink_name, price))
    conn.commit()


# Чистит таблицу
def del_all(table):
    cursor.execute(f"DELETE FROM {table}")
    conn.commit()


# Чистит таблицу orders
def del_ord(tg_id):
    cursor.execute(f"UPDATE orders SET pizza_id='', drink_name='', drink_id='', size='' WHERE tg_id={tg_id}")
    conn.commit()


def del_drinks(tg_id):
    cursor.execute(f"UPDATE orders SET drink_name='', drink_id='' WHERE tg_id={tg_id}")
    conn.commit()


def del_pizzes(tg_id):
    cursor.execute(f"UPDATE orders SET pizza_id='', size='' WHERE tg_id={tg_id}")
    conn.commit()


def del_time(tg_id):
    cursor.execute(f"UPDATE orders SET time_ship='', time_ship_conf='' WHERE tg_id={tg_id}")
    conn.commit()


# Достает продукты
def select_products(table):
    cursor.execute(f"SELECT * FROM {table}")
    rows = cursor.fetchall()
    return rows


cursor.execute(
    f"SELECT * FROM pizzes")
rows = cursor.fetchall()
print(rows)
cursor.execute(
    f"SELECT * FROM orders")
rows = cursor.fetchall()
print(rows)

