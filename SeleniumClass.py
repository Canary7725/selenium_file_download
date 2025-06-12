import os
import time
import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class SeleniumUtils:
    def __init__(self,driver:webdriver.Chrome,wait_time=10):
        self.driver=driver
        self.wait=WebDriverWait(driver,wait_time)

    def get_all_hrefs(self):
        return [a.get_attribute("href") for a in self.driver.find_elements(By.TAG_NAME,"a") if a.get_attribute("href")]

    def get_elements_by_text(self,match_text):
        xpath=f'//a[contains(string(.),"{match_text}")]'
        return self.driver.find_elements(By.XPATH, xpath)
    
    def search_element_by_href_content(self,match_keyword):
        all_links = self.driver.find_elements(By.XPATH, '//a[@href]')
        pattern = re.compile(rf"{match_keyword}", re.IGNORECASE)  # Example pattern
        matched = [link for link in all_links if pattern.search(link.get_attribute('href'))]
        return matched
    
    def click_element(self,element):
        self.wait.until(EC.element_to_be_clickable(element)).click()

    def click_elements_by_xpaths(self,xpath_list):
        for xpath in xpath_list:
            try:
                self.wait.until(EC.element_to_be_clickable(xpath)).click()
            except Exception as e:
                print(f'Error: {e}')
            
    def accept_alert(self):
        try:
            self.wait.until(EC.alert_is_present())
            Alert(self.driver).accept()
        except Exception as e:
            print(f'Error: {e}')
    
    def wait_for_page_to_be_ready(self,timeout=20):
        WebDriverWait(self.driver,timeout).until(
            lambda d:d.execute_script("return document.readyState")=="complete"
        )

    def wait_until_clickable(self,locator:tuple):
        self.wait.until(EC.visibility_of_all_elements_located(locator))
        self.wait.until(EC.element_to_be_clickable(locator))
        return self.driver.find_element(*locator)
    
    def get_element_by_attribute_text_match(self, attr_name, match_text):
        xpath = f'//*[@{attr_name}]'
        elements = self.driver.find_elements(By.XPATH, xpath)
        for elem in elements:
            if elem.get_attribute(attr_name) == match_text:
                return elem
        return None

    def get_elements_with_attributes(self, attr_list):
        attr_xpath = " and ".join([f"@{attr}" for attr in attr_list])
        xpath = f'//*[{attr_xpath}]'
        return self.driver.find_elements(By.XPATH, xpath)

    def download_file_by_click(self, element, download_dir, timeout=30):
        before_files = set(os.listdir(download_dir))
        element.click()
        end_time = time.time() + timeout
        while time.time() < end_time:
            after_files = set(os.listdir(download_dir))
            new_files = after_files - before_files
            if new_files:
                downloaded_file = new_files.pop()
                file_path = os.path.join(download_dir, downloaded_file)
                if not file_path.endswith('.crdownload'):  # Chrome temp download
                    return True
            time.sleep(1)
        return False