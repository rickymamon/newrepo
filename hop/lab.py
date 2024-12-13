from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datatime

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysql-connector://root:admin@127.0.0.1/mydb'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Client(db.Model):
    __tablename__ = 'client'
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(30), nullable=False)
    last_name = db.Column(db.String(30), nullable=False)
    address = db.Column(db.String(30), nullable=False)
    contact = db.Column(db.String(30), nullable=False)
    email = db.Column(db.String(30), nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "address": self.address,
            "contact":self.contact,
            "email": self.email,
        }
@app.route("/client", methods=["GET"])
def get_Client():
    Client = Client.query
    return jsonify(
        {
            "success": True,
            "data": [Client.to_dict() for Client in Client]
        }
    ), 200
    
@app.route("/client/<int:id>", methods=['GET'])
def get_client(id):
    client = db.session.get(Client, id)
    if not client:
        return jsonify(
            {
                "success": False,
                "error": "Client not found"
            }
        ), 404
    return jsonify(
        {
            "success": True,
            "data": client.to_dict()
        }
    ), 200
    
@app.route("/client", methods=['POST'])
def add_client():
    if not request.is_json:
        return jsonify(
            {
                "success": False,
                "error": "Content-type must be application/json"
            }
        ), 400
        
    data = request.get_json()
    required_fields = ["first_name", "last_name", "address", "contact", "email"]
    
    
    for field in required_fields:
        if field not in data:
            return jsonify(
                {
                    "success": False,
                    "error": f"Missing field: {field}"
                }
            ), 400

    try:
        new_client = Client(
            first_name=data["first_name"],
            last_name=data["last_name"],
            address=data["address"],
            contact=data["contact"],
            email=data["email"],
        )
        db.session.add(new_client)
        db.session.commit()
    except Exception as e:
        return jsonify(
            {
                "success": False,
                "error": str(e)
            }
        ), 500

    return jsonify(
        {
            "success": True,
            "data": new_client.to_dict()
        }
    ), 201
@app.route("/client/<int:id>", methods=["PUT"])
def update_client(id):
    client = db.session.get(Client, id)
    if not client:
        return jsonify(
            {
                "success": False,
                "error": "Client not found"
            }
        ), 404

    data = request.get_json()
    updatable_fields = ["first_name", "last_name", "address", "contact", "email"]
    
    for field in updatable_fields:
        if field in data:
            setattr(client, field, data[field])

    db.session.commit()
    return jsonify(
        {
            "success": True,
            "data": client.to_dict()
        }
    ), 200

@app.route("/client/<int:id>", methods=["DELETE"])
def delete_client(id):
    client = db.session.get(Client, id)
    if not client:
        return jsonify(
            {
                "success": False,
                "error": "Client not found"
            }
        ), 404
    db.session.delete(client)
    db.session.commit()

    return jsonify(
        {
            "success": True,
            "message": "Client successfully deleted"
        }
    ), 200
    

if __name__ == '__main__':
    app.run(debug=True)
