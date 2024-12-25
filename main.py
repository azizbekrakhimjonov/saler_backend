# # """
# #     code    category    point    used_by
# #    NN5H2J       1         5       NULL
# # """
# from string import ascii_uppercase, digits
# from random import choices
# from pprint import pprint as print
# import sqlite3
#
# # Connect to the SQLite database
# conn = sqlite3.connect('product.db')
# cursor = conn.cursor()
#
# # Create the promocode table if it doesn't exist
# cursor.execute('''
#     CREATE TABLE IF NOT EXISTS promocode (
#         id INTEGER PRIMARY KEY AUTOINCREMENT,
#         code TEXT UNIQUE,
#         category TEXT,
#         point INTEGER,
#         used_by TEXT DEFAULT NULL)
# ''')
#
# categories = {
#     'category1': 5,
#     'category2': 10,
#     'category3': 15,
#     'category4': 20,
#     'category5': 25,
#     'category6': 30,
#     'category7': 35,
#     'category8': 40,
#     'category9': 45,
#     'category10': 50
# }
#
# try:
#     for category, point in categories.items():
#         for i in range(100):
#             code = ''.join(choices(ascii_uppercase + digits, k=6))
#             data = (code, category, point, 'NULL')
#             sql = '''
#                 INSERT OR IGNORE INTO promocode (code, category, point, used_by)
#                 VALUES (?, ?, ?, ?);
#             '''
#             cursor.execute(sql, data)
#
#     # Commit changes
#     conn.commit()
#
# except sqlite3.Error as e:
#     print(f"An error occurred: {e}")
#     conn.rollback()
#
# finally:
#     conn.close()
#
# # cursor.execute("SELECT * FROM promocode")
# # rows = cursor.fetchall()
# # print(rows)
