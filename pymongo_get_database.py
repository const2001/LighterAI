from pymongo import MongoClient
from yeelight_controller import *


def get_database():
    # Provide the mongodb atlas url to connect python to mongodb using pymongo
    CONNECTION_STRING = "mongodb+srv://it21994:it21994@cluster0.rpnvpef.mongodb.net/?retryWrites=true&w=majority"


    # Create a connection using MongoClient. You can import MongoClient or use pymongo.MongoClient
    client = MongoClient(CONNECTION_STRING)

    # Create the database for our example (we will use the same database throughout the tutorial
    return client['LighterAI-db']


# This is added so that many files can reuse the function get_database()
if __name__ == "__main__":
    # Get the database
    #ybulbs = get_local_bulbs()
    db = get_database()
    collection = db['Yeelight-bulbs']
    #test bulbs
    ybulbs = [{'capabilities': {'bright': '50',
                   'color_mode': '1',
                   'ct': '2700',
                   'fw_ver': '45',
                   'hue': '359',
                   'id': '0x0000000002dfb19a',
                   'model': 'color',
                   'name': 'bedroom',
                   'power': 'off',
                   'rgb': '16711935',
                   'sat': '100',
                   'support': 'get_prop set_default set_power toggle '
                              'set_bright start_cf stop_cf set_scene cron_add '
                              'cron_get cron_del set_ct_abx set_rgb set_hsv '
                              'set_adjust set_music set_name'},
  'ip': '192.168.2.106',
  'port': 55443},
  {'capabilities': {'bright': '50',
                   'color_mode': '1',
                   'ct': '2700',
                   'fw_ver': '45',
                   'hue': '359',
                   'id': '0x0000000002dfb2f1',
                   'model': 'color',
                   'name': 'livingroom',
                   'power': 'off',
                   'rgb': '16711935',
                   'sat': '100',
                   'support': 'get_prop set_default set_power toggle '
                              'set_bright start_cf stop_cf set_scene cron_add '
                              'cron_get cron_del set_ct_abx set_rgb set_hsv '
                              'set_adjust set_music set_name'},
  'ip': '192.168.2.209',
  'port': 55443}]

    for bulb in ybulbs:
     query = {'id': bulb['capabilities']['id']}
     update = {'$set': bulb}
     collection.update_one(query, update, upsert=True)
     
        #print(bulb['capabilities']['id'])
    # # Try to find a record with the same id
    # print(bulb)
    # if result:
    #     # If a record exists, update it with the new data
    #     collection.update_one({"id": bulb['capabilities']['id']}, {"$set": bulb})
    # else:
    #     # If a record doesn't exist, insert the new item into the collection
    #     collection.insert_one(bulb)  