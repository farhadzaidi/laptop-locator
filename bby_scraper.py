from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Initialize the WebDriver (e.g., for Chrome)
driver = webdriver.Chrome()

# Open the webpage
driver.get("https://www.bestbuy.com/site/laptop-computers/all-laptops/pcmcat138500050001.c?id=pcmcat138500050001")

# Wait for the pagination list to load
pagination = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "ol.paging-list")))

# Find the last page number
#last_page_number = int(driver.find_element(By.CSS_SELECTOR, "ol.paging-list li.page-item:last-child").text)
last_page_number = 1
# Iterate through each page
for page_number in range(1, last_page_number + 1):
    # Construct the URL for the current page
    if page_number > 1:
        url = f"https://www.bestbuy.com/site/searchpage.jsp?_dyncharset=UTF-8&browsedCategory=pcmcat138500050001&cp={page_number}&id=pcat17071&iht=n&ks=960&list=y&sc=Global&st=categoryid%24pcmcat138500050001&type=page&usc=All%20Categories"
        driver.get(url)
    print("Processing page", page_number)

    # Open the page


    # Wait for the product list to load
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "ol.sku-item-list")))


    # Find all products on the page
    products = driver.find_elements(By.CSS_SELECTOR, "ol.sku-item-list li.sku-item")

    # Process each product
    for product in products:
        #go to product page
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.column-middle")))

        title_element = product.find_element(By.CSS_SELECTOR, "div.column-middle h4.sku-title > a")
        title_element.click()

        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.col-xs-7.col-lg-8")))

        check_spec = driver.find_element(By.CSS_SELECTOR, "button.c-button.c-button-outline.c-button-md.show-full-specs-btn.col-xs-6")
        check_spec.click()

        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.overflow-scroll-wrapper")))


        # Go back to the previous page
        driver.execute_script("window.history.go(-1)")

        # Wait for the product list to load on the previous page
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "ol.sku-item-list li.sku-item")))











#        title_text = title_text.replace('-', '')
#        title = title_text.split()
#        sku = product.get_attribute("data-sku-id")
#        laptop_brand = title[0]
#        if laptop_brand == 'Macbook':
#            laptop_brand = 'Apple'
#        print(title)
#        print(sku)

# Close the browser
driver.quit()
