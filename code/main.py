## CODIGO FINAL TESTES A4 FUNDO TRANSPARENTE COM 01 CROMO FALTANTE PELA MEDIA RGB COM ASSINATURA!!! ###
import os
from PIL import Image, ImageDraw, ImageFont, UnidentifiedImageError
import numpy as np

# Configurações para o tamanho A4
DPI = 300  # Resolução (300 DPI é comum para impressão)
A4_WIDTH = int(8.27 * DPI)  # 8.27 polegadas (largura A4) em pixels
A4_HEIGHT = int(11.69 * DPI)  # 11.69 polegadas (altura A4) em pixels
A4_SIZE = (A4_WIDTH, A4_HEIGHT)

# Número de colunas e linhas fixas
NUM_COLUNAS = 6
NUM_LINHAS = 6

# Caminho para a pasta contendo as imagens
caminho_pasta = "C:/Imagens/NFT"
pasta_testes = os.path.join("code", "testes")

# Criar a pasta "Testes" se não existir
if not os.path.exists(pasta_testes):
    os.makedirs(pasta_testes)

# Lista todas as imagens na pasta com extensões válidas
imagens = [os.path.join(caminho_pasta, arquivo) for arquivo in os.listdir(caminho_pasta)
           if arquivo.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp'))]

if not imagens:
    print("Nenhuma imagem encontrada na pasta especificada.")
    exit()

# Limitar para as 35 primeiras imagens, caso haja mais
imagens = imagens[:35]

# Função para calcular a cor média de uma imagem
def calcular_cor_media(imagem):
    imagem_np = np.array(imagem)
    if len(imagem_np.shape) == 3:  # Verifica se a imagem tem 3 canais (RGB)
        return tuple(imagem_np.mean(axis=(0, 1)))
    else:
        return (0, 0, 0)  # Para imagens em escala de cinza

# Abrir todas as imagens, ajustar orientação e calcular cor média
imagens_abertas = []
cores_totais = []
for imagem in imagens:
    try:
        img = Image.open(imagem)
        # Detectar orientação e ajustar
        if img.width > img.height:  # Imagem horizontal (paisagem)
            img = img.rotate(90, expand=True)
        # Converter para RGBA para preservar transparência
        if img.mode != 'RGBA':
            img = img.convert('RGBA')
        # Calcular a cor média
        cor_media = calcular_cor_media(img)
        cores_totais.append(cor_media)
        imagens_abertas.append((img, cor_media))
    except UnidentifiedImageError:
        print(f"Erro ao abrir a imagem: {imagem}")

if not imagens_abertas:
    print("Nenhuma imagem válida encontrada na pasta.")
    exit()

# Ordenar as imagens por escala de cores (luminosidade ou outro critério)
imagens_abertas.sort(key=lambda x: np.mean(x[1]))  # Ordenação por luminosidade média (média de RGB)

# Calcular a média geral das cores para criar a imagem faltante
cor_media_geral = tuple(int(np.mean([c[i] for c in cores_totais])) for i in range(3))

# Função para criar a imagem faltante e salvar na pasta Testes
def criar_e_salvar_cromo_faltante(cor, tamanho, texto="ATAMAiNET, 2025"):
    largura, altura = tamanho
    imagem = Image.new("RGBA", tamanho, cor + (255,))
    draw = ImageDraw.Draw(imagem)
    try:
        # Tente carregar uma fonte padrão do sistema
        fonte = ImageFont.truetype("arial.ttf", 40)
    except:
        # Use uma fonte padrão embutida no Pillow
        fonte = ImageFont.load_default()

    # Calcular o tamanho do texto
    texto_bbox = fonte.getbbox(texto)
    texto_largura = texto_bbox[2] - texto_bbox[0]
    texto_altura = texto_bbox[3] - texto_bbox[1]

    # Calcular a posição para centralizar o texto
    posicao = ((largura - texto_largura) // 2, (altura - texto_altura) // 2)

    # Adicionar o texto na imagem
    draw.text(posicao, texto, fill=(0, 0, 0, 255), font=fonte)

    # Salvar a imagem na pasta Testes
    caminho_imagem = os.path.join(pasta_testes, "cromo_faltante.png")
    imagem.save(caminho_imagem, "PNG")
    print(f"Imagem cromo faltante salva em: {caminho_imagem}")
    return imagem

# Criar e salvar a imagem cromo faltante
imagem_cromo_faltante = criar_e_salvar_cromo_faltante(
    cor=cor_media_geral,
    tamanho=(A4_WIDTH // NUM_COLUNAS, A4_HEIGHT // NUM_LINHAS)
)

# Adicionar a imagem faltante ao layout final
imagens_abertas.append((imagem_cromo_faltante, cor_media_geral))

# Criar uma nova imagem no formato A4 com fundo transparente
imagem_compilada = Image.new('RGBA', A4_SIZE, (255, 255, 255, 0))  # Fundo transparente (RGBA)

# Calcular o tamanho exato de cada célula para preencher o A4 sem espaços
celula_largura = A4_WIDTH // NUM_COLUNAS
celula_altura = A4_HEIGHT // NUM_LINHAS

# Preencher a matriz radial com as imagens
matriz = [[None for _ in range(NUM_COLUNAS)] for _ in range(NUM_LINHAS)]
imagens_dispostas = imagens_abertas

# Preencher as células da matriz
direcoes = [(0, 1), (1, 0), (0, -1), (-1, 0)]  # Direções: direita, baixo, esquerda, cima
x, y = 0, 0
direcao_atual = 0

for imagem, _ in imagens_dispostas:
    matriz[y][x] = imagem
    nx, ny = x + direcoes[direcao_atual][0], y + direcoes[direcao_atual][1]
    if not (0 <= nx < NUM_COLUNAS and 0 <= ny < NUM_LINHAS and matriz[ny][nx] is None):
        direcao_atual = (direcao_atual + 1) % 4
        nx, ny = x + direcoes[direcao_atual][0], y + direcoes[direcao_atual][1]
    x, y = nx, ny

# Redimensionar e colar as imagens na grade
for linha in range(NUM_LINHAS):
    for coluna in range(NUM_COLUNAS):
        if matriz[linha][coluna] is not None:
            imagem = matriz[linha][coluna]
            imagem_redimensionada = imagem.resize((celula_largura, celula_altura))
            pos_x = coluna * celula_largura
            pos_y = linha * celula_altura
            imagem_compilada.paste(imagem_redimensionada, (pos_x, pos_y), imagem_redimensionada)

# Função para gerar um nome único para o arquivo
def gerar_nome_arquivo(base_path, nome_base, extensao):
    contador = 1
    novo_nome = f"{nome_base}{extensao}"
    while os.path.exists(os.path.join(base_path, novo_nome)):
        novo_nome = f"{nome_base}_{contador}{extensao}"
        contador += 1
    return novo_nome

# Nome do arquivo base
nome_arquivo_base = "imagens_compiladas_a4"
extensao = ".png"

# Gerar o nome do arquivo final
output_path_png = os.path.join(pasta_testes, gerar_nome_arquivo(pasta_testes, nome_arquivo_base, extensao))

# Salvar a imagem compilada na pasta Testes
try:
    imagem_compilada.save(output_path_png, "PNG")
    print(f"Imagem compilada salva no formato A4 com fundo transparente na pasta Testes: {output_path_png}")
except OSError as e:
    print(f"Erro ao salvar a imagem compilada como PNG: {e}")