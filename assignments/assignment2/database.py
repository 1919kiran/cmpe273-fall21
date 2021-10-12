import sqlite3
import datetime

DATABASE = 'database.sqlite'
UNIT = ['minute', 'hour', 'day', 'week', 'month', 'year']


def init_db():
    try:
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        with open('ddl.sql', 'r') as sql_file:
            sql_script = sql_file.read()
        cursor.executescript(sql_script)
        print('Initialized the database')

    except sqlite3.Error as e:
        print('SQLite error occurred: ', e)


def insert(url_data, short_url, domain):
    try:
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        query1 = """ INSERT INTO url_store(long_url, short_url, domain, create_time, update_time, created_by, title)
            values (?,?,?,?,?,?,?);
         """
        query2 = """ INSERT INTO clicks(short_url, domain, click_time, minute, hour, day, week, month, year)
            values (?,?,?,?,?,?,?,?,?);"""

        time = datetime.datetime.now().isoformat()
        minute = time.minute
        hour = time.hour
        day = time.day
        month = time.month
        year, week, day_of_week = datetime.date.today().isocalendar()
        click_data = (
            short_url,
            domain,
            time,
            minute,
            hour,
            day,
            week,
            month,
            year
        )
        cursor.execute(query1, url_data)
        cursor.execute(query2, click_data)
        print('Inserted into the database')
        conn.commit()

    except sqlite3.Error as e:
        print('SQLite error occurred: ', e)


def get_clicks(short_url, unit, units, unit_reference):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    if unit not in UNIT:
        unit = 'day'

    query = """ select click_time, count(1) from clicks 
            where short_url='{}' and domain='{}' and {}={} and click_time <= '{}' group by {}; """.format(
        short_url, unit, units, unit_reference, unit)

    if units == -1:
        query = """ select click_time, count(1) from clicks 
                where short_url='{}' and domain='{}' and click_time <= '{}' group by {}; """.format(
            short_url, unit_reference, unit)

    cursor.execute(query)
    clicks = cursor.fetchall()

    link_clicks = []
    for row in clicks:
        print({"clicks": row[1], "date": row[0]})
        link_clicks.append({"clicks": row[1], "date": row[0]})

    return link_clicks
