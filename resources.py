# *********************************************************************************************
# ******   FATEC - Faculdade de Tecnologia de Carapicuiba                                ******
# ******   Funcao: responsavel por efetuar o processamento principal do jogo com todas   ******
# ******           as regras, definicoes e comportamento da aplicacao cliente            ******
# ******   Nome..: Diego Vinicius de Mello Munhoz                                        ******
# ******           Thiago Zacarias da Silva                                              ******
# ******           Victor Otavio Ponciano                                                ******
# ******   Data..: 07/07/2018                                                            ******
# *********************************************************************************************

import pygame

BRANCO = (255, 255, 255)
PRETO = (0, 0, 0)
VERMELHO = (255, 0, 0)
VERDE = (0, 255, 0)
AZUL = (0, 0, 255)

BOTAO = 'imagens/botao.png'
BOTAO2 = 'imagens/botao2.png'
BACKGROUND_JOGO = 'imagens/mesaBG.png'
BACKGROUND_MENU = 'imagens/background_menu.png'
FUNDO_CARTA = 'imagens/fundo.png'
BARALHO = 'imagens/baralho.png'
TURNO = 'imagens/turno.png'
SPRITESHEET_BARALHO = pygame.image.load('imagens/sprite_baralho.png')
SPRITESHEET_AVATAR = pygame.image.load('imagens/avatar_sprite_sheet.png')
PAGINA_PORTUGUES = pygame.image.load('imagens/pagina_pt.png')
PAGINA_INGLES = pygame.image.load('imagens/pagina_ig.png')
BANDEIRA = pygame.image.load('imagens/bandeira.png')
FUNDO_AVATAR = 'imagens/fundoAvatar.png'
PROJETOK = 'imagens/projetok.png'
PROJETOK_FATEC = 'imagens/projetok.jpg'
LEFT = 'imagens/left.png'
RIGHT = 'imagens/right.png'
SPRITESHEET_LOGO = pygame.image.load('imagens/logo_spritesheet.png')
ESPELHO = 'imagens/avatar_mirror.png'
VENCEDOR_BG = 'imagens/vencedorBg.jpg'
LOBBY_BG = 'imagens/lobbyBg.jpg'
REGRAS = pygame.image.load('imagens/regras.png')
REGRAS_INGLES = pygame.image.load('imagens/regrasIng.png')

CG_INICIAL = pygame.image.load('imagens/animInicial.png')

FX_CARD = './audio/distCarta.wav'
FX_CLICK = './audio/clicMenu.wav'
GAMEPLAY_MUSIC = './audio/gameplaySong.wav'
MENU_MUSIC = './audio/menuSong.wav'

frames = []
logo = [] 
regrasPt = []
regrasIng = []
avatar = []
cg_inicial = []
bandeira = []
pagina_pt = []
pagina_ig = []

def pagina_portugues():
    x = 0
    for i in range(5):
        pagina_pt.append(PAGINA_PORTUGUES.subsurface(pygame.Rect(x, 0, 800, 600)))
        x += 800
    return pagina_pt

def pagina_ingles():
    x = 0
    for i in range(5):
        pagina_ig.append(PAGINA_INGLES.subsurface(pygame.Rect(x, 0, 800, 600)))
        x += 800
    return pagina_ig

def bandeiraSprite():
    x = 0
    for i in range(4):
        bandeira.append(BANDEIRA.subsurface(pygame.Rect(x, 0, 84, 56)))
        x += 84
    return bandeira

def animInicial():
    y = 0
    for i in range(23):
        cg_inicial.append(CG_INICIAL.subsurface(pygame.Rect(0, y, 800, 600)))
        y += 600
    return cg_inicial

def spritesBaralho():
    x = 0
    for i in range(24):
        frames.append(SPRITESHEET_BARALHO.subsurface(pygame.Rect(x, 0, 50, 75)))
        x += 50
    return frames

def spriteLogo():
    x = 0
    for i in range(0, 23):
        logo.append(SPRITESHEET_LOGO.subsurface(pygame.Rect(x, 0, 480, 220)))
        x += 480

    return logo

def spriteRegrasPt():
    x = 0
    for i in range(4):
        regrasPt.append(REGRAS.subsurface(pygame.Rect(x, 0, 800, 424)))
        x += 800

    return regrasPt

def spriteRegrasIng():
    x = 0
    for i in range(4):
        regrasIng.append(REGRAS_INGLES.subsurface(pygame.Rect(x, 0, 800, 424)))
        x += 800

    return regrasIng

#Cria uma lista com os retângulos recortados da spritesheet avatar e suas imagens
def spriteAvatar():
    y = 0
    for i in range(15):
        avatar.append(SPRITESHEET_AVATAR.subsurface(pygame.Rect(0, y, 55, 100)))
        y += 100
    return avatar