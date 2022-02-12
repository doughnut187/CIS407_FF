'''
code: email functionality
group: Wholesome as Heck Programmers
author(s): Thomas Joyce
last modified: 20 Nov 2021
ref:
    https://stackoverflow.com/questions/15088037/python-script-to-do-something-at-the-same-time-every-day
    look here for scheduling daily sending functionality. 
'''

from db_manager import *
import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

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

def email(user_email, user_plan):
    '''
    if using a local debugging server, use localhost as SMTP server and use port 
    1025 rather than port 465. won’t need to use login() or encrypt the 
    communication using SSL. SSL (Secure Sockets Layer) is a protocol used to 
    encrypt an SMTP connection. It’s not necessary to use when using a local 
    debugging server.
    '''

    # email contents here
    sender_email = "fitnessfiend.dev@gmail.com"
    sender_pass = "fitnessfiend#1"
    receiver_email = user_email
    #receiver_email = "fraylookalike@gmail.com" #put mine here to test
    message = MIMEMultipart("alternative")
    message["Subject"] = "Workout Plan"
    message["From"] = sender_email
    message["To"] = receiver_email

    # Create the plain-text and HTML version of your message
    text = """\
    Hi,
    Here is your workout plan for the day!
    {}
    To see your plan in more detail visit:
    http://www.FitnessFiends.com
    Let us know how the workout goes!""".format(user_plan)
    html = """\
    <html>
    <body>
        <p>Hi!<br>
        <br>
        Here is your workout plan for the day:<br>
        <br>
        <ul type="disc">{}</ul><br>
        <br>
        To see your plan in more detail visit:
        <a href="https://my-fitness-fiend-vzhj3.ondigitalocean.app/SignIn">Fitness Fiends</a>
        <br>
        </p>
        Let us know how the workout goes!
    </body>
    </html>
    """.format(user_plan)

    # Turn these into plain/html MIMEText objects
    part1 = MIMEText(text, "plain")
    part2 = MIMEText(html, "html")

    # Add HTML/plain-text parts to MIMEMultipart message
    # The email client will try to render the last part first
    message.attach(part1)
    message.attach(part2)
        
    # Create secure connection with server and send email
    context = ssl.create_default_context()
    if localhost == False:
        port = 465 # For SSL
        smtp = "smtp.gmail.com"
        with smtplib.SMTP_SSL(smtp, port, context=context) as server:
            server.login(sender_email, sender_pass)
            server.sendmail(sender_email, receiver_email, message.as_string())
    else:
        port = 1025 # for localhost
        smtp = "localhost"
        with smtplib.SMTP(smtp, port) as server:
            server.sendmail(sender_email, receiver_email, message.as_string())


def get_user(user_id):
    '''
    Main method. Call this to run.
    pass user_id as a string. 
    Will get user email and latest workout plan from database then call email()
    '''
    user_email_raw = db_mgr.get_one_row("users",["email"],\
                                 {"user_id": user_id})
    if user_email_raw:
        user_email = user_email_raw[0].strip()
    else:
        raise Exception('Bad Email')
        #user_email = "test@gmail.com"
    # user_plan_raw = db_mgr.get_one_row("workoutLogs",["details"],\
    #                                   {"user_id": user_id,\
    #                                    "user_has_completed": 0}, ["and"])
    user_plan_raw = most_recent_workout(user_id, columns=["details"])
    if user_plan_raw:
        user_plan = ""
        plan_list = user_plan_raw[0][0].strip("[]")
        plan_list = plan_list.replace("'", "")
        plan_list = plan_list.replace(" ", "")
        plan_list = plan_list.split(",")
        #print("here's the id's for the plan: {}".format(plan_list))
        for exercise in plan_list:
            workout_raw = fetch_Workout(int(exercise))
            # workout_raw = db_mgr.get_one_row("workouts",["name"], \
            #                             {"workout_id": int(exercise)})
            if workout_raw:
                user_plan += workout_raw[0][0]
                user_plan += "&nbsp&nbsp&nbsp&nbsp"
                user_plan += ": 3 sets of 8 reps"
                user_plan += "<br>" #for html formatting
            else:
                user_plan.append("workout not added")
    else:
        user_plan = ["test", "test", "test"]
    # print("end of get_email. Here's what I'm sending: ")
    # print("user_email: {}".format(user_email))
    # print("user_plan: {}".format(user_plan))
    email(user_email, user_plan)


if __name__ == "__main__":
    # to test enter in terminal: py -m smtpd -c DebuggingServer -n localhost:1025
    # then set localhost to True, and run. the output will be in the terminal.
    localhost = False
    get_user("1")