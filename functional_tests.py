from selenium import webdriver

driverLocation = '../webdriver/chromedriver'
# browser = webdriver.Chrome()
browser = webdriver.Chrome(driverLocation)
browser.get('http://localhost:8000')

assert 'Django' in browser.title