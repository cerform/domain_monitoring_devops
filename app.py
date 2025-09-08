from flask import Flask,request,jsonify
app = Flask(__name__)


@app.route('/', methods=['GET'])
def main():
    return app.send_static_file('main/main.html')


@app.route('/login', methods=['GET','POST'])
def main():
    if request.method == 'GET':
        return app.send_static_file('login/login.html')
    else:
        loginInfo=request.json
        ## check login details from json


@app.route('/register', methods=['GET','POST'])
def main():
    if request.method == 'GET':
        return app.send_static_file('register/register.html')
    else:
        registerInfo=request.json
        ## check register details from json


@app.route('/dashboard', methods=['GET'])
def main():
    return app.send_static_file('dashboard/dashboard.html')


@app.route('/<filename>', methods=['GET'])
def static_files(filename):
    return app.send_static_file(filename)


app.run(debug=True, host="0.0.0.0", port="8080")