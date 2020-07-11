import os
import sys
import time
# from multiprocessing import Process
import urllib
import urllib.request as urlreq
# from urllib.request import urlopen
from bs4 import BeautifulSoup
import json
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class Downloader(object):

    def __init__(self,
                 hashtag,
                 target_download_numbers,
                 ig_account,
                 ig_password,
                 chrome_driver,
                 root_savepath='./instagram_datas/',
                 browser_type='chrome',
                 has_monitor=False,
                 basic_scroll_step=800,  # 910
                 refersh_toppost_times=5,
                 save_rate=300,
                 load_prvs_json=False,
                 log=True):
        """
            hashtag : hashtag you want to download.
            target_download_numbers : how many numbers you want to download ?
            ig_account : your instagram account.
            ig_password : your instagram password.
            root_savepath : save path root direction.
            browser_type : chorme (now).
            has_monitor : want to show driver action or not.
            save_rate : save json file every ? download.
            log : want to log message in terminal or not.
        """
        assert browser_type == 'chrome'
        self.load_prvs_json = load_prvs_json
        self.hashtag = hashtag
        self.target_download_numbers = target_download_numbers
        self.log = log
        self.ig_account, self.ig_password = ig_account, ig_password
        if sys.platform == "win32":
            self.chrome_driverpath = chrome_driver + ".exe"
        else:
            self.chrome_driverpath = chrome_driver
        self.has_monitor = has_monitor
        self.root_url = 'https://www.instagram.com/accounts/login/?next=/explore/tags/'
        self.goal_url = self.root_url + urllib.parse.quote(hashtag)  # get url
        self.driver = self._get_driver()  # get driver
        self.root_savepath = root_savepath
        self.create_folder(root_savepath)  # default: check root save dir is exist or not
        self.save_img_path = root_savepath + "/" + hashtag + "/"
        self.create_folder(self.save_img_path)  # create this hashtag folder

        self.success_download, self.fail_download = self.load_process_json()

        self.web_ypos = 0
        self.basic_scroll_step = basic_scroll_step
        self.refersh_toppost_times = refersh_toppost_times
        self.save_rate = save_rate

    def _get_driver(self):
        chrome_options = Options()
        if not self.has_monitor:
            chrome_options.add_argument("--headless")
        chrome_options.add_argument("--start-maximized")
        chrome_options.add_argument("--no-sandbox")
        driver = webdriver.Chrome(executable_path=self.chrome_driverpath,
                                  service_args=["--ignore-ssl-errors=true"],
                                  chrome_options=chrome_options,
                                  )
        return driver

    def create_folder(self, path):
        if not os.path.isdir(path):
            os.mkdir(path)
            if self.log:
                print("   * create folder: {}".format(path))

    def save_json(self):
        hashtag_encode = urllib.parse.quote(self.hashtag)
        if self.log:
            print("[hashtag-->{}] saving json...".format(hashtag_encode))
        with open(self.root_savepath + "/{}_success.json".format(hashtag_encode), "w") as fjson:
            fjson.write(json.dumps(self.success_download, indent=2))
        with open(self.root_savepath + "/{}_fails.json".format(hashtag_encode), "w") as fjson:
            fjson.write(json.dumps(self.fail_download, indent=2))
        if self.log:
            print("[hashtag-->{}] saving json done.".format(hashtag_encode))

    def start_download(self):
        self.driver.get(self.goal_url)
        if self.log:
            print("!! connect to {}".format(self.goal_url))

        self.login()
        if self.log:
            print("!! login successully.")

        # download top post reference times
        for i in range(self.refersh_toppost_times):
            self.download_top_posts()
            self.refresh_page(wait_time=1)
            if self.log:
                print("hashtag-->{}, top posts : {}/{}".format(self.hashtag, i, self.refersh_toppost_times))

        self.scroll_down()  # scroll down once for optimizer web page
        self.save_json()
        
        time.sleep(3.5) # prevent error
        
        count = len(self.success_download)
        while count < self.target_download_numbers:
            self.download_most_recent()
            self.scroll_down()
            time.sleep(1)
            count = len(self.success_download)
            if self.log:
                print("hashtag-->{}, process:{}/{}".format(self.hashtag, count, self.target_download_numbers))
            if count % self.save_rate == 0:
                self.save_json()

    def download_top_posts(self):
        
        time.sleep(4)

        bsoup = BeautifulSoup(self.driver.page_source, "html.parser")

        top_posts_div = bsoup.find_all('div', 'EZdmt')
        assert len(top_posts_div) == 1

        top_posts = top_posts_div[0].find_all('div', 'KL4Bh')
        self.download_by_divs(posts=top_posts, download_name='top posts')

    def download_most_recent(self):
        posts_element = self.driver.find_element_by_xpath("//article[@class='KC1QD']/div[2]")
        bsoup = BeautifulSoup(posts_element.get_attribute('innerHTML'), "html.parser")
        recent_posts = bsoup.find_all('div', 'KL4Bh')
        self.download_by_divs(posts=recent_posts, download_name='most recent posts')

    def download_by_divs(self, posts, download_name):
        for post in posts:
            try:
                img_url = post.find('img')['src']
                img_name = img_url.split('/')[-1].split('?')[0]
                if img_name in self.success_download:
                    continue  # skip this download
                # urllib.request.urlretrieve(img_url, self.save_img_path + "/" + img_name)
                # we need to explicitly import urllib.request as request
                urlreq.urlretrieve(img_url, self.save_img_path + "/" + img_name)
                self.success_download[img_name] = img_url
            except:
                self.fail_download[img_name] = img_url
                if self.log:
                    print("[ERROR][{}] download fail: {}".format(download_name, img_url))

    def refresh_page(self, wait_time):
        self.driver.refresh()
        time.sleep(wait_time)

    def scroll_down(self):
        next_pos = self.web_ypos + self.basic_scroll_step
        js_down = 'window.scrollTo(0,{})'.format(next_pos)
        self.driver.execute_script(js_down)
        self.web_ypos = next_pos
        time.sleep(0.5)

    def scroll_up(self):
        next_pos = self.web_ypos - self.basic_scroll_step
        next_pos = max(next_pos, 0)
        js_up = 'window.scrollTo(0,{})'.format(next_pos)
        self.driver.execute_script(js_up)
        self.web_ypos = next_pos
        time.sleep(0.5)

    def login(self):
        # log in ...
        try:
            element = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.NAME, "username"))
            )
        except:
            print("[LOGIN ERROR 0] driver not find element!")

        username = self.driver.find_element_by_name('username')
        username.send_keys(self.ig_account)
        password = self.driver.find_element_by_name('password')
        password.send_keys(self.ig_password)

        try:
            element = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, ".L3NKy"))
            )
        except:
            print("[LOGIN ERROR 1] driver not find element!")

        login_btn = self.driver.find_element(By.CSS_SELECTOR, ".L3NKy")
        login_btn.click()

        time.sleep(3)  # wait for login

        try:
            element = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, ".L3NKy"))
            )
        except:
            print("[LOGIN ERROR 2] driver not find element!")

        login_btn = self.driver.find_element(By.CSS_SELECTOR, ".L3NKy")
        login_btn.click()

        time.sleep(3)  # wait for loding

    def load_process_json(self):
        success_download, fail_download = {}, {}
        if self.load_prvs_json:
            if self.log:
                print("[hashtag-->{}] saving json...".format(self.hashtag))
            with open(self.root_savepath + "/{}_success.json".format(self.hashtag), "r") as fjson:
                success_download = json.load(fjson)
            with open(self.root_savepath + "/{}_fails.json".format(self.hashtag), "r") as fjson:
                fail_download = json.load(fjson)
        return success_download, fail_download

    def __del__(self):
        self.save_json()
