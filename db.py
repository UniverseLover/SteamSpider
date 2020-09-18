import pymongo
import logging

db_url = "mongodb://47.107.109.43:52613"

client = pymongo.MongoClient(db_url)

test_db = client['test_db']
steam_db = client['steam_db']

test_col = test_db['game']
game_col = steam_db['game']

def storage(bson):
    try:
        game_col.insert(bson)
    except Exception as e:
        logging.warning(e.__str__())

def test_storage(bson):

    test_col.insert(bson)


