import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()

CONN = psycopg2.connect(
    dbname=os.getenv("TEST_DB_NAME"),
    user=os.getenv("TEST_DB_USER"),
    password=os.getenv("TEST_DB_PASSWORD"),
    host=os.getenv("TEST_DB_HOST"),
    port=os.getenv("TEST_DB_PORT"),
    )

def set_inputs_to_none_if_empty(func):
    def wrapper(*args, **kwargs):

        modified_args = tuple(None if arg == '' else arg for arg in args)
        modified_kwargs = {key: (None if value == '' else value) for key, value in kwargs.items()}
        result = func(*modified_args, **modified_kwargs)
        
        return result
    return wrapper


def get_user_exercises(username: str) -> list[str]:
    """Returns the list of exercises currently in the db for that user."""
    cur = CONN.cursor()

    cur.execute(
            """
            SELECT DISTINCT exercise FROM weightlifting
            WHERE user_id = %s
            """, (username,)               
        )
    
    return [s[0] for s in sorted(cur.fetchall())]

@set_inputs_to_none_if_empty
def add_exercise(
    user_id: str,
    exercise: str,
    weight: float,
    reps: int,
    date: str,
    after_wod: bool,
    comment: str
):

    print(user_id, exercise, weight, reps, date, after_wod, comment)
    assert float(weight)
    assert int(reps)

    cur = CONN.cursor()
    cur.execute(
        """
        INSERT INTO weightlifting
        (user_id, exercise, weight, reps, date, after_wod, comment)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (user_id, exercise, weight, reps, date, after_wod, comment)
    )
    CONN.commit()

@set_inputs_to_none_if_empty
def add_amrap(
    user_id: str,
    wod: str,
    timecap: int,
    rounds_plus_reps: str,
    date: str,
    comment: str
):    
    assert int(timecap)

    cur = CONN.cursor()
    cur.execute(
        """
        INSERT INTO amrap
        (user_id, wod, timecap, rounds_plus_reps, date, comment)
        VALUES (%s, %s, %s, %s, %s, %s)
        """, (user_id, wod, timecap, rounds_plus_reps, date, comment)
    )
    CONN.commit()

@set_inputs_to_none_if_empty
def add_emom(
    user_id: str,
    wod: str,
    duration: int,
    date: str,
    comment: str,
):    
    assert int(duration)

    cur = CONN.cursor()
    cur.execute(
        """
        INSERT INTO emom
        (user_id, wod, duration, date, comment)
        VALUES (%s, %s, %s, %s, %s)
        """, (user_id, wod, duration, date, comment)
    )
    CONN.commit()

@set_inputs_to_none_if_empty
def add_cardio(
    user_id: str,
    activity: str,
    distance: float,
    time: float,
    date: str,
    comment: str
):    
    assert float(distance)
    assert float(time)

    cur = CONN.cursor()
    cur.execute(
        """
        INSERT INTO cardio
        (user_id, activity, distance_km, time, date, comment)
        VALUES (%s, %s, %s, %s, %s, %s)
        """, (user_id, activity, distance, time, date, comment)
    )
    CONN.commit()

