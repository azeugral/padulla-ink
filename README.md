# Padulla Ink

Site do Padulla ([@padulla_ink](https://www.instagram.com/padulla_ink/)), tatuador de cybertribal, cybersigilism e blackwork no Estúdio Súbito (Vila Mariana, São Paulo).

Publicado em https://azeugral.github.io/padulla-ink/ (com `noindex` até a aprovação).

## Páginas
- `index.html`: hero com fumaça em shader, disponíveis, estilos, portfólio com filtro e galeria, como agendar, cuidados, sobre, estúdio.
- `agendar.html`: pedido em 4 etapas (desenho, corpo, ideia, você). O texto sai com "GOTH" na frente, é copiado e a DM abre em outra aba. O Instagram não aceita texto pronto no link da DM, por isso a cópia.

## Ferramentas (`tools/`)
- `processar.py`: gera `assets/img` e `assets/obras.json` a partir de `../_ref/ig` (lista OBRAS, HERO e FLASH).
- `vetorizar.py`: ornamento da folha de disponíveis em SVG (usado como máscara).
- `gerar_video.py`: renderiza `assets/js/fumaca.js` em MP4 para celular e o pôster.
- `og.py`: `og.jpg` e favicons.

## CONFIRMAR com o cliente
- [ ] Nome para o site: hoje é só "Padulla". Usa nome completo?
- [ ] Preço dos disponíveis: o site diz "a partir de R$ 280" (post de junho/2026; em janeiro era R$ 290).
- [ ] Valor e forma de pagamento do sinal (o destaque "sinal" é só vídeo falado).
- [ ] Quais flashes da folha de outubro ainda estão livres (estrela, coração, anjo, Moonlight, cruz, Sweet life).
- [ ] Endereço do Estúdio Súbito: o site só diz Vila Mariana, a 3 min do metrô Ana Rosa, e manda o endereço pela DM. O botão de mapa aponta para a estação.
- [ ] Se ele quer receber pedidos também por WhatsApp ou e-mail.
- [ ] Foto do "Quem tatua" (selfie do dump de maio). Tem uma preferida?
- [ ] Domínio próprio (o perfil mostra padulla.ink como nome).
