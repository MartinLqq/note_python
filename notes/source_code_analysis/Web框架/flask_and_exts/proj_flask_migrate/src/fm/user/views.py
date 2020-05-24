from flask import jsonify, request

from src import db
from src.fm.models import Person, Address
from src.fm.user import BP_USER


@BP_USER.route('/add', methods=['GET'])
def add_user():
    name = request.args.get('name', 'null')
    email = request.args.get('email', 'null')
    per = Person(name=name)
    db.session.add(per)
    db.session.commit()
    addr = Address(email=email, person_id=per.id)
    db.session.add(addr)
    db.session.commit()
    return jsonify(data={'name': name, 'email': email})


@BP_USER.route('/')
def users():
    pers = db.session.query('name').select_from(Person).all()
    return jsonify(data=pers)
