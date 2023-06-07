'''
Disciplina:  1804 INTELIGENCIA ARTIFICIAL
Atividade: Avaliação 5 – Aplicação com o algoritmo Genético
Programa 04
Acadêmicos: Sydney Matheus de Souza
            Carlos Daniel Batista
'''
import base64
import random
import numpy as np
import pandas as pd
import PySimpleGUI as sg
from random import randint


sg.change_look_and_feel('LightGrey1')
esquerda = [
        [sg.Text('Número de População'), sg.Input(size=(6, 0), key='nPopula_', tooltip='Digite um número inteiro par maior que zero')],
        [sg.Text('       '),sg.Text('Número máximo de iterações'), sg.Input(size=(6, 0), key='itera_', tooltip='Digite um número inteiro maior que zero')],
        [sg.Text('       '),sg.Text('Taxa de Mutação'), sg.Input(size=(6, 0), key='muta_', tooltip='Digite um número inteiro de 0 a 100')],
        [sg.Text(''),sg.Button('Começar',size=(20,1))]
]

centro = [
        [sg.Text('  A          B          C          D          E          F          G          H')],
        [sg.Text('0\n\n\n1\n\n\n2\n\n\n3\n\n\n4\n\n\n5\n\n\n6\n\n\n7'), sg.Graph(canvas_size=(400, 400),graph_bottom_left=(0,0),graph_top_right=(410,410),background_color='white', key = 'graph'),sg.Text('0\n\n\n1\n\n\n2\n\n\n3\n\n\n4\n\n\n5\n\n\n6\n\n\n7')],
        [sg.Text('  A          B          C          D          E          F          G          H')]
]

direita = [
        [sg.Output(size=(60,30), key='Output')]
]

layout = [[sg.Column(esquerda, element_justification='c'),sg.VSeparator(),sg.Column(centro, element_justification='c'),sg.VSeparator(),sg.Column(direita, element_justification='c')]]

window = sg.Window('Rainhas', layout, finalize=True)
graph = window['graph']

paint = 1
tamQuad = 50
for lin in range(8):
    for col in range(8):
        if paint:
            graph.draw_rectangle((col*tamQuad+5,lin*tamQuad+3),(col*tamQuad+tamQuad+5, lin*tamQuad+tamQuad+3), line_color='black',  fill_color='black')
            paint = 0
        else:
            graph.draw_rectangle((col * tamQuad + 5, lin * tamQuad + 3),(col * tamQuad + tamQuad + 5, lin * tamQuad + tamQuad + 3), line_color='black')
            paint = 1
    paint = 1
    if lin % 2 == 0:
        paint = 0

filename = 'queen.png'

def verificar_Diagonais(populacao, Npopula):

    colisoes = np.zeros(Npopula, dtype=int)
    i = 0
    while i < Npopula:
        j = 0
        while j < 8:
            x = 1
            while x < 8:
                cima = populacao[i][j] - x
                baixo = populacao[i][j] + x

                if(j+x < 8):
                    if(populacao[i][j+x] == cima or populacao[i][j+x] == baixo):
                        colisoes[i] = colisoes[i] + 1

                if(j-x > -1):
                    if(populacao[i][j-x] == cima or populacao[i][j-x] == baixo):
                        colisoes[i] = colisoes[i] + 1

                x = x + 1
            j = j + 1
        i = i + 1

    return colisoes

def torneio (fitness, populacao):
    rand = np.zeros(int(len(populacao)/10+2), dtype=int)
    for n in range(int(len(populacao)/10+2)):
        rand[n]=randint(0, len(populacao)-1)

    maior = fitness[rand[0]]
    menor = fitness[rand[1]]
    maiorPos = 0

    for n in range(int(len(populacao)/10+2)):
        if maior < menor:
            maior = fitness[rand[n]]
            maiorPos = n

        if n < (int(len(populacao)/10+1)):
            menor = fitness[rand[n+1]]

    return rand[maiorPos]

def cruzamento (populacao, fitness, taxaMuta):

    cromo1 = torneio(fitness, populacao)
    cromo2 = torneio(fitness, populacao)

    cromo1_ = populacao[cromo1][0:8]
    cromo2_ = populacao[cromo2][0:8]

    limite = randint(2,4)
    filho1 = populacao[cromo1][0:limite]
    filho1 = list(filho1)
    filho2 = populacao[cromo2][limite:8]
    filho2 = list(filho2)

    cromo1 = limite

    while len(filho1) < 8:
        x = cromo2_[cromo1]
        if x not in filho1:
            filho1.append(cromo2_[cromo1])
        cromo1=cromo1+1
        if cromo1 == 8:
            cromo1 = 0

    cromo2 = 0
    while len(filho2) < 8:
        x = cromo1_[cromo2]
        if x not in filho2:
            filho2.append(cromo1_[cromo2])
        cromo2=cromo2+1
        if cromo2 == 8:
            cromo2 = 0

    if randint(0, 100) <= taxaMuta:

        a = randint(0, 1);
        x = randint(0,7)
        y = randint(0,7)

        if a == 0:
            print("Mutação: ", filho1)
            filho1[x],filho1[y]=filho1[y],filho1[x]
            print("Para: ", filho1)
        else:
            print("Mutação: ", filho2)
            filho2[x], filho2[y] = filho2[y], filho2[x]
            print("Para: \t", filho2)


    filhos = [filho1, filho2]
    return filhos

while True:
    event, values = window.read()
    if event in (sg.WIN_CLOSED, 'Exit'):
        break

    comecar = 0

    if event == 'Começar':
        window['Output'].update(value='')
        try:
            for n in range(8):
                graph.delete_figure(x[n])

        except:
            window['Output'].update(value='')
        Npopula=    values['nPopula_']
        try:
            Npopula = abs(int(Npopula))
            if Npopula==0:
                    Npopula=1
        except:
            Npopula = 1
            print("Digite uma entrada válida!")

        iteracoes = values['itera_']
        iteraOK = 0
        try:
            iteracoes = abs(int(iteracoes))
            if iteracoes==0:
                    iteracoes=1
            iteraOK = 1
        except:
            print("Digite uma entrada válida!")

        taxaMuta = values['muta_']
        try:
            taxaMuta = abs(int(taxaMuta))
        except:
            taxaMuta = 200
            print("Digite uma entrada válida!")

        taxaOK = 0
        if taxaMuta - 100 <= 0:
            taxaOK=1

        if Npopula % 2 == 0 and iteraOK and taxaOK:
            comecar = 1

        if comecar:
            populacao = np.zeros((Npopula, 8), dtype=int)

            i = 0
            while i<8:
                populacao[:,i]=i
                i += 1

            i = 0
            while i<Npopula:
                random.shuffle(populacao[i,:])
                i += 1

            print(populacao)

            k = 0
            while k < iteracoes:
                print("\n\nIteração: ", k+1)
                print("Populacao:\n", populacao)
                colisoes = verificar_Diagonais(populacao, Npopula)
                print("Colisoes:\n",colisoes)

                fitness = np.zeros(Npopula, dtype=int)
                i = 0
                while i < Npopula:
                    fitness[i] = 56 - colisoes[i]
                    i = i + 1

                print("Fitness:\n", fitness)

                if 56 in fitness:                                                               #Condição de parada por fitness
                    w = indice = 0
                    while w < len(fitness):
                        if fitness[w] == 56:
                            break
                        w += 1

                    solucao = np.zeros(Npopula, dtype=int)
                    solucao = populacao[w][0:8]
                    print("Solução: ", solucao)
                    c=0
                    x = np.zeros(8, dtype=int)
                    while c<8:
                        x[c] = graph.draw_image(filename=filename, location=(0 + tamQuad * c, 60 + tamQuad * abs(solucao[c]-7)))
                        c += 1

                    break

                Novapopula =np.zeros((Npopula, 8), dtype=int)
                i = 0
                while i < ((Npopula/2)+(Npopula/2)-1):                                              #Cruzamento gera objeto_[filho1,filho2]
                    Novapopula[i,:], Novapopula[i+1,:] = cruzamento(populacao, fitness, taxaMuta)   #Novapopula[filho1, filho2, filho3, ... filhoN]
                    i += 2

                populacao = Novapopula                                                              #Os filhos se tornam a nova população
                print("Filhos\n", populacao)

                k=k+1
window.close()