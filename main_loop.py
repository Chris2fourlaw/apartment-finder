from scraper import do_scrape
from settings import SLEEP_INTERVAL
from time import sleep, ctime
from sys import exit, exc_info
from traceback import print_exc

if __name__ == "__main__":
    while True:
        print("{}: Starting scrape cycle".format(ctime()))
        try:
            do_scrape()
        except KeyboardInterrupt:
            print("Exiting....")
            exit(1)
        except Exception as exc:
            print("Error with the scraping:", exc_info()[0])
            print_exc()
        else:
            print("{}: Successfully finished scraping".format(ctime()))
        sleep(SLEEP_INTERVAL)
