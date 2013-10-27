import crawler
from db_access import *
DATABASE="database/transparencia.db"

db = TransparenciaDB(DATABASE)

########### DEPUTADOS ##################
bancadas = crawler.ObterLideresBancadas(0)

partidos=[[partido['sigla'],partido['nome']] for partido in bancadas.info]
for partido in partidos:
    print partido
    db.insert_partido(partido[0],partido[1])
print db.get_list_partidos()

deputados = crawler.ObterDeputados(0).info

for dep in deputados:
    db.insert_deputado(dep['idecadastro'],dep['idparlamentar'],dep['nome'],dep['nomeparlamentar'],dep['sexo'],dep['uf'],dep['partido'],dep['gabinete'],dep['anexo'],dep['fone'],dep['email'])
    suplente = dep['comissoes']['suplente']
    titular = suplente = dep['comissoes']['suplente']
    for sup in suplente:
        db.insert_comissao_deputado(dep['nome'],dep['partido'],dep['uf'],sup['nome'],sup['sigla'],'suplente')
    for til in titular:
        db.insert_comissao_deputado(dep['nome'],dep['partido'],dep['uf'],til['nome'],til['sigla'],'titular')

print db.get_list_deputados()
print db.get_list_comissao_deputados()
print db.get_list_comissoes()

########################################################################
    

