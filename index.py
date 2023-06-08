import time
import random
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup

def getRandomDelay():
    # Random delay between 2 and 5 seconds
    return random.uniform(2, 5)

def getRandomScroll():
    # Random scroll distance between 200 and 400 pixels
    return random.randint(200, 400)

def scrapeGoogleResults(query, numPages):
    try:
        driver = webdriver.Chrome()  # Assurez-vous d'avoir le driver Chrome correctement installé et configuré
        driver.get('https://www.google.com')
        time.sleep(10)  # Attendez que la page se charge complètement

        search_input = driver.find_element(By.NAME, 'q')
        search_input.send_keys(query)
        search_input.send_keys(Keys.RETURN)

        results = []

        for page in range(numPages):
            results_html = driver.page_source
            soup = BeautifulSoup(results_html, 'html.parser')

            result_elements = soup.select('.g')

            for result_element in result_elements:
                title = result_element.select_one('.LC20lb').text
                link = result_element.select_one('.yuRUbf a')['href']

                snippet = ''
                snippet_element = result_element.select_one('.VwiC3b')
                if snippet_element:
                    snippet = snippet_element.get_text(strip=True)

                result = {
                    'title': title,
                    'snippet': snippet,
                    'link': link
                }
                results.append(result)

            if page != numPages - 1:
                next_button = driver.find_element(By.ID, 'pnnext')
                driver.execute_script("arguments[0].scrollIntoView(true);", next_button)
                driver.execute_script(f"window.scrollBy(0, -{getRandomScroll()});")
                time.sleep(getRandomDelay())  # Attendez avant de cliquer sur le bouton Suivant

                next_button.click()

                time.sleep(getRandomDelay())  # Attendez que la page suivante se charge complètement

            # Save the results to a JSON file after each page
            with open('resultatRecherche/icloudResult.json', 'w') as file:
                json.dump(results, file, indent=4)

        print('Results have been saved to results.json')

        driver.quit()
    except Exception as e:
        print('Error while searching on Google:', str(e))
        driver.quit()

# Using the function to perform a search and scrape 2 pages of results
scrapeGoogleResults('site:vinted.fr @icloud.com', 40)

#site:vinted.fr @gmail.com
#site:linkedin.com @gmail.com
