// Busca vídeos no TikTok por palavra-chave (ou lista um perfil) com a sessão logada da conta de busca.
// Uso: node tiktok_busca.mjs "termo 1" "termo 2" ... [--rolagens=6] [--saida=resultados.jsonl] [--cookies=arquivo.txt]
//      node tiktok_busca.mjs "#hashtag" "discover:slug-da-pagina" ...
// Cada termo vira 3 fontes: busca logada (o TikTok costuma pedir captcha para servidor), a página de hashtag
// (/tag/<termo sem espaço>) e a página discover (/discover/<termo-com-hifen>). Hashtag e discover funcionam
// sem login e sem captcha — são a fonte principal.
// Login: variável de ambiente TIKTOK_COOKIES (conteúdo de um cookies.txt no formato Netscape, puro ou em
// base64) ou TIKTOK_SESSIONID (só o cookie sessionid). Nunca grave cookies no repositório.
import { chromium } from 'playwright-core';
import fs from 'node:fs';

const args = process.argv.slice(2);
const opt = Object.fromEntries(args.filter(a => a.startsWith('--')).map(a => a.slice(2).split('=')));
const termos = args.filter(a => !a.startsWith('--'));
const rolagens = Number(opt.rolagens ?? 6);
const saida = opt.saida ?? 'resultados.jsonl';
const CHROME = process.env.CHROME_PATH ?? '/opt/pw-browsers/chromium-1194/chrome-linux/chrome';

function cookies() {
  const out = [];
  let txt = process.env.TIKTOK_COOKIES ?? (opt.cookies ? fs.readFileSync(opt.cookies, 'utf8') : '');
  if (txt && !txt.includes('\t')) { try { txt = Buffer.from(txt, 'base64').toString('utf8'); } catch {} }
  for (const l of txt.split('\n')) {
    const p = l.split('\t');
    if (p.length >= 7 && p[0].includes('tiktok')) {
      out.push({ name: p[5], value: p[6].trim(), domain: p[0].replace(/^#HttpOnly_/, ''), path: p[2], secure: p[3] === 'TRUE', httpOnly: l.startsWith('#HttpOnly_') });
    }
  }
  if (!out.length && process.env.TIKTOK_SESSIONID) {
    for (const name of ['sessionid', 'sessionid_ss', 'sid_tt'])
      out.push({ name, value: process.env.TIKTOK_SESSIONID, domain: '.tiktok.com', path: '/', secure: true, httpOnly: true });
  }
  return out;
}

const browser = await chromium.launch({ executablePath: CHROME, args: ['--no-sandbox', '--disable-blink-features=AutomationControlled'] });
const ctx = await browser.newContext({
  userAgent: 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36',
  viewport: { width: 1280, height: 900 }, locale: 'pt-BR',
});
const ck = cookies();
if (ck.length) await ctx.addCookies(ck);
const page = await ctx.newPage();
// contexto anônimo: hashtag/discover abrem sem captcha quando NÃO há login (logado o TikTok pede captcha)
const ctxAnon = await browser.newContext({
  userAgent: 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36',
  viewport: { width: 1280, height: 900 }, locale: 'pt-BR',
});
const pageAnon = await ctxAnon.newPage();

// checa o login
await page.goto('https://www.tiktok.com/explore', { waitUntil: 'domcontentloaded', timeout: 60000 });
const conta = await page.evaluate(() => fetch('/passport/web/account/info/?aid=1459', { credentials: 'include' })
  .then(r => r.json()).catch(() => ({})));
const logado = Boolean(conta?.data?.username);
if (logado) console.error(`✓ logado como @${conta.data.username}`);
else console.error(`✗ sem login válido (${conta?.data?.name ?? 'sem cookie'}) — busca por palavra-chave não retorna resultados`);

const vistos = new Map();
function guardar(it, termo) {
  const v = it?.item ?? it;
  if (!v?.id || vistos.has(v.id)) return;
  vistos.set(v.id, {
    termo, id: v.id, url: `https://www.tiktok.com/@${v.author?.uniqueId}/video/${v.id}`,
    autor: v.author?.uniqueId, legenda: (v.desc ?? '').slice(0, 200),
    duracao: v.video?.duration, largura: v.video?.width, altura: v.video?.height,
    plays: v.stats?.playCount ?? v.statsV2?.playCount, likes: v.stats?.diggCount ?? v.statsV2?.diggCount,
    criado: v.createTime,
  });
}
let termoAtual = '';
for (const pg of [page, pageAnon]) pg.on('response', async r => {
  // só resultados da busca/hashtag/discover — o feed "para você" que a página carrega por trás é ignorado
  if (!/\/api\/(search\/(item|general)|challenge\/item_list|discover|explore\/item_list|post\/item_list)/.test(r.url())) return;
  try {
    const j = await r.json();
    for (const it of (j.itemList ?? j.item_list ?? (Array.isArray(j.data) ? j.data : []))) guardar(it, termoAtual);
  } catch {}
});

function fontes(termo) {
  if (termo.startsWith('#')) return [`https://www.tiktok.com/tag/${encodeURIComponent(termo.slice(1))}`];
  if (termo.startsWith('discover:')) return [`https://www.tiktok.com/discover/${termo.slice(9)}`];
  if (termo.startsWith('@')) return [`https://www.tiktok.com/${termo}`];
  const semAcento = termo.normalize('NFD').replace(/[\u0300-\u036f]/g, '').toLowerCase().trim();
  const out = [`https://www.tiktok.com/tag/${encodeURIComponent(semAcento.replace(/\s+/g, ''))}`,
               `https://www.tiktok.com/discover/${encodeURIComponent(semAcento.replace(/\s+/g, '-'))}`];
  if (logado) out.unshift(`https://www.tiktok.com/search/video?q=${encodeURIComponent(termo)}`);
  return out;
}

for (const termo of termos) {
  termoAtual = termo;
  for (const url of fontes(termo)) {
    const pg = url.includes('/search/') ? page : pageAnon;
    const antes = vistos.size;
    try {
      await pg.goto(url, { waitUntil: 'domcontentloaded', timeout: 60000 });
      await pg.waitForTimeout(5000);
      for (let i = 0; i < rolagens; i++) { await pg.mouse.wheel(0, 3000); await pg.waitForTimeout(1800); }
    } catch (e) { console.error(`  ${url}: erro ${e.message.slice(0, 80)}`); continue; }
    const captcha = await pg.$('text=/quebra-cabe|captcha|deslizante|puzzle/i');
    console.error(`  "${termo}" ${url.split('.com')[1]}: +${vistos.size - antes} vídeos${captcha ? ' (captcha)' : ''}`);
  }
}
fs.writeFileSync(saida, [...vistos.values()].map(v => JSON.stringify(v)).join('\n') + '\n');
console.error(`${vistos.size} vídeos em ${saida}`);
await browser.close();
