import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()

def get_db() -> psycopg2.extensions.cursor:
    """Establishes a connection to the database and returns connection object"""
    conn = psycopg2.connect(
        host=os.getenv("TEST_DB_HOST"),
        user=os.getenv("TEST_DB_USER"),
        password=os.getenv("TEST_DB_PASSWORD"),
        port=os.getenv("TEST_DB_PORT"),
    )
    return conn


def add_exercise(
    username: str,
    date: str,
    exercise: str,
    n_reps: int,
    n_sets: int,
    weight: float,
):
    """
    Adds an exercise to the database. In the case of `n_sets>`, it adds a
    record for each set performed.
    """
    conn = get_db()
    cur = conn.cursor()
    for _ in range(n_sets):
        try:
            cur.execute(
                """
                INSERT INTO records (username, date, exercise, reps, weight)
                VALUES (%s, %s, %s, %s, %s)
                """,
                (username, date, exercise, n_reps, weight)
            )
            conn.commit()
        except psycopg2.errors.ForeignKeyViolation as e:
            if "Key (username)" in str(e):
                return 'Invalid username'
            elif "Key (username)" in str(e):
                return 'Invalid exercise'
            else:
                raise e
        else:
            conn.commit()
