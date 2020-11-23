import csv 
import os
import sys
import json
import cloudant
from cloudant.document import Document
from datetime import datetime, date
from urllib.request import Request, urlopen

def main():
    docs = read_csv()
    (client, db) = db_init(None)
    record_count = 0
    print ("Attempting to load {} docs".format(str(len(docs))))
    for doc in docs:
        record_count += persist(db, doc)
    print( { "New Records" : str(record_count) } )
    db_client_teardown(client)
    
def key(record):
    return ':'.join(["Fireball", str(record['timestamp']), record['event'].upper()])

def read_csv():
    docs = []
    filename ="fireball_data.csv"
    with open(filename, 'r') as data:
        for line in csv.DictReader(data):
            line['timestamp'] = stamp(line['date'])
            new_doc = {
                '_id': key(line),
                'type': 'LottoResult',
                'game': 'Fireball',
                'date': line['date'],
                'timestamp': line['timestamp'],
                'event': line['event'].upper(),
                'ball': line['Fireball']
            }
            docs.append(new_doc)
    return docs

def stamp(date):
    date_format = "%m/%d/%Y"
    parse_date = datetime.strptime(date, date_format)
    return parse_date.timestamp()

def db_init(args):
    print("Loading local config")
    with open('db-config.json') as f:
        cfg = json.load(f)
        CLOUDANT_USERNAME = cfg['username']
        CLOUDANT_PASSWORD = cfg['password']
        CLOUDANT_URL = cfg['url']
    client = cloudant.Cloudant(CLOUDANT_USERNAME, CLOUDANT_PASSWORD, url=CLOUDANT_URL, connect=True)
    db = client.create_database("lottodb", throw_on_exists=False)
    return (client, db)

def persist(db, draw_result):
    doc_id = key(draw_result)
    if exists(db, doc_id):
        return 0
    else:
        create_doc(db, doc_id, draw_result)
        print("Loaded {}".format(doc_id))
        return 1

def create_doc(db, doc_id, record):
    new_doc = {
        '_id': doc_id,
        'type': 'LottoResult',
        'game': 'Fireball',
        'date': record['date'],
        'timestamp': record['timestamp'],
        'event': record['event'],
        'ball': record['ball']
    }
    db.create_document(new_doc)

def exists(db, key):
    return Document(db, key).exists()

def db_client_teardown(client):
    client.disconnect()

if __name__ == "__main__":
    main()