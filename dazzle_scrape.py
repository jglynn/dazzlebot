#
# main() will be run when you invoke this action
#
# @param Cloud Functions actions accept a single parameter, which must be a JSON object.
#
# @return The output of this action, which must be a JSON object.
#
#
import os
import sys
import json
import cloudant
from cloudant.document import Document
from datetime import datetime, date
from bs4 import BeautifulSoup
from urllib.request import Request, urlopen

AGENT = "Mozilla/5.0 (iPhone; CPU iPhone OS 10_3 like Mac OS X) AppleWebKit/602.1.50 (KHTML, like Gecko) CriOS/56.0.2924.75 Mobile/14E5239e Safari/602.1"

def main(args):
    (client, db) = db_init(args)
    il_draws = [ "https://www.lotterypost.com/game/53/results", "https://www.lotterypost.com/game/49/results"]
    record_count = 0
    for draw in il_draws:
        result = scrape_il(draw)
        record_count += persist(db, result)
    result = { "New Records" : str(record_count) }
    db_client_teardown(client)
    return result

def scrape_il(draw_url):
    req = Request(draw_url , headers={'User-Agent': AGENT})
    page = urlopen(req)
    html = page.read().decode("utf-8")
    soup = BeautifulSoup(html, "html.parser")
    latest_draw = soup.find("div", class_="latest-draw")
    fireball = latest_draw.find("li", class_="orange")
    event = latest_draw.find("div",class_="TOD")
    draw_date = latest_draw.find("div", class_="lp-resultsstate-drawdate")
    date = parse_il_date(draw_date.text)
    return { 
            "game": "Fireball",
            "date" : format_date(date),
            "timestamp": date.timestamp(),
            "event" : event.text.upper(), 
            "ball" : fireball.text 
        }  

def parse_il_date(date_string):
    # Input: Saturday, November 21, 2020
    input_date_format = "%A, %B %d, %Y"
    return datetime.strptime(date_string, input_date_format)
    return parse_date.strftime(output_date_format)

def format_date(date):
    output_date_format = "%m/%d/%Y"
    return date.strftime(output_date_format)

def persist(db, draw_result):
    doc_id = key(draw_result)
    if exists(db, doc_id):
        return 0
    else:
        create_doc(db, doc_id, draw_result)
        return 1

def db_init(args):
    if args != None and 'db_config' in args:
        print("Loading config from args")
        CLOUDANT_USERNAME = args['db_config']['username']
        CLOUDANT_PASSWORD = args['db_config']['password']
        CLOUDANT_URL = args['db_config']['url']
    elif os.path.isfile('config.json'):
        print("Loading local config")
        with open('db-config.json') as f:
            cfg = json.load(f)
            CLOUDANT_USERNAME = cfg['username']
            CLOUDANT_PASSWORD = cfg['password']
            CLOUDANT_URL = cfg['url']
    client = cloudant.Cloudant(CLOUDANT_USERNAME, CLOUDANT_PASSWORD, url=CLOUDANT_URL, connect=True)
    db = client.create_database("lottodb", throw_on_exists=False)
    return (client, db)

def create_doc(db, doc_id, record):
    new_doc = {
        '_id': doc_id,
        'type': 'LottoResult',
        'game': 'Fireball',
        'date': record['date'],
        'timestamp' : record['timestamp']
        'event': record['event'],
        'ball': record['ball']
    }
    result = db.create_document(new_doc)

def exists(db, key):
    return Document(db, key).exists()

def key(record):
    return ':'.join([record['game'], str(record['timestamp']), record['event']])

def db_client_teardown(client):
    client.disconnect()

if __name__ == "__main__":
    main(None)