<h1>json_teste.py</h1>

Programa para teste de contabilização utilizando webservices com REST API.

Suporta as consultas e retornos previstos na interface de contabilização padrão.

Para executar, sincronize todos os arquivos, execute:

python3 json_teste.py

É necessário ter o Python 3 instalado, e também os módulos que constam nos inserts.

O json_teste.py levanta um servidor web na porta 8081, pronto para receber requisições HTTP.

Para criação das chaves JWT foi utilizado o módulo PyJWT. O Flask tem, entretanto, um módulo JWT integrado, chamado Flask-JWT. Pode ser que o uso do Flask-JWT seja mais prático, porém isso não foi testado.

Abaixo estão exemplos de consultas, utilizando o httpie como cliente, e os arquivos de JSON de exemplo. Pode consultar pode ser utilizado qualquer navegador de Internet ou biblioteca que suporte requisições HTTP.
 
Obtenção de token:
http POST http://127.0.0.1:8081/api/auth < exemplo_autenticacao.json
 
Os dados de autenticação para obtenção do token estão no arquivo INI
 
Antes de executar os processos abaixo, é necessário obter o token e colocá-lo no campo access_token dos arquivos de exemplo

Consulta de lotes disponíveis para contabilização
http POST http://127.0.0.1:8081/api/contab < exemplo_consulta_lotes.json
 
Contabilização de um determinado lote:
http POST http://127.0.0.1:8081/api/contab < exemplo_contab.json
