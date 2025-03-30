from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

from apps.web_crawler.dubai.config import BASE_URL, get_chrome_driver
from apps.web_crawler.dubai.utils import save_links_to_file

def scroll_down(driver):
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(2)

def crawl_dubai_buildings():
    driver = get_chrome_driver()
    driver.get(BASE_URL)

    building_links = set()
    page_number = 1

    while True:
        print(f"In progress {page_number}...")

        for _ in range(3):
            scroll_down(driver)

        try:
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//a[contains(@href, '/buildings/')]"))
            )
        except:
            print("Error loading building links!")

        buildings = driver.find_elements(By.XPATH, "//a[contains(@href, '/buildings/')]")

        for building in buildings:
            link = building.get_attribute("href")
            if link and "/buildings/" in link and "/page/" not in link:
                building_links.add(link)

        try:
            next_button = driver.find_element(By.XPATH, "//button[contains(text(), 'Next')]")
            driver.execute_script("arguments[0].click();", next_button)
            page_number += 1
            time.sleep(5)
        except:
            print("There is no next page. Scraping complete.")
            break

    driver.quit()
    print(f"All buildings are : {len(building_links)}")
    save_links_to_file(building_links)
    print("Links saved.")
