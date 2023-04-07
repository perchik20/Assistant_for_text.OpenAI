import sqlite3


def add_data(question, answer, album_name):
    try:
        sqlite_connection = sqlite3.connect('test.db')
        cursor = sqlite_connection.cursor()
        print("Подключен к SQLite")

        sqlite_insert_query = f"INSERT INTO Users (question, answer, album_name) VALUES ('{question}', '{answer}', '{album_name}');"
        count = cursor.execute(sqlite_insert_query)
        sqlite_connection.commit()
        print("Запись успешно вставлена в таблицу sqlitedb_developers ", cursor.rowcount)
        cursor.close()

    except sqlite3.Error as error:
        print("Ошибка при работе с SQLite", error)
    finally:
        if sqlite_connection:
            sqlite_connection.close()
            print("Соединение с SQLite закрыто")


def get_data(text):
    try:
        records1 = []
        conn = sqlite3.connect('test.db')
        cursor = conn.cursor()
        method = text
        cursor.execute(method)
        records = cursor.fetchall()

        return records

    except sqlite3.Error as error:
        print("Ошибка при работе с SQLite", error)

    finally:
        if conn:
            conn.close()
            print("Соединение с SQLite закрыто")
