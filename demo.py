from flask import Flask,request,jsonify
from flask_sqlalchemy import SQLAlchemy

app=Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:2630@localhost/amrith'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    phone = db.Column(db.VARCHAR(100), unique=True, nullable=False)

    def _init_(self,username,phone):
        self.username=username
        self.phone=phone

@app.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()
    user_list = [{'id':user.id, 'username': user.username, 'phone': user.phone} for user in users]
    return jsonify({'users': user_list})

@app.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = User.query.get(user_id)

    if user:
        return jsonify({'id': user.id, 'username': user.username, 'phone': user.phone})
     

    else:
        return jsonify({'error': 'User not found'}), 404
    
@app.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    with app.app_context():
        data = request.get_json()
        user_to_update = User.query.get(user_id)
        if not user_to_update:
            return jsonify({'error': 'User not found'})
        if 'username' in data:
            user_to_update.username = data['username']
        if 'phone' in data:
            user_to_update.phone = data['phone']
        db.session.commit()

        return jsonify({'message': 'User updated successfully'})
       

@app.route('/users', methods=['POST'])
def add_user():
    data = request.get_json()

    if isinstance(data, list):
        for data in data:
            new_user = User(username=data['username'], phone=data['phone'])
            db.session.add(new_user)
            db.session.commit()
            return jsonify({'message': 'Users added successfully'})
    else:
        new_user = User(username=data['username'], phone=data['phone'])
        db.session.add(new_user)
        db.session.commit()
        return jsonify({'message': 'User added successfully'})
                
@app.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    user = User.query.get(user_id)
    if user is None:
        return jsonify({'error': 'User not found'}), 404

    db.session.delete(user)
    db.session.commit()

    return jsonify({'message': 'User deleted successfully'})



                                                                            #main method(OR)Run

if __name__ == '__main__':
    with app.app_context():
     db.create_all()
    app.run(debug=True)

    
    
    


