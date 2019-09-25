import os
import re
import time
from selenium import webdriver
from selenium.common.exceptions import TimeoutException

class ScreenShotter:

    def __init__(self, urls, start_position=0, max_time=10, ads=False, fullscreen=False):
        self.urls = self.filter_urls(self.read_file(urls)[start_position:])

        if ads:
            self.driver = webdriver.Firefox()
        else:
            ffprofile = webdriver.FirefoxProfile()
            ffprofile.add_extension('adblock_plus-3.6.3-an+fx.xpi')
            ffprofile.set_preference("extensions.adblockplus.currentVersion", "3.6.3")
            self.driver = webdriver.Firefox(ffprofile)

        self.driver.set_page_load_timeout(max_time)
        if fullscreen:
            self.driver.fullscreen_window()

    def read_file(self, f):
        '''Returns a list of urls from a text file or urls.'''
        with open(f, 'r') as f:
            return f.read().splitlines()

    def filter_urls(self, urls):
        '''Takes in a list of urls and filters out sketchy content.'''
        bads = ['?', 'jpg', 'png', 'pdf', 'download', 'csv', 'svg']
        return list(filter(lambda url: not any(part in url for part in bads), urls))

    def run(self):
        with self.driver as driver:
            for index, url in enumerate(self.urls):
                self.grab_url(driver, url)

    def grab_url(self, driver, url):
        try:
            name = re.sub('\.', '_', url)
            if name + '.png' not in os.listdir('images'):
                driver.get('http://'+url)
                driver.save_screenshot(f'images/{name}.png')
                print("Saved:", url)
            else:
                print("Already collected:", url)
        except TimeoutException:
            print("Timed out:", url)
        except Exception as e:
            print("Unkown error:", e, url)

if __name__ == "__main__":
    shotter = ScreenShotter('little_websites.txt')
    shotter.run()
