# *********************************************************************************************
# ******   FATEC - Faculdade de Tecnologia de Carapicuiba                                ******
# ******   Funcao: responsavel por efetuar o processamento principal do jogo com todas   ******
# ******           as regras, definicoes e comportamento da aplicacao cliente            ******
# ******   Nome..: Diego Vinicius de Mello Munhoz                                        ******
# ******           Thiago Zacarias da Silva                                              ******
# ******           Victor Otavio Ponciano                                                ******
# ******   Data..: 07/07/2018                                                            ******
# *********************************************************************************************

import os
import pygame
import pygame.mixer
import resources
import config
import textos
import random
import socket

os.environ['SDL_VIDEO_CENTERED'] = '1'


menuDic = {'btStart': [(14, 252), (80, 270)], 'btConfig': [(14, 416), (40, 429)], 'posBandeira': (710, 10),
           'btAvatar': [(14, 334), (80, 348)], 'nomeJogo': (0, 0), 'btVoltar': [(488, 529), (560, 540)],
           'btLeft': (7, 434), 'btRight': (263, 434), 'opcaoIdioma': (52, 434), 'nomeMenu': (325, 205), 'posAvatarMenu': (342, 240), 'posAvatarLoja': (185, 266), 'btLeftAvatar': (20, 249), 'btRightAvatar': (130, 249),
           'nomeTexto': (300, 514), 'contrato1': (325, 30), 'contrato2': (50, 120), 'contrato3': (30, 200), 'contrato4': (350, 250), 'contrato5': (50, 320),
           'btnServer': (121, 246), 'btnClient': (492, 246), 'btnConfirmServer': (595, 431),  'ipTxt': (248, 260), 'posEspelho': (300, 213), 'nomeSalaEspera': (14, 357), 'posAvatarSalaEspera': (24, 247), 'txtLobby': (20, 20),
           'txtAguardando': (20, 50), 'txtErrorLobby': (50, 70), 'btnMudarNome': (12, 220), 'btnCredito': (12, 300), 'txtMudarNome': (26, 235), 'txtCreditos': (50, 315), 'btnSingle': (626, 317), 'btnMult': (626, 252),
           'txtSinglePlayer': (642, 337), 'txtMultiPlayer': (642, 271), 'btnRegras': (12, 529), 'txtRegras': (42, 549), 'imgRegras': (0, 0)}


jogoDic = {'posCartaPlayer1': [(309, 525), (375, 525), (441, 525)], 'posCartaPlayer2': [(716, 388), (716, 340), (716, 290)], 'posCartaPlayer3': [(16, 278), (16, 328), (16, 378)],
           'posJogada': [(343, 290), (416, 388), (546, 278)], 'posBralho': (192, 290), 'posCartaVirada': (242, 290), 'posPontoJogador1': (680, 540), 'posPontoJogador2': (680, 100), 'posPontoJogador3': (68, 100),
           'posTextoRodada': (292, 8), 'posTextoNomeJogador': [(540, 545), (540, 112), (126, 112)], 'posBgFundoAvatar': [(675, 475), (675, 23), (7, 24)], 'posAvatar': [(740, 490), (730, 34), (7, 34)],
           'posAvatarVencedor': (340, 208), 'posNomeVencedor': (333, 425), 'posTextoVencedor': (292, 8), 'posTxtPerdedor': [(228, 540), (449, 540)], 'posPerdedores': [(228, 483), (449, 483)]}

botao = pygame.image.load(resources.BOTAO)
botao2 = pygame.image.load(resources.BOTAO2)
backgroundMenu = pygame.image.load(resources.BACKGROUND_MENU)
backgroundJogo = pygame.image.load(resources.BACKGROUND_JOGO)
baralhoImg = pygame.image.load(resources.BARALHO)
logo = (resources.spriteLogo())
imgProjetoK = pygame.image.load(resources.PROJETOK)
imgPKFatec = pygame.image.load(resources.PROJETOK_FATEC)
imgEspelho = pygame.image.load(resources.ESPELHO)
fundoCarta = pygame.image.load(resources.FUNDO_CARTA)
fundoAvatarBg = pygame.image.load(resources.FUNDO_AVATAR)
spriteSheetAvatar = (resources.spriteAvatar())
bandeira = resources.bandeiraSprite()
paginaPortugues = resources.pagina_portugues()
paginaIngles = resources.pagina_ingles()
cgInicial = (resources.animInicial())
left = pygame.image.load(resources.LEFT)
right = pygame.image.load(resources.RIGHT)
leftRegras = pygame.image.load(resources.LEFT)
rightRegres = pygame.image.load(resources.RIGHT)

turnoImg = pygame.image.load(resources.TURNO)
vencedorBg = pygame.image.load(resources.VENCEDOR_BG)
lobbyBg = pygame.image.load(resources.LOBBY_BG)
imgRegras = (resources.spriteRegrasPt())
imgRegrasIngles = (resources.spriteRegrasIng())

screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption(config.TITULO)
clock = pygame.time.Clock()

pygame.mixer.init()
pygame.mixer.music.load(resources.MENU_MUSIC)
fxCardAnim = pygame.mixer.Sound(resources.FX_CARD)
fxBtn = pygame.mixer.Sound(resources.FX_CLICK)


global cronometro1, cronometro2, contadorG, pagina
cronometro1, cronometro2, contadorG = 0, 0, 0

global paginaRegras

paginaRegras = 0

global s, host, porta, instruction, player, multiplayer, estadoJogo, animator, animation

pagina = 0
animator = 0
animation = 0
estadoJogo = 0
multiplayer = True
instruction = [['', '', ''], ['', '', ''], ['', '', ''], ['', '', '']]
player = None
porta = 8291
host = 'localhost'
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

pygame.font.init()


def enterNomePlayer(idioma, nome, idiomaTexto):
    font = pygame.font.Font('font/Pixellari.ttf', 45)
    font2 = pygame.font.Font('font/Pixellari.ttf', 35)

    mouse = pygame.mouse.get_pos() 
    screen.fill(resources.PRETO) 

    retBandeira = pygame.Rect(menuDic['posBandeira'][0], menuDic['posBandeira'][1], bandeira[0].get_width(), bandeira[0].get_height())

    if idioma['idioma'] == 'portugues':
        if retBandeira.collidepoint(mouse[0], mouse[1]):
            screen.blit(bandeira[3], menuDic['posBandeira'])
        else:
            screen.blit(bandeira[2], menuDic['posBandeira'])
    else:
        if retBandeira.collidepoint(mouse[0], mouse[1]):
            screen.blit(bandeira[1], menuDic['posBandeira'])
        else:
            screen.blit(bandeira[0], menuDic['posBandeira'])

    texto = font.render(nome, 1, resources.BRANCO)

    screen.blit(font2.render((idioma['contrato1']), 1, resources.BRANCO), menuDic['contrato1'])
    screen.blit(font2.render((idioma['contrato2']), 1, resources.BRANCO), menuDic['contrato2'])
    screen.blit(font2.render((idioma['contrato3']), 1, resources.BRANCO), menuDic['contrato3'])
    screen.blit(font2.render((idioma['contrato4']), 1, resources.BRANCO), menuDic['contrato4'])
    screen.blit(font2.render((idioma['contrato5']), 1, resources.BRANCO), menuDic['contrato5'])

    nome = nome.split()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if retBandeira.collidepoint(mouse):
                if idioma['idioma'] == 'portugues':
                    idioma = textos.dicIngles
                    idiomaTexto = 'Inglês'
                else:
                    idioma = textos.dicPortugues 
                    idiomaTexto = 'Português' 

        if event.type == pygame.KEYDOWN:
            if event.unicode.isalpha() or event.unicode.isnumeric():
                fxBtn.play()
                for i in range(len(nome)):
                    if nome[i] == '_':
                        nome[i] = event.unicode
                        break
            if event.key == pygame.K_BACKSPACE:
                fxBtn.play()
                for i in range(len(nome)):
                    if nome[i] == '_':
                        nome[i - 1] = '_'
                        break
                    elif i == (len(nome) - 1):
                        nome[i] = '_'
            if event.key == pygame.K_SPACE:
                fxBtn.play()
                for i in range(len(nome)):
                    if nome[i] == '_':
                        nome[i] = '-'
                        break
            if event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER:
                fxBtn.play()
                nomeTemp = ' '.join(str(nome) for nome in nome)
                nomeTemp = nomeTemp.replace('_', '')
                nomeTemp = nomeTemp.replace(' ', '')
                if nomeTemp != '':
                    return 'menu', nomeTemp, idioma, idiomaTexto 

    nomeTemp = ' '.join(str(nome) for nome in nome)
    screen.blit(texto, menuDic['nomeTexto'])

    return 'escreverNome', nomeTemp, idioma, idiomaTexto

"""Metodo responsavel por controlar todo o processamento do menu principial, suas animacoes, 
   definicoes de fontes, colisoes, chamada das telas de configuracao, avatar e inicio do jogo"""
def menu(idioma, nome, avatarJogador, estadoMenu):
    global animator, multiplayer

    if pygame.mixer.music.get_busy():
        pass
    else:
        pygame.mixer.music.play()
    font = pygame.font.Font('font/Pixellari.ttf', 45)
    font2 = pygame.font.Font('font/Pixellari.ttf', 35)
    font3 = pygame.font.Font('font/Pixellari.ttf', 25)
    mouse = pygame.mouse.get_pos()
    screen.blit(backgroundMenu, (0, 0))
    screen.blit(imgEspelho, menuDic['posEspelho'])
    botaoRetIniciar = pygame.Rect(menuDic['btStart'][0][0], menuDic['btStart'][0][1], botao.get_width(), botao.get_height())
    botaoRetConfigurar = pygame.Rect(menuDic['btConfig'][0][0], menuDic['btConfig'][0][1], botao.get_width(), botao.get_height())
    botaoRetAvatar = pygame.Rect(menuDic['btAvatar'][0][0], menuDic['btAvatar'][0][1], botao.get_width(), botao.get_height())

    botaoRetSingle = pygame.Rect(menuDic['btnSingle'][0], menuDic['btnSingle'][1], botao.get_width(), botao.get_height())
    botaoRetMult = pygame.Rect(menuDic['btnMult'][0], menuDic['btnMult'][1], botao.get_width(), botao.get_height())

    if estadoMenu == 'jogar':
        if botaoRetSingle.collidepoint(mouse):
            screen.blit(botao2, menuDic['btnSingle'])
        else:
            screen.blit(botao, menuDic['btnSingle'])
        if botaoRetMult.collidepoint(mouse):
            screen.blit(botao2, menuDic['btnMult'])
        else:
            screen.blit(botao, menuDic['btnMult'])
        screen.blit(font3.render((idioma['umJogador']), 1, resources.BRANCO), menuDic['txtSinglePlayer'])
        screen.blit(font3.render((idioma['multiJogador']), 1, resources.BRANCO), menuDic['txtMultiPlayer'])

    if botaoRetIniciar.collidepoint(mouse):
        screen.blit(botao2, menuDic['btStart'][0])
    else:
        screen.blit(botao, menuDic['btStart'][0])
    screen.blit(font2.render((idioma['iniciar']), 1, resources.BRANCO), (menuDic['btStart'][1]))

    if botaoRetConfigurar.collidepoint(mouse):
        screen.blit(botao2, menuDic['btConfig'][0])
    else:
        screen.blit(botao, menuDic['btConfig'][0])
    screen.blit(font2.render((idioma['configurar']), 1, resources.BRANCO), menuDic['btConfig'][1])

    if botaoRetAvatar.collidepoint(mouse):
        screen.blit(botao2, menuDic['btAvatar'][0])
    else:
        screen.blit(botao, menuDic['btAvatar'][0])
    screen.blit(font2.render((idioma['avatar']), 1, resources.BRANCO), menuDic['btAvatar'][1])

    screen.blit(font.render(nome, 1, resources.BRANCO), menuDic['nomeMenu'])

    if animator < 30:
        screen.blit(pygame.transform.flip(pygame.transform.scale2x(spriteSheetAvatar[avatarJogador]), -1, 0), menuDic['posAvatarMenu'])
    else:
        screen.blit(pygame.transform.flip(pygame.transform.scale2x(spriteSheetAvatar[avatarJogador + 1]), -1, 0), menuDic['posAvatarMenu'])

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if botaoRetIniciar.collidepoint(mouse):
                fxBtn.play()
                estadoMenu = 'jogar'
            elif botaoRetConfigurar.collidepoint(mouse):
                fxBtn.play()
                estadoMenu = ''
                return 'configuracao', avatarJogador, estadoMenu

            elif botaoRetAvatar.collidepoint(mouse):
                fxBtn.play()
                estadoMenu = ''
                return 'avatar', avatarJogador, estadoMenu

            if estadoMenu == 'jogar':
                if botaoRetSingle.collidepoint(mouse):
                    multiplayer = False
                    fxBtn.play()
                    estadoMenu = ''
                    return 'jogandoSingle', avatarJogador, estadoMenu
                elif botaoRetMult.collidepoint(mouse):
                    multiplayer = True
                    fxBtn.play()
                    estadoMenu = ''
                    return 'aguardandoJogadores', avatarJogador, estadoMenu

    return 'menu', avatarJogador, estadoMenu


def configuracao(idioma, idiomaTexto, nome):
    global estadoJogo, paginaRegras

    paginaRegras = paginaRegras

    if pygame.mixer.music.get_busy():
        pass
    else:
        pygame.mixer.music.play()

    font = pygame.font.Font('font/Pixellari.ttf', 45)
    font2 = pygame.font.Font('font/Pixellari.ttf', 35)
    font3 = pygame.font.Font('font/Pixellari.ttf', 25)
    font4 = pygame.font.Font('font/Pixellari.ttf', 20)

    mouse = pygame.mouse.get_pos()

    screen.blit(backgroundMenu, (0, 0))


    botaoRetVoltar = pygame.Rect(menuDic['btVoltar'][0][0], menuDic['btVoltar'][0][1], botao.get_width(), botao.get_height())
    botaoRetLeft = pygame.Rect(menuDic['btLeft'][0], menuDic['btLeft'][1], left.get_width(), left.get_height())
    botaoRetRight = pygame.Rect(menuDic['btRight'][0], menuDic['btRight'][1], right.get_width(), right.get_height())
    botaoRetLeftRegras = pygame.Rect(690,380, leftRegras.get_width(), leftRegras.get_height())
    botaoRetRightRegras = pygame.Rect(730,380, rightRegres.get_width(), rightRegres.get_height())
    botaoRetMudarNome = pygame.Rect(menuDic['btnMudarNome'][0], menuDic['btnMudarNome'][1], botao.get_width(), botao.get_height())
    botaoRetCredito = pygame.Rect(menuDic['btnCredito'][0], menuDic['btnCredito'][1], botao.get_width(), botao.get_height())
    botaoRetRegras = pygame.Rect(menuDic['btnRegras'][0], menuDic['btnRegras'][1], botao.get_width(), botao.get_height())

    screen.blit(left, menuDic['btLeft'])
    screen.blit(right, menuDic['btRight'])
    screen.blit(font.render(idiomaTexto, 1, resources.BRANCO), menuDic['opcaoIdioma'])

    if botaoRetVoltar.collidepoint(mouse):
        screen.blit(botao2, menuDic['btVoltar'][0])
    else:
        screen.blit(botao, menuDic['btVoltar'][0])
    screen.blit(font2.render(idioma['voltar'], 1, resources.BRANCO), menuDic['btVoltar'][1])

    if botaoRetMudarNome.collidepoint(mouse):
        screen.blit(botao2, menuDic['btnMudarNome'])
    else:
        screen.blit(botao, menuDic['btnMudarNome'])

    if botaoRetCredito.collidepoint(mouse):
        screen.blit(botao2, menuDic['btnCredito'])
    else:
        screen.blit(botao, menuDic['btnCredito'])

    if botaoRetRegras.collidepoint(mouse):
        screen.blit(botao2, menuDic['btnRegras'])
    else:
        screen.blit(botao, menuDic['btnRegras'])

    screen.blit(font2.render(idioma['regras'], 1, resources.BRANCO), menuDic['txtRegras'])
    screen.blit(font2.render(idioma['mudarNome'], 1, resources.BRANCO), menuDic['txtMudarNome'])
    screen.blit(font2.render(idioma['credito'], 1, resources.BRANCO), menuDic['txtCreditos'])

    if estadoJogo == 'creditos':
        screen.blit(font3.render('Diego Munhoz', 1, resources.BRANCO), (300, 220))
        screen.blit(font4.render('Programing, Compress Programing', 1, resources.BRANCO), (325, 245))
        screen.blit(font3.render('Thiago Zacarias da Silva', 1, resources.BRANCO), (300, 268))
        screen.blit(font4.render('Gameplay Programing, Network Programing', 1, resources.BRANCO), (325, 289))
        screen.blit(font3.render('Victor Ponciano', 1, resources.BRANCO), (300, 316))
        screen.blit(font4.render('Programing, Game design, Art', 1, resources.BRANCO), (325, 335))
        screen.blit(font3.render('BGM', 1, resources.BRANCO), (260, 356))
        screen.blit(font4.render('Jazz in Paris-Media Right Productions-YouTube Audio Library', 1, resources.BRANCO), (265, 375))
        screen.blit(font4.render('Bitters At The Saloon-Bird Creek-YouTube Audio Library', 1, resources.BRANCO),(265, 405))
        screen.blit(font3.render('SFX', 1, resources.BRANCO), (300, 445))
        screen.blit(font4.render('site FreeSFX - www.freesfx.co.uk', 1, resources.BRANCO),
                    (325, 475))

    if estadoJogo == 'regras':
        if idioma['idioma'] == 'ingles':
            screen.blit(imgRegrasIngles[paginaRegras], menuDic['imgRegras'])
        else:
            screen.blit(imgRegras[paginaRegras], menuDic['imgRegras'])
        screen.blit(leftRegras, (690,380))
        screen.blit(rightRegres, (730,380))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if botaoRetMudarNome.collidepoint(mouse):
                fxBtn.play()
                nome = '_ _ _ _ _ _'
                estadoJogo = 0
                return 'escreverNome', idiomaTexto, idioma, nome
            elif botaoRetCredito.collidepoint(mouse):
                fxBtn.play()
                if estadoJogo == 0:
                    estadoJogo = 'creditos'
                else:
                    estadoJogo = 0
            elif botaoRetRegras.collidepoint(mouse):
                fxBtn.play()
                if estadoJogo == 0:
                    estadoJogo = 'regras'
                    paginaRegras = 0
                else:
                    estadoJogo = 0
            elif botaoRetVoltar.collidepoint(mouse):
                fxBtn.play()
                estadoJogo = 0
                return 'menu', idiomaTexto, idioma, nome
            elif botaoRetLeft.collidepoint(mouse) or botaoRetRight.collidepoint(mouse):
                fxBtn.play()
                if idiomaTexto == 'Português':
                    idiomaTexto = 'Inglês'
                    idioma = textos.dicIngles
                else:
                    idiomaTexto = 'Português'
                    idioma = textos.dicPortugues
            elif botaoRetLeftRegras.collidepoint(mouse) :
                fxBtn.play()
                if paginaRegras == 0:
                    paginaRegras = 3
                else:
                    paginaRegras -=1
            elif botaoRetRightRegras.collidepoint(mouse):
                fxBtn.play()
                if paginaRegras == 3:
                    paginaRegras = 0
                else:
                    paginaRegras +=1

        screen.blit(font.render(idiomaTexto, 1, resources.BRANCO), menuDic['opcaoIdioma'])


    return 'configuracao', idiomaTexto, idioma, nome


def avatar(idioma, avatarJogador):
    global pagina

    pagina = int(avatarJogador/2)

    if pygame.mixer.music.get_busy():
        pass
    else:
        pygame.mixer.music.play()

    font = pygame.font.Font('font/Pixellari.ttf', 35)
    mouse = pygame.mouse.get_pos()

    screen.blit(backgroundMenu, (0, 0))

    botaoRetVoltar = pygame.Rect(menuDic['btVoltar'][0][0], menuDic['btVoltar'][0][1], botao.get_width(), botao.get_height())
    botaoRetLeft = pygame.Rect(menuDic['btLeftAvatar'][0], menuDic['btLeftAvatar'][1], left.get_width(), left.get_height())
    botaoRetRight = pygame.Rect(menuDic['btRightAvatar'][0], menuDic['btRightAvatar'][1], right.get_width(), right.get_height())

    if idioma['idioma'] == 'portugues':
        screen.blit(paginaPortugues[pagina], (0, 0))
    else:
        screen.blit(paginaIngles[pagina], (0, 0))

    if botaoRetVoltar.collidepoint(mouse):
        screen.blit(botao2, menuDic['btVoltar'][0])
    else:
        screen.blit(botao, menuDic['btVoltar'][0])

    screen.blit(font.render(idioma['voltar'], 1, resources.BRANCO), menuDic['btVoltar'][1])
    screen.blit(left, menuDic['btLeftAvatar'])
    screen.blit(right, menuDic['btRightAvatar'])

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if botaoRetVoltar.collidepoint(mouse):
                fxBtn.play()
                return 'menu', avatarJogador
            if botaoRetLeft.collidepoint(mouse):
                fxBtn.play()
                if 10 > avatarJogador >= 2:
                    avatarJogador -= 2
                    pagina -= 1
                else:
                    avatarJogador = 8
                    pagina = 4

            if botaoRetRight.collidepoint(mouse):
                fxBtn.play()
                if avatarJogador < 8:
                    avatarJogador += 2
                    pagina += 1
                else:
                    avatarJogador = 0
                    pagina = 0

    return 'avatar', avatarJogador


def entregarCartas(baralho, cartasPlayer=[]):
    global s, host, porta, instruction, player, multiplayer

    if multiplayer:
        if player == 0:
            cartasPlayer[0] = int(instruction[1])
            cartasPlayer[1] = int(instruction[2])
            cartasPlayer[2] = int(instruction[3])
        elif player == 1:
            cartasPlayer[0] = int(instruction[4])
            cartasPlayer[1] = int(instruction[5])
            cartasPlayer[2] = int(instruction[6])
        else:
            cartasPlayer[0] = int(instruction[7])
            cartasPlayer[1] = int(instruction[8])
            cartasPlayer[2] = int(instruction[9])

        return cartasPlayer, baralho
    else:
        cartasPlayer = [[None, None, None], [None, None, None], [None, None, None]]

        for i in range(3):
            for j in range(3):
                while True:
                    cartasPlayer[i][j] = random.randint(0, len(baralho) - 1)
                    if baralho[cartasPlayer[i][j]] != None:
                        break
                baralho[cartasPlayer[i][j]] = None

        return cartasPlayer, baralho

def inverterPosCartas(spritesBaralho, cartasInverter=[]):
    temp = [0] * 4
    for i in range(4):
        temp[i] = spritesBaralho[cartasInverter[i]]
    while i >= 0:
        spritesBaralho.remove(spritesBaralho[cartasInverter[i]])
        i -= 1
    for i in range(4):
        spritesBaralho.append(temp[i])

    return spritesBaralho

def virarCarta(baralho, spritesBaralho):
    global s, host, porta, instruction, player, multiplayer

    if multiplayer:
        cartaVirada = int(instruction[10])
    else:
        while True:
            cartaVirada = random.randint(0, len(baralho) - 1)
            if baralho[cartaVirada] != None:
                break
        baralho[cartaVirada] = None
    if 0 <= cartaVirada <= 3:
        spritesBaralho = inverterPosCartas(spritesBaralho, [4, 5, 6, 7])
    elif 4 <= cartaVirada <= 7:
        spritesBaralho = inverterPosCartas(spritesBaralho, [8, 9, 10, 11])
    elif 8 <= cartaVirada <= 11:
        spritesBaralho = inverterPosCartas(spritesBaralho, [12, 13, 14, 15])
    elif 12 <= cartaVirada <= 15:
        spritesBaralho = inverterPosCartas(spritesBaralho, [16, 17, 18, 19])
    elif 16 <= cartaVirada <= 19:
        spritesBaralho = inverterPosCartas(spritesBaralho, [20, 21, 22, 23])
    elif 20 <= cartaVirada <= 23:
        spritesBaralho = inverterPosCartas(spritesBaralho, [0, 1, 2, 3])
        cartaVirada -= 4 
    return cartaVirada, baralho, spritesBaralho 

def distribuirCartas(distribuir_cartas, animacaoCarta, cartaVirada, baralho, cartasComJogador, spritesBaralho):

    global s, host, porta, instruction, player, multiplayer
    if multiplayer:
        instruction[24] = 1
        if distribuir_cartas and animacaoCarta[1] < 9:
            screen.blit(fundoCarta, (animacaoCarta[0], 290))

            animacaoCarta[0] += 10
            if animacaoCarta[0] > 300:
                fxCardAnim.play()
                animacaoCarta[0] = 192
                animacaoCarta[1] += 1
            if animacaoCarta[0] < 100:
                fxCardAnim.play()
                animacaoCarta[0] = 192
                animacaoCarta[1] += 1
            if animacaoCarta[1] >= 1:
                screen.blit(fundoCarta, jogoDic['posCartaPlayer1'][0])
            if animacaoCarta[1] >= 2:
                screen.blit(fundoCarta, jogoDic['posCartaPlayer1'][1])
            if animacaoCarta[1] >= 3:
                screen.blit(fundoCarta, jogoDic['posCartaPlayer1'][2])
            if animacaoCarta[1] >= 4:
                screen.blit(pygame.transform.rotate(fundoCarta, 90), jogoDic['posCartaPlayer2'][0])
            if animacaoCarta[1] >= 5:
                screen.blit(pygame.transform.rotate(fundoCarta, 90), jogoDic['posCartaPlayer2'][1])
            if animacaoCarta[1] >= 6:
                screen.blit(pygame.transform.rotate(fundoCarta, 90), jogoDic['posCartaPlayer2'][2])
                animacaoCarta[0] -= 20
            if animacaoCarta[1] >= 7:
                screen.blit(pygame.transform.rotate(fundoCarta, -90), jogoDic['posCartaPlayer3'][0])
            if animacaoCarta[1] >= 8:
                screen.blit(pygame.transform.rotate(fundoCarta, -90), jogoDic['posCartaPlayer3'][1])
            if animacaoCarta[1] >= 9:
                screen.blit(pygame.transform.rotate(fundoCarta, -90), jogoDic['posCartaPlayer3'][2])
                distribuir_cartas = False
                cartasComJogador, baralho = entregarCartas(baralho, cartasComJogador)
                cartaVirada, baralho, spritesBaralho = virarCarta(baralho, spritesBaralho)

        return distribuir_cartas, animacaoCarta, cartaVirada, baralho, cartasComJogador, spritesBaralho

    else:
        if distribuir_cartas and animacaoCarta[1] < 9:
            screen.blit(fundoCarta, (animacaoCarta[0], 290))
            animacaoCarta[0] += 10
            if animacaoCarta[0] > 300:
                animacaoCarta[0] = 192
                fxCardAnim.play()
                animacaoCarta[1] += 1 
            if animacaoCarta[0] < 100:
                fxCardAnim.play()
                animacaoCarta[0] = 192
                animacaoCarta[1] += 1

            if animacaoCarta[1] >= 1:
                screen.blit(fundoCarta, jogoDic['posCartaPlayer1'][0])
            if animacaoCarta[1] >= 2:
                screen.blit(fundoCarta, jogoDic['posCartaPlayer1'][1])
            if animacaoCarta[1] >= 3:
                screen.blit(fundoCarta, jogoDic['posCartaPlayer1'][2])

            if animacaoCarta[1] >= 4:
                screen.blit(pygame.transform.rotate(fundoCarta, 90), jogoDic['posCartaPlayer2'][0])
            if animacaoCarta[1] >= 5:
                screen.blit(pygame.transform.rotate(fundoCarta, 90), jogoDic['posCartaPlayer2'][1])
            if animacaoCarta[1] >= 6:
                screen.blit(pygame.transform.rotate(fundoCarta, 90), jogoDic['posCartaPlayer2'][2])
                animacaoCarta[0] -= 20
            if animacaoCarta[1] >= 7:
                screen.blit(pygame.transform.rotate(fundoCarta, -90), jogoDic['posCartaPlayer3'][0])
            if animacaoCarta[1] >= 8:
                screen.blit(pygame.transform.rotate(fundoCarta, -90), jogoDic['posCartaPlayer3'][1])
            if animacaoCarta[1] >= 9:
                screen.blit(pygame.transform.rotate(fundoCarta, -90), jogoDic['posCartaPlayer3'][2])
                distribuir_cartas = False
                cartasComJogador, baralho = entregarCartas(baralho, cartasComJogador)
                cartaVirada, baralho, spritesBaralho = virarCarta(baralho, spritesBaralho)

        return distribuir_cartas, animacaoCarta, cartaVirada, baralho, cartasComJogador, spritesBaralho 

def atribuirPontos(rodada, pontosJogador, vencedor):
    global estadoJogo
    if rodada == 1:
        pontosJogador[vencedor] += 3
    elif rodada == 2:
        pontosJogador[vencedor] += 2
    else:
        pontosJogador[vencedor] += 1
    if pontosJogador[vencedor] == 12:
        estadoJogo = 'vencedor'
    elif pontosJogador[vencedor] > 12:
        pontosJogador[vencedor] = 0
    return pontosJogador


def verificarVencedorRodada(cartasJogadas, rodada, pontosJogador):
    forcaCarta = [1, 1, 1, 1,
                  2, 2, 2, 2,
                  3, 3, 3, 3,
                  4, 4, 4, 4,
                  5, 5, 5, 5,
                  6, 6, 6, 6]
    if forcaCarta[cartasJogadas[0]] != 6 and forcaCarta[cartasJogadas[1]] != 6 and forcaCarta[cartasJogadas[2] != 6]:
        if cartasJogadas[0] > cartasJogadas[1] and cartasJogadas[0] > cartasJogadas[2]:
            if forcaCarta[cartasJogadas[0]] != forcaCarta[cartasJogadas[1]] and forcaCarta[cartasJogadas[0]] != forcaCarta[cartasJogadas[2]]:
                pontosJogador = atribuirPontos(rodada, pontosJogador, 0)
            else:
                pass
        elif cartasJogadas[1] > cartasJogadas[0] and cartasJogadas[1] > cartasJogadas[2]:
            if forcaCarta[cartasJogadas[1]] != forcaCarta[cartasJogadas[0]] and forcaCarta[cartasJogadas[1]] != forcaCarta[cartasJogadas[2]]:
                pontosJogador = atribuirPontos(rodada, pontosJogador, 1)
            else:
                pass
        elif cartasJogadas[2] > cartasJogadas[0] and cartasJogadas[2] > cartasJogadas[1]:
            if forcaCarta[cartasJogadas[2]] != forcaCarta[cartasJogadas[0]] and forcaCarta[cartasJogadas[2]] != forcaCarta[cartasJogadas[1]]:
                pontosJogador = atribuirPontos(rodada, pontosJogador, 2)
            else:
                pass
    else:
        if cartasJogadas[0] > cartasJogadas[1] and cartasJogadas[0] > cartasJogadas[2]:
            pontosJogador = atribuirPontos(rodada, pontosJogador, 0)
        elif cartasJogadas[1] > cartasJogadas[0] and cartasJogadas[1] > cartasJogadas[2]:
            pontosJogador = atribuirPontos(rodada, pontosJogador, 1)
        else:
            pontosJogador = atribuirPontos(rodada, pontosJogador, 2)

    return pontosJogador

def jogarMult(idioma, nome, baralho, turno, rodada, pontosJogador, cartasComJogador, cartasJogadas, cartaVirada, distribuir_cartas, animacaoCarta, spritesBaralho, avatarJogador, tempoExibicaoRodada, conectionC):

    global s, host, porta, instruction, player, cronometro1, estadoJogo, cronometro2, animator

    if pygame.mixer.music.get_busy():
        pass
    else:
        pygame.mixer.music.play()

    try:
        instruction = s.recv(1024)
        instruction = instruction.decode('utf-8')
        instruction = instruction.split(',')
    except socket.error:
        main()

    font = pygame.font.Font('font/Pixellari.ttf', 45)
    font2 = pygame.font.Font('font/Pixellari.ttf', 35)
    font3 = pygame.font.Font('font/Pixellari.ttf', 25)

    mouse = pygame.mouse.get_pos()
    screen.blit(backgroundJogo, (0, 0))

    if distribuir_cartas:

        for i in range(3):
            screen.blit(fundoAvatarBg, jogoDic['posBgFundoAvatar'][i])

        if player == 0:
            if animator < 30:
                screen.blit(pygame.transform.flip(spriteSheetAvatar[int(instruction[17])], -1, 0), jogoDic['posAvatar'][0])
                screen.blit(pygame.transform.flip(spriteSheetAvatar[int(instruction[18])], -1, 0), jogoDic['posAvatar'][1])
                screen.blit(spriteSheetAvatar[int(instruction[19])], jogoDic['posAvatar'][2])
            else:
                screen.blit(pygame.transform.flip(spriteSheetAvatar[int(instruction[17]) + 1], -1, 0),
                            jogoDic['posAvatar'][0])
                screen.blit(pygame.transform.flip(spriteSheetAvatar[int(instruction[18]) + 1], -1, 0),
                            jogoDic['posAvatar'][1])
                screen.blit(spriteSheetAvatar[int(instruction[19]) + 1], jogoDic['posAvatar'][2])

            screen.blit(font.render(instruction[20], 1, resources.BRANCO), jogoDic['posPontoJogador1'])
            screen.blit(font.render(instruction[21], 1, resources.BRANCO), jogoDic['posPontoJogador2'])
            screen.blit(font.render(instruction[22], 1, resources.BRANCO), jogoDic['posPontoJogador3'])
            screen.blit(font2.render(instruction[14], 1, resources.BRANCO), jogoDic['posTextoNomeJogador'][0])
            screen.blit(font2.render(instruction[15], 1, resources.BRANCO), jogoDic['posTextoNomeJogador'][1])
            screen.blit(font2.render(instruction[16], 1, resources.BRANCO), jogoDic['posTextoNomeJogador'][2])
        elif player == 1:
            if animator < 30:
                screen.blit(pygame.transform.flip(spriteSheetAvatar[int(instruction[18])], -1, 0), jogoDic['posAvatar'][0])
                screen.blit(pygame.transform.flip(spriteSheetAvatar[int(instruction[19])], -1, 0), jogoDic['posAvatar'][1])
                screen.blit(spriteSheetAvatar[int(instruction[17])], jogoDic['posAvatar'][2])
            else:
                screen.blit(pygame.transform.flip(spriteSheetAvatar[int(instruction[18]) + 1], -1, 0),
                            jogoDic['posAvatar'][0])
                screen.blit(pygame.transform.flip(spriteSheetAvatar[int(instruction[19]) + 1], -1, 0),
                            jogoDic['posAvatar'][1])
                screen.blit(spriteSheetAvatar[int(instruction[17]) + 1], jogoDic['posAvatar'][2])

            screen.blit(font.render(instruction[21], 1, resources.BRANCO), jogoDic['posPontoJogador1'])
            screen.blit(font.render(instruction[22], 1, resources.BRANCO), jogoDic['posPontoJogador2'])
            screen.blit(font.render(instruction[20], 1, resources.BRANCO), jogoDic['posPontoJogador3'])

            screen.blit(font2.render(instruction[15], 1, resources.BRANCO), jogoDic['posTextoNomeJogador'][0])
            screen.blit(font2.render(instruction[16], 1, resources.BRANCO), jogoDic['posTextoNomeJogador'][1])
            screen.blit(font2.render(instruction[14], 1, resources.BRANCO), jogoDic['posTextoNomeJogador'][2])
        elif player == 2:
            if animator < 30:
                screen.blit(pygame.transform.flip(spriteSheetAvatar[int(instruction[19])], -1, 0), jogoDic['posAvatar'][0])
                screen.blit(pygame.transform.flip(spriteSheetAvatar[int(instruction[17])], -1, 0), jogoDic['posAvatar'][1])
                screen.blit(spriteSheetAvatar[int(instruction[18])], jogoDic['posAvatar'][2])
            else:
                screen.blit(pygame.transform.flip(spriteSheetAvatar[int(instruction[19]) + 1], -1, 0),
                            jogoDic['posAvatar'][0])
                screen.blit(pygame.transform.flip(spriteSheetAvatar[int(instruction[17]) + 1], -1, 0),
                            jogoDic['posAvatar'][1])
                screen.blit(spriteSheetAvatar[int(instruction[18]) + 1], jogoDic['posAvatar'][2])

            screen.blit(font.render(instruction[22], 1, resources.BRANCO), jogoDic['posPontoJogador1'])
            screen.blit(font.render(instruction[20], 1, resources.BRANCO), jogoDic['posPontoJogador2'])
            screen.blit(font.render(instruction[21], 1, resources.BRANCO), jogoDic['posPontoJogador3'])

            screen.blit(font2.render(instruction[16], 1, resources.BRANCO), jogoDic['posTextoNomeJogador'][0])
            screen.blit(font2.render(instruction[14], 1, resources.BRANCO), jogoDic['posTextoNomeJogador'][1])
            screen.blit(font2.render(instruction[15], 1, resources.BRANCO), jogoDic['posTextoNomeJogador'][2])

        screen.blit(font.render(idioma['embaralhar'], 1, resources.BRANCO), (jogoDic['posTextoRodada'][0] - 40, jogoDic['posTextoRodada'][1]))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
        distribuir_cartas, animacaoCarta, cartaVirada, baralho, cartasComJogador, spritesBaralho = distribuirCartas(distribuir_cartas, animacaoCarta, cartaVirada, baralho, cartasComJogador, spritesBaralho)

    else:
        retCartas = [None] * 3
        for i in range(3):
            retCartas[i] = pygame.Rect(jogoDic['posCartaPlayer1'][i][0], jogoDic['posCartaPlayer1'][i][1],
                                       spritesBaralho[0].get_width(), spritesBaralho[0].get_height())

        for i in range(3):
            if cartasComJogador[i] != None:
                if retCartas[i].collidepoint(mouse[0], mouse[1]):
                    screen.blit(spritesBaralho[cartasComJogador[i]], (jogoDic['posCartaPlayer1'][i][0], jogoDic['posCartaPlayer1'][i][1] - 15))
                    if player == 0:
                        if i == 0:
                            instruction[26] = 1
                        elif i == 1:
                            instruction[27] = 1
                        else:
                            instruction[28] = 1
                    elif player == 1:
                        if i == 0:
                            instruction[29] = 1
                        elif i == 1:
                            instruction[30] = 1
                        else:
                            instruction[31] = 1
                    else:
                        if i == 0:
                            instruction[32] = 1
                        elif i == 1:
                            instruction[33] = 1
                        else:
                            instruction[34] = 1
                else:
                    screen.blit(spritesBaralho[cartasComJogador[i]], jogoDic['posCartaPlayer1'][i])
                    if player == 0:
                        if i == 0:
                            instruction[26] = -1
                        elif i == 1:
                            instruction[27] = -1
                        else:
                            instruction[28] = -1
                    elif player == 1:
                        if i == 0:
                            instruction[29] = -1
                        elif i == 1:
                            instruction[30] = -1
                        else:
                            instruction[31] = -1
                    else:
                        if i == 0:
                            instruction[32] = -1
                        elif i == 1:
                            instruction[33] = -1
                        else:
                            instruction[34] = -1

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                estadoJogo = 'sair'
                instruction[24] = -10
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if player == int(instruction[0]):
                    if retCartas[0].collidepoint(mouse[0], mouse[1]) and cartasComJogador[0] != None:
                        fxCardAnim.play()
                        if int(instruction[11]) == -1:
                            instruction[11] = cartasComJogador[0]
                        elif int(instruction[12]) == -1:
                            instruction[12] = cartasComJogador[0]
                        elif int(instruction[13]) == -1:
                            instruction[13] = cartasComJogador[0]
                        cartasComJogador[0] = None
                        if int(instruction[11]) == -1 or int(instruction[12]) == -1 or int(instruction[13]) == -1:
                            if player == 0:
                                instruction[0] = 1
                                instruction[1] = -1
                            elif player == 1:
                                instruction[0] = 2
                                instruction[4] = -1
                            elif player == 2:
                                instruction[0] = 0
                                instruction[7] = -1
                    elif retCartas[1].collidepoint(mouse[0], mouse[1]) and cartasComJogador[1] != None:
                        fxCardAnim.play()
                        if int(instruction[11]) == -1:
                            instruction[11] = cartasComJogador[1]
                        elif int(instruction[12]) == -1:
                            instruction[12] = cartasComJogador[1]
                        elif int(instruction[13]) == -1:
                            instruction[13] = cartasComJogador[1]
                        cartasComJogador[1] = None
                        if int(instruction[11]) == -1 or int(instruction[12]) == -1 or int(instruction[13]) == -1:
                            if player == 0:
                                instruction[0] = 1
                                instruction[2] = -1
                            elif player == 1:
                                instruction[0] = 2
                                instruction[5] = -1
                            elif player == 2:
                                instruction[0] = 0
                                instruction[8] = -1
                    elif retCartas[2].collidepoint(mouse[0], mouse[1]) and cartasComJogador[2] != None:
                        fxCardAnim.play()
                        if int(instruction[11]) == -1:
                            instruction[11] = cartasComJogador[2]
                        elif int(instruction[12]) == -1:
                            instruction[12] = cartasComJogador[2]
                        elif int(instruction[13]) == -1:
                            instruction[13] = cartasComJogador[2]
                        cartasComJogador[2] = None

                        if int(instruction[11]) == -1 or int(instruction[12]) == -1 or int(instruction[13]) == -1:
                            if player == 0:
                                instruction[0] = 1
                                instruction[3] = -1
                            elif player == 1:
                                instruction[0] = 2
                                instruction[6] = -1
                            elif player == 2:
                                instruction[0] = 0
                                instruction[9] = -1

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.mixer.music.load(resources.MENU_MUSIC)
                    instruction[24] = -10
        screen.blit(spritesBaralho[cartaVirada], jogoDic['posCartaVirada'])


        if player == 0:
            if int(instruction[4]) != -1:
                if int(instruction[29]) == -1:
                    screen.blit(pygame.transform.rotate(fundoCarta, 90), jogoDic['posCartaPlayer2'][0])
                else:
                    screen.blit(pygame.transform.rotate(fundoCarta, 90), (jogoDic['posCartaPlayer2'][0][0] - 15, jogoDic['posCartaPlayer2'][0][1]))

            if int(instruction[5]) != -1:
                if int(instruction[30]) == -1:
                    screen.blit(pygame.transform.rotate(fundoCarta, 90), jogoDic['posCartaPlayer2'][1])
                else:
                    screen.blit(pygame.transform.rotate(fundoCarta, 90), (jogoDic['posCartaPlayer2'][1][0] - 15, jogoDic['posCartaPlayer2'][1][1]))

            if int(instruction[6]) != -1:
                if int(instruction[31]) == -1:
                    screen.blit(pygame.transform.rotate(fundoCarta, 90), jogoDic['posCartaPlayer2'][2])
                else:
                    screen.blit(pygame.transform.rotate(fundoCarta, 90),
                                (jogoDic['posCartaPlayer2'][2][0] - 15, jogoDic['posCartaPlayer2'][2][1]))

            if int(instruction[7]) != -1:
                if int(instruction[32]) == -1:
                    screen.blit(pygame.transform.rotate(fundoCarta, -90), jogoDic['posCartaPlayer3'][0])
                else:
                    screen.blit(pygame.transform.rotate(fundoCarta, -90), (jogoDic['posCartaPlayer3'][0][0] + 15, jogoDic['posCartaPlayer3'][0][1]))

            if int(instruction[8]) != -1:
                if int(instruction[33]) == -1:
                    screen.blit(pygame.transform.rotate(fundoCarta, -90), jogoDic['posCartaPlayer3'][1])
                else:
                    screen.blit(pygame.transform.rotate(fundoCarta, -90), (jogoDic['posCartaPlayer3'][1][0] + 15, jogoDic['posCartaPlayer3'][1][1]))
            if int(instruction[9]) != -1:
                if int(instruction[34]) == -1:
                    screen.blit(pygame.transform.rotate(fundoCarta, -90), jogoDic['posCartaPlayer3'][2])
                else:
                    screen.blit(pygame.transform.rotate(fundoCarta, -90), (jogoDic['posCartaPlayer3'][2][0] + 15, jogoDic['posCartaPlayer3'][2][1]))
        elif player == 1:
            if int(instruction[7]) != -1:
                if int(instruction[32]) == -1:
                    screen.blit(pygame.transform.rotate(fundoCarta, 90), jogoDic['posCartaPlayer2'][0])
                else:
                    screen.blit(pygame.transform.rotate(fundoCarta, 90),
                                (jogoDic['posCartaPlayer2'][0][0] - 15, jogoDic['posCartaPlayer2'][0][1]))

            if int(instruction[8]) != -1:
                if int(instruction[33]) == -1:
                    screen.blit(pygame.transform.rotate(fundoCarta, 90), jogoDic['posCartaPlayer2'][1])
                else:
                    screen.blit(pygame.transform.rotate(fundoCarta, 90),
                                (jogoDic['posCartaPlayer2'][1][0] - 15, jogoDic['posCartaPlayer2'][1][1]))
            if int(instruction[9]) != -1:
                if int(instruction[34]) == -1:
                    screen.blit(pygame.transform.rotate(fundoCarta, 90), jogoDic['posCartaPlayer2'][2])
                else:
                    screen.blit(pygame.transform.rotate(fundoCarta, 90),
                                (jogoDic['posCartaPlayer2'][2][0] - 15, jogoDic['posCartaPlayer2'][2][1]))

            if int(instruction[1]) != -1:
                if int(instruction[26]) == -1:
                    screen.blit(pygame.transform.rotate(fundoCarta, -90), jogoDic['posCartaPlayer3'][0])
                else:
                    screen.blit(pygame.transform.rotate(fundoCarta, -90),
                                (jogoDic['posCartaPlayer3'][0][0] + 15, jogoDic['posCartaPlayer3'][0][1]))
            if int(instruction[2]) != -1:
                if int(instruction[27]) == -1:
                    screen.blit(pygame.transform.rotate(fundoCarta, -90), jogoDic['posCartaPlayer3'][1])
                else:
                    screen.blit(pygame.transform.rotate(fundoCarta, -90),
                                (jogoDic['posCartaPlayer3'][1][0] + 15, jogoDic['posCartaPlayer3'][1][1]))
            if int(instruction[3]) != -1:
                if int(instruction[28]) == -1:
                    screen.blit(pygame.transform.rotate(fundoCarta, -90), jogoDic['posCartaPlayer3'][2])
                else:
                    screen.blit(pygame.transform.rotate(fundoCarta, -90),
                                (jogoDic['posCartaPlayer3'][2][0] + 15, jogoDic['posCartaPlayer3'][2][1]))
        elif player == 2:
            if int(instruction[1]) != -1:
                if int(instruction[26]) == -1:
                    screen.blit(pygame.transform.rotate(fundoCarta, 90), jogoDic['posCartaPlayer2'][0])
                else:
                    screen.blit(pygame.transform.rotate(fundoCarta, 90),
                                (jogoDic['posCartaPlayer2'][0][0] - 15, jogoDic['posCartaPlayer2'][0][1]))
            if int(instruction[2]) != -1:
                if int(instruction[27]) == -1:
                    screen.blit(pygame.transform.rotate(fundoCarta, 90), jogoDic['posCartaPlayer2'][1])
                else:
                    screen.blit(pygame.transform.rotate(fundoCarta, 90),
                                (jogoDic['posCartaPlayer2'][1][0] - 15, jogoDic['posCartaPlayer2'][1][1]))
            if int(instruction[3]) != -1:
                if int(instruction[28]) == -1:
                    screen.blit(pygame.transform.rotate(fundoCarta, 90), jogoDic['posCartaPlayer2'][2])
                else:
                    screen.blit(pygame.transform.rotate(fundoCarta, 90),
                                (jogoDic['posCartaPlayer2'][2][0] - 15, jogoDic['posCartaPlayer2'][2][1]))

            if int(instruction[4]) != -1:
                if int(instruction[29]) == -1:
                    screen.blit(pygame.transform.rotate(fundoCarta, -90), jogoDic['posCartaPlayer3'][0])
                else:
                    screen.blit(pygame.transform.rotate(fundoCarta, -90),
                                (jogoDic['posCartaPlayer3'][0][0] + 15, jogoDic['posCartaPlayer3'][0][1]))
            if int(instruction[5]) != -1:
                if int(instruction[30]) == -1:
                    screen.blit(pygame.transform.rotate(fundoCarta, -90), jogoDic['posCartaPlayer3'][1])
                else:
                    screen.blit(pygame.transform.rotate(fundoCarta, -90),
                                (jogoDic['posCartaPlayer3'][0][0] + 15, jogoDic['posCartaPlayer3'][1][1]))
            if int(instruction[6]) != -1:
                if int(instruction[31]) == -1:
                    screen.blit(pygame.transform.rotate(fundoCarta, -90), jogoDic['posCartaPlayer3'][2])
                else:
                    screen.blit(pygame.transform.rotate(fundoCarta, -90),
                                (jogoDic['posCartaPlayer3'][2][0] + 15, jogoDic['posCartaPlayer3'][2][1]))


        temp = 0
        for i in range(11, 14):
            if int(instruction[i]) != -1:
                screen.blit(spritesBaralho[int(instruction[i])], jogoDic['posJogada'][temp])
                temp += 1


        for i in range(3):
            screen.blit(fundoAvatarBg, jogoDic['posBgFundoAvatar'][i])

        if player == 0:
            if animator < 30:
                screen.blit(pygame.transform.flip(spriteSheetAvatar[int(instruction[17])], -1, 0), jogoDic['posAvatar'][0])
                screen.blit(pygame.transform.flip(spriteSheetAvatar[int(instruction[18])], -1, 0), jogoDic['posAvatar'][1])
                screen.blit(spriteSheetAvatar[int(instruction[19])], jogoDic['posAvatar'][2])
            else:
                screen.blit(pygame.transform.flip(spriteSheetAvatar[int(instruction[17]) + 1], -1, 0),
                            jogoDic['posAvatar'][0])
                screen.blit(pygame.transform.flip(spriteSheetAvatar[int(instruction[18]) + 1], -1, 0),
                            jogoDic['posAvatar'][1])
                screen.blit(spriteSheetAvatar[int(instruction[19]) + 1], jogoDic['posAvatar'][2])

            screen.blit(font.render(instruction[20], 1, resources.BRANCO), jogoDic['posPontoJogador1'])
            screen.blit(font.render(instruction[21], 1, resources.BRANCO), jogoDic['posPontoJogador2'])
            screen.blit(font.render(instruction[22], 1, resources.BRANCO), jogoDic['posPontoJogador3'])

            screen.blit(font2.render(instruction[14], 1, resources.BRANCO), jogoDic['posTextoNomeJogador'][0])
            screen.blit(font2.render(instruction[15], 1, resources.BRANCO), jogoDic['posTextoNomeJogador'][1])
            screen.blit(font2.render(instruction[16], 1, resources.BRANCO), jogoDic['posTextoNomeJogador'][2])

            if int(instruction[0]) == 0:
                screen.blit(turnoImg, jogoDic['posAvatar'][0])
            elif int(instruction[0]) == 1:
                screen.blit(turnoImg, jogoDic['posAvatar'][1])
            else:
                screen.blit(turnoImg, jogoDic['posAvatar'][2])
        elif player == 1:
            if animator < 30:
                screen.blit(pygame.transform.flip(spriteSheetAvatar[int(instruction[18])], -1, 0), jogoDic['posAvatar'][0])
                screen.blit(pygame.transform.flip(spriteSheetAvatar[int(instruction[19])], -1, 0), jogoDic['posAvatar'][1])
                screen.blit(spriteSheetAvatar[int(instruction[17])], jogoDic['posAvatar'][2])
            else:
                screen.blit(pygame.transform.flip(spriteSheetAvatar[int(instruction[18]) + 1], -1, 0),
                            jogoDic['posAvatar'][0])
                screen.blit(pygame.transform.flip(spriteSheetAvatar[int(instruction[19]) + 1], -1, 0),
                            jogoDic['posAvatar'][1])
                screen.blit(spriteSheetAvatar[int(instruction[17]) + 1], jogoDic['posAvatar'][2])

            screen.blit(font.render(instruction[21], 1, resources.BRANCO), jogoDic['posPontoJogador1'])
            screen.blit(font.render(instruction[22], 1, resources.BRANCO), jogoDic['posPontoJogador2'])
            screen.blit(font.render(instruction[20], 1, resources.BRANCO), jogoDic['posPontoJogador3'])

            screen.blit(font2.render(instruction[15], 1, resources.BRANCO), jogoDic['posTextoNomeJogador'][0])
            screen.blit(font2.render(instruction[16], 1, resources.BRANCO), jogoDic['posTextoNomeJogador'][1])
            screen.blit(font2.render(instruction[14], 1, resources.BRANCO), jogoDic['posTextoNomeJogador'][2])

            if int(instruction[0]) == 0:
                screen.blit(turnoImg, jogoDic['posAvatar'][2])
            elif int(instruction[0]) == 1:
                screen.blit(turnoImg, jogoDic['posAvatar'][0])
            else:
                screen.blit(turnoImg, jogoDic['posAvatar'][1])
        elif player == 2:
            if animator < 30:
                screen.blit(pygame.transform.flip(spriteSheetAvatar[int(instruction[19])], -1, 0), jogoDic['posAvatar'][0])
                screen.blit(pygame.transform.flip(spriteSheetAvatar[int(instruction[17])], -1, 0), jogoDic['posAvatar'][1])
                screen.blit(spriteSheetAvatar[int(instruction[18])], jogoDic['posAvatar'][2])
            else:
                screen.blit(pygame.transform.flip(spriteSheetAvatar[int(instruction[19]) + 1], -1, 0),
                            jogoDic['posAvatar'][0])
                screen.blit(pygame.transform.flip(spriteSheetAvatar[int(instruction[17]) + 1], -1, 0),
                            jogoDic['posAvatar'][1])
                screen.blit(spriteSheetAvatar[int(instruction[18]) + 1], jogoDic['posAvatar'][2])

            screen.blit(font.render(instruction[22], 1, resources.BRANCO), jogoDic['posPontoJogador1'])
            screen.blit(font.render(instruction[20], 1, resources.BRANCO), jogoDic['posPontoJogador2'])
            screen.blit(font.render(instruction[21], 1, resources.BRANCO), jogoDic['posPontoJogador3'])

            screen.blit(font2.render(instruction[16], 1, resources.BRANCO), jogoDic['posTextoNomeJogador'][0])
            screen.blit(font2.render(instruction[14], 1, resources.BRANCO), jogoDic['posTextoNomeJogador'][1])
            screen.blit(font2.render(instruction[15], 1, resources.BRANCO), jogoDic['posTextoNomeJogador'][2])

            if int(instruction[0]) == 0:
                screen.blit(turnoImg, jogoDic['posAvatar'][1])
            elif int(instruction[0]) == 1:
                screen.blit(turnoImg, jogoDic['posAvatar'][2])
            else:
                screen.blit(turnoImg, jogoDic['posAvatar'][0])

        screen.blit(font.render(idioma['rodada'] + ' ' + instruction[23], 1, resources.BRANCO), jogoDic['posTextoRodada'])

    screen.blit(baralhoImg, jogoDic['posBralho'])

    if int(instruction[24]) == -1:
        spritesBaralho.clear()
        spritesBaralho = resources.spritesBaralho()
        distribuir_cartas = True
        animacaoCarta[1] = 0

    if int(instruction[24]) == -10 and estadoJogo != 'sair':
        estadoJogo = -10

    if instruction[35] == instruction[14] or instruction[35] == instruction[15] or instruction[35] == instruction[16]:
        cronometro2 += 1
        instruction[37] = cronometro2
        screen.blit(vencedorBg, (0, 0))
        screen.blit(font2.render(idioma['vencedor'], 1, resources.BRANCO), jogoDic['posTextoVencedor'])
        screen.blit(font2.render(instruction[35], 1, resources.BRANCO), jogoDic['posNomeVencedor'])
        if animation < 30:
            screen.blit(pygame.transform.scale2x(spriteSheetAvatar[int(instruction[36])]), jogoDic['posAvatarVencedor'])
        else:
            screen.blit(pygame.transform.scale2x(spriteSheetAvatar[int(instruction[36])] + 1), jogoDic['posAvatarVencedor'])

        if instruction[35] == instruction[14]:
            screen.blit(pygame.transform.rotate(spriteSheetAvatar[int(int(instruction[18]) / 2 + 10)], 90), jogoDic['posPerdedores'][0])
            screen.blit(pygame.transform.rotate(spriteSheetAvatar[int(int(instruction[19]) / 2 + 10)], 90), jogoDic['posPerdedores'][1])

            screen.blit(font3.render(instruction[15], 1, resources.BRANCO), jogoDic['posTxtPerdedor'][0])
            screen.blit(font3.render(instruction[16], 1, resources.BRANCO), jogoDic['posTxtPerdedor'][1])

        elif instruction[35] == instruction[15]:
            screen.blit(pygame.transform.rotate(spriteSheetAvatar[int(int(instruction[17]) / 2 + 10)], 90), jogoDic['posPerdedores'][0])
            screen.blit(pygame.transform.rotate(spriteSheetAvatar[int(int(instruction[19]) / 2 + 10)], 90), jogoDic['posPerdedores'][1])
            screen.blit(font3.render(instruction[14], 1, resources.BRANCO), jogoDic['posTxtPerdedor'][0])
            screen.blit(font3.render(instruction[16], 1, resources.BRANCO), jogoDic['posTxtPerdedor'][1])
        else:
            screen.blit(pygame.transform.rotate(spriteSheetAvatar[int(int(instruction[17]) / 2 + 10)], 90), jogoDic['posPerdedores'][0])
            screen.blit(pygame.transform.rotate(spriteSheetAvatar[int(int(instruction[18]) / 2 + 10)], 90), jogoDic['posPerdedores'][1])
            screen.blit(font3.render(instruction[14], 1, resources.BRANCO), jogoDic['posTxtPerdedor'][0])
            screen.blit(font3.render(instruction[15], 1, resources.BRANCO), jogoDic['posTxtPerdedor'][1])
    else:
        cronometro2 = 0

    if int(instruction[13]) != -1:
        cronometro1 += 1
        instruction[25] = cronometro1
    else:
        cronometro1 = 0

    try:
        instruction = ','.join(str(e) for e in instruction)
        if estadoJogo != -10:
            s.send((instruction.encode('utf-8')))
        else:
            main()
    except socket.error:
        main()

    if estadoJogo == 'sair':
        pygame.quit()

    if estadoJogo == -10:
        conectionC = False
        estadoJogo = 0
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        baralho, distribuir_cartas, animacaoCarta, spritesBaralho, rodada = resetar(baralho, distribuir_cartas, animacaoCarta, spritesBaralho, rodada)
        return 'menu', baralho, turno, rodada, pontosJogador, cartasComJogador, cartasJogadas, cartaVirada, animacaoCarta, distribuir_cartas, spritesBaralho, avatarJogador, conectionC

    return 'jogandoMult', baralho, turno, rodada, pontosJogador, cartasComJogador, cartasJogadas, cartaVirada, animacaoCarta, distribuir_cartas, spritesBaralho, avatarJogador, conectionC

def jogarSingle(idioma, nome, baralho, turno, rodada, pontosJogador, cartasComJogador, cartasJogadas, cartaVirada, distribuir_cartas, animacaoCarta, spritesBaralho, avatarJogador, tempoExibicaoRodada):
    global estadoJogo, cronometro2, animator

    if pygame.mixer.music.get_busy():
        pass
    else:
        pygame.mixer.music.play()

    font = pygame.font.Font('font/Pixellari.ttf', 45)
    font2 = pygame.font.Font('font/Pixellari.ttf', 35)
    font3 = pygame.font.Font('font/Pixellari.ttf', 25)
    mouse = pygame.mouse.get_pos()
    screen.blit(backgroundJogo, (0, 0))

    if distribuir_cartas:

        for i in range(3):
            screen.blit(fundoAvatarBg, jogoDic['posBgFundoAvatar'][i])

        if animator < 30:
            screen.blit(pygame.transform.flip(spriteSheetAvatar[avatarJogador], -1, 0), jogoDic['posAvatar'][0])
            screen.blit(pygame.transform.flip(spriteSheetAvatar[0], -1, 0), jogoDic['posAvatar'][1])
            screen.blit(spriteSheetAvatar[2], jogoDic['posAvatar'][2])
        else:
            screen.blit(pygame.transform.flip(spriteSheetAvatar[avatarJogador + 1], -1, 0),
                        jogoDic['posAvatar'][0])
            screen.blit(pygame.transform.flip(spriteSheetAvatar[1], -1, 0),
                        jogoDic['posAvatar'][1])
            screen.blit(spriteSheetAvatar[3], jogoDic['posAvatar'][2])


        screen.blit(font.render(str(pontosJogador[0]), 1, resources.BRANCO), jogoDic['posPontoJogador1'])
        screen.blit(font.render(str(pontosJogador[1]), 1, resources.BRANCO), jogoDic['posPontoJogador2'])
        screen.blit(font.render(str(pontosJogador[2]), 1, resources.BRANCO), jogoDic['posPontoJogador3'])

        screen.blit(font2.render(str(nome), 1, resources.BRANCO), jogoDic['posTextoNomeJogador'][0])
        screen.blit(font2.render('Morte', 1, resources.BRANCO), jogoDic['posTextoNomeJogador'][1])
        screen.blit(font2.render('Burocrata', 1, resources.BRANCO), jogoDic['posTextoNomeJogador'][2])

        screen.blit(font.render(idioma['embaralhar'], 1, resources.BRANCO), (jogoDic['posTextoRodada'][0] - 40, jogoDic['posTextoRodada'][1]))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
        distribuir_cartas, animacaoCarta, cartaVirada, baralho, cartasComJogador, spritesBaralho = distribuirCartas(distribuir_cartas, animacaoCarta, cartaVirada, baralho, cartasComJogador, spritesBaralho)


    else:
        retCartas = [None] * 3
        for i in range(3):
            retCartas[i] = pygame.Rect(jogoDic['posCartaPlayer1'][i][0], jogoDic['posCartaPlayer1'][i][1],
                                       spritesBaralho[0].get_width(), spritesBaralho[0].get_height())
        for i in range(3):
            if cartasComJogador[0][i] != None:
                if retCartas[i].collidepoint(mouse[0], mouse[1]):
                    screen.blit(spritesBaralho[cartasComJogador[0][i]], (jogoDic['posCartaPlayer1'][i][0], jogoDic['posCartaPlayer1'][i][1] - 15))
                else:
                    screen.blit(spritesBaralho[cartasComJogador[0][i]], jogoDic['posCartaPlayer1'][i])

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if turno == 0:
                    if retCartas[0].collidepoint(mouse[0], mouse[1]) and cartasComJogador[0][0] != None:
                        cartasJogadas.append(cartasComJogador[0][0])
                        cartasComJogador[0][0] = None
                        turno += 1
                        fxCardAnim.play()
                    elif retCartas[1].collidepoint(mouse[0], mouse[1]) and cartasComJogador[0][1] != None:
                        cartasJogadas.append(cartasComJogador[0][1])
                        cartasComJogador[0][1] = None
                        turno += 1
                        fxCardAnim.play()
                    elif retCartas[2].collidepoint(mouse[0], mouse[1]) and cartasComJogador[0][2] != None:
                        cartasJogadas.append(cartasComJogador[0][2])
                        cartasComJogador[0][2] = None
                        turno += 1
                        fxCardAnim.play()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.mixer.music.load(resources.MENU_MUSIC)
                    estadoJogo = 0
                    pontosJogador[0], pontosJogador[1], pontosJogador[2] = 0, 0, 0
                    baralho, distribuir_cartas, animacaoCarta, spritesBaralho, rodada = resetar(baralho, distribuir_cartas, animacaoCarta, spritesBaralho, rodada)
                    return 'menu', baralho, turno, rodada, pontosJogador, cartasComJogador, cartasJogadas, cartaVirada, animacaoCarta, distribuir_cartas, spritesBaralho, avatarJogador

        screen.blit(spritesBaralho[cartaVirada], jogoDic['posCartaVirada'])

        for i in range(3):
            if cartasComJogador[1][i] != None:
                screen.blit(pygame.transform.rotate(fundoCarta, 90), jogoDic['posCartaPlayer2'][i])

        for i in range(3):
            if cartasComJogador[2][i] != None:
                screen.blit(pygame.transform.rotate(fundoCarta, -90), jogoDic['posCartaPlayer3'][i])

        for i in range(len(cartasJogadas)):
            screen.blit(spritesBaralho[cartasJogadas[i]], jogoDic['posJogada'][i])

        for i in range(3):
            screen.blit(fundoAvatarBg, jogoDic['posBgFundoAvatar'][i])

        if animator < 30:
            screen.blit(pygame.transform.flip(spriteSheetAvatar[avatarJogador], -1, 0), jogoDic['posAvatar'][0])
            screen.blit(pygame.transform.flip(spriteSheetAvatar[0], -1, 0), jogoDic['posAvatar'][1])
            screen.blit(spriteSheetAvatar[2], jogoDic['posAvatar'][2])
        else:
            screen.blit(pygame.transform.flip(spriteSheetAvatar[avatarJogador + 1], -1, 0),
                        jogoDic['posAvatar'][0])
            screen.blit(pygame.transform.flip(spriteSheetAvatar[1], -1, 0),
                        jogoDic['posAvatar'][1])
            screen.blit(spriteSheetAvatar[3], jogoDic['posAvatar'][2])

        screen.blit(font.render(str(pontosJogador[0]), 1, resources.BRANCO), jogoDic['posPontoJogador1'])
        screen.blit(font.render(str(pontosJogador[1]), 1, resources.BRANCO), jogoDic['posPontoJogador2'])
        screen.blit(font.render(str(pontosJogador[2]), 1, resources.BRANCO), jogoDic['posPontoJogador3'])
        screen.blit(font2.render(str(nome), 1, resources.BRANCO), jogoDic['posTextoNomeJogador'][0])
        screen.blit(font2.render('Morte', 1, resources.BRANCO), jogoDic['posTextoNomeJogador'][1])
        screen.blit(font2.render('Burocrata', 1, resources.BRANCO), jogoDic['posTextoNomeJogador'][2])
        screen.blit(font.render(idioma['rodada'] + ' ' + str(rodada), 1, resources.BRANCO), jogoDic['posTextoRodada'])

    screen.blit(baralhoImg, jogoDic['posBralho'])

    if turno == 1:
        while True:
            aleatorio = random.randint(0, 2)
            if cartasComJogador[1][aleatorio] != None:
                break
        cartasJogadas.append(cartasComJogador[1][aleatorio])
        cartasComJogador[1][aleatorio] = None
        turno += 1

    if turno == 2:
        while True:
            aleatorio = random.randint(0, 2)
            if cartasComJogador[2][aleatorio] != None:
                break
        cartasJogadas.append(cartasComJogador[2][aleatorio])
        cartasComJogador[2][aleatorio] = None
        turno = -1

    if estadoJogo == 'vencedor':
        screen.blit(vencedorBg, (0, 0))
        if pontosJogador[0] == 12:
            screen.blit(font2.render(nome, 1, resources.BRANCO), jogoDic['posNomeVencedor'])
            if animation < 30:
                screen.blit(pygame.transform.scale2x(spriteSheetAvatar[avatarJogador]), jogoDic['posAvatarVencedor'])
            else:
                screen.blit(pygame.transform.scale2x(spriteSheetAvatar[avatarJogador] + 1), jogoDic['posAvatarVencedor'])
            screen.blit(font2.render(idioma['vencedor'], 1, resources.BRANCO), jogoDic['posTextoVencedor'])
            screen.blit(pygame.transform.rotate(spriteSheetAvatar[10], 90), jogoDic['posPerdedores'][0])
            screen.blit(pygame.transform.rotate(spriteSheetAvatar[11], 90), jogoDic['posPerdedores'][1])
            screen.blit(font3.render('Morte', 1, resources.BRANCO), jogoDic['posTxtPerdedor'][0])
            screen.blit(font3.render('Burocrata', 1, resources.BRANCO), jogoDic['posTxtPerdedor'][1])

        elif pontosJogador[1] == 12:
            if animation < 30:
                screen.blit(pygame.transform.scale2x(spriteSheetAvatar[0]), jogoDic['posAvatarVencedor'])
            else:
                screen.blit(pygame.transform.scale2x(spriteSheetAvatar[0] + 1), jogoDic['posAvatarVencedor'])

            screen.blit(font2.render('Morte', 1, resources.BRANCO), jogoDic['posNomeVencedor'])
            screen.blit(pygame.transform.rotate(spriteSheetAvatar[int(avatarJogador / 2 + 10)], 90), jogoDic['posPerdedores'][0])
            screen.blit(pygame.transform.rotate(spriteSheetAvatar[11], 90), jogoDic['posPerdedores'][1])
            screen.blit(font3.render(str(nome), 1, resources.BRANCO), jogoDic['posTxtPerdedor'][0])
            screen.blit(font3.render('Burocrata', 1, resources.BRANCO), jogoDic['posTxtPerdedor'][1])
        else:
            if animation < 30:
                screen.blit(pygame.transform.scale2x(spriteSheetAvatar[2]), jogoDic['posAvatarVencedor'])
            else:
                screen.blit(pygame.transform.scale2x(spriteSheetAvatar[2] + 1), jogoDic['posAvatarVencedor'])
            screen.blit(font2.render('Burocrata', 1, resources.BRANCO), jogoDic['posNomeVencedor'])
            screen.blit(pygame.transform.rotate(spriteSheetAvatar[int(avatarJogador / 2 + 10)], 90), jogoDic['posPerdedores'][0])
            screen.blit(pygame.transform.rotate(spriteSheetAvatar[10], 90), jogoDic['posPerdedores'][1])
            screen.blit(font3.render(str(nome), 1, resources.BRANCO), jogoDic['posTxtPerdedor'][0])
            screen.blit(font3.render('Morte', 1, resources.BRANCO), jogoDic['posTxtPerdedor'][1])
        cronometro2 += 1
        if cronometro2 >= 120:
            pontosJogador[0], pontosJogador[1], pontosJogador[2] = 0, 0, 0
            baralho, distribuir_cartas, animacaoCarta, spritesBaralho, rodada = resetar(baralho, distribuir_cartas, animacaoCarta, spritesBaralho, rodada)
            estadoJogo = 0
    else:
        cronometro2 = 0

    if turno == -1:
        global cronometro1
        cronometro1 += 1
        if cronometro1 == tempoExibicaoRodada:
            pontosJogador = verificarVencedorRodada(cartasJogadas, rodada, pontosJogador)
            cartasJogadas.clear()
            turno = 0
            rodada += 1
            cronometro1 = 0
        if rodada > 3 and estadoJogo != 'vencedor':
            baralho, distribuir_cartas, animacaoCarta, spritesBaralho, rodada = resetar(baralho, distribuir_cartas, animacaoCarta, spritesBaralho, rodada)

    return 'jogandoSingle', baralho, turno, rodada, pontosJogador, cartasComJogador, cartasJogadas, cartaVirada, animacaoCarta, distribuir_cartas, spritesBaralho, avatarJogador


def resetar(baralho, distribuir_cartas, animacaoCarta, spritesBaralho, rodada):
    baralho = [0, 1, 2, 3,
               4, 5, 6, 7,
               8, 9, 10, 11,
               12, 13, 14, 15,
               16, 17, 18, 19,
               20, 21, 22, 23]
    distribuir_cartas = True
    animacaoCarta[1] = 0
    spritesBaralho.clear()
    spritesBaralho = resources.spritesBaralho()
    rodada = 1
    return baralho, distribuir_cartas, animacaoCarta, spritesBaralho, rodada

def abertura(apresentacao):
    if pygame.mixer.music.get_busy():
        pass
    else:
        pygame.mixer.music.play()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
    global cronometro1, contadorG

    screen.fill(resources.BRANCO)

    font = pygame.font.Font('font/Pixellari.ttf', 45)

    if apresentacao == 1:
        cronometro1 += 1
        if cronometro1 <= 10:
            screen.blit(logo[0], (160, 190))
        elif 5 < cronometro1 <= 10:
            screen.blit(logo[1], (160, 190))
        elif 10 < cronometro1 <= 15:
            screen.blit(logo[2], (160, 190))
        elif 15 < cronometro1 <= 20:
            screen.blit(logo[3], (160, 190))
        elif 20 < cronometro1 <= 25:
            screen.blit(logo[4], (160, 190))
        elif 25 < cronometro1 <= 30:
            screen.blit(logo[5], (160, 190))
        elif 30 < cronometro1 <= 35:
            screen.blit(logo[6], (160, 190))
        elif 35 < cronometro1 <= 40:
            screen.blit(logo[7], (160, 190))
        elif 40 < cronometro1 <= 45:
            screen.blit(logo[8], (160, 190))
        elif 45 < cronometro1 <= 50:
            screen.blit(logo[9], (160, 190))
        elif 50 < cronometro1 <= 55:
            screen.blit(logo[10], (160, 190))
        elif 55 < cronometro1 <= 60:
            screen.blit(logo[11], (160, 190))
        elif 60 < cronometro1 <= 65:
            screen.blit(logo[12], (160, 190))
        elif 65 < cronometro1 <= 70:
            screen.blit(logo[13], (160, 190))
        elif 70 < cronometro1 <= 75:
            screen.blit(logo[14], (160, 190))
        elif 75 < cronometro1 <= 80:
            screen.blit(logo[15], (160, 190))
        elif 80 < cronometro1 <= 85:
            screen.blit(logo[16], (160, 190))
        elif 85 < cronometro1 <= 90:
            screen.blit(logo[17], (160, 190))
        elif 90 < cronometro1 <= 95:
            screen.blit(logo[18], (160, 190))
        elif 95 < cronometro1 <= 100:
            screen.blit(logo[19], (160, 190))
        elif 100 < cronometro1 <= 105:
            screen.blit(logo[20], (160, 190))
        elif 105 < cronometro1 <= 110:
            screen.blit(logo[21], (160, 190))
        elif 110 < cronometro1 <= 115:
            screen.blit(logo[22], (160, 190))
        elif 115 < cronometro1 <= 120:
            screen.blit(logo[22], (160, 190))
        else:
            screen.blit(logo[21], (160, 190))
            cronometro1 = 0
            contadorG = -100
            apresentacao += 1
    elif apresentacao == 2:
        cronometro1 += 1
        screen.blit(logo[10], (160, 190))
        if contadorG < 270:
            screen.blit(font.render('Apresenta', 1, resources.PRETO), (contadorG, 439))
            contadorG += 20
        else:
            screen.blit(font.render('Apresenta', 1, resources.PRETO), (270, 439))
            if cronometro1 > 50:
                apresentacao += 1
                cronometro1 = 0
                contadorG = 0
    elif apresentacao == 3:
        screen.blit(imgProjetoK, (0, 0))
        cronometro1 += 1
        if cronometro1 > 60:
            screen.blit(imgPKFatec, (0, 0))
            if cronometro1 > 120:
                apresentacao += 1
                cronometro1 = 0
    elif apresentacao == 4:
        cronometro1 += 1
        if cronometro1 <= 10:
            screen.blit(cgInicial[0], (0, 0))
        elif 5 < cronometro1 <= 10:
            screen.blit(cgInicial[1], (0, 0))
        elif 10 < cronometro1 <= 15:
            screen.blit(cgInicial[2], (0, 0))
        elif 15 < cronometro1 <= 20:
            screen.blit(cgInicial[3], (0, 0))
        elif 20 < cronometro1 <= 25:
            screen.blit(cgInicial[4], (0, 0))
        elif 25 < cronometro1 <= 30:
            screen.blit(cgInicial[5], (0, 0))
        elif 30 < cronometro1 <= 35:
            screen.blit(cgInicial[6], (0, 0))
        elif 35 < cronometro1 <= 40:
            screen.blit(cgInicial[7], (0, 0))
        elif 40 < cronometro1 <= 45:
            screen.blit(cgInicial[8], (0, 0))
        elif 45 < cronometro1 <= 50:
            screen.blit(cgInicial[9], (0, 0))
        elif 45 < cronometro1 <= 55:
            screen.blit(cgInicial[10], (0, 0))
        elif 50 < cronometro1 <= 60:
            screen.blit(cgInicial[11], (0, 0))
        elif 55 < cronometro1 <= 65:
            screen.blit(cgInicial[12], (0, 0))
        elif 60 < cronometro1 <= 70:
            screen.blit(cgInicial[13], (0, 0))
        elif 65 < cronometro1 <= 75:
            screen.blit(cgInicial[14], (0, 0))
        elif 70 < cronometro1 <= 80:
            screen.blit(cgInicial[15], (0, 0))
        elif 75 < cronometro1 <= 85:
            screen.blit(cgInicial[16], (0, 0))
        elif 80 < cronometro1 <= 90:
            screen.blit(cgInicial[17], (0, 0))
        elif 85 < cronometro1 <= 95:
            screen.blit(cgInicial[18], (0, 0))
        elif 90 < cronometro1 <= 100:
            screen.blit(cgInicial[19], (0, 0))
        elif 95 < cronometro1 <= 105:
            screen.blit(cgInicial[20], (0, 0))
        elif 100 < cronometro1 <= 110:
            screen.blit(cgInicial[21], (0, 0))
        elif cronometro1 > 110:
            screen.blit(cgInicial[22], (0, 0))
        if cronometro1 > 120:
            apresentacao += 1
            cronometro1 = 0
            cgInicial.clear()
            return 'escreverNome', 0
    return 'abertura', apresentacao

def aguardarJogadores(idioma, conectionC, serverIp, nome, avatarJogador):
    global s, host, porta, instruction, player

    mouse = pygame.mouse.get_pos()
    font = pygame.font.Font('font/Pixellari.ttf', 45)
    font2 = pygame.font.Font('font/Pixellari.ttf', 25)
    font3 = pygame.font.Font('font/Pixellari.ttf', 35)
    screen.blit(lobbyBg, (0, 0))

    screen.blit(spriteSheetAvatar[avatarJogador], menuDic['posAvatarSalaEspera'])
    screen.blit(font2.render(nome, 1, resources.BRANCO), menuDic['nomeSalaEspera'])

    botaoRetConfirm = pygame.Rect(menuDic['btnConfirmServer'][0], menuDic['btnConfirmServer'][1], botao.get_width(), botao.get_height())

    if botaoRetConfirm.collidepoint(mouse):
        screen.blit(botao2, menuDic['btnConfirmServer'])
    else:
        screen.blit(botao, menuDic['btnConfirmServer'])
    screen.blit(font3.render(idioma['confirmar'], 1, resources.BRANCO),(menuDic['btnConfirmServer'][0] + 10, menuDic['btnConfirmServer'][1] + 10))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if botaoRetConfirm.collidepoint(mouse):
                fxBtn.play()
                if not conectionC:
                    try:
                        s.connect((serverIp, porta))
                        msgFromServer = s.recv(1024)
                        screen.blit(font2.render(idioma['aguardandoJogadores'], 1, resources.BRANCO), menuDic['txtAguardando'])
                        player = int(msgFromServer.decode('utf-8'))
                        conectionC = True

                        instruction = s.recv(1024)
                        instruction = instruction.decode('utf-8')
                        instruction = instruction.split(',')

                        if player == 0:
                            instruction[14] = nome
                            instruction[17] = avatarJogador
                        elif player == 1:
                            instruction[15] = nome
                            instruction[18] = avatarJogador
                        else:
                            instruction[16] = nome
                            instruction[19] = avatarJogador

                        instruction = ','.join(str(e) for e in instruction)
                        s.send((instruction.encode('utf-8')))
                        pygame.mixer.music.load(resources.GAMEPLAY_MUSIC)
                        return 'jogandoMult', conectionC, serverIp, nome, avatarJogador
                    except socket.error:
                        screen.blit(font2.render('Erro', 1, resources.BRANCO), menuDic['txtErrorLobby'])
                    finally:
                        pass

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE:
                try:
                    serverIp = serverIp.split()
                    serverIp.pop(len(serverIp) - 1)
                    serverIp = ''.join(serverIp)
                except IndexError:
                    serverIp = ''.join(serverIp)
            elif event.key == pygame.K_ESCAPE:
                return 'menu', conectionC, serverIp, nome, avatarJogador
            elif event.unicode:
                serverIp += str(event.unicode)

    screen.blit(font.render(idioma['digiteServidor'], 1, resources.BRANCO), menuDic['txtLobby'])
    screen.blit(font.render(str(serverIp), 1, resources.BRANCO), menuDic['ipTxt'])

    return 'aguardandoJogadores', conectionC, serverIp, nome, avatarJogador


def main():
    global s, host, porta, instruction, player, animator
    pygame.mixer.music.load(resources.MENU_MUSIC)
    baralho = [0, 1, 2, 3,
               4, 5, 6, 7,
               8, 9, 10, 11,
               12, 13, 14, 15,
               16, 17, 18, 19,
               20, 21, 22, 23]
    conectionC = False
    serverIp = 'localhost'
    pontosJogador = [0] * 3
    cartasComJogador = [None, None, None]
    cartasComJogadorSingle = [[None, None, None], [None, None, None], [None, None, None]]
    cartasJogadas = []
    distribuir_cartas = True
    turno = 0
    rodada = 1
    tempoExibicaoRodada = 85
    cartaVirada = None
    animacaoCarta = [192, 0]
    spritesBaralho = resources.spritesBaralho()
    apresentacao = 1
    avatarJogador = 6
    estadoMenu = ''

    pygame.init()
    pygame.font.init()

    estado = 'abertura'
    nome = '_ _ _ _ _ _'
    idioma = textos.dicPortugues
    idiomaTexto = 'Português'



    while True:
        if estado == 'abertura':
            estado, apresentacao = abertura(apresentacao)

        elif estado == 'escreverNome':
            estado, nome, idioma, idiomaTexto = enterNomePlayer(idioma, nome, idiomaTexto)

        elif estado == 'menu':
            estado, avatarJogador, estadoMenu = menu(idioma, nome, avatarJogador, estadoMenu)

        elif estado == 'configuracao':
            estado, idiomaTexto, idioma, nome = configuracao(idioma, idiomaTexto, nome)

        elif estado == 'avatar':
            estado, avatarJogador = avatar(idioma, avatarJogador)

        elif estado == 'aguardandoJogadores':
            estado, conectionC, serverIp, nome, avatarJogador = aguardarJogadores(idioma, conectionC, serverIp, nome, avatarJogador)

        elif estado == 'jogandoMult':
            estado, baralho, turno, rodada, pontosJogador, cartasComJogador, cartasJogadas, cartaVirada, animacaoCarta, distribuir_cartas, spritesBaralho, avatarJogador, conectionC = \
                jogarMult(idioma, nome, baralho, turno, rodada,  pontosJogador, cartasComJogador, cartasJogadas, cartaVirada, distribuir_cartas, animacaoCarta, spritesBaralho, avatarJogador, tempoExibicaoRodada, conectionC)

        elif estado == 'jogandoSingle':
            estado, baralho, turno, rodada, pontosJogador, cartasComJogadorSingle, cartasJogadas, cartaVirada, animacaoCarta, distribuir_cartas, spritesBaralho, avatarJogador = \
                jogarSingle(idioma, nome, baralho, turno, rodada, pontosJogador, cartasComJogadorSingle, cartasJogadas, cartaVirada, distribuir_cartas, animacaoCarta, spritesBaralho, avatarJogador, tempoExibicaoRodada)

        animator += 1
        if animator == 60:
            animator = 0

        clock.tick(config.FPS)
        pygame.display.update()

main()