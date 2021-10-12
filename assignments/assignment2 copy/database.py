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
        query1 = """ INSERT INTO url_store(long_url, short_url, domain, create_time, update_time, created_by, 
        updated_by, group_guid, tags, deeplinks, title)
            values (?,?,?,?,?,?,?,?,?,?,?);
         """
        query2 = """ INSERT INTO clicks(short_url, domain, click_time, minute, hour, day, week, month, year)
            values (?,?,?,?,?,?,?,?,?);"""

        time = datetime.datetime.now()
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

    return retrive_url(domain, short_url, False)


def get_clicks(short_url, domain, unit, units, unit_reference):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    if unit not in UNIT:
        unit = 'day'

    query = """ select click_time, count(1) from clicks 
            where short_url='{}' and domain='{}' and {}={} and click_time <= '{}' group by {}; """.format(
        short_url, domain, unit, units, unit_reference, unit)

    if units == -1:
        query = """ select click_time, count(1) from clicks 
                where short_url='{}' and domain='{}' and click_time <= '{}' group by {}; """.format(
            short_url, domain, unit_reference, unit)

    cursor.execute(query)
    clicks = cursor.fetchall()

    link_clicks = []
    for row in clicks:
        link_clicks.append({"clicks": row[1], "date": row[0]})

    return link_clicks


def retrive_url(domain, short_url, update_clicks=False):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    query = """ SELECT * from url_store where domain = '{}' and short_url = '{}' """.format(
        domain, short_url
    )
    cursor.execute(query)
    link_data = cursor.fetchall()

    result = {}
    if len(link_data) == 0:
        col_names = [tup[0] for tup in cursor.description]
        row_values = ["" for tup in cursor.description]
        result = dict(zip(col_names, row_values))
    else:
        for row in link_data:
            col_names = [tup[0] for tup in cursor.description]
            row_values = [i for i in row]
            result = dict(zip(col_names, row_values))

    if update_clicks:
        query = """ INSERT INTO clicks(short_url, domain, click_time, minute, hour, day, week, month, year)
                    values (?,?,?,?,?,?,?,?,?);"""
        time = datetime.datetime.now()
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
        cursor.execute(query, click_data)
        conn.commit()
        pass

    return result


def update_link(domain, short_url, title, tags, deeplinks, updated_by, group_guid):
    pass
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    get_result = retrive_url(domain, short_url, True)
    query = """ UPDATE url_store set
             title = coalesce ("{}", "{}"),
             tags = coalesce ("{}", "{}"),
             deeplinks = coalesce ("{}", "{}"),
             group_guid = coalesce ("{}", "{}"),
             updated_by = coalesce ("{}", "{}")
             where domain = '{}' and short_url = '{}';
        """.format(title, get_result.get('title')
                   , tags, get_result.get('tags')
                   , deeplinks, get_result.get('deeplinks')
                   , group_guid, get_result.get('group_guid')
                   , updated_by, get_result.get('updated_by')
                   , domain, short_url)

    cursor = conn.execute(query)
    conn.commit()
    return retrive_url(domain, short_url, False)
