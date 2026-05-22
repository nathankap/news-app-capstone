import sqlite3

db = sqlite3.connect("")

cursor = db.cursor()

cursor.execute('''
               CREATE TABLE IF NOT EXISTS python_programming (
                        id INTEGER PRIMARY KEY,
                        name STRING,
                        grade INTEGER
               )
''')

# (id, name, grade)
student_list = [(55, 'Carl Davis', 61),
                (66, 'Dennis Fredrickson', 88),
                (77, 'Jane Richards', 78),
                (12, 'Peyton Sawyer', 45),
                (2, 'Lucas Brooke', 99)]
cursor.executemany('''
                   INSERT INTO python_programming(id, name, grade) VALUES(?, ?, ?)
                   ''', student_list)
cursor.execute('SELECT name, grade FROM python_programming WHERE grade >= 60 AND grade <= 80')
students_60_80 = cursor.fetchall()

print("Students between 60 and 80:\n")
for student in students_60_80:
    print(f"{student[0]} : {student[1]}")

cursor.execute('''UPDATE python_programming SET grade = 65 WHERE id = 55''')
cursor.execute('''DELETE FROM python_programming WHERE id = 66''')
cursor.execute('''UPDATE python_programming SET grade = 80 WHERE id > 55''')
cursor.execute('''SELECT * FROM python_programming''')
table = cursor.fetchall()
print(table)
db.commit()
db.close()