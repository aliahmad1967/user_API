from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Create Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///my_database.db'
db = SQLAlchemy(app)

# Create Model
class User(db.Model):  # Use PascalCase for class names
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'password': self.password
        }

# Create Database Tables
with app.app_context():
    db.create_all()

# Create Routes
@app.route('/')
def home():
    return jsonify({'message': 'Welcome to the API'})  # Fixed typo

@app.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()
    return jsonify([user.to_dict() for user in users])  # Fixed list comprehension

@app.route('/users/<int:id>', methods=['GET'])
def get_user(id):
    user_data = User.query.get(id)  # Renamed variable
    if user_data:
        return jsonify (user_data.to_dict())
    else:
        return jsonify({'message': 'User  not found'}), 404

@app.route('/users', methods=['POST'])
def create_user():
    data = request.get_json()
    new_user = User(username=data['username'], email=data['email'], password=data['password'])
    db.session.add(new_user)
    db.session.commit()
    return jsonify(new_user.to_dict()), 201

@app.route('/users/<int:id>', methods=['PUT'])
def update_user(id):
    data = request.get_json()
    user_data = User.query.get(id)  # Renamed variable
    if user_data:
        user_data.username = data.get('username', user_data.username)
        user_data.email = data.get('email', user_data.email)
        user_data.password = data.get('password', user_data.password)

        db.session.commit()
        return jsonify(user_data.to_dict())
    else:
        return jsonify({'message': 'User  not found'}), 404

@app.route('/users/<int:id>', methods=['DELETE'])
def delete_user(id):
    user_data = User.query.get(id)  # Use the `id` parameter
    if user_data:
        db.session.delete(user_data)
        db.session.commit()
        return jsonify({'message': 'User  deleted successfully'})
    else:
        return jsonify({'message': 'User  not found'}), 404

if __name__ == '__main__':
    app.run(debug=True)