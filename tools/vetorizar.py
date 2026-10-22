Esta versão do potracer traça o claro: para arte preta sobre papel fica inverter=False (vale também para a Cinnamott)."""
import os, numpy as np, potrace
from PIL import Image, ImageFilter
AQUI = os.path.dirname(os.path.abspath(__file__)); SITE = os.path.dirname(AQUI)
R = os.path.join(SITE, '..', '_ref', 'ig')
def vet(src, caixa, dst, escala=3, limiar=110, blur=1.2, inverter=False, girar=0):
    im = Image.open(os.path.join(R, src)).convert('L').crop(caixa)
    if girar: im = im.rotate(girar, expand=True, fillcolor=255)
    im = im.resize((im.width * escala, im.height * escala), Image.LANCZOS).filter(ImageFilter.GaussianBlur(blur * escala))
    a = np.array(im) > limiar
    if inverter: a = ~a
    path = potrace.Bitmap(a).trace(turdsize=12 * escala, alphamax=1.0, opticurve=True, opttolerance=0.3)
    ys, xs = np.where(np.array(im) <= limiar); pad = 4 * escala; h, w = a.shape  # caixa pelo traço escuro
    x0, y0, x1, y1 = max(xs.min() - pad, 0), max(ys.min() - pad, 0), min(xs.max() + pad, w), min(ys.max() + pad, h)
    parts = []
    for c in path:
        s = c.start_point; d = [f'M{s.x:.1f} {s.y:.1f}']
        for seg in c.segments:
            if seg.is_corner: d.append(f'L{seg.c.x:.1f} {seg.c.y:.1f}L{seg.end_point.x:.1f} {seg.end_point.y:.1f}')
            else: d.append(f'C{seg.c1.x:.1f} {seg.c1.y:.1f} {seg.c2.x:.1f} {seg.c2.y:.1f} {seg.end_point.x:.1f} {seg.end_point.y:.1f}')
        parts.append(''.join(d) + 'Z')
    open(os.path.join(SITE, 'assets', 'img', dst), 'w').write(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{x0} {y0} {x1-x0} {y1-y0}"><path fill="#000" fill-rule="evenodd" d="{"".join(parts)}"/></svg>')
    print(dst, len(parts), 'contornos', x1 - x0, 'x', y1 - y0)
vet('006_1.jpg', (412, 1219, 937, 1369), 'ornamento.svg')
