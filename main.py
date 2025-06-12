# from selenium import webdriver
# from selenium.webdriver.chrome.options import Options
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# import os
# import time


# download_dir = os.path.abspath(".")

# chrome_options = Options()
# chrome_options.add_experimental_option('prefs', {
#     'download.default_directory': download_dir,
#     'download.prompt_for_download': False,
#     'download.directory_upgrade': True,
#     'safebrowsing.enabled': True
# })

# chrome_options.add_argument("--headless=new")

# driver = webdriver.Chrome(options=chrome_options)

# driver.command_executor._commands["send_command"] = ("POST", '/session/$sessionId/chromium/send_command')
# params = {
#     'cmd': 'Page.setDownloadBehavior',
#     'params': {
#         'behavior': 'allow',
#         'downloadPath': download_dir
#     }
# }
# driver.execute("send_command", params)



# def load_config():
#     with open("config.json") as config:
#         return json.load(config)


# def wait_for_page_load(driver,timeout=30):
#     WebDriverWait(driver, timeout).until(
#         lambda d: d.execute_script("return document.readyState") == "complete"
#     )

# def wait_for_download_complete(directory, timeout=30):
#     end_time = time.time() + timeout
#     while time.time() < end_time:
#         files = os.listdir(directory)
#         if any(f.endswith(".crdownload") for f in files):
#             time.sleep(1)
#         else:
#             return True
#     return False


# def search_element_by_partial_text(driver,match_file):
#     match_url=driver.find_element(By.PARTIAL_LINK_TEXT,match_file)
#     file_url=match_url.get_attribute("href")
#     return match_url


# def download_matched_file(match_link):
#     wait_for_page_load(driver)
#     print("Page loaded")
#     match_link.click()
#     time.sleep(2)
#     if wait_for_download_complete(download_dir):
#         print("Download completed")
#     else:
#         print("Download failed or timed out")

# def main():
#     config=load_config()
#     url=config['url']
#     match_file_name=config['match_file']
#     driver.get(url) #Getting all href from the page
#     download_matched_file(search_element_by_partial_text(driver,match_file_name))
#     # download_matched_file(html_content,match_file)

# if __name__=="__main__":
#     main()



import json
import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

from SeleniumClass import SeleniumUtils

def load_config():
    with open("config.json") as config:
        return json.load(config)



def main():
        # Set up download directory and Chrome options
    download_dir = os.path.abspath("downloads")
    os.makedirs(download_dir, exist_ok=True)

    chrome_options = Options()
    prefs = {"download.default_directory": download_dir}
    chrome_options.add_experimental_option("prefs", prefs)
    chrome_options.add_argument("--headless=new")  # optional: headless browser
    driver = webdriver.Chrome(service=Service(), options=chrome_options)

    utils=SeleniumUtils(driver)

    config=load_config()

    driver.get(config['url'])

    utils.wait_for_page_to_be_ready()


# Get all elements from matching the text content by passing match_keyword
    # elements_by_text=utils.get_elements_by_text("2024 HSD")
    # if elements_by_text:
    #     utils.click_element(elements_by_text[0])
    #     utils.wait_for_page_to_be_ready()
    # else:
    #     print("Couldn't find the page with the href content")
    # return

#Get all elements from matching the href content 
    # elements_by_href = utils.search_element_by_href_content("2024-HSD-Reference")
    # print(f"Found {len(elements_by_href)} downloadable file links.")
    # if elements_by_href:
    #     print("Trying to download the first file...")
    #     download_success = utils.download_file_by_click(elements_by_href[0], download_dir)
    #     print("Download success:", download_success)


#Get element by Attribute-text-match

    




    

    


if __name__=='__main__':
    main()
