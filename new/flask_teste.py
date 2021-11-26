from datetime import datetime
from flask import Flask
from markupsafe import escape
from flask import render_template
from flask import request
#import os
#from sqlalchemy import SQLAlchemy
import sqlite3
from pathlib import Path

from werkzeug.datastructures import T


app = Flask(__name__)

if __name__ == "__main__":
    app.run(debug=False)

#port = int(os.getenv('PORT'),'5000')
#app.run(host='0.0.0.0',port=port)

#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////univesp.db'
#db = SQLAlchemy(app)

global materia

def get_db_connection():
    conn = sqlite3.connect('univesp.db')
    conn.row_factory = sqlite3.Row
    return conn
    
@app.route("/teste.html",methods=['GET','POST'])
def vereadores():
    #self.nome = self.listarnomes()
    conn = get_db_connection()
    posts = conn.execute('SELECT * FROM nome_vereadores n\
                        inner join part_vereadores p on n.IdVereador = p.IdVereador\
                        inner join contato_vereadores c on n.IdVereador = c.IdVereador').fetchall()
    conn.close()
    return render_template('teste.html',vereador=posts)

@app.route("/materias.html",methods=['GET','POST'])
def materias():
    #self.nome = self.listarnomes()
    conn = get_db_connection()
    posts = conn.execute('select * from materias_vereadores m\
                          inner join nome_vereadores n \
                          on m.IdVereador = n.IdVereador').fetchall()

    diretorio = Path('.')
    arquivo = diretorio/'univesp.db'
    dt_object = datetime.fromtimestamp(arquivo.stat().st_mtime) 

    materia =  'Matérias Legislativas atualizadas em: '+datetime.strftime(dt_object,'%d/%m/%Y as %H:%M')   
    conn.close()
    return render_template('materias.html',materias=posts,mat=materia)

    
