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
    if not 'user_name' in post_data or not 'password':
        return jsonify({"""
            "status" : "error",
            "comment" : "Please follow the current template {"user_name" : "John",
            "password" : "*****"}"
            """
        })

    user_name = post_data['user_name']
    user_password = post_data['password']
    user_id = check_db.get_user_id(user_name)

    if user_id and check_db.password_is_correct(user_name, user_password):
        token = check_db.generate_token(user_id)
        return jsonify({
            "status" : "ok",
            "comment": "You are successfully logged in",
            "token" : token
        })  

    return  jsonify ({
        "status" : "error",
        "comment": "Please check your user_name/password or sign up by following link [sign_up]"
    })

    
@app.route('/registration', methods=['POST'])
def registration():
    post_data = request.get_json()
    if not post_data:
        return jsonify({
            "status" : "error",
            "comment" : "Invalid format, check your input and try again"
        })
    
    if not 'user_name' in post_data or not 'password':
        return jsonify({"""
            "status" : "error",
            "comment" : "Please follow the current template {"user_name" : "John",
            "password" : "*****"}"
            """
        })

    if not check_db.get_user_id(post_data['user_name']):
        check_db.new_user(post_data['user_name'], post_data['password'])
        return jsonify({
            "status" : "ok",
            "comment": "You are successfully registered"
        })    
    else:
        return jsonify( {
            "status" : "error",
            "comment" : "This user_name already exists, please choose the new one"
        })

    
@app.route('/stats', methods=['POST'])
def statistics():
    post_data = request.get_json()
    if not post_data:
        return jsonify({
            "status" : "error",
            "comment" : "Invalid format, check your input and try again"
        })
    
    if not 'user_name' in post_data or not 'token':
        return jsonify({"""
            "status" : "error",
            "comment" : "Please follow the current template {"user_name" : "John",
            "token" : "*****"}"
            """
        })

    if not check_db.token_is_valid(post_data['token']):
        return jsonify({
            "status" : "error",
            "comment" : "Invalid token"
        })
    
    user_id = check_db.get_user_id(post_data['user_name'])
    if not user_id:
        return jsonify({
            "status" : "error",
            "comment" : "Cannot check statistics, user does not exists"
        })
    

    return jsonify({
        "status" : "ok",
        "statistics" : check_db.get_user_stats(user_id).to_dict()
    })

if __name__ == "__main__":
    check_db.init_db()
    app.run()
