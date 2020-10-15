from datetime import datetime

import psycopg2
from psycopg2 import sql

import TwitterZuil.twitter_api as twitter
import TwitterZuil.weather_api as weather
from TwitterZuil.models import *
import TwitterZuil.db_auth as db_auth

connection = None
cursor = None


def open_db_connection():
    global connection, cursor
    try:
        # connection = psycopg2.connect(user="postgres",
        #                               password="Schouten2002",
        #                               host="127.0.0.1",
        #                               port="5432",
        #                               database="postgres")
        # up.uses_netloc.append("postgres")
        # url = up.urlparse(os.environ["postgres://inxcdtzn:IItRJjOeR5tr_DbJvfOpTYkZL9QMyYgg@rogue.db.elephantsql.com:5432/inxcdtzn "])

        connection = psycopg2.connect(f"dbname='{db_auth.name}' user='{db_auth.name}' host='{db_auth.host}' password='{db_auth.password}'")
        cursor = connection.cursor()
    except (Exception, psycopg2.Error) as error:
        print("Error while connecting to PostgreSQL", error)


def tweet_message(msg, name):
    currentdateTime = getCurrentDateTime()

    query = sql.SQL('insert into ns_berichten.tweet values (default, %s, %s, %s, false, false, null)')
    data = (msg, name, currentdateTime)
    execute_query(query, data)


def add_scherm(name, location):
    if weather.getWeather(location):
        query = sql.SQL('insert into ns_berichten.scherm values (default, %s, %s)')
        data = (location, name)
        execute_query(query, data)
        return True
    return None


def close_db_connection():
    # closing database connection.
    if connection:
        cursor.close()
        connection.close()
        # print("PostgreSQL connection is closed")


def execute_query(query, data):
    open_db_connection()

    cursor.execute(query, data)
    connection.commit()

    close_db_connection()


def getTweetToBeReviewed():
    open_db_connection()

    cursor.execute('select * from ns_berichten.tweet where is_reviewed = false order by id asc')
    result = cursor.fetchone()
    close_db_connection()

    try:
        tweet = Tweet(
            result[0],
            result[1],
            result[2],
            result[3],
            result[4],
            result[5],
            result[6]
        )

        return tweet
    except TypeError:
        return None


def post_tweet(msg, tweet_id):
    twitter_tweet_id = str(twitter.tweet_message(msg))
    if twitter_tweet_id:
        query = sql.SQL(
            'update ns_berichten.tweet set is_reviewed = true, is_tweeted = true, twitter_tweet_id = %s where id = %s')
        data = (twitter_tweet_id, tweet_id)

        queryUpdate = sql.SQL('insert into ns_berichten.scherm_tweet values (%s, null, null)')
        dataUpdate = (tweet_id,)

        execute_query(query, data)
        execute_query(queryUpdate, dataUpdate)

        print('Tweet posted!')

    else:
        print('403! This Tweet is a duplicate')


def reject_tweet(tweet_id, remark, moderator_id):
    currentdateTime = getCurrentDateTime()
    queryUpdate = sql.SQL('update ns_berichten.tweet set is_reviewed = true where id = %s')
    dataUpdate = (tweet_id,)

    queryInsert = sql.SQL('insert into ns_berichten.tweet_moderator values (%s, %s, %s, %s)')
    dataInsert = (tweet_id, moderator_id, currentdateTime, remark)
    execute_query(queryUpdate, dataUpdate)
    execute_query(queryInsert, dataInsert)
    print('Tweet rejected!')


def getModeratorByName(name, password):
    open_db_connection()

    names = str(name).split()
    first_name = '{} '.format(names[0])
    infix = ''
    last_name = ''

    if len(names) == 3:
        infix = '{} '.format(names[1])
        last_name = names[2]
    elif len(names) == 2:
        last_name = names[1]

    cursor.execute('select * from ns_berichten.moderator where first_name = %s and infix = %s and last_name = %s',
                   (first_name.strip(), infix.strip(), last_name))
    result = cursor.fetchone()

    close_db_connection()

    if result is not None:
        if result[4] == password:
            moderator = Moderator(
                result[0],
                first_name + infix + last_name,
                result[1],
                result[2],
                result[3],
                result[4]
            )

            return moderator
    return None


def getAllSchermen():
    open_db_connection()
    cursor.execute('select * from ns_berichten.scherm')
    results = cursor.fetchall()
    close_db_connection()

    schermen = []

    for result in results:
        scherm = Scherm(
            result[0],
            result[1],
            result[2],
        )
        # print(result)
        schermen.append(scherm)

    return schermen


def getSchermById(id):
    open_db_connection()
    cursor.execute('select * from ns_berichten.scherm where id = %s', (id,))
    result = cursor.fetchone()
    close_db_connection()

    scherm = Scherm(
        result[0],
        result[1],
        result[2],
    )

    return scherm


def createNewModerator(firstname, infix, lastname, password):
    open_db_connection()

    cursor.execute('select * from ns_berichten.moderator m where first_name = %s and infix = %s and last_name = %s',
                   (str(firstname), str(infix), str(lastname)))
    result = cursor.fetchone()
    close_db_connection()

    if result is None:
        query = sql.SQL('insert into ns_berichten.moderator values (default, %s, %s, %s, %s)')
        data = (str(firstname), str(infix), str(lastname), str(password))
        execute_query(query, data)
        return True

    return False


def getTweetsToDisplay(scherm):
    open_db_connection()
    # SHOW ONCE AND THEN WEATHER MESSAGE!
    cursor.execute(
        'select * from ns_berichten.tweet where id = (select id_tweet from ns_berichten.scherm_tweet where id_scherm is null order by id_tweet asc limit 1)')
    result = cursor.fetchone()
    close_db_connection()

    if result and isTweetYoungerThan(result[3], 24):
        tweet = Tweet(
            result[0],
            result[1],
            result[2],
            result[3],
            result[4],
            result[5],
            result[6]
        )
        query = sql.SQL('update ns_berichten.scherm_tweet set id_scherm = %s, first_view_date = %s where id_tweet = %s')
        data = (scherm.id, getCurrentDateTime(), tweet.id)
        execute_query(query, data)
        return tweet
    # elif result is None:
    # while True:
    #     result


def isTweetYoungerThan(creation_date_time, hours):
    nowConverted = datetime.strptime(getCurrentDateTime(), "%Y-%m-%d %H:%M:%S")  # convert string to time
    dateTimeDifference = nowConverted - creation_date_time
    tweetAge = dateTimeDifference.total_seconds() / 3600

    return tweetAge < hours


def getCurrentDateTime():
    return datetime.today().strftime("%Y-%m-%d %H:%M:%S")
