import requests
from bs4 import BeautifulSoup
from datetime import date
from datetime import datetime
import pymongo


def main():
    new_forum_data = get_new_forum_data()
    update_forum_data(new_forum_data)


def mongo_rs_forum_data():
    uri = "mongodb+srv://fef:dbtest@cluster0-9cldq.mongodb.net/test?retryWrites=true&w=majority"
    client = pymongo.MongoClient(uri)
    database = client['forum_data']
    collection = database['rs_forum_data']
    return collection


def get_current_forum_data():
    return list(mongo_rs_forum_data().find())


def get_new_forum_data():
    # Making html soup, yum
    html_data = str(requests.get('https://secure.runescape.com/m=forum/forums').text.encode('utf-8'))
    soup = BeautifulSoup(html_data, 'lxml')

    # Get Community Lounge data
    community_lounge = soup.find(id='group43')
    articles = community_lounge.find_all('article')

    # Adding Data to Array
    forum_data_new = []
    for article in articles:
        forum_data_new.append({
            "board_name": article.h3.text,
            "num_posts": article.find('span', class_='forum-stat forum-stat--posts').text,
            "downloaded_at": str(date.today()) + " " + datetime.now().strftime("%H:%M")
        })
    return forum_data_new


def update_forum_data(new_forum_data):
    # Write JSON remotely to mongo
    # mongo_rs_forum_data().insert_many(master_forum_data)


if __name__ == "__main__":
    main()
