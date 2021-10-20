from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options


options = Options()
options.add_argument("--headless")
driver = webdriver.Chrome(r"/home/milenna/Área de Trabalho/Estudos do Papai/Projeto Integrador I/chromedriver",options=options)
# implicit wait for 5 seconds
driver.implicitly_wait(5)
# maximize with maximize_window()
# driver.maximize_window()

driver.get('http://www.camarasorocaba.sp.gov.br/materias.html')
for i in range(1, 5):
    pagina = "<a href=\"javascript: postPesquisaMateria('1')\">1</a>"
    proxima_pagina = f"<a href=\"javascript:postPesquisaMateria('{i}')\">{i}</a>"
    # identify element with title attribute and click()
    l = driver.find_element(By.XPATH, f"/html/body/div[2]/div[3]/section[2]/div/div/div/div/div[7]/ul/li[{i}]/a")
    l.click()
    print("Pagina %d " % i)
driver.quit()