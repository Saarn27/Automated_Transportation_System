import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import (
    ElementClickInterceptedException,
    ElementNotInteractableException,
    TimeoutException,
)

is_going_on_weekend_or_holiday = False

options = webdriver.ChromeOptions()
options.add_experimental_option("detach", True)

# Launch Chrome (Selenium 4.6+ auto-manages drivers)
driver = webdriver.Chrome(options=options)
wait = WebDriverWait(driver, 20)

# Open target page
driver.get("http://iride/auth/home.aspx")
# letting the page load
time.sleep(4)

# clicking on 'understood' button in first modal screen
modal = driver.find_element(By.XPATH, "//*[@id='divModalNotYetConfirmYourPresence']/div/div/div[3]/button")
modal.click()

# letting the page load
time.sleep(2)

signUpButton = driver.find_element(By.XPATH, "//*[@id='cph_btnBooking']")
signUpButton.click()

# letting the page load
time.sleep(2)


# Function to select available morning seat
def select_morning_seat():
    time.sleep(2)
    # Click the morning pickup button
    driver.find_element(By.ID, "divRideTypes").find_element(By.XPATH, "//*[@id='divRideTypes']/label[1]").click()
    time.sleep(2)
    # Get all form-group divs inside #divCarMic
    morning_seats_div = (driver.find_element(By.ID, "divCarMic").find_element(By.TAG_NAME, "div").find_elements(By.CLASS_NAME, "form-group"))

    # Loop through and find the first available seat
    for div in morning_seats_div:
        seats = div.find_elements(By.TAG_NAME, "span")
        for seat in seats:
            bg = seat.value_of_css_property("background-color")
            # checking if the seat is already booked (blue)
            if "0, 0, 139" in bg:
                return
            # checking if the seat is available (green)
            elif "0, 100, 0" in bg:  # check for green
                seat.click()
                print("Seat selected!")
                # Confirm booking
                time.sleep(2)
                driver.find_element(By.ID, "btnConfirmBooking").click()
                time.sleep(2)
                driver.find_element(By.XPATH,"//*[@id='divModalSavedSuccessfully']/div/div/div[3]/button",).click()
                return  # exit function after booking


def select_afternoon_seat():
    time.sleep(2)
    # Click the afternoon pickup button
    driver.find_element(By.ID, "divRideTypes").find_element(By.XPATH, "//*[@id='divRideTypes']/label[2]").click()
    time.sleep(2)
    # Get all form-group divs inside #divCarMic
    afternoon_seats_div = (driver.find_element(By.ID, "divCarMic").find_element(By.TAG_NAME, "div").find_elements(By.CLASS_NAME, "form-group"))

    # Loop through and find the first available seat
    for div in afternoon_seats_div:
        seats = div.find_elements(By.TAG_NAME, "span")
        for seat in seats:
            bg = seat.value_of_css_property("background-color")
            # checking if the seat is already booked (blue)
            if "0, 0, 139" in bg:
                return
            elif "0, 100, 0" in bg:  # check for green
                seat.click()
                print("Seat selected!")
                # Confirm booking
                time.sleep(2)
                driver.find_element(By.XPATH, "//*[@id='btnConfirmBooking']").click()
                time.sleep(2)
                driver.find_element(By.XPATH,"//*[@id='divModalSavedSuccessfully']/div/div/div[3]/button",).click()
                return  # exit function after booking


# Function to select available date
def select_date(days):
    for day in days.find_elements(By.TAG_NAME, "label"):
        # checking if the date is available (green) or if day is missing morning or afternoon (blue) or if the employee want to work on friday (white and is_going_on_weekend_or_holiday needs to be true)
        color = day.value_of_css_property("background-color")
        if color in ("rgba(255, 0, 0, 1)", "rgba(0, 0, 255, 1)") or (color == "rgba(255, 255, 255, 1)" and is_going_on_weekend_or_holiday):
            day.click()
            select_morning_seat()
            select_afternoon_seat()
    return


# now checking for if date to sign up is available and if so selecting it
daysToPick = driver.find_element(By.ID, "divDates2")
select_date(daysToPick)
