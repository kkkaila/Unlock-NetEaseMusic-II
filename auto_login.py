# coding: utf-8

import os
import time
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from retrying import retry

# Configure logging
logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(asctime)s %(message)s')

@retry(wait_random_min=5000, wait_random_max=10000, stop_max_attempt_number=3)
def enter_iframe(browser):
    logging.info("Enter login iframe")
    time.sleep(5)  # 给 iframe 额外时间加载
    try:
        iframe = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.XPATH, "//*[starts-with(@id,'x-URS-iframe')]")
        ))
        browser.switch_to.frame(iframe)
        logging.info("Switched to login iframe")
    except Exception as e:
        logging.error(f"Failed to enter iframe: {e}")
        browser.save_screenshot("debug_iframe.png")  # 记录截图
        raise
    return browser

@retry(wait_random_min=1000, wait_random_max=3000, stop_max_attempt_number=5)
def extension_login():
    chrome_options = webdriver.ChromeOptions()

    logging.info("Load Chrome extension NetEaseMusicWorldPlus")
    chrome_options.add_extension('NetEaseMusicWorldPlus.crx')

    logging.info("Initializing Chrome WebDriver")
    try:
        service = Service(ChromeDriverManager().install())  # Auto-download correct chromedriver
        browser = webdriver.Chrome(service=service, options=chrome_options)
    except Exception as e:
        logging.error(f"Failed to initialize ChromeDriver: {e}")
        return

    # Set global implicit wait
    browser.implicitly_wait(20)

    browser.get('https://music.163.com')

    # Inject Cookie to skip login
    logging.info("Injecting Cookie to skip login")
    browser.add_cookie({"name": "MUSIC_U", "value": "009C9B5CB511C53AD5B714B5011036FA529A1F615EF87A8F1A5071C4271E1DB45D7DF28457FB25414B382F184F47B46E1754AC9BC570CFE667FB34C6B58F324452A92BD7B793DBF1A9CDD803E19D02531C1BCCEA87231E41BEE9CA657285F47D5EAB5756F832013D689197FD77310608C4B5932A6FB5A081E2CC7EFE97423FA8523D15628F7ECB55C442D766F4D600F92CC2F186576F198150A8B86E3123E2FA8E40F5C2EF89AD4D4A0DED8341157E2B357590A0B9D19B20EAFE06EB6294BF83E701125D4CE7C9F84F291B8ECBDFA56CD225412D96D36332AB4E417588B095B1BDC135738045EF848E00C41D7EC625249902FA099E2A345E42ABF8108C913358B383101318ABD2D996B8DF0225B0FAD51CAC5DA9A024B0D3AB70FC901590E6E7E4140B113CCD51F8A11468FA05346900F25BE2F20BA8AEAE2906554756FC844C4ECD2534A1F38536ACE9997A7F31C9A2047AC23946D267306834357E207A180304"})
    browser.refresh()
    time.sleep(5)  # Wait for the page to refresh
    logging.info("Cookie login successful")

    # Confirm login is successful
    logging.info("Unlock finished")

    time.sleep(10)
    browser.quit()


if __name__ == '__main__':
    try:
        extension_login()
    except Exception as e:
        logging.error(f"Failed to execute login script: {e}")
