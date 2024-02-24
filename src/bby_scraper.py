from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import mysql.connector
from datetime import datetime
import time
from dbconfig import DBCONFIG



def check_specs(url, l_cost):
    driver.get(url)
    #variables for laptop
    product_name = None #string
    brand = None #string
    cpu_brand = None #string
    cpu_model = "" #string
    cpu_model_n = "" #merge with cpu model to get i7 7399k
    gpu_brand = None #string
    gpu_mem = None #int
    gpu = None #string
    ram_size = None #int
    ram_type = None #string
    ram_speed = None #int
    storage_size = None #int
    storage_type = "" #string
    screen_res = None #int
    screen_refresh_rate = None #int
    screen_size = None #decimal
    has_webcam = 0 #int

    # waits for button to be clickable then clicks it
    spec_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable(
        (By.CSS_SELECTOR, "div > div > div > div > div:nth-child(2) > button.show-full-specs-btn")))
    spec_button.click()

    # pulls data from webpage
    specs_row = driver.find_elements(By.CSS_SELECTOR, "div.pdp-drawer-content > div.overflow-scroll-wrapper > ul.zebra-stripe-list > li.zebra-list-item > div.zebra-row")

    # loop through each row of specs
    for row in specs_row:
        spec_title = row.find_element(By.CSS_SELECTOR, "div.drawer-modal-wrapper > div.property")
        spec_value = row.find_element(By.CSS_SELECTOR, "div.description")
        if spec_title.text.strip() == "Product Name":
            product_name = spec_value.text.strip() #laptop_title VARCHAR
            product_split = product_name.split()
            for x in product_split:
                if x.endswith('”'):
                    screen_size = float(x.strip('”')) #screen_size DECIMAL
            if product_name.find("NVIDIA") > 0:
                x = product_name.find("NVIDIA")
                gpu = ""
                for y in range(0, 23):
                    gpu = (gpu + product_name[y + x]) #gpu string
                    gpu = gpu.strip("-")
                    gpu = gpu.rstrip()
        elif spec_title.text.strip() == "Screen Resolution":
            screen_res_split = spec_value.text.strip().split()
            screen_res = int(screen_res_split[2]) #screen_res INT
        elif spec_title.text.strip() == "Screen Size":
            screen_size = float(spec_value.text.split()[0])
        elif spec_title.text.strip() == "Refresh Rate":
            screen_refresh_rate = int(spec_value.text.strip("Hz"))
        elif spec_title.text.strip() == "Front-Facing Camera":
            if spec_value.text.strip().lower() == "yes":
                has_webcam = 1
            else:
                has_webcam = 0 #has_webcam int
        elif spec_title.text.strip() == "Processor Brand":
            cpu_brand = spec_value.text.strip() #cpu_brand VARCHAR
        elif spec_title.text.strip() == "Processor Model":
            cpu_model = spec_value.text.strip()
        elif spec_title.text.strip() == "Processor Model Number":
            cpu_model_n = spec_value.text.strip()
        elif spec_title.text.strip() == "Total Storage Capacity":
            storage = spec_value.text.strip().split()
            if storage[1].lower().startswith("t"):
                storage_size = int(storage[0]) * 1000#storage_size INT
            else:
                storage_size = int(storage[0])
        elif spec_title.text.strip() == "Solid State Drive Capacity":
            ssd = spec_value.text.strip().split()
            if ssd is not None:
                storage_type = storage_type + "SSD" + " "
        elif spec_title.text.strip() == "Hard Disk Drive Capacity":
            hdd = spec_value.text.strip().split()
            if hdd is not None:
                storage_type = storage_type + "HDD" + " "
        elif spec_title.text.strip() == "System Memory (RAM)":
            ram_size = int(spec_value.text.strip().split()[0])#ram_size INT
        elif spec_title.text.strip() == "Type of Memory (RAM)":
            ram_type = spec_value.text.strip()#ram_type VARCHAR
        elif spec_title.text.strip() == "System Memory RAM Speed":
            ram_speed = int(spec_value.text.strip().split()[0])#ram_speed INT
        elif spec_title.text.strip() == "GPU Brand":
            gpu_brand = spec_value.text.strip()#gpu_brand string
        elif spec_title.text.strip() == "Graphics Type":
            if spec_value.text.strip() == "Integrated":
                gpu = "Integrated GPU"
        elif spec_title.text.strip() == "Graphics Memory":
            gpu_mem = int(spec_value.text.strip().split()[0])#gpu_mem INT
        elif spec_title.text.strip() == "Brand":#G
            brand = spec_value.text.strip()

    # cpu name code
    cpu_name = cpu_merge(cpu_model, cpu_model_n)

    # laptop id code
    laptop_id = (
            brand +
            cpu_brand +
            (cpu_name.replace(" ", "") if cpu_name is not None else "") +
            (gpu_brand.replace(" ", "") if gpu_brand is not None else "") +
            (gpu.replace(" ", "") if gpu is not None else "") +
            str(ram_size) +
            str(storage_size) +
            str(screen_res) +
            str(screen_size)
    ).lower()

    current_date = datetime.now().date()

    # begin adding to database here
    laptop_specs = {
        "laptop_id" : laptop_id,
        "laptop_title": product_name,
        "price": l_cost,
        "laptop_brand": brand,
        "cpu_brand": cpu_brand,
        "cpu_name": cpu_name,
        "gpu_brand": gpu_brand,
        "gpu_name": gpu,
        "gpu_mem": gpu_mem,
        "ram_size": ram_size,
        "ram_type": ram_type,
        "ram_speed": ram_speed,
        "storage_size": storage_size,
        "storage_type": storage_type,
        "screen_res" : screen_res,
        "screen_refresh_rate" : screen_refresh_rate,
        "screen_size" : screen_size,
        "has_webcam": has_webcam
    }
    print(laptop_id, "/n", url)
    sql_laptop = "INSERT INTO laptop (laptop_id, laptop_title, price, laptop_brand, cpu_brand, cpu_name, gpu_brand, gpu_name, gpu_mem, ram_size, ram_type, ram_speed, storage_size, storage_type, screen_res, screen_refresh_rate, screen_size, has_webcam) VALUES (%s, %s, %s, %s, %s,%s, %s, %s, %s, %s,%s, %s, %s, %s, %s, %s, %s, %s)"
    sql_prices = "INSERT INTO price (laptop_id, retailer_id, price, recorded_date) VALUES (%s, %s, %s, %s)"
    laptop_values = (laptop_id, product_name, l_cost, brand, cpu_brand, cpu_name, gpu_brand, gpu, gpu_mem, ram_size, ram_type, ram_speed, storage_size, storage_type, screen_res, screen_refresh_rate, screen_size, has_webcam)
    price_values = (laptop_id, 1, l_cost, current_date)

    try:
        cursor.execute(sql_laptop, laptop_values)
    except Exception as e:
        print(e)

    try:
        cursor.execute(sql_prices, price_values)
    except Exception as e:
        print(e)

    mydb.commit()
# this function merges cpu model and model number to get a proper cpu name
def cpu_merge(model, model_n):
    cpu = ""
    m_s = model.split()
    try:
        if m_s[0] == "Apple":
            cpu = model
        elif "Generation" in model:
            m_s = model.split()
            cpu = m_s[3] + " " + m_s[-1] + " " + model_n.strip()
        elif "Ultra" in model:
            cpu = m_s[2] + " " + m_s[3] + " " + model_n.strip()
        elif "Ryzen" in model:
            cpu = "Ryzen " + m_s[2] + " " + model_n.strip()
        else:
            cpu = " ".join(m_s[1:]) + " " + model_n.strip()
    except IndexError as e:
        print(f"Error while merging CPU names: {e}")
    return cpu


# this function tests the connection to the database
def test_database_connection(connection):
    try:
        connection.ping()
        print("Database connection successful.")
    except mysql.connector.Error as e:
        print(f"Error connecting to the database: {e}")


mydb = mysql.connector.connect(**DBCONFIG)

test_database_connection(mydb)
# Begin Time
start_time = time.time()
cursor = mydb.cursor()

# Initialize the WebDriver
driver = webdriver.Chrome()

# driver pulls catalog of laptops
o_url = "https://www.bestbuy.com/site/searchpage.jsp?_dyncharset=UTF-8&browsedCategory=pcmcat138500050001&id=pcat17071&iht=n&ks=960&list=y&qp=condition_facet%3DCondition~New&sc=Global&st=categoryid%24pcmcat138500050001&type=page&usc=All%20Categories"
driver.get(o_url)

# Looks for the max amount of page
last_page = driver.find_element(By.CSS_SELECTOR,"div > div > div > div.component-sku-list > div > div.footer.top-border.wrapper > div.right-side > div > div.footer-pagination > ol > li:nth-child(5) > a")
last_page = int(last_page.text.strip())

# Stores the href for every laptop on the current page
href_arr = list()
for page in range(1, 2):
    if page > 1:
        o_url = f"https://www.bestbuy.com/site/searchpage.jsp?_dyncharset=UTF-8&browsedCategory=pcmcat138500050001&cp={page}&id=pcat17071&iht=n&ks=960&list=y&qp=condition_facet%3DCondition~New&sc=Global&st=categoryid%24pcmcat138500050001&type=page&usc=All%20Categories"
        driver.get(o_url)

    products = driver.find_elements(By.CSS_SELECTOR, "ol.sku-item-list > li.sku-item div.embedded-sku > div > div > div.shop-sku-list-item > div.list-item > div.column-middle > h4.sku-title > a")
    counter = 1
    for product in products:
        product_href = product.get_attribute("href")
        href_arr.append(product_href)

    cost = driver.find_elements(By.CSS_SELECTOR, "li.sku-item > div.embedded-sku > div > div > div.shop-sku-list-item > div.list-item > div.column-right > div.sku-list-item-price > div > div > div > div.pricing-price > div.pricing-price > div > div > div.pricing-price.priceView-price > div.flex > div > div > div.priceView-hero-price > span:first-child")
    n_cost = list()
    for price in cost:
        n_price = price.text.replace(",", "").replace("$", "").replace(" ", "")
        n_cost.append(float(n_price.strip()))

    for url, n_price in zip(href_arr, n_cost):
        print("Page:", page, "\nProduct:", counter)
        try:
            check_specs(url, n_price)
            counter = counter + 1
        except Exception as e:
            print(e)
            check_specs(url, n_price)

    driver.get(o_url)
# End Time
end_time = time.time()
elapsed_time = end_time - start_time
print(f"Time taken: {elapsed_time} seconds")
# exit
cursor.close()
mydb.close()
driver.quit()
