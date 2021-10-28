from logging import error
from re import sub,compile
from bs4 import BeautifulSoup
import requests
import re
import mysql.connector
from mysql.connector import Error
from requests.models import HTTPError
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

#*********** Abre a conexão com o Banco de Dados ***********

def Conexao():
    global cursor
    global con
    try:
        #con = mysql.connector.connect(host='localhost',database='univesp',user='univesp',password='univesp')
        con = mysql.connector.connect(host='localhost',database='univesp',user='root',password='univesp')
        #Cria tabela no Banco MySql
        nome_vereadores = "CREATE TABLE nome_vereadores(IdVereador int(12) not null,NomeVereador VARCHAR(50) not null,SobreNome VARCHAR(80),PRIMARY KEY (IdVereador))"
        part_vereadores = "CREATE TABLE part_vereadores(IdVereador int(12) not null,PartidoVereador VARCHAR(40) not null,GabineteVereador VARCHAR(30),PRIMARY KEY (IdVereador))"
        
        contato_vereadores = "CREATE TABLE contato_vereadores(IdVereador int(12) not null,"\
                             "Telefone_gab VARCHAR(30),E_mail VARCHAR(50),Facebook VARCHAR(50),"\
                             "Instagram VARCHAR(50),Site VARCHAR(130),Whats VARCHAR(30),"\
                             "PRIMARY KEY (IdVereador))"
        
        
        tables = ['nome_vereadores','part_vereadores','contato_vereadores']
        
        Qry = "SHOW TABLES"
        cursor = con.cursor()
        cursor.execute(Qry)
        #results = cursor.fetchall()
        
        #print('All existing tables:', results) # Returned as a list of tuples
        
        #results_list = [item[0] for item in results] # Conversion to list of str
        results_list = [i[0] for i in cursor.fetchall()]
        
        if tables in results_list:
            print(tables, 'was found!')
        else:
            print(tables, 'was NOT found!')

        #Cria cursor e executa SQL no banco
        #cursor = con.cursor()
        #cursor.execute(nome_vereadores,part_vereadores,contato_vereadores)
        #cursor.execute(contato_vereadores)
        
    except Error as erro:
        print('Falha na conexão com o banco de dados: {}'.format(erro))

#*********** Fecha a conexão com o banco de dados ***********

def Fecha_Con():
    if (con.is_connected()):
        con.close()
        cursor.close()
        print('Conexão MySQL finalizada...')


#*********** Scraper da página e gravação no banco de dados ***********

def Nomes():
    i = 1
    #html = requests.get(input('Entre com a URL: ')).content
    html = requests.get('http://www.camarasorocaba.sp.gov.br/vereadores.html').content
    html.decode('utf-8')
    soup = BeautifulSoup(html, 'html.parser')
    vereadores = soup.find_all(class_="sec-info")
    part = gab = tel = email = face = insta = site = whats = " "
    
    for i in range(0,len(vereadores)):
        data = vereadores[i].text.replace("\n","").split()
        site = ""
        for j in range(0,len(data)):
            if data[j] == "Partido:":
                part = data[j+1]
            if data[j] == "Gabinete":
                gab = data[j+1]
            if data[j] == "Gabinete:":
                tel = data[j+1]+" "+data[j+2]
            if data[j] == "E-mail:":
                email = data[j+1]
            if data[j] == "Facebook:":
                face = data[j+1]
            if data[j] == "Instagram:":
                insta = data[j+1]
            if "site:" in data[j].lower():# and (data[i].lower() in data[j+1].lower()):
                site += data[j+1]+' - '
            if "whats" in data[j].lower():
                whats = data[j+1]+" "+data[j+2]
            
        try:
            insere3 = "insert into univesp.contato_vereadores (IdVereador,Telefone_gab,"\
                      "E_mail,Facebook,Instagram,Site,Whats)"\
                      "values ("+str(i+1)+",'"+tel+"','"+email+"','"+face+"','"+insta+"','"+site+"','"+whats+"')"
            #insere2 = "insert into univesp.part_vereadores (IdVereador,PartidoVereador,GabineteVereador) values ("+str(i+1)+",'"+part+"','"+gab+"')"
            #"insert into univesp.part_vereadores (IdVereador,PartidoVereador,GabineteVereador) values ("+str(i+1)+"','"+part+"','"+gab+"')'"

            #"insert into univesp.part_vereadores (IdVereador,PartidoVereador,GabineteVereador) values ("+str(i+1)+",'"+all_part[i].split("\r\n",1)[0]+"','"+all_part[j].split("\r\n",1)[0]+"')"
            #cursor.execute(insere1,insere2)
            cursor.execute(insere3)
            con.commit()
            
        except Error as erro:
            print('Registros já existem no Banco de Dados: {}'.format(erro))

       
def materias():

    i = 1
    j = 1
    #html = requests.get(input('Entre com a URL: ')).content
    try:
        html = requests.get('http://www.camarasorocaba.sp.gov.br/materias.html').content
    except HTTPError as e:
        print("conexão fora do ar, reportado o seguinte errro: "+e)
    else:    
        html.decode('utf-8')
        soup = BeautifulSoup(html, 'html.parser')
        info_materias = soup.find_all(class_="sec-info")
        info_texto = soup.find_all(class_="headline")
        #paginas = [a['href'] for a in soup.find_all('a', href=True)] 
        paginas = [a['href'] for a in soup.select('a[href]')] #Lista todas as páginas
        pag = re.findall(r'\d+', paginas[142])[0] # Encontra qual é o número da última página para fazer o for externo

        for i in range(int(pag)):
            for j in range(len(info_materias)):
                materias = info_materias[j].text.replace("\n","")
                print(materias+'\n'+info_texto[j].text)


def paginas():

    options = Options()
    options.add_argument("--headless")
    driver = webdriver.Chrome(r"/home/milenna/Área de Trabalho/Estudos do Papai/Projeto Integrador I/chromedriver",options=options)
    # implicit wait for 5 seconds
    driver.implicitly_wait(5)
    # maximize with maximize_window()
    # driver.maximize_window()

    driver.get('http://www.camarasorocaba.sp.gov.br/materias.html')
    html = requests.get('http://www.camarasorocaba.sp.gov.br/materias.html').content
    for i in range(1, 3):
        pagina = "<a href=\"javascript: postPesquisaMateria('1')\">1</a>"
        proxima_pagina = f"<a href=\"javascript:postPesquisaMateria('{i}')\">{i}</a>"
        # identify element with title attribute and click()
        l = driver.find_element(By.XPATH, f"/html/body/div[2]/div[3]/section[2]/div/div/div/div/div[7]/ul/li[{i}]/a")
        l.click()
        print("Pagina %d " % i)

        html.decode('utf-8')
        soup = BeautifulSoup(html, 'html.parser')
        info_materias = soup.find_all(class_="sec-info")
        info_texto = soup.find_all(class_="headline")
        #paginas = [a['href'] for a in soup.find_all('a', href=True)] 
        paginas = [a['href'] for a in soup.select('a[href]')] #Lista todas as páginas
        #pag = re.findall(r'\d+', paginas[142])[0] # Encontra qual é o número da última página para fazer o for externo

        #for i in range(int(pag)):
        for j in range(len(info_materias)):
            materias = info_materias[j].text.replace("\n","")
            print(materias+'\n'+info_texto[j].text)

    driver.quit()            

#Chama a função para conectar com o Banco de Dados "sakila"
Conexao()

#Chama a função que faz o Scraper do site ( nomes partidos e contatos dos vereadores )
#Nomes()

#Chama a função que faz o Scraper das matérias ( matérias legislativas )
#materias()

#paginas()

#Fecha_Con()

