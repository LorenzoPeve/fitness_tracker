from datetime import datetime
import psycopg2

CONN = psycopg2.connect(
    dbname='fitness',
    user='root',
    password='root',
    host='localhost',
    port='5432')

# print(conn)

# cur = conn.cursor()
# cur.execute(
#         """
#         SELECT DISTINCT exercise FROM weightlifting
#         WHERE user_id = %s
#         """, ('lpeve',)
#     )
# print(cur.fetchall())

def get_exercise_records(
    username: str,
    exercise: str,
    reps: float
    ) -> list[tuple]:
    """
    Returns a list of tuples in the form (date, weight_lifted) for a
    given user and exercise.
    """
    cur = CONN.cursor()
    cur.execute(
        """
        SELECT date, weight
        FROM weightlifting
        WHERE
            user_id = %s
            AND exercise = %s
            AND reps = %s
        ORDER BY date DESC;
        """, (username, exercise, reps)               
        )
    
    records = [(i[0], float(i[1])) for i in cur.fetchall()]
    dates = [datetime.combine(i[0], datetime.min.time()) for i in records]
    weights = [i[1] for i in records]
    return dates, weights

dates, weights = get_exercise_records('lpeve', 'deadlift', 5)

print(dates)
print(weights)
from bokeh.plotting import figure, show
p = figure(width=800, height=250, x_axis_type="datetime")
p.scatter(dates, weights, color='navy', alpha=0.5)

show(p)
print(p.y_range)