from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

from bs4 import BeautifulSoup
import requests
from requests.models import HTTPError

#from TESTE_SCRAPER import Teste_Scraper
i=0
titulo = []
data_materia = []
tipo_materia = []
autor = []
situacao = []

options = webdriver.ChromeOptions()
options.add_argument("--headless")
#driver = webdriver.Chrome(r"chromedriver.exe")
driver = webdriver.Chrome(chrome_options=options)
# implicit wait for 5 seconds
driver.implicitly_wait(5)
# maximize with maximize_window()
# driver.maximize_window()
driver.get('http://www.camarasorocaba.sp.gov.br/materias.html')

for i in range(2,4):
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

    itens = 0

    Idv=Idx=Idy=Idz=0

#*********************************************************************
    while itens < len(dados_de_apresentacao_materia):
#*********************************************************************
        data_materia.append(dados_de_apresentacao_materia[itens].text)
        itens += 1
#*********************************************************************
        tipo_materia.append(dados_de_apresentacao_materia[itens].text)
        itens += 1
#*********************************************************************
        author = dados_de_apresentacao_materia[itens].text.split(": ")
        author = author[1]
        autor.append(author)
        itens += 1
#*********************************************************************
        condition = dados_de_apresentacao_materia[itens].text.split(": ")
        condition = condition[1]
        situacao.append(condition)
        itens += 1
#*********************************************************************
    #print("titulo: ", titulo)
    
    #Idv=Idx=Idy=Idz=0
#*********************************************************************
    v=0
    for v in range(len(data_materia)):
        print("Id: "+str(Idv)+' - '+"data: ", data_materia[v])
        Idv = Idv + 1
        if Idv > 5:
            Idv = 0    

#*********************************************************************
    x=0
    for x in range(len(tipo_materia)):
        print("Id: "+str(Idx)+' - '+"Tipo: ", tipo_materia[x])
        Idx = Idx + 1
        #if Idx > 5:
        #    Idx = 0
#*********************************************************************
    y=0
    for y in range(len(autor)):
        print("Id: "+str(Idy)+' - '+"autor: ", autor[y])
        Idy = Idy + 1
        #if Idy > 5:
        #    Idy = 0
#*********************************************************************
    z=0
    for z in range(len(situacao)):
        print("Id: "+str(Idz)+' - '+"situaçao: ", situacao[z])
        Idz = Idz + 1
        #if Idz > 5:
        #    Idz = 0
#*********************************************************************

driver.quit()