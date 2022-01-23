from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from perfecto import PerfectoExecutionContext, TestResultFactory, TestContext, PerfectoReportiumClient
from perfecto import model

from selenium.webdriver.support.wait import WebDriverWait

# 1. Replace "<Cloud Name>" with your cloud name (e.g, trial is the cloudName of trial.app.perfectomobile.com)
cloudName = "<Cloud Name>"

capabilities = {
    #  2. Replace <<security token>> with your perfecto security token.
    'securityToken': "<<security token>>",

    # 3. Set Windows VM/browser capabilities.
    'platformName': 'Windows',
    'platformVersion': '10',
    'browserName': 'Chrome',
    'browserVersion': '97',
    'location': 'US East',
    'resolution': '1024x768',

    #Script Name
    'scriptName': 'PythonWindowsChrome',

    # Set other capabilities.
    'takesScreenshot': False,
    'screenshotOnError': True
}

# Initialize the Selenium driver
driver = webdriver.Remote('https://' + cloudName + '.perfectomobile.com/nexperience/perfectomobile/wd/hub',capabilities)
print("Driver initiation successful")

# set implicit wait time
driver.implicitly_wait(5)

wait = WebDriverWait(driver, 30)

# Define custom field tags key/value pair for reporting.
cf1 = model.CustomField('CustomTag1', 'Customvalue1')
cf2 = model.CustomField('CustomTag2', 'Customvalue2')

# Reporting client
perfecto_execution_context = PerfectoExecutionContext(webdriver=driver,
                                                              tags=['Tag1', 'Tag2'],
                                                              job=model.Job('ExpenseJob', '1', 'MainBranch'),
                                                              project=model.Project('ExpenseWindowsChrome', '1.0'),
                                                              customFields=[cf1,cf2])

reporting_client = PerfectoReportiumClient(perfecto_execution_context)
print("Reporting client created")

# Test start
reporting_client.test_start('ExpenseWindowsChromePython', TestContext(customFields=[cf1, cf2], tags=['Native', 'Android']))

try:
    reporting_client.step_start("Navigate to URL")
    driver.get("http://expensetracker.perfectomobile.com")
    driver.maximize_window()
    reporting_client.step_end()

    reporting_client.step_start("Enter Email")
    email = wait.until(EC.presence_of_element_located((By.XPATH, "//*[@id='login_email']/input")))
    email.send_keys('test@perfecto.com')
    reporting_client.step_end()

    reporting_client.step_start("Enter Password")
    password = wait.until(EC.presence_of_element_located((By.XPATH, "//*[@id='login_password']/input")))
    password.send_keys('test123')
    reporting_client.step_end()

    reporting_client.step_start("Click on Login")
    login = wait.until(EC.presence_of_element_located((By.NAME, "login_login_btn")))
    login.click()

    reporting_client.step_start("Click on Logout")
    driver.find_element_by_name("log-out").click()
    reporting_client.step_end()

    reporting_client.test_stop(TestResultFactory.create_success())

except Exception as e:
    print("in Exception")
    reporting_client.test_stop(TestResultFactory.create_failure(str(e)))
    print(e)
finally:
    try:
        print("In final block")
        driver.quit()
        # Retrieve the URL of the Single Test Report, can be saved to your execution summary and used to download the report at a later point
        report_url = reporting_client.report_url()
        print("Test report URL: ", report_url)

    except Exception as e:
        print(e)

print('Windows Chrome Python Test run ended')