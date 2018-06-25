from time import sleep
import re

from selenium.webdriver import Chrome


def parse_fit(browser, a, b, c, d, e, f, g, h):
    # Select Male - Road - CM
    browser.find_element_by_xpath(
        "//div[@class='fit-option gender-male active']"
    ).click()
    browser.find_element_by_xpath(
        "//div[@class='fit-option ride-road active']"
    ).click()
    browser.find_element_by_xpath(
        "//div[@class='fit-option unit-cm']"
    ).click()
    browser.find_element_by_xpath(
        "//a[@class='btn btn-next js-next']"
    ).click()
    sleep(0.3)
    # Get inputs
    fill_data = {
        "inseam": a,
        "trunk": b,
        "forearm": c,
        "arm": d,
        "thigh": e,
        "lowerLeg": f,
        "sternalNotch": g,
        "overallHeight": h,
    }
    [
        browser\
        .find_element_by_xpath("//div[@id='measures']/fieldset")\
        .find_element_by_xpath(f'//input[@id="{key}"]')\
        .send_keys(value) for (key, value) in fill_data.items()
    ]
    # Continue
    browser.find_element_by_xpath('//button[@id="calculate"]').click()
    sleep(2)
    # Collect results
    digits = re.compile('\s(-?\d*\.?\d?)\s-\s(-?\d*\.?\d?)')
    fit_type = 'eddy'
    def get_value(measurement):
        """Sanitize and return parsed value"""
        html = browser.find_element_by_xpath(
            f'//div[@id="{fit_type}"]/div/div[@id="fit-{measurement}"]',
        )
        value_raw =  html.get_attribute('innerHTML')
        if 'not' in value_raw:
            return False
        elif 'setback' in value_raw:
            return True
        else:
            return digits.search(value_raw).groups()
    geometry_measurements = {
        'Top Tube': 'top_tube_length',
        'Seat Tube Range CC': 'seat_tube_range_cc',
        'Seat Tube Range CT': 'seat_tube_range_ct',
        'Stem Length': 'stem_length',
        'BB Saddle Position': 'bb_saddle_position',
        'Saddle Handlebar': 'saddle_handlebar',
        'Saddle Setback': 'saddle_setback',
        'Setback Seatpost': 'seatpost_type',
    }
    results = {key:get_value(value) for (key, value) in geometry_measurements.items()}
    return results

def test():
    browser = Chrome('webdriver/chromedriver')
    browser.get(
        'https://www.competitivecyclist.com/Store/catalog/fitCalculatorBike.jsp'
    )
    sleep(1)
    args = [
        (52, 40, 17, 35, 35, 32, 78, 129),
        (52, 40, 17, 35, 35, 68, 78, 129),
    ]
    try:
        fit = parse_fit(browser, *args[1])
    except ValueError:
        browser.quit()
    browser.quit()
    print(fit)

if __name__ == '__main__':
    test()
