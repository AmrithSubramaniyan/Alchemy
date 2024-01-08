from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app= Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:2630@localhost/flask'
app.config['SQLALCHEMY_TRACK_MODIFICATION'] = False

db = SQLAlchemy(app)

class Azar(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    phone = db.Column(db.VARCHAR(15), unique=True, nullable=False)
    email = db.Column(db.VARCHAR(20), unique=True, nullable=False)


@app.route('/gets', methods=['GET'])
def get_gets():
    getting = Azar.query.all()
    user_list = [{'id': tab.id, 'username': tab.username, 'phone': tab.phone, 'email': tab.email }for tab in getting]
    return jsonify({'gets': user_list})


@app.route('/gets', methods=['post'])
def add_post():
    posting = request.get_json()
    if isinstance(posting, list):
        for upload in posting:
            new_user=Azar(username=upload['username'],email=upload['email'],phone=upload['phone'])
            db.session.add(new_user)
            db.session.commit()

    else:
         new_user = [{'id': upload.id, 'username': upload.username, 'phone': upload.phone, 'email': upload.email }]
         db.session.add(new_user)
         db.session.commit()
         return jsonify({'message': 'Users added successfully'})




if __name__ =='__main__':
    with app.app_context():
        db.create_all()
        app.run(debug=True)