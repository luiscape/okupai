import crawler
from db_access import *
DATABASE="database/transparencia.db"

db = TransparenciaDB(DATABASE)

########### PROPOSICOES ##################
tipo_autores = crawler.ListarTiposAutores(0)
tipoautores=[[tipoautor['id'],tipoautor['descricao']] for tipoautor in tipo_autores.info]
for tipoautor in tipoautores:
    print tipoautor
    db.insert_tipos_autores(tipoautor[0],tipoautor[1])
print db.get_tipos_autores()

situacao_proposicao = crawler.ListarSituacoesProposicao(0)
situacoes=[[situacao['id'],situacao['descricao'],situacao['ativa']] for situacao in situacao_proposicao.info]
for situacao in situacoes:
    print situacao
    db.insert_situacao_proposicao(situacao[0],situacao[1],situacao[2])
print db.get_situacao_proposicao()

sigla_tipo_proposicao = crawler.ListarSiglasTipoProposicao(0)
tiposiglas=[[tiposigla['tiposigla'],tiposigla['descricao'],tiposigla['ativa'],tiposigla['genero'],""] for tiposigla in sigla_tipo_proposicao.info]
for tiposigla in tiposiglas:
    print tiposigla
    db.insert_siglas_tipo_proposicao(tiposigla[0],tiposigla[1],tiposigla[2],tiposigla[3],tiposigla[4])
print db.get_siglas_tipo_proposicao()

########################################################################

