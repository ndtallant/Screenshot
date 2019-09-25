import os
import re
import time
import logging
from selenium import webdriver
from selenium.common.exceptions import TimeoutException



class ScreenShotter:

    def __init__(self, urls, start_position=0, max_time=10, ads=False, fullscreen=False):

        logging.basicConfig(filename='collection.log',
                            filemode='w',
                            format='%(asctime)s - %(message)s',
                            level=logging.INFO)
        self.plog('Screenshot tool initialized.')

        self.urls = self.filter_urls(self.read_file(urls)[start_position:])

        if ads:
            self.driver = webdriver.Firefox()
        else:
            ffprofile = webdriver.FirefoxProfile()
            ffprofile.add_extension('adblock_plus-3.6.3-an+fx.xpi')
            ffprofile.set_preference("extensions.adblockplus.currentVersion", "3.6.3")
            self.driver = webdriver.Firefox(ffprofile)
            self.plog("ADBLOCK Installed")

        self.driver.set_page_load_timeout(max_time)
        if fullscreen:
            self.driver.fullscreen_window()
            self.plog("FULLSCREEN Set")

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
                self.plog(f'Saved: {url}')
            else:
                self.plog(f'Already collected: {url}')
        except TimeoutException:
            self.plog(f'Timed out: {url}')
        except Exception as e:
            self.plog(f'Error {e}: {url}')

    def plog(self, message):
        '''Prints and logs.'''
        print(message)
        logging.info(message)

if __name__ == "__main__":

    import argparse
    parser = argparse.ArgumentParser()

    ### Command line arguments.
    parser.add_argument('--start_position',
        help='The line in the urls file to start on. Default is 0.')
    parser.add_argument('--max_time',
        help='The max timeout rate for a url in seconds. Default is 10.')
    parser.add_argument('--ads',
        help='True for ads, False for no ads. Defualt is False.')
    parser.add_argument('--fullscreen',
        help='True for fullscreen, False for no fullscreen. Defualt is False.')
    args = parser.parse_args()

    ### Make args a dictionary to pass easily.
    dict_args = {}
    for arg in ['ads', 'fullscreen', 'max_time', 'start_position']:
        if getattr(args, arg):
            dict_args[arg] = getattr(args, arg)

    ### Init and run.
    shotter = ScreenShotter('little_websites.txt', **dict_args)
    shotter.run()
