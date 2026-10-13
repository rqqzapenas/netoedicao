---
name: criativo-broll
description: >
  Editar criativos de anúncio 100% b-roll no método do Neto (TikTok, Facebook, Instagram, 9:16) —
  voz feminina de IA do início ao fim, b-roll de receita/produto cortado em cenas de no máximo 2 s,
  partes diferentes do mesmo b-roll reaproveitadas, música alegre entrando seca no segundo 22, CTA
  "Clique no botão abaixo" + ícone do WhatsApp com badge, e cauda final de ~11 s só com música, texto e
  b-roll. Use SEMPRE que o pedido for montar, editar, renderizar, revisar ou analisar um criativo/anúncio
  em vídeo de produto/oferta (receitas, infoproduto, CTWA/WhatsApp), mesmo que o usuário só mande
  b-rolls + voz, diga "monta o criativo", "edita no meu método", "sobe a voz nesses b-rolls", ou mande
  um criativo de referência para dissecar. Constrói o projeto HyperFrames e renderiza o MP4.
---

# Criativo b-roll — método do Neto

Esses criativos faturam milhões por mês. **Cada elemento abaixo é proposital: replique-o exatamente**,
não "melhore" com legendas, transições, zooms ou efeitos que o método não usa. Quando estiver em dúvida,
faça como a referência (`references/anatomia-gelato.md`, medida frame a frame).

## Por que funciona (a lógica por trás de cada regra)

1. **O olho nunca descansa.** Cena ≤ 2 s (mediana ~1,35 s) e só corte seco: a cada piscada tem uma imagem
   nova e apetitosa. Em feed de rolagem, isso segura a retenção melhor que qualquer efeito.
2. **O desejo vem antes da explicação.** Os primeiros 5 s são só produto pronto ("money shot"): bola
   saindo da boleadora, casquinha erguida, calda escorrendo. Cortes acelerando (1,4 → 0,3 s) = gancho visual
   que trabalha junto do gancho falado.
3. **"É fácil e eu consigo."** Logo depois vêm ingredientes simples e processo caseiro (açúcar, ovo, máquina,
   espátula) — prova de que dá para fazer em casa.
4. **"Tem MUITA coisa."** Blocos de 5–15 s, cada um com um sabor/variação diferente → percepção de
   volume de conteúdo (muitas receitas no produto).
5. **Prova social sem talking head.** A cada ~20 s, uma pessoa feliz segurando/provando o produto — sem
   falar para a câmera. Humaniza sem quebrar o formato b-roll.
6. **Familiaridade sem repetição.** O mesmo b-roll volta 15–30 s depois, em **outro trecho**: o cérebro
   reconhece ("já vi, é bom") mas a imagem é nova. Também economiza b-roll.
7. **Ritmo em ondas.** Rápido → médio → calmo → rajada → calmo → rajada → cauda calma. Rajadas
   (0,6–0,9 s) acordam o espectador antes de ele cansar.
8. **A voz vende, a música dá energia.** Os primeiros 22 s são só voz (gancho + promessa entendidos
   sem disputa). A música entra seca no 22 — uma "virada" de energia exatamente quando a atenção cairia.
   Música alegre e coerente com a receita = emoção positiva associada ao produto.
9. **CTA visual + falado ao mesmo tempo.** O texto/ícone aparece quando a voz fala o fechamento
   (~4 s antes de a voz acabar). Verde + ícone do WhatsApp com badge "1" = "tem mensagem esperando",
   coerente com o funil CTWA.
10. **Cauda de ~11 s só música + CTA + b-roll.** Silêncio de voz = espaço para a decisão; o b-roll
    apetitoso continua alimentando o desejo enquanto o botão está na tela. Também deixa o vídeo
    "loopar" bem e alonga o tempo de visualização.

## Regras de edição (números exatos)

### Formato
- 1080x1920, 30 fps, H.264 + AAC. Vertical nativo. Duração = fim da voz + ~11 s (a referência tem 82,5 s).
- B-roll em tela cheia (`object-fit: cover`), sem bordas, sem moldura, sem marca d'água por cima.

### Cortes
- **Máximo 2,0 s por cena. Sempre.** Mediana alvo ~1,35 s, média ~1,4–1,5 s.
- **Só corte seco**: nenhuma transição, fade, zoom, punch-in, shake, filtro ou velocidade alterada.
- Gancho 0–5,5 s: 6 cenas ≈ 1,43 · 1,13 · 0,83 · 0,67 · **0,27 (flash)** · 1,13, só produto final/textura.
- Flashes de 0,17–0,33 s de vez em quando (outro trecho/ângulo de algo já visto) para dar "soco".
- Rajadas de 4–6 cortes de 0,6–0,9 s a cada ~20–25 s; entre elas, cenas de 1,5–2,0 s.
- Cauda (CTA): cenas mais longas, 1,6–2,0 s.
- Nunca o mesmo b-roll em duas cenas seguidas.

### B-roll (ordem de uso)
| Categoria | Nome do arquivo | Onde entra |
|---|---|---|
| Produto final / money shot | `final_*.mp4` | gancho (0–5 s), voltas ao longo do vídeo, cauda |
| Processo / ingredientes | `processo_*.mp4` | 5–13 s e reinícios de bloco |
| Textura / ASMR (calda, raspar, macro) | `textura_*.mp4` | corpo e rajadas |
| Reação humana (sem falar p/ câmera) | `reacao_*.mp4` | ~25 s e ~46 s (a cada ~20 s) |
| Sem prefixo | qualquer | coringa |

- Clipes verticais de TikTok com **mão/utensílio em movimento**, luz quente, cozinha clara e bonita.
- Variedade: cada bloco de 5–15 s mostra uma variação diferente do produto.
- **Reaproveitar o mesmo b-roll em partes diferentes**: 2º uso em outro trecho do arquivo, 15–30 s depois.
- Nunca usar b-roll com rosto falando para a câmera (o método é 100% b-roll), nem com texto/legenda
  queimado de outro criador se der para evitar.

### Voz
- Feminina, gerada no MiniMax/ElevenLabs. **Uma voz fixa por produto** (ver `produtos.json`).
- Entra em ~0,2 s (praticamente no primeiro frame) e fala sem parar até o CTA.
- Pausas entre frases apertadas para 0,15–0,25 s (o script faz isso).
- Nível: −16 LUFS (o script normaliza).

### Música
- Alegre, coerente com a receita/produto, ~100–120 BPM (referência: ~110). **Uma música fixa por produto.**
- **Entra seca no segundo 22,0** (sem fade-in) e vai até o último frame (sem fade-out).
- ~11 LU abaixo da voz (−27 LUFS), nível constante: **sem ducking e sem subir na cauda**.

### Texto na tela
- **Zero legenda durante a narração.** O único texto é o CTA.
- CTA: "Clique no / botão abaixo" (2 linhas), entra **~4 s antes da voz acabar**, no meio de uma cena,
  e fica até o fim.
- Animação: grupo texto + ícone cresce de 0 → 100% em 0,33 s (10 frames) a partir do centro, sem bounce.
- Estilo: Montserrat SemiBold ~122 px, branco com contorno preto grosso, cada linha sobre faixa verde
  `#009407` com bordas irregulares de pincel; bloco em y ≈ 580–830 (30–43% da altura).
- Ícone: balão verde do WhatsApp com telefone branco, contorno branco de sticker, badge vermelho "1",
  ~380 px, centro em (540, ~1240). Fora das zonas de UI do TikTok/Reels (rodapé e lateral direita).

## Fluxo de trabalho

1. **Setup da sessão**: `scripts/setup.sh` na raiz do repo (Chrome do render). CDNs são bloqueados:
   tudo que o HTML usa fica local (a skill já traz `assets/gsap.min.js`, fontes e o ícone).
2. **Material**: voz (mp3/wav), música do produto e uma pasta de b-rolls com os prefixos de categoria.
   Se o usuário não mandar voz/música, use as padrão do produto em `produtos.json` na raiz do repo.
   Peça o que faltar — **nunca invente voz ou música**. Quanto mais b-rolls (ideal 12–25 clipes de
   5–20 s, de 4–8 variações do produto), melhor a variedade.
3. **Classifique os b-rolls**: abra uma folha de contato de cada um
   (`ffmpeg -i x.mp4 -vf "fps=1,scale=180:-1,tile=6x2" x.png`), renomeie com o prefixo certo e descarte
   clipes com talking head, texto queimado grande, horizontal com faixas ou muito escuros.
4. **Spec** (`spec.json` ao lado do material):
   ```json
   {
     "nome": "gelatos_ad07",
     "produto": "gelatos",
     "voz": "voz.mp3",
     "musica": "musica.mp3",
     "musica_offset": 0,
     "broll_dir": "broll",
     "cta_linhas": ["Clique no", "botão abaixo"],
     "seed": 1
   }
   ```
   Opcionais: `broll_dirs` (lista), `cauda` (padrão 11), `cta_antecedencia` (padrão 4),
   `apertar_pausas` (padrão true), `clips` (EDL manual `[{"src","in","dur"}]` que ignora o planejador).
5. **Monte**: `python3 .claude/skills/criativo-broll/scripts/montar_criativo.py spec.json`
   → gera a pasta do projeto com `index.html`, `edl.json` (plano de cortes) e relatório de conformidade.
   Leia o relatório: máx ≤ 2,00 s, 0 b-roll em sequência, reaproveitamento > 0, música no 22.
6. **Revise o plano** (`edl.json`): as 6 primeiras cenas precisam ser produto final de dar água na boca;
   troque `seed` ou renomeie categorias se o gancho ficou fraco. Ajuste fino → passe a usar `clips`.
7. **Renderize**: `--render` no mesmo comando (ou `npx hyperframes render -o saida.mp4` na pasta).
   Render local leva ~4x o tempo do vídeo; rode em segundo plano.
8. **Confira o MP4** antes de entregar:
   - `scripts/analisar_referencia.sh saida.mp4` → cenas ≤ 2 s, música entrando em ~22 s,
     voz até ~(fim − 11 s), cauda só música.
   - Olhe as folhas de contato: gancho forte, nenhuma cena preta/congelada, CTA legível.
9. **Entregue** com `SendUserFile` e um resumo de 3–5 linhas (duração, nº de cenas, b-rolls usados).

## Analisando novas referências do usuário
Rode `scripts/analisar_referencia.sh video.mp4 pasta/` e leia as folhas, o espectrograma e `cenas.tsv`.
Compare com as regras acima; **se encontrar um padrão novo e consistente em vários criativos, adicione-o
a esta skill** (e ao `references/`), com o número medido e o porquê.

## Pendências conhecidas (para a próxima rodada de treino)
- Os criativos das duas pastas do Drive e o projeto do CapCut (`ad2_gelatos`) ainda não foram analisados
  (a rede deste ambiente bloqueia drive.google.com e o arquivo do CapCut está só no Mac do usuário).
  Quando chegarem, confirme/ajuste: tamanho e posição do CTA, nível da música, duração da cauda, se há
  efeitos/keyframes no projeto CapCut (o `draft_content.json` revela cada corte, velocidade e volume
  exatos) e se a música começa sempre no 22 ou em outro ponto conforme o produto.
- Captura de b-roll do TikTok: skill futura.
