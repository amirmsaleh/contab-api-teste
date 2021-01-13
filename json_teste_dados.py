#! /usr/bin/python3

# Subrotinas para simular buscas em bancos de dados
# Deve ser utilizado em conjunto com o json_teste.py

import json

# Consulta lotes disponíveis para contabilização
def consulta_lotes(bdados,dinicial,dfinal,empresa):
    dempresa = {
        "7171": {
            "empresa": "7171", 
            "lotes": ["238", "892", "893", "087", "402"]
            },
        "8181": {
            "empresa": "8181",
            "lotes": ["382", "839", "592"]
            },
        "9191": {
            "empresa": "9191",
            "lotes": ["832"]
            }
    }
    
    if bdados != "acme":
        return {}
    
    if empresa == "7171" or empresa == "8181" or empresa == "9191":
        return dempresa[empresa]
    elif not empresa:
        return [dempresa["7171"],dempresa["8181"],dempresa["9191"]]
    else:
        return {}
# print (json.dumps(consulta_lotes("acme","2020-08-10","2020-09-10",""), indent =3))

# Contabilização
# Exemplo para lote 382
def contab(nlote):
    if (nlote == "382"):
        # Observações
        # 1. Há casos em que uma mesma despesa pode estar associada a mais de um adiantamento. Nesse caso, será feita a divisão da despesa em duas. Uma associada a um adiantamento e a outra associada a outro.
        # 2. Há casos em que parte de uma despesa estará associada a um adiantamento e outra parte a nenhum. Essa parte que não está associada a nenhum adiantamento deverá ser objeto de reembolso. Nesse caso, a despesa também será dividida em duas.
        # 3. Despesas em dinheiro que não tenham adiantamento associado deverão ser objeto de reembolso.
        
        # Despesa em dinheiro, com adiantamento associado
        despesa1 = {
            "tipo": "dinheiro",      # Pode ser "dinheiro" ou "cartao"
            "ccontabil": "5324",     # conta contábil referente a cada despesa
            "valor": 100,            # Valor da despesa
            "moeda": "BRL",          # Código da moeda de acordo com a ISO4217 
            "ddesp": "20200721",   # data da despesa
            "nadiant": "32892",      # número do adiantamento associado (se houver) se não houver número de adiantamento associado, e o tipo for "dinheiro" é necessário fazer reembolso ao funcionário
            "reembolso": False,      # indica se é ou não reembolso
            "ccustos": "3892928",    # centro de custos associado à despesa
            "subcod": "3423"         # subcódigo que consta no cadastro de centro de custos
        }
        
        # Despesa em dinheiro sem adiantamento associado
        despesa2 = {
            "tipo": "dinheiro",
            "ccontabil": "5324",
            "valor": 47.52,
            "moeda": "BRL",
            "ddesp": "20200722",
            "reembolso": True,
            "ccustos": "3892928",
            "subcod": "3423"
        }
        
        # Devolução de valor para a companhia (despesa negativa em dinheiro)
        # Centro de custos sem subcódigo
        despesa3 = {
            "tipo": "dinheiro",
            "ccontabil": "8372",
            "valor": -80.5,
            "moeda": "BRL",
            "ddesp": "20200723",
            "reembolso": False,
            "ccustos": "439283"
        }
        
        # Despesa cartão de crédito ou outro meio de pagamento eletrônico
        despesa4 = {
            "tipo": "cartao",
            "ccontabil": "5324",
            "valor": 147.32,
            "moeda": "BRL",
            "ddesp": "20200711",
            "corte": 37,             # Número do corte do cartão de crédito - apenas para meios de pagamento eletrônicos 
            "ccustos": "3892928",
            "subcod": "3423"
        }
        
        # Reembolso no cartão de crédito (despesa negativa no cartão)
        despesa5 = {
            "tipo": "cartao",
            "ccontabil": "5324",
            "valor": -237.47,
            "moeda": "BRL",
            "ddesp": "20200712",
            "corte": 37,
            "ccustos": "3892928",
            "subcod": "3423"
        }
        
        despesas_r1 = (despesa1, despesa2, despesa5)
        despesas_r2 = (despesa3, despesa4)
        
        relatorio1 = {
            "nrelat": "23870001",     # número do relatório de despesas
            "drelat": "20200727",   # data do relatório de despesas
            "cpf": "28392089940",     # CPF do funcinário
            "matricula": "9382",      # campo legajo do funcionário, no Dinnero
            "nome": "João da Silva",  # Nome do funcionário
            "despesas": despesas_r1
        }
        
        relatorio2 = {
            "nrelat": "73620001",
            "drelat": "20201027",
            "cpf": "13843767930",
            "matricula": "9295",
            "nome": "Francisco José dos Santos",
            "despesas": despesas_r2
        }
        
        relatorios = (relatorio1, relatorio2)
        
        dados_lote = {
            "cnpj": "8293049288392", # CPNJ da empresa cadastrado no Dinnero
            "empresa": "3829",       # código da empresa no Dinnero
            "nlote": "382",          # número do lote
            "dlote": "20200828",   # Data da contabilização
            "dinicio": "20200727", # menor data de prestação de contas dentro do lote
            "dfinal": "20200827",  # maior data de prestação de contas dentro do lote
            "qrelat": 4,             # quantidade de relatórios de despesas no lote
            "qregistros": 20,        # quantidade de registros de despesas (dinheiro ou cartão) presentes na contabilização
            "relatorios": relatorios
        }
        
        lote = {"lote": dados_lote}
    else:
        lote = {"lote": "Inexistente"}
    return (lote)
# print (json.dumps(contab(382), indent = 3))

# Consulta adiantamentos disponíveis para contabilização
def consulta_adiant(bdados,dinicial,dfinal,empresa):
    dempresa = {
        "7171": {
            "empresa": "7171", 
            "lotes": ["124","287","110","134","177"]
            },
        "8181": {
            "empresa": "8181",
            "lotes": ["221","321","121"]
            },
        "9191": {
            "empresa": "9191",
            "lotes": ["144"]
            }
    }
    
    if bdados != "acme":
        return {}
    
    if empresa == "7171" or empresa == "8181" or empresa == "9191":
        return dempresa[empresa]
    elif not empresa:
        return [dempresa["7171"],dempresa["8181"],dempresa["9191"]]
    else:
        return {}
#print (json.dumps(consulta_adiant("acme","2020-08-10","2020-09-10","7171"), indent =3))

# Adiantamento
# Exemplo para o adiantamento 121
def contab_adiant(nadiant):
    if (nadiant == "121"):
        dados_adiant = {
            "cnpj": "8293049288392",  # CPNJ da empresa cadastrado no Dinnero
            "empresa": "7171",        # código da empresa no Dinnero
            "nadiant": "121",         # número do adiantamento
            "dadiant": "20200828",    # data da solicitação do adiantamento
            "dpago": "20200901",      # data do pagamento do adiantamento
            "cpf": "28392089940",     # CPF do funcinário (se houver)
            "matricula": "9382",      # campo legajo do funcionário, no Dinnero
            "nome": "João da Silva",  # Nome do funcionário
            "valor": 500.00,          # Valor do adiantamento
            "ccustos": "3892928",     # centro de custos associado à despesa
            "subcod": "3423"          # subcódigo que consta no cadastro de centro de custos (se houver)
        }
        adiant = dados_adiant
    else:
        adiant = ["Inexistente"]
    return (adiant)
#print (json.dumps(contab_adiant("121"), indent = 3))  

def contab_fatura(ncorte):
    if (ncorte == "37"):
        ccusto1 = {
            "valor": 33794.23,       # somatório por centro de custo
            "ccustos": "3892928",     # centro de custos associado à despesa
            "subcod": "3423"          # subcódigo que consta no cadastro de centro de custos (se houver)            
        }
        ccusto2 = {
            "valor": 87234.21,
            "ccustos": "3928272",
            "subcod": "3927"
        }
        ccusto3 = {
            "valor": 126294.93,
            "ccustos": "9382729",
            "subcod": "8276"
        }

        divcc = (ccusto1, ccusto2, ccusto3)

        dados_corte = {
            "cnpj": "8293049288392",  # CPNJ da empresa cadastrado no Dinnero
            "empresa": "7171",        # código da empresa no Dinnero
            "operadora": "???",       # identificação da operadora do meio de pagamento
            "ncorte": "37",           # número do corte
            "dcorte": "20200828",     # data do corte
            "vtotal": 247323.37,      # valor total da fatura
            "moeda": "BRL",           # moeda
            "divcc": divcc            # divição por centros de custos
        }
        fatura = dados_corte
    else:
        fatura = ["Inexistente"]
    return (fatura)
#print (json.dumps(contab_fatura("37"), indent = 3))  


def ccustos():
    ccusto1 = {
        "ccustos": "392802",
        "subcod": "0927",
        "descricao": "Fábrica 1",
        "ativo": True,
        "empresa": "9191"
    }  
    ccusto2 = {
        "ccustos": "389282",
        "subcod": "3982",
        "descricao": "Fábrica 2",
        "ativo": True,
        "empresa": "9191"
    }  

    ccustos = (ccusto1, ccusto2)

    cadcc = {
        "processo": "cadcc",
        "access_token": "eyJ0eXAiOiJKV1Q...CGKJlRZwjeuX0E-xg",
        "ccustos": ccustos
    }
    
    return (cadcc)
#print (json.dumps(ccustos(), indent = 3))  

def funcionarios():
    funcionario1 = {
        "matricula": "284738278",
        "login": "jsilva",
        "cpf": "28473827840",
        "nome": "José da Silva",
        "empresa": "9191",
        "email": "jsilva@acme.com",
        "ccusto": "938202",
        "superior": "214513784",
        "desligamento": "20200817"
    }
    funcionario2 = {
        "matricula": "214513784",
        "login": "jsilva",
        "cpf": "21451378440",
        "nome": "João dos Santos",
        "empresa": "9191",
        "email": "jsantos@acme.com",
        "ccusto": "392832",
        "superior": "138429428"
    }    

    funcs = (funcionario1, funcionario2)

    funcionarios = {
        "processo": "cadfunc",
        "access_token": "eyJ0eXAiOiJKV1Q...CGKJlRZwjeuX0E-xg",
        "funcionarios": funcs
    }
    return(funcionarios)
#print (json.dumps(funcionarios(), indent = 3)) 
        






