from flask import Blueprint, request, jsonify
from marvel_inventory.helpers import token_required
from marvel_inventory.models import Characters, db, User, character_schema, characters_schema
from datetime import datetime

api = Blueprint('api', __name__, url_prefix='/api')



@api.route('/getdata')
def getdata():
    return {'some_value': 52, 'another_value': 800}

# CREATE character ENDPOINT
@api.route('/characters', methods = ['POST'])
@token_required
def create_character(current_user_token):
    print(request.get_json())
    name = request.json["name"]
    description = request.json['description']
    comics_appeared_in = request.json['comics_appeared_in']
    super_power = request.json['super_power']
    owner = current_user_token.token

    print(f'TESTER: {current_user_token.token}')

    character = Characters(name,description,comics_appeared_in,super_power, owner)

    db.session.add(character)
    db.session.commit()

    response = character_schema.dump(character)
    return jsonify(response)

# RETRIEVE ALL characters
@api.route('/characters', methods = ['GET'])
@token_required
def get_characters(current_user_token):
    character = Characters.query.filter_by(owner = current_user_token.token).all()
    response = characters_schema.dump(character)
    return jsonify(response)


#RETRIEVE SINGLE character ENDPOINT
@api.route('/characters/<id>', methods = ['GET'])
@token_required
def get_story(current_user_token, id):
    character = Characters.query.get(id)
    response =character_schema.dump(character)
    return jsonify(response)

#UPDATE Acharacter BY ID ENDPOINT
@api.route('/characters/<id>', methods = ['POST'])
@token_required
def update_character(current_user_token, id):
    character = Characters.query.get(id)
    print(character)
    character.name = request.json['name']
    character.description = request.json['description']
    character.comics_appeared_in = request.json['comics_appeared_in']
    character.super_power = request.json['super_power']
    character.owner = current_user_token.token

    response =character_schema.dump(character)
    db.session.commit()
    return jsonify(response)

#DELETEcharacter BY ID
@api.route('/characters/<id>', methods = ['DELETE'])
@token_required
def delete_character(current_user_token, id):
    character = Characters.query.get(id)
    if character:
        db.session.delete(character)
        db.session.commit()

        response =character_schema.dump(character)
        return jsonify(response)
    else:
        return jsonify({'Error': 'That character does not exist in this repository.'})
