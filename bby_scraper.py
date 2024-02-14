from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException

# Initialize the WebDriver
driver = webdriver.Chrome()

# driver pulls catalog of laptops
o_url = "https://www.bestbuy.com/site/searchpage.jsp?_dyncharset=UTF-8&browsedCategory=pcmcat138500050001&id=pcat17071&iht=n&ks=960&list=y&qp=condition_facet%3DCondition~New&sc=Global&st=categoryid%24pcmcat138500050001&type=page&usc=All%20Categories"
driver.get(o_url)

# waits unti it sees css element
WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "ol.sku-item-list li.sku-item")))

# finds final page
last_page = driver.find_element(By.CSS_SELECTOR,
                                "div > div > div > div.component-sku-list > div > div.footer.top-border.wrapper > div.right-side > div > div.footer-pagination > ol > li:nth-child(5) > a")
last_page = int(last_page.text.strip())

for page in range(1, last_page):
    if page > 1:
        o_url = f"https://www.bestbuy.com/site/searchpage.jsp?_dyncharset=UTF-8&browsedCategory=pcmcat138500050001&cp={page}&id=pcat17071&iht=n&ks=960&list=y&qp=condition_facet%3DCondition~New&sc=Global&st=categoryid%24pcmcat138500050001&type=page&usc=All%20Categories"
        driver.get(o_url)

    print("1")
    title_elements = driver.find_elements(By.CSS_SELECTOR,
                                          " ol.sku-item-list > li.sku-item > div.shop-sku-list-item > div.list-item.sv > div.product-header > h4.sku-title > a")
    for title_element in title_elements:
        title_href = title_element.get_attribute("href")
        print(title_href, "123")
        print("2")
        # Finds item using css
        #products = driver.find_elements(By.CSS_SELECTOR, "ol.sku-item-list li.sku-item")

        #    for product in products:

        # will go to the page pulled from href
        driver.get(title_href)

        # waits unti it sees css element
        WebDriverWait(driver, 10).until(EC.presence_of_element_located(
            (By.CSS_SELECTOR, "div > div > div > div.row.p-none.m-none > div.col-xs-7.col-lg-8")))
        print("2")

        # waits for button to be clickable then clicks it
        spec_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable(
            (By.CSS_SELECTOR, "div > div > div > div > div:nth-child(2) > button.show-full-specs-btn")))
        spec_button.click()

        # waits for spec menu to load
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "div.overflow-scroll-wrapper > ul.zebra-stripe-list")))

        # pulls data from webpage
        specs_row = driver.find_elements(By.CSS_SELECTOR, "div.overflow-scroll-wrapper > ul.zebra-stripe-list")
        print(len(specs_row))

        # loop through each row of specs
        for row in specs_row:
            spec_title = row.find_element(By.CSS_SELECTOR, "div.zebra-row > div.drawer-modal-wrapper > div.property")
            spec_value = row.find_element(By.CSS_SELECTOR, "div.zebra-row > div.description")

            print(spec_title.text.strip(), " ", spec_value.text)

        # back to original page
        driver.get(o_url)

# exit
driver.quit()

# shop-sku-list-item-49988458 > div.shop-sku-list-item > div.list-item.sv > div.product-header > h4.sku-title > a