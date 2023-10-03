from flask import Flask, jsonify, make_response, request, session
from flask_migrate import Migrate
from flask_restful import Api, Resource
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy

from models import DogHouse, User
from config import app, db, api

# Example route to get a list of dog houses
@app.route('/api/dog_houses', methods=['GET'])
def get_dog_houses():
    dog_houses = DogHouse.query.all()
    dog_houses_data = [dog_house.serialize() for dog_house in dog_houses]
    return jsonify(dog_houses_data)

# Route to create a new dog house
@app.route('/api/dog_houses', methods=['POST'])
def create_dog_house():
    data = request.get_json()  # Parse JSON data from the request
    if data:
        # Extract data from the JSON object
        name = data.get('name')
        location = data.get('location')
        description = data.get('description')

        if name and location:
            new_dog_house = DogHouse(name=name, location=location, description=description)
            db.session.add(new_dog_house)
            db.session.commit()
            return jsonify({'message': 'Dog house created successfully'})
        else:
            return jsonify({'error': 'Name and location are required fields'})
    else:
        return jsonify({'error': 'Invalid JSON data'})


# Example route to get a specific dog house by ID
@app.route('/api/dog_houses/<int:dog_house_id>', methods=['GET'])
def get_dog_house(dog_house_id):
    dog_house = DogHouse.query.get(dog_house_id)
    if dog_house:
        return jsonify(dog_house.serialize())
    else:
        return jsonify({'error': 'Dog house not found'})

# Add routes for other CRUD actions (update and delete) and for other models (User and Review)

# Route for signing up
@app.route('/api/signup', methods=['POST'])
def signup():
    data = request.get_json()
    # form = UserForm(request.form)

    if data:
        username = data.get('username')
        email = data.get('email')
        password = data.get('password')
        new_user = User(
            username= username,
            email=email,
            password_hash=password
        )
        db.session.add(new_user)
        db.session.commit()
        return jsonify({'message': 'User created successfully'})
    else:
        return jsonify({'error': 'Invalid data'})
    
#Route for Logging in
@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    if not data:
        return jsonify({'error': 'Invalid JSON data'})

    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({'error': 'Invalid credentials'})

    user = User.query.filter(User.email == email).first()

    if user is None or not user.authenticate(password):
        return jsonify({'error': 'Invalid credentials'})

    session['user_id'] = user.id
    return jsonify({'message': 'Logged in successfully!'})
    
# Check session for auto-login
@app.route('/api/check_session')
def check_session():
    user = User.query.filter(User.id == session.get('user_id')).first()
    if user:
        return jsonify(user.to_dict())
    else:
        return '', 204
    
# Clearing the session after logging out
@app.route('/api/logout', methods=['DELETE'])
def logout():
    # Clear the user_id session variable to log the user out
    session.pop('user_id', None)
    return jsonify({'message': 'Logged out successfully'}), 200

if __name__ == '__main__':
    app.run(debug=True, port=5555)
