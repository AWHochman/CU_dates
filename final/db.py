from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy() 


association_table = db.Table('association', db.Model.metadata,
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('community_id', db.Integer, db.ForeignKey('community.id'))
)

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    age = db.Column(db.Integer, nullable=False)
    bio = db.Column(db.String, nullable=False)
    matches = db.relationship('Match', cascade='delete')
    communities = db.relationship('Community', secondary=association_table, back_populates='members')

    def __init__(self, **kwargs):
        self.name = kwargs.get('name', '')
        self.age = kwargs.get('age', '')
        self.bio = kwargs.get('bio', '')

    def serialize(self):
        return {
            'id': self.id, 
            'name': self.name,
            'age': self.age,
            'bio': self.bio,
            'matches': [m.serialize() for m in self.matches],
            'communities': [c.serialize_no_mem() for c in self.communities]
        }
    
    def serialize_no_com(self):
        return {
            'id': self.id, 
            'name': self.name,
            'age': self.age,
            'bio': self.bio,
            'matches': [m.serialize() for m in self.matches]
        }
    
    def serialize_no_mat(self):
        return {
            'id': self.id, 
            'name': self.name,
            'age': self.age,
            'bio': self.bio
        }

class Match(db.Model):
    __tablename__ = 'matches'
    id = db.Column(db.Integer, primary_key=True)
    user1_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user2_id = db.Column(db.Integer, nullable=False)
    accepted = db.Column(db.Boolean)

    def __init__(self, **kwargs):
        self.accepted = kwargs.get('accepted') 
        self.user1_id = kwargs.get('user1_id')
        self.user2_id = kwargs.get('user2_id')

    def serialize(self):
        return {
            'id': self.id,
            'accepted': self.accepted,
            'user1_id': self.user1_id,
            'user2_id': self.user2_id
        }


class Community(db.Model):
    __tablename__ = 'community'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    description = db.Column(db.String, nullable=False)
    members = db.relationship('User', secondary=association_table, back_populates='communities')

    def __init__(self, **kwargs):
        self.name = kwargs.get('name')
        self.description = kwargs.get('description')

    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'members': [m.serialize_no_mat() for m in self.members]
        }

    def serialize_no_mem(self):
        return {
            'id': self.id,
            'name': self.name, 
            'description': self.description
        }
