from time import sleep
from datetime import datetime
from db import Database
from generate_table import calculate_table_size
from generate_table import create_table
from parser import parse_fit
from selenium.webdriver import ChromeOptions
from selenium.webdriver import Chrome
from selenium.common.exceptions import TimeoutException
from create_db import DBNAME


URL = 'https://www.competitivecyclist.com/Store/catalog/fitCalculatorBike.jsp'

def parse(db):
    start_time = datetime.now()
    no_gui = ChromeOptions()
    no_gui.set_headless(headless=True)
    try:
        browser = Chrome(executable_path='webdriver/chromedriver', options=no_gui)
    except Exception as error:
        print(error)
        db.heal()
        sleep(5)
        return
    try:
        browser.get(URL)
    except TimeoutException as error:
        print(error)
        browser.quit()
        db.heal()
        return
    sleep(1)
    import pdb ; pdb.set_trace()
    pass
    data = db.fetch_unprocessed()
    if data is None:
        db.heal()
        if db.get_unprocessed_count() == 0:
            print('FINISHED!')
            exit()
        return
    args = data[1:]
    key = data[0]
    try:
        parsed_data = parse_fit(browser, *args)
    except Exception as error:
        print(f'Row {key}: {error}Args: {args}')
        browser.quit()
        sleep(5)
        return
    browser.quit()
    db.insert_parsed_data(parsed_data, key)
    finish_time = datetime.now()
    elapsed_time = finish_time - start_time
    print(f'Row {key}: parsed in {elapsed_time.seconds}.{elapsed_time.microseconds}')

def main():
    print('Starting parser...')
    db = Database(DBNAME)
    while True:
        for _ in range(250):
            parse(db)
        print('Healing database...')
        db.heal()

if __name__ == '__main__':
    main()
