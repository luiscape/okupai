import crawler
from db_access import *
DATABASE="database/transparencia.db"
ALL_PROPOSICOES = "tmp/all_proposicoes.txt"

f=open(ALL_PROPOSICOES,'w')

db = TransparenciaDB(DATABASE)

siglas_list = db.get_siglas_tipo_proposicao()
siglas_list = [sigla[1] for sigla in siglas_list]

years_list = ["2001","2000","1999","1998","1997"]

tipos_year = [[[sigla,year] for sigla in siglas_list] for year in years_list]

for year in tipos_year:
    for tipo in year:
        print tipo
        print tipo[0]+" "+tipo[1]+"\n"
        f.write(tipo[0]+" "+tipo[1]+"\n")
f.close()
