import logging

import pymongo

IP = '47.107.109.43'
PORT = 52613

db_url = "mongodb://{}:{}".format(IP,PORT)

client = pymongo.MongoClient(db_url)

steam_db = client['steam_db']
game_col = steam_db['game']

def storage(bson):
    try:
        game_col.insert(bson)
    except Exception as e:
        logging.warning(e.__str__())
