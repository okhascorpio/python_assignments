#
# Handels everything related to the todo items in the database
#
#



from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from src.database import db, Users, Todos, STATUS
from datetime import datetime

# todo items related blueprint
todos = Blueprint("todos", __name__, url_prefix="/api/v1/")


####################################################################################################
# set route
@todos.route('/todos', methods=['POST', 'GET'])

# require access token
@jwt_required()
def todo_items():
    # get current user's identity
    current_user = get_jwt_identity()
    user = Users.query.filter_by(id=current_user).first()


# Handle POST requests ie create new todo item
    if request.method == 'POST':

        # if not provided, default empty
        name = request.json.get('name', '')
        if name=='': return {'error':'item should have a name at least'}
        # optional description, default empty
        description = request.json.get('description', '')

        # if not provided default status is set to NotStarted
        status = request.json.get('status', 'NotStarted')

        # if status provided, check if it is in the STATUS ENUM class in database
        if STATUS.has_key(status) == False:
            return {'error': "can only be one of these 'OnGoing','NotStarted','Completed'"}

        # create a todo item comprising given data
        todo_item = Todos(user_id=current_user, name=name,
                          description=description, status=status)

        # add todo item in the database
        db.session.add(todo_item)
        db.session.commit()

        return {'message': 'todo item added','user':user.email}




####################################################################################################
# Handel Get requests

    else:  # if request is not POST, it must be GET

        # if status parameter is given in the URL
        if 'status' in request.args:  # parameter is specified
            status = request.args.get('status', type=str)

            # if status parameter is present, check if is in allowed STATUS from database
            if STATUS.has_key(status):

                # query database based on current user id AND the status
                todo_items = Todos.query.filter_by(
                    user_id=current_user, status=status)

            # if status was not in the allowed STATUS ENUM in the database
            else:
                return {'error': "argument can only be one of these 'OnGoing','NotStarted','Completed'"}

        # if no parameter named 'status' is given return all items
        else:
            todo_items = Todos.query.filter_by(user_id=current_user)

        # collect all requested items in an array
        data = []
        for todo_item in todo_items:
            data.append(
                {'id': todo_item.id,
                 'user': todo_item.user_id,
                 'name': todo_item.name,
                 'description': todo_item.description,
                 'status': todo_item.status
                 }
            )
        return ({'items': data})





####################################################################################################
# Handel PUT requests for Updates

# set url end point with integer id of the todo item
@todos.put("/todos:<int:id>")
# acceww token is required to use this resourse
@jwt_required()
def update_todo_item(id):

    # get current user's identity
    current_user = get_jwt_identity()
    user = Users.query.filter_by(id=current_user).first()

    # fetch todo item based on the given id number and the current user identity
    todo_item = Todos.query.filter_by(user_id=current_user, id=id).first()

    # if todo item is not found for the current user
    if not todo_item:
        return {
            'error': 'todo item not found, send correct id',
            'user' : user.email
        }

    # if item is found we can update its fields
    else:

        # if no name is provided, keeps original name
        name = request.json.get('name', '')

        # optional description, if not provided keeps original
        description = request.json.get('description', '')

        # optional status, if not provided keep original
        status = request.json.get('status', '')

        # if status is provided but is not one of the allowed options
        if status != '' and STATUS.has_key(status) == False:
            return {'error': "can only be one of these 'OnGoing','NotStarted','Completed'"}

        # if all provided data is correct, go ahead and update required fields
        else:

            # if no name is provided keep original, if provided then update
            if name != '':
                todo_item.name = name

        # if no description is provided keep original, if provided then update
            if description != '':
                todo_item.description = description

        # if no status is provided keep original, if provided then update
            if status != '':
                todo_item.status = status

        # update the update_at timestamp
            todo_item.updated_at = datetime.now()

        # commit changes to the database
            db.session.commit()

        return jsonify({'message':'item updated'},{
            'id': todo_item.id,
            'user': todo_item.user_id,
            'name': todo_item.name,
            'description': todo_item.description,
            'status': todo_item.status
        }
        )




####################################################################################################
# Handel DELETE requests

# delete route with item id integer in url
@todos.delete("/todos:<int:id>")
# require authentication access token
@jwt_required()
def delete_todo_item(id):

    # get id of current user
    current_user = get_jwt_identity()
    user = Users.query.filter_by(id=current_user).first()

    # query todo item based on current user id and item id
    todo_item = Todos.query.filter_by(user_id=current_user, id=id).first()

    # if no item found corresponding to the current user and providid item id
    if not todo_item:
        return {
            'error': 'todo item not found, send correct id',
            'user':user.email
        }

    # if item is found
    else:

        # delete item
        db.session.delete(todo_item)
        
        # commit changes to datanase
        db.session.commit()

        return {'message': 'requested item deleted'}

####################################################################################################
# END