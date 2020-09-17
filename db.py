import pymongo
import logging

db_url = "mongodb://127.0.0.1:27017"

client = pymongo.MongoClient(db_url)

test_db = client['test_db']
steam_db = client['steam_db']

test_col = test_db['game']
game_col = steam_db['game']

def storage(bson):
    try:
        game_col.insert(bson)
    except Exception as e:
        logging.warn(e)

def test_storage(bson):

    test_col.insert(bson)


