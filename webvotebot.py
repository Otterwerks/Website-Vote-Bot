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

#define function
def choose(command):
    if command == "1":
        return options[0]
    elif command == "2":
        return options[1]
    elif command == "3":
        return random.choice(options)

#initialize variables
choice = ""
options = ["Grapefruit", "Eucalyptus"]
grapefruit_votes = 0
eucalyptus_votes = 0
start_time = 0
end_time = 0
chrome_options = Options()
chrome_options.add_argument('--log-level=3')

while True:
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
    headless = input("Show browser (y/n)? ")

    if headless != "y":
        chrome_options.add_argument('headless')

    #begin automation----------------------------------

    #open browser and begin timer
    start_time = time.time()
    driver = webdriver.Chrome(options=chrome_options)

    #tqdm() progress bar
    for _ in tqdm(range(int(number_of_votes))):

        click_try = 0
        
        try:
            #interpret input with choose funtion
            choice = choose(command) #must be in loop for random to function correctly

            #navigate to website and find buttons
            driver.get("https://www.eoproducts.com/")
            driver.execute_script("window.scrollTo(0, -5000)") #avoids spam detection in headless
            driver.switch_to.frame(driver.find_element_by_xpath("//*[@id='da810ed3_1538078810']/iframe"))
            WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "input[value='"+choice+"']")))
            radio_button = driver.find_element_by_xpath("//input[@value='"+choice+"']")
            vote = driver.find_element_by_id('submitButton')

            #make sure button is selected, try one more time to switch to frame and select choice before breaking on error
            while radio_button.is_selected() == False and click_try < 10:
                time.sleep(1)
                radio_button.click()
                click_try += 1
                
                
                    #driver.switch_to.frame(driver.find_element_by_xpath("//*[@id='da810ed3_1538078810']/iframe"))
                    #WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "input[value='"+choice+"']")))
                    #radio_button.click()
                    
                
            #time delays avoid spam detection
            time.sleep(1)
            vote.click()
            time.sleep(1)
            
            #count vote (only if successful)
            if choice == "Grapefruit":
                grapefruit_votes += 1
            elif choice == "Eucalyptus":
                eucalyptus_votes += 1
                
        except: #if there is an error...
            continue #try again

    #close browser and stop timer
    driver.quit()
    end_time = time.time()
    break

    #end automation------------------------------------

#final report and exit
print("\nProcess complete in " + str(round(end_time - start_time, 2)) + " seconds.")
print("Times voted for Grapefruit: " + str(grapefruit_votes))
print("Times voted for Eucalyptus: " + str(eucalyptus_votes))
print("Errors: " + str(int(number_of_votes) - (grapefruit_votes + eucalyptus_votes)))
pause("\nPress any key to exit.")
exit()








