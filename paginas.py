from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

from bs4 import BeautifulSoup
import requests
from requests.models import HTTPError

#from TESTE_SCRAPER import Teste_Scraper
i=0
options = webdriver.ChromeOptions()
options.add_argument("--headless")
#driver = webdriver.Chrome(r"chromedriver.exe")
driver = webdriver.Chrome(chrome_options=options)
# implicit wait for 5 seconds
driver.implicitly_wait(5)
# maximize with maximize_window()
# driver.maximize_window()
driver.get('http://www.camarasorocaba.sp.gov.br/materias.html')
for i in range(2,5):
    pagina = "<a href=\"javascript: postPesquisaMateria('1')\">1</a>"
    proxima_pagina = f"<a href=\"javascript:postPesquisaMateria('{i}')\">{i}</a>"
    # identify element with title attribute and click()
    l = driver.find_element(By.XPATH, f"/html/body/div[2]/div[3]/section[2]/div/div/div/div/div[7]/ul/li[{i}]/a")
    l.click()
    #Teste_Scraper.materias(
    print("****************** Pagina %d ******************" %i)
    titulo_da_materia             = driver.find_elements(By.CLASS_NAME,"materiaLegislativaTitle")
    dados_de_apresentacao_materia = driver.find_elements(By.CLASS_NAME, "time")
    texto_da_materia              = driver.find_elements(By.CLASS_NAME, "headline")
    h=0
    for h in range(len(titulo_da_materia)):
        print('Id: '+str(h)+' - '+titulo_da_materia[h].text)
       
    
    n=0
    for n in range(len(texto_da_materia)):
        print('Id: '+str(n)+' - '+texto_da_materia[n].text)

    '''
    j=0
    for j in range(len(dados_de_apresentacao_materia)):
        print(dados_de_apresentacao_materia[j].text
    '''
    
    
driver.quit()