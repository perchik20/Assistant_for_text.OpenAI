import psycopg2


def add_data(question, answer, album_name, hash):
    try:
        conn = psycopg2.connect(dbname="metanit", user="postgres", password="School1367", host="127.0.0.1")
        cursor = conn.cursor()
        print("Подключен к SQLite")

        sqlite_insert_query = f"INSERT INTO Answers (question, answer, album_name, hash) VALUES ('{question}', '{answer}', '{album_name}', '{hash}');"
        cursor.execute(sqlite_insert_query)
        conn.commit()
        print("Запись успешно вставлена в таблицу sqlitedb_developers ", cursor.rowcount)
        cursor.close()

    except (Exception, psycopg2.Error) as error:
        print("Ошибка при работе с SQLite", error)
    finally:
        if conn:
            conn.close()


def get_data(text):
    try:
        conn = psycopg2.connect(dbname="metanit", user="postgres", password="School1367", host="127.0.0.1")
        cursor = conn.cursor()
        method = text
        cursor.execute(method)
        records = cursor.fetchall()

        return records

    except (Exception, psycopg2.Error) as error:
        print("Ошибка при работе с SQLite", error)

    finally:
        if conn:
            conn.close()

