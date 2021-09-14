import pyodbc

conn = pyodbc.connect('Driver={SQL Server};'
                      'Server=DESKTOP-D3E52S7\SQLEXPRESS;'
                      'Database=mydatabase;'
                      'Trusted_Connection=yes;')

cursor = conn.cursor()
cursor.execute('SELECT * FROM mydatabase.dbo.Catedraticos')

for row in cursor:
    print(row)