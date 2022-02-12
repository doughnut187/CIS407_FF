'''
code: gets users latest workout from the DB for use in the front end.
group: Wholesome as Heck Programmers
author(s): Thomas Joyce
last modified: 20 Nov 2021
ref:

'''

from db_manager import *

# Gets the most recent workoutlog 
def most_recent_workout(user_id, columns=["*"]):
    sql = f"SELECT {','.join(columns)} FROM workoutLogs WHERE user_id={user_id}\
          ORDER BY time_created DESC LIMIT 1"

    return db_mgr.submit_query(sql)

def fetch_Workout(workout_id):
        '''
        pass id as an int (10)
        will call for a workout from the database of that id
        '''
        exercise = db_mgr.get_all_rows("workouts",["name"],\
                                      {"workout_id": workout_id})
        return exercise

def get_plan(user_id):
    '''
    Main method. Call this to run.
    pass user_id as a string. 
    Will get user's latest workout plan from database
    returns a string.
    '''
    user_plan_raw = most_recent_workout(user_id, columns=["details"])
    if user_plan_raw:
        user_plan = ""
        plan_list = user_plan_raw[0][0].strip("[]")
        plan_list = plan_list.replace("'", "")
        plan_list = plan_list.replace(" ", "")
        plan_list = plan_list.split(",")
        for exercise in plan_list:
            workout_raw = fetch_Workout(int(exercise))
            if workout_raw:
                user_plan += workout_raw[0][0]
                user_plan += ": 3 sets of 8 reps"
                user_plan += ","
            else:
                user_plan.append("workout not added")
    else:
        user_plan = ["test", "test", "test"]
    return user_plan


if __name__ == "__main__":
    test = get_plan("1")
    print(test)