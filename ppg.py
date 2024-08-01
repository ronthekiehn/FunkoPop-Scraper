import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

from bs4 import BeautifulSoup

# Configure Chrome options
options = webdriver.ChromeOptions()
options.add_argument('--headless')  # Enable headless mode

driver=webdriver.Chrome(options=options)

# Inputs
popname = input("Enter funko pop: ")
reference = input("Reference number: ")
result = popname + " " + str(reference)
autographed = input("Is the funko Pop signed? ")

namelist = result.split(' ')
popname = '%20'.join(namelist)
if autographed.lower() == "yes":
    signed_by = input("Who is this Funko autographed by? ").strip().lower()

url = f'https://www.hobbydb.com/marketplaces/poppriceguide/catalog_items?filters[q][0]={popname}'
driver.get(url)

# Wait for the price guide to load
try:
    element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'price-guide')))
    if autographed.lower() == "yes":
        # Locate the link using XPath by its text
        link = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, "//a[contains(., 'Autographed')]")))
        
        # Scroll the link into view and click using JavaScript
        driver.execute_script("arguments[0].scrollIntoView(true);", link)
        WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//a[contains(., 'Autographed')]")))
        driver.execute_script("arguments[0].click();", link)

        # Wait for the next page to load
        WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CLASS_NAME, 'price-guide')))

except:
    print("Funko not found")
    exit()
finally:
    web_content = driver.page_source
    driver.quit()

soup = BeautifulSoup(web_content, 'html.parser')

for pop in soup.find_all("div", class_="catalog-item-card"):
    try:
        if autographed.lower() == "yes":
            autograph_li = pop.find('li', {"ng-if": "item.attributes.autographedBy && item.attributes.autographedBy.length > 0"})
            if autograph_li:
                # Extract the names from the <a> tags within the <li>
                autographed_by_list = [a.text.strip().lower() for a in autograph_li.find_all('a', class_='ng-binding')]
                autographed_by_str = ", ".join(autographed_by_list)

                # Check if the signed_by input matches any of the names
                if any(signed_by in autographed_name for autographed_name in autographed_by_list):
                    # Print the name of the Funko Pop
                    print("-------")
                    print("Name:", pop.find('a', class_='catalog-item-name').text.strip())
            
                    #Print Reference Number
                    ref_li = pop.find('li', {"ng-if": "!!item.attributes.refNumber"})
                    if ref_li:
                        reference_number = ref_li.find('span', class_='ng-binding').text.strip()
                        print("Reference Number:", reference_number)
                    
                    #Print Estimated Value
                    price_guide_text = pop.find('div', class_='price-guide').text.strip()
                    dollar_value = re.search(r'\$\d+', price_guide_text)  # Regex to find the dollar value
                    if dollar_value:
                        print("PPG Estimated Value:", dollar_value.group())
                    
                    # Print the autograph information
                    print("Autographed By:", autographed_by_str)
                    
                    #Print additional information, if available (this is the amount you can buy it for on other websites listed on PPG)
                    additional_info = pop.find('a', class_='btn btn-primary btn-sm ng-binding ng-scope').text.strip()
                    if additional_info:
                        print("Additional Info:", additional_info)
        if autographed.lower() != "yes":
            # Print Catalog Item Name
            funko_pop = pop.find('a', class_='catalog-item-name').text.strip()
            if funko_pop:
                print("-------")
                print("Funko Pop:", funko_pop)
            
            #Print Reference Number
            ref_li = pop.find('li', {"ng-if": "!!item.attributes.refNumber"})
            if ref_li:
                reference_number = ref_li.find('span', class_='ng-binding').text.strip()
                print("Reference Number:", reference_number)
            
            #Print Estimated Value
            price_guide_text = pop.find('div', class_='price-guide').text.strip()
            dollar_value = re.search(r'\$\d+', price_guide_text)  # Regex to find the dollar value
            if dollar_value:
                print("PPG Estimated Value:", dollar_value.group())
            
            #Print additional information, if available (this is the amount you can buy it for on other websites listed on PPG)
            additional_info = pop.find('a', class_='btn btn-primary btn-sm ng-binding ng-scope').text.strip()
            if additional_info:
                print("Additional Info:", additional_info)

    except:
        continue