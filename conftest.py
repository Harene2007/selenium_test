import os
import pytest
from selenium import webdriver

@pytest.fixture(params=["chrome", "safari"], scope="function")
def driver(request):
    browser = request.param
    
    # LambdaTest Credentials from Environment Variables
    username = os.environ.get("LT_USERNAME", "YOUR_LT_USERNAME")
    access_key = os.environ.get("LT_ACCESS_KEY", "YOUR_LT_ACCESS_KEY")
    
    # Grid URL
    grid_url = f"https://{username}:{access_key}@hub.lambdatest.com/wd/hub"
    
    # LambdaTest capabilities based on requested browser
    lt_options = {
        "user": username,
        "accessKey": access_key,
        "build": "Selenium 101 Assignment",
        "name": f"Test Scenario - {browser.capitalize()}",
        "platformName": "Windows 10" if browser == "chrome" else "macOS Catalina",
        "browserName": browser.capitalize() if browser != "chrome" else "Chrome",
        "version": "latest",
        "network": True,
        "visual": True,
        "video": True,
        "console": True
    }

    if browser == "chrome":
        options = webdriver.ChromeOptions()
    else:
        options = webdriver.SafariOptions()

    options.set_capability("LT:Options", lt_options)

    # Initialize remote webdriver
    driver = webdriver.Remote(command_executor=grid_url, options=options)
    
    driver.implicitly_wait(10)
    
    yield driver
    
    # Set status in LambdaTest dashboard based on test success/failure
    # Using pytest request node to determine if test failed
    if request.node.rep_call.failed:
        driver.execute_script("lambda-status=failed")
    else:
        driver.execute_script("lambda-status=passed")
        
    driver.quit()

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    # Execute all other hooks to obtain the report object
    outcome = yield
    rep = outcome.get_result()
    # Set an attribute for each phase of a call, which can
    # be "setup", "call", "teardown"
    setattr(item, "rep_" + rep.when, rep)
