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


@app.route('/')
def hello():
    return render_template('index.html')

@app.route('/register',methods=['POST'])
def register():
    form = request.form
    username = form['username']
    password = form['password']
    save_user_to_db(username,password)
    return render_template('love.html')

@app.route("/get_all_user",methods=['GET'])
def get_all_user():
    query_select_all_user = "select * from user"
    sql.execute(query_select_all_user)
    result = sql.fetchall()

    resp = ""
    for i in result:
        col = f"<p>Tài khoản: {i[1]} - Mật khẩu: {i[2]}</p><br>"
        resp+=col
    return resp


def save_user_to_db(username,password):
    query_insert_user = f"insert into user(username,password) values('{username}','{password}')"
    sql.execute(query_insert_user)
    conn.commit()

if __name__ == "__main__":
	app.run(port = 80)






