from flask import Flask,render_template,request

app = Flask(__name__)


@app.route('/')
def hello():
    return render_template('index.html')

@app.route('/register',methods=['POST'])
def register():
    form = request.form
    user = form['username']+"|"+form['password']
    saveUser(user)
    return "dang ki thanh cong"


def saveUser(user):
    f = open('account.txt','a+')
    f.write(user+"\n")

if __name__ == "__main__":
	app.run(port = 80)