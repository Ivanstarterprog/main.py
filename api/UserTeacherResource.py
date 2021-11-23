from data import db_session
from data.users import User
from flask_restful import Resource
from flask import jsonify
from api.aborts import abort_if_thing_not_found

class TeacherResource(Resource):
    def get(self, user_id, secret_key):
        if secret_key == 'Kuzpc':
            abort_if_thing_not_found(user_id, User)
            session = db_session.create_session()
            user = session.query(User).get(user_id)
            return jsonify({'Admin user': user.to_dict(
                only=('name', 'familia', 'otch', 'user_id', 'email'))})

    def delete(self, user_id, secret_key):
        if secret_key == 'Kuzpc':
            abort_if_thing_not_found(user_id, User)
            session = db_session.create_session()
            user = session.query(User).get(user_id)
            user.teacher = False
            session.commit()
            return jsonify({'success': 'OK'})

    def post(self, user_id, secret_key):
        if secret_key == 'Kuzpc':
            abort_if_thing_not_found(user_id, User)
            session = db_session.create_session()
            user = session.query(User).get(user_id)
            user.teacher = True
            session.commit()
            return jsonify({'success': 'OK'})

class TeachersListResource(Resource):
    def get(self, secret_key):
        if secret_key == 'geeks_are_cool':
            session = db_session.create_session()
            teachers = session.query(User).filter(User.teacher)
            return jsonify({'admin': [item.to_dict(
                only=('name', 'familia', 'otch', 'user_id', 'email')) for item in teachers]})
