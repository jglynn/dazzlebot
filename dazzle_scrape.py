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
#import cloudscraper
from cloudant.document import Document
from datetime import datetime, date, timezone
from bs4 import BeautifulSoup
from urllib.request import Request, urlopen

AGENT = "Mozilla/5.0 (iPhone; CPU iPhone OS 10_3 like Mac OS X) AppleWebKit/602.1.50 (KHTML, like Gecko) CriOS/56.0.2924.75 Mobile/14E5239e Safari/602.1"

def main(args):
    (client, db) = db_init(args)
    evening_draw =  "https://www.lotteryusa.com/illinois/daily-3/"
    midday_draw = "https://www.lotteryusa.com/illinois/midday-3/"
    record_count = 0
    record_count += process_feed(db, evening_draw, "EVENING")
    record_count += process_feed(db, midday_draw, "MIDDAY")
    result = { "New Records" : str(record_count) }
    db_client_teardown(client)
    return result

def process_feed(db, draw_url, draw_event):
    print("fetching {} for {}".format(draw_url,draw_event))
    record_count = 0
    results = scrape_il(draw_url, draw_event)
    for result in results:
        record_count += persist(db, result)
    return record_count

def scrape_il(draw_url, draw_event):
    html = fetch_page(draw_url)
    soup = BeautifulSoup(html, "html.parser")
    draws = soup.find_all("tr", class_="c-game-table__item")
    results = []
    for draw in draws:
        date_time = draw.find("time", class_="c-game-table__game-date")
        if date_time:
            draw_datetime = parse_date(date_time['datetime'])
            draw_obj = {
                "game": "Fireball",
                "event": draw_event.upper(),
                "date": format_date(draw_datetime),
                "timestamp": draw_datetime.replace(tzinfo=timezone.utc).timestamp(),
                "ball":  draw.find("span", class_="c-result__ball--fire").text
            }
            results.append(draw_obj)

    return results

def fetch_page(draw_url):
    #scraper = cloudscraper.create_scraper()    
    #html = scraper.get(draw_url).text
    req = Request(draw_url , headers={'User-Agent': AGENT})
    page = urlopen(req)
    return page.read().decode("utf-8")

def parse_date(date_string):
    # Input: Saturday, November 21, 2020
    input_date_format = "%Y-%m-%d"
    return datetime.strptime(date_string, input_date_format)

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
    elif os.path.isfile('db-config.json'):
        print("Loading local config")
        with open('db-config.json') as f:
            cfg = json.load(f)
            CLOUDANT_USERNAME = cfg['username']
            CLOUDANT_PASSWORD = cfg['password']
            CLOUDANT_URL = cfg['url']
    client = cloudant.Cloudant(CLOUDANT_USERNAME, CLOUDANT_PASSWORD, url=CLOUDANT_URL, connect=True)
    db = client.create_database("lottodb", throw_on_exists=False)
    return (client, db)


def delete_doc(db, id, rev):
    try:
        doc = db[id]
    except KeyError:
        print("doc does not exist with id:{}".format(id))

def create_doc(db, doc_id, record):
    new_doc = {
        '_id': doc_id,
        'type': 'LottoResult',
        'game': 'Fireball',
        'date': record['date'],
        'timestamp' : record['timestamp'],
        'event': record['event'],
        'ball': record['ball']
    }
    result = db.create_document(new_doc)
    if result.exists():
        print("created record {}".format(result))
    else:
        print("failed to create record in Cloudant")

def exists(db, key):
    return Document(db, key).exists()

def key(record):
    return ':'.join([record['game'], str(record['timestamp']), record['event']])

def db_client_teardown(client):
    client.disconnect()

if __name__ == "__main__":
    main(None)