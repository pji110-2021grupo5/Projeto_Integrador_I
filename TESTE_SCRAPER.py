#from logging import error
from re import sub,compile
from bs4 import BeautifulSoup
import requests
import re

#import scrapy
#import urllib
#import json

import mysql.connector
from mysql.connector import Error
from requests.models import HTTPError

#import paginas 

#*********** Abre a conexão com o Banco de Dados ***********
class Teste_Scraper:
    def Conexao():
        global cursor
        global con
        try:
            con = mysql.connector.connect(host='localhost',database='univesp',user='univesp',password='univesp')
            #Cria tabela no Banco MySql
            #nome_vereadores = "CREATE TABLE nome_vereadores(IdVereador int(12) not null,NomeVereador VARCHAR(50) not null,nome_vereador VARCHAR(80),PRIMARY KEY (IdVereador))"
            #part_vereadores = "CREATE TABLE part_vereadores(IdVereador int(12) not null,PartidoVereador VARCHAR(40) not null,GabineteVereador VARCHAR(30),PRIMARY KEY (IdVereador))"
            
            tables = "SHOW TABLES FROM UNIVESP"
            #Cria cursor e executa SQL no banco
            cursor = con.cursor()
            cursor.execute(tables)

            tabelas = cursor.fetchall()

            result = [item[0] for item in tabelas]

            if 'contato_vereadores' not in result:
                contato_vereadores = "CREATE TABLE contato_vereadores(IdVereador int(12) not null,\
                                                                      Telefone_gab VARCHAR(30),\
                                                                      E_mail VARCHAR(50),\
                                                                      Facebook VARCHAR(50),\
                                                                      Instagram VARCHAR(50),\
                                                                      Site VARCHAR(130),\
                                                                      Whats VARCHAR(30),\
                                                                      PRIMARY KEY (IdVereador))"
                cursor.execute(contato_vereadores)
            elif 'nome_vereadores' not in result:
                  nome_vereadores = "CREATE TABLE nome_vereadores(IdVereador int(12) not null,\
                                                                  NomeVereador VARCHAR(50) not null,\
                                                                  nome_vereador VARCHAR(80),\
                                                                  PRIMARY KEY (IdVereador))"
                  cursor.execute(nome_vereadores)
            elif 'part_vereadores' not in result:
                part_vereadores = "CREATE TABLE part_vereadores(IdVereador int(12) not null,\
                                                                PartidoVereador VARCHAR(40) not null,\
                                                                GabineteVereador VARCHAR(30),\
                                                                PRIMARY KEY (IdVereador))"
                cursor.execute(part_vereadores)
            elif 'materias_vereadores' not in result:
                materias_vereadores = "CREATE TABLE materias_vereadores(IdMateria int not null AUTO_INCREMENT,\
                                                                        TituloMateria VARCHAR(20) not null,\
                                                                        TextoMateria VARCHAR(200), \
                                                                        DataMateria VARCHAR(10),\
                                                                        TipoMateria VARCHAR(20),\
                                                                        AutorMateria VARCHAR(50),\
                                                                        SituacaoMateria VARCHAR(30),\
                                                                        PRIMARY KEY (IdMateria))"
                cursor.execute(materias_vereadores)    
            else:
                print('o Banco de dados já possui as tabelas:'+str(result)+' criadas')

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
        part = gab = tel = email = face = insta = site = whats = ""

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
                insere_contato = "insert into univesp.contato_vereadores (IdVereador,Telefone_gab,"\
                          "E_mail,Facebook,Instagram,Site,Whats)"\
                          "values ("+str(i+1)+",'"+tel+"','"+email+"','"+face+"','"+insta+"','"+site+"','"+whats+"')"
                
                cursor.execute(insere_contato)
                con.commit()

            except Error as erro:
                print('Registros já existem no Banco de Dados: {}'.format(erro))

            
    def materias():

        i = 1
        j = 1
        nome_vereador = ""
        
        try:
            html = requests.get('http://www.camarasorocaba.sp.gov.br/materias.html').content
        except HTTPError as e:
            print("conexão fora do ar, reportado o seguinte errro: "+e)
        else:    
            html.decode('utf-8')
            soup = BeautifulSoup(html, 'html.parser')
            info_materias = soup.find_all(class_="sec-info")
            info_texto = soup.find_all(class_="headline")
            
            #print(materias+'\n'+info_texto[j].text)

            for j in range(len(info_materias)):
                materias = info_materias[j].text.replace("\n","")
                m = materias.split()
                nome_vereador = ''
                
                #for k in range(len(m)):
                print(m[0]+' - '+m[1])                              # TituloMateria
                print(m[2])                                         # DataMateria
                print(m[3])                                         # TipoMateria
                #-----------------------------------------------------------------------------    
                for l in range(5,len(m)):
                    if m[l] != 'Situação:':
                        nome_vereador = nome_vereador+' '+m[l]
                    else:
                        break
                print(nome_vereador.strip())                                # AutorMateria
                #-----------------------------------------------------------------------------    
                q = 0
                #for p in range(l,len(m)):
                p = l
                resto = m[p]
                for s in range(p, len(m)-1):
                    q = q+1
                    resto = resto + ' ' + m[p+q]
                print(resto)                                                # TextoMateria
                #-----------------------------------------------------------------------------    
                #    Inserir os dados ( values ) na tabela materias_vereadores
                #-----------------------------------------------------------------------------    
                materias_vereadores = "insert into materias_vereadores(TituloMateria,TextoMateria,DataMateria,\
                                                                        TipoMateria,AutorMateria,SituacaoMateria)\
                                       values('"+m[0]+' - '+m[1]+"')"
                #-----------------------------------------------------------------------------    

            

    #Chama a função para conectar com o Banco de Dados "sakila"
    Conexao()

    #Chama a função que faz o Scraper do site ( nomes partidos e contatos dos vereadores )
    Nomes()

    #Chama a função que faz o Scraper das matérias ( matérias legislativas )
    materias()

    Fecha_Con()

