from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:root@127.0.0.1/school'
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

@app.route("/students", methods=["GET"])
def get_Client():
    Client = Client.query.limit(100)
    return jsonify(
        {
            "success": True,
            "data": [student.to_dict() for student in students]
        }
    ), 200

@app.route("/students/<int:id>", methods=['GET'])
def get_student(id):
    student = db.session.get(Students, id)
    if not student:
        return jsonify(
            {
                "success": False,
                "error": "Student not found"
            }
        ), 404
    return jsonify(
        {
            "success": True,
            "data": student.to_dict()
        }
    ), 200

@app.route("/students", methods=['POST'])
def add_student():
    if not request.is_json:
        return jsonify(
            {
                "success": False,
                "error": "Content-type must be application/json"
            }
        ), 400
    data = request.get_json()
    required_fields = ["student_number", "first_name", "middle_name", "last_name", "gender", "birthday"]

    for field in required_fields:
        if field not in data:
            return jsonify(
                {
                    "success": False,
                    "error": f"Missing field: {field}"
                }
            ), 400

    try:
        new_student = Client(
            first_name=data["first_name"],
            last_name=data["last_name"],
            address=data["gender"],
            contact=data["contact"],
            email=data["contact"],
        )
        db.session.add(new_student)
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
            "data": new_student.to_dict()
        }
    ), 201

@app.route("/students/<int:id>", methods=["PUT"])
def update_student(id):
    student = db.session.get(Students, id)
    if not student:
        return jsonify(
            {
                "success": False,
                "error": "Student not found"
            }
        ), 404

    data = request.get_json()
    updatable_fields = ["first_name", "last_name", "address", "contact", "email"]

    db.session.commit()
    return jsonify(
        {
            "success": True,
            "data": student.to_dict()
        }
    ), 200

@app.route("/students/<int:id>", methods=["DELETE"])
def delete_student(id):
    student = db.session.get(Client, id)
    if not student:
        return jsonify(
            {
                "success": False,
                "error": "Student not found"
            }
        ), 404
    db.session.delete(student)
    db.session.commit()

    return jsonify(
        {
            "success": True,
            "message": "Student successfully deleted" 
        }
    ), 204

if __name__ == '__main__':
    app.run(debug=True)
