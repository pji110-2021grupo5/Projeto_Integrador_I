# -*- coding: utf-8 -*-
__author__ = "pji110-2021grupo5"
__copyright__ = "pji110-2021grupo5"
__credits__ = ["https://github.com/pji110-2021grupo5/pji110-2021grupo5"]
__license__ = "GNU General Public License v1.0"
__version__ = "1.0"
__maintainer__ = "pji110-2021grupo5"
__email__ = "pji110-2021grupo5@gmail.com"
__status__ = "Production"

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from time import sleep
import sqlite3

#import mysql.connector
#from mysql.connector import Error

class materias:
    def __init__(self):
        options = webdriver.ChromeOptions()
        options.add_argument("--headless")

        self.driver       = webdriver.Chrome(chrome_options=options) #webdriver.Chrome()
        self.driver.implicitly_wait(5)
        self.titulo       = []
        self.texto_materia= []
        self.data_materia = []
        self.tipo_materia = []
        self.autor        = []
        self.situacao     = []

    def Iniciar(self):
        self.proxima_pagina = 1
        self.acessar_site()

    def acessar_site(self):
        self.driver.get('http://www.camarasorocaba.sp.gov.br/materias.html')
        # Faz o script parar por 5 segundos
        sleep(5)
        self.captura_informacoes()

    def captura_informacoes(self):
        # Tag xpath para Titulo materia: /html/body/div[2]/div[3]/section[2]/div/div/div/div/div[1]/a/div/h3
        # Tag class para dados da apresentação da matéria: By.CLASS_NAME, "time"

        for i in range(2,12):
            titulo_da_materia             = self.driver.find_elements(By.CLASS_NAME,"materiaLegislativaTitle")
            dados_de_apresentacao_materia = self.driver.find_elements(By.CLASS_NAME, "time")
            texto_da_materia              = self.driver.find_elements(By.CLASS_NAME, "headline")
            self.gravar_informacoes(titulo_da_materia, texto_da_materia, dados_de_apresentacao_materia)
            #l = self.driver.find_element(By.XPATH, f"/html/body/div[2]/div[3]/section[2]/div/div/div/div/div[7]/ul/li[{i}]/a")
            #l.click()
            self.navegar_proximo_link(self.driver,i)
            #print('************************ Página %d ************************'%i-1)
            print('************************ Página %r ************************'%i)#str(int(i)-1))
        
    def gravar_informacoes(self, titulo_da_materia, texto_da_materia, dados_de_apresentacao_materia):
        
        self.titulo=[]
        self.texto_materia=[]

        global cur
        global conn
        try:
            conn = sqlite3.connect('new/univesp.db')
            cur = conn.cursor()
        except sqlite3.Error as erro:
            print('Captura_Materias: Falha na conexão com o banco de dados: {}'.format(erro))
            exit()


        for i in range(0, len(titulo_da_materia)):
            self.title = titulo_da_materia[i].text.split(" ")  # Separa texto em lista
            self.title = self.title[1]  # Seleciona somente uma informaçao da lista
            self.titulo.append(self.title)

            self.txt_materia = texto_da_materia[i].text
            self.texto_materia.append(self.txt_materia)
            
            itens = 0
            
            self.data_materia=[]
            self.tipo_materia=[]
            self.autor       =[]
            self.situacao    =[]
            
            while itens < len(dados_de_apresentacao_materia):
                self.data_materia.append(dados_de_apresentacao_materia[itens].text)
                itens += 1
                self.tipo_materia.append(dados_de_apresentacao_materia[itens].text)
                itens += 1
                self.author = dados_de_apresentacao_materia[itens].text.split(": ")
                self.author = self.author[1]
                self.autor.append(self.author)
                itens += 1
                self.condition = dados_de_apresentacao_materia[itens].text.split(": ")
                self.condition = self.condition[1]
                self.situacao.append(self.condition)
                itens += 1
            try:
                materias_vereadores = "insert or ignore into materias_vereadores(\
                                       IdVereador,TituloMateria,TextoMateria,DataMateria,\
                                       TipoMateria,AutorMateria,SituacaoMateria)\
                values((select IdVereador from nome_vereadores where NomeVereador||' '||SobreNome = '"+self.autor[i]+"'),'"\
                        +self.titulo[i]+"','"+self.texto_materia[i]+"','"+self.data_materia[i]+"','"+self.tipo_materia[i]+"','"\
                        +self.autor[i]+"','"+self.situacao[i]+"')"

                cur.execute(materias_vereadores)
                conn.commit()

            except sqlite3.Error as erro: #except Error as erro:
                print('Algo deu errado, erro reportado: {}'.format(erro))


        '''
        print("Titulo: "          , self.titulo      )
        print("Texto da Matéria: ", self.texto_materia )
        print("Data: "            , self.data_materia)
        print("Tipo: "            , self.tipo_materia)
        print("Autor: "           , self.autor       )
        print("Situaçao: "        , self.situacao    )
        '''
        self.titulo       = []
        self.texto_materia= []
        self.data_materia = []
        self.tipo_materia = []
        self.autor        = []
        self.situacao     = []

    def navegar_proximo_link(self,driver,i):
        l = driver.find_element(By.XPATH, f"/html/body/div[2]/div[3]/section[2]/div/div/div/div/div[7]/ul/li[{i}]/a")
        l.click()
        sleep(3)
    
'''
    def Conect(self,materias_vereadores):
        global cursor
        global con
        try:
            #Faz a conexão com o banco de dados do MySql
            con = mysql.connector.connect(host='localhost',database='univesp',user='univesp',password='univesp')
            #Cria cursor e executa SQL no banco
            cursor = con.cursor()

            cursor.execute(materias_vereadores)
            con.commit()

        except Error as erro:
            print('Falha na conexão com o banco de dados: {}'.format(erro))


    def Fecha_Con():
        if (con.is_connected()):
            con.close()
            con.cursor.close()
            print('Conexão MySQL finalizada...')

'''