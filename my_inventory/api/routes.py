from flask import Blueprint, request, jsonify
from my_inventory.helpers import token_required
from my_inventory.models import Stories, db, User, Stories, story_schema, stories_schema


api = Blueprint('api', __name__, url_prefix='/api')



@api.route('/getdata')
def getdata():
    return {'some_value': 52, 'another_value': 800}

# CREATE STORY ENDPOINT
@api.route('/stories', methods = ['POST'])
@token_required
def create_story(current_user_token):
    print(request.get_json())
    name = request.json["name"]
    summary = request.json['summary']
    category = request.json['category']
    relevantdx = request.json['relevantdx']
    user_token = current_user_token.token

    print(f'TESTER: {current_user_token.token}')

    story = Stories(name,summary,category,relevantdx,user_token=user_token)

    db.session.add(story)
    db.session.commit()

    response = story_schema.dump(story)
    return jsonify(response)

# RETRIEVE ALL STORIES
@api.route('/stories', methods = ['GET'])
@token_required
def get_stories(current_user_token):
    owner = current_user_token.token
    story = Stories.query.filter_by(user_token = owner).all()
    response = stories_schema.dump(story)
    return jsonify(response)


#RETRIEVE SINGLE STORY ENDPOINT
@api.route('/stories/<id>', methods = ['GET'])
@token_required
def get_story(current_user_token, id):
    story = Stories.query.get(id)
    response = story_schema.dump(story)
    return jsonify(response)

#UPDATE A STORY BY ID ENDPOINT
@api.route('/stories/<id>', methods = ['POST'])
@token_required
def update_story(current_user_token, id):
    story = Stories.query.get(id)
    print(story)
    story.name = request.json['name']
    story.summary = request.json['summary']
    story.category = request.json['category']
    story.relevantdx = request.json['relevantdx']
    story.user_token = current_user_token.token

    response = story_schema.dump(story)
    return jsonify(response)

#DELETE STORY BY ID
@api.route('/stories/<id>', methods = ['DELETE'])
@token_required
def delete_story(current_user_token, id):
    story = Stories.query.get(id)
    if story:
        db.session.delete(story)
        db.session.commit()

        response = story_schema.dump(story)
        return jsonify(response)
    else:
        return jsonify({'Error': 'That story does not exist in this repository.'})