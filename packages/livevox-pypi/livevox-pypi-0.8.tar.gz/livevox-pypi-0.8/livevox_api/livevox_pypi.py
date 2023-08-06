from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.select import Select
from datetime import datetime, timedelta
import time
import pandas as pd
import os
import warnings
warnings.filterwarnings('ignore')
   
def login_livevox(driver:webdriver, username:str,password:str,client_code:str)->None:
    """Login livevox using username, password and client code.

    Args:
        driver (webdriver): Selenium object
        username (str): username
        password (str): password
        client_code (str): client code in livevox
    """
    
    try:
        now = datetime.now().strftime('%c')
        link = 'https://portal.na6.livevox.com/'
        driver.get(link)

        client_c = client_code #'Teleperformance_Col'
        usuario = username #'marcel2.0'
        contraseña = password #'pythonbot1'

        # LOGIN
        client_code = driver.find_element_by_name('clientCode')
        time.sleep(1)
        input_user = driver.find_element_by_name('userName')

        input_pass = driver.find_element_by_name('password')
        time.sleep(1)

        # Escribir en los inputs
        client_code.clear()
        client_code.send_keys(client_c)
        time.sleep(1)

        input_user.clear()
        input_user.send_keys(usuario)
        time.sleep(1)

        input_pass.clear()
        input_pass.send_keys(contraseña + Keys.RETURN)

        time.sleep(5)
        print(f'Login Successfully with user: {usuario}--> {now}')
    except:
        print('Invalid Credentials')

def setting_selenium_options(headless:bool,download_path = os.getcwd() )->webdriver.ChromeOptions:
    """Set the recommended selenium options 

    Args:
        headless (bool): True will run webdriver headless
        download_path (str): set the download path (cwd as default)

    Returns:
        webdriver.ChromeOptions: option webdriver object
    """
    options = webdriver.ChromeOptions()
    if headless == True:
        options.add_argument('--headless')
    
    options.add_argument("--disable-notifications")
    options.add_argument("--start-maximized")
    options.add_argument("--disable-extensions")
    options.add_argument("--proxy-server='direct://'")
    options.add_argument("--proxy-bypass-list=*")
    options.add_argument('--disable-gpu')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--no-sandbox')
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--allow-running-insecure-content')
    user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.50 Safari/537.36'
    options.add_argument(f'user-agent={user_agent}')
    prefs = {"download.default_directory" : download_path}
    options.add_experimental_option("prefs",prefs)
    return options

def download_report_cdr_between_dates(driver:webdriver,report_name:str,start_date:str,end_date:str,call_center:str = ''):
    """Download cdr report using the report name, call center and start,end dates.

    Args:
        driver (webdriver): Selenium object
        report_name (str): name of the report
        start_date (str): start date for fetch (mm-dd-YYYY)
        end_date (str): end date for fetch (mm-dd-YYYY)
        call_center (str): name of the lob for download (default: all lobs)
    """
    start_date = pd.to_datetime(start_date)
    end_date = pd.to_datetime(end_date)
    driver.get('https://portal.na6.livevox.com/Teleperformance_Col#review/1')
    driver.refresh()
    time.sleep(10)
    try:
        driver.switch_to.frame('lvshell__iframe')
    except:
        pass
    while start_date <= end_date:
        
        time.sleep(0.5)
        date_for_field = start_date.strftime('%m/%d/%Y')
        start_date_field = driver.find_element_by_id('search-panel__start-date')
        start_date_field.clear()
        start_date_field.send_keys(date_for_field)
        time.sleep(0.5)
        end_date_field = driver.find_element_by_id('search-panel__end-date')
        end_date_field.clear()
        end_date_field.send_keys(date_for_field)
        time.sleep(0.5)
        call_center_drop_down = Select(driver.find_element_by_id('callcenter_combo')) # Report format dropdown menu
        if call_center != '':
            call_center_drop_down.select_by_visible_text(call_center) # select call center 
        time.sleep(0.5)
        report_format = Select(driver.find_element_by_id('report_format_combo')) # Report format dropdown menu
        report_format.select_by_visible_text(report_name) # select report 
        driver.find_element_by_class_name('lv-button__inside').click() # click on 'Generate Report'
        time.sleep(1)
        start_date = start_date + timedelta(1)
    print('All the reports have been downloaded')  