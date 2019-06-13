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
    user_id = db.get_user_id_by_name(user_name)

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


@app.route('/logout', methods=['POST'])
def loggout():
    post_data = request.get_json()
    if not post_data:
        return jsonify({
            "result" : "error",
            "comment" : "Invalid format, check your input and try again"
        })
    
    if not 'token' in post_data :
        return jsonify({"""
            "result" : "error",
            "comment" : "Please follow the current template {"token" : "*************"}"
            """
        })
    
    user_id = db.get_user_id_by_token(post_data['token'])
    if not user_id:
        return jsonify( {
            "result" : "error",
            "comment" : "Invalid token, try again"
        })
    
    db.delete_token(user_id)
    return jsonify({
        "result" : "ok",
        "comment": "You are successfully logged out"
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

    if not db.get_user_id_by_name(post_data['user_name']):
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

    if not db.get_user_id_by_token(post_data['token']):
        return jsonify({
            "result" : "error",
            "comment" : "Invalid token"
        })
    
    user_id = db.get_user_id_by_name(post_data['user_name'])
    if not user_id:
        return jsonify({
            "result" : "error",
            "comment" : "Cannot check statistics, user does not exists"
        })
    

    return jsonify({
        "result" : "ok",
        "statistics" : db.get_user_stats(user_id).to_dict()
    })


@app.route('/battle/join', methods=['POST'])
def join_battle():
    post_data = request.get_json()
    if not post_data:
        return jsonify({
            "result" : "error",
            "comment" : "Invalid format, check your input and try again"
        })      
    
    if not 'token' in post_data:
        return jsonify({"""
            "result" : "error",
            "comment" : "Please follow the current template {"token" : "*****"}"
            """
        })

    user_id = db.get_user_id_by_token(post_data['token'])
    if not user_id:
        return jsonify({
            "result" : "error",
            "comment" : "Invalid token"
        })

    user_enemy_name = db.find_enemy(user_id)
    if not user_enemy_name:
        return jsonify({
            "result" : "error",
            "comment" : "Cannot find battle partner"
        })
    
    return jsonify({
        "result" : "ok",
        "comment" : f"Your enemy is: {user_enemy_name}" 
    })


@app.route('/battle/status', methods=['POST'])
def battle_status():
    post_data = request.get_json()
    if not post_data:
        return jsonify({
            "result" : "error",
            "comment" : "Invalid format, check your input and try again"
        })      
    
    if not 'token' in post_data:
        return jsonify({"""
            "result" : "error",
            "comment" : "Please follow the current template {"token" : "*****"}"
            """
        })

    user_id = db.get_user_id_by_token(post_data['token'])
    if not user_id:
        return jsonify({
            "result" : "error",
            "comment" : "Invalid token"
        })

    user_enemy_name = db.get_user_enemy(user_id)
    if not user_enemy_name:
        return jsonify({
            "result" : "ok",
            "status" : "You are not in the battle"
        })

    return jsonify({
        "result" : "ok",
        "status" : f"You are fighting against {user_enemy_name}" 
    })
    
        
@app.route('/battle/action', methods=['POST'])
def battle_action():
    post_data = request.get_json()
    if not post_data:
        return jsonify({
            "result" : "error",
            "comment" : "Invalid format, check your input and try again"
        })      
    
    if 'token' not in post_data or 'action' not in post_data:
        return jsonify({
            "result" : "error",
            "comment" : "Please follow the current template {'token' : '*****', 'action' : 'your_action'}"
            
        })
    
    user_id = db.get_user_id_by_token(post_data['token'])
    if not user_id:
        return jsonify({
            "result" : "error",
            "comment" : "Invalid token"
        })

    user_enemy_name = db.get_user_enemy(user_id)
    if not user_enemy_name:
        return jsonify({
            "result" : "error",
            "comment" : "You are not in the battle"
        })
    current_turn_user_id = db.get_current_turn_user_id(user_id)
    if current_turn_user_id != user_id:
        return jsonify({
            "result": "error",
            "comment": "It is not your turn"
        })

    action = post_data['action']
    if action not in ('up', 'down', 'left', 'right'):
        return jsonify({
            "result": "error",
            "comment": "Invalid action. Available actions: 'up', 'down', 'left', 'right'"
        })
  
    new_position, battle_won = db.make_action(user_id, action)
    if battle_won:
        comment = 'You won the battle!'
    else:
        commet = f'Action made successfuly. Your new position is [{new_position.x}, {new_position.y}]'
    return jsonify({
        "result": "ok",
        "comment": comment,
    })


@app.route('/help', methods=['POST'])
def help():
    post_data = request.get_json()
    if not post_data:
        return jsonify({
            "result" : "error",
            "comment" : "Invalid format, check your input and try again"
        })      
    
    if not 'help' in post_data:
        return jsonify({"""
            "result" : "error",
            "comment" : "Please follow the current template {"help"}"
            """
        })

    return """
registration: curl -X POST -H "Content-Type:application/json" -d '{"user_name" : "your_user_name", "password" : "your_password"}' http://host:port/registration
login: curl -X POST -H "Content-Type:application/json" -d '{"user_name" : "your_user_name", "password" : "your_password"}' http://host:port/login
logout: curl -X POST -H "Content-Type:application/json" -d '{"token" : "your_valid_token"}' http://host:port/logout
statistics: curl -X POST -H "Content-Type:application/json" -d '{"user_name" : "chosen_user_name", "token" : "your_valid_token"}' http://host:port/stats
join the battle: curl -X POST -H "Content-Type:application/json" -d '{"token" : "your_valid_token"}' http://host:port/battle/join    
see your battle status: curl -X POST -H "Content-Type:application/json" -d '{"token" : "your_valid_token"}' http://host:port/battle/status
fighting the battle: curl -X POST -H "Content-Type:application/json" -d '{"token" : "your_valid_token", "action" : "up/down/right/left"}' http://host:port/battle/action\n"""


if __name__ == "__main__":
    print("""!!!!!!!!!!!!!HELP ALERT!!!!!!!!!!!!!\n curl -X POST -H "Content-Type:application/json" -d '{"help": "me!"}' http://host:port/help \n!!!!!!!!!!!!!!!
""")
    db.init_db()
    app.run()
