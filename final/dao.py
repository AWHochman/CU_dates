from db import db, Match, User, Community

def get_all_users():
    return [u.serialize_no_mat() for u in User.query.all()]

def create_user(name, age, bio):
    new_user = User(
        name=name, 
        age=age, 
        bio=bio
    )

    db.session.add(new_user)
    db.session.commit()
    return new_user.serialize() 

def get_user_by_id(user_id):
    user = db.session.query(User).filter_by(id=user_id).first()
    if user is None:
        return None
    user = user.serialize()
    user['matches'] = get_matches_by_id(user_id)
    print(get_matches_by_id(user_id))
    return user

"""def get_user_by_id_noMatches(user_id):
    user = db.session.query(User).filter_by(id=user_id).first()
    user = user.serialize()
    del user['matches']
    return user"""

def delete_user_by_id(user_id):
    user = db.session.query(User).filter_by(id=user_id).first()
    if user is None:
        return None
    db.session.delete(user)
    db.session.commit()
    return user.serialize()


def create_match(user1_id, user2_id, accepted):
    match = db.session.query(Match).filter_by(user1_id=user2_id, user2_id=user1_id).first()

    # matchB should never exist
    # If it does then it means that user1 must have seen user2 before
    # The way the program is written someone should only ever 'swipe' on another person one time
    matchB = db.session.query(Match).filter_by(user1_id=user1_id, user2_id=user2_id).first()
    if matchB is not None:
        return None

    if match is not None:
        match.accepted = accepted 
        db.session.commit()
        return match.serialize()

    # accepted can only be changed to true when user2 also accepts
    # if accepted is ever set to false then it will remain that way 
    if accepted == True: 
        accepted = None

    new_match = Match(
        user1_id=user1_id,
        user2_id=user2_id,
        accepted=accepted
    )
    
    db.session.add(new_match)
    db.session.commit()
    return new_match.serialize()


def get_potential_match(user1_id):
    """
    We want to find a user that user1 has a chance of being matched with. 
    This means that user1 and another user have not been either previously
    matched or if they have then it was the other user (not user1) who 
    'swiped right' giving user1 the opportunity to accept the match.
    """
    users = db.session.query(User).filter(User.id != user1_id).all()
    for user in users:
        if potential_match(user1_id, user.id):
            return user.serialize_no_mat()
        

def get_matches_by_id(user_id):
    user = db.session.query(User).filter_by(id=user_id).first()
    potential_matches = db.session.query(Match).filter_by(user2_id=user_id).all()
    matches = []
    for match in potential_matches:
        if match.accepted == True:
            matches.append(match)
    return [m.serialize() for m in user.matches+matches if m.accepted == True]

        
def get_all_matches():
    return [m.serialize() for m in Match.query.all()]


def potential_match(user1_id, user2_id):
    matchA = db.session.query(Match).filter_by(user1_id=user1_id, user2_id=user2_id).first()
    matchB = db.session.query(Match).filter_by(user1_id=user2_id, user2_id=user1_id).first()

    if matchA is None and matchB is None:
        return True  
    elif matchB is not None and matchB.accepted == None:
        return True 
    return False

def get_all_communities():
    return [c.serialize() for c in Community.query.all()]

def create_communnity(name, description):
    new_community = Community(
        name=name,
        description=description
    )
    db.session.add(new_community)
    db.session.commit()
    return new_community.serialize()

def join_community(user_id, community_id):
    user = User.query.filter_by(id=user_id).first()
    community = Community.query.filter_by(id=community_id).first()
    if user is None or community is None:
        return None
    community.members.append(user)
    db.session.commit()
    return user.serialize()

def get_potential_match_by_community(user1_id, community_id):
    community = Community.query.filter_by(id=community_id).first()
    members = community.members
    user = User.query.filter_by(id=user1_id).first()
    try:
        del members[members.index(user)]
    except:
        return None
    for member in members:
        if potential_match(user1_id, member.id):
            return member.serialize_no_mat()
    return None