import os, os.path, sys
import logging, click
from pathlib import Path
import json
# Open file csv
#parâmetros de chamada
#caminho do arquivo: filepath=input()  ///defaut = caminho atual
#tipo da entrada (csv ou json): filetype=csv/json ///defaut = csv
#separador de caracter do cvs: sep=;/,/tab ///defaut = ,
def add_line_json(entrada, cabecalho, ln_dado):
   #
   if ln_dado=='':
      entrada = entrada + '      "'+cabecalho+'": null, \n' 
   elif ln_dado[0]=='\"':       
      entrada=entrada + '      "'+cabecalho+'": '+ln_dado+' ,\n'
   elif ln_dado.isnumeric():
      entrada = entrada + '      "'+cabecalho+'": '+ln_dado+',\n'   
   elif True:
      entrada = entrada + '      "'+cabecalho+'": "'+ln_dado+'",\n'
   return entrada


def csv2json (DIR, arquivo):
   print(print("----> CSV to JSON\n"))
   arq = open(os.path.join(DIR, arquivo), 'r', encoding='UTF-8')
   #print(arq)
   #
   cab=True
   json=''
   for line in arq:
      list_line = (line.split(";"))
      saida=""
      if cab: #monta cabeçalho de atributos
         atributos= list_line
      else: 
         saida="  {\n"
         for i in range(0,len(list_line)-2):
            saida = add_line_json(saida, atributos[i], list_line[i])
         #incluir a ultima linha sem a virgula par o separador
         saida = add_line_json(saida, atributos[i+1], list_line[i+1])
         saida = saida[0:len(saida)-2] +  "\n  },\n"
         
      cab=False
      json = json + saida
      
   json = '[\n' + json[0:len(json)-2] + '\n]' 
   #print(json)
   arq.close()
   arq = open(os.path.join(DIR, arquivo.split('.')[0]+'.json'), 'w', encoding='UTF-8' )
   arq.write(json)
   arq.close()
#
def json2csv(DIR, arquivo):
   print("----> JSON to CSV\n")
   arq = open(os.path.join(DIR, arquivo), 'r', encoding='UTF-8')
   #cod_pagina= (arq.encoding)
   #arq.close()
   #arq = open(os.path.join(DIR, arquivo), 'r', encoding = cod_pagina)
   csv=''
   entrada_json=''
   linhas = arq.readlines()
   for linha in linhas:
      entrada_json+=linha
   
   arq.close()
   dados_json = json.loads(entrada_json)
   
   for coluna in dados_json[0].keys():
      csv += '"'+ coluna +'";'
   csv=csv[0:len(csv)-1]+"\n" 
   
   for linha in range(0,len(dados_json)):
      #print(linha, (dados_json[linha].keys()))
      for coluna in dados_json[linha].keys():
        #print('dado -->', dados_json[linha][coluna])
        if str(dados_json[linha][coluna]).isnumeric():
            csv += str(dados_json[linha][coluna]) +';'
        else:
            csv += '"'+ str(dados_json[linha][coluna]) +'";'
      csv=csv[0:len(csv)-1] +"\n" 
   #print(csv)
   #
   arq = open(os.path.join(DIR, arquivo.split('.')[0]+'.csv'), 'w', encoding='UTF-8')
   arq.write(csv)
   arq.close()

#

#
logging.basicConfig(
   level='DEBUG', format="'%(asctime)s - %(name)s - %(levelname)s - %(message)s'"  
)
logger = logging.getLogger(__name__)   
@click.command()
#
def converter(Input: str = "./", Output: str="./", delimiter:str=",", prefix: str=None):
   print(Input)
   
   DIR="D:/files/"
   #name ='Judicial.csv'
   name ='Judicial.json'
   path=os.path.join(DIR, name)
   cont_arq = (len([name for name in os.listdir(DIR) if os.path.isfile(os.path.join(DIR, name))]))

   if os.path.isfile(os.path.join(DIR, name)):#trata um arquivo isoladamente
      print("é arquivo isolado:") 
      arquivos= [name] 
      
      if arquivos[0].split('.')[1].upper()=='csv'.upper(): #teste se a entrada é CSV
         csv2json(DIR, arquivos[0])   #csv2json()
      elif arquivos[0].split('.')[1].upper()=='json'.upper(): #teste se a entrada é Json
         json2csv(DIR, arquivos[0])      
   #
   else: #trata vário arquivos simultaneos
      print("São arquivos multiplos:")
      arquivos = [name for name in os.listdir(DIR) if os.path.isfile(os.path.join(DIR, name))]
      for cont in range(0, cont_arq):
         if arquivos[cont].split('.')[1].upper()=='csv'.upper(): #teste se a entrada é CSV
            csv2json(DIR, arquivos[cont])   #csv2json()
         elif arquivos[cont].split('.')[1].upper()=='json'.upper(): #teste se a entrada é Json
            json2csv(DIR, arquivos[cont])
            continue
         else:
            continue    #comando caso o arquivo não for .csv ou .json
         
      #print(arquivos)
      
if __name__ == '__main__':
#   
   for param in sys.argv :
      print(param)
      print('::',__name__,'::')
#converter()
   