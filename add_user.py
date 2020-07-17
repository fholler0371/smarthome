import bcrypt
import sqlite3
import sys

real_name = input('echter Name: ')
user = input('Nutzer: ')
passwd = input('Passwort: ')
print('----------------------------------')

salt = bcrypt.gensalt()
hashed = bcrypt.hashpw(passwd.encode(), salt).decode()
print('Nutzer: ', user)
print('hashed Password: ', hashed)
print('----------------------------------')

passwd = input('Passwort wiederholen: ')
hashed2 = bcrypt.hashpw(passwd.encode(), hashed[:29].encode()).decode()
print(hashed2)
print('identisch: ', (hashed == hashed2))
print('----------------------------------')

if hashed != hashed2:
    sys.exit(0)

conn = sqlite3.connect("db/auth.db")
cur = conn.cursor()

sql = "CREATE TABLE IF NOT EXISTS user (id integer PRIMARY KEY, name text NOT NULL, user text Not Null, passwd text Not Null)"
cur.execute(sql)
conn.commit()

sql = "SELECT id FROM user WHERE user='" + user + "'"
cur.execute(sql)
res = cur.fetchone()

if res == None:
    sql = "INSERT INTO user (name, user, passwd) VALUES ('" + real_name + "', '" + user + "', '" + hashed + "')"
else:
    id = res[0]
    sql = "UPDATE user set name='" + real_name + "', passwd='" + hashed + "' WHERE id='" + str(id) + "'"
cur.execute(sql)
conn.commit()
conn.close()


