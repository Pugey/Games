#%%
#
import sqlite3

try:
    conn = sqlite3.connect('score.db')
    c = conn.cursor()
    print("Connected to SQLite")

    c.execute("""CREATE TABLE employees (
                first text,
                last text,
                pay integer
                )""") 

    sqlite_insert_query = """INSERT INTO employees
                          (first, last, pay) 
                          VALUES ('Terje', 'Lærær', 50);"""
    c.execute(sqlite_insert_query)

    sql_update_query = """Update employees set pay = 10000 where last = 'Pedersen'"""
    c.execute(sql_update_query) 

    sql_delete_query = """DELETE from employees where last = 'Pedersen'"""
    c.execute(sql_delete_query) 

    conn.commit()
    c.close()

except sqlite3.Error as error:
    print("Error while working with SQLite", error)
finally:
    if conn:
        print("Total Rows affected since the database connection was opened: ", conn.total_changes)
        c.close()
        print("sqlite connection is closed")





















# %%
