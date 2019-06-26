# -*- coding: utf-8 -*-
import os
import sys

TODO_FILE = 'todo.txt'
ARCHIVE_FILE = 'done.txt'

RED   = "\033[1;31m"  
BLUE  = "\033[1;34m"
CYAN  = "\033[1;36m"
GREEN = "\033[0;32m"
RESET = "\033[0;0m"
BOLD    = "\033[;1m"
REVERSE = "\033[;7m"
YELLOW = "\033[0;33m"

ADICIONAR = 'a'
REMOVER = 'r'
FAZER = 'f'
PRIORIZAR = 'p'
LISTAR = 'l'
AJUDA = "help"


# Imprime texto com cores. Por exemplo, para imprimir "Oi mundo!" em vermelho, basta usar
#
# printCores('Oi mundo!', RED)
# printCores('Texto amarelo e negrito', YELLOW + BOLD)

def printCores(texto, cor):
    print(cor + texto + RESET, end="")


# Adiciona um compromisso aa agenda. Um compromisso tem no minimo
# uma descrição. Adicionalmente, pode ter, em caráter opcional, uma
# data (formato DDMMAAAA), um horário (formato HHMM), uma prioridade de A a Z, 
# um contexto onde a atividade será realizada (precedido pelo caractere
# '@') e um projeto do qual faz parte (precedido pelo caractere '+'). Esses
# itens opcionais são os elementos da tupla "extras", o segundo parâmetro da
# função.
#
# extras ~ (data, hora, prioridade, contexto, projeto)
#
# Qualquer elemento da tupla que contenha um string vazio ('') não
# deve ser levado em consideração. 
def adicionar(descricao, extras):
    # não é possível adicionar uma atividade que não possui descrição.
    novaAtividade = ""
    if descricao == '':
        return False
    else:
        novaAtividade = extras[0] + " " + extras[1] + " " + extras[2] + " " + descricao + " " + extras[3] + " " + \
                        extras[4]
    found = False

    try:
        fp = open(TODO_FILE, 'r')
        x = fp.readlines()
        for i in x:
            i = i.strip()

            if novaAtividade == i:
                os.system('cls' if os.name == 'nt' else 'clear')
                print("Atividade já cadastrada.")
                s = input("Digite enter para continuar...")
                os.system('cls' if os.name == 'nt' else 'clear')
                found = True

        fp.close()
    except IOError as err:
        os.system('cls' if os.name == 'nt' else 'clear')
        print("Não foi possível escrever para o arquivo " + TODO_FILE)
        print(err)
        return False

    ################ COMPLETAR

    # Escreve no TODO_FILE.
    try:
        fp = open(TODO_FILE, 'a')
        if not found:
            fp.write(novaAtividade + "\n")
            os.system('cls' if os.name == 'nt' else 'clear')
            print("Evento cadastrado com sucesso.")
            s = input("Digite enter para continuar...")
            os.system('cls' if os.name == 'nt' else 'clear')

        fp.close()
    except IOError as err:
        print("Não foi possível escrever para o arquivo " + TODO_FILE)
        print(err)
        return False

    return True


# Valida a prioridade.
def prioridadeValida(pri):
    if len(pri) != 3:
        return False
    else:
        if 65 <= ord(pri[1]) <= 90:
            return True
        return False
    ################ COMPLETO


# Valida a hora. Consideramos que o dia tem 24 horas, como no Brasil, ao invés
# de dois blocos de 12 (AM e PM), como nos EUA.
def horaValida(horaMin):
    if len(horaMin) != 4 or not soDigitos(horaMin):
        # print("HORA inválida. Tente novamente.")
        return False
    else:
        if (horaMin[0] + horaMin[1]) < "00" or horaMin[0] + horaMin[1] > "23":
            # print("HORA inválida. Tente novamente.")
            return False
        elif (horaMin[2] + horaMin[3]) < "00" or horaMin[2] + horaMin[3] > "60":
            # print("HORA inválida. Tente novamente.")
            return False
        else:
            return True

        ################ COMPLETO


# Valida datas. Verificar inclusive se não estamos tentando
# colocar 31 dias em fevereiro. Não precisamos nos certificar, porém,
# de que um ano é bissexto. 
def dataValida(data):
    if len(data) != 8 or not soDigitos(data):
        # print("DATA inválida. Tente novamente.")

        return False

    elif (data[0] + data[1]) < "00" or (data[0] + data[1]) > "31":
        # print("DATA inválida. Tente novamente.")

        return False
    elif (data[2] + data[3]) < "00" or (data[2] + data[3]) > "12":
        # print("DATA inválida. Tente novamente.")
        return False
    # elif (data[4] + data[5] + data[6] + data[7]) < "2019":
    #
    #   return False
    else:

        if (data[0] + data[1] > "29") and ((data[2] + data[3]) == "02"):
            return False

        elif data[0] + data[1] > "30":
            if ((data[2] + data[3]) == "04") and ((data[2] + data[3]) == "06") and ((data[2] + data[3]) == "09") and (
                    (data[2] + data[3]) == "11"):
                return False

        elif data[0] + data[1] == "31":
            if ((data[2] + data[3]) == "01") and ((data[2] + data[3]) == "03") and ((data[2] + data[3]) == "05") and (
                    (data[2] + data[3]) == "07") and ((data[2] + data[3]) == "08") and (
                    (data[2] + data[3]) == "10") and ((data[2] + data[3]) == "12"):
                return False
        else:
            return True

    ################ COMPLETO

    return False


# Valida que o string do projeto está no formato correto.
def projetoValido(proj):
    if proj[0] != "+" and len(proj) < 2:
        return False
    else:
        return True

    ################ COMPLETO


# Valida que o string do contexto está no formato correto. 
def contextoValido(cont):
    if len(cont) < 2 and cont[0] != "@":
        return False
    else:
        return True
    ################ COMPLETO


# Valida que a data ou a hora contém apenas dígitos, desprezando espaços
# extras no início e no fim.
def soDigitos(numero):
    if type(numero) != str:
        return False
    for x in numero:
        if x < '0' or x > '9':
            return False
    return True


# Dadas as linhas de texto obtidas a partir do arquivo texto todo.txt, devolve
# uma lista de tuplas contendo os pedaços de cada linha, conforme o seguinte
# formato:
#
# (descrição, prioridade, (data, hora, contexto, projeto))
#
# É importante lembrar que linhas do arquivo todo.txt devem estar organizadas de acordo com o
# seguinte formato:
#
# DDMMAAAA HHMM (P) DESC @CONTEXT +PROJ
#
# Todos os itens menos DESC são opcionais. Se qualquer um deles estiver fora do formato, por exemplo,
# data que não tem todos os componentes ou prioridade com mais de um caractere (além dos parênteses),
# tudo que vier depois será considerado parte da descrição.  
def organizar(linhas):
    itens = []
    # print("ENTROU ORGANIZAR", linhas)
    for l in linhas:

        data = ''
        hora = ''
        pri = ''
        desc = ''
        contexto = ''
        projeto = ''

        l = l.strip()  # remove espaços em branco e quebras de linha do começo e do fim
        tokens = l.split()  # quebra o string em palavras

        # print("Tokens: ", tokens)

        i = 0
        while i < len(tokens):

            if tokens[i].isdigit():
                if len(tokens[i]) == 8:
                    if dataValida(tokens[i]):
                        data = tokens[i]
                        tokens.remove(tokens[i])
                        i = 0
                elif len(tokens[i]) == 4:
                    if horaValida(tokens[i]):
                        hora = tokens[i]
                        tokens.remove(tokens[i])
                        i = 0

                else:
                    os.system('cls' if os.name == 'nt' else 'clear')
                    print("DATA/HORA INVÁLIDOS")


                    h = input("Digite enter para continuar...")
                    os.system('cls' if os.name == 'nt' else 'clear')
                    return []
                    # tokens.pop(0)
                    # i += 1

            elif len(tokens[i]) == 1:
                x = "(" + tokens[i].upper() + ")"
                if prioridadeValida(x):
                    pri = x
                    tokens.remove(tokens[i])
                    x = 0

            elif tokens[i][0] == "(":
                tokens[i] = tokens[i].upper()
                x = ""

                if prioridadeValida(tokens[i]):
                    pri = tokens[i]
                    tokens.remove(tokens[i])
                    i = 0

            elif tokens[i][0] == "@":
                if contextoValido(tokens[i]):
                    contexto = tokens[i]
                    tokens.remove(tokens[i])
                    i = 0
            elif tokens[i][0] == "+":

                if projetoValido(tokens[i]):
                    projeto = tokens[i]
                    tokens.remove(tokens[i])
                    i = 0

            else:
                i += 1

        for p in tokens:
            desc = desc + p
            desc = desc + " "

        # Processa os tokens um a um, verificando se são as partes da atividade.
        # Por exemplo, se o primeiro token é uma data válida, deve ser guardado
        # na variável data e posteriormente removido a lista de tokens. Feito isso,
        # é só repetir o processo verificando se o primeiro token é uma hora. Depois,
        # faz-se o mesmo para prioridade. Neste ponto, verifica-se os últimos tokens
        # para saber se são contexto e/ou projeto. Quando isso terminar, o que sobrar
        # corresponde à descrição. É só transformar a lista de tokens em um string e
        # construir a tupla com as informações disponíveis.

        ################ COMPLETAR
        itens.append((desc, (data, hora, pri, contexto, projeto)))


    return itens


# Datas e horas são armazenadas nos formatos DDMMAAAA e HHMM, mas são exibidas
# como se espera (com os separadores apropridados). 
#
# Uma extensão possível é listar com base em diversos critérios: (i) atividades com certa prioridade;
# (ii) atividades a ser realizadas em certo contexto; (iii) atividades associadas com
# determinado projeto; (vi) atividades de determinado dia (data específica, hoje ou amanhã). Isso não
# é uma das tarefas básicas do projeto, porém. 
def listar():
    x = open("todo.txt", "r")
    file = x.readlines()
    listaLinhasArquivo = []
    listaTodasAsLinhasArquivoOrganizada = []
    for i in file:

        x = ["".join(i)]

        temp = organizar(x)
        listaLinhasArquivo.append(temp)

        listaTodasAsLinhasArquivoOrganizada = []

        cont = 0
        while cont <= len(listaLinhasArquivo) - 1:
            listaTodasAsLinhasArquivoOrganizada = listaTodasAsLinhasArquivoOrganizada + listaLinhasArquivo[cont]
            cont += 1

    ################ COMPLETO
    return listaTodasAsLinhasArquivoOrganizada


def ordenarPorDataHora(itens, listaSemDataNemHora):
    y = 0

    while y < len(itens) - 1:

        if itens[y][1][0][4:] > itens[y + 1][1][0][4:]:
            auxiliar = itens[y]
            itens[y] = itens[y + 1]
            itens[y + 1] = auxiliar
            y = 0
        elif itens[y][1][0][4:] == itens[y + 1][1][0][4:]:
            if itens[y][1][0][2:4] > itens[y + 1][1][0][2:4]:
                auxiliar = itens[y]
                itens[y] = itens[y + 1]
                itens[y + 1] = auxiliar
                y = 0

            elif itens[y][1][0][2:4] == itens[y + 1][1][0][2:4]:
                if itens[y][1][0][:2] > itens[y + 1][1][0][:2]:
                    auxiliar = itens[y]
                    itens[y] = itens[y + 1]
                    itens[y + 1] = auxiliar
                    y = 0
                elif itens[y][1][0][:2] == itens[y + 1][1][0][:2]:

                    if itens[y][1][1] != "":
                        if itens[y][1][1][:2] > itens[y + 1][1][1][:2]:
                            auxiliar = itens[y]
                            itens[y] = itens[y + 1]
                            itens[y + 1] = auxiliar
                            y = 0
                        elif itens[y][1][1][:2] == itens[y + 1][1][1][:2]:


                            if itens[y][1][1][2:] > itens[y + 1][1][1][2:]:

                                auxiliar = itens[y]
                                itens[y] = itens[y + 1]
                                itens[y + 1] = auxiliar
                                y = 0
                            else:
                                y += 1
                        else:
                            y += 1
                    else:
                        y += 1
                else:
                    y += 1
            else:
                y += 1
        else:
            y += 1

    ################ COMPLETAR


    return itens


def ordenarPorPrioridade(itens):
    x = 0
    while x <= len(itens) - 2:
        if itens[x][1][2][1] > itens[x + 1][1][2][1]:
            aux = itens[x]
            itens[x] = itens[x + 1]
            itens[x + 1] = aux
            x = 0
        else:
            x += 1

    ################ COMPLETAR

    return itens


def fazer(num):
    num = int(num)

    x = open("todo.txt", "r")
    arq = x.readlines()

    lista_linhas = []
    nova_lista_linhas = []

    for i in arq:
        i = i.strip()
        lista_linhas.append(i)
    x.close()

    if num > len(lista_linhas)-1:
        os.system('cls' if os.name == 'nt' else 'clear')
        print("Índice não encontrado. Tente novamente.")
        s = input("Digite enter para continuar...")
        os.system('cls' if os.name == 'nt' else 'clear')
    elif num < 0:
        os.system('cls' if os.name == 'nt' else 'clear')
        print("Índice inválido. Tente novamente.")
        s = input("Digite enter para continuar...")
        os.system('cls' if os.name == 'nt' else 'clear')
    else:

        x = open("todo.txt", "w")
        y = open("done.txt", "a")

        cont = 0
        # linha_alvo = ""
        for i in lista_linhas:
            if cont != num:
                nova_lista_linhas.append(i)
                x.write(i + "\n")
            else:
                # linha_alvo = i
                y.write(i + "\n")
            cont += 1

        os.system('cls' if os.name == 'nt' else 'clear')
        print("Atividade realizada!")
        s = input("Digite enter para continuar...")
        os.system('cls' if os.name == 'nt' else 'clear')






    ################ COMPLETAR

    return


def remover(target):
    x = open("todo.txt", "r")

    arq = x.readlines()
    x.close()

    lista = []
    for i in arq:
        i = i.strip()
        lista.append(i)

    if target > len(lista)-1 or target < 0:
        return False
    else:
        cont = 0
        while cont < len(lista):
            if cont == target:
                lista.pop(target)
            cont += 1

        x = open("todo.txt", "w")
        for i in lista:
            x.write(i + "\n")
        x.close()
        return True

    ################ COMPLETAR


# prioridade é uma letra entre A a Z, onde A é a mais alta e Z a mais baixa.
# num é o número da atividade cuja prioridade se planeja modificar, conforme
# exibido pelo comando 'l'. 
def priorizar(num, prioridade):
    x = open("todo.txt", "r")
    arq = x.readlines()
    num = int(num)
    todas_as_linhas = []
    for i in arq:
        i = i.strip()
        i = i.split()
        todas_as_linhas.append(i)
    x.close()

    contLinhas = 0
    entrar = True
    for linha in todas_as_linhas:
        found = False

        if contLinhas == num:

            for token in linha:
                if len(token) == 3 and token[0] == "(" and token[2] == ")" and entrar:

                    linha.remove(token)
                    token = "(" + prioridade + ")"
                    linha.append(token)
                    found = True
                    os.system('cls' if os.name == 'nt' else 'clear')
                    print("Prioridade alterada com sucesso.")
                    s = input("Digite enter para continuar...")
                    os.system('cls' if os.name == 'nt' else 'clear')
                    contLinhas += 1
                    entrar = False
            if not found:
                print("Erro. Atividade não possui prioridade. Impossível alterar.")
                contLinhas += 1

        elif num > len(todas_as_linhas)-1 and entrar:
            os.system('cls' if os.name == 'nt' else 'clear')
            print("Indice não encontrado. Tente novamente.")
            s = input("Digite enter para continuar...")
            os.system('cls' if os.name == 'nt' else 'clear')
            entrar = False

        elif num < 0:
            os.system('cls' if os.name == 'nt' else 'clear')
            print("Indice inválido. Tente novamente. ")

            s = input("Digite enter para continuar...")
            os.system('cls' if os.name == 'nt' else 'clear')
            break
        else:

            contLinhas += 1




    x = open("todo.txt", "w")

    for linha in todas_as_linhas:
        for token in linha:
            x.write(token + " ")
        x.write("\n")

    x.close()




    ################ COMPLETAR

    return


# Esta função processa os comandos e informações passados através da linha de comando e identifica
# que função do programa deve ser invocada. Por exemplo, se o comando 'adicionar' foi usado,
# isso significa que a função adicionar() deve ser invocada para registrar a nova atividade.
# O bloco principal fica responsável também por tirar espaços em branco no início e fim dos strings
# usando o método strip(). Além disso, realiza a validação de horas, datas, prioridades, contextos e
# projetos. 
def processarComandos(comandos):
    if len(comandos) == 1:
        print(REVERSE, end='')
        os.system('cls' if os.name == 'nt' else 'clear')
        print("Sintaxe de chamada do aplicativo inválida. Para ajuda, chamar a agenda e passar 'help' como parâmetro.")
        print(YELLOW, end='')
        s = input("Digite enter para continuar...")
        os.system('cls' if os.name == 'nt' else 'clear')
    else:

        if comandos[1] == ADICIONAR:

            comandos.pop(0)  # remove 'agenda.py'
            comandos.pop(0)  # remove 'adicionar'

            # print("AQUWIUASHASDLJ: ", organizar([' '.join(comandos)])[0])
            itemParaAdicionar = organizar([' '.join(comandos)])[0]
            # itemParaAdicionar = (descricao, (prioridade, data, hora, contexto, projeto))
            if itemParaAdicionar != "0":
                if not adicionar(itemParaAdicionar[0], itemParaAdicionar[1]):
                    print("Erro. Descrição vazia. Tente novamente.")

        elif comandos[1] == LISTAR:

            if len(comandos) <= 2:
                somenteListar = True
            else:
                somenteListar = False

            comandos.pop(0)  # remove 'agenda.py'
            comandos.pop(0)  # remove 'adicionar'

            listaTodasAsLinhasArquivo = listar()
            listaTodasAsLinhasArquivoSEMdatahora = []
            listaTodasAsLinhasArquivoCOMdatahora = []
            listaTodasAsLinhasArquivoSEMdataNEMhora = []

            for i in listaTodasAsLinhasArquivo:

                if (i[1][0] == "" and i[1][1] != "") or (i[1][0] != "" and i[1][1] == ""):
                    listaTodasAsLinhasArquivoSEMdatahora.append(i)
                elif i[1][0] == "" and i[1][1] == "":
                    listaTodasAsLinhasArquivoSEMdataNEMhora.append(i)
                else:
                    listaTodasAsLinhasArquivoCOMdatahora.append(i)
            listaTeste = listaTodasAsLinhasArquivoCOMdatahora + listaTodasAsLinhasArquivoSEMdatahora
            ####################

            # tarefasOrdenadasDataHora = ordenarPorDataHora(
            #     listaTodasAsLinhasArquivoCOMdatahora) + listaTodasAsLinhasArquivoSEMdatahora + listaTodasAsLinhasArquivoSEMdataNEMhora
            tarefasOrdenadasDataHora = ordenarPorDataHora(listaTeste, listaTodasAsLinhasArquivoSEMdataNEMhora) + listaTodasAsLinhasArquivoSEMdataNEMhora
            ####################

            listaTodasAsLinhasArquivoComPrioridade = []
            listaTodasAsLinhasArquivoSEMPrioridade = []

            for i in tarefasOrdenadasDataHora:
                if i[1][2] != "":
                    listaTodasAsLinhasArquivoComPrioridade.append(i)
                else:
                    listaTodasAsLinhasArquivoSEMPrioridade.append(i)

            tarefasOrdenadasPrioridade = ordenarPorPrioridade(listaTodasAsLinhasArquivoComPrioridade)
            tarefasOrdenadasPrioridade = tarefasOrdenadasPrioridade + listaTodasAsLinhasArquivoSEMPrioridade
            # print("listaTodasAsLinhasArquivo: ", tarefasOrdenadasPrioridade)

            x = open("todo.txt", "w")

            for i in tarefasOrdenadasPrioridade:
                x.write(i[1][0] + " " + i[1][1] + " " + i[1][2] + " " + i[0] + " " + i[1][3] + " " + i[1][4] + "\n")

            x.close()

            os.system('cls' if os.name == 'nt' else 'clear')
            print(
                "N|DATA      |   HORA   |PRIOR|                                       DESCRIÇÃO                                                |       CONTEXTO        |       PROJETO")
            indice = 0

            for i in tarefasOrdenadasPrioridade:



                if i[1][0] == "":
                    if i[1][2] != "":
                        if i[1][2][1] == "A" or i[1][2][1] == "B" or i[1][2][1] == "C" or i[1][2][1] == "D":

                            print(RED, end="")
                    if indice < 10:
                        if i[1][2] != "":
                            print("{}:".format(indice) + "---------", end="")
                    else:

                        print("{}:".format(indice) + "--------", end="")
                    print("    ", end='')
                else:
                    if i[1][2] != "":
                        if i[1][2][1] == "A" or i[1][2][1] == "B" or i[1][2][1] == "C" or i[1][2][1] == "D":
                            print(RED, end="")
                        print(
                            "{}:".format(indice) + i[1][0][0] + i[1][0][1] + "/" + i[1][0][2] + i[1][0][3] + "/" + i[1][0][4:],
                            end="")
                        if indice > 9:
                            print("  ", end='')
                        else:
                            print("   ", end='')


                if i[1][1] == "":
                    print("------", end="")
                    print("    ", end='')
                else:
                    print(i[1][1][0] + i[1][1][1] + ":" + i[1][1][2] + i[1][1][3], end="")
                    print("     ", end='')

                if i[1][2] == "":
                    print("---", end="")
                    print("   ", end='')
                else:
                    if i[1][2] != "":
                        if i[1][2][1] == "A" or i[1][2][1] == "B" or i[1][2][1] == "C" or i[1][2][1] == "D":
                            printCores(i[1][2], RED)
                            print("   ", end='')
                        else:
                            print(i[1][2], end="")
                            print("   ", end='')

                if i[1][2] != "":
                    if i[1][2][1] == "A" or i[1][2][1] == "B" or i[1][2][1] == "C" or i[1][2][1] == "D":
                        print(RED, end="")

                        print(i[0] + "." * (98 - len(i[0])), end="")
                        print(RESET, end="")
                        print("  ", end='')
                    else:
                        print(i[0] + "." * (98 - len(i[0])), end="")
                        print("  ", end='')
                        print(RESET, end="")
                else:
                    print(i[0] + "." * (98 - len(i[0])), end="")
                    print("  ", end='')

                if i[1][3] == "":
                    if i[1][2] != "":
                        if i[1][2][1] == "A" or i[1][2][1] == "B" or i[1][2][1] == "C" or i[1][2][1] == "D":
                            print(RED, end="")
                    print("-----------", end="")
                    print("              ", end="")
                else:
                    if i[1][2] != "":
                        if i[1][2][1] == "A" or i[1][2][1] == "B" or i[1][2][1] == "C" or i[1][2][1] == "D":
                            print(RED, end="")

                    print(i[1][3], end="")

                    print(" " * (25 - len(i[1][3])), end="")

                if i[1][4] == "":
                    print("-----------")
                    print(RESET, end="")
                else:
                    print(i[1][4])
                    print(RESET, end="")
                indice += 1

            return
            ################ COMPLETAR

        elif comandos[1] == REMOVER:
            comandos.pop(0)
            comandos.pop(0)
            indice = int(comandos[0])


            if not remover(indice):
                os.system('cls' if os.name == 'nt' else 'clear')
                print("Índice não encontrado. Tente novamente.")
                s = input("Digite enter para continuar...")
                os.system('cls' if os.name == 'nt' else 'clear')
            else:
                os.system('cls' if os.name == 'nt' else 'clear')
                print("Atividade deletada com sucesso.")
                s = input("Digite enter para continuar...")
                os.system('cls' if os.name == 'nt' else 'clear')
            return

            ################ COMPLETAR

        elif comandos[1] == FAZER:
            comandos.pop(0)
            comandos.pop(0)
            fazer(comandos[0])
            return

            ################ COMPLETAR

        elif comandos[1] == PRIORIZAR:
            comandos.pop(0)
            comandos.pop(0)
            if len(comandos) == 1:
                os.system('cls' if os.name == 'nt' else 'clear')
                print("Sintaxe inválida. Para ajuda, chamar help como parâmetro para a agenda.")
                s = input("Digite enter para continuar...")
                os.system('cls' if os.name == 'nt' else 'clear')
            else:
                # print(comandos[0], comandos[1])
                priorizar(comandos[0], comandos[1])


            ################ COMPLETAR

        elif comandos[1].lower() == AJUDA:
            os.system('cls' if os.name == 'nt' else 'clear')
            print(YELLOW, end='')
            print("Funcionalidades: Para chamar alguma das funcionalidades, chamar o python3, seguido do agenda.py e "
                  "logo após digitar algum dos seguintes parâmetros(SEM ASPAS):")
            print("\nCadastro: Cadastrar na agenda o dia, hora, prioridade, descrição, contexto(PRECEDIDO DE @) e projeto"
                  "(PRECEDIDO DE +) de um compromisso.\nParâmetro: a\n\nListar: Lista todos os compromissos cadastrados na "
                  "agenda.\nParâmetro: l\n\nRemover: Remove um compromisso da agenda.\nParâmetro: r + número do "
                  "compromisso.\n\nFazer: Marca um compromisso como realizado.\nParâmetro: f + número do compromisso.\n\nPriorizar: Muda a"
                  "prioridade de um compromisso que já tenha prioridade cadastrada.\nParâmetro: p + número do compromisso. + nova prioridade.\n\n\n")

            s = input("Digite enter para continuar...")
            os.system('cls' if os.name == 'nt' else 'clear')
        else:
            os.system('cls' if os.name == 'nt' else 'clear')
            print("Comando inválido.")
            s = input("Digite enter para continuar...")
            os.system('cls' if os.name == 'nt' else 'clear')


# sys.argv é uma lista de strings onde o primeiro elemento é o nome do programa
# invocado a partir da linha de comando e os elementos restantes são tudo que
# foi fornecido em sequência. Por exemplo, se o programa foi invocado como
#
# python3 agenda.py a Mudar de nome.
#
# sys.argv terá como conteúdo
#
# ['agenda.py', 'a', 'Mudar', 'de', 'nome']

# listaTeste = ["agenda.py", "a", "f", "2007201", "1842", "issoaianiversario", "de", "AGORAAAAfulano","@TESTE", "+FACULDADE"]


# o = ["agenda.py", "p", "4", "Z"]

processarComandos(sys.argv)
