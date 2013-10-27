"""
Crawler for Transparencia na Camara website: 
"""

import os
import sys
import time
import aux

import urllib
from bs4 import BeautifulSoup
import re

CRAWLER_DELAY=5  #delay (in s)




class Data:
	def __init__(self,url,fields,filename,DOWNLOAD):
		self.filename = filename
		self.fields = fields
		self.url = url
		
		if (DOWNLOAD == 1):
			self.download_raw_from_url(self.url,self.filename)
	
		bs_raw = self.soup_from_raw(self.get_raw_from_file(self.filename),self.fields)
	
		self.info = self.info_from_soup(bs_raw,self.fields)
  
		
	def get_raw_from_file(self,FILENAME):
		try:
			f=open(FILENAME)
			text=f.read()
			return text
		except:
			print "Problem reading FILE: "+FILENAME+"!!!!"
			return 0
		
	def download_raw_from_url(self,url,POST_TMP):
		try:
			urllib.urlretrieve(url,POST_TMP)
			return 1
		except:
			print "Problem reading url: "+url+"!!!!"
			return 0
		
	def soup_from_raw(self,rawText,field):
		return BeautifulSoup(rawText).find(field['field_name'])
	
	def info_from_soup(self,bs_rawText,field):
	
		bs=bs_rawText
	
		
       		if (len(field['parameters'])==0 and len(field['subfields'])==0):
			info = bs.text
#			if field['type']=='int':
#				info = int(info)
			info = aux.prepare_string_to_db(info)
       			return info
       		else:
			info={}
		
			
		       	for param in field['parameters']:
				try:
					info[param]=bs[param]
				except:
					info[param]=''
       			if (field['type']=='list'):
				for subfield in field['subfields']:
					info[subfield['field_name']]=[]
					if (bs.find(subfield['field_name'])):
						for information in bs.find_all(subfield['field_name']):
							info[subfield['field_name']].append(self.info_from_soup(information,subfield))	
       			else:	
				for subfield in field['subfields']:
					if(bs.find(subfield['field_name'])):
						info[subfield['field_name']]=self.info_from_soup(bs.find(subfield['field_name']),subfield)
			if(len(info)==1):
				info=info[info.keys()[0]]
			return info
			
###   DEPUTADOS   ###

class ObterDeputados:
	def __init__(self,DOWNLOAD):
		self.url="http://www.camara.gov.br/SitCamaraWS/Deputados.asmx/ObterDeputados"
		self.DOWNLOAD_FILE = "tmp/ObterDeputados.xml"
		self.fields = {'field_name':'deputados','parameters':{},'type':'list','subfields':[{'field_name': 'deputado', 'parameters':{},'type':'dict','subfields':[{'field_name':'idecadastro','parameters':{},'type':'int','subfields':[]},{'field_name':'idparlamentar','parameters':{},'type':'int','subfields':[]},{'field_name':'nome','parameters':{},'type':'str','subfields':[]},{'field_name':'nomeparlamentar','parameters':{},'type':'str','subfields':[]},{'field_name':'sexo','parameters':{},'type':'str','subfields':[]},{'field_name':'uf','parameters':{},'type':'str','subfields':[]},{'field_name':'partido','parameters':{},'type':'str','subfields':[]},{'field_name':'gabinete','parameters':{},'type':'int','subfields':[]},{'field_name':'anexo','parameters':{},'type':'int','subfields':[]},{'field_name':'email','parameters':{},'type':'str','subfields':[]},{'field_name':'fone','parameters':{},'type':'str','subfields':[]},{'field_name':'comissoes','parameters':{},'type':'dict','subfields':[{'field_name':'titular','parameters':{},'type':'list','subfields':[{'field_name':'comissao','parameters':{'nome':'str','sigla':'str'},'type':'dict','subfields':[]}]},{'field_name':'suplente','parameters':{},'type':'list','subfields':[{'field_name':'comissao','parameters':{'nome':'str','sigla':'str'},'type':'dict','subfields':[]}]}]}]}]}
		
		data = Data(self.url,self.fields,self.DOWNLOAD_FILE,DOWNLOAD)
		self.info = data.info


class ObterLideresBancadas:
	def __init__(self,DOWNLOAD):
		self.url = "http://www.camara.gov.br/SitCamaraWS/Deputados.asmx/ObterLideresBancadas"
		self.DOWNLOAD_FILE = "tmp/ObterLideresBancadas.xml"
		self.fields = {'field_name':'bancadas','parameters':{},'type':'list','subfields':[{'field_name':'bancada','parameters':{'nome':'str','sigla':'str'},'type':'list','subfields':[{'field_name':'lider','parameters':{},'type':'dict','subfields':[{'field_name':'nome','parameters':{},'type':'dict','subfields':[ ]},{'field_name':'partido','parameters':{},'type':'str','subfields':[ ]},{'field_name':'uf','parameters':{},'type':'dict','subfields':[ ]} ]},{'field_name':'vice_lider','parameters':{},'type':'dict','subfields':[{'field_name':'nome','parameters':{},'type':'dict','subfields':[ ]},{'field_name':'partido','parameters':{},'type':'str','subfields':[ ]},{'field_name':'uf','parameters':{},'type':'dict','subfields':[ ]} ]} ]}, ]}
		
		data = Data(self.url,self.fields,self.DOWNLOAD_FILE,DOWNLOAD)
		self.info = data.info


###   ORGAOS   ###
class ListarCargosOrgaosLegislativosCD:
		
	def __init__(self,DOWNLOAD):
		self.url="http://www.camara.gov.br/SitCamaraWS/Orgaos.asmx/ListarCargosOrgaosLegislativosCD"
		self.DOWNLOAD_FILE = "tmp/ListarOrgaosLegislativosCD.xml"
		self.fields = {'field_name':'cargosorgaos','parameters':{},'type':'list','subfields':[ {'field_name':'cargo','parameters':{'id':'str','descricao':'str'},'type':'dict','subfields':[]} ]}

		data = Data(self.url,self.fields,self.DOWNLOAD_FILE,DOWNLOAD)
		self.info = data.info		

class ListarTiposOrgaos:
		
	def __init__(self):
		self.url="http://www.camara.gov.br/SitCamaraWS/Orgaos.asmx/ListarTiposOrgaos"
		self.DOWNLOAD_FILE = "tmp/ListarTiposOrgaos.xml"
		self.fields = {'field_name':'tiposorgaos','parameters':{},'type':'list','subfields':[ {'field_name':'tipoorgao','parameters':{'id':'str','descricao':'str'},'type':'dict','subfields':[]} ]}

		data = Data(self.url,self.fields,self.DOWNLOAD_FILE)
		self.info = data.info

#DOWNLOAD = 0
#test= ListarTiposOrgaos()
#info = test.info
#print info

class ObterAndamento:
		
	def __init__(self,sigla,numero,ano,dataIni,codOrgao):
		self.url="http://www.camara.gov.br/SitCamaraWS/Orgaos.asmx/ObterAndamento?sigla="+ sigla+"&numero="+str(numero)+"&ano="+str(ano)+"&dataIni="+dataIni+"&codOrgao="+codOrgao
		self.DOWNLOAD_FILE = "tmp/ObterAndamento.xml"

		data = {'field_name':'data','parameters':{},'type':'str','subfields':[ ]}
	       	codorgao = {'field_name':'codorgao','parameters':{},'type':'str','subfields':[ ]}
		orgao = {'field_name':'orgao','parameters':{},'type':'str','subfields':[ ]}
		descricao = {'field_name':'descricao','parameters':{},'type':'str','subfields':[ ]}
		tramitacao = {'field_name':'tramitacao','parameters':{},'type':'str','subfields':[data,codorgao,orgao,descricao]}
	       	ultimaacao = {'field_name':'ultimaacao','parameters':{},'type':'list','subfields':[tramitacao ]}
		andamento = {'field_name':'andamento','parameters':{},'type':'list','subfields':[tramitacao ]}
		situacao =  {'field_name':'situacao','parameters':{},'type':'str','subfields':[ ]}
		ementa = {'field_name':'ementa','parameters':{},'type':'str','subfields':[ ]}
		idproposicao = {'field_name':'idproposicao','parameters':{},'type':'str','subfields':[ ]}
		self.fields = {'field_name':'proposicao','parameters':{'tipo':'str','numero':'int','ano':'str'},'type':'dict','subfields':[ situacao,ementa,idproposicao,ultimaacao,andamento ]}

		data = Data(self.url,self.fields,self.DOWNLOAD_FILE)
		self.info = data.info

#DOWNLOAD = 0
#test= ObterAndamento('PL',3962,'2008','01/01/2009','')
#info = test.info
#print info

	
		
class ObterEmendasSubstitutivoRedacaoFinal:
		
	def __init__(self,tipo,numero,ano):
		self.url="http://www.camara.gov.br/SitCamaraWS/Orgaos.asmx/ObterEmendasSubstitutivoRedacaoFinal?tipo="+tipo+"&numero="+str(numero)+"&ano="+str(ano)
		self.DOWNLOAD_FILE = "tmp/ObterEmentasSubstitutivoRedacaoFinal.xml"

		substitutivo =  {'field_name':'substitutivo','parameters':{'codproposicao':'str','descricao':'str'},'type':'dict','subfields':[ ]}
		substitutivos =  {'field_name':'substitutivos','parameters':{},'type':'list','subfields':[substitutivo]}	
		redacaofinal =  {'field_name':'redacaofinal','parameters':{'codproposicao':'str','descricao':'str'},'type':'dict','subfields':[ ]}
		redacoesfinais =  {'field_name':'redacoesfinais','parameters':{},'type':'list','subfields':[redacaofinal]}
		emenda =  {'field_name':'emenda','parameters':{'codproposicao':'str','descricao':'str'},'type':'dict','subfields':[ ]}
		emendas =  {'field_name':'emendas','parameters':{},'type':'list','subfields':[emenda]}
		self.fields = {'field_name':'proposicao','parameters':{'tipo':'str','numero':'int','ano':'str'},'type':'dict','subfields':[ substitutivos,redacoesfinais,emendas ]}

		data = Data(self.url,self.fields,self.DOWNLOAD_FILE)
		self.info = data.info

#DOWNLOAD = 0
#test= ObterEmendasSubstitutivoRedacaoFinal('PL',3962,'2008')
#info = test.info
#print info
			
class ObterIntegraComissoesRelator:
		
	def __init__(self,tipo,numero,ano):
		self.url="http://www.camara.gov.br/SitCamaraWS/Orgaos.asmx/ObterIntegraComissoesRelator?tipo="+tipo+"&numero="+str(numero)+"&ano="+str(ano)
		self.DOWNLOAD_FILE = "tmp/ObterIntegraComissoesRelator.xml"
		
		relator =  {'field_name':'relator','parameters':{},'type':'str','subfields':[]}
		parecer =  {'field_name':'parecer','parameters':{},'type':'str','subfields':[]}
		comissao =  {'field_name':'comissao','parameters':{'nome':'str','sigla':'str'},'type':'dict','subfields':[relator,parecer]}
		comissoes =  {'field_name':'comissoes','parameters':{},'type':'list','subfields':[comissao]}
		integra =  {'field_name':'integra','parameters':{'linkarquivo':'str'},'type':'dict','subfields':[ ]}
		self.fields = {'field_name':'proposicao','parameters':{'tipo':'str','numero':'int','ano':'str'},'type':'dict','subfields':[ comissoes,integra ]}

		data = Data(self.url,self.fields,self.DOWNLOAD_FILE)
		self.info = data.info

#DOWNLOAD = 0
#test= ObterIntegraComissoesRelator('PL',3962,'2008')
#info = test.info
#print info
	
		
				
class ObterMembrosOrgao:
		
	def __init__(self,IdOrgao):
		self.url="http://www.camara.gov.br/SitCamaraWS/Orgaos.asmx/ObterMembrosOrgao?IDOrgao="+str(IdOrgao)
		self.DOWNLOAD_FILE = "tmp/ObterMembrosOrgao.xml"
		
		nome =  {'field_name':'nome','parameters':{},'type':'str','subfields':[]}
		partido =  {'field_name':'partido','parameters':{},'type':'str','subfields':[]}
		uf =  {'field_name':'uf','parameters':{},'type':'str','subfields':[]}
		situacao =  {'field_name':'situacao','parameters':{},'type':'str','subfields':[]}
		presidente =  {'field_name':'presidente','parameters':{},'type':'str','subfields':[nome,partido,uf,situacao]}
		primeirovice_presidente =  {'field_name':'primeirovice-presidente','parameters':{},'type':'str','subfields':[nome,partido,uf,situacao]}
		segundovice_presidente =  {'field_name':'segundovice-presidente','parameters':{},'type':'str','subfields':[nome,partido,uf,situacao]}
		terceirovice_presidente =  {'field_name':'terceitovice-presidente','parameters':{},'type':'str','subfields':[nome,partido,uf,situacao]}		
		membro =  {'field_name':'membro','parameters':{},'type':'str','subfields':[nome,partido,uf,situacao]}		
	        membros=  {'field_name':'membros','parameters':{},'type':'list','subfields':[presidente,primeirovice_presidente,segundovice_presidente,terceirovice_presidente,membro]}

		self.fields = {'field_name':'orgao','parameters':{'nome':'str'},'type':'dict','subfields':[membros]}

		data = Data(self.url,self.fields,self.DOWNLOAD_FILE)
		self.info = data.info

#DOWNLOAD = 0
#test= ObterMembrosOrgao(2004)
#info = test.info
#print info	

class ObterOrgao:
		
	def __init__(self,DOWNLOAD):
		self.url="http://www.camara.gov.br/SitCamaraWS/Orgaos.asmx/ObterOrgaos"
		self.DOWNLOAD_FILE = "tmp/ObterOrgaos.xml"
		
		orgao=  {'field_name':'orgao','parameters':{'id':'int','sigla':'str','descricao':'str'},'type':'dict','subfields':[]}
		self.fields = {'field_name':'orgaos','parameters':{},'type':'list','subfields':[orgao]}

		data = Data(self.url,self.fields,self.DOWNLOAD_FILE,DOWNLOAD)
		self.info = data.info

#DOWNLOAD = 0
#test= ObterOrgao()
#info = test.info
#print info[0]	
		
class ObterPauta:
		
	def __init__(self,IdOrgao,datIni,datFim):
		self.url="http://www.camara.gov.br/SitCamaraWS/Orgaos.asmx/ObterPauta?IDOrgao="+str(IdOrgao)+"&datIni="+datIni+"&datFim="+datFim
		self.DOWNLOAD_FILE = "tmp/ObterPauta.xml"

		data=  {'field_name':'data','parameters':{},'type':'str','subfields':[]}
		horario=  {'field_name':'horario','parameters':{},'type':'str','subfields':[]}
		local=  {'field_name':'local','parameters':{},'type':'str','subfields':[]}
		estado=  {'field_name':'estado','parameters':{},'type':'str','subfields':[]}
		tipo=  {'field_name':'tipo','parameters':{},'type':'str','subfields':[]}
		objeto=  {'field_name':'objeto','parameters':{},'type':'str','subfields':[]}
		
		sigla=  {'field_name':'sigla','parameters':{},'type':'str','subfields':[]}
		ementa=  {'field_name':'ementa','parameters':{},'type':'str','subfields':[]}
		
		proposicao=  {'field_name':'proposicao','parameters':{},'type':'dict','subfields':[sigla,ementa]}
		proposicoes=  {'field_name':'proposicoes','parameters':{},'type':'list','subfields':[proposicao]}
		
		reuniao=  {'field_name':'reuniao','parameters':{},'type':'dict','subfields':[data,horario,local,estado,tipo,objeto,proposicoes]}
		
		self.fields = {'field_name':'pauta','parameters':{'orgao':'str','datainicial':'str','datafinal':'str'},'type':'list','subfields':[reuniao]}

		data = Data(self.url,self.fields,self.DOWNLOAD_FILE)
		self.info = data.info

#DOWNLOAD = 0
#test= ObterPauta(2004,'01/01/2012','30/04/2012')
#info = test.info
#print info
		
		
class ObterRegimeTramitacaoDespacho:
		
	def __init__(self,tipo,numero,ano):
		self.url="http://www.camara.gov.br/SitCamaraWS/Orgaos.asmx/ObterRegimeTramitacaoDespacho?tipo="+tipo+"&numero="+str(numero)+"&ano="+str(ano)
	       	self.DOWNLOAD_FILE = "tmp/ObterRegimeTramitacaoDespacho.xml"

		autor = {'field_name':'autor','parameters':{},'type':'str','subfields':[]}
		regimetramitacao = {'field_name':'regimetramitacao','parameters':{},'type':'str','subfields':[]}
		apreciacao = {'field_name':'apreciacao','parameters':{},'type':'str','subfields':[]}
		despacho = {'field_name':'despacho','parameters':{},'type':'str','subfields':[]}
		self.fields = {'field_name':'proposicao','parameters':{'tipo':'str','numero':'int','ano':'2010'},'type':'dict','subfields':[autor,regimetramitacao,apreciacao,despacho]}

		data = Data(self.url,self.fields,self.DOWNLOAD_FILE)
		self.info = data.info

#DOWNLOAD = 0
#test= ObterRegimeTramitacaoDespacho('PL',8035,2010)
#info = test.info
#print info
		
		
	
###   PROPOSICOES   ###
		
class ListarProposicoes:
		
	def __init__(self,sigla,numero,ano,datApresentacaoIni,datApresentacaoFim,autor,parteNomeAutor,siglaPartidoAutor,siglaUFAutor, generoAutor, codEstado,codOrgaoEstado,emTramitacao,DOWNLOAD):
		self.url="http://www.camara.gov.br/SitCamaraWS/Proposicoes.asmx/ListarProposicoes?sigla="+sigla+"&numero="+str(numero)+"&ano="+str(ano)+"&datApresentacaoIni="+datApresentacaoIni+"+&datApresentacaoFim="+datApresentacaoFim+"&autor="+autor+"&parteNomeAutor="+parteNomeAutor+"&siglaPartidoAutor="+siglaPartidoAutor+"&siglaUFAutor="+siglaUFAutor+"&generoAutor="+generoAutor+"&codEstado="+codEstado+"&codOrgaoEstado="+codOrgaoEstado+"&emTramitacao="+emTramitacao
	       	self.DOWNLOAD_FILE = "tmp/ListarProposicoes.xml"

		Id = {'field_name':'id','parameters':{},'type':'str','subfields':[]}
	        nome = {'field_name':'nome','parameters':{},'type':'str','subfields':[]}

		tipoID = {'field_name':'id','parameters':{},'type':'str','subfields':[]}
		tipoSigla = {'field_name':'sigla','parameters':{},'type':'str','subfields':[]}
		tipoNome = {'field_name':'nome','parameters':{},'type':'str','subfields':[]}
		tipoproposicao = {'field_name':'tipoproposicao','parameters':{},'type':'dict','subfields':[tipoID,tipoSigla,tipoNome]}

		numero = {'field_name':'numero','parameters':{},'type':'int','subfields':[]}	
		ano = {'field_name':'ano','parameters':{},'type':'int','subfields':[]}	

		OrgaoNumeradorID = {'field_name':'id','parameters':{},'type':'str','subfields':[]}
		OrgaoNumeradorSigla = {'field_name':'sigla','parameters':{},'type':'str','subfields':[]}
		OrgaoNumeradorNome = {'field_name':'nome','parameters':{},'type':'str','subfields':[]}
		orgaonumerador = {'field_name':'orgaonumerador','parameters':{},'type':'dict','subfields':[OrgaoNumeradorID,OrgaoNumeradorSigla,OrgaoNumeradorNome]}

		datapresentacao = {'field_name':'dataapresentacao','parameters':{},'type':'str','subfields':[]}
		txtementa = {'field_name':'txtementa','parameters':{},'type':'str','subfields':[]}
		txtexplicacaoementa = {'field_name':'txtexplicacaoementa','parameters':{},'type':'str','subfields':[]}
		qtdautores = {'field_name':'qtdautores','parameters':{},'type':'int','subfields':[]}

		codregime = {'field_name':'codregime','parameters':{},'type':'str','subfields':[]}
		txtregime = {'field_name':'txtregime','parameters':{},'type':'str','subfields':[]}
		regime = {'field_name':'regime','parameters':{},'type':'dict','subfields':[codregime,txtregime]}

		ApreciacaoID = {'field_name':'id','parameters':{},'type':'str','subfields':[]}
		txtApreciacao = {'field_name':'txtapreciacao','parameters':{},'type':'str','subfields':[]}
		apreciacao = {'field_name':'apreciacao','parameters':{},'type':'dict','subfields':[ApreciacaoID,txtApreciacao]}
	
		txtNomeAutor = {'field_name':'txtnomeautor','parameters':{},'type':'str','subfields':[]}
	        codPartido = {'field_name':'codpartido','parameters':{},'type':'str','subfields':[]}
		txtsiglapartido = {'field_name':'txtsiglapartido','parameters':{},'type':'str','subfields':[]}
		txtsiglaUF = {'field_name':'txtsiglauf','parameters':{},'type':'str','subfields':[]}
		autor1 = {'field_name':'autor1','parameters':{},'type':'dict','subfields':[txtNomeAutor,codPartido,txtsiglapartido,txtsiglaUF]}

		datDespacho = {'field_name':'datdespacho','parameters':{},'type':'str','subfields':[]}
		txtDespacho = {'field_name':'txtdespacho','parameters':{},'type':'str','subfields':[]}
		ultimoDespacho = {'field_name':'ultimodespacho','parameters':{},'type':'dict','subfields':[datDespacho,txtDespacho]}

		situacaoID = {'field_name':'id','parameters':{},'type':'str','subfields':[]}
	        descricao = {'field_name':'descricao','parameters':{},'type':'str','subfields':[]}
		codorgaoestado = {'field_name':'codorgaoestado','parameters':{},'type':'str','subfields':[]}
		siglaorgaoestado = {'field_name':'siglaorgaoestado','parameters':{},'type':'str','subfields':[]}
		orgao = {'field_name':'orgao','parameters':{},'type':'dict','subfields':[codorgaoestado,siglaorgaoestado]}
	       	codProposicaoPrincipal = {'field_name':'codproposicaoprincipal','parameters':{},'type':'str','subfields':[]}
		proposicaoPrincipal = {'field_name':'proposicaoprincipal','parameters':{},'type':'str','subfields':[]}
		principal = {'field_name':'principal','parameters':{},'type':'dict','subfields':[codProposicaoPrincipal,proposicaoPrincipal]}
		situacao = {'field_name':'situacao','parameters':{},'type':'dict','subfields':[situacaoID,descricao,orgao,principal]}

		proposicao = {'field_name':'proposicao','parameters':{},'type':'dict','subfields':[Id,nome,tipoproposicao,numero,ano,orgaonumerador,datapresentacao,txtementa,txtexplicacaoementa,qtdautores,regime,apreciacao,autor1,ultimoDespacho,situacao]}
	
		self.fields = {'field_name':'proposicoes','parameters':{},'type':'list','subfields':[proposicao]}

	
		data = Data(self.url,self.fields,self.DOWNLOAD_FILE,DOWNLOAD)
		self.info = data.info

#DOWNLOAD = 0
#test= ListarProposicoes('PL','',2010,'','','','','','','','','','')
#info = test.info
#print info[0]		
		

		
class ListarSiglasTipoProposicao:
		
	def __init__(self,DOWNLOAD):
		self.url="http://www.camara.gov.br/SitCamaraWS/Proposicoes.asmx/ListarSiglasTipoProposicao"
		self.DOWNLOAD_FILE = "tmp/ListarSiglasTipoProposicao.xml"
		silga = {'field_name':'silga','parameters':{'tiposigla':'str','descricao':'str','ativa':'str','genero':'str'},'type':'str','subfields':[]}
		self.fields = {'field_name':'siglas','parameters':{},'type':'list','subfields':[silga]}
		data = Data(self.url,self.fields,self.DOWNLOAD_FILE,DOWNLOAD)
		self.info = data.info

#DOWNLOAD = 0
#test= ListarSiglasTipoProposicao()
#info = test.info
#print info	



class ListarSituacoesProposicao:
		
	def __init__(self,DOWNLOAD):
		self.url="http://www.camara.gov.br/SitCamaraWS/Proposicoes.asmx/ListarSituacoesProposicao"
		self.DOWNLOAD_FILE = "tmp/ListarSituacoesProposicao.xml"

		situacaoproposicao = {'field_name':'situacaoproposicao','parameters':{'id':'srt','descricao':'str','ativa':'str'},'type':'dict','subfields':[]}
		self.fields = {'field_name':'situacaoproposicao','parameters':{},'type':'list','subfields':[situacaoproposicao]}

		data = Data(self.url,self.fields,self.DOWNLOAD_FILE,DOWNLOAD)
		self.info = data.info

#DOWNLOAD = 0
#test= ListarSituacoesProposicao()
#info = test.info
#print info

		
class ListarTiposAutores:
		
	def __init__(self,DOWNLOAD):
		self.url="http://www.camara.gov.br/SitCamaraWS/Proposicoes.asmx/ListarTiposAutores"
	       	self.DOWNLOAD_FILE = "tmp/ListarTiposAutores.xml"

		tipoautor = {'field_name':'tipoautor','parameters':{'id':'int','descricao':'str'},'type':'dict','subfields':[]}
		self.fields = {'field_name':'siglas','parameters':{},'type':'list','subfields':[tipoautor]}

		data = Data(self.url,self.fields,self.DOWNLOAD_FILE,DOWNLOAD)
		self.info = data.info

#DOWNLOAD = 0
#test= ListarTiposAutores()
#info = test.info
#print info

class ObterProposicao:
	def __init__(self,tipo,numero,ano,DOWNLOAD):
		self.url="http://www.camara.gov.br/SitCamaraWS/Proposicoes.asmx/ObterProposicao?tipo="+str(tipo)+"&numero="+str(numero)+"&ano="+str(ano)
		self.DOWNLOAD_FILE = "tmp/ObterProposicao.xml"


		linkinteiroteor = {'field_name':'linkinteiroteor','parameters':{},'type':'str','subfields':[]}
		situacao = {'field_name':'situacao','parameters':{},'type':'str','subfields':[]}
		indexacao = {'field_name':'indexacao','parameters':{},'type':'str','subfields':[]}
		apreciacao = {'field_name':'apreciacao','parameters':{},'type':'str','subfields':[]}
		ultimodespacho = {'field_name':'ultimodespacho','parameters':{'data':'str'},'type':'str','subfields':[]}
		regimetramitacao = {'field_name':'regimetramitacao','parameters':{},'type':'str','subfields':[]}
		dataapresentacao = {'field_name':'dataapresentacao','parameters':{},'type':'str','subfields':[]}
		autor = {'field_name':'autor','parameters':{},'type':'str','subfields':[]}
		explicacaoementa = {'field_name':'explicacaoementa','parameters':{},'type':'srt','subfields':[]}
		ementa = {'field_name':'ementa','parameters':{},'type':'str','subfields':[]}
		idproposicao = {'field_name':'idproposicao','parameters':{},'type':'int','subfields':[]}
		self.fields = {'field_name':'proposicao','parameters':{'tipo':'str','numero':'int','ano':'str'},'type':'dict','subfields':[idproposicao,ementa,explicacaoementa,autor,dataapresentacao,regimetramitacao,ultimodespacho,apreciacao,indexacao,situacao,linkinteiroteor]}
		
		data = Data(self.url,self.fields,self.DOWNLOAD_FILE,DOWNLOAD)
		self.info = data.info

#DOWNLOAD = 0
#test= ObterProposicao('PL',3962,2008)
#info = test.info
#print info


		

class ObterProposicaoPorID:
	def __init__(self,IdProp,DOWNLOAD):
		self.url="http://www.camara.gov.br/SitCamaraWS/Proposicoes.asmx/ObterProposicaoPorID?IdProp="+str(IdProp)
		self.DOWNLOAD_FILE = "tmp/ObterProposicaoPorID.xml"

		linkinteiroteor = {'field_name':'linkinteiroteor','parameters':{},'type':'str','subfields':[]}
		situacao = {'field_name':'situacao','parameters':{},'type':'str','subfields':[]}
		indexacao = {'field_name':'indexacao','parameters':{},'type':'str','subfields':[]}
		apreciacao = {'field_name':'apreciacao','parameters':{},'type':'str','subfields':[]}
		ultimodespacho = {'field_name':'ultimodespacho','parameters':{'data'},'type':'str','subfields':[]}
		regimetramitacao = {'field_name':'regimetramitacao','parameters':{},'type':'str','subfields':[]}
		dataapresentacao = {'field_name':'dataapresentacao','parameters':{},'type':'str','subfields':[]}
		autor = {'field_name':'autor','parameters':{},'type':'str','subfields':[]}
		explicacaoementa = {'field_name':'explicacaoementa','parameters':{},'type':'srt','subfields':[]}
		ementa = {'field_name':'ementa','parameters':{},'type':'str','subfields':[]}
		tipoproposicao = {'field_name':'tipoproposicao','parameters':{},'type':'str','subfields':[]}
		nomeproposicao = {'field_name':'nomeproposicao','parameters':{},'type':'str','subfields':[]}
		
		self.fields = {'field_name':'proposicao','parameters':{'tipo':'str','numero':'int','ano':'str'},'type':'dict','subfields':[tipoproposicao,nomeproposicao,ementa,explicacaoementa,autor,dataapresentacao,regimetramitacao,ultimodespacho,apreciacao,indexacao,situacao,linkinteiroteor]}


		data = Data(self.url,self.fields,self.DOWNLOAD_FILE,DOWNLOAD)
		self.info = data.info

#DOWNLOAD = 0
#test=ObterProposicaoPorID(354258)
#info = test.info
#print info

	
class ObterVotacaoProposicao:
	def __init__(self,tipo, numero,ano,DOWNLOAD):
		self.url="http://www.camara.gov.br/SitCamaraWS/Proposicoes.asmx/ObterVotacaoProposicao?tipo="+str(tipo)+"&numero="+str(numero)+"&ano="+str(ano)
		self.DOWNLOAD_FILE = "tmp/ObterVotacaoProposicao.xml"

		deputado = {'field_name':'deputado','parameters':{'nome':'str','partido':'str','uf':'str','voto':'str'},'type':'dict','subfields':[]}
		votacao = {'field_name':'votacao','parameters':{'resumo':'str','hora':'str','objvotacao':'str','data':'str'},'type':'list','subfields':[deputado]}
		votacoes = {'field_name':'votacoes','parameters':{},'type':'list','subfields':[votacao]}
		ano = {'field_name':'ano','parameters':{},'type':'str','subfields':[]}
		numero = {'field_name':'numero','parameters':{},'type':'str','subfields':[]}
		sigla = {'field_name':'sigla','parameters':{},'type':'str','subfields':[]}
		self.fields = {'field_name':'proposicao','parameters':{},'type':'dict','subfields':[sigla,numero,ano,votacoes]}

		data = Data(self.url,self.fields,self.DOWNLOAD_FILE,DOWNLOAD)
		self.info = data.info


#test= ObterVotacaoProposicao('PL',1992,2007,1)
#info = test.info
#print info	
	

								
###   SESSOES REUNIOES   ###
class ListarSituacoesReuniaoSessao:
	def __init__(self,DOWNLOAD):
		self.url="http://www.camara.gov.br/SitCamaraWS/SessoesReunioes.asmx/ListarSituacoesReuniaoSessao"
		self.DOWNLOAD_FILE = "tmp/ListarSituacoesReuniaoSessao.xml"

		autor = {'field_name':'autor','parameters':{},'type':'str','subfields':[]}
		regimetramitacao = {'field_name':'regimetramitacao','parameters':{},'type':'str','subfields':[]}
		apreciacao = {'field_name':'apreciacao','parameters':{},'type':'str','subfields':[]}
		despacho = {'field_name':'despacho','parameters':{},'type':'str','subfields':[]}
		self.fields = {'field_name':'proposicao','parameters':{'tipo':'str','numero':'int','ano':'2010'},'type':'dict','subfields':[autor,regimetramitacao,apreciacao,despacho]}
		
		data = Data(self.url,self.fields,self.DOWNLOAD_FILE,DOWNLOAD)
		self.info = data.info

#DOWNLOAD = 1
#test= ObterRegimeTramitacaoDespacho('PL',8035,2010)
#info = test.info
#print info
	
	
#class ListarSituacoesReuniaoSessao:
#	def __init__(self):
#		self.url="http://www.camara.gov.br/SitCamaraWS/SessoesReunioes.asmx/ListarSituacoesReuniaoSessao"
		
#		self.ID = "" #int
#		self.Descricao = -1 #string
		
#		self.rawText=get_raw_from_url(self.url)
#		self.soup(self.rawText)
				
#	def soup(self,rawText):
#		return(rawText)		
		

### CRAWLER ###

class Crawler:
	def __init__(self):
		print "WELCOME"

cr=Crawler()














