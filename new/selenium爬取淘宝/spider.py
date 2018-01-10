from selenium import webdiver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

browser = webdiver.Chrome()
def search():
  driver.get("https://www.taobao.com/")
  input = WebDriverWait(driver, 10).until(
      EC.presence_of_element_located((By.CSS_SELECTOR, "#q"))
  )

