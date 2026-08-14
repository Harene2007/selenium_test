import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys

BASE_URL = "https://www.testmuai.com/selenium-playground/"

def test_simple_form_demo(driver):
    """Test Scenario 1: Simple Form Demo"""
    driver.get(BASE_URL)
    
    # Click "Simple Form Demo"
    link = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.LINK_TEXT, "Simple Form Demo"))
    )
    link.click()
    
    # Validate URL contains "simple-form-demo"
    assert "simple-form-demo" in driver.current_url
    
    # Create variable and enter values
    message = "Welcome to TestMu AI"
    input_box = driver.find_element(By.ID, "user-message")
    input_box.send_keys(message)
    
    # Click "Get Checked Value"
    button = driver.find_element(By.CSS_SELECTOR, "#showInput")
    button.click()
    
    # Validate displayed message
    displayed_message = driver.find_element(By.ID, "message").text
    assert displayed_message == message

def test_drag_and_drop_sliders(driver):
    """Test Scenario 2: Drag & Drop Sliders"""
    driver.get(BASE_URL)
    
    # Click "Drag & Drop Sliders"
    link = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.PARTIAL_LINK_TEXT, "Drag & Drop Sliders"))
    )
    link.click()
    
    # Select slider "Default value 15"
    slider = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//div[@id='slider3']//input[@type='range']"))
    )
    
    # Drag to 95
    action = ActionChains(driver)
    
    # The slider width is mapped to the range (0-100).
    width = slider.size['width']
    
    # ActionChains move_to_element moves to the center of the slider (value 50).
    # To reach 95, we need to drag it 45% further to the right.
    offset = int(width * 0.45)
    
    # Perform the drag
    action.move_to_element(slider).click_and_hold().move_by_offset(offset, 0).release().perform()
    
    # Nudge if needed in case of pixel/rounding differences
    for _ in range(10): 
        current_val = int(driver.find_element(By.ID, "rangeSuccess").text)
        if current_val == 95:
            break
        elif current_val < 95:
            slider.send_keys(Keys.ARROW_RIGHT)
        elif current_val > 95:
            slider.send_keys(Keys.ARROW_LEFT)

    # Final assertion
    assert driver.find_element(By.ID, "rangeSuccess").text == "95"

def test_input_form_submit(driver):
    """Test Scenario 3: Input Form Submit"""
    driver.get(BASE_URL)
    
    # Click "Input Form Submit"
    link = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.LINK_TEXT, "Input Form Submit"))
    )
    link.click()
    
    # Click "Submit" without filling info
    submit_btn = driver.find_element(By.XPATH, "//button[contains(text(), 'Submit')]")
    submit_btn.click()
    
    # Assert validation error message
    name_input = driver.find_element(By.ID, "name")
    validation_msg = name_input.get_attribute("validationMessage")
    # Cross-browser check (Chrome: "Please fill out this field.", Safari may vary slightly but contains "fill")
    assert "fill" in validation_msg.lower() or "please fill in this field." in validation_msg.lower()
    
    # Fill in required fields
    name_input.send_keys("John Doe")
    driver.find_element(By.ID, "inputEmail4").send_keys("john.doe@example.com")
    driver.find_element(By.ID, "inputPassword4").send_keys("securepassword123")
    driver.find_element(By.ID, "company").send_keys("TestMu")
    driver.find_element(By.ID, "websitename").send_keys("https://testmuai.com")
    
    # Select Country "United States"
    country_dropdown = Select(driver.find_element(By.NAME, "country"))
    country_dropdown.select_by_visible_text("United States")
    
    # Fill remaining fields
    driver.find_element(By.ID, "inputCity").send_keys("New York")
    driver.find_element(By.ID, "inputAddress1").send_keys("123 Test Ave")
    driver.find_element(By.ID, "inputAddress2").send_keys("Apt 4B")
    driver.find_element(By.ID, "inputState").send_keys("NY")
    driver.find_element(By.ID, "inputZip").send_keys("10001")
    
    # Click Submit
    submit_btn.click()
    
    # Validate success message
    success_msg_locator = (By.CSS_SELECTOR, ".success-msg")
    success_element = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located(success_msg_locator)
    )
    
    assert "Thanks for contacting us, we will get back to you shortly." in success_element.text
