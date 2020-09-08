import json

import pandas as pd
from urllib.request import Request, urlopen
import io
import os
import sys
import time
import glob

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager


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

    def run_scraper(self,  headless:bool = False)->str:
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
         headless = if we run the scraper in headless mode (WITH OUT UI)

         :RETURNS:
         --------
         PATH TO THE DOWNLOADED FILE
        """

        # Open the selectors
        with open(f"{self.PROJECT_PATH}/selectors.json") as a:
            selectors = json.load(a)

        # Load the base link for the page
        link = selectors.get("base_link")

        # Create web Driver 
        driver = self._login_custom( input_link = link,
                    headless = headless)

        # Take some time for load the Page ....
        time.sleep(5)

        # SCRAP BOTTOM CONTENT

        # Search for bottom content
        bottom_content = driver.find_elements_by_xpath(selectors.get("bottom_content_web_el"))

        # Search for "Exportar CSV" button
        download_button = bottom_content[0].find_element_by_xpath(selectors.get("download_votes_csv_button"))

        # Perform click on donwload button
        # This will download the file into the 
        download_button.click()
        
        time.sleep(5)

        driver.close()

        # Create path dir for the downloaded file
        full_path_to_file = self.get_downloaded_file_name(folder = self.DOWNLOAD_DIR, 
                                        aprox_file_name = self.elections_options["opt1"])
        
        print("full_path_to_file: ", full_path_to_file)

        return full_path_to_file

    def get_downloaded_file_name(self, folder:str, aprox_file_name:str)->str:
        """
         Compares two strings, if one is equal or aprox to the another, returns the original string.
         
         PARAMS:
         -------
            folder: string that represent the location of a lot of csv files.
            aprox_file_name: name for the year of the scraping , this is how is writed in the page.
         RETURNS:
         -------
         String, the full path to the downloaded file.

        """
        
        files = glob.glob(folder+"/*.csv")
        for f in files:

            f_name_norm = f.split("/")[-1].lower()
            aprox_file_name_norm = aprox_file_name.lower()

            if aprox_file_name_norm in f_name_norm:
                return f

        # if not match, return the last el in the list of files
        return files[-1]

    def test_read_remote_csv(self, csv_link):
        """
        Legacy code for read a href link to a remote csv  to Pandas Dataframe
        """

        response_raw = Request(csv_link, headers={'User-Agent': 'Mozilla/5.0'})
        response = urlopen(response_raw,  timeout=2).read()

        response = response.decode('utf-8')
        
        df =pd.read_csv(io.StringIO(response))

        print(df.head())
    
    def read_csv_to_dataframe(self, csv_path:str)->pd.DataFrame:
        """
        This method reads a csv file and returns a pandas dataframe
        """

        df = pd.read_csv(csv_path)


        return df

    def main(self,   headless:bool = False):
        """
        Main pipelin for download the csv file from the page.

        Step 1. Download the CSV file
        Step 2. Read this CSV file and make something with it
        """

        # Step 1
        local_path_dir = self.run_scraper( headless = headless)

        # Step 2
        df = self.read_csv_to_dataframe(csv_path = local_path_dir )

        print(df.head())


if __name__ == "__main__":

    cwd = os.getcwd()
    # Create aux folder name for download files
    download_path = os.path.join(cwd, "tmp")

    # Create safe dir Folder 
    os.makedirs(download_path, exist_ok=True)  # succeeds even if directory exists.


    # Create Instance of the scraper
    elecciones = EleccionesScraper(project_path = cwd , download_dir = download_path)
    
    # Test main pipeline
    elecciones.main(headless=False)

    # Test read remote csv
    #elecciones.test_read_remote_csv(csv_link = "http://atlaselectoral.oep.org.bo/descarga/52/votos_totales.csv")