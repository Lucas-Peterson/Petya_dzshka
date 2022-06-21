import sqlite3

base = sqlite3.connect('new.db')

cur = base.cursor()
'''

text, integer, real, blob, null
base.execute('CREATE TABLE IF NOT EXISTS {}(login PRIMARY KEY, password text)'.format('data'))
base.commit()
cur.execute('INSERT INTO data VALUES(?, ?)', ('billy5565', '12345678'))
base.commit()
cur.execute('INSERT INTO data VALUES(?, ?)', ('Petya555y', 'pASSWORD148'))
base.commit()
r = cur.execute('SELECT * FROM data').fetchall()
r = cur.execute('SELECT password FROM data WHERE login == ?', ('billy5565',)).fetchone()

cur.execute('UPDATE data SET password == ? WHERE login == ?', ('12345678','billy5565'))
base.commit()
'''
cur.execute('DELETE FROM data WHERE login == ?', ('Petya555y',))
base.commit()
base.close()