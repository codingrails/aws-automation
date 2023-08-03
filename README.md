# AWS Code Activation Script

This script automates the process of activating AWS promo codes to claim AWS credits. It uses the Selenium library to navigate the AWS website and validates the codes from an input file. Valid codes and their corresponding AWS credit packages are saved to an output file. The script also handles waiting for 24 hours before rechecking a code that was previously found invalid.

## Prerequisites
- Python 3.x installed
- Chrome browser and ChromeDriver installed (compatible with your Chrome version)

## Installation
1. Install the required Python packages using pip:
```bash
pip install selenium
```
2. Download ChromeDriver from https://sites.google.com/a/chromium.org/chromedriver/downloads and make sure it is accessible from your system's PATH.

## Usage
1. Open the script in a text editor and replace `email` and `password` with your AWS account credentials.
2. Prepare an input file named `input.txt` containing the promo codes, with one code per line.
3. Run the script:
```bash
python aws_code_activation.py
```
4. The output will be saved in `output.txt`.

Note: Be cautious with your AWS credentials and avoid sharing them or committing them to version control.

## Script Details

1. Import required libraries.
2. Set your AWS account credentials (`Email` and `Password`).
3. Read the promo codes from the `input.txt` file and store them in a list.
4. Initialize a Selenium Chrome WebDriver and maximize the window.
5. Navigate to the AWS homepage and wait for the page to load.
6. Click the appropriate button to sign in and enter your AWS account email.
7. Click the "Next" button and enter your account password.
8. Click the "Sign in" button to log in to your AWS account.
9. Open the `output.txt` file and read the existing codes to avoid rechecking them too soon.
10. Calculate the waiting time for rechecking a code (24 hours from the last execution time).
11. Loop through the promo codes and check their validity by attempting to activate the AWS credits.
12. If the code is valid, extract the available credit packages and save them to the `output.txt` file.
13. If the code is invalid, mark it as such in the `output.txt` file.
14. Pause the script for 24 hours after checking every 20 codes to comply with AWS's activation policy.
15. Close the WebDriver and end the script.

Remember to run this script responsibly and in compliance with AWS's terms of service. Happy coding!
