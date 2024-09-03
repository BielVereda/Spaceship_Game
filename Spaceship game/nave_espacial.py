import pygame
import sys
import random
import os

# Inicialize o Pygame
pygame.init()

# Configurações da tela
largura_tela = 800
altura_tela = 600
tela = pygame.display.set_mode((largura_tela, altura_tela))
pygame.display.set_caption("Jogo de Nave Espacial")

# Cores
PRETO = (0, 0, 0)
BRANCO = (255, 255, 255)

# Função para carregar uma imagem e verificar se foi carregada corretamente
def carregar_imagem(caminho):
    if os.path.isfile(caminho):
        return pygame.image.load(caminho)
    else:
        print(f"Erro: Arquivo não encontrado: {caminho}")
        pygame.quit()
        sys.exit()

# Função para carregar um som e verificar se foi carregado corretamente
def carregar_som(caminho):
    if os.path.isfile(caminho):
        return pygame.mixer.Sound(caminho)
    else:
        print(f"Erro: Arquivo de som não encontrado: {caminho}")
        pygame.quit()
        sys.exit()

# Carregue as imagens
fundo_img = carregar_imagem('C:/Users/gabri/Downloads/VS Code/Spaceship game/fundo.jpg')
nave_img = carregar_imagem('C:/Users/gabri/Downloads/VS Code/Spaceship game/nave.png')
tiro_img = carregar_imagem('C:/Users/gabri/Downloads/VS Code/Spaceship game/tiro.png')
inimigo_img = carregar_imagem('C:/Users/gabri/Downloads/VS Code/Spaceship game/inimigo.png')
meteoro_img = carregar_imagem('C:/Users/gabri/Downloads/VS Code/Spaceship game/meteoro.png')
explosao_img = carregar_imagem('C:/Users/gabri/Downloads/VS Code/Spaceship game/explosao.png')
coracao_img = carregar_imagem('C:/Users/gabri/Downloads/VS Code/Spaceship game/coracao.png')

# Redimensione as imagens
novo_tamanho_inimigo = (50, 50)
inimigo_img = pygame.transform.scale(inimigo_img, novo_tamanho_inimigo)

novo_tamanho_meteoro = (40, 40)
meteoro_img = pygame.transform.scale(meteoro_img, novo_tamanho_meteoro)

novo_tamanho_explosao = (50, 50)
explosao_img = pygame.transform.scale(explosao_img, novo_tamanho_explosao)

novo_tamanho_coracao = (30, 30)
coracao_img = pygame.transform.scale(coracao_img, novo_tamanho_coracao)

# Carregar sons
som_tiro = carregar_som('C:/Users/gabri/Downloads/VS Code/Spaceship game/tiro_som.wav')
som_explosao = carregar_som('C:/Users/gabri/Downloads/VS Code/Spaceship game/explosao_som.wav')
pygame.mixer.music.load('C:/Users/gabri/Downloads/VS Code/Spaceship game/musica_fundo.mp3')
pygame.mixer.music.play(-1)  # Reproduzir música em loop

# Configurações da nave
class Nave(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = nave_img
        self.rect = self.image.get_rect()
        self.rect.center = (largura_tela // 2, altura_tela - 50)
        self.vidas = 3

# Configurações do tiro
class Tiro(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = tiro_img
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.velocidade = -10

    def update(self):
        self.rect.y += self.velocidade
        if self.rect.bottom < 0:
            self.kill()

# Configurações dos inimigos
class Inimigo(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = inimigo_img
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, largura_tela - self.rect.width)
        self.rect.y = random.randint(-150, -self.rect.height)
        self.velocidade = velocidade_inimigos  # Use the velocidade_inimigos variable

    def update(self):
        self.rect.y += self.velocidade
        if self.rect.top > altura:
            self.rect.x = random.randint(0, largura_tela - self.rect.width)
            self.rect.y = random.randint(-150, -self.rect.height)

# Configurações dos meteoros
class Meteoro(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = meteoro_img
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, largura_tela - self.rect.width)
        self.rect.y = random.randint(-150, -self.rect.height)
        self.velocidade = velocidade_meteoros  # Use the velocidade_meteoros variable

    def update(self):
        self.rect.y += self.velocidade
        if self.rect.top > altura_tela:
            self.rect.x = random.randint(0, largura_tela - self.rect.width)
            self.rect.y = random.randint(-150, -self.rect.height)

# Configurações da explosão
class Explosao(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = explosao_img
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.frame = 0
        self.velocidade_frame = 1

    def update(self):
        self.frame += self.velocidade_frame
        if self.frame > 5:
            self.kill()

# Inicialize as variáveis
velocidade_inimigos = 1  # Velocidade inicial dos inimigos
velocidade_meteoros = 1  # Velocidade inicial dos meteoros
pontos = 0
fonte_pontos = pygame.font.Font(None, 36)

# Crie os grupos de sprites
todos_sprites = pygame.sprite.Group()
inimigos_sprites = pygame.sprite.Group()
meteoros_sprites = pygame.sprite.Group()
tiros_sprites = pygame.sprite.Group()
explosao_sprites = pygame.sprite.Group()

# Crie a nave
nave = Nave()
todos_sprites.add(nave)

# Game loop
while True:
    # Eventos
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                tiro = Tiro(nave.rect.centerx, nave.rect.top)
                todos_sprites.add(tiro)
                tiros_sprites.add(tiro)
                som_tiro.play()

    # Atualize a nave
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        nave.rect.x -= 5
    if keys[pygame.K_RIGHT]:
        nave.rect.x += 5

    # Atualize os inimigos
    for inimigo in inimigos_sprites:
        inimigo.update()
        if inimigo.rect.top > altura_tela:
            inimigos_sprites.remove(inimigo)
            todos_sprites.remove(inimigo)

    # Atualize os meteoros
    for meteoro in meteoros_sprites:
        meteoro.update()
        if meteoro.rect.top > altura_tela:
            meteoros_sprites.remove(meteoro)
            todos_sprites.remove(meteoro)

    # Atualize os tiros
    for tiro in tiros_sprites:
        tiro.update()
        if tiro.rect.bottom < 0:
            tiros_sprites.remove(tiro)
            todos_sprites.remove(tiro)

    # Verifique colisões
    for tiro in tiros_sprites:
        for inimigo in inimigos_sprites:
            if tiro.rect.colliderect(inimigo.rect):
                explosao = Explosao(inimigo.rect.centerx, inimigo.rect.centery)
                todos_sprites.add(explosao)
                explosao_sprites.add(explosao)
                som_explosao.play()
                inimigos_sprites.remove(inimigo)
                todos_sprites.remove(inimigo)
                pontos += 1

    for tiro in tiros_sprites:
        for meteoro in meteoros_sprites:
            if tiro.rect.colliderect(meteoro.rect):
                explosao = Explosao(meteoro.rect.centerx, meteoro.rect.centery)
                todos_sprites.add(explosao)
                explosao_sprites.add(explosao)
                som_explosao.play()
                meteoros_sprites.remove(meteoro)
                todos_sprites.remove(meteoro)
                pontos += 1

    # Verifique se a nave colidiu com um inimigo ou meteoro
    for inimigo in inimigos_sprites:
        if nave.rect.colliderect(inimigo.rect):
            nave.vidas -= 1
            inimigos_sprites.remove(inimigo)
            todos_sprites.remove(inimigo)

    for meteoro in meteoros_sprites:
        if nave.rect.colliderect(meteoro.rect):
            nave.vidas -= 1
            meteoros_sprites.remove(meteoro)
            todos_sprites.remove(meteoro)

    # Desenhe tudo
    tela.fill(PRETO)
    todos_sprites.draw(tela)
    texto_pontos = fonte_pontos.render(f"Pontos: {pontos}", True, BRANCO)
    tela.blit(texto_pontos, (10, 10))
    texto_vidas = fonte_pontos.render(f"Vidas: {nave.vidas}", True, BRANCO)
    tela.blit(texto_vidas, (10, 40))

    # Atualize a tela
    pygame.display.flip()
    pygame.time.Clock().tick(60)

    # Adicione inimigos e meteoros aleatoriamente
    if random.random() < 0.1:
        inimigo = Inimigo()
        todos_sprites.add(inimigo)
        inimigos_sprites.add(inimigo)

    if random.random() < 0.05:
        meteoro = Meteoro()
        todos_sprites.add(meteoro)
        meteoros_sprites.add(meteoro)