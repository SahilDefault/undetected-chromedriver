import csv
import time
from datetime import datetime
from math import ceil

from selenium.webdriver.common.by import By


def login(driver, username, password):
    # Sign in button
    btns = driver.find_elements(By.CSS_SELECTOR, "a.js-open-popup-login.nav-link")

    if not len(btns):
        print("Sign In button not found")
        return None

    btns[0].click()
    time.sleep(2)

    # input fields
    input_fields = driver.find_elements(By.CLASS_NAME, "WvIqLXU")
    email_field = input_fields[0]
    password_field = input_fields[1]

    email_field.click()
    email_fields = email_field.find_elements(By.CSS_SELECTOR, "input.field-input")
    email_fields[0].send_keys(username)

    time.sleep(2)

    password_field.click()
    password_fields = password_field.find_elements(By.CSS_SELECTOR, "input.field-input")
    password_fields[0].send_keys(password)

    time.sleep(2)

    continue_btn_instances = driver.find_elements(By.CSS_SELECTOR, "button.FW1syM7.L1yjt43.co-white.Kk1804g.OCrkteb")

    if not len(continue_btn_instances):
        print("Continue button not found")
        return None

    continue_btn_instances[0].click()
    time.sleep(2)

    return "SUCCESS"


def click_on_see_more_btn(driver, total_clicks):
    wait_time = 3
    total_wait_time = total_clicks * wait_time
    print("Estimated wait time: ", total_wait_time, " Seconds")
    see_more_btns = driver.find_elements(By.CLASS_NAME, "see-more-button")

    if not len(see_more_btns):
        print("See More buttons not found")
        return None
    try:
        for click_number in range(total_clicks):
            total_wait_time -= wait_time
            print("Click Number: ", click_number, " Time left: ", total_wait_time, " Seconds")
            see_more_btns[0].click()
            driver.implicitly_wait(10)
            time.sleep(wait_time)

    except Exception as ex:
        print("ERROR - click_on_see_more_btn: ", ex)
        return None

    return "SUCCESS"


def export_gig_reviews_data_to_csv(driver, csv_filename):
    headers = ['Username', 'Country', 'Time']
    total_reviews = driver.find_elements(By.CLASS_NAME, "review-item-component-wrapper")

    if not len(total_reviews):
        print("No reviews to export")
        return None

    print("Total reviews data to export: ", len(total_reviews))
    with open(f'{csv_filename}.csv', 'w', newline='') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(headers)

        i = 1
        for review in total_reviews:
            try:
                print("Review number: ", i)
                i += 1

                review_data = review.text.splitlines()
                if not len(review_data):
                    continue
                username = review_data[0]
                if len(username) == 1:
                    data = [review_data[1], review_data[2], review_data[4]]
                else:
                    data = [review_data[0], review_data[1], review_data[3]]
                csvwriter.writerow(data)

            except Exception as ex:
                print("ERROR - export_gig_reviews_data_to_csv: ", ex)

    return "SUCCESS"


def scrap_gig_reviews_data(driver, gig_url):
    driver.get(gig_url)

    print("PLEASE CLOSE POP UPS IF ANY, YOU HAVE 10 SECONDS")
    time_range = [i for i in range(0, 11)][::-1]

    for item in time_range:
        print("TIME LEFT: ", item)
        time.sleep(1)

    print("TIME OVER, PROCEEDING")

    # Find total reviews
    total_reviews_instance = driver.find_elements(By.CSS_SELECTOR, "span.rating-count-number")

    if not len(total_reviews_instance):
        print("Total reviews not found")
        return None

    total_reviews = int(total_reviews_instance[0].text.splitlines()[0].replace(',', ''))

    # Calculate total number of clicks
    total_clicks = ceil(total_reviews/5)

    print("Total clicks: ", total_clicks)

    is_success = click_on_see_more_btn(driver, total_clicks)

    if not is_success:
        print("All review buttons was not clicked")

    # Export reviews
    csv_filename = f"{datetime.now()}".replace(" ", "").replace(".", "").replace(":", "")
    print(csv_filename)

    is_success = export_gig_reviews_data_to_csv(driver, csv_filename)

    if not is_success:
        print("All data is not scrapped")

    return "SUCCESS"
