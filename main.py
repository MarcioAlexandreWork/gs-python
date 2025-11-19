import json
import random
import os
import copy
from operator import index

import requests
from datetime import datetime
from datetime import date



# Colocar nas instruções que é necessário instalar a biblioetca playsound
def volta()->None:
    """
    Função que existe apenas para
    não ficar o tempo inteiro fazendo
    "print('Voltando')" em toda função
    :return:
    """
    a = input('Dê enter para voltar ao menu principal\n')

def get1()->dict:
    if os.path.exists('compr.json'):
        with open('compr.json', 'r') as agenda:
            dicto = json.load(agenda)
    else:
        dicto = {
            'compromissos':
                {
                 "reunioes":[],
                 "pessoais":[],
                 "tarefas":[]
             }
        }
    return dicto



def get2()->dict:
    pass
#     """
#     API do linkedin para trabalhos
#     utilizar apenas quando outilizar o código de forma oficial
#     tentar não usar em testes para não esgotar o limite de gets
#     :return:
#     """
#     url = "https://linkedin-job-search-api.p.rapidapi.com/active-jb-24h"
#     querystring = {"limit": "10", "offset": "0", "title_filter": "\"Data Engineer\"",
#                    "location_filter": "\"United States\" OR \"United Kingdom\"", "description_type": "text"}
#     headers = {
#         "x-rapidapi-key": "ea8d1789cemsh1b0e493bbf3e38cp116f87jsncbd8e51146a2",
#         "x-rapidapi-host": "linkedin-job-search-api.p.rapidapi.com"
#     }
#     return requests.get(url, headers=headers, params=querystring)




def get3():
    """
    Decoy de empresas
    utilizado API constante sem updates
    usado só quando a API atualizável está dando código 4XX ou 3XX
    :return:
    """
    return requests.get("https://raw.githubusercontent.com/MarcioAlexandreWork/API-minhas--faculdade-/refs/heads/main/empresas.json") # Repositório pessoal contendo a API
        # Essa função deverá ser usada apenas se o local de request de API não estiver mais aceitando request já que ele possui um número de requests limitado por mês
        # essa função também é utilizada para testes com a API, para que eu não fique dando toda hora requests acabando com o limite que eu tenho por mês, assim entregando um produto final mais completo e sem falhas

def getvagas()->list:
    """
    Função para leitura de info
    dentro do arquivo empresas.json
    e fazer um return delas
    :return:
    """
    if os.path.exists('empresas.json.'):
        with open('empresas.json', 'r') as f:
            dicto = json.load(f)
    else:
        dicto = []
    return dicto


def act1() ->None:
    """
    Agendamento de compromissos
    recebe nenhum valor como parâmetro e retorna nada
    tudo é feito dentro da função
    :return:
    """
    dicto = get1()
    try:
        categ = int(input('De que categoria o seu agendamento é?\n1-Reunião\n2-Pessoal\n3-Tarefa\nCaso nenhuma, apenas tecle qualquer coisa\n'))
    except ValueError:
        categ = 0
        print('Erro na escolha de categoria\nEscolha apenas números INTEIROS\nCaso o erro persista, tente contato com a nossa empresa\n')
    if categ == 1:
        categ = "reunioes"
    elif categ == 2:
        categ = "pessoais"
    elif categ == 3:
        categ = "tarefas"

    if categ=='reunioes' or categ=='pessoais': # Reuniões e pessoais tem estruturas identicas, a unica coisa que muda é a categoria
                                               # Isso é feito apenas pela organização, já que os arquivos JSON são um só
        try:
            tipo = int(input("Qual é o tipo de reunião?\n1-Online\n2-Presencial"))
        except ValueError: #Tornando os valores nulos para que o usuário não tenha que fazer toda a operação novamente
            tipo = None
            link = None
            local = None
            print("Erro: Você colocou algum valor não inteiro\nPor isso o tipo, link e local serão considerados nulos\nArrume isso depois na opção 3 dos agendamentos\n")
        if tipo == 1:
            tipo = "online"
            link = input('Cole aqui o link da reunião: ')
            local = None
        elif tipo == 2:
            tipo = "presencial"
            link = None
            local = input("Cole aqui o endereço do local da reunião: ")
        else:
            print('Você colocou algum valor que está fora das opções\nAssim valores como tipo, link e local serão nulos\nArrume-os depois na opção 3')
            tipo = None
            link = None
            local = None
        assunto = input('Qual é o assunto da reunião?')
        try:
            corrigir = False
            DD = int(input('Qual o dia da reunião?\nEX: 17\n'))
            MM = int(input('Qual o mês da reuniao?\nEX: 11\n'))
            AAAA = int(input('Qual é o ano da reuniao?\nEX: 2025\n'))
            horas = int(input('Qual é a hora da ruenião?\nXX:MM\n'))
            min = int(input('Quais são os minutos da reunião?\nHH:XX\n'))

            if DD<=9: #Operações no
                DD = "0"+str(DD)
            if MM<=9:
                MM = "0"+str(MM)

            if horas<=9:
                horas = "0"+str(horas)
            if min<=9:
                min = "0"+str(min)

            horario = f'{horas}:{min}'
            data = f"{AAAA}-{MM}-{DD}"
        except ValueError:
            print('Erro: Você colocou um número não inteiro\nDia de reunião e horário serão colocados para hoje e agora\nEdite depois na opção 3 do menu\n')
            data = str(date.today())
            horario = str(datetime.now().time())[0:5]

        if data==str(date.today()): #Checar se a reunião já ocorreu ou não, mesmo que possa ser inutil para cosias como agendamento de eventos futuros, o usuário pode usar para o assunto da reunião anterior ou só para registro mesmo
            if horario<f'{str(datetime.now().hour)}:{str(datetime.now().minute)}':
                ocorreu = True
            else:
                ocorreu = False
        else:
            ocorreu = True
        a = input(f'Categoria: {categ}\nTipo: {tipo}\nAssunto: {assunto}\nLink: {link}\nLocal: {local}\nData: {data}\nHorario: {horario}\n\nAs informações estão corretas?\nCaso não, digite "SAIR" para voltar o menu principal\n')
        if not a.upper() == 'SAIR':
            if not dicto['compromissos'][categ]==[]:
                while True:
                    exists = False
                    b = str(random.randint(1000,9999))
                    for i in dicto['compromissos'][categ]:
                        if b in i["id"]:
                            exists = True
                    if not exists:
                        iden = b
                        break
            else:
                b = str(random.randint(1000, 9999))
                iden = b
            reuniao={
                "id": iden,
                "tipo": tipo,
                "assunto": assunto,
                "link": link,
                "local": local,
                "data": data,
                "horario": horario,
                "dia_de_criacao": str(date.today()),
                "ultima_edicao": {
                  "dia": None,
                  "ultimo_item_modificado": None
                },
                "ocorreu": ocorreu
            }
            dicto['compromissos'][categ].append(reuniao)
            print(f'Aqui está o ID do compromisso: {iden}')
            with open('compr.json','w') as f:
                json.dump(dicto, f, indent=3)

    elif categ=='tarefas':
        tarefa = input('Qual é a tarefa a ser realizada?')
        observacoes = input('Alguma observação sobre a tarefa a ser realizada?')
        objetivo_atual = input('Algum objetivo atual?\nEX: Colocar comentários // Arrumar erros // Adicionar uma terceira função\n')
        try:
            DD = int(input('Até que dia você tem que fazer essa tarefa?\nEX: 17\n'))
            MM = int(input('Até que mês você tem que fazer essa tarefa?\nEX: 11\n'))
            AAAA = int(input('Até que ano você tem que fazer essa tarefa?\nEX: 2025\n'))
            horas = int(input('Até que horas você tem que fazer essa tarefa?\nXX:MM\n'))
            min = int(input('E quais são os minutos limite da tarefa?\nHH:XX\n'))

            if DD<=9: #Operações no
                DD = "0"+str(DD)
            if MM<=9:
                MM = "0"+str(MM)

            if horas<=9:
                horas = "0"+str(horas)

            if min<=9:
                min = "0"+str(min)

            horario = f'{horas}:{min}'
            deadline = f"{AAAA}-{MM}-{DD}"
        except ValueError:
            print('Erro: Você colocou um número não inteiro\nDia de reunião e horário serão colocados para hoje e agora\nEdite depois na opção 3 do menu\n')
            deadline = str(date.today())
            horario = str(datetime.today().time())[0:5]



        if deadline==str(date.today()): #Checar se a reunião já ocorreu ou não, mesmo que possa ser inutil para cosias como agendamento de eventos futuros, o usuário pode usar para o assunto da reunião anterior ou só para registro mesmo
            if horario<f'{str(datetime.now().hour)}:{str(datetime.now().minute)}':
                ocorreu = True
            else:
                ocorreu = False
        elif deadline<str(datetime.today()):
            ocorreu = True
        else:
            ocorreu = False
        a = input(f'Categoria: {categ}\nTarefa: {tarefa}\nObservações: {observacoes}\nObjetivo atual: {objetivo_atual}\nData limite: {deadline}\nTempo limite: {horario}\n\nAs informações estão corretas?\nCaso não, digite "SAIR" para voltar o menu principal\n')
        if not a.upper() == 'SAIR':
            if not dicto['compromissos']['tarefas']==[]:
                while True:
                    exists = False
                    b = str(random.randint(1000,9999))
                    for i in dicto['compromissos'][categ]:
                        if b in i["id"]:
                            exists = True
                    if not exists:
                        iden = b
                        break
            else:
                b = str(random.randint(1000, 9999))
                iden = b
            tarefa={
                "id": iden,
                "tarefa": tarefa,
                "observacoes": observacoes,
                "objetivo_atual": objetivo_atual,
                "deadline": deadline,
                "horario": horario,
                "dia_de_criacao": str(date.today()),
                "ultima_edicao": {
                  "dia": None,
                  "ultimo_item_modificado": None
                },
                "ocorreu": ocorreu
            }

            dicto['compromissos']['tarefas'].append(tarefa)
            print(f'Agendamento salvo!\nAqui está o ID da tarefa: {iden}')
            with open('compr.json','w') as f:
                json.dump(dicto, f, indent=3)

    volta()

def act2() ->None:
    """
    Exclusão de agendamentos
    recebe nenhum valor como parâmetro e retorna nada
    tudo é feito dentro da função
    :return:
    """
    dicto = get1()
    exists = False

    try:
        categ = int(input('Qual é a categoria do agendamento que você deseja deletar?\n1 - Reunioes\n2 - Pessoal\n3 - Tarefas\n'))
        id = int(input('Qual é o ID do compromisso que deseja deletar\n'))
        if categ == 1:
            categ = 'reunioes'
        elif categ == 2:
            categ = 'pessoais'
        elif categ == 3:
            categ = 'tarefas'
        else:
            print('Não temos essa opção')
        if categ in dicto['compromissos']:
            for i in dicto['compromissos'][categ]:
                if i['id'] == str(id):
                    exists = True
                    agendamento = i

            if not exists:
                print(
                    'Esse agendamento não existe, tem certeza que ele está na categoria correta? Ou se ele ao menos existe?')
            else:
                if categ == 'reunioes' or categ == 'pessoais':
                    print(
                        f'Categoria: {categ}\nTipo: {agendamento['tipo']}\nAssunto: {agendamento['assunto']}\nLink: {agendamento['link']}\nLocal: {agendamento['local']}\nData: {agendamento['data']}\nHorario: {agendamento['horario']}\nDia de criação: {agendamento['dia_de_criacao']}\nSe Ocorreu: {agendamento['ocorreu']}\nUltima edição: {agendamento['ultima_edicao']['dia']}\nUltimo item editado: {agendamento['ultima_edicao']['ultimo_item_modificado']}\n\n')
                elif categ == 'tarefas':
                    print(
                        f'Categoria: {categ}\nTarefa: {agendamento['tarefa']}\nObservacoes: {agendamento['observacoes']}\nObjetivo atual: {agendamento['objetivo_atual']}\nDeadline: {agendamento['deadline']}\nHorario: {agendamento['horario']}\nDia de criação: {agendamento['dia_de_criacao']}\nSe Ocorreu: {agendamento['ocorreu']}\nUltima edição: {agendamento['ultima_edicao']['dia']}\nUltimo item editado: {agendamento['ultima_edicao']['ultimo_item_modificado']}\n\n')

                deletar = input('Você tem CERTEZA que quer deletar esse agendamento? Se sim, digite "DELETAR"\n')
                if deletar.upper() == 'DELETAR':
                    dicto['compromissos'][categ].remove(agendamento)
                    print('Deletado.')
                    with open('compr.json', 'w') as f:
                        json.dump(dicto, f, indent=3)
                else:
                    print('Operação cancelada')
    except ValueError:
        print('Números inteiros apenas')
    volta()

def act3() ->None:
    """
    Edita agendamentos
    recebe nenhum valor como parâmetro e retorna nada
    tudo é feito dentro da função
    :return:
    """
    dicto = get1()
    try:
        categ = int(input('Diga a categoria do agendamento que você deseja editar\n1-Reuniões\n2-Pessoais\n3-Tarefas\n'))
    except ValueError:
        categ = 0
        print('Número inteiros apenas')
    if categ==1:
        categ = 'reunioes'
    elif categ==2:
        categ = 'pessoais'
    elif categ==3:
        categ = 'tarefas'
    else:
        print('Essa categoria não existe')

    if categ == 'reunioes' or categ == 'pessoais' or categ == 'tarefas':
        identi = input('Qual é o ID do agendamento?\nVerifique na opção 5 do menu caso não saiba e busque pelo ID\n')
        exists = False
        ind = 0
        for i in dicto['compromissos'][categ]:
            if i['id'] == str(identi):
                exists = True
                agendamento = i
                antigo = agendamento.copy()
                break
            ind+=1
        if not exists:
            print('Esse ID não existe ou você o colocou de forma errada\n')
        else:
             #Criação de um arquivo antigo só para comparar depois e saber qual foi a ultima edição e que item foi modificado
            if categ=='reunioes':
                while True:
                    print(f'Categoria: {categ}\nTipo: {agendamento['tipo']}\nAssunto: {agendamento['assunto']}\nLink: {agendamento['link']}\nLocal: {agendamento['local']}\nData: {agendamento['data']}\nHorario: {agendamento['horario']}\nDia de criação: {agendamento['dia_de_criacao']}\nSe Ocorreu: {agendamento['ocorreu']}\nUltima edição: {agendamento['ultima_edicao']['dia']}\nUltimo item editado: {agendamento['ultima_edicao']['ultimo_item_modificado']}\n\n')
                    editar = input('\nQue informação você quer editar?\n1-Tipo\n2-Assunto\n3-Link\n4-Local\n5-Data\n6-Horario\n7-Ocorrência\n\nSe quer parar de editar, tecle "SAIR" e dê enter')
                    if editar=='1':
                        print(f'Tipo atual: {agendamento['tipo']}')
                        a = input('Qual o tipo novo?\n1-Online\n2-Presencial\n')
                        if a=='1':
                            agendamento['tipo'] = 'online'
                        elif a=='2':
                            agendamento['tipo'] = 'presencial'
                        else:
                            print('Essa opção não existe.')
                        if not agendamento['tipo'] == antigo['tipo']:
                            agendamento['ultima_edicao']['ultimo_item_modificado']="Tipo"

                    elif editar=='2':
                        print(f'Assunto atual: {agendamento['assunto']}')
                        a = input('Qual o novo assunto?')
                        agendamento['assunto'] = a
                        if not agendamento['tipo'] == antigo['tipo']:
                            agendamento['ultima_edicao']['ultimo_item_modificado']="Assunto"
                        else:
                            print('Nada foi editado')
                    elif editar=='3':
                        print(f'Link atual: {agendamento['link']}')
                        a = input('Qual o novo link?\n(Coloque "None" no caso queira deixar vazio\n)')
                        if a.upper()=='NONE':
                            a=None
                        agendamento['link'] = a
                        if not agendamento['link'] == antigo['link']:
                            agendamento['ultima_edicao']['ultimo_item_modificado'] = "Link"
                        else:
                            print('Nada foi editado')
                    elif editar=='4':
                        print(f'Local atual: {agendamento['local']}')
                        a = input('Qual o local novo?\nColoque "None" caso queira deixar vazio\n')
                        if a.upper()=='NONE':
                            a=None
                        agendamento['local'] = a
                        if not agendamento['local'] == antigo['local']:
                            agendamento['ultima_edicao']['ultimo_item_modificado']="Local"
                        else:
                            print('Nada foi editado')
                    elif editar=='5':
                        print(f'Tipo atual: {agendamento['assunto']}')
                        try:
                            DD = int(input('Qual o dia do compromisso?\nEX: 17\n'))
                            MM = int(input('Qual o mês do compromisso?\nEX: 11\n'))
                            AAAA = int(input('Qual o ano do compromisso?\nEX: 2025\n'))


                            if DD <= 9:
                                DD = "0" + str(DD)
                            if MM <= 9:
                                MM = "0" + str(MM)

                            data = f"{AAAA}-{MM}-{DD}"
                            agendamento['data'] = data
                            if not antigo['data'] == data:
                                agendamento['ultima_edicao']['ultimo_item_modificado'] = "Data"
                            else:
                                print('Nada foi editado')
                        except ValueError:
                            print('Números inteiros apenas por favor')

                    elif editar=='6':
                        print(f'Horário antigo: {agendamento["horario"]}')
                        try:
                            horas = int(input('Horas do compromisso?\nXX:MM\n'))
                            min = int(input('Minutos do compromisso?\nHH:XX\n'))
                            if horas <= 9:
                                horas = "0" + str(horas)
                            if min <= 9:
                                min = "0" + str(min)
                            horario = f'{horas}:{min}'
                            agendamento['horario'] = horario
                            if not antigo['horario'] == horario:
                                agendamento['ultima_edicao']['ultimo_item_modificado'] = "Horario"
                            else:
                                print('Nada foi editado')
                        except ValueError:
                            print('Número inteiros apenas por favor')

                    elif editar=='7':
                        print(f'Ocorrência atual: {agendamento['ocorreu']}')
                        a = input('Qual a nova ocorrência?\n1-Falso\n2-Verdadeiro\n')
                        if a == '1':
                            agendamento['ocorreu'] = False
                        elif a == '2':
                            agendamento['ocorreu'] = True
                        else:
                            print('Essa opção não existe.')
                        if not agendamento['ocorreu'] == antigo['ocorreu']:
                            agendamento['ultima_edicao']['ultimo_item_modificado'] = "Ocorrencia"
                        else:
                            print('Nada foi editado')

                    elif editar.upper()=='SAIR':
                        break
                    else:
                        print('Essa opção não existe')



            elif categ=='pessoais':
                while True:
                    print(antigo)
                    print(f'Categoria: {categ}\nTipo: {agendamento['tipo']}\nAssunto: {agendamento['assunto']}\nLink: {agendamento['link']}\nLocal: {agendamento['local']}\nData: {agendamento['data']}\nHorario: {agendamento['horario']}\nDia de criação: {agendamento['dia_de_criacao']}\nSe Ocorreu: {agendamento['ocorreu']}\nUltima edição: {agendamento['ultima_edicao']['dia']}\nUltimo item editado: {agendamento['ultima_edicao']['ultimo_item_modificado']}\n\n')
                    editar = input('\nQue informação você quer editar?\n1-Tipo\n2-Assunto\n3-Link\n4-Local\n5-Data\n6-Horario\n7-Ocorrência\n\nSe quer parar de editar, tecle "SAIR" e dê enter')
                    if editar=='1':
                        print(f'Tipo atual: {agendamento['tipo']}')
                        a = input('Qual o tipo novo?\n1-Online\n2-Presencial\n')
                        if a=='1':
                            agendamento['tipo'] = 'online'
                        elif a=='2':
                            agendamento['tipo'] = 'presencial'
                        else:
                            print('Essa opção não existe.')
                        if not agendamento['tipo'] == antigo['tipo']:
                            agendamento['ultima_edicao']['ultimo_item_modificado']="Tipo"

                    elif editar=='2':
                        print(f'Assunto atual: {agendamento['assunto']}')
                        a = input('Qual o novo assunto?')
                        agendamento['assunto'] = a
                        if not agendamento['tipo'] == antigo['tipo']:
                            agendamento['ultima_edicao']['ultimo_item_modificado']="Assunto"
                        else:
                            print('Nada foi editado')
                    elif editar=='3':
                        print(f'Link atual: {agendamento['link']}')
                        a = input('Qual o novo link?\n(Coloque "None" no caso queira deixar vazio\n)')
                        if a.upper()=='NONE':
                            a=None
                        agendamento['link'] = a
                        if not agendamento['link'] == antigo['link']:
                            agendamento['ultima_edicao']['ultimo_item_modificado'] = "Link"
                        else:
                            print('Nada foi editado')
                    elif editar=='4':
                        print(f'Local atual: {agendamento['local']}')
                        a = input('Qual o local novo?\nColoque "None" caso queira deixar vazio\n')
                        if a.upper()=='NONE':
                            a=None
                        agendamento['local'] = a
                        if not agendamento['local'] == antigo['local']:
                            agendamento['ultima_edicao']['ultimo_item_modificado']="Local"
                        else:
                            print('Nada foi editado')
                    elif editar=='5':
                        print(f'Tipo atual: {agendamento['assunto']}')
                        try:
                            DD = int(input('Qual o dia do compromisso?\nEX: 17\n'))
                            MM = int(input('Qual o mês do compromisso?\nEX: 11\n'))
                            AAAA = int(input('Qual o ano do compromisso?\nEX: 2025\n'))


                            if DD <= 9:
                                DD = "0" + str(DD)
                            if MM <= 9:
                                MM = "0" + str(MM)

                            data = f"{AAAA}-{MM}-{DD}"
                            agendamento['data'] = data
                            if not antigo['data'] == data:
                                agendamento['ultima_edicao']['ultimo_item_modificado'] = "Data"
                            else:
                                print('Nada foi editado')
                        except ValueError:
                            print('Números inteiros apenas por favor')

                    elif editar=='6':
                        print(f'Horário antigo: {agendamento["horario"]}')
                        try:
                            horas = int(input('Horas do compromisso?\nXX:MM\n'))
                            min = int(input('Minutos do compromisso?\nHH:XX\n'))
                            if horas <= 9:
                                horas = "0" + str(horas)
                            if min <= 9:
                                min = "0" + str(min)
                            horario = f'{horas}:{min}'
                            agendamento['horario'] = horario
                            if not antigo['horario'] == horario:
                                agendamento['ultima_edicao']['ultimo_item_modificado'] = "Horario"
                            else:
                                print('Nada foi editado')
                        except ValueError:
                            print('Número inteiros apenas por favor')

                    elif editar=='7':
                        print(f'Ocorrência atual: {agendamento['ocorreu']}')
                        a = input('Qual a nova ocorrência?\n1-Falso\n2-Verdadeiro\n')
                        if a == '1':
                            agendamento['ocorreu'] = False
                        elif a == '2':
                            agendamento['ocorreu'] = True
                        else:
                            print('Essa opção não existe.')
                        if not agendamento['ocorreu'] == antigo['ocorreu']:
                            agendamento['ultima_edicao']['ultimo_item_modificado'] = "Ocorrencia"
                        else:
                            print('Nada foi editado')

                    elif editar.upper()=='SAIR':
                        break
                    else:
                        print('Essa opção não existe')



            elif categ=='tarefas':
                while True:
                    print(f'Categoria: {categ}\nTarefa: {agendamento['tarefa']}\nObservacoes: {agendamento['observacoes']}\nObjetivo atual: {agendamento['objetivo_atual']}\nDeadline: {agendamento['deadline']}\nHorario: {agendamento['horario']}\nDia de criação: {agendamento['dia_de_criacao']}\nSe Ocorreu: {agendamento['ocorreu']}\nUltima edição: {agendamento['ultima_edicao']['dia']}\nUltimo item editado: {agendamento['ultima_edicao']['ultimo_item_modificado']}\n\n')
                    editar = input('Que informa~]ap deseja editar?\n1-Tarefa\n2-Observações\n3-Objetivo atual\n4-Deadline\n5-Horário\n6-Ocorrência\nDigite "SAIR" para parar de editar\n')

                    if editar=='1':
                        print(f'Tarefa atual: {agendamento["tarefa"]}')
                        a = input('Qual o nome da nova tarefa?\n')
                        agendamento['tarefa'] = a
                        if not agendamento['tarefa'] == antigo['tarefa']:
                            agendamento['ultima_edicao']['ultimo_item_modificado'] = "Tarefa"
                        else:
                            print('Nada foi editado.')


                    elif editar=='2':
                        print(f'Observações atuais: {agendamento["observacoes"]}')
                        a = input('Quais são as novas observações?\n(Coloque "None" caso queira deixar vazio)\n')
                        if a.upper()=='NONE':
                            a=None
                        agendamento['observacoes'] = a
                        if not antigo['observacoes'] == agendamento['observacoes']:
                            agendamento['ultima_edicao']['ultimo_item_modificado'] = "Observações"
                        else:
                            print('Nada foi editado.')


                    elif editar=='3':
                        print(f'Objetivo atual: {agendamento["objetivo_atual"]}')
                        a = input('Qual é o novo objetivo?\n')
                        if not agendamento['objetivo_atual'] == antigo['objetivo_atual']:
                            agendamento['ultima_edicao']['ultimo_item_modificado'] = "Objetivos"
                        else:
                            print('Nada foi editado')


                    elif editar=='4':
                        print(f'Deadline atual: {agendamento["deadline"]}')
                        try:
                            DD = int(input('Qual o dia limite da tarefa?\nEX: 17\n'))
                            MM = int(input('Qual o mês limite da tarefa?\nEX: 11\n'))
                            AAAA = int(input('Qual o ano limite da tarefa?\nEX: 2025\n'))

                            if DD <= 9:
                                DD = "0" + str(DD)
                            if MM <= 9:
                                MM = "0" + str(MM)

                            data = f"{AAAA}-{MM}-{DD}"
                            agendamento['deadline'] = data
                            if not antigo['deadline'] == data:
                                agendamento['ultima_edicao']['ultimo_item_modificado'] = "Deadline"
                            else:
                                print('Nada foi editado')
                        except ValueError:
                            print('Números inteiros apenas por favor')


                    elif editar=='5':
                        print(f'Horário antigo: {agendamento["horario"]}')
                        try:
                            horas = int(input('Horas limite?\nXX:MM\n'))
                            min = int(input('Minutos limite?\nHH:XX\n'))
                            if horas <= 9:
                                horas = "0" + str(horas)
                            if min <= 9:
                                min = "0" + str(min)
                            horario = f'{horas}:{min}'
                            agendamento['horario'] = horario
                            if not antigo['horario'] == horario:
                                agendamento['ultima_edicao']['ultimo_item_modificado'] = "Horario"
                            else:
                                print('Nada foi editado')
                        except ValueError:
                            print('Número inteiros apenas por favor')


                    elif editar=='6':
                        print(f'Ocorrência atual: {agendamento['ocorreu']}')
                        a = input('Qual a nova ocorrência?\n1-Falso\n2-Verdadeiro\n')
                        if a == '1':
                            agendamento['ocorreu'] = False
                        elif a == '2':
                            agendamento['ocorreu'] = True
                        else:
                            print('Essa opção não existe.')
                        if not agendamento['ocorreu'] == antigo['ocorreu']:
                            agendamento['ultima_edicao']['ultimo_item_modificado'] = "Ocorrencia"
                        else:
                            print('Nada foi editado')


                    elif editar.upper()=='SAIR':
                        break

                    else:
                        print('Essa opção não existe')
            if not antigo==agendamento:

                agendamento['ultima_edicao']['dia'] = str(date.today())
                dicto['compromissos'][categ].pop(ind)
                dicto['compromissos'][categ].append(agendamento)
                print('Arquivos atualizados!')
                with open('compr.json', 'w') as f:
                    json.dump(dicto, f, indent=3)
            else:
                print('Nada foi editado, portanto, nada irá ser salvo')


    volta()

def act4() ->None:
    """
    Verifica agendamentos
    pode ver todos os agendamento ou um em específico
    recebe nenhum valor como parâmetro e retorna nada
    tudo é feito dentro da função
    :return:
    """
    dicto = get1()
    exists = False

    try:
        categ = int(input('Qual é a categoria que deseja ver?\n1 - Reunioes\n2 - Pessoal\n3 - Tarefas\n'))

        if categ==1:
            categ = 'reunioes'
        elif categ==2:
            categ = 'pessoais'
        elif categ==3:
            categ = 'tarefas'
        else:
            print('Não temos essa opção')
        escolha = input('Você deseja ver apenas um compromisso em específico ou todos dessa categoria?\n1-Todos\n2-Um em específico\n')

        if escolha=='1':
            print('###########################################')
            print(f'Categoria escolhida: {categ}')
            if categ=='reunioes' or categ=='pessoais':
                for agendamento in dicto['compromissos'][categ]:
                    print(
                        f'ID: {agendamento['id']}\nTipo: {agendamento['tipo']}\nAssunto: {agendamento['assunto']}\nLink: {agendamento['link']}\nLocal: {agendamento['local']}\nData: {agendamento['data']}\nHorario: {agendamento['horario']}\nDia de criação: {agendamento['dia_de_criacao']}\nOcorreu: {agendamento['ocorreu']}\nUltima edição: {agendamento['ultima_edicao']['dia']}\nUltimo item editado: {agendamento['ultima_edicao']['ultimo_item_modificado']}\n\n')
            if categ=='tarefas':
                for agendamento in dicto['compromissos'][categ]:
                    print(f'Categoria: {categ}\nTarefa: {agendamento['tarefa']}\nObservacoes: {agendamento['observacoes']}\nObjetivo atual: {agendamento['objetivo_atual']}\nDeadline: {agendamento['deadline']}\nHorario: {agendamento['horario']}\nDia de criação: {agendamento['dia_de_criacao']}\nSe Ocorreu: {agendamento['ocorreu']}\nUltima edição: {agendamento['ultima_edicao']['dia']}\nUltimo item editado: {agendamento['ultima_edicao']['ultimo_item_modificado']}\n\n')



        elif escolha=='2':
            id = int(input('Qual é o ID do compromisso que deseja ver\n'))
            if categ in dicto['compromissos']:
                for i in dicto['compromissos'][categ]:
                    if i['id'] == str(id):
                        exists = True
                        agendamento = i

                if not exists:
                    print('Esse agendamento não existe, tem certeza que ele está na categoria correta? Ou se ele ao menos existe?')
                else:
                    if categ=='reunioes' or categ=='pessoais':
                        a = input(
                            f'Categoria: {categ}\nTipo: {agendamento['tipo']}\nAssunto: {agendamento['assunto']}\nLink: {agendamento['link']}\nLocal: {agendamento['local']}\nData: {agendamento['data']}\nHorario: {agendamento['horario']}\nDia de criação: {agendamento['dia_de_criacao']}\nOcorreu: {agendamento['ocorreu']}\nUltima edição: {agendamento['ultima_edicao']['dia']}\nUltimo item editado: {agendamento['ultima_edicao']['ultimo_item_modificado']}\n\n')
                    elif categ == 'tarefas':
                        print(
                            f'Categoria: {categ}\nTarefa: {agendamento['tarefa']}\nObservacoes: {agendamento['observacoes']}\nObjetivo atual: {agendamento['objetivo_atual']}\nDeadline: {agendamento['deadline']}\nHorario: {agendamento['horario']}\nDia de criação: {agendamento['dia_de_criacao']}\nSe Ocorreu: {agendamento['ocorreu']}\nUltima edição: {agendamento['ultima_edicao']['dia']}\nUltimo item editado: {agendamento['ultima_edicao']['ultimo_item_modificado']}\n\n')
        else:
            print('Essa opção mão existe')

    except ValueError:
        print('Números inteiros apenas') # Try na função inteira já que ela só recebe 2 valores os quais precisam ser inteiros
    volta()









# ///////////////////////////////////////////////////////////////////////////////////////////////////////////////
# 5, 6 e 7 são para vagas, não mexa a não ser que o erro seja sobre eles, e não sobre os agendamentos

def act5() ->None:
    """
    Buscar por informações de emprego
    dentro da API do LinkedIN
    Caso a API esteja indísponivel
    retorna um decoy em guardado em outro link
    Também salva algumas vagas se o user quiser
    :return:
    """
    # res = get2()
    # if res.status_code == 200:
    #     print('API acessada!')
    dicto = get3().json()
    salvar = []
    contador = 0
    for i in dicto:
        contador += 1
        print(f'Número: {contador}\nQuando foi postado: {str(i['date_posted'])[:10]}\nVaga: {i['title']}\nValidade: {str(i['date_validthrough'])[:10]}\nEmpresa: {i['organization']}\nLink da empresa: {i['organization_url']}\nTipos de vaga: {i['employment_type']}\nLink da vaga: {i['url']}\nSenioridade: {i['seniority']}\nEspecialidades da empresa: {i['linkedin_org_specialties']}\nSlogan da empresa: {i['linkedin_org_slogan']}\n')
    print('Caso queira mais detalhes, tente entra nos links do linkedin da empresa ou no link da vaga.')
    while True:
        try: #date_valid
            a = int(input('Deseja arquivar uma vaga?\nSe sim, dê coloque o número da empresa (o que fica em bem no inicio das informações sobre a empre e dê enter)\n\n----Caso não, digite "9999" para sair.\n-> '))
            if a == 9999:
                break
            elif contador >= a >= 1:
                a=a-1
                salvar.append(dicto[a])

                print('Item salvo!\n')
                print(f'Aqui está o ID da vaga: {dicto[a]["id"]}\n')
            else:
                print(f'Esse valor não está dentro da quantidade de vagas que são {contador}.')
        except ValueError:
            print('Número inteiros apenas, por favor')
    if not salvar==[]:
        with open('empresas.json', 'w') as f:
            json.dump(salvar, f, indent=3)
    volta() #

def act6() ->None:
    """
    Mosta as vagas salvas
    pode mostrar todas as vagas
    ou pode mostrar só uma vaga
    :return:
    """
    dicto = getvagas()
    veri = input('Se deseja ver todas as empresas, apenas der enter\nCaso queira ver apenas uma, punxando-a pelo ID, digite "PUXAR".')
    if veri.upper()=='PUXAR':
        exists = False
        iden = input('Qual é o ID da vaga?\n')
        for i in dicto:
            if i['id'] == iden:
                exists = True
                vaga = i
                break
        if not exists:
            print('Esse ID não está catalogado\nTem certeza que é o ID correto ou se ele ao menos existe?\n')
        else:
            print(
                f'ID da vaga: {vaga['id']}\nQuando foi postado: {vaga['date_posted']}\nVaga: {vaga['title']}\nValidade: {vaga['date_validthrough']}\nEmpresa: {vaga['organization']}\nLink da empresa: {vaga['organization_url']}\nTipos de vaga: {vaga['employment_type']}\nLink da vaga: {vaga['url']}\nSenioridade: {vaga['seniority']}\nEspecialidades da empresa: {vaga['linkedin_org_specialties']}\nSlogan da empresa: {vaga['linkedin_org_slogan']}\n')
    else:
        for i in dicto:
            print(
                f'ID da vaga: {i['id']}\nQuando foi postado: {i['date_posted']}\nVaga: {i['title']}\nValidade: {i['date_validthrough']}\nEmpresa: {i['organization']}\nLink da empresa: {i['organization_url']}\nTipos de vaga: {i['employment_type']}\nLink da vaga: {i['url']}\nSenioridade: {i['seniority']}\nEspecialidades da empresa: {i['linkedin_org_specialties']}\nSlogan da empresa: {i['linkedin_org_slogan']}\n')

    volta()

def act7() ->None:
    dicto = getvagas()
    exists = False
    iden = input('Qual é o ID da vaga?\n')
    for i in dicto:
        if i['id'] == iden:
            exists = True
            vaga = i
    if not exists:
        print('Esse ID não está catalogado\nTem certeza que é o ID correto ou se ele ao menos existe?\n')
    else:
        print(f'Quando foi postado: {vaga['date_posted']}\nVaga: {vaga['title']}\nValidade: {vaga['date_validthrough']}\nEmpresa: {vaga['organization']}\nLink da empresa: {vaga['organization_url']}\nTipos de vaga: {vaga['employment_type']}\nLink da vaga: {vaga['url']}\nSenioridade: {vaga['seniority']}\nEspecialidades da empresa: {vaga['linkedin_org_specialties']}\nSlogan da empresa: {vaga['linkedin_org_slogan']}\n')
        deleta = input('VocÊ tem certeza que quer deletar essa vaga?\nSe sim, digite "DELETAR".\n')
        if deleta.upper() == 'DELETAR':
            dicto.remove(vaga)
            print('Vaga deletada com sucesso!')
            with open('empresas.json', 'w') as f:
                json.dump(dicto, f, indent=3)
        else:
            print('Operação cancelada.')
        volta()


def verificar() ->None:
    """
    Função utilizada para verificar
    os compromissos com data limite
    para o dia atual
    :return: 
    """
    
    dicto = get1()
    hojerp=[]
    hojet=[]


    if os.path.exists('compr.json'):
        if not dicto['compromissos']['reunioes']==[]:
            for i in dicto['compromissos']['pessoais'] and dicto['compromissos']['reunioes']:
                if i['data']==str(date.today()):
                    hojerp.append(i)

        if not dicto['compromissos']['pessoais']==[]:
            for i in dicto['compromissos']['pessoais']:
                if i['data']==str(date.today()):
                    hojerp.append(i)

        if not dicto['compromissos']['tarefas']==[]:
            for i in dicto['compromissos']['tarefas']:
                if i['deadline']==str(date.today()):
                    hojet.append(i)

    print('Compromissos para hoje:\n')
    if not hojerp==[]:
        for i in hojerp:
            print(f'Tipo: {i['tipo']}\nAssunto: {i['assunto']}\nLink: {i['link']}\nLocal: {i['local']}\nData: {i['data']}\nHorario: {i['horario']}\n\n')
    else:
        print('  Sem compromissos!\n')

    print('Tarefas para hoje:\n')
    if not hojet==[]:
        for i in hojet:
            print(f'Tarefa: {i['tarefa']}\nObservações: {i["observacoes"]}\nObjetivo atual: {i["objetivo_atual"]}\nDeadline: {i["deadline"]}\nHoras: {i["horario"]}\nDia de criacao: {i["dia_de_criacao"]}\nUltima edição: {i["ultima_edicao"]["dia"]}\nID: {i["id"]}\n')
    else:
        print('  Sem tarefas!\n')
    volta()



def main() ->None:
    while True:
        print("\n/////////////////////////////////////////////////////////////")
        print('1 - Compromissos e tarefas para HOJE')
        print('2 - Agendamento ')
        print('3 - Excluir agendamentos')
        print('4 - Editar agendamentos')
        print('5 - Ver agendamentos')
        print('6 - Ver e salvar informações de vagas')
        print('7 - Ver vagas salvas')
        print('8 - Excluir vagas salvas') #OBS: Eu não criei um "Editar vaga salva" pois é desnecessário editar as informações e vagas
        print('9 - Sair')
        a = input('O que deseja fazer?\n')
        if a =='1':
            verificar()
        elif a =='2':
            act1()
        elif a =='3':
            act2()
        elif a =='4':
            act3()
        elif a=='5':
            act4()
        elif a =='6':
            act5()
        elif a =='7':
            act6()
        elif a =='8':
            act7()
        elif a =='9':
            break
        else:
            print('Essa opção não existe.')

main()
