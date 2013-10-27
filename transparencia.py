import crawler
from db_access import *
import aux
import time
import get_votacoes

DATABASE="database/transparencia.db"
ALL_PROPOSICOES="tmp/all_proposicoes.txt"
PROPOSICOES_INSERTED="tmp/proposicoes_inserted.txt"
LOGGING_FILE="tmp/log.txt"

db = TransparenciaDB(DATABASE)


class Proposicao:

    def __init__(self):
        self.active_list=[]

        f_all=open(ALL_PROPOSICOES,'r')
        f_inserted = open(PROPOSICOES_INSERTED,'r')
    
        all_tipos = [tipo.split(' ') for tipo in f_all.read().split('\n')][0:-1]
        inserted_tipos = [tipo.split(' ') for tipo in f_inserted.read().split('\n')][0:-1]

        f_all.close()
        f_inserted.close()

        for tipo in all_tipos:
            if tipo not in inserted_tipos:
                self.active_list.append(tipo)

    def iterate(self):
        if len(self.active_list)==0:
            aux.logging(LOGGING_FILE,"No more propositions to read ")
            return -1
        
        else:
            tipo=self.active_list.pop(0)

            self.soup=[]
            aux.logging(LOGGING_FILE,"Starting propositions with sigla="+str(tipo[0])+" ano="+str(tipo[1]))
            try:
                self.soup=crawler.ListarProposicoes(tipo[0],'',tipo[1],'','','','','','','','','','',1)
            except:
                aux.logging(LOGGING_FILE,"Cannot soup xml for propositions sigla="+tipo[0]+" ano="+tipo[1])
                self.mark_as_inserted(tipo)
                self.iterate()
                return 0
            aux.logging(LOGGING_FILE,"Souped proposition with sigla="+str(tipo[0])+" ano="+str(tipo[1]))
            for prop in self.soup.info:
                self.__insert_soup(prop)
            self.mark_as_inserted(tipo)
            aux.logging(LOGGING_FILE,"Marking propositions with sigla="+str(tipo[0])+" ano="+str(tipo[1])+" as inserted")
            return 1
                
    def __insert_soup(self,bs):
        ID = bs['id']
        aux.logging(LOGGING_FILE,"Reading proposition ID="+str(ID))
        if db.get_proposicao_db_ID(ID)<0:
            tipo = bs['tipoproposicao']['sigla']
            numero = bs['numero']
            ano = bs['ano']
            id_regime = bs['regime']['codregime']
            regime = bs['regime']['txtregime']
            id_apreciacao = bs['apreciacao']['id']
            apreciacao = bs['apreciacao']['txtapreciacao']
            autor_nome = bs['autor1']['txtnomeautor']
            autor_partido = bs['autor1']['txtsiglapartido']
            autor_uf = bs['autor1']['txtsiglauf']
            despacho_data = bs['ultimodespacho']['datdespacho']
            despacho = bs['ultimodespacho']['txtdespacho']
            ementa=bs['txtementa']
            explicacao_ementa=bs['txtexplicacaoementa']
            
            id_orgao_numerador=-1
            try:
                id_orgao_numerador=db_access.get_orgaos_db_ID(bs['orgaonumerador']['id'])
            except:
                pass
        
            id_situacao =bs['situacao']['id']
            orgao_situacao =bs['situacao']['orgao']['codorgaoestado']

 #           print ID
 #           print tipo
 #           print numero
 #           print ano

            try:
                time.sleep(1)
                soupOP = crawler.ObterProposicaoPorID(ID,1)
            
                situacao_proposicao = soupOP.info['situacao']
                link_inteiro_teor=soupOP.info['linkinteiroteor']
                indexacao=soupOP.info['indexacao']
            except:
                aux.logging(LOGGING_FILE,"ObterProposicaoPor ID error: Proposition ID="+str(ID)+" not found")
                situacao_proposicao =''
                link_inteiro_teor=''
                indexacao=''
                
            self.insert_indexacao(ID,indexacao)

            db.insert_proposicao(ID,tipo,numero,ano,id_orgao_numerador,ementa,explicacao_ementa,id_regime,regime,id_apreciacao,apreciacao,autor_nome,autor_partido,autor_uf,despacho,despacho_data,id_situacao,orgao_situacao,situacao_proposicao,link_inteiro_teor)
            propID=db.get_proposicao_db_ID(ID)
            if(propID>-1):
                get_votacoes.insert_votacoes_proposicao(propID)
                aux.logging(LOGGING_FILE,"Inserting votacoes for proposition ID="+str(propID))
        
    def insert_indexacao(self,ID,indexacao):
        aux.logging(LOGGING_FILE,"Inserting Indexacao for proposition ID="+str(ID))
        indices = indexacao.split(',')
        for indice in indices:
            indice=aux.prepare_string_to_db(indice.strip('\n'))
            if indice != '':
                db.insert_indices(indice)


    def mark_as_inserted(self,proposition_type):
        f=open(PROPOSICOES_INSERTED,'a')
        f.write(proposition_type[0]+' '+proposition_type[1]+"\n")
        f.close()
    
p=Proposicao()

while p.iterate()>-1:
    pass



