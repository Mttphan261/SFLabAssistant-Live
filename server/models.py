from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy import MetaData
from sqlalchemy.orm import validates
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.ext.hybrid import hybrid_property
from collections import OrderedDict
from flask_login import UserMixin, LoginManager
import re
from datetime import datetime

from config import db, bcrypt

################## Models Below####################

class Character(db.Model, SerializerMixin):
    __tablename__ = 'characters'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    head_img = db.Column(db.String)
    main_img = db.Column(db.String)
    bio = db.Column(db.String)

    #relationships
    moves = db.relationship('Move', back_populates='character')    
    user_characters = db.relationship('UserCharacter', back_populates='character')
    videos = db.relationship('Video', back_populates='character')
    combos = db.relationship('Combo', back_populates='character')


    #serialization
    serialize_rules = ('-moves.character', '-videos.character', '-user_characters.character', '-moves.character',)

    def __repr__(self):
        return f'ID: {self.id}, Name: {self.name}'
    
class Move(db.Model, SerializerMixin):
    __tablename__ = 'moves'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    command = db.Column(db.String)

    character_id = db.Column(db.Integer, db.ForeignKey('characters.id'))

    #relationships
    character = db.relationship('Character', back_populates='moves')

    #serialization
    serialize_rules = ('-character.moves',)

    def __repr__(self):
        return f'Move: {self.id}, Character: {self.character_id}'
    

class Combo(db.Model, SerializerMixin):
    __tablename__ = 'combos'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    notation = db.Column(db.String)

    #FKs
    character_id = db.Column(db.Integer, db.ForeignKey('characters.id'))

    #relationships
    character = db.relationship('Character', back_populates='combos')

    #serialization
    serialize_rules = ('-character.combos',)

    def __repr__(self):
        return f'Combo: {self.id}, Character: {self.character_id}'

class User(db.Model, SerializerMixin, UserMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True, nullable=False)
    _password_hash = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False, unique=True)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    #VALIDATIONS
    @validates('email')
    def validate_email(self, key, email):
        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            raise ValueError('Invalid email format')
        return email

    @validates('username')
    def validate_username(self, key, username):
        if not username and len(username) < 1:
            raise ValueError('Invalid username')
        return username

    #PASSWORD HASHING
    @hybrid_property
    def password_hash(self):
        raise Exception('Password hashes may not be viewed.')
    
    @password_hash.setter
    def password_hash(self, password):
        password_hash = bcrypt.generate_password_hash(
            password.encode('utf-8'))
        self._password_hash = password_hash.decode('utf-8')

    def authenticate(self, password):
        return bcrypt.check_password_hash(
            self._password_hash, password.encode('utf-8'))
    
    #relationships
    user_characters = db.relationship('UserCharacter', back_populates='user')
    videos = db.relationship('Video', back_populates='user')
    training_notes = db.relationship('TrainingNote', back_populates='user')

    #serialization
    # serialize_rules = ('-user.user_characters', '-videos.user', '-user_characters.user')
    serialize_rules = ('-user.user_characters', '-videos', '-user_characters.user', '-training_notes.user')


    def __repr__(self):
        return f'''
        ID: {self.id},
        Username: {self.username},
        Email: {self.email}
        UserCharacters: {self.user_characters}
        '''
    
class UserCharacter(db.Model, SerializerMixin):
    __tablename__ = 'user_characters'
    __table_args__= (
        db.UniqueConstraint('user_id', 'character_id', name='_user_character_uc'),
    )

    id = db.Column(db.Integer, primary_key=True)
    is_main = db.Column(db.Boolean)
    is_alt = db.Column(db.Boolean)
    #SAVED VIDEOS WILL GO HERE

    #FKs
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    character_id = db.Column(db.Integer, db.ForeignKey('characters.id'))
    
    #relationships
    user = db.relationship('User', back_populates='user_characters')
    character = db.relationship('Character', back_populates='user_characters')
    videos = db.relationship('Video', back_populates='user_character', cascade="all, delete-orphan")
    training_notes = db.relationship('TrainingNote', back_populates='user_character', cascade="all, delete-orphan")
    matchups = db.relationship('Matchup', back_populates='user_character', cascade="all,  delete-orphan")

    #serialization
    # serialize_rules = ('-user.user_characters', '-character.user_characters', '-videos.user_character')
    serialize_rules = ('-user.user_characters', '-character.user_characters', '-user_character.user', '-training_notes.user_character', '-matchups.user_character')


    def __repr__(self):
        return f'''
        ID: {self.id}
        Character: {self.character.name}
        User: {self.user.username},
        '''

class Video(db.Model, SerializerMixin):
    __tablename__ = 'videos'

    id=db.Column(db.Integer, primary_key=True)
    title=db.Column(db.String)
    description=db.Column(db.String)
    video_id=db.Column(db.String)
    embed_html=db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())    

    #FKs
    character_id=db.Column(db.Integer, db.ForeignKey('characters.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    user_character_id = db.Column(db.Integer, db.ForeignKey('user_characters.id'))
    
    #relationships
    user = db.relationship('User', back_populates='videos')
    character = db.relationship('Character', back_populates='videos')
    user_character = db.relationship('UserCharacter', back_populates='videos')

    #serialization
    serialize_rules = ('-user.videos', '-character.videos', '-user_character', '-user.user_characters', '-character.user_characters')

class TrainingNote(db.Model, SerializerMixin):
    __tablename__ = 'training_notes'

    id = db.Column(db.Integer, primary_key=True)
    note = db.Column(db.String)

    #FKs
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    user_character_id = db.Column(db.Integer, db.ForeignKey('user_characters.id'))

    #relationships
    user = db.relationship('User', back_populates='training_notes')
    user_character = db.relationship('UserCharacter', back_populates='training_notes')

    #serialization
    serialize_rules = ('-user', '-user_character',) #had to exclude both user and uc to avoid max recurision

class Matchup(db.Model, SerializerMixin):
    __tablename__ = 'matchups'

    id=db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    status = db.Column(db.String)

    #FKs
    user_character_id = db.Column(db.Integer, db.ForeignKey('user_characters.id'))

    #relationships
    user_character = db.relationship('UserCharacter', back_populates='matchups')

    #serialization
    serialize_rules = ('-user_character.matchups',)