from flask_migrate import Migrate
from models import Character, Move, User, UserCharacter, Video, TrainingNote, Matchup
from flask import Flask, request, session, make_response, jsonify, redirect
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from config import app, db, api, Resource
import ipdb
import traceback
from YouTubeAPI import fetch_videos


migrate = Migrate(app, db)
login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.filter_by(id=user_id).first()

class Characters(Resource):
    def get(self):
        try:
            characters = [c.to_dict() for c in Character.query.all()]
            return characters, 200
        except:
            return {'error' : 'characters not found'}, 404

api.add_resource(Characters, '/characters')

class CharacterByName(Resource):
    def get(self, name):
        try:
            character = Character.query.filter_by(name=name).first().to_dict()
            return character, 200
        except:
            return {'error': 'fighter not found'}, 404

api.add_resource(CharacterByName, '/characters/<string:name>')

class UserCharacters(Resource):
    @login_required
    def post(self):
        try:            
            data = request.get_json()
            name = data['name']
            user = current_user
            character = Character.query.filter_by(name=name).first()
            characters = Character.query.all()

            already_in_roster = UserCharacter.query.filter_by(
                user_id = user.id,
                character_id = character.id
            ).first()

            if already_in_roster:
                return {"message": "Character already exists in the user's roster"}, 400    

            new_user_character = UserCharacter(
                user_id = user.id,
                character_id = character.id,
                is_main = False,
                is_alt = False
            )


            db.session.add(new_user_character)
            db.session.commit()
            
            for opponent_character in characters:
                matchup=Matchup(
                    user_character_id = new_user_character.id,
                    name = opponent_character.name,
                    status = 'neutral'
                )
                db.session.add(matchup)
            db.session.commit()

            return new_user_character.to_dict(), 201
        
        except Exception as e:
            traceback.print_exc()
            return {"error": "UserCharacter failed.", "message": str(e)}, 500 
        
api.add_resource(UserCharacters, '/usercharacters')

class UserCharacterByID(Resource):
    @login_required
    def delete(self, user_character_id):
        try:
            deleted_uc = UserCharacter.query.get(user_character_id)
            if not deleted_uc or deleted_uc.user_id != current_user.id:
                return {'error': 'User character not found'}, 404
            db.session.delete(deleted_uc)
            db.session.commit()
            return {'message': 'Character deleted from user roster'}
        
        except Exception as e:
            traceback.print.exc()
            return {'error': 'Failed to delete character from user roster', 'message': str(e)}, 500  

api.add_resource(UserCharacterByID, '/usercharacters/<int:user_character_id>')

#**********AUTHENTICATION ROUTES**********
class Users(Resource):
    @login_required
    def get(self):
        # try:
            user = current_user
            if user:
                # return {
                #     "id": user.id,
                #     "username": user.username,
                #     "email": user.email,
                #     # "videos": user.videos,'TypeError: Object of type Video is not JSON serializable'
                #     "user_characters": [uc.to_dict() for uc in user.user_characters]
                # }, 200
                return user.to_dict()
            else:
                return {"error": "User not found"}, 404
        # except:
        #     return {"error": "An error occurred while fetching the user"}, 500
    
    @login_required
    def delete(self):
        try:
            user = current_user
            if user:
                db.session.delete(user)
                db.session.commit()
                return {}, 204
            else:
                return {"error": "User not found"}, 404
        except:
            return {"error":"An error occurred while deleting the user"}, 500


api.add_resource(Users, '/users')

class Signup(Resource):
    def post(self):
        try:
            data = request.get_json()
            new_user = User(
                username=data['username'],
                email=data['email'],
            )
            new_user.password_hash = data['password']
            db.session.add(new_user)
            db.session.commit()

            # session['user_id'] = new_user.id
            login_user(new_user, remember=True)

            return new_user.to_dict(), 201
        
        except Exception as e:
            traceback.print_exc()
            return {"error": "Signup failed.", "message": str(e)}, 500

api.add_resource(Signup, '/signup')


class Login(Resource):

    def post(self):
        try:
            data = request.get_json()
            username = data.get('username')
            password = data.get('password')

            user = User.query.filter(User.username == username).first()

            if user:
                if user.authenticate(password):
                    login_user(user, remember=True)
                    return user.to_dict(), 200
            return {'error': '401 Unauthorized'}, 401
        
        except Exception as e:
            traceback.print_exc()
            return {"error": "Signup failed.", "message": str(e)}, 500        


api.add_resource(Login, '/login')

class CheckSession(Resource):
    def get(self):
        if current_user.is_authenticated:
            user = current_user.to_dict()
            return user, 200
        return {"error": "unauthorized"}, 401

api.add_resource(CheckSession, '/check_session')

@app.route("/logout", methods=["POST"])
@login_required
def logout():
    logout_user()
    return f'You have logged out. Goodbye'

class Videos(Resource):
    @login_required
    def post(self):
        try:
            data = request.get_json()
            character_id = data['character_id']
            video_id = data['video_id']

            video_data = fetch_videos([video_id])
            if video_data:
                video_info = video_data[0]
                title = video_info['title']
                description = video_info['description']
                embed_html = video_info['embed_html']

                video = Video(
                    title = title,
                    description = description,
                    video_id = video_id,
                    embed_html = embed_html,
                    character_id = character_id,
                    user_id = current_user.id
                )
                db.session.add(video)
                db.session.commit()
                return video.to_dict(), 201
            
        except Exception as e:
            traceback.print_exc()
            return {"error": "Video Submission failed", "message": str(e)}, 500

api.add_resource(Videos, '/videos')


class UserCharacterVideos(Resource):
    @login_required
    def post(self, user_character_id):
        try:
            user_character = UserCharacter.query.get(user_character_id)

            if not user_character or user_character.user_id != current_user.id:
                return {'error': 'User character not found'}, 404
            data = request.get_json()
            title = data.get('title')
            description = data.get('description')
            video_id = data.get('video_id')
            embed_html = data.get('embed_html')

            video = Video(
                title=title,
                description=description,
                video_id=video_id,
                embed_html=embed_html,
                user_character_id=user_character_id
            )

            db.session.add(video)
            db.session.commit()

            return video.to_dict(), 201
        except Exception as e:
            traceback.print.exc()
            return {'error': 'Failed to add video to user character', 'message': str(e)}, 500
        
    @login_required
    def delete(self, user_character_id):
        data = request.get_json()
        videoId = data.get('videoId')
        try:
            user_character = UserCharacter.query.get(user_character_id)
            deleted_video = Video.query.get(videoId)

            if not user_character or not deleted_video or user_character.user_id != current_user.id:
                return {'error': 'User character or video not found'}, 404

            db.session.delete(deleted_video)
            db.session.commit()
            return {'message': 'User character video deleted'}, 200
        
        except Exception as e:
            traceback.print.exc()
            return {'error': 'Failed to delete video for user character', 'message': str(e)}, 500  
        
api.add_resource(UserCharacterVideos, '/usercharacters/<int:user_character_id>/videos')


class TrainingNotes(Resource):
    @login_required
    def post(self, user_character_id):
        try:
            user_character = UserCharacter.query.get(user_character_id)

            if not user_character or user_character.user_id != current_user.id:
                return {'error': 'User character not found'}, 404
            data = request.get_json()
            note = data.get('note')

            new_training_note = TrainingNote(
                note = note,
                user_id = current_user.id,
                user_character_id = user_character_id
            )
            db.session.add(new_training_note)
            db.session.commit()
            return new_training_note.to_dict()
        except Exception as e:
            traceback.print.exc()
            return {'error': 'Failed to add video to user character', 'message': str(e)}, 500   

    @login_required
    def delete(self, user_character_id):
        data = request.get_json()
        note_id = data.get('note_id')
        try:
            user_character = UserCharacter.query.get(user_character_id)
            training_note = TrainingNote.query.get(note_id)

            if not user_character or not training_note or user_character.user_id != current_user.id:
                return {'error': 'User character or training note not found'}, 404

            db.session.delete(training_note)
            db.session.commit()
            return {'message': 'Training note deleted'}, 200
        except Exception as e:
            traceback.print.exc()
            return {'error': 'Failed to add video to user character', 'message': str(e)}, 500  

    @login_required
    def patch(self, user_character_id):
        data = request.get_json()
        note_id = data.get('note_id')
        note = data.get('note')
        try:
            user_character = UserCharacter.query.get(user_character_id)
            training_note = TrainingNote.query.get(note_id)

            if not user_character or not training_note or user_character.user_id != current_user.id:
                return {'error': 'User character or training note not found'}, 404
            
            training_note.note = note
            db.session.add(training_note)
            db.session.commit()

            return training_note.to_dict(), 200
        
        except Exception as e:
            traceback.print.exc()
            return {'error': 'Failed to add video to user character', 'message': str(e)}, 500   

api.add_resource(TrainingNotes, '/usercharacters/<int:user_character_id>/notes')

class Matchups(Resource):
    @login_required
    def patch(self, matchup_id):
        try:
            matchup = Matchup.query.get(matchup_id)

            if not matchup or matchup.user_character.user_id != current_user.id:
                return {'error': 'Matchup not found or does not belong to the current user'}, 404
            
            data = request.get_json()
            new_status = data.get('status')
            matchup.status = new_status
            db.session.commit()

            return matchup.to_dict(), 200
        
        except Exception as e:
            traceback.print_exc()
            return {'error': 'Failed to update matchup status', 'message': str(e)}, 500

api.add_resource(Matchups, '/matchups/<int:matchup_id>')

if __name__ == '__main__':
    app.run(port=5555, debug=True)
