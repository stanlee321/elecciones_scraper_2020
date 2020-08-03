import sqlite3
import json


import os
from tqdm import tqdm
import sys

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager


class EleccionesScraper:

    HOME_PATH = os.getenv('HOME')
    SCRAPED_DATA_DIRECTORY = os.path.join(HOME_PATH, "ELECCIONES") 
    
    def __init__(self, headless:bool = True):
        """
        This scraper downloads information from http://atlaselectoral.oep.org.bo/
        """
        pass

    def _login_custom(self,
                    input_link:str,
                    headless:bool):
        """ Logging into our own profile """

        try:
            driver = None
            options = Options()

            #  Code to disable notifications pop up of Chrome Browser
            options.add_argument("--disable-notifications")
            options.add_argument("--disable-infobars")
            options.add_argument("--mute-audio")
            options.add_argument("--start-maximized")
            options.add_argument("--disable-extensions")
            options.add_argument("--no-sandbox")

            if headless:
                options.add_argument("--headless")
            
            # Pass the argument 1 to allow and 2 to block
            options.add_experimental_option("prefs", {
                "profile.default_content_setting_values.notifications": 1
            })

            try:
                driver = webdriver.Chrome(
                    executable_path=ChromeDriverManager().install(), options=options
                )
            except Exception:
                print("Error loading chrome webdriver " + sys.exc_info()[0])
                exit(1)

            driver.get(input_link)
            driver.maximize_window()

            return driver

        except Exception as e:
            print(e)
            print("There's some error in log in.")
            print(sys.exc_info()[0])

    def main(self, link:str, headless:bool = False):

        with open(f"{ self.FB_PROFILE_SCRAPER_FOLDER }/selectors.json") as a:
            selectors = json.load(a)

        link = selectors.get("base_link")

        driver = self._login_custom(self,
                    input_link = link,
                    headless = headless)
        