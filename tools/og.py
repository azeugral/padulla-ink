"""Gera og.jpg (1200x630) e os favicons (P gótico em vermelho, fundo transparente) com Playwright/Edge."""
import os, pathlib
from playwright.sync_api import sync_playwright
B = pathlib.Path(__file__).resolve().parent.parent
u = lambda p: (B / p).as_uri()
FONTES = '<link href="https://fonts.googleapis.com/css2?family=UnifrakturMaguntia&family=JetBrains+Mono:wght@500&display=swap" rel="stylesheet">'
og = f"""{FONTES}<body style="margin:0;width:1200px;height:630px;background:#070505 url({u('assets/img/fumaca.webp')}) center/cover;color:#efe8df;position:relative;overflow:hidden">
<img src="{u('assets/img/hero-1.webp')}" style="position:absolute;right:70px;top:65px;width:400px;height:500px;object-fit:cover;border:1px solid rgba(239,232,223,.2)">
<div style="position:absolute;left:80px;top:0;height:630px;display:flex;flex-direction:column;justify-content:center;gap:26px">
<div style="font:22px 'JetBrains Mono';letter-spacing:.2em;text-transform:uppercase;color:#f02a2f">Tatuador em São Paulo</div>
<div style="font:190px/.86 'UnifrakturMaguntia';text-shadow:0 0 40px rgba(211,20,29,.4)">Padulla</div>
<div style="font:22px/1.5 'JetBrains Mono';letter-spacing:.08em;color:#d9d0c7">cybertribal · cybersigilism<br>Estúdio Súbito, Vila Mariana</div></div></body>"""
ico = f"""{FONTES}<body style="margin:0;width:512px;height:512px;background:transparent;display:flex;align-items:center;justify-content:center">
<span style="font:500px/1 'UnifrakturMaguntia';color:#d3141d;transform:translateY(-4%)">P</span></body>"""
with sync_playwright() as p:
    br = p.chromium.launch(channel='msedge')
    pg = br.new_page(viewport={'width': 1200, 'height': 630})
    tmp = B / 'tools/_og.html'
    tmp.write_text(og, encoding='utf8'); pg.goto(tmp.as_uri()); pg.wait_for_timeout(1500)
    pg.screenshot(path=str(B / 'og.jpg'), type='jpeg', quality=84)
    pg = br.new_page(viewport={'width': 512, 'height': 512})
    tmp.write_text(ico, encoding='utf8'); pg.goto(tmp.as_uri()); pg.wait_for_timeout(1500)
    pg.screenshot(path=str(B / 'tools/_ico.png'), omit_background=True)
    tmp.unlink(); br.close()
from PIL import Image
im = Image.open(B / 'tools/_ico.png'); im = im.crop(im.getbbox())
lado = max(im.size) + 24; q = Image.new('RGBA', (lado, lado)); q.paste(im, ((lado - im.width) // 2, (lado - im.height) // 2))
for nome, t in [('favicon-32.png', 32), ('favicon-64.png', 64)]: q.resize((t, t), Image.LANCZOS).save(B / nome, optimize=True)
fundo = Image.new('RGBA', (lado, lado), '#070505'); fundo.alpha_composite(q); fundo.convert('RGB').resize((180, 180), Image.LANCZOS).save(B / 'apple-touch-icon.png')
(B / 'tools/_ico.png').unlink()
print('ok', os.path.getsize(B / 'og.jpg') // 1024, 'KB')
