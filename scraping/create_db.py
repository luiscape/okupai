import sqlite3

def create_deputados_tables(db_name):
    conn = sqlite3.connect(db_name)
    cur = conn.cursor()
    cur.execute('''CREATE TABLE deputado
    (id_deputado INTEGER PRIMARY KEY AUTOINCREMENT, idecadastro TEXT, idparlamentar TEXT, nome TEXT, nomeparlamenter TEXT, sexo TEXT, uf TEXT, id_partido INTEGER, gabinete TEXT, anexo TEXT, fone TEXT, email TEXT)''')
    cur.execute('''CREATE TABLE comissao
                         (id_comissao INTEGER PRIMARY KEY AUTOINCREMENT, nome TEXT, sigla TEXT)''')
    cur.execute('''CREATE TABLE comissao_deputado
                         (id_comissao INTEGER,id_deputado INTEGER,tipo TEXT)''')
    cur.execute('''CREATE TABLE partido
                         (id_partido INTEGER PRIMARY KEY AUTOINCREMENT, nome TEXT, sigla TEXT)''')
    cur.execute('''CREATE TABLE bancada
                         (id_partido INTEGER,id_deputado INTEGER,tipo TEXT)''')
    conn.commit()

def create_proposicoes_tables(db_name):
    conn = sqlite3.connect(db_name)
    cur = conn.cursor()
 
    cur.execute('''CREATE TABLE siglas_tipo_proposicao
                         (id_siglas_tipo_proposicao INTEGER PRIMARY KEY AUTOINCREMENT, tiposigla TEXT, descricao TEXT, ativa TEXT,genero TEXT, id_tipo TEXT)''')
    
    cur.execute('''CREATE TABLE situacao_proposicao
                         (id_situacao_proposicao INTEGER PRIMARY KEY AUTOINCREMENT, id TEXT, descricao TEXT, ativa TEXT)''')
    
    cur.execute('''CREATE TABLE tipos_autores
                         (id_tipos_autores INTEGER PRIMARY KEY AUTOINCREMENT, id TEXT,descricao TEXT)''')

    cur.execute('''CREATE TABLE proposicoes
                         (id_proposicao INTEGER PRIMARY KEY AUTOINCREMENT, id TEXT, tipo TEXT, numero TEXT, ano TEXT, id_orgao_numerador INTEGER, ementa TEXT, explicao_ementa TEXT, id_regime TEXT, regime TEXT, id_apreciacao TEXT, apreciacao TEXT, autor_nome TEXT, autor_partido TEXT, autor_uf TEXT, despacho TEXT, despacho_data TEXT,id_situacao TEXT, orgao_situacao TEXT, situacao_proposicao TEXT, link_interior_teor TEXT)''')  

    cur.execute('''CREATE TABLE indices
                         (id_indice INTEGER PRIMARY KEY AUTOINCREMENT, indice TEXT)''')
    
    cur.execute('''CREATE TABLE indexacao
                         (id_proposicao INTEGER, id_indice INTEGER)''')
 
    conn.commit()

def create_votacoes_table(db_name):
    conn=sqlite3.connect(db_name)
    cur=conn.cursor()
     
    cur.execute('''CREATE TABLE votacao
                         (id_votacao INTEGER PRIMARY KEY AUTOINCREMENT, id_proposicao INTEGER, resumo TEXT, data TEXT, hora TEXT, obj_votacao TEXT)''')

 
    cur.execute('''CREATE TABLE voto
                         (id_voto INTEGER PRIMARY KEY AUTOINCREMENT, id_votacao INTEGER,  nome_deputado TEXT,partido_deputado TEXT, uf_deputado TEXT, voto TEXT)''')

    conn.commit()
    
def create_orgaos_tables(db_name):
    conn = sqlite3.connect(db_name)
    cur = conn.cursor()
    cur.execute('''CREATE TABLE orgaos
                         (id_orgaos INTEGER PRIMARY KEY AUTOINCREMENT, id TEXT, sigla TEXT, descricao TEXT)''')
  
    conn.commit()



def main():

    
    db_name = 'database/transparencia.db' 
#    print create_proposicoes_tables(db_name)
#    print create_deputados_tables(db_name)
#    print create_orgaos_tables(db_name)
    print create_votacoes_table(db_name)
    
if __name__ == '__main__':
    main()
