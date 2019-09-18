import re
import time
from selenium import webdriver

class ScreenShotter:

    def __init__(self, urls):
        self.urls = self.read_file(urls)
        self.driver = webdriver.Firefox()
        #self.driver.fullscreen_window()

    def read_file(self, f):
        with open(f, 'r') as f:
            return f.readlines()

    def verify_link_from_path(path):
        '''Takes in a selenium xpath and appends the href to self.extra_urls.'''
        link = path.get_attribute('href')
        not_these = ['?', 'jpg', 'png', 'pdf', 'download', 'csv', 'svg']
        if any(part in link for part in not_these):
            return
        return link

    def run(self):
        with self.driver as driver:
            for url in self.urls:
                self.grab_url(driver, url)

    def grab_url(self, driver, url):
        try:
            driver.get('http://'+url)
            time.sleep(1)
            name = re.sub('\.', '_', url)
            driver.save_screenshot(f'images/{name}.png')
            print("Saved", url)
            #self.extra_urls += [verify_link_from_path(path) for path in driver.find_elements_by_xpath("//a[@href]")]
        except:
            print(url, "DID NOT WORK")

if __name__ == "__main__":
    shotter = ScreenShotter('big_websites.txt')
    shotter.run()
