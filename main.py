
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
        This scraper downloads information from http://atlaselectoral.oep.org.bo/
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

    def run_scraper(self, selectors:dict,  headless:bool = False)->str:
        """
         Download a file from a given page.
         
         The name of the page is in selectors.json ->["base_link"],
         In this case is https://atlaselectoral.oep.org.bo/#/subproceso/17/1/1 , 
         this is the 2014 elections page, we can replace this link with any other link for scrap the page
         for the "Exportar CSV" button in this new format of the target page.

         Since this name is constat we take this as an approach for download the file in the bottom page
         when we madee .click() on the "Exportar CSV" button.
         
         :PARAMS:
         -------
         :param: headless: bool - if we run the scraper in headless mode (WITH OUT UI)

         :RETURNS:
         --------
         PATH TO THE DOWNLOADED FILE
        """

        # Load the base link for the page
        link = selectors.get("base_link")

        print(link)

        # Create web Driver 
        driver = self._login_custom( input_link = link,
                    headless = headless)

        # Take some time for load the Page ....
        time.sleep(5)

        # SCRAP BOTTOM CONTENT

        # Search for bottom content
        bottom_content = driver.find_elements_by_xpath(selectors.get("download_button"))

        time.sleep(5)

        # Perform click on donwload button
        # This will download the file into the 
        bottom_content[1].click()
        
        time.sleep(10)

        pop_up_window = driver.find_element_by_xpath(selectors.get("popup_field"))

        time.sleep(5)
        # Search for "Exportar CSV" button
        pop_up_download_button = driver.find_element_by_xpath(selectors.get("popup_download_button"))

        time.sleep(5)

        pop_up_download_button.click()

        time.sleep(5)

        # driver.close()

        # # Create path dir for the downloaded file
        # full_path_to_file = self.get_downloaded_file_name(folder = self.DOWNLOAD_DIR, 
        #                                 aprox_file_name = self.elections_options["opt1"])
        
        # print("full_path_to_file: ", full_path_to_file)

        # return full_path_to_file

    def run_scraper_nal(self, selectors:dict,  headless:bool = False)->str:
        """
        Download a file from a given page.
        
        The name of the page is in selectors.json ->["base_link"],
        In this case is https://atlaselectoral.oep.org.bo/#/subproceso/17/1/1 , 
        this is the 2014 elections page, we can replace this link with any other link for scrap the page
        for the "Exportar CSV" button in this new format of the target page.

        Since this name is constat we take this as an approach for download the file in the bottom page
        when we madee .click() on the "Exportar CSV" button.
        
        :PARAMS:
        -------
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

            time.sleep(10)

            # Click on "Consultar"

            button_consultar = driver.find_elements_by_xpath(selectors.get("consultar_button"))

            button_consultar[-1].click()
            
            time.sleep(20)

            ##############################
            #############################
            # Search for buttom content
            bottom_content = driver.find_elements_by_xpath(selectors.get("download_button"))

            time.sleep(5)

            # Perform click on donwload button
            # This will download the file into the 
            bottom_content[1].click()
            
            time.sleep(10)

            pop_up_window = driver.find_element_by_xpath(selectors.get("popup_field"))

            time.sleep(5)

            if pop_up_window is not None:

                dialog_buttons = pop_up_window.find_element_by_xpath(selectors.get("dialog_field"))
                
        
                if dialog_buttons is not None:
                    download_el = driver.find_elements_by_xpath(selectors.get("popup_download_button"))
                    #download_el = dialog_buttons.find_element_by_xpath(selectors.get("popup_download_button"))
                    download_el[-1].click()

            time.sleep(5)
            
            driver.close()

            print("DONE!!!")
            # # Create path dir for the downloaded file
            # full_path_to_file = self.get_downloaded_file_name(folder = self.DOWNLOAD_DIR, 
            #                                 aprox_file_name = self.elections_options["opt1"])
            
            # print("full_path_to_file: ", full_path_to_file)

            # return full_path_to_file
            now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            log.logger.info(f"DONE!!! at time: {now}")

        except Exception as e:
            print(e)

            now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            log.logger.error(f"ERROR!!! at time: {now}, {e}")

        return None

    def run_scraper_excel(self, selectors:dict,  headless:bool = False):
        try:
                
            print("SELECTORS: ", selectors)
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

            time.sleep(10)

            # Click on "Consultar"

            button_consultar = driver.find_elements_by_xpath(selectors.get("consultar_button"))

            button_consultar[-1].click()
            
            time.sleep(20)

            ##############################
            #############################
            # Search for buttom content
            bottom_content = driver.find_elements_by_xpath(selectors.get("download_button"))

            time.sleep(5)

            # Perform click on donwload button
            # This will download the file into the 
            bottom_content[1].click()
            
            time.sleep(10)

            pop_up_window = driver.find_element_by_xpath(selectors.get("popup_field"))

            time.sleep(5)

            if pop_up_window is not None:
                
                excel_button = pop_up_window.find_element_by_xpath(selectors.get("excel_button"))
                
                if excel_button is not None:
                    excel_button.click()
                    time.sleep(5)

                    # Load again the popup?

                    pop_up_window = driver.find_element_by_xpath(selectors.get("popup_field"))

                    dialog_buttons = pop_up_window.find_element_by_xpath(selectors.get("dialog_field"))
                
                    if dialog_buttons is not None:
                        download_el = driver.find_elements_by_xpath(selectors.get("popup_download_button"))
                        print(len(download_el))
                        #download_el = dialog_buttons.find_element_by_xpath(selectors.get("popup_download_button"))
                        download_el[-1].click()

            time.sleep(5)
            
            driver.close()

            print("DONE!!!")
            # # Create path dir for the downloaded file
            # full_path_to_file = self.get_downloaded_file_name(folder = self.DOWNLOAD_DIR, 
            #                                 aprox_file_name = self.elections_options["opt1"])
            
            # print("full_path_to_file: ", full_path_to_file)

            # return full_path_to_file
            now = str(datetime.now())
            log.logger.info(f"DONE!!! at time: {now}")
        except Exception as e:
            now = str(datetime.now())
            log.logger.error(f"ERROR!!! at time: {now}")
        return None

    def main(self, selectors:dict,  headless:bool = False, kind="nal"):
        """
        Main pipelin for download the csv file from the page.

        Step 1. Download the CSV file
        Step 2. Read this CSV file and make something with it
        """
        if kind == "nal":
            local_path_dir = self.run_scraper_nal(selectors = selectors, headless = headless)

    def main_excel(self, selectors:dict,  headless:bool = False):
        
        local_path_dir = self.run_scraper_excel(selectors = selectors, headless = headless)



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
    elecciones = EleccionesScraper(project_path = cwd , download_dir = download_path)
    
    # Test main pipeline
    elecciones.main(selectors=selectors, headless=False, kind = "nal")
    
    elecciones.main_excel(selectors=selectors, headless=False)

    
    # Test read remote csv
    #elecciones.test_read_remote_csv(csv_link = "http://atlaselectoral.oep.org.bo/descarga/52/votos_totales.csv")