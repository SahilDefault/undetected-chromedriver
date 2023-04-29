import undetected_chromedriver as uc
from fiverr_script.functions import login, scrap_gig_reviews_data


def run_fiverr_script():
    driver = uc.Chrome()
    driver.maximize_window()
    driver.get('https://www.fiverr.com/')

    print("Enter username/email : ")
    username = input()

    print("Enter password: ")
    password = input()

    is_success = login(driver, username, password)

    if not is_success:
        print("ERROR - LOGIN FAILED - PLEASE FIX ISSUE")
        return None

    print("Please type 'Y' once you entered the otp: ")
    confirmation = input()

    if str(confirmation).lower() != 'y':
        print("CONFIRMATION FAILED - PLEASE RUN SCRIPT AGAIN OR CONTACT DEVELOPER")
        return None

    print("THANKS FOR CONFIRMATION")

    print("PLEASE PASTE GIG URL: ")
    gig_url = input()

    is_success = scrap_gig_reviews_data(driver, gig_url)

    if not is_success:
        print("DATA NOT SCRAPPED PROPERLY - PLEASE CHECK ERROR LOGS")
        return None

    print("DATA SCRAPPED SUCCESSFULLY")
    driver.close()
