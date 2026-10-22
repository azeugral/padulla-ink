"""Gera as imagens do site a partir de _ref/ig (posts do Instagram, chaves "001" = mais novo).
Uso: python tools/processar.py"""
import json, os
from PIL import Image, ImageOps, ImageEnhance
AQUI = os.path.dirname(os.path.abspath(__file__)); SITE = os.path.dirname(AQUI)
R = os.path.join(SITE, '..', '_ref', 'ig')
A = os.path.join(SITE, 'assets', 'img')
for d in ('obras', 'flash'): os.makedirs(os.path.join(A, d), exist_ok=True)

# (post, categoria, título, foto de capa, desvio vertical do recorte 0..1)
OBRAS = [
 (9, 'tribal', 'Cybertribal no peito', 4, .45),
 (10, 'goth', 'Espada cybertribal no antebraço', 5, .5),
 (1, 'sigil', 'Saint com caligrafia', 2, .5),
 (24, 'tribal', 'Darktribal na mão', 3, .5),
 (60, 'tribal', 'Dark cybertribal no ombro', 1, .4),
 (12, 'goth', 'Leão cyber, autoral', 2, .5),
 (28, 'floral', 'Cybersigilism com lírios', 3, .5),
 (7, 'sigil', 'Cyber delicada no ombro', 2, .5),
 (46, 'goth', 'Anjo em cyberescultura', 4, .45),
 (39, 'letra', 'Loyalty', 3, .5),
 (72, 'goth', 'Asas cybergóticas nas costas', 1, .5),
 (59, 'tribal', 'Cybertribal no antebraço', 1, .45),
 (8, 'goth', 'Freehand gótico com decalque', 4, .5),
 (50, 'goth', 'Adaga medieval', 4, .5),
 (54, 'sigil', 'Cybertribal fino no braço', 1, .4),
 (62, 'floral', 'Lírios cyberflorais, Tame Impala', 1, .5),
 (26, 'tribal', 'Bring Me The Horizon, autoral', 2, .45),
 (47, 'letra', 'Born to die na costela', 3, .5),
 (66, 'tribal', 'Pelagem de gatinho bravo', 1, .5),
 (76, 'goth', 'Espadona na perna inteira', 2, .35),
 (32, 'goth', 'Sereia autoral', 3, .45),
 (48, 'sigil', 'Arabesco cyber no pé', 1, .5),
 (56, 'goth', 'Cybergótica de arquitetura', 1, .3),
 (68, 'floral', 'Cyberfloral no antebraço', 2, .5),
 (34, 'goth', 'Aranha cyber no pescoço', 1, .5),
 (79, 'tribal', 'Morcegão na lombar', 1, .5),
 (49, 'letra', 'Frases simétricas nas pernas', 2, .45),
 (61, 'goth', 'Espada cybergótica', 2, .5),
 (16, 'goth', 'Caveira punk com freehand', 1, .5),
 (109, 'tribal', 'Borboleta cybertribal', 1, .5),
 (17, 'goth', 'Memento mori', 1, .4),
 (75, 'floral', 'Lírio fluido em preto e vermelho', 1, .5),
 (91, 'sigil', 'Freehand na costela', 2, .5),
 (70, 'tribal', 'Bracelete cybertribal', 1, .5),
 (85, 'goth', 'Caveira autoral', 1, .45),
 (105, 'tribal', 'Cybertribal no cóccix', 2, .5),
 (99, 'sigil', 'Estrela cybersigil', 1, .5),
 (77, 'goth', 'Espadona de respeito', 1, .5),
 (83, 'goth', 'Gatinho gótico', 1, .5),
 (88, 'tribal', 'Rosto com tribal', 1, .5),
]
# fotos com texto por cima, que ficam fora da galeria
FORA = {'010_1', '087_3', '087_4', '087_5', '096_2', '096_3'}
HERO = [(9, 4, .45, 'Cybertribal no peito'), (10, 5, .5, 'Espada cybertribal'), (24, 3, .5, 'Darktribal na mão'),
        (1, 2, .5, 'Saint com caligrafia'), (60, 1, .4, 'Dark cybertribal no ombro')]
# flashes da folha de disponíveis de outubro (006_1, 1350x1687): (nome, título, caixa)
FLASH = [('estrela', 'Estrela em halftone', (20, 40, 545, 565)),
         ('coracao', 'Coração tribal', (600, 15, 995, 525)),
         ('anjo', 'Anjo de pedra', (281, 525, 806, 1238)),
         ('moonlight', 'Moonlight', (810, 30, 1295, 860)),
         ('cruz', 'Cruz ornamental', (805, 880, 1310, 1615)),
         ('sweet', 'Sweet life com terço', (410, 1385, 1055, 1650))]

def corta(im, ar, dy=.5):
    w, h = im.size
    if w / h > ar: nw = int(h * ar); x = (w - nw) // 2; return im.crop((x, 0, x + nw, h))
    nh = int(w / ar); y = int((h - nh) * dy); return im.crop((0, y, w, y + nh))
def salva(im, p, w, q=80):
    im = im.convert('RGB')
    if im.width > w: im = im.resize((w, round(im.height * w / im.width)), Image.LANCZOS)
    im.save(p, 'WEBP', quality=q, method=6)
def abre(f): return ImageOps.exif_transpose(Image.open(os.path.join(R, f)))

dados = json.load(open(os.path.join(R, 'dados.json'), encoding='utf8'))
saida = []
for i, (n, cat, tit, capa, dy) in enumerate(OBRAS, 1):
    p = dados[f'{n:03d}']; fotos = []
    for k, f in enumerate([x for x in p['fotos'] if not x['video']], 1):
        nome = f['f'][:-4]
        if k == capa: salva(corta(abre(f['f']), 4 / 5, dy), os.path.join(A, 'obras', f'{i:02d}.webp'), 720, 78)
        if nome in FORA: continue
        salva(abre(f['f']), os.path.join(A, 'obras', f'{i:02d}-{k}.webp'), 1280, 80); fotos.append(f'{i:02d}-{k}')
    saida.append({'id': f'{i:02d}', 'cat': cat, 'titulo': tit, 'fotos': fotos, 'data': p['data'], 'ig': p['code']})
for i, (n, k, dy, _) in enumerate(HERO, 1):
    salva(corta(abre(f'{n:03d}_{k}.jpg'), 4 / 5, dy), os.path.join(A, f'hero-{i}.webp'), 900, 82)
folha = abre('006_1.jpg').convert('RGB')
for nome, _, cx in FLASH:
    # o fundo de oncinha cinza da folha vira papel liso; o traço preto fica
    im = ImageEnhance.Contrast(folha.crop(cx)).enhance(1.12).point(lambda v: 255 if v > 196 else min(255, int(v * 1.08)))
    salva(im, os.path.join(A, 'flash', nome + '.webp'), 900, 84)
salva(corta(abre('031_2.jpg'), 4 / 5, .3), os.path.join(A, 'padulla.webp'), 800, 82)
json.dump(saida, open(os.path.join(SITE, 'assets', 'obras.json'), 'w', encoding='utf8'), ensure_ascii=False, indent=1)
print(len(saida), 'obras,', sum(len(o['fotos']) for o in saida), 'fotos')
