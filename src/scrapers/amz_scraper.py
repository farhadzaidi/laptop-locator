from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

def create_driver():
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')

    driver = webdriver.Chrome(
        options=options,
        service=Service(ChromeDriverManager().install())
    )

    return driver

def create_records(driver, links):
    records = []
    for link in links:
        driver.get(link)
        record = []

def main():
    driver = create_driver()
    driver.get('http://amazon.com/s?k=laptop')

    # XPath is tentative since the structure or data-cy attribute could change
    # in the future. Unfortunately, Amazon does not use ids or names in their 
    # HTML so this is the best we can do for now.
    # TODO: add some form of verification
    xpath = "//div[@datacy='title-recipe']/h2/a" 
    anchors = driver.find_elements(By.XPATH, xpath)
    links = [a.get_attribute('href') for a in anchors]

    driver.quit()

if __name__ == '__main__':
    main()