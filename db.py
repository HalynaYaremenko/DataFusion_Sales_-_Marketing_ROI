import sqlite3  # підключаємо стандартну бібліотеку для роботи з SQLite

# Створюємо підключення до бази даних.
# Якщо файлу shop_sglite.db ще не існує — він буде створений автоматично
conn = sqlite3.connect('shop_sglite.db')

# Створюємо курсор — через нього ми будемо виконувати SQL-запити
cur = conn.cursor()

# Відкриваємо файл з SQL-командами (створення таблиць, вставка даних тощо)
# 'r' означає режим читання
with open('orders_sqlite.sql', 'r', encoding='utf-8') as f:
    # Читаємо весь SQL-файл як один текст
    sql_script = f.read()

# Виконуємо всі SQL-команди з файлу одразу
# Наприклад: CREATE TABLE, INSERT INTO і т.д.
cur.executescript(sql_script)

# Виконуємо SQL-запит:
cur.execute('''
             SELECT *
             FROM orders
             LIMIT 5;
            ''')

# Виводимо результат запиту у консоль
print(cur.fetchall())

# Зберігаємо всі зміни в базі даних
conn.commit()

# Закриваємо підключення до бази даних
conn.close()

