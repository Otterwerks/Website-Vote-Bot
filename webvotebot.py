#this script automates the voting process for a fragrance preference poll, assuming the poll allows multiple votes per IP address and does not simply reassign the vote when voting from the same IP address
#install google chrome
#search for / download chromedriver.exe and place in the same directory as this script
#pip install selenium
#pip install getch
#pip install tqdm

import time
import random
import selenium
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from getch import pause
from tqdm import tqdm


while True:

    #initialize variables
    choice = ""
    options = ["Grapefruit", "Eucalyptus"]
    grapefruit_votes = 0
    eucalyptus_votes = 0
    start_time = 0
    end_time = 0
    chrome_options = Options()
    chrome_options.add_argument('--log-level=3')


    #define functions
    def choose(command):
        if command == "1":
            return options[0]
        elif command == "2":
            return options[1]
        elif command == "3":
            return random.choice(options)

    #print instructions
    print("\n     Website Vote Bot\n")
    print("Enter 1 to vote for Grapefruit")
    print("Enter 2 to vote for Eucalyptus")
    print("Enter 3 to vote randomly")
    print("Enter \"Quit\" to exit\n")

    #what to do
    command = input("1, 2, 3, or Quit? ")

    #check input
    if command == "Quit":
        exit()
    elif command not in {"1", "2", "3"}:
        print("Try again...")
        continue

    #how many times to run the script
    number_of_votes = input("Vote how many times? ")

    #check input
    try:
        int(number_of_votes)
    except ValueError:
        print("Enter a number...")
        continue

    #show browser option, no check needed
    headless = input("Hide browser (y/n)? ")

    if headless == "n":
        pass
    else:
        chrome_options.add_argument('headless')

    #begin main loop----------------------------------

    #open browser and begin timer
    driver = webdriver.Chrome(options=chrome_options)
    start_time = time.time()

    #tqdm() progress bar
    for _ in tqdm(range(int(number_of_votes))):
        try:
            #interpret input with choose funtion
            choice = choose(command)

            #navigate to website and find buttons
            driver.get("https://www.eoproducts.com/")
            #driver.find_element_by_id('shopify-section-1534423477636')
            #driver.find_element_by_id('shopify-section-1542417642909')
            #driver.find_element_by_class_name('aos-init')
            #driver.find_element_by_class_name('arrow-left') #necessary in case there is a video instead of image on homepage
            
            driver.execute_script("return arguments[0].scrollIntoView(true);", driver.find_element_by_id("da810ed3_1538078810"))
            driver.execute_script("return arguments[0].scrollIntoView(true);", driver.find_element_by_id("da810ed3_1538078810"))
            #driver.find_element_by_id("da810ed3_1538078810")
            #driver.switch_to.frame(driver.find_element_by_tag_name('iframe'))
            WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "input[value='"+choice+"']")))
            radio_button = driver.find_element_by_css_selector("input[value='"+choice+"']")
            vote = driver.find_element_by_id('submitButton')
            time.sleep(1)

            #make sure button is selected
            while radio_button.is_selected() == False:
                radio_button.click()
                time.sleep(1)

            #time delays avoid spam detection
            time.sleep(1)
            vote.click()
            time.sleep(1)

            #count votes
            if choice == "Grapefruit":
                grapefruit_votes += 1
            elif choice == "Eucalyptus":
                eucalyptus_votes += 1
        except: #if there is an error, try again...
            continue

    #close browser and stop timer
    driver.quit()
    end_time = time.time()
    break

    #end main looop------------------------------------

#final report and exit
print("\nProcess complete in " + str(round(end_time - start_time, 2)) + " seconds.")
print("Times voted for Grapefruit: " + str(grapefruit_votes))
print("Times voted for Eucalyptus: " + str(eucalyptus_votes))
print("Errors: " + str(int(number_of_votes) - (grapefruit_votes + eucalyptus_votes)))
pause("\nPress any key to exit.")
exit()








