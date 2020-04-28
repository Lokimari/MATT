import json
import requests
from bs4 import BeautifulSoup
from datetime import date
from datetime import datetime
import pymongo

# Tag: 5:07pm 4/28/2020

def main():
    old_forum_data = get_current_forum_data()
    new_forum_data = get_new_forum_data()
    update_forum_data(old_forum_data, new_forum_data)


def get_current_forum_data():
    try:
        with open("runescape_stats.json", "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return []


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


def update_forum_data(forum_data_old, forum_data_new):
    master_forum_data = forum_data_old + forum_data_new

    # Write JSON remotely to mongo
    uri = "mongodb+srv://fef:dbtest@cluster0-9cldq.mongodb.net/test?retryWrites=true&w=majority"
    client = pymongo.MongoClient(uri)
    database = client['forum_data']
    collection = database['rs_forum_data']
    collection.insert_many(master_forum_data)

    # Write JSON locally
    # with open("runescape_stats.json", "w") as towrite:
    #     towrite.write(json.dumps(master_forum_data, indent=2))


if __name__ == "__main__":
    main()
