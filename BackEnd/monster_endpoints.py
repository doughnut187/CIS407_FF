"""
Filename: monster_endpoints.py

Purpose:
Contains the monster endpoints and functions for the monster_pagelication.

Authors: Jordan Smith
Group: Wholesome as Heck Programmers
Last modified: 11/16/21
"""
import flask
from db_manager import db_mgr
from Fiend_Skeleton import * 

###
#   Globals
###
monster_page = flask.Blueprint('monster_page', __name__)

###
#   Helper functions
###
def get_user_monster_info(user_id):
    # Columns we want to pull from
    desired_columns = ['name', 'species', 'exp', 'level', 'has_finished_quiz']

    # Query that is a bit more complicated than the 
    #   db_mgr can handle
    sql_query = f"""
    SELECT {", ".join(desired_columns)}
    from monsters left join users on monsters.user_id = users.user_id
    WHERE users.user_id = {int(user_id)};
    """
    user_monster_info = db_mgr.submit_query(sql_query)

    # The user doesn't have a monster
    if (user_monster_info == []):
        user_monster_info = [None for _ in range(len(desired_columns) - 1)]
        user_monster_info += db_mgr.get_one_row('users', 'has_finished_quiz', {'user_id': int(user_id)})
    else:
        user_monster_info = user_monster_info[0]

    # Transform results into a dictionary and return
    monster_data = {}
    for i in range(len(desired_columns)):
        monster_data[desired_columns[i]] = user_monster_info[i]

    return monster_data

###
#   Route endpoints
###
"""
Endpoint to get the user's monster info from the database as well as whether or not
    the user has finished the initial quiz
"""
@monster_page.route("/get_user_info", methods=["GET"])
def user_info():
    user_id = flask.request.headers.get("user_token")

    return get_user_monster_info(user_id), 201

"""
Endpoint to level the user's monster up and return the monster's info and quiz status
    Returns 201 if succeeds,
            409 if the user doesn't have a monster,
            500 if the update fails 
"""
@monster_page.route("/level_monster_up", methods=["GET"])
def monster_level_up():
    user_id = flask.request.headers.get("user_token")

    monster_info = get_user_monster_info(user_id)
    
    if monster_info["name"] is None:
        return {'message': 'User does not have a monster'}, 409

    # Probably do something with the fiend class
    currFiend = Fiend(nickname=monster_info["name"],
                      species=monster_info['species'],
                      level=monster_info['level'])
    currFiend.level.levelUp()

    # Update the info in the monster database
    update_res = db_mgr.update_rows("monsters",
                                   {"level": currFiend.tellLevel()},
                                   where_options={"user_id": int(user_id)}
                                   )
    if not update_res:
        return {"message": "Monster could not be leveled up"}, 500

    monster_info["level"] = int(monster_info["level"]) + 1

    return monster_info, 201

"""
Endpoint to reset the user's monster level (FOR TESTING)
"""
@monster_page.route("/reset_monster_level")
def reset_level():
    user_id = flask.request.headers.get("user_token")

    update_res = db_mgr.update_rows("monsters", 
                                    {"level": 1},
                                    where_options={"user_id": int(user_id)})

    if not update_res:
        return {"message": "Monster level could not be reset"}, 500
    
    return {"message": "success"}, 201

"""
Initializes a monster for a user in the database
    Returns 201 if succeeds,
            409 if the user already has a monster
"""
@monster_page.route("/create_monster_for_user", methods=["POST"])
def create_monster():
    request_data = json.loads(flask.request.data)

    user_id = int(request_data['user_id'])
    monster_data = request_data['monster_info']

    # Check if the user already has a monster 
    user_monsters = db_mgr.get_all_rows('monsters',
                                        'monster_id',
                                        {'user_id': user_id}
                                        )
    if (len(user_monsters) > 0):
        return {"message": "User already has a monster"}, 409

    # Insert the new monster into the database
    monster_data['user_id'] = user_id
    insert_result = db_mgr.add_one_row('monsters', monster_data)

    print(insert_result)

    return {"message": "success"}, 201