from flask import Flask
app = Flask(__name__)


@app.route('/', methods=['GET'])
def main():
    return app.send_static_file('main/main.html')

@app.route('/<filename>', methods=['GET'])
def static_files(filename):
    return app.send_static_file(filename)

app.run(debug=True, host="0.0.0.0", port="8080")