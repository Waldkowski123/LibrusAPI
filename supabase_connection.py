from supabase import create_client, Client
import os
from dotenv import load_dotenv
load_dotenv()  
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
LIBRUS_LOGIN = os.getenv("LIBRUS_LOGIN")
LIBRUS_PASS = os.getenv("LIBRUS_PASS")
from main import Librus
import json
def insert_data_to_gpt(login, password):
    url = SUPABASE_URL
    key = SUPABASE_KEY

    supabase: Client = create_client(url, key)

    session = Librus()
    session.login(login, password)

    student_info = session.get_student_info()

    teachers = session.get_teachers()

    grades = session.get_grades()

    math_grades = session.get_grades_for_specific_subject('Matematyka')

    events = session.get_events()

    today_events = session.get_today_events()
    all_data = {
        "Student info": student_info,
        "Teachers": teachers,
        "Grades": grades,
        "Math grades": math_grades,
        "Events": events,
        "Today events": today_events
    }
    json_data = json.dumps(all_data)

    data, count = supabase.table('gpt_student_data').select('userid').eq('userid', student_info[4]).execute()
    print(data, count)
    data = list(filter(None, data))

    if len(data) == 2:
        print("User already exists")
    else:
        student_insert = supabase.table('gpt_student_data').insert([{
            'userid': student_info[4],
            'name': student_info[0],
            'summary_file': json_data,
        }])

        student_result = student_insert.execute()
        if isinstance(student_result, str):
            print("Error inserting student:", student_result)
        else:
            print("User has been added")


#write a function that gets the data from the database
def get_data_from_gpt():
    url = SUPABASE_URL
    key = SUPABASE_KEY
    supabase: Client = create_client(url, key)

    #get all the data from the table gpt_student_data
    data, count = supabase.table('gpt_student_data').select('summary_file').execute()
    print(data, count)


insert_data_to_gpt(LIBRUS_LOGIN, LIBRUS_PASS)





