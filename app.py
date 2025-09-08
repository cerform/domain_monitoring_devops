from flask import Flask
app = Flask(__name__)


@app.route('/', methods=['GET'])
def main():
    return app.send_static_file('main/main.html')

@app.route('/login', methods=['GET'])
def main():
    return app.send_static_file('login/login.html')

@app.route('/register', methods=['GET'])
def main():
    return app.send_static_file('register/register.html')

@app.route('/dashboard', methods=['GET'])
def main():
    return app.send_static_file('dashboard/dashboard.html')

@app.route('/<filename>', methods=['GET'])
def static_files(filename):
    return app.send_static_file(filename)

app.run(debug=True, host="0.0.0.0", port="8080")