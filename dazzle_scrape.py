#
# main() will be run when you invoke this action
#
# @param Cloud Functions actions accept a single parameter, which must be a JSON object.
#
# @return The output of this action, which must be a JSON object.
#
#
import sys
from bs4 import BeautifulSoup
from urllib.request import Request, urlopen

AGENT = "Mozilla/5.0 (iPhone; CPU iPhone OS 10_3 like Mac OS X) AppleWebKit/602.1.50 (KHTML, like Gecko) CriOS/56.0.2924.75 Mobile/14E5239e Safari/602.1"

def main(args):
    il_draws = [ "https://www.lotterypost.com/game/53/results", "https://www.lotterypost.com/game/49/results"]
    record_count = 0
    for draw in il_draws:
        result = scrape_il(draw)
        record_count += persist(result)
    result = { "New Records" : str(record_count)}
    print(result)
    return result

def scrape_il(draw_url):
    req = Request(draw_url , headers={'User-Agent': AGENT})
    page = urlopen(req)
    html = page.read().decode("utf-8")
    soup = BeautifulSoup(html, "html.parser")
    latest_draw = soup.find("div", class_="latest-draw")
    draw_date = latest_draw.find("div", class_="lp-resultsstate-drawdate")
    fireball = latest_draw.find("li", class_="orange")
    event = latest_draw.find("div",class_="TOD")
    return { 
            "date" : draw_date.text, 
            "event" : event.text, 
            "fireball" : fireball.text 
        }  

def persist(draw_result):
    print(str(draw_result))
    # TODO: Check Cloudant for record and create if doesnt exist
    return 0;

if __name__ == "__main__":
    main(None)