from dotenv import load_dotenv
import psycopg2
import os
import sys
import django

# required for models to load
sys.path.insert(
    0, os.path.abspath(os.path.join(__file__, '..', '..', 'fitness_tracker')))
os.environ['DJANGO_SETTINGS_MODULE'] = 'fitness_tracker.settings'
django.setup()

from app.models import User

load_dotenv()

conn = psycopg2.connect(
    dbname=os.getenv("TEST_DB_NAME"),
    user=os.getenv("TEST_DB_USER"),
    password=os.getenv("TEST_DB_PASSWORD"),
    host=os.getenv("TEST_DB_HOST"),
    port=os.getenv("TEST_DB_PORT"),
)

cur = conn.cursor()

# Add Users ###################################################################
admin = User.objects.create_superuser(
    username="admin",
    password="123",
    first_name="admin",
    last_name="goodadmin",
    email="admin@admin.com",
    dob='2024-01-01'
)
admin.save()

me = User.objects.create_user(
    username="lpeve",
    password='123',
    first_name="Lorenzo",
    last_name="Peve",
    email="lpeve01@gmail.com",
    dob='1996-03-31',
    city='Austin',
    state='Texas',
    country='USA'
)
me.save()


# 2.0 CREATE DB SCHEMA ########################################################
cur.execute("""
CREATE TABLE weightlifting (
    id SERIAL PRIMARY KEY,
	user_id VARCHAR(20) NOT NULL,
	exercise VARCHAR(30) NOT NULL,
	weight NUMERIC(4, 1) NOT NULL CHECK (weight >= 0),
	reps INT NOT NULL CHECK (reps > 0),
	date DATE NOT NULL,
	after_wod BOOLEAN DEFAULT false,
	comment VARCHAR(100) DEFAULT NULL,
	
	FOREIGN KEY (user_id) references app_user(username)
);
            
CREATE TABLE amrap (
    id SERIAL PRIMARY KEY,
	user_id VARCHAR(20) NOT NULL,
	wod VARCHAR(200) NOT NULL,
	timecap INT NOT NULL, -- minutes
	rounds_plus_reps VARCHAR(10) NOT NULL,
	date DATE NOT NULL,
	comment VARCHAR(100) DEFAULT NULL,
	
	FOREIGN KEY (user_id) references app_user(username),
	CONSTRAINT valid_amrap_score CHECK (rounds_plus_reps ~ '[0-9]+\+*[0-9]*')
);
            
CREATE TABLE emom (
    id SERIAL PRIMARY KEY,
	user_id VARCHAR(20) NOT NULL,
	wod VARCHAR(200) NOT NULL,
	duration INT NOT NULL, -- minutes
	date DATE NOT NULL,
	comment VARCHAR(100) DEFAULT NULL,
	
	FOREIGN KEY (user_id) references app_user(username)
);

CREATE TABLE rounds_for_time (
    id SERIAL PRIMARY KEY,
	user_id VARCHAR(20) NOT NULL,
	wod VARCHAR(200) NOT NULL,
	rounds INT NOT NULL,
	time NUMERIC(5, 2) NOT NULL,  -- minutes
	date DATE NOT NULL,
	comment VARCHAR(100) DEFAULT NULL,
	
	FOREIGN KEY (user_id) references app_user(username)
);
            
CREATE TABLE hero_and_benchmarks_wods (
    user_id VARCHAR(20),
    name VARCHAR(20),
	description VARCHAR(200) NOT NULL,
    
    PRIMARY KEY(user_id, name),
    FOREIGN KEY (user_id) references app_user(username)
);

CREATE TABLE hero_and_benchmarks (
    id SERIAL PRIMARY KEY,
	user_id VARCHAR(20) NOT NULL,
	name VARCHAR(20) NOT NULL,
	time NUMERIC(5, 2) NOT NULL,  -- minutes
	date DATE NOT NULL,
	comment VARCHAR(100) DEFAULT NULL,
	
	FOREIGN KEY (user_id) references app_user(username),
	FOREIGN KEY (user_id, name) references hero_and_benchmarks_wods(user_id, name)
);

CREATE TABLE cardio (
    id SERIAL PRIMARY KEY,
	user_id VARCHAR(20) NOT NULL,
	activity VARCHAR(20) NOT NULL,
	distance_km NUMERIC NOT NULL, -- kilometers
	time NUMERIC NOT NULL,
	date DATE NOT NULL,
	comment VARCHAR(100) DEFAULT NULL,
	
	FOREIGN KEY (user_id) references app_user(username)
);
""")
conn.commit()

cur.execute("""
INSERT INTO weightlifting (user_id, exercise, weight, reps, date, after_wod)
VALUES
	('lpeve', 'bench press', 135, 10, '04-16-2024', FALSE),
	('lpeve', 'bench press', 135, 10, '04-15-2024', FALSE),
	('lpeve', 'deadlift', 500.5, 10, '04-17-2024', FALSE);
	
INSERT INTO amrap (user_id, wod, timecap, rounds_plus_reps, date) VALUES
	('lpeve', '30 wall ball\r\n30 burpees', 12, '10+3', '04-15-2024'),
	('lpeve', '30 wall ball\r\n30 burpees', 12, '2+300', '04-14-2024'),
	('lpeve', '30 wall ball\r\n30 burpees', 12, '300+3', '04-16-2024'),
	('lpeve', '30 wall ball\r\n30 burpees', 12, '4', '04-18-2024');

INSERT INTO emom (user_id, wod, duration, date, comment) VALUES
	('lpeve', '10 snatches\r\n10 pullups', 10, '04-16-2024', 'killer wod'),
	('lpeve', '10 snatches\r\n10 pullups', 12, '04-17-2024', NULL),
	('lpeve', '10 snatches\r\n10 pullups', 12, '04-18-2024', NULL);

INSERT INTO rounds_for_time (user_id, wod, rounds, time, date, comment)
VALUES
	('lpeve', '5 snatches; 5 muscle ups; 5 bench press', 5, 50.24,'04-16-2024', 'killer wod'),
	('lpeve', '5 snatches; 5 muscle ups; 5 bench press', 5, 150.24,'04-16-2024', 'killer wod');

INSERT INTO hero_and_benchmarks_wods VALUES
	('lpeve', 'Murph', 'For time: 1 mile Run 100 Pull-ups 200 Push-ups 300 Squats 1 mile Run'),
	('lpeve', 'JT', '21-15-9 reps for time of: Handstand push-ups Ring dips Push-ups');

INSERT INTO hero_and_benchmarks (user_id, name, time, date, comment) VALUES
	('lpeve', 'Murph', 50.24,'04-16-2024', 'w/ vest');
	
INSERT INTO cardio (user_id, activity, distance_km, time, date, comment) VALUES 
	('lpeve', 'running', 10, 48.55, '04-16-2024', 'w/ vest'),
	('lpeve', 'row', 20, 128.55, '04-16-2024', NULL);
""")

conn.commit()