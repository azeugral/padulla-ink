/* Pedido de agendamento em 4 etapas. O Instagram não aceita texto pronto no link da DM,
   então o pedido é montado aqui, copiado e a DM abre numa aba nova para colar.
   O texto começa com "GOTH", a palavra que o Padulla pede nas reservas. */
(() => {
  const DM = 'https://ig.me/m/padulla_ink';
  const CHAVE = 'padulla-pedido-v1';
  const $ = (s, r = document) => r.querySelector(s);
  const $$ = (s, r = document) => [...r.querySelectorAll(s)];
  const calmo = matchMedia('(prefers-reduced-motion: reduce)').matches;

  const form = $('[data-pedido]'), etapas = $$('[data-etapa]', form), passos = $$('[data-passos] li');
  const bVoltar = $('[data-voltar]'), bAvancar = $('[data-avancar]'), bEnviar = $('[data-enviar]');
  const radio = n => { const r = $(`input[name="${n}"]:checked`); return r ? r.value : ''; };
  const val = id => $('#' + id).value.trim();
  let atual = 0, maxVisto = 0;

  /* com "Um disponível", aparece a escolha do desenho e a ideia vira opcional */
  const blocoFlash = $('[data-bloco-flash]');
  const tipo = () => {
    const d = radio('tipo') === 'Um disponível';
    blocoFlash.hidden = !d;
    $('[data-ideia-rotulo]').innerHTML = d ? 'Algum ajuste no desenho? <em>(opcional)</em>' : 'Como você imagina?';
  };
  $$('input[name="tipo"]').forEach(r => r.addEventListener('change', tipo));

  const validar = i => {
    let ok = true;
    if (i === 0) ok = !!radio('tipo') && (radio('tipo') !== 'Um disponível' || !!radio('flash'));
    if (i === 1) ok = !!radio('lugar') && !!radio('tamanho');
    if (i === 2) ok = radio('tipo') === 'Um disponível' || val('ideia').length > 0;
    if (i === 3) ok = val('nome').length > 0;
    $(`[data-erro="${i}"]`).hidden = ok;
    if (!ok) $(`[data-erro="${i}"]`).scrollIntoView({ behavior: calmo ? 'auto' : 'smooth', block: 'center' });
    return ok;
  };
  form.addEventListener('change', () => { $$('.erro-msg').forEach(e => e.hidden = true); });

  const texto = () => {
    const insta = val('insta').replace(/^@/, '');
    const l = [
      'GOTH',
      `Oi, Padulla! Sou ${val('nome') || '…'}${insta ? ` (@${insta})` : ''} e quero orçar uma tattoo pelo site.`,
      '',
      `Tipo: ${radio('tipo')}${radio('tipo') === 'Um disponível' && radio('flash') ? `, ${radio('flash')}` : ''}`,
      `Lugar: ${radio('lugar')}`,
      `Tamanho: ${radio('tamanho')}`
    ];
    if (val('ideia')) l.push(`Ideia: ${val('ideia')}`);
    if (val('ref')) l.push(`Referência: ${val('ref')}`);
    if (radio('primeira')) l.push(`Primeira tattoo: ${radio('primeira')}`);
    if (radio('quando')) l.push(`Pra quando: ${radio('quando')}`);
    return l.join('\n');
  };

  const ir = (i, foco = true) => {
    atual = Math.max(0, Math.min(etapas.length - 1, i));
    maxVisto = Math.max(maxVisto, atual);
    etapas.forEach((et, k) => et.hidden = k !== atual);
    passos.forEach((p, k) => {
      k === atual ? p.setAttribute('aria-current', 'step') : p.removeAttribute('aria-current');
      p.classList.toggle('feito', k < atual || (k <= maxVisto && k !== atual));
    });
    bVoltar.hidden = atual === 0;
    bAvancar.hidden = atual === etapas.length - 1;
    bEnviar.hidden = atual !== etapas.length - 1;
    $('[data-progresso]').style.transform = `scaleX(${(atual + 1) / etapas.length})`;
    if (atual === etapas.length - 1) $('[data-texto]').textContent = texto();
    if (foco) {
      const y = form.getBoundingClientRect().top + scrollY - 90;
      if (scrollY > y) scrollTo({ top: y, behavior: 'auto' });
      const h = $('h2', etapas[atual]); h.tabIndex = -1; h.focus({ preventScroll: true });
    }
  };
  bAvancar.addEventListener('click', () => { if (validar(atual)) { salvar(); ir(atual + 1); } });
  bVoltar.addEventListener('click', () => ir(atual - 1));
  $$('[data-ir]').forEach(b => b.addEventListener('click', () => {
    const alvo = +b.dataset.ir;
    for (let k = 0; k < alvo; k++) if (!validar(k)) return ir(k);
    ir(alvo);
  }));
  /* um toque numa opção de escolha única já avança, como num app */
  $$('input[name="lugar"], input[name="tamanho"]').forEach(r => r.addEventListener('change', () => {
    if (radio('lugar') && radio('tamanho')) setTimeout(() => { if (atual === 1) bAvancar.click(); }, 260);
  }));
  $$('input[name="nome"], #nome, #insta').forEach(el => el.addEventListener('input', () => { $('[data-texto]').textContent = texto(); }));
  form.addEventListener('keydown', e => {
    if (e.key === 'Enter' && e.target.tagName === 'INPUT') { e.preventDefault(); atual < etapas.length - 1 ? bAvancar.click() : bEnviar.click(); }
  });

  /* rascunho só neste navegador */
  const salvar = () => {
    try {
      const d = { e: maxVisto, c: {} };
      $$('input, textarea', form).forEach(el => {
        if (el.type === 'radio') { if (el.checked) d.c[el.name] = el.value; } else d.c[el.id] = el.value;
      });
      localStorage.setItem(CHAVE, JSON.stringify(d));
    } catch (e) { /* sem armazenamento */ }
  };
  form.addEventListener('input', salvar); form.addEventListener('change', salvar);
  try {
    const d = JSON.parse(localStorage.getItem(CHAVE) || 'null');
    if (d) {
      Object.entries(d.c).forEach(([k, v]) => {
        const r = $(`input[type="radio"][name="${k}"][value="${CSS.escape(v)}"]`);
        if (r) r.checked = true; else if ($('#' + k)) $('#' + k).value = v;
      });
      $('[data-rascunho]').textContent = 'Continuando de onde você parou.';
    }
  } catch (e) { /* ignora */ }

  /* vindo de "Quero esse" (?flash=id) ou de "arte do zero" (?tipo=autoral) */
  const q = new URLSearchParams(location.search);
  const fl = q.get('flash') && $(`input[name="flash"][data-id="${CSS.escape(q.get('flash'))}"]`);
  if (fl) { $('input[name="tipo"][value="Um disponível"]').checked = true; fl.checked = true; }
  if (q.get('tipo') === 'autoral') $('input[name="tipo"][value="Arte autoral do zero"]').checked = true;
  tipo();
  ir(fl ? 1 : 0, false);

  const copiar = async t => {
    try { await navigator.clipboard.writeText(t); return true; } catch (e) {
      const a = document.createElement('textarea'); a.value = t; a.style.cssText = 'position:fixed;opacity:0';
      document.body.appendChild(a); a.select(); let ok = false; try { ok = document.execCommand('copy'); } catch (er) { /* */ }
      a.remove(); return ok;
    }
  };
  form.addEventListener('submit', async e => {
    e.preventDefault();
    for (let k = 0; k < etapas.length; k++) if (!validar(k)) return ir(k);
    const t = texto();
    /* a aba abre antes do await, senão o navegador bloqueia como pop-up */
    const aba = window.open(DM, '_blank');
    if (aba) aba.opener = null;
    const ok = await copiar(t);
    $('[data-texto-final]').textContent = t;
    if (!ok) $('.pronto h2').textContent = 'Copia o pedido abaixo';
    if (!aba) $('.pronto p').textContent = 'Toca em “Abrir a DM”, cola o texto na conversa e envia.';
    form.hidden = true; $('.ag-passos').hidden = true; $('.ag-prog').hidden = true; $('.ag-cab').hidden = true;
    const pr = $('[data-pronto]'); pr.hidden = false; scrollTo({ top: 0, behavior: 'auto' }); pr.focus({ preventScroll: true });
    try { localStorage.removeItem(CHAVE); } catch (er) { /* */ }
  });
  $('[data-copiar]').addEventListener('click', async e => {
    const ok = await copiar($('[data-texto-final]').textContent);
    e.currentTarget.querySelector('span').textContent = ok ? 'Copiado' : 'Selecione o texto e copie';
  });
})();
