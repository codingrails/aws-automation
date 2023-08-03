import time
from datetime import datetime, timedelta
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import re

Email = "email"
Password = "password"

filename = "input.txt"  # Replace with the path to your input file

codes = []
with open(filename, "r") as file:
    for line in file:
        line = line.strip().replace(" ", "")  # Remove leading/trailing spaces and spaces within the line
        codes.append(line)

driver = webdriver.Chrome()
driver.maximize_window()

driver.get("https://aws.amazon.com/")
time.sleep(5)

button = driver.find_element(By.CSS_SELECTOR, '.data-attr-wrapper.lb-tiny-iblock.lb-none-pad.lb-box')
button.click()
time.sleep(5)

email_input = driver.find_element(By.CSS_SELECTOR, 'input#resolving_input')
email_input.clear()
email_input.send_keys(Email)
time.sleep(4)

button = driver.find_element(By.CSS_SELECTOR, 'button#next_button')
button.click()
time.sleep(10)

password_input = driver.find_element(By.CSS_SELECTOR, 'input#password')
password_input.clear()
password_input.send_keys(Password)
time.sleep(4)

button = driver.find_element(By.CSS_SELECTOR, 'button#signin_button')
button.click()
time.sleep(10)

with open("output.txt", "a+") as file:
    # Read the existing codes from the file
    existing_codes = set()
    file.seek(0)
    for line in file:
        code = line.split(":")[0].strip()
        existing_codes.add(code)

    # Calculate the time to wait for 10 minutes from the last execution
    wait_time = timedelta(hours=24)
    last_execution_time = datetime.now() - wait_time

    valid_codes_count = 0  # Track the count of new valid codes
    for i, c in enumerate(codes):
        # Check if the code is already present in the existing codes
        if c in existing_codes:
            print(f"The code {c} already exists in the file. Skipping...")
            continue

        driver.get("https://us-west-2.console.aws.amazon.com/activate/home?region=us-east-1#/apply-for-credits")
        time.sleep(10)
        radio_button = driver.find_element(By.XPATH, '//input[contains(@id, "value-PORTFOLIO")]')
        radio_button.click()
        time.sleep(5)
        input_field = driver.find_element(By.CSS_SELECTOR, 'input.awsui_input_2rhyz_phpti_97')

        input_field.clear()
        input_field.send_keys(c)
        time.sleep(4)
        continue_button = driver.find_element(By.CSS_SELECTOR, 'button.awsui_primary-button_1xupv_s2w1u_391.awsui_button_vjswe_zs0n5_101.awsui_variant-primary_vjswe_zs0n5_210')
        continue_button.click()
        time.sleep(5)

        try:
            # Try to find the <a> tag using XPath and its text
            a_tag = driver.find_element(By.XPATH, '//a[contains(text(), "Choose a credit package")]')

            response = "valid"
            time.sleep(5)

            # Find all elements containing text starting with "$"
            dollar_elements = driver.find_elements(By.XPATH, '//*[starts-with(normalize-space(), "$")]')
            dollar_values = []
            for element in dollar_elements:
                matches = re.findall(r"\$\d{1,3}(?:,\d{3})*(?:\.\d+)?", element.text)
                dollar_values.extend(matches)

            valid_numbers = set()
            for value in dollar_values:
                amount = re.search(r"\d{1,3}(?:,\d{3})*(?:\.\d+)?", value)
                if amount:
                    valid_numbers.add(amount.group())

            if valid_numbers:
                formatted_numbers = [format(float(num.replace(",", "")), ",") for num in valid_numbers]
                formatted_numbers = [f"${num}" for num in formatted_numbers]
                file.write(f"{c}: {response} {' | '.join(formatted_numbers)}\n")
                valid_codes_count += 1  # Increment the count of new valid codes

        except NoSuchElementException:
            response = "invalid"
            file.write(f"{c}: {response}\n")

        print(f"The code {c} is {response}")

        # Pause for 10 minutes after checking every 2 codes
        if (i + 1) % 20 == 0:
            print("Pausing for 24 hours...")
            time.sleep(wait_time.total_seconds())

    driver.quit()
