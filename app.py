import json 
import db

from flask import Flask, request, jsonify

DEBUG = True

app = Flask(__name__)
app.config.from_object(__name__)

@app.route('/login', methods=['POST'])
def login():
    post_data = request.get_json()
    if not post_data:
        return jsonify({
            "result" : "error",
            "comment" : "Invalid format, check your input and try again"
        })
    if not 'user_name' in post_data or not 'password':
        return jsonify({"""
            "result" : "error",
            "comment" : "Please follow the current template {"user_name" : "John",
            "password" : "*****"}"
            """
        })

    user_name = post_data['user_name']
    user_password = post_data['password']
    user_id = db.get_user_id(user_name)

    if user_id and db.password_is_correct(user_name, user_password):
        token = db.generate_token(user_id)
        return jsonify({
            "result" : "ok",
            "comment": "You are successfully logged in",
            "token" : token
        })  

    return  jsonify ({
        "result" : "error",
        "comment": "Please check your user_name/password or sign up by following link [sign_up]"
    })

    
@app.route('/registration', methods=['POST'])
def registration():
    post_data = request.get_json()
    if not post_data:
        return jsonify({
            "result" : "error",
            "comment" : "Invalid format, check your input and try again"
        })
    
    if not 'user_name' in post_data or not 'password':
        return jsonify({"""
            "result" : "error",
            "comment" : "Please follow the current template {"user_name" : "John",
            "password" : "*****"}"
            """
        })

    if not db.get_user_id(post_data['user_name']):
        db.new_user(post_data['user_name'], post_data['password'])
        return jsonify({
            "result" : "ok",
            "comment": "You are successfully registered"
        })    
    else:
        return jsonify( {
            "result" : "error",
            "comment" : "This user_name already exists, please choose the new one"
        })

    
@app.route('/stats', methods=['POST'])
def statistics():
    post_data = request.get_json()
    if not post_data:
        return jsonify({
            "result" : "error",
            "comment" : "Invalid format, check your input and try again"
        })
    
    if not 'user_name' in post_data or not 'token':
        return jsonify({"""
            "result" : "error",
            "comment" : "Please follow the current template {"user_name" : "John",
            "token" : "*****"}"
            """
        })

    if not db.token_is_valid(post_data['token']):
        return jsonify({
            "result" : "error",
            "comment" : "Invalid token"
        })
    
    user_id = db.get_user_id(post_data['user_name'])
    if not user_id:
        return jsonify({
            "result" : "error",
            "comment" : "Cannot check statistics, user does not exists"
        })
    

    return jsonify({
        "result" : "ok",
        "statistics" : db.get_user_stats(user_id).to_dict()
    })

if __name__ == "__main__":
    db.init_db()
    app.run()
