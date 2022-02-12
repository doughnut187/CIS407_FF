"""
Filename: app.py

Authors: Jordan Smith
Group: Wholesome as Heck Programmers
Last modified: 11/19/21
"""
import flask
from flask_restful import reqparse, abort, Api, Resource
from login import login_page
from monster_endpoints import monster_page
from db_manager import db_mgr
import json
import datetime

# Generate the flask app
app = flask.Flask(__name__)
app.register_blueprint(login_page)
app.register_blueprint(monster_page)

# Generate the Api instance
api = Api(app)

# List of table names for abort errors
db_tables = db_mgr.get_tables()

###
#   Helper API functions
###
def get_results(table, arg_columns, where_specifiers, id_name=None, id_value=None):
    try:
        # The id_name and the id_value are optional
        where_options_local = where_specifiers
        if (id_name is not None and id_value is not None):
            where_options_local[id_name] = id_value

        # Specify the AND connections
        and_connections = ["AND" for _ in range(len(where_options_local) - 1)]

        value_results = db_mgr.get_all_rows(table, arg_columns, where_options=where_options_local, where_connectors=and_connections)
    except TypeError:
        abort(500, message="Error: Failure parsing arguments")

    # Store the results in a json format
    json_result = {}
    for row_count, row in enumerate(value_results):
        curr_row = {}
        for col_count, column in enumerate(arg_columns):
            val = row[col_count]

            # If the value returned is a date, we need to convert it to a string 
            if (isinstance(val, datetime.datetime)):
                curr_row[column] = val.strftime("%d/%m/%Y, %H:%M:%S")
            else:
                curr_row[column] = val

        # Append the current json dictionary to the overall dict
        json_result[row_count] = curr_row
    
    return json_result

def post_results(table, data, where_specifiers, id_name=None, id_value=None):
    # Make sure the data is a dictionary
    if (type(data) is not dict):
        abort(405, message="Error: Data must be a dictionary")

    where_options_local = where_specifiers
    if (id_name is not None and id_value is not None):
        where_options_local[id_name] = id_value

    # Specify the AND connections
    and_connections = ["AND" for _ in range(len(where_options_local) - 1)]

    update_results = db_mgr.update_rows(table, data, where_options=where_options_local, where_connectors=and_connections)

    if (update_results):
        return {"message": f"Rows of {table} has been updated"}, 201
    return {"message": f"Rows of {table} could not be updated"}, 500

    

###
#   Rest API Endpoint classes
#   First class requires an id to be tacked onto the end of the endpoint, and second class does not
#
#   Class Methods:
#       get     -> Used to retrieve data (takes in an id from the uri and wants list data for columns)
#       post    -> Used to update data   (takes in an id from the uri and wants dict data for new data)
#       put     -> Used to create data   (wants data to store) (TODO)
###
class ApiInfoPointSpec(Resource):
    def get(self, table_name, id):
        # Try to get the arguments to the user
        try: 
            args = json.loads(flask.request.data)
        except json.decoder.JSONDecodeError:
            args = {}

        # If no where specifiers are sent, just leave it as an empty dict
        if "where" not in args:
            args['where'] = {}

        # If column data was not sent, use all of the columns from the table
        if "columns" not in args:
            args['columns'] = [col[0] for col in db_mgr.get_table_columns(table_name)]

        primary_key = db_mgr.get_table_primary_key(table_name)

        return get_results(table_name, args['columns'], args['where'], primary_key, id), 201

    def post(self, table_name, id):
        args = json.loads(flask.request.data)

        # Throw a fit if data is not sent
        if "data" not in args:
            abort(405, "Data is required for POST method")

        # If no where specifiers are sent, just leave it as an empty dict
        if "where" not in args:
            args['where'] = {}

        primary_key = db_mgr.get_table_primary_key(table_name)

        return post_results(table_name, args['data'], args['where'], primary_key, id), 201


class ApiInfoPoint(Resource):
    def get(self, table_name):
        # Try to get the arguments to the user
        try: 
            args = json.loads(flask.request.data)
        except json.decoder.JSONDecodeError:
            args = {}
        
        # If no where specifiers are sent, just leave it as an empty dict
        if "where" not in args:
            args['where'] = {}

        # If column data was not sent, use all of the columns from the table
        if "columns" not in args:
            args['columns'] = [col[0] for col in db_mgr.get_table_columns(table_name)]

        return get_results(table_name, args['columns'], args['where']), 201

    def post(self, table_name):
        args = json.loads(flask.request.data)

        # Throw a fit if data is not sent
        if "data" not in args:
            abort(405, "Data is required for POST method")

        # If no where specifiers are sent, just leave it as an empty dict
        if "where" not in args:
            args['where'] = {}

        return post_results(table_name, args['data'], args['where']), 201

# Add the api endpoints to the api and connect them to their class
api.add_resource(ApiInfoPoint, '/api/<table_name>')
api.add_resource(ApiInfoPointSpec, '/api/<table_name>/<int:id>')


###
#   More specific endpoints
###
@app.route('/test')
def test():
    return "Hello World"

"""
Endpoint to reset a user's quiz status (FOR TESTING)
    Returns 201 on success, 500 on failure
"""
@app.route("/reset_user_quiz")
def reset_quiz():
    user_id = flask.request.headers.get("user_token")

    res = db_mgr.update_rows("users", {"has_finished_quiz": False}, where_options={"user_id": user_id})

    if res:
        return {'message': 'success'}, 201
    else:
        return {'message': 'failure'}, 500

"""
Endpoint to get and store the data from a user's quiz
"""
@app.route("/submit_user_quiz", methods=["PUT", "POST"])
def submit_user_quiz():
    request_data = json.loads(flask.request.data)

    # Load the results from the quiz
    user_id = request_data['user_id']
    quiz_results = request_data['quiz_results']

    # Split the data into what needs to be stored into the monsters table and what needs to be stored in the users table
    monster_keys = ["species"]
    user_keys = ["experience", "daysPerWeek", "availableEquipment"]

    filterByKeys = lambda keys: {x: quiz_results[x] for x in keys}

    monster_data = filterByKeys(monster_keys)
    user_data = filterByKeys(user_keys)

    # Add the user id to the monster data and set the user's quiz status to completed
    monster_data['user_id'] = user_id
    user_data['has_finished_quiz'] = True

    # Store the data in the database
    user_update_res = db_mgr.update_rows("users", user_data, where_options={"user_id": user_id}) 
    monster_insert_res = db_mgr.add_one_row("monsters", monster_data)

    if not user_update_res or not monster_insert_res:
        return {'message': 'Error inserting data'}, 500

    return {'message': 'success'}, 201

# Gets the most recent workoutlog 
def most_recent_workoutlog(user_id, columns=["*"]):
    sql = f"SELECT {','.join(columns)} FROM workoutLogs WHERE user_id={user_id} ORDER BY time_created LIMIT 1"

    return db_mgr.submit_query(sql)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port="5000", debug=True)

