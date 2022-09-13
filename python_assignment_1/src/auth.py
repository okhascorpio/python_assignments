#
# Handels everything related to the users of the database
#



from flask import Blueprint, request
from werkzeug.security import check_password_hash, generate_password_hash
from src.database import db, Users
from flask_jwt_extended import jwt_required, get_jwt_identity, create_refresh_token, create_access_token
from datetime import datetime


# user related blueprint
auth = Blueprint("auth", __name__, url_prefix="/api/v1/")



####################################################################################################
# Handle signup requests

@auth.post('/signup')
def sign_up():

    # Post jason data, email and password  {"email":"example@example.com","password":"YourPassword}"

    email = request.json.get('email', '')
    password = request.json.get('password', '')

    if Users.query.filter_by(email=email).first() is not None:
        return {'error': 'Email is taken'}

    pwd_hash = generate_password_hash(password)

    user = Users(email=email, password=pwd_hash)

    db.session.add(user)
    db.session.commit()

    return {'message': 'User created'}





####################################################################################################
# handle signin requests

@auth.post('/signin')
def sign_in():
    email = request.json.get('email', '')
    password = request.json.get('password', '')

    # query user from the database 
    user = Users.query.filter_by(email=email).first()

    # If user exists:
    if user:

        # check if password is correct:
        pass_check = check_password_hash(user.password, password)
    
        # if password hash match the stored data
        if pass_check:

            # generate tokens
            refresh = create_refresh_token(identity=user.id)
            access = create_access_token(identity=user.id)
            
            # return access/refresh token
            return {
                'user': {
                    'access token': access,
                    'user': user.email,
                    'user id':user.id
                }
            }

        #if password didnt match stored data
        else:
            return {'message': 'incorrect Password'}

    # if requested email was not found in database
    else:
        return "User not found"




####################################################################################################
# handle password change requests

@auth.put('/changePassword')

#require access token from current loged in user
@jwt_required()
def change_password():

    # get the id of current user
    current_user = get_jwt_identity() 
    # receive new password in json format from the user
    new_password = request.json.get('password', '')

    # Check if no password is porvided
    if new_password == '':
        return {'error': 'password cannot be empty'}

    # update the new password
    else:
        user = Users.query.filter_by(id=current_user).first()
        user.password = generate_password_hash(new_password)
        user.updated_at=datetime.now()
        db.session.commit()
        
        return {'user email': user.email,'message':'password changed'}



####################################################################################################
# END