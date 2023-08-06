from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.select import Select
from datetime import datetime, timedelta
import time
import pandas as pd

   
def login_livevox(driver:webdriver, user:str,password:str)->None:
    
    """Función para iniciar sesión en livevox usando las credenciales de Marcel2.0

    Args:
        driver (webdriver): objeto webdriver de la libreria selenium
    """
    try:
        now = datetime.now().strftime('%c')
        link = 'https://portal.na6.livevox.com/'
        driver.get(link)

        client_c = 'Teleperformance_Col'
        usuario = user#'marcel2.0'
        contraseña = password#'pythonbot1'

        # LOGIN
        client_code = driver.find_element_by_name('clientCode') #driver.find_element_by_xpath('//*[@id="lv-app"]/div/div/div[2]/div/div[1]/div/div/div[2]/div[2]/div[1]/form/div[1]/div/input')
        time.sleep(1)
        input_user = driver.find_element_by_name('userName')#driver.find_element_by_xpath('//*[@id="lv-app"]/div/div/div[2]/div/div[1]/div/div/div[2]/div[2]/div[1]/form/div[2]/div/input')

        input_pass = driver.find_element_by_name('password')#driver.find_element_by_xpath('//*[@id="lv-app"]/div/div/div[2]/div/div[1]/div/div/div[2]/div[2]/div[1]/form/div[3]/div/input')
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
        print(f'Login Sucesfully with user: {usuario}-->{now}')
    except:
        print('Invalid Credentials')

def setting_selenium_options(headless:bool,download_path:str)->webdriver.ChromeOptions:
    """
    Funcion para configurar las opciones de seleniumm
    Args:
        headless (bool): parametro para inicializar selenium headless

    Returns:
        webdriver.ChromeOptions: Selenium object
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

def download_report_cdr_between_dates(driver:webdriver,report_name:str,call_center:str,start_date:str,end_date:str):

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
       