from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
import os
import time
import json


download_dir = os.path.abspath(".")

chrome_options = Options()
chrome_options.add_experimental_option('prefs', {
    'download.default_directory': download_dir,
    'download.prompt_for_download': False,
    'download.directory_upgrade': True,
    'safebrowsing.enabled': True
})

chrome_options.add_argument("--headless=new")

driver = webdriver.Chrome(options=chrome_options)

driver.command_executor._commands["send_command"] = ("POST", '/session/$sessionId/chromium/send_command')
params = {
    'cmd': 'Page.setDownloadBehavior',
    'params': {
        'behavior': 'allow',
        'downloadPath': download_dir
    }
}
driver.execute("send_command", params)

def load_config():
    with open("config.json") as config:
        return json.load(config)


def wait_for_page_load(driver,timeout=30):
    WebDriverWait(driver, timeout).until(
        lambda d: d.execute_script("return document.readyState") == "complete"
    )

def wait_for_download_complete(directory, timeout=30):
    end_time = time.time() + timeout
    while time.time() < end_time:
        files = os.listdir(directory)
        if any(f.endswith(".crdownload") for f in files):
            time.sleep(1)
        else:
            return True
    return False


def download_matched_file(url,match_file):
    driver.get(url)
    wait_for_page_load(driver)
    print("Page loaded")
    try:
        download_link = driver.find_element(By.XPATH,f"//a[contains(string(.),'{match_file}')]")
        print("Required element found")
    except Exception as e:
        print(f"Error: {e}")

    file_url=download_link.get_attribute('href')
    download_link.click()
    time.sleep(2)
    
    if wait_for_download_complete(download_dir):
        print("Download completed")
    else:
        print("Download failed or timed out")

def main():
    config=load_config()
    url=config['url']
    match_file=config['match_file']
    download_matched_file(url,match_file)

if __name__=="__main__":
    main()