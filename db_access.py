import sqlite3 as lite
import aux

class TransparenciaDB:
    def __init__(self,db_name):
        self.conn = lite.connect(db_name)
        self.cur = self.conn.cursor()

    def close(self):
        self.conn.close()

#################### Partidos #################################
    def __get_partido_db_ID(self,sigla):
        self.cur.execute("SELECT id_partido FROM partido WHERE sigla=?",(sigla,))
        id_partido=self.cur.fetchone()
        if id_partido:
            return id_partido[0]
        else:
            return -1
        
    def insert_partido(self,sigla,nome):
        data=(nome,sigla)
        is_inserted = self.__get_partido_db_ID(sigla)
        if is_inserted<0:
            data=(None,nome,sigla)
            data=tuple([aux.prepare_string_to_db(d) for d in data])
            self.cur.execute("INSERT INTO partido VALUES (?,?,?)",data)
            self.conn.commit()
            print "Partido "+sigla+" inserted"
        else:
            print "Partido "+sigla+" already is on the database"
        
    def get_list_partidos(self):
        partidos_list = self.cur.execute("SELECT * FROM partido")
        return partidos_list.fetchall()

#################Comissao ########################
    def __get_comissao_db_ID(self,sigla):
        self.cur.execute("SELECT id_comissao FROM comissao WHERE sigla=?",(sigla,))
        id_comissao=self.cur.fetchone()
        if id_comissao:
            return id_comissao[0]
        else:
            return -1
        
    def insert_comissao(self,sigla,nome):
        data=(nome,sigla)
        is_inserted = self.__get_comissao_db_ID(sigla)
        data =(None,nome,sigla)
        data=tuple([aux.prepare_string_to_db(d) for d in data])
        if is_inserted<0:
            self.cur.execute("INSERT INTO comissao VALUES (?,?,?)",data)
            self.conn.commit()
            print "Comissao "+sigla+" inserted"
        else:
            print "Comissao "+sigla+" already is on the database"
        
    def get_list_comissoes(self):
        partidos_list = self.cur.execute("SELECT * FROM comissao")
        return partidos_list.fetchall()


##################   Deputado ##############################

    def __get_deputado_db_ID(self,nome,partido,uf):
        id_partido=self.__get_partido_db_ID(partido)
        if id_partido < 0:
            return -2
        
        self.cur.execute("SELECT id_deputado FROM deputado WHERE nome=? and id_partido=? and uf=?",(nome,id_partido,uf))
        dep=self.cur.fetchone()
        if dep:
            return dep[0]
        else:
            return -1
         
    def insert_deputado(self,idecadastro,idparlamentar,nome,nomeparlamentar,sexo,uf,sigla,gabinete,anexo,fone,email):
        id_partido=self.__get_partido_db_ID(sigla)
        id_deputado=self.__get_deputado_db_ID(nome,sigla,uf)
        if (id_partido>0 and id_deputado<0):
            data=(None,idecadastro,idparlamentar,nome,nomeparlamentar,sexo,uf,id_partido,gabinete,anexo,fone,email)
            data=tuple([aux.prepare_string_to_db(d) for d in data])
            self.cur.execute("INSERT INTO deputado VALUES (?,?,?,?,?,?,?,?,?,?,?,?)",data)
            self.conn.commit()
            print "Deputado "+nome+" inserted"
        else:
            if id_partido<0:
                print "Partido "+sigla+" does not exist in the database"
            if id_deputado>0:
                print "Deputado "+nome+" already in the database"
            
        
    def get_list_deputados(self):
        deputados_list = self.cur.execute("SELECT * FROM deputado")
        return deputados_list.fetchall()

#################### deputado comissoes #########

    def __get_comissao_deputado_db_ID(self,id_comissao,id_deputado,nome,sigla,tipo):
        self.cur.execute("SELECT * FROM comissao_deputado WHERE id_comissao=? and id_deputado=?",(id_comissao,id_deputado,))
        dep=self.cur.fetchone()
        if dep:
            return dep[0]
        else:
            return -1
         
    def insert_comissao_deputado(self,nome_dep,sigla_dep,uf_dep,nome,sigla,tipo):
        id_comissao=self.__get_comissao_db_ID(sigla)
        if id_comissao<0:
            self.insert_comissao(sigla,nome)
        id_comissao=self.__get_comissao_db_ID(sigla)
        id_deputado=self.__get_deputado_db_ID(nome_dep,sigla_dep,uf_dep)
        if (id_comissao>0 and id_deputado>0):
            data=(id_comissao,id_deputado,tipo)
            data=tuple([aux.prepare_string_to_db(d) for d in data])
            self.cur.execute("INSERT INTO comissao_deputado VALUES (?,?,?)",data)
            self.conn.commit()
            print "Comissao_Deputado "+nome+" inserted"
        else:
            if id_comissao<0:
                print "Comissao "+sigla_comissao+" does not exist in the database"
            if id_deputado<0:
                print "Deputado "+nome_dep+" does not exist in the database"
            
        
    def get_list_comissao_deputados(self):
        comisssao_deputados_list = self.cur.execute("SELECT * FROM comissao_deputado")
        return comisssao_deputados_list.fetchall()

#################### bancada comissoes #########

    def __get_bancada_db_ID(self,id_partido,id_deputado,tipo):
        self.cur.execute("SELECT * FROM bancada WHERE id_partido=? and id_deputado=?",(id_partido,id_deputado,))
        banc=self.cur.fetchone()
        if banc:
            return banc[0]
        else:
            return -1
         
    def insert_bancada(self,nome_dep,sigla_dep,uf_dep,partido,tipo):
        id_partido=self.__get_partido_db_ID(partido)
        id_deputado=self.__get_deputado_db_ID(nome_dep,sigla_dep,uf_dep)
        if (id_partido>0 and id_deputado>0):
            data=(id_partido,id_deputado,tipo)
            data=tuple([aux.prepare_string_to_db(d) for d in data])
            self.cur.execute("INSERT INTO bancada VALUES (?,?,?)",data)
            self.conn.commit()
            print "bancada  inserted"
        else:
            if id_partido<0:
                print "Partido "+partido+" does not exist in the database"
            if id_deputado<0:
                print "Deputado "+nome_dep+" does not exist in the database"
            
        
    def get_list_bancada(self):
        bancada_list = self.cur.execute("SELECT * FROM bancada")
        return bancada_list.fetchall()


   

####################  Siglas Tipo Proposicoes #########

    def __get_siglas_tipo_proposicao_db_ID(self,sigla):
        self.cur.execute("SELECT * FROM siglas_tipo_proposicao WHERE tiposigla=? ",(sigla,))
        banc=self.cur.fetchone()
        if banc:
            return banc[0]
        else:
            return -1
        
    def change_id_tipo(self,id_tipo,sigla):
        self.cur.execute("SELECT * FROM siglas_tipo_proposicao WHERE tiposigla=? ",(sigla,))
        banc=self.cur.fetchone()
        if banc:
            self.cur.execute("UPDATE siglas_tipo_proposicao SET id_tipo=? WHERE tiposigla=?",(id_tipo,sigla))
            return banc[0]
        else:
            return -1

        
    def insert_siglas_tipo_proposicao(self,tiposigla,descricao,ativa,genero,id_tipo):
       
        id_siglas=self.__get_siglas_tipo_proposicao_db_ID(tiposigla)
        if ( id_siglas<0):
            data=(None,tiposigla,descricao,ativa,genero,id_tipo)
            data=tuple([aux.prepare_string_to_db(d) for d in data])
            self.cur.execute("INSERT INTO siglas_tipo_proposicao VALUES (?,?,?,?,?,?)",data)
            self.conn.commit()
            print "tipo_sigla_proposicao  inserted"
        else:
            print "tipo_sigla_proposicao "+tiposigla+" already inserted"
                 
    def get_siglas_tipo_proposicao(self):
        siglas_tipo_list = self.cur.execute("SELECT * FROM siglas_tipo_proposicao")
        return siglas_tipo_list.fetchall()

###################  Situacao Proposicao #########

    def __get_situacao_proposicao_db_ID(self,id):
        self.cur.execute("SELECT * FROM situacao_proposicao WHERE id=? ",(id,))
        banc=self.cur.fetchone()
        if banc:
            return banc[0]
        else:
            return -1
         
    def insert_situacao_proposicao(self,id,descricao,ativa):
       
        id_situacao=self.__get_situacao_proposicao_db_ID(id)
        if ( id_situacao<0):
            data=(None,id,descricao,ativa)
            data=tuple([aux.prepare_string_to_db(d) for d in data])
            self.cur.execute("INSERT INTO situacao_proposicao VALUES (?,?,?,?)",data)
            self.conn.commit()
            print "tipo_situacao_proposicao inserted"
        else:
            print "tipo_situacao_proposicao "+descricao+" already inserted"
           
            
        
    def get_situacao_proposicao(self):
        situacao_proposicao_list = self.cur.execute("SELECT * FROM situacao_proposicao")
        return situacao_proposicao_list.fetchall()

###################  Tipos Autores #########

    def __get_tipos_autores_db_ID(self,id):
        self.cur.execute("SELECT * FROM tipos_autores WHERE id=? ",(id,))
        banc=self.cur.fetchone()
        if banc:
            return banc[0]
        else:
            return -1
         
    def insert_tipos_autores(self,id,descricao):
       
        id_tipos_autores=self.__get_tipos_autores_db_ID(id)
        if ( id_tipos_autores<0):
            data=(None,id,descricao)
            data=tuple([aux.prepare_string_to_db(d) for d in data])
            self.cur.execute("INSERT INTO tipos_autores VALUES (?,?,?)",data)
            self.conn.commit()
            print "tipos_autores inserted"
        else:
            print "tipos_autores "+descricao+" already inserted"
        
    def get_tipos_autores(self):
        tipos_autores_list = self.cur.execute("SELECT * FROM tipos_autores")
        return tipos_autores_list.fetchall()


###################  Indices #########

    def __get_indices_db_ID(self,indice):
        self.cur.execute("SELECT * FROM indices WHERE indice=? ",(indice,))
        banc=self.cur.fetchone()
        if banc:
            return banc[0]
        else:
            return -1
         
    def insert_indices(self,indice):
       
        id_indice=self.__get_indices_db_ID(indice)
        if ( id_indice<0):
            data=(None,indice)
            data=tuple([aux.prepare_string_to_db(d) for d in data])
            self.cur.execute("INSERT INTO indices VALUES (?,?)",data)
            self.conn.commit()
#            print "Indice "+str(indice)+" inserted"
        else:
            pass
 #           print "Indice "+str(indice)+" already inserted"
        
    def get_indices(self):
        indices_list = self.cur.execute("SELECT * FROM indices")
        return indices_list.fetchall()


###################  Indexacao #########

    def __get_indexacao_db_ID(self,id_proposicao,id_indice):
        self.cur.execute("SELECT * FROM indexacao WHERE id_indice=? and id_proposicao=? ",(id_indice,id_proposicao))
        banc=self.cur.fetchone()
        if banc:
            return banc[0]
        else:
            return -1
         
    def insert_indexacao(self,id_proposicao, id_indice):
       
        id_indexacao=self.__get_indexacao_db_ID(id_proposicao,id_indice)
        if ( id_indexacao<0):
            data=(id_proposicao,id_indice)
            data=tuple([aux.prepare_string_to_db(d) for d in data])
            self.cur.execute("INSERT INTO indexacao VALUES (?,?)",data)
            self.conn.commit()
            print "Indexacao "+id_indice+'-'+id_proposicao+" inserted"
        else:
            print "Indexacao "+id_indice+'-'+id_proposicao+" already inserted"
        
    def get_indexacao(self):
        indexacao_list = self.cur.execute("SELECT * FROM indexacao")
        return indexacao_list.fetchall()


###################  Orgaos #########

    def get_orgaos_db_ID(self,id):
        self.cur.execute("SELECT * FROM orgaos WHERE id=? ",(id,))
        banc=self.cur.fetchone()
        if banc:
            return banc[0]
        else:
            return -1
         
    def insert_orgaos(self,id,sigla,descricao):
       
        id_orgaos=self.get_orgaos_db_ID(id)
        if ( id_orgaos<0):
            data=(None,id,sigla,descricao)
            data=tuple([aux.prepare_string_to_db(d) for d in data])
            self.cur.execute("INSERT INTO orgaos VALUES (?,?,?,?)",data)
            self.conn.commit()
            print "orgao "+sigla+" inserted"
        else:
            print "tipos_autores "+sigla+" already inserted"
        
    def get_orgaos(self):
        orgaos_list = self.cur.execute("SELECT * FROM orgaos")
        return orgaos_list.fetchall()

###################  Proposicao #########

    def get_proposicao_db_ID(self,id):
        self.cur.execute("SELECT * FROM proposicoes WHERE id=?",(id,))
        banc=self.cur.fetchone()
        if banc:
            return banc[0]
        else:
            return -1

    

    def get_proposicao_db_ID_by_type(self,tipo,numero,ano):
        self.cur.execute("SELECT * FROM proposicoes WHERE tipo=? AND numero=? AND ano=?",(tipo,numero,ano,))
        banc=self.cur.fetchone()
        if banc:
            return banc[0]
        else:
            return -1
  
         
    def insert_proposicao(self,id,tipo,numero,ano,id_orgao_numerador,ementa,explicacao_ementa,id_regime,regime, id_apreciacao,apreciacao, autor_nome, autor_partido,autor_uf, despacho, despacho_data, id_situacao, orgao_situacao, situacao_proposicao, link_interior_teor):
       
        id_proposicao=self.get_proposicao_db_ID(id)
        if ( id_proposicao<0):
            data=(None, id, tipo, numero, ano, id_orgao_numerador, ementa, explicacao_ementa, id_regime, regime, id_apreciacao, apreciacao, autor_nome, autor_partido, autor_uf, despacho, despacho_data, id_situacao, orgao_situacao, situacao_proposicao, link_interior_teor)
            data=tuple([aux.prepare_string_to_db(d) for d in data])
            self.cur.execute("INSERT INTO proposicoes VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",data)
            self.conn.commit()
            print "Proposicao "+id+" inserted"
        else:
            print "Proposicao "+id+" already inserted"
        
    def get_proposicao(self):
        proposicao_list = self.cur.execute("SELECT * FROM proposicoes")
        return proposicao_list.fetchall()


###################  Votacao #########

    def get_votacao_db_ID(self,id_proposicao,resumo,data,hora):
        id_proposicao=aux.prepare_string_to_db(id_proposicao)
        resumo=aux.prepare_string_to_db(resumo)
        data=aux.prepare_string_to_db(data)
        hora=aux.prepare_string_to_db(hora)
        
        self.cur.execute("SELECT * FROM votacao WHERE id_proposicao=? AND resumo=? AND data=? AND hora=?",(id_proposicao,resumo,data,hora,))
        banc=self.cur.fetchone()
        if banc:
            return banc[0]
        else:
            return -1
         
    def insert_votacao(self,id_proposicao,resumo,data,hora,objvotacao):
        id_proposicao=aux.prepare_string_to_db(id_proposicao)
        resumo=aux.prepare_string_to_db(resumo)
        data=aux.prepare_string_to_db(data)
        hora=aux.prepare_string_to_db(hora)
        objvotacao=aux.prepare_string_to_db(objvotacao)
        
        id=self.get_votacao_db_ID(id_proposicao,resumo,data,hora)
        if ( id<0):
            data=(None, id_proposicao,resumo,data,hora,objvotacao)
            data=tuple([aux.prepare_string_to_db(d) for d in data])
            self.cur.execute("INSERT INTO votacao VALUES (?,?,?,?,?,?)",data)
            self.conn.commit()
            print "votacao for proposicao "+str(id_proposicao)+" inserted"
        else:
            print "votacao "+str(id)+" already inserted"
        
    def get_votacao(self):
        proposicao_list = self.cur.execute("SELECT * FROM votacao")
        return proposicao_list.fetchall()


 
###################  Votos #########

    def get_voto_db_ID(self,id_votacao,nome_deputado,partido_deputado,uf_deputado,voto):
        self.cur.execute("SELECT * FROM voto WHERE id_votacao=? AND nome_deputado=? AND partido_deputado=? AND uf_deputado=? AND voto=?",(id_votacao,nome_deputado,partido_deputado,uf_deputado,voto))
        banc=self.cur.fetchone()
        if banc:
            return banc[0]
        else:
            return -1
         
    def insert_voto(self,id_votacao,nome_deputado,partido_deputado,uf_deputado,voto):
        id=self.get_voto_db_ID(id_votacao,nome_deputado,partido_deputado,uf_deputado,voto)
        if (id<0):
            data=(None,id_votacao,nome_deputado,partido_deputado,uf_deputado,voto)
            data=tuple([aux.prepare_string_to_db(d) for d in data])
            self.cur.execute("INSERT INTO voto VALUES (?,?,?,?,?,?)",data)
            self.conn.commit()
            print "voto  inserted in votacao "+str(id_votacao)
        else:
            print "voto "+str(id)+" already inserted"
        
    def get_voto(self):
        voto_list = self.cur.execute("SELECT * FROM voto")
        return voto_list.fetchall() 









