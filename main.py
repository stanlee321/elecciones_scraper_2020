
import json

import os
import sys
import time

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from logger import LoggingHandler

from datetime import  datetime

log = LoggingHandler()

class EleccionesScraper:

    def __init__(self,project_path:str, download_dir:str ):
        """
        This scraper downloads information from https://computo.oep.org.bo/
        """
        # Project path

        self.PROJECT_PATH = project_path
        self.DOWNLOAD_DIR = download_dir

        self.elections_options = {
            "opt1"      :   "Elecciones Generales 2014",
            "opt2"      :   "Elecciones Generales 2014 Exterior",
            "opt3"      :   "Elecciones Diputados Uninominales 2014",
            "opt4"      :   "Elecciones Diputados Especiales 2014"
        }

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
                "profile.default_content_setting_values.notifications": 1,
                "download.default_directory": self.DOWNLOAD_DIR,
                "download.prompt_for_download": False,
                "download.directory_upgrade": True,
                "safebrowsing.enabled": True
                
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


    def run_scraper_dep(self, dep_id:int, selectors:dict,  headless:bool = False )->None:
        """
        Download a file from a given page.
        
        
        :PARAMS:
        -------
        :params: dep_id: int - the index position in the list of departamentos dropdown to download.
        :param: headless: bool - if we run the scraper in headless mode (WITH OUT UI)

        :RETURNS:
        --------
        PATH TO THE DOWNLOADED FILE
        """

        try:
                
            # Load the base link for the page
            link = selectors.get("base_link")

            # Create web Driver 
            driver = self._login_custom( input_link = link,
                        headless = headless)

            # Take some time for load the Page ....
            time.sleep(5)

            # SCRAP Dropdown buttons

            dropdown_buttons = driver.find_elements_by_xpath(selectors.get("dropdown_buttons"))

            time.sleep(5)

            dropdown_buttons[0].click()

            time.sleep(5)
            
            #list dropdown inner elements

            dropdown_elements = driver.find_elements_by_xpath(selectors.get("dropdown_els"))

            time.sleep(5)

            #click on the last element
            dropdown_elements[-1].click()

            time.sleep(5)

            # Click on "Consultar"

            button_consultar = driver.find_elements_by_xpath(selectors.get("consultar_button"))

            button_consultar[-1].click()
            
            time.sleep(5)

            ##############################
            #############################
            # Search for buttom content
            bottom_content = driver.find_elements_by_xpath(selectors.get("download_button"))

            time.sleep(5)

            # Perform click on donwload button
            # This will download the file into the 
            bottom_content[1].click()
            
            time.sleep(5)

            pop_up_window = driver.find_element_by_xpath(selectors.get("popup_field"))

            print("popup field ....")

            time.sleep(5)
            # Search for "Exportar CSV" button

            if pop_up_window is not None:
                deps_drop_down = pop_up_window.find_element_by_xpath(selectors.get("dep_fields"))
                deps_drop_down.click()
                time.sleep(5)
                dep_fields = driver.find_elements_by_xpath(selectors.get("dep_fields_options"))
                print(len(dep_fields))
                dep_fields[dep_id].click()
                time.sleep(5)
                button_consultar = pop_up_window.find_elements_by_xpath(selectors.get("consultar_button"))
                button_consultar[-1].click()
                time.sleep(10)
           
            driver.close()


        except Exception as e:
            print(e)

            now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            log.logger.error(f"ERROR!!! at time: {now}, {e}")

        return None


    def main(self, selectors:dict,  headless:bool = False, kind="nal"):
        """
        Main pipelin for download the csv file from the page.

        Step 1. Download the CSV file
        Step 2. Read this CSV file and make something with it
        """
        for dep in range(0, 9):
            local_path_dir = self.run_scraper_dep(selectors = selectors, headless = headless, dep_id=dep)



if __name__ == "__main__":

    cwd = os.getenv("PROJ_DIR")

    # Create aux folder name for download files

    download_path = os.path.join(cwd, "tmp")

    # Open the selectors
    with open(f"{cwd}/selectors_nal.json") as a:
        selectors = json.load(a)

    # Create safe dir Folder 
    os.makedirs(download_path, exist_ok=True)  # succeeds even if directory exists.

    # Create Instance of the scraper
    while True:
        # Test main pipeline
        elecciones = EleccionesScraper(project_path = cwd , download_dir = download_path)
        elecciones.main(selectors=selectors, headless=True, kind = "nal")
