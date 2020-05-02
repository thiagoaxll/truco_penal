# *********************************************************************************************
# ******   FATEC - Faculdade de Tecnologia de Carapicuiba                                ******
# ******   Funcao: responsavel por efetuar o processamento principal do jogo com todas   ******
# ******           as regras, definicoes e comportamento da aplicacao cliente            ******
# ******   Nome..: Diego Vinicius de Mello Munhoz                                        ******
# ******           Thiago Zacarias da Silva                                              ******
# ******           Victor Otavio Ponciano                                                ******
# ******   Data..: 07/07/2018                                                            ******
# *********************************************************************************************

import socket
import time
import random

global host, porta, s
host = socket.gethostbyname(socket.gethostname())
porta = 8291
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
controle = 1

clients = ['', '', '']

global instruction
instruction = ['0',   # [0] Turno
               '-1',  # [1] cartaP1[1]
               '-1',  # [2] cartaP1
               '-1',  # [3] cartaP1
               '-1',  # [4] cartaP2
               '-1',  # [5] cartaP2
               '-1',  # [6] cartaP2
               '-1',  # [7] cartaP3
               '-1',  # [8] cartaP3
               '-1',  # [9] cartaP3
               '-1',  # [10] Virou
               '-1',  # [11] cartaMesa1
               '-1',  # [12] cartaMesa2
               '-1',  # [13] cartaMesa3
               '-1',  # [14] nome1
               '-1',  # [15] nome2
               '-1',  # [16] nome3
               '0',   # [17] avatar1
               '1',   # [18] avatar2
               '2',   # [19] avatar3
               '0',   # [20] ponto1
               '0',   # [21] ponto2
               '0',   # [22] ponto3
               '1',   # [23] rodada
               '-1',  # [24] estado do jogo
               '-1',  # [25] time
               '-1',  # [26] animCartaP1
               '-1',  # [27] animCartaP1
               '-1',  # [28] animCartaP1
               '-1',  # [29] animCartaP2
               '-1',  # [30] animCartaP2
               '-1',  # [31] animCartaP2
               '-1',  # [32] animCartaP3
               '-1',  # [33] animCartaP3
               '-1',  # [34] animCartaP3
               '-1',  # [35] NomeVencedor
               '-1',  # [36] AvatarVencedor
               '-1',  # [37] Time2
               '-1']
instructionBackup = instruction

def distribuirCartas():
    global instruction
    instruction[24] = -1
    instruction[23] = 1
    cartasSorteadas = [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1]
    cartasTemp = [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1]

    for i in range(10):
        while True:
            cartasSorteadas[i] = random.randint(0, 23)
            repetida = False
            for j in range(9):
                if cartasSorteadas[i] == cartasTemp[j]:
                    repetida = True
            if not repetida:
                cartasTemp[i] = cartasSorteadas[i]
                break

    instruction[1] = cartasSorteadas[0]
    instruction[2] = cartasSorteadas[1]
    instruction[3] = cartasSorteadas[2]
    instruction[4] = cartasSorteadas[3]
    instruction[5] = cartasSorteadas[4]
    instruction[6] = cartasSorteadas[5]
    instruction[7] = cartasSorteadas[6]
    instruction[8] = cartasSorteadas[7]
    instruction[9] = cartasSorteadas[8]
    instruction[10] = cartasSorteadas[9]

    print('Cartas com: ', instruction[14], '[',  instruction[1],  instruction[2],  instruction[3], ']')
    print('Cartas com: ', instruction[15], '[', instruction[4], instruction[5], instruction[6], ']')
    print('Cartas com: ', instruction[16], '[', instruction[7], instruction[8], instruction[9], ']')

    print('distribuir cartas')

    instruction = ','.join(str(e) for e in instruction)
    instruction = instruction.split(',')

def atribuirPontos(vencedor, turno, nomeJogador):
    print('turno: ', turno)
    if vencedor != 0:
        if int(instruction[23]) == 1:
            instruction[vencedor] = int(instruction[vencedor]) + 3
        elif int(instruction[23]) == 2:
            instruction[vencedor] = int(instruction[vencedor]) + 2
        elif int(instruction[23]) == 3:
            instruction[vencedor] = int(instruction[vencedor]) + 1

        if turno == 0:
            turno = 0
        elif turno == 1:
            turno = 1
        else:
            turno = 2
    else:
        if turno == 0:
            turno = 2
        elif turno == 1:
            turno = 0
        else:
            turno = 1

    if int(instruction[vencedor]) == 12:
        print('Jogador {} Venceu.'.format(instruction[nomeJogador]))
        instruction[35] = instruction[nomeJogador]
        if vencedor == 20:
            instruction[36] = instruction[17]
        elif vencedor == 21:
            instruction[36] = instruction[18]
        else:
            instruction[36] = instruction[19]
        print('Vencedor: ', instruction[35], 'Avatar: ', instruction[36])
        instruction[20], instruction[21], instruction[22] = 0, 0, 0
    elif int(instruction[vencedor]) > 12:
        print('Jogador {} Zerou.'.format(instruction[nomeJogador]))
        instruction[vencedor] = 0
        if turno == 0:
            turno = 0
        elif turno == 1:
            turno = 1
        else:
            turno = 2

    if int(instruction[23]) == 3:
        print('Embaralhar Novamente')
        distribuirCartas()
    else:
        instruction[23] = int(instruction[23]) + 1

    instruction[0] = turno

# Verifica quem jogou a carta com o maior valor.
def verificarVencedorRodada():
    forcaCarta = [1, 1, 1, 1,
                  2, 2, 2, 2,
                  3, 3, 3, 3,
                  4, 4, 4, 4,
                  5, 5, 5, 5,
                  6, 6, 6, 6]

    if forcaCarta[int(instruction[11])] != 6 and forcaCarta[int(instruction[12])] != 6 and forcaCarta[int(instruction[13])] != 6:
        print('Nao tem manilha')
        if int(instruction[11]) > int(instruction[12]) and int(instruction[11]) > int(instruction[13]):
            if forcaCarta[int(instruction[11])] != forcaCarta[int(instruction[12])] and forcaCarta[int(instruction[11])] != forcaCarta[int(instruction[13])]:
                if int(instruction[0]) == 0:
                    atribuirPontos(21, 1, 15)
                elif int(instruction[0]) == 1:
                    atribuirPontos(22, 2, 16)
                elif int(instruction[0]) == 2:
                    atribuirPontos(20, 0, 14)
            else:
                atribuirPontos(0, int(instruction[0]), '')  # empate
        elif int(instruction[12]) > int(instruction[11]) and int(instruction[12]) > int(instruction[13]):
            if forcaCarta[int(instruction[12])] != forcaCarta[int(instruction[11])] and forcaCarta[int(instruction[12])] != forcaCarta[int(instruction[13])]:
                if int(instruction[0]) == 0:
                    atribuirPontos(22, 2, 16)
                elif int(instruction[0]) == 1:
                    atribuirPontos(20, 0, 14)
                elif int(instruction[0]) == 2:
                    atribuirPontos(21, 1, 15)
            else:
                atribuirPontos(0, int(instruction[0]), '')  # empate
        elif int(instruction[13]) > int(instruction[11]) and int(instruction[13]) > int(instruction[12]):
            if forcaCarta[int(instruction[13])] != forcaCarta[int(instruction[11])] and forcaCarta[int(instruction[13])] != forcaCarta[int(instruction[12])]:
                if int(instruction[0]) == 0:
                    atribuirPontos(20, 0, 14)
                elif int(instruction[0]) == 1:
                    atribuirPontos(21, 1, 15)
                elif int(instruction[0]) == 2:
                    atribuirPontos(22, 2, 16)
            else:
                atribuirPontos(0, int(instruction[0]), '')  # empate
    else:
        print('Tem manilha')
        if int(instruction[11]) > int(instruction[12]) and int(instruction[11]) > int(instruction[13]):
            if int(instruction[0]) == 0:
                atribuirPontos(21, 1, 15)
            elif int(instruction[0]) == 1:
                atribuirPontos(22, 2, 16)
            elif int(instruction[0]) == 2:
                atribuirPontos(20, 0, 14)
        elif int(instruction[12]) > int(instruction[11]) and int(instruction[12]) > int(instruction[13]):
            if int(instruction[0]) == 0:
                atribuirPontos(22, 2, 16)
            elif int(instruction[0]) == 1:
                atribuirPontos(20, 0, 14)
            elif int(instruction[0]) == 2:
                atribuirPontos(21, 1, 15)
        else:
            if int(instruction[0]) == 0:
                atribuirPontos(20, 0, 14)
            elif int(instruction[0]) == 1:
                atribuirPontos(21, 1, 15)
            elif int(instruction[0]) == 2:
                atribuirPontos(22, 2, 16)

    print('Turno: ', instruction[0])
# /Verifica quem jogou a carta com o maior valor.

def mudarRodada():
    verificarVencedorRodada()

    for i in range(11, 14):
        instruction[i] = '-1'

def servidor():
    global instruction, porta, host, s
    s.bind((host, porta))
    s.listen(1)
    time.sleep(1)
    print('HOST: ', host)
    print('Aguardando conexões.')
    for i in range(0, 3):
        clients[i], client = s.accept()
        clients[i].send((str(i).encode('utf-8')))
        instruction = ','.join(str(e) for e in instruction)
        clients[i].send((instruction.encode('utf-8')))

        instruction = clients[i].recv(1024)
        instruction = instruction.decode('utf-8')
        instruction = instruction.split(',')

        print('Conectado com', client, '\n')
        print('Aguardando {} jogadores.'.format(2 - i))
    print('Todas as conexões foram estabelecidas\nO jogo foi iniciado..')
    conection = 3
    distribuirCartas()

    while True:
        for i in range(3):
            instruction = ','.join(str(e) for e in instruction)
            saiu = instruction.split(',')
            if saiu[24] == '-10':
                conection -= 1
            try:
                clients[i].send((instruction.encode('utf-8')))
                instruction = clients[i].recv(1024)
                instruction = instruction.decode('utf-8')
                instruction = instruction.split(',')
            except socket.error:
                s.close()
                break
            if conection < 2:
                print('Reiniciando partida.')
                instruction = instructionBackup
                s.close()
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                servidor()
            limparMesa = 0
            try:
                if int(instruction[37]) >= 150:
                    distribuirCartas()
                    instruction[35] = '-1'
                    instruction[37] = 0
                for j in range(11, 14):
                    if int(instruction[j]) != -1:
                        limparMesa += 1
                if instruction[35] == '-1':
                    if int(instruction[37]) >= 60:

                        mudarRodada()
                    elif limparMesa == 3 and int(instruction[25]) >= 30:
                        mudarRodada()

            except IndexError:
                print('Reiniciando partida.')
                instruction = instructionBackup
                s.close()
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                servidor()

        time.sleep(0.003)

servidor()