from flask import Flask, jsonify, abort, make_response, request
from flask import url_for
from flask_httpauth import HTTPBasicAuth


menu = Flask(__name__)
auth = HTTPBasicAuth()


@auth.get_password
def get_password(username):
    if username == "adminQA":
        return "assignmentAPI"
    return None


@auth.error_handler
def unauthorized():
    return make_response(jsonify({"error": "unauthorized access"}), 401)
    

menus = [
    {
        "order": 1,
        "cuisine": "filipino",
        "food": "Kare-Kare",
        "description": "Kare Kare is a type of Filipino stew with a rich and thick peanut sauce",
        "done": False,
    },
    {
        "order": 2,
        "cuisine": "filipino",
        "food": "Sinigang na Baboy",
        "description": "It is composed of pork and vegetables boiled in a clear sour broth.",
        "done": False,
    },
    {
        "order": 3,
        "cuisine": "korean",
        "food": "Bibimbap",
        "description": "Rice meal with cooked vegetables, usually meat, and often a raw or fried egg",
        "done": False,
    },
    {
        "order": 4,
        "cuisine": "korean",
        "food": "Jajangmyeon",
        "description": "Black bean noodles",
        "done": False,
    },
]

    
@menu.route('/')
def index():
    return "Hello! Welcome to API Restaurant."

@menu.route("/apitesting/restaurant/v1.0/menu", methods=["GET"])
@auth.login_required()
def get_menus():
    return jsonify({"menus": [make_public_menu(menu) for menu in menus]})

@menu.route("/apitesting/restaurant/v1.0/menu/<int:order_id>", methods=["GET"])
def get_order(order_id):
    menu = [menu for menu in menus if menu["order"] == order_id]
    if not menu:
        abort(404)
    return jsonify(menu)

@menu.errorhandler(404)
def not_found(error):
    return make_response(jsonify({"error": "Not found"}), 404)

@menu.route("/apitesting/restaurant/v1.0/menu", methods=["POST"])
def create_menu():
    if not request.json or "food" not in request.json:
        abort(400)
    menu = {
        "order": menus[-1]["order"] + 1,
        "food": request.json["food"],
        "description": request.json.get("description", ""),
        "done": False,
    }
    menus.append(menu)
    return jsonify({"menu": menu}), 201

@menu.route("/apitesting/restaurant/v1.0/menu/<int:order_id>", methods=["PUT"])
def update_menu(order_id):
    menu = [menu for menu in menus if menu["order"] == order_id]
    if not menu:
        abort(404)
    if not request.json:
        abort(400)
    if "food" in request.json and type(request.json["food"]) != str:
        abort(400)
    if "description" in request.json and type(request.json["description"]) is not str:
        abort(400)
    menu[0]["food"] = request.json.get("food", menu[0]["food"])
    menu[0]["description"] = request.json.get("description", menu[0]["description"])
    menu[0]["done"] = request.json.get("done", menu[0]["done"])
    return jsonify({"menu": menu[0]})
    
@menu.route("/apitesting/restaurant/v1.0/menu/<int:order_id>", methods=["PATCH"])
def modify_menu(order_id):
    menu = [menu for menu in menus if menu["order"] == order_id]
    if not menu:
        abort(404)
    if not request.json:
        abort(400)
    if "food" in request.json and type(request.json["food"]) != str:
        abort(400)
    if "description" in request.json and type(request.json["description"]) is not str:
        abort(400)
    menu[0]["food"] = request.json.get("food", menu[0]["food"])
    menu[0]["description"] = request.json.get("description", menu[0]["description"])
    menu[0]["done"] = request.json.get("done", menu[0]["done"])
    return jsonify({"menu": menu[0]})
    
@menu.route("/apitesting/restaurant/v1.0/menu/<int:order_id>", methods=["DELETE"])
def delete_task(order_id):
    menu = [menu for menu in menus if menu["order"] == order_id]
    if not menu:
        abort(404)
    menus.remove(menu[0])
    return jsonify({"result": True})

def make_public_menu(menu):
    new_menu = {}
    for field in menu:
        if field == "order":
            new_menu["uri"] = url_for("get_order", order_id=menu["order"], _external=True)
        else:
            new_menu[field] = menu[field]
    return new_menu
    
def shutdown_server():
    func = request.environ.get("werkzeug.server.shutdown")
    if func is None:
        raise RuntimeError("Not running with the Werkzeug Server")
    func()


@menu.route("/shutdown", methods=["GET"])
def shutdown():
    shutdown_server()
    return "Server shutting down..."

if __name__ == "__main__":
    menu.run(host="0.0.0.0", port="8080", debug=True)
