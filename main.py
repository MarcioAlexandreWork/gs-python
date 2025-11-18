import json
import random
import os
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

def get1()->None:
    if os.path.exists('compr.json'):
        with open('compr.json', 'r') as agenda:
            dicto = json.load(agenda)
    else:
        dicto = {
            'compromissos':
                {
                 "reunioes":[],
                 "pessoais":[],
                 "tarefas":[],
                 "online":[],''
             }
        }
    return dicto



# def get2():
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
        # LER PARA MELHOR COMPREENSÃO: INFORMÇÕES APENAS DE DECOY EM CASO DO ARQUIVO JSON NÃO EXISTIR, deixei só 2 pois deve ser mais que o suficiente para demonstrar como que a função de request deveria funcionar e de como os arquivos deveriam sair
        # essa função deverá ser usada apenas se o local de request de API não estiver mais aceitando request já que ele possui um número de requests limitado por mês
        # essa função também é utilizada para testes com a API, para que eu não fique dando toda hora requests acambando com o limite que eu tenho por mês, assim entregando um produto final mais completo






def act1() ->None:
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
            data = str(datetime.today())
            horario = f'{str(datetime.now().hour)}:{str(datetime.now().minute)}'
        if data==str(datetime.today()): #Checar se a reunião já ocorreu ou não, mesmo que possa ser inutil para cosias como agendamento de eventos futuros, o usuário pode usar para o assunto da reunião anterior ou só para registro mesmo
            if horario<f'{str(datetime.now().hour)}:{str(datetime.now().minute)}':
                ocorreu = True
            else:
                ocorreu = False
        else:
            ocorreu = True
        a = input(f'Categoria: {categ}\nTipo: {tipo}\nAssunto: {assunto}\nLink: {link}\nLocal: {local}\nData: {data}\nHorario: {horario}\n\nAs informações estão corretas?\nCaso não, digite "SAIR" para voltar o menu principal\n')
        if not a.upper() == 'SAIR':
            if not dicto[categ]==[]:
                while True:
                    exists = False
                    b = str(random.randint(1000,9999))
                    for i in dicto[categ]:
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
            dicto[categ].append(reuniao)
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
            deadline = str(datetime.today())
            horario = f'{str(datetime.now().hour)}:{str(datetime.now().minute)}'
        if deadline==str(datetime.today()): #Checar se a reunião já ocorreu ou não, mesmo que possa ser inutil para cosias como agendamento de eventos futuros, o usuário pode usar para o assunto da reunião anterior ou só para registro mesmo
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
            if not dicto['tarefas']==[]:
                while True:
                    exists = False
                    b = str(random.randint(1000,9999))
                    for i in dicto['tarefas']:
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

            dicto['tarefas'].append(tarefa)
            print(f'Agendamento salvo!\nAqui está o ID da tarefa: {iden}')
            with open('compr.json','w') as f:
                json.dump(dicto, f, indent=3)

    volta()

def act2() ->None:
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
        if categ in dicto:
            for i in dicto[categ]:
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
                    dicto[categ].remove(agendamento)

                with open('compr.json', 'w') as f:
                    json.dump(dicto, f, indent=4)
    except ValueError:
        print('Números inteiros apenas')
    volta()

def act3() ->None:  ##Não esquecer de fazer a função 3
    volta()

def act4() ->None:
    dicto = get1()
    exists = False

    try:
        categ = int(input('Qual é a categoria que deseja ver?\n1 - Reunioes\n2 - Pessoal\n3 - Tarefas\n'))
        id = int(input('Qual é o ID do compromisso que deseja ver\n'))
        if categ==1:
            categ = 'reunioes'
        elif categ==2:
            categ = 'pessoais'
        elif categ==3:
            categ = 'tarefas'
        else:
            print('Não temos essa opção')
        if categ in dicto:
            for i in dicto[categ]:
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

    except ValueError:
        print('Números inteiros apenas') # Try na função inteira já que ela só recebe 2 valores os quais precisam ser inteiros
    volta()

def act5() ->None:
    """
    Buscar por informações de emprego
    dentro da API do LinkedIN
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
        print(f'Número: {contador}\nQuando foi postado: {i['date_posted']}\nVaga: {i['title']}\nValidade: {i['date_validthrough']}\nEmpresa: {i['organization']}\nLink da empresa: {i['organization_url']}\nTipos de vaga: {i['employment_type']}\nLink da vaga: {i['url']}\nSenioridade: {i['seniority']}\nEspecialidades da empresa: {i['linkedin_org_specialties']}\nSlogan da empresa: {i['linkedin_org_slogan']}\n')
    print('Caso queira mais detalhes, tente entra nos links do linkedin da empresa ou no link da vaga.')
    while True:
        try:
            a = int(input('Deseja arquivar uma vaga?\nSe sim, dê coloque o número da emprega (o que fica em bem no inicio das informações sobre a empre e dê enter)\n\nCaso não, digite "SAIR".\n'))
            if a == 'SAIR':
                break
            elif a<=20 or a>=1:
                a=a-1
                salvar.append(dicto[a])
                print('Item salvo!\n')
        except ValueError:
            print('Número inteiros apenas, por favor')
    if not salvar==[]:
        with open('empresas.json', 'w') as f:
            json.dump(salvar, f, indent=3)
    volta()




def verificar() ->None:
    dicto = get1()
    hojerp=[]
    hojet=[]

    print(dicto['reunioes'])
    print(dicto['pessoais'])

    if not dicto['reunioes']==[]:
        for i in dicto['pessoais'] and dicto['reunioes']:
            if i['data']==str(date.today()):
                hojerp.append(i)

    if not dicto['pessoais']==[]:
        for i in dicto['pessoais']:
            if i['data']==str(date.today()):
                hojerp.append(i)

    print(dicto['tarefas'])
    if not dicto['tarefas']==[]:
        for i in dicto['tarefas']:
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
        print('1 - Compromissos e tarefas de hoje')
        print('2 - Agendamento ')
        print('3 - Excluir agendamentos')
        print('4 - Editar agendamentos')
        print('5 - Ver agendamentos')
        print('6 - Ver e salvar informações de emprego')
        print('7 - Sair')
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
            break

main()
