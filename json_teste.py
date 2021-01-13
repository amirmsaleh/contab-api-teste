#! /usr/bin/python3

# Programa para teste de contabilização utilizando webservices com REST API
#
# Suporta as consultas e retornos previstos na interface de contabilização padrão
#
# Levanta um servidor web na porta 8081, pronto para receber requisições HTTP
#
# Para criação das chaves JWT foi utilizado o módulo PyJWT
# O Flask tem, entretanto, um módulo JWT integrado, chamado Flask-JWT.
# Pode ser que o uso do Flask-JWT seja mais prático, porém isso não foi testado.
#
# Abaixo estão exemplos de consultas, utilizando o httpie como cliente, e os arquivos de JSON de exemplo.
# 
# Obtenção de token:
# http POST http://127.0.0.1:8081/api/auth < exemplo_autenticacao.json
# 
# Os dados de autenticação para obtenção do token estão no arquivo INI
# 
# Antes de executar os processos abaixo, é necessário obter o token e colocá-lo no campo access_token dos arquivos de exemplo
#
# Consulta de lotes disponíveis para contabilização
# http POST http://127.0.0.1:8081/api/contab < exemplo_consulta_lotes.json
# 
# Contabilização de um determinado lote:
# http POST http://127.0.0.1:8081/api/contab < exemplo_contab.json
#

import json, jwt, time, configparser
from flask import Flask, request
from flask_restful import Resource, Api, reqparse
# O arquivo json_teste_dados tem subrotinas para simular buscas em bancos de dados
import json_teste_dados

# Caminho do arquivo de configurações
# 
arqini = './json_teste.ini'

# Aquivo INI
ini = configparser.ConfigParser()
ini.read(arqini)

#########
# A FAZER
# Colocar os dados de payload, chave e duração do token no arquivo INI de configuração

# Dados para o payload
issuer = "acme.intra"
# Duração do token em segundos
duracao = 86400
# Chave utilizada na criação do token, utilizando o HS256
chave = "ebac816cf02104b7a38ab42c3b9a2e5a"

# Inicia o Flask
app = Flask(__name__)
api = Api(app)




@app.route('/api/auth', methods=['POST'])
def create_token():
    if request.is_json:
        conteudo = request.get_json()
        # print (conteudo)
        username = conteudo.get("username")
        password = conteudo.get("password")
        bdados = conteudo.get("base")
        print ("Username:",username,"Password:",password,"Base:",bdados)
        
        # Verifica autenticação utilizando dados do arquivo INI
        if (username and password and ini[username]["bdados"] == bdados and ini[username]["password"] == password):
            hora = int(time.time())
            
            # Payload para o access_token
            payload = {
                "iss": issuer,
                "iat": hora,
                "exp": hora + duracao,
                "sub": bdados,              # Utiliza o campo "sub" do payload para armazenar o nome da base de dados
                "username": username
            }
            
            # Payload para o refresh_token
            payload_refresh = {
                "iss": issuer,
                "iat": hora,
                "exp": hora + (2*duracao), # O refresh_token tem o dobro da duração do access token
                "sub": bdados,
                "username": username
            }
            print ("Payload:",payload,"\nRefresh payload:",payload_refresh)
            
            #########
            # A FAZER
            # Testar também o funcionamento do algoritmo RS256 (RSA), de chaves assimétricas

            # Gera o token através da biblioteca jwt e algoritmo HS256
            token_bytes= jwt.encode(payload, chave, algorithm='HS256')
            # O token é gerado como uma série de bytes, e deve ser convertido em caracteres
            token = token_bytes.decode('UTF-8')
            # O mesmo para o refresh token
            token_bytes_refresh= jwt.encode(payload_refresh, chave, algorithm='HS256')
            token_refresh = token_bytes_refresh.decode('UTF-8')
            # print ("Token:",token,"\nRefresh token:",token_refresh)
            saida = {"access_token": token, "refresh_token": token_refresh}
            # print ("Saida JSON:",json.dumps(saida))
            
            # Retorna os token com o código 200 HTTP em caso de sucesso
            return app.response_class(response=json.dumps(saida), mimetype='application/json'),200
       
        else:
            
            # Retorna vazio com o código 401 HTTP em caso de falha na autenticação
            return app.response_class(response=json.dumps({}), mimetype='application/json'),401

# CONTABILIZAÇÃO
@app.route('/api/contab', methods=['POST'])
def contab():
    # Se a entrada não for JSON, retorna erro
    if not request.is_json:
        return app.response_class(response=json.dumps({"erro": "Erro no formato JSON"}), mimetype='application/json'),401 
        
    conteudo = request.get_json()
    token = conteudo.get("access_token")
    processo = conteudo.get("processo")
    
    # Consulta se o token é válido
    resultado_token, cod_token, dados_token = verifica_token(token)
    print (resultado_token, cod_token, dados_token)
    
    # Caso o token não seja válido retorna erro
    if cod_token != 200:
        return app.response_class(response=json.dumps(resultado_token), mimetype='application/json'),cod_token   
    
    print ("Payload do token:",dados_token,"Processo:",processo)
    
    # Estabelece que o banco de dados é que está no campo sub do payload
    bdados = dados_token["sub"]
    
    # Consulta lotes disponíveis
    if processo == "consulta_lotes":
        dinicial = conteudo.get("dinicial")
        dfinal = conteudo.get("dfinal")
        try:
            empresa = conteudo.get("empresa")
        except:
            empresa = ""
        lista_lotes = json_teste_dados.consulta_lotes(bdados,dinicial,dfinal,empresa)
        return app.response_class(response=json.dumps(lista_lotes), mimetype='application/json')
    
    # Contabiliza um determinado lote
    if processo == "contab":
        nlote = conteudo.get("lote")
        dcontab = json_teste_dados.contab(nlote)
        return app.response_class(response=json.dumps(dcontab), mimetype='application/json')
        
    #########
    # A FAZER
    # Implementar os demais processos de contabilização:
    # consulta_adiant
    # contab_adiant
    # consulta_faturas
    # contab_fatura
    
# RH e centros de custos
@app.route('/api/rhcc', methods=['POST'])
def rhcc():
    #########
    # A FAZER
    # Implementar os processos de integração de RH/centros de custos
    # cadcc
    # cadfunc
    rhcc = []
    return app.response_class(response=json.dumps(drhcc), mimetype='application/json')  
                    
def verifica_token(token):
    dados = ""
    try:
        dados = jwt.decode(token,chave,algorithms="HS256")
        return_data = {
            "error": "0",
            "message": "Token OK"
            }
        cod = 200
    except jwt.exceptions.ExpiredSignatureError:
        return_data = {
            "error": "1",
            "message": "Token expirado"
            }
        cod = 401
    except Exception as e:
        return_data = {
            "error" : "3",
            "message" : "Erro no uso do token"
            }
        cod = 400
    except:
        return_data = {
            "error": "2",
            "message": "Token invalido"
        }
        cod = 400            
    return return_data, cod, dados

if __name__ == '__main__':
    # Executa aplicação Flask com debug ativado
    # app.run(host='0.0.0.0', port= 8081, debug=True)  
    # Executa aplicação Flask com debug desativado
    app.run(host='0.0.0.0', port= 8081)


##########################################################
# Métodos HTTP
# GET		Obter os dados de um recurso.
# POST	Criar um novo recurso.
# PUT		Substituir os dados de um determinado recurso.
# PATCH	Atualizar parcialmente um determinado recurso.
# DELETE	Excluir um determinado recurso.
#    
# Códigos HTTP
# Código	Descrição				Quando utilizar
# 200		OK						Em requisições GET, PUT e DELETE executadas com sucesso.
# 201		Created					Em requisições POST, quando um novo recurso é criado com sucesso.
# 206		Partial 				Content	Em requisições GET que devolvem apenas uma parte do conteúdo de um recurso.
# 302		Found					Em requisições feitas à URIs antigas, que foram alteradas.
# 400		Bad Request				Em requisições cujas informações enviadas pelo cliente sejam invalidas.
# 401		Unauthorized			Em requisições que exigem autenticação, mas seus dados não foram fornecidos.
# 403		Forbidden				Em requisições que o cliente não tem permissão de acesso ao recurso solicitado.
# 404		Not Found				Em requisições cuja URI de um determinado recurso seja inválida.
# 405		Method Not Allowed		Em requisições cujo método HTTP indicado pelo cliente não seja suportado.
# 406		Not Acceptable			Em requisições cujo formato da representação do recurso requisitado pelo cliente não seja suportado.
# 415		Unsupported Media Type	Em requisições cujo formato da representação do recurso enviado pelo cliente não seja suportado.
# 429		Too Many Requests		No caso do serviço ter um limite de requisições que pode ser feita por um cliente, e ele já tiver sido atingido.
# 500		Internal Server Error	Em requisições onde um erro tenha ocorrido no servidor.
# 503		Service Unavailable		Em requisições feitas a um serviço que esta fora do ar, para manutenção ou sobrecarga.
    
    
    
    



