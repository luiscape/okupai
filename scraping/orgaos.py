import crawler
from db_access import *
DATABASE="database/transparencia.db"

db = TransparenciaDB(DATABASE)

########### ORGAOS ##################
orgaos_list = crawler.ObterOrgao(0)

orgaos=[[orgao['id'],orgao['sigla'],orgao['descricao']] for orgao in orgaos_list.info]
for orgao in orgaos:
    db.insert_orgaos(orgao[0],orgao[1],orgao[2])
print db.get_orgaos()
