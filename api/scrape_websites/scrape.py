import time

from utils import get_data, extract_data, save_to_file

"""
This can be done also using scraping libraries such as Scrapy, Beautifulsoup.
"""
URLS = {
    "gold": "https://www.investing.com/commodities/gold-historical-data",
    "silver": "https://www.investing.com/commodities/silver-historical-data"
}
PAUSE_IN_SEC = 5


def run():
    for key, url in URLS.items():
        print('Processing ', url)
        result, html = get_data(url=url)
        if not result:
            print('Could not access URL ', url)
            continue
        data = extract_data(html=html)
        save_to_file(data=data, key=key)
        print("Done")
        print("Wait for {} sec".format(PAUSE_IN_SEC))
        time.sleep(PAUSE_IN_SEC)


if __name__ == "__main__":
    run()
