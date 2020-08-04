import json

import pandas as pd
from urllib.request import Request, urlopen
import io
import os
import sys
import time

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager


class EleccionesScraper:


    def __init__(self,project_path:str,  headless:bool = True):
        """
        This scraper downloads information from http://atlaselectoral.oep.org.bo/
        """
        # Project path

        self.PROJECT_PATH = project_path
        self.SCRAPER_PATH = os.path.join(self.PROJECT_PATH)

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

    def main(self,  headless:bool = False):

        with open(f"{self.SCRAPER_PATH}/selectors.json") as a:
            selectors = json.load(a)

        link = selectors.get("base_link")

        driver = self._login_custom( input_link = link,
                    headless = headless)

        # Perform click on Elecciones Generales.

        time.sleep(2)

        buttons_dropdown_bar = driver.find_elements_by_xpath(
            selectors.get("buttons_dropdown_bar")
        )

        print(f"FOUNR {len(buttons_dropdown_bar)}")

        buttons_dropdown_bar[0].click()

        # Find mat-menu-content
        
        mat_menu_content = driver.find_elements_by_xpath(
            selectors.get("mat-menu-content")
        )

        # perform click in each one of the sub dropdown sub elements:
        sub_buttons_dropdown_bar = mat_menu_content[0].find_elements_by_xpath(
            selectors.get("sub_buttons_dropdown_bar")
        )

        print(f"DOWNDOWN COUNTS {len(sub_buttons_dropdown_bar)}")


        for dropdown in sub_buttons_dropdown_bar:

            dropdown.click()

            sub_sub_button_dropdown_div = driver.find_elements_by_id(
                selectors.get("sub_sub_button_dropdown_div")
            )

            sub_sub_button_dropdown_div[0].click()

            nav_buttons_div = driver.find_elements_by_xpath(
                selectors.get("buttons_center_div")
            )

            nav_buttons = nav_buttons_div[0].find_elements_by_xpath(
                selectors.get("buttons_center_el")
            )
            time.sleep(2)
            
            nav_buttons[-1].click()


            els = driver.find_elements_by_xpath(
                            selectors.get("data_column")
            )

            time.sleep(2)


            data_links = els[-1].find_elements_by_xpath(
                            selectors.get("download_votes_els")
            ) 

            for el in data_links:
                print(el.text)
                print(el.get_attribute("href"))

                self.test_read_remote_csv( el.get_attribute("href") )

        time.sleep(5)

    def test_read_remote_csv(self, csv_link):

        response_raw = Request(csv_link, headers={'User-Agent': 'Mozilla/5.0'})
        response = urlopen(response_raw,  timeout=2).read()

        response = response.decode('utf-8')
        
        df =pd.read_csv(io.StringIO(response))

        print(df.head())

if __name__ == "__main__":
    elecciones = EleccionesScraper(project_path = ".")

    elecciones.main(headless=True)
    #elecciones.test_read_remote_csv(csv_link = "http://atlaselectoral.oep.org.bo/descarga/52/votos_totales.csv")