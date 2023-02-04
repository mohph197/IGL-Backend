import os
from time import sleep
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains

def test_post_announcement(driver: webdriver.Chrome, wait: WebDriverWait):
    url = os.getenv('FRONTEND_URL')

    driver.get(url)
    # Handle authentication
    auth_token = os.getenv('TEST_TOKEN')
    driver.execute_script(f'localStorage.setItem("@token", "{auth_token}")')
    driver.refresh()

    def scroll_element_to_view(element):
        driver.execute_script('arguments[0].scrollIntoView(true);', element)
        wait.until(lambda driver: driver.execute_script('return arguments[0].getBoundingClientRect().bottom < window.innerHeight', element))

    # Navigate to announcements page
    wait.until(EC.element_to_be_clickable((By.ID, 'route-posted-announcements'))).click()
    # Go to create announcement page
    wait.until(EC.element_to_be_clickable((By.ID, 'route-posted-announcements/create'))).click()

    # Fill in form
    title = 'Test Announcement'
    price = '100000'
    surface = '100'
    address = 'Test Address'
    # Title
    wait.until(EC.presence_of_element_located((By.ID, 'Titre'))).send_keys(title)
    # Category
    wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '#Catégorie-select button'))).click()
    category_choice = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '#Catégorie-select li:nth-child(1)')))
    category = category_choice.text
    category_choice.click()
    # Type
    wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '#Type-select button'))).click()
    type_choice = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '#Type-select li:nth-child(1)')))
    type = type_choice.text
    type_choice.click()
    # Price
    wait.until(EC.presence_of_element_located((By.ID, 'Prix'))).send_keys(price)
    # Surface
    wait.until(EC.presence_of_element_located((By.ID, 'Surface'))).send_keys(surface)
    # Description
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#description .ql-editor'))).send_keys('This is a test announcement')
    # Pictures
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#photo-picker-0 input[type="file"]'))).send_keys(os.path.join(os.getcwd(), 'tests', 'selenium', 'res', 'announcement-picture.png'))
    # Wilaya
    wilaya_button = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#Wilaya-select button')))
    scroll_element_to_view(wilaya_button)
    wilaya_button.click()
    wilaya_choice = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '#Wilaya-select li:nth-child(2)')))
    wilaya = wilaya_choice.text
    wilaya_choice.click()
    # Commune
    wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '#Commune-select button'))).click()
    commune_choice = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '#Commune-select li:nth-child(2)')))
    commune = commune_choice.text
    commune_choice.click()
    location = f'{wilaya}\n{commune}'
    # Address
    wait.until(EC.presence_of_element_located((By.ID, 'Adresse'))).send_keys(address)
    # Map
    scroll_element_to_view(wait.until(EC.presence_of_element_located((By.ID, 'map'))))
    marker_pin = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#map .leaflet-marker-pane img')))
    marker_pin.click()
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#map .leaflet-popup-pane .leaflet-popup-content-wrapper'))).click()
    marker_action = ActionChains(driver)
    marker_action.click_and_hold(marker_pin)
    marker_action.move_by_offset(10, 200)
    marker_action.release()
    marker_action.perform()
    # Submit form
    submit_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[type="submit"]')))
    scroll_element_to_view(submit_button)
    submit_button.click()

    # Check if announcement was created
    latest_element = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#announcements-table .rdt_TableBody > div:nth-child(1)')))
    announcement_id = latest_element.get_attribute('id').split('-')[1]
    announcement_title = driver.find_element(By.ID, f'cell-3-{announcement_id}').text
    announcement_category = driver.find_element(By.ID, f'cell-4-{announcement_id}').text
    announcement_surface = driver.find_element(By.ID, f'cell-5-{announcement_id}').text.split(' ')[0]
    announcement_price = driver.find_element(By.ID, f'cell-6-{announcement_id}').text.split(' ')[0]
    announcement_location = driver.find_element(By.ID, f'cell-7-{announcement_id}').text
    announcement_date = datetime.strptime(driver.find_element(By.ID, f'cell-8-{announcement_id}').text, '%a %b %d %Y')

    # Check if information is correct
    assert announcement_title == title
    assert announcement_category == category
    assert announcement_surface == surface
    assert announcement_price == price
    assert announcement_location == location
    assert datetime.now().date() == announcement_date.date()