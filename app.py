import json 
import check_db

from flask import Flask, request, jsonify

DEBUG = True

app = Flask(__name__)
app.config.from_object(__name__)

@app.route('/login', methods=['POST'])
def login():
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

    user_login = post_data['login']
    user_password = post_data['password']

    if check_db.user_exists(user_login) and check_db.password_is_correct(user_login, user_password):
        token = check_db.generate_token(user_login, user_password)
        return jsonify({
            "status" : "ok",
            "comment": "You are successfully logged in",
            "token" : token
        })  

    return  jsonify ({
        "status" : "error",
        "comment": "Please check your login/password or sign up by following link [sign_up]"
    })

    
@app.route('/registration', methods=['POST'])
def registration():
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

    if not check_db.user_exists(post_data['login']):
        check_db.new_user(post_data['login'], post_data['password'])
        return jsonify({
            "status" : "ok",
            "comment": "You are successfully registered"
        })    
    else:
        return jsonify( {
            "status" : "error",
            "comment" : "This login already exists, please choose the new one"
        })

    
@app.route('/stats', methods=['POST'])
def statistics():
    post_data = request.get_json()
    if not post_data:
        return jsonify({
            "status" : "error",
            "comment" : "Invalid format, check your input and try again"
        })
    
    if not 'login' in post_data or not 'token':
        return jsonify({"""
            "status" : "error",
            "comment" : "Please follow the current template {"login" : "John",
            "token" : "*****"}"
            """
        })

    if not check_db.token_is_valid(post_data['token']):
        return jsonify({
            "status" : "error",
            "comment" : "Invalid token"
        })

    if not check_db.user_exists(post_data['login']):
        return jsonify({
            "status" : "error",
            "comment" : "Cannot check statistics, user does not exists"
        })
    

    return jsonify({
        "status" : "ok",
        "statistics" : check_db.get_user_stats(post_data['login']).to_dict()
    })

if __name__ == "__main__":
    check_db.init_db()
    app.run()
