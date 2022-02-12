'''
code: Creating the Workout classes and subclasses
group: Workout assistance Program
author(s): Thomas Joyce
last modified: 17 Nov 2021
'''
from db_manager import *
from collections import defaultdict


class Workout:
    '''
    workout parent class. provides fetch_workout and populate_plan methods
    '''
    def __init__(self, name=None):
        self.name = name
        self.exercises = defaultdict(list)

    def fetch_Workout(self, category):
        '''
        pass category as string of workout type (ie, chest)
        will call for a workout from the database of that type
        prioritizes workouts set as primary
        '''
        exercise = db_mgr.get_all_rows("workouts",["workout_id"],\
                                      {"type": category,"is_priority":1},["and"])
        return exercise
    
    def populate_plan(self):
        '''
        creates the workout plan by calling fetch_workout for each category in 
        the workout plan. The returned values will be a tuple containing the 
        workout id, name, and any equipment needed. 
        '''
        for key in self.exercises:
            self.exercises[key] = self.fetch_Workout(key)


class fullBody(Workout):
    def __init__(self, difficulty="easy"):
        '''
        pass difficulty as string (easy, moderate, hard)
        will call the populate plan in parent workout class to fill exercises
        from workout database. 
        will be a 1 day split
        '''
        self.name = "Full Body"
        self.difficulty = difficulty
        self.exercises = {"Chest":[], "Shoulders":[], "Biceps":[], "Triceps":[],\
                          "Upper Back":[], "Lower Back":[], "Butt":[],\
                          "Thighs":[], "Hamstrings":[], "Calves":[]}
        
    def build(self):
        self.populate_plan()

class pushPull(Workout):
    def __init__(self, difficulty="easy"):
        '''
        pass difficulty as string (easy, moderate, hard)
        will call the populate plan in parent workout class to fill exercises
        from workout database. 
        will be 2 day split
        '''
        self.name = "Push/Pull"
        self.difficulty = difficulty
        self.exercises = {"Chest":[], "Shoulders":[], "Biceps":[], "Triceps":[],\
                          "Upper Back":[], "Abs":[], "Thighs":[], \
                          "Hamstrings":[]}
        
    def build(self):
        self.populate_plan()


class upperLower(Workout):
    def __init__(self, difficulty="easy"):
        '''
        pass difficulty as string (easy, moderate, hard)
        will call the populate plan in parent workout class to fill exercises
        from workout database. 
        will be a 2 day split
        '''
        self.name = "Upper/Lower"
        self.difficulty = difficulty
        self.exercises = {"Chest":[], "Shoulders":[], "Biceps":[], "Triceps":[],\
                          "Upper Back":[], "Lower Back":[], "Butt":[],\
                          "Thighs":[], "Hamstrings":[], "Calves":[]}
        
    def build(self):
        self.populate_plan()



class Strength:
    '''
    parent class for strength workouts
    reps, sets, and days per week set to default
    '''
    def __init__(self, reps=8, sets=3, name=None, days=3, goal="general",\
                 intensity="medium"):
        self.reps = reps
        self.sets = sets
        self.name = name
        self.days = days
        self.goal = goal
        self.intesity = intensity
        if self.intesity == "light":
            self.weight = 0.6
        elif self.intesity == "medium":
            self.weight = 0.7
        else:
            self.weight = 0.8


class Cardio:
    '''
    #todo
    pass duration in minutes as an int 
    pass intesity in as a str, light, medium, heavy for type of workout
    '''
    def __init__(self, name=None, duration=30, intensity="medium"):
        self.name = name
        self.duration = duration
        self.intensity = intensity
    
    def __repr__(self):
        return "test"
    
    def __str__(self):
        return "test"


class Weights(Strength):
    '''
    pass weight in as a float range(0,1) for weight calculations
    pass intesity in as a str, light, medium, heavy for type of workout

    '''
    def __init__(self):
        '''
        by default plan is set to full body
        '''
        self.plan = fullBody()
        super().__init__(self)

    def __repr__(self):
        return "{}".format(self.plan.exercises)
    
    def __str__(self):
        return "{}".format(self.plan.exercises)

    def generate_Workout(self):
        '''
        user data stored when the strength parent class is created will dictate
        which workout is created. 
        '''
        if self.goal == "general":
            self.plan = fullBody()
        elif self.goal == "Strength":
            self.plan = pushPull()
        else:
            self.plan = upperLower()
        self.plan.build()


class Calisthenics(Strength):
    '''
    #todo
    still in progress
    '''
    def __init__(self, duration=None):
        self.duration = duration
        super().__init__(self, reps=8, sets=3, name=None, days=3,\
                         goal="general", intensity="medium")

    def __repr__(self):
        return "test"
    
    def __str__(self):
        return "test"


def make_plan(user_id):
    '''
    pass user_id as a string. 
    Will get all user data from database and then build a workout based off the
    user data. 
    the workout plan is stored in workout logs under the user id. 
    '''
    goal_id = db_mgr.get_one_row("users",["fitness_goal_id"],\
                                 {"user_id": user_id})
    goal = db_mgr.get_one_row("fitnessGoal",["name"], {"name": goal_id})
    w = Weights()
    w.goal = goal
    w.generate_Workout()
    exercises = []
    for exercise in w.plan.exercises:
        exercises.append(w.plan.exercises[exercise][0][0])
    x = ''
    for i in range(len(exercises)):
        x += str(exercises[i])
        if i < (len(exercises) - 1):
            x += ','
    db_mgr.add_one_row("workoutLogs", {"user_id":user_id,\
                       "details": x, "user_has_completed": False,\
                       "user_enjoyment": 0})
    

if __name__ == "__main__":
    # make_plan("1")
    test = db_mgr.get_one_row("workoutLogs",["details"],\
                                 {"user_id": "1"})
    print(test)
    w = Weights()
    w.generate_Workout()
    exercises = []
    for exercise in w.plan.exercises:
        exercises.append(w.plan.exercises[exercise][0][0])
    print(exercises)

    test = db_mgr.get_all_rows("workoutLogs", ["user_id", "details"])
    print(test)