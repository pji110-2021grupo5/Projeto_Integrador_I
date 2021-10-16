from selenium import webdriver 
from selenium.webdriver.support.ui import Select 


driver = webdriver.Chrome() 
driver.get("http://demo.automationtesting.in/Windows.html") 
driver.find_element_by_xpath('//*[@id="Tabbed"]/a/button').click() 
handles = driver.window_handles 
for i in handles: 
    driver.switch_to.window(i) 
  
    
    print(driver.title) 