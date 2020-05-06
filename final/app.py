from flask import Flask, request
from db import db
import json
import dao 

app = Flask(__name__)
db_filename = 'CUDates.db'

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///%s" % db_filename
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = True

db.init_app(app)
with app.app_context():
    db.create_all()


def success_response(data, code=200):
    return json.dumps({"success": True, "data": data}), code

def failure_response(message, code=404):
    return json.dumps({"success": False, "error": message}), code

@app.route('/api/users/')
def get_users():
    return success_response(dao.get_all_users()) 

@app.route('/api/users/', methods=['POST'])
def create_new_user():
    body = json.loads(request.data)
    user = dao.create_user(
        name=body.get('name'),
        age=body.get('age'),
        bio=body.get('bio')
    ) 
    return success_response(user, 201)

@app.route('/api/users/<int:user_id>/')
def get_user_by_id(user_id):
    user = dao.get_user_by_id(user_id)
    if user is not None:
        return success_response(user)
    return failure_response('User could not be found') 

@app.route('/api/users/<int:user_id>/', methods=['DELETE'])
def delete_user_by_id(user_id):
    user = dao.delete_user_by_id(user_id)
    if user is not None:
        return success_response(user)
    return failure_response('User could not be found') 

@app.route('/api/users/<int:user_id>/browse/')
def get_potential_match(user_id):
    user2 = dao.get_potential_match(user_id)
    if user2 is not None:
        return success_response(user2)
    return failure_response('No Available Matches') 

@app.route('/api/users/<int:user_id>/browse/', methods=['POST'])
def create_match(user_id):
    body = json.loads(request.data)
    match = dao.create_match(
        user1_id=user_id,
        user2_id=body.get('user2_id'),
        accepted=body.get('accepted')
    )
    # if match is None then it must be a duplicate (explained further in dao)
    if match is None:
        return failure_response('Duplicate match created')
    return success_response(match)

    # want to return another potential match
    """user2 = dao.get_potential_match(user_id)
    if user2 is not None:
        return success_response(user2)
    return failure_response('No Available Matches')"""

@app.route('/api/users/<int:user_id>/matches/')
def get_matches(user_id):
    return success_response(dao.get_matches_by_id(user_id))

@app.route('/api/communities/')
def get_all_communities():
    return success_response(dao.get_all_communities())

@app.route('/api/communities/', methods=['POST'])
def create_community():
    body = json.loads(request.data)
    community = dao.create_communnity(
        name=body.get('name'),
        description=body.get('description')
    )
    if community is not None:
        return success_response(community)
    return failure_response('Community Could not Be Created')

@app.route('/api/users/<int:user_id>/communities/<int:community_id>/', methods=['POST'])
def join_community(user_id, community_id):
    user = dao.join_community(user_id, community_id)
    if user is not None:
        return success_response(user)
    return failure_response(user)

@app.route('/api/users/<int:user_id>/browse/<int:community_id>/')
def browse_by_community(user_id, community_id):
    user2 = dao.get_potential_match_by_community(user_id, community_id)
    if user2 is not None:
        return success_response(user2)
    return failure_response('No Available Matches or You Are Not A Member of This Community')

@app.route('/api/users/<int:user_id>/browse/<int:community_id>/', methods=['POST'])
def create_match_by_community(user_id, community_id):
    body = json.loads(request.data)
    match = dao.create_match(
        user1_id=user_id,
        user2_id=body.get('user2_id'),
        accepted=body.get('accepted')
    )
    # if match is None then it must be a duplicate (explained further in dao)
    if match is None:
        return failure_response('Duplicate match created')
    return success_response(match)

    """user2 = dao.get_potential_match_by_community(user_id, community_id)
    if user2 is not None:
        return success_response(user2)
    return failure_response('No more matches available')"""

# only for testing 
@app.route('/api/matches/')
def get_all_matches():
    return success_response(dao.get_all_matches())

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
