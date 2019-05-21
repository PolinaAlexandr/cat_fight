import json 
import check_db

from flask import Flask, request, jsonify

DEBUG = True

app = Flask(__name__)
app.config.from_object(__name__)

@app.route('/login', methods=['POST'])
def authentification():
    post_data = request.get_json()
    if not post_data:
        return jsonify({
            "status" : "error",
            "comment" : "Invalid format, check your input and try again"
        })
    if not 'login' in post_data or not 'password':
        return jsonify({"""
            "status" : "error",
            "comment" : "Please follow the current template {"login" : "John",
            "password" : "*****"}"
            """
        })
        return

    if check_db.user_exists(post_data['login']):
        return jsonify({
            "status" : "ok",
            "comment": "You are seccussfully logged in"
        })  

    return  jsonify ({
        "status" : "error",
        "comment": "Please check your login or sign up by following link [sign_up]"
    })
    


if __name__ == "__main__":
    check_db.init_db()
    app.run()
