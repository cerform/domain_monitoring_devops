from flask import Flask, request, jsonify, session, redirect
import os
from UserManagementModule import UserManager as UM

app = Flask(__name__)
app.secret_key = os.environ.get("FLASK_SECRET_KEY", "dev-secret-change-me")


@app.route('/', methods=['GET'])
def main_page():
    return app.send_static_file('main/main.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return app.send_static_file('login/login.html')
    else:
        loginInfo = request.json or {}
        username = (loginInfo.get("username") or "").strip()
        password = loginInfo.get("password") or ""

        if not UM.validate_login(username, password):
            return jsonify({"ok": False, "error": "Invalid username or password"}), 401

        session["username"] = username
        return jsonify({"ok": True, "message": "Login successful", "username": username}), 200


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return app.send_static_file('register/register.html')
    else:
        registerInfo = request.json or {}
        username = (registerInfo.get("username") or "").strip()
        password = registerInfo.get("password") or ""

        if not username or not password:
            return jsonify({"ok": False, "error": "Username and password required"}), 400

        if not UM.is_username_available(username):
            return jsonify({"ok": False, "error": "Username already exists"}), 409

        ok, reason = UM.is_password_valid(password)
        if not ok:
            return jsonify({"ok": False, "error": f"Invalid password: {reason}"}), 400

        UM.add_user(username, password)
        UM.ensure_user_domain_file(username)

        return jsonify({"ok": True, "message": "User created"}), 201


@app.route('/dashboard', methods=['GET'])
def dashboard():
    if "username" not in session:
        return redirect("/login")
    return app.send_static_file('dashboard/dashboard.html')


@app.route('/add_domain', methods=['POST'])
def add_domain():
    if "username" not in session:
        return jsonify({"ok": False, "error": "Unauthorized"}), 401

    domain_info = request.json or {}
    raw_domain = (domain_info.get("domain") or "").strip()

    ok, norm_domain, reason = UM.validate_domain(raw_domain)
    if not ok:
        return jsonify({"ok": False, "error": f"Invalid domain: {reason}"}), 400

    saved = UM.add_domain(session["username"], norm_domain)
    if not saved:
        return jsonify({"ok": False, "error": "Domain already exists"}), 409

    return jsonify({"ok": True, "domain": norm_domain}), 201


@app.route('/<filename>', methods=['GET'])
def static_files(filename):
    return app.send_static_file(filename)


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=8080)
