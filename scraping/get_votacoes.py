import crawler
from db_access import *
import aux
import time

DATABASE="database/transparencia.db"
ALL_PROPOSICOES="tmp/all_proposicoes.txt"
PROPOSICOES_INSERTED="tmp/proposicoes_inserted.txt"
LOGGING_FILE="tmp/log.txt"
PROPOSICAO_VOTACAO_ID="tmp/proposicoes_votacao_id.txt"
VALID_VOTACAO_PROPOSICAO="tmp/valid_proposicao_votacao.txt"

db = TransparenciaDB(DATABASE)


def insert_votacoes_proposicao(id_proposicao):
    db.cur.execute("SELECT * FROM proposicoes WHERE id_proposicao=? ",(id_proposicao,))

    prop=db.cur.fetchone()

    if prop:
        try: 
            votacoes=crawler.ObterVotacaoProposicao(prop[2],prop[3],prop[4],1).info['votacoes']
        except:
            f=open(PROPOSICAO_VOTACAO_ID,'a')
            f.write(str(id_proposicao)+'\n')
            f.close()            
            print "problem downloading votacao for proposicao "+str(id_proposicao)
            return -2
        for votacao in votacoes:
            db.insert_votacao(id_proposicao,votacao['resumo'],votacao['data'],votacao['hora'],votacao['objvotacao'])
            id=db.get_votacao_db_ID(id_proposicao,votacao['resumo'],votacao['data'],votacao['hora'])
            insert_votacao(id,votacao)
            
        print "inserted votacoes with ID :"+str(id)
        f=open(PROPOSICAO_VOTACAO_ID,'a')
        f.write(str(id_proposicao)+'\n')
        f.close()
        
        f=open(VALID_VOTACAO_PROPOSICAO,'a')
        f.write(str(id_proposicao)+'\n')
        f.close()       
        
            #print "*******************"
        return 1
    else:
        f=open(PROPOSICAO_VOTACAO_ID,'a')
        f.write(str(id_proposicao)+'\n')
        f.close()
        return -1
    
def insert_votacao(id_votacao,votacao):
    for voto in votacao['deputado']:
        db.insert_voto(id_votacao,voto['nome'],voto['partido'],voto['uf'],voto['voto'])


#f=open(PROPOSICAO_VOTACAO_ID,'r')
#inserted_ids = f.read().split('\n')[0:-1]
#f.close()


#proposicoes = db.cur.execute("SELECT id_proposicao FROM proposicoes").fetchall()

#id_list=[proposicao[0] for proposicao in proposicoes]

#for id_proposicao in id_list:
#    if str(id_proposicao) not in inserted_ids:
#        insert_votacoes_proposicao(id_proposicao)


