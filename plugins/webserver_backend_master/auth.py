import sqlite3
import bcrypt
import time
import json
from Crypto.Cipher import AES
import base64

def getSalt(sh, data):
    out = data
    out['login'] = False
    user = data['data']['user']
    password = data['data']['passwd']
    del data['data']
    if 'token' in out:
        del out['token']
    try:
        file = sh.const.path+'/db/auth.db'
        conn = sqlite3.connect(file)
        cur = conn.cursor()
        sql = "SELECT passwd, name FROM user WHERE user='" + user + "'"
        cur.execute(sql)
        res = cur.fetchone()
        passwd = res[0]
        name = res[1]
        if bcrypt.checkpw(password.encode(), passwd.encode()):
            out['login'] = True
            out['name'] = name
            out['token'] = {'timeout': int(time.time()+900), 'packages': ['sm_backend']}
            out = encode(sh, out)
    except:
        pass
    del out['client']
    del out['cmd']
    return out

def check_aes(sh):
     if sh.const.aes_key == '':
         file = sh.const.path+'/db/auth.db'
         conn = sqlite3.connect(file)
         cur = conn.cursor()
         sql = "CREATE TABLE IF NOT EXISTS aes (id integer PRIMARY KEY, aes_key text NOT NULL)"
         cur.execute(sql)
         conn.commit()
         sql = "SELECT aes_key FROM aes WHERE id='1'"
         cur.execute(sql)
         res = cur.fetchone()
         if res == None:
             sh.const.aes_key = bcrypt.gensalt().decode()
             sql = "INSERT INTO aes (aes_key) VALUES ('" + sh.const.aes_key + "')"
             cur.execute(sql)
             conn.commit()
             print('need aes key')
         else:
             sh.const.aes_key = res[0]
         conn.close()


def encode(sh, _in):
     check_aes(sh)
     out = _in
     cipher = AES.new(sh.const.aes_key[:16].encode(), AES.MODE_EAX)
     _in['token']['timeout'] = int(time.time()+900)
     if 'cmd' in _in['token']:
         del _in['token']['cmd']
     if 'client' in _in['token']:
         del _in['token']['client']
     token = json.dumps(_in['token']).encode()
     ciphertext, tag = cipher.encrypt_and_digest(token)
     out['token'] = base64.encodestring(cipher.nonce+ciphertext).decode()
     return out

def decode(sh, _in):
    check_aes(sh)
    out = _in
    try:
        ciphertext = base64.decodestring(_in['token'].encode())
        nonce = ciphertext[:AES.block_size]
        ciphertext = ciphertext[AES.block_size:]
        cipher = AES.new(sh.const.aes_key[:16].encode(), AES.MODE_EAX, nonce=nonce)
        text = cipher.decrypt(ciphertext)
        out['token'] = json.loads(text.decode())
        out['login'] = out['token']['timeout'] > time.time()
    except:
        out['login'] = False
        pass
    return out
