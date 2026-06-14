import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "users.db")

#Подключаемся к базе данных
conn = sqlite3.connect("users.db")

#Создаем курсор это инструмент для запросов
cursor = conn.cursor()

#Создаем таблицу
cursor.execute("""
               CREATE TABLE IF NOT EXISTS users (
               id INTEGER PRIMARY KEY,
               name TEXT,
               age TEXT,
               city TEXT
               )
              """)
conn.commit()
conn.close()

#Создаем функцию для сохранения и получения пользователей
def save_user(user_id, name, age, city):
    conn = sqlite3.connect("DB_PATH")
    cursor = conn.cursor()
    cursor.execute("""
                   INSERT OR REPLACE INTO users(id, name, age, city)
                   VALUES (?, ?, ?, ?)
                   """, (user_id, name, age,city))
    conn.commit()
    conn.close()

#Функция которая получает пользователя из базы:
def get_user(user_id):
    conn = sqlite3.connect("DB_PATH")
    cursor = conn.cursor()
    cursor.execute("SELECT name, age, city FROM users WHERE id = ?", (user_id,))
    user = cursor.fetchone()
    conn.close()
    return user

#Функция удаления
def delete_user(user_id):
    conn = sqlite3.connect("DB_PATH")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM users WHERE id = ?", (user_id,))
    conn.commit()
    conn.close()

def init_db():
    conn = sqlite3.connect("DB_PATH")
    cursor = conn.cursor()
    cursor.execute("""
                   CREATE TABLE IF NOT EXISTS users (
                   id INTEGER PRIMARY KEY,
                   name TEXT,
                   age TEXT,
                   city TEXT
                   )
                   """)
    conn.commit()
    conn.close()
