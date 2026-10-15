---
name: criativo-broll
description: >
  Editar criativos de anúncio 100% b-roll no método do Neto (TikTok, Facebook, Instagram, 9:16) — voz
  feminina de IA do início ao fim, hook visual que mostra EXATAMENTE o que a primeira frase fala, b-roll
  sincronizado com o que a voz nomeia, cenas de no máximo 2 s só com corte seco, partes diferentes do mesmo
  b-roll reaproveitadas, música alegre por baixo desde o início (a partir do 0:22 da faixa), CTA "Clique no
  botão abaixo" + ícone do WhatsApp com badge entrando junto com a fala do CTA, e cauda final só com
  música, texto e b-roll. Use SEMPRE que o pedido for montar, editar, renderizar, revisar ou analisar um
  criativo/anúncio em vídeo de produto/oferta (receitas, infoproduto, CTWA/WhatsApp, Brasil ou México),
  mesmo que o usuário só mande b-rolls + voz + música, diga "monta o criativo", "edita no meu método", ou
  mande um criativo de referência para dissecar. Esta skill é a BASE de toda edição deste repositório.
---

# Criativo b-roll — método do Neto

Esses criativos faturam milhões por mês. **Cada elemento é proposital: replique exatamente.** Não "melhore"
com legendas, zooms, efeitos ou transições que o método não usa. Na dúvida, faça como as referências medidas
frame a frame em `references/`:
- `anatomia-salsas.md` — o criativo que **mais faturou** (México, espanhol). Leia primeiro.
- `anatomia-gelato.md` — criativo Brasil (português).
- `lote-drive-30.md` — **os 30 criativos das duas ofertas medidos**: perfil de mixagem por produto e as
  famílias de gancho com a imagem que cada uma usa. Tabela por vídeo em `lote_drive_30_medidas.tsv`.

## A regra nº 1: o que a voz fala, a tela mostra

**O hook visual SEMPRE é congruente com o hook falado.** Salsas: "¿Tú crees que *estos frasquitos*…?" →
os primeiros 4,6 s são só os frasquinhos. Gelato: "Sabe aquele *gelato* de casquinha que custa uma
fortuna?" → os primeiros 5,5 s são gelato sendo servido. A pessoa ouve e vê a mesma coisa no mesmo
instante: o cérebro não precisa traduzir nada, e o "estos/esse/aquele" da frase aponta para a tela.

E a congruência continua o vídeo inteiro: **cada vez que a voz nomeia algo concreto** (ingrediente,
variedade, pote, dinheiro, produto pronto), **o b-roll mostra aquilo na mesma hora** (até ~1 s depois).
Exemplos medidos: "3 ingredientes" → açúcar/ovo/leite; "pote de 1 litro" → creme indo para o pote;
"chocolate" → raspas de chocolate; "mermeladas de chile" → mermelada de chile; "chile de árbol" →
salsa caindo com chiles de árbol em volta; "habanero" → habaneros na mão. Frases abstratas (história,
autoridade, "é técnica") ficam com b-roll bonito de processo/variedade.

**Quando a frase de abertura não nomeia nada visível** (história de dor: "me demitiram porque engravidei",
"meu ex-marido disse…", "trabalhava 12 h num hospital"), a abertura mostra **o produto sendo feito ou
servido**, no plano mais apetitoso: a virada, o "hoje". Não se ilustra a dor. Medido nos 30 criativos;
a tabela de famílias de gancho × imagem está em `references/lote-drive-30.md`. Resumo:
- demonstrativo + objeto ("esses potinhos") → o objeto;
- ingredientes ("un puñito de chiles y una cebolla") → os ingredientes, na ordem falada;
- "vem comigo" → pessoa ou produção;
- inimigo/mercado ("conservadores", "pote do mercado") → o inimigo;
- promessa de "100 receitas" → variedade;
- lista → o 1º item.

**Antes de montar, leia a copy e marque cada substantivo concreto.** Cada um vira uma âncora de
sincronia (`sincronia` no spec). O gancho vira o clipe `gancho`. Se não houver b-roll para um item
importante, avise o usuário antes de renderizar.

## Por que o resto funciona

1. **O olho nunca descansa.** Cena ≤ 2 s (mediana ~1,35 s), corte seco: a cada piscada, uma imagem nova
   e apetitosa. Isso segura a retenção no feed.
2. **Primeiro o desejo, depois a explicação.** Gancho só com o objeto do hook. Logo depois: processo
   caseiro simples ("é fácil, eu consigo"), e então blocos de variedade ("tem MUITA coisa").
3. **Prova social sem talking head.** Pessoas felizes com o produto, ou cozinhando, a cada ~20 s, mas
   nunca falando para a câmera.
4. **Familiaridade sem repetição.** O mesmo b-roll volta 15–30 s depois, em **outro trecho**.
5. **Ritmo em ondas.** Rápido → médio → calmo → rajada → calmo → rajada → cauda. As rajadas (cortes de
   0,13–0,9 s) caem em momentos de virada (oferta, prova, "antes de pagar").
6. **A voz vende, a música dá clima.** A música alegre fica por baixo o tempo todo, bem abaixo da voz,
   e o volume nunca muda.
7. **CTA visual + falado juntos.** O botão aparece uma fração de segundo antes da voz dizer "clique no
   botão". O verde e o ícone do WhatsApp com badge "1" passam a ideia de "tem mensagem esperando".
8. **Cauda só com música.** Sem voz, sobra espaço para decidir, e o b-roll apetitoso continua
   alimentando o desejo com o botão na tela.

## Estrutura da copy (as duas referências seguem a mesma) → o que mostrar em cada bloco

| Bloco | Salsas | Gelato | B-roll |
|---|---|---|---|
| 1. Gancho-pergunta com o produto + dinheiro/valor | "estos frasquitos… 20 mil pesos" | "aquele gelato… custa uma fortuna" | **o objeto citado** (`gancho`) |
| 2. Prova com números / facilidade | "tercer día… 30 al día" | "3 ingredientes… 15 reais… pote de 1 litro" | produção/ingredientes **citados** |
| 3. Ponte / história / autoridade | "remodelé mi cocina…" | "Luciana… Itália… Bologna" | variedade bonita, ritmo calmo |
| 4. Objeção + mecanismo | "no es suerte, es técnica" | "técnica dos italianos" | processo e textura |
| 5. Pilha de conteúdo nomeada | "100 recetas: árbol, habanero…" / "Y no solo eso…" | "130 receitas: pistache, chocolate…" | **cada variedade citada** |
| 6. Ganho / família / preço | "primeros 3 mil pesos… 100 pesos" | "marido… filhos raspam o pote" | produto pronto/pessoas |
| 7. Reversão de risco | "te mando primero a tu WhatsApp" | "mando no WhatsApp antes de pagar" | **rajada** de cortes |
| 8. CTA + empurrão | "dale clic al botón… tu oportunidad" | "Clica no botão… vem comigo" | CTA na tela, 1 plano de produto |

## Regras de edição (números medidos)

### Formato
- 1080x1920, 30 fps, H.264 + AAC. B-roll em tela cheia (`object-fit: cover`), sem bordas nem barras pretas.
- Duração = fim da voz + cauda. Nos 30: salsas 70–130 s, gelato 44–110 s. Quem define é a copy.

### Cortes
- **Máximo 2,0 s por cena** (regra do dono). Mediana alvo ~1,35 s.
  - As salsas têm várias cenas de 3–6 s (ações contínuas: liquidificador, tomates, panela) e o último
    plano de 12,8 s sob o CTA. Isso é exceção observada, não regra. Só use se o dono pedir.
- **Corte seco** é o padrão.
  - **Exceção rara** (só nas salsas): 1 flash branco de 0,2 s numa virada de bloco ("Y no solo eso") e
    1 transição zoom+fade. No máximo 1–2 por vídeo e só nas viradas de bloco (`flash_em` no spec).
  - O flash entra 0,3 s antes da frase da virada e **o corte de cena fica escondido no pico do flash**.
- **Gancho (0 → ~5 s)**: 5–6 cortes **do(s) clipe(s) do objeto do hook**, em trechos diferentes, acelerando
  até um flash.
  - Gelato: 1,43 · 1,13 · 0,83 · 0,67 · 0,27 · 1,13.
  - Salsas: 1,43 · 1,90 · 0,27 · 0,37 · 0,63.
- Flashes de 0,13–0,33 s de vez em quando (outro trecho ou ângulo de algo já visto).
- Rajadas de 3–7 cortes rápidos a cada ~20–25 s e na reversão de risco; entre elas, cenas de 1,5–2,0 s.
- Nunca o mesmo b-roll em duas cenas seguidas, exceto dentro do gancho.
- **Nunca repetir o mesmo trecho de um b-roll** (feedback do dono no teste de salsas: "tá repetindo os mesmos
  b-rolls nas mesmas partes do começo ao fim").
  - Um arquivo só volta num trecho que ainda não apareceu, sem sobreposição, e a ≥ 15 s do uso anterior.
  - Se o banco não dá conta, a solução é **mais b-roll**, nunca repetir. O banco precisa ter **≥ 1,3× a
    duração do vídeo** em material (85 s de vídeo → ≥ 110 s; ideal 15–25 clipes de 5–20 s, com várias
    variações do produto).
  - O montador faz isso sozinho e avisa "b-roll insuficiente" com os trechos repetidos. Nesse caso, peça ou
    busque mais b-roll antes de renderizar a versão oficial.

### B-roll
| Categoria | Prefixo do arquivo | Onde entra |
|---|---|---|
| **Objeto do hook** | `gancho_*` (ou `"gancho"` no spec) | 0 → ~5 s, obrigatório |
| Produto final / money shot | `final_*` | voltas ao longo do vídeo, cauda |
| Processo / ingredientes | `processo_*` | depois do gancho, blocos de "como faz" |
| Textura / ASMR (calda, colher, macro) | `textura_*` | corpo e rajadas |
| Pessoa com o produto (sem falar p/ câmera) | `reacao_*` | a cada ~20 s |
| Sem prefixo | qualquer | coringa |

- Clipes verticais de TikTok com **mão/utensílio em movimento**, luz quente, cozinha bonita.
- Evite: rosto falando para a câmera, barras pretas, texto/sticker/logo de outro criador queimado na
  imagem. As salsas tinham alguns e funcionaram, mas não procure isso.

### Voz (sempre enviada pelo dono)
- Feminina, gerada no MiniMax/ElevenLabs. **O dono manda a voz pronta em todo criativo** (a mesma voz
  para todos os criativos de um produto). Nunca gere nem troque a voz por conta própria.
- Entra em ~0,2 s e fala sem parar até o fim do CTA. Pausas entre frases de 0,25–0,45 s (vêm da própria voz).
- Nível −16 LUFS. **Nunca corte o fim da voz**: o script só tira silêncio do começo e acrescenta 0,25 s
  de respiro no final.

### Música (sempre enviada pelo dono)
- Alegre, coerente com o produto. **Uma música por produto**: 15/15 salsas a 105 BPM e 15/15 gelato a
  110 BPM. O dono manda o arquivo.
- **Toca desde o 0:00 do vídeo até o último frame** (batida presente no início em **30/30** criativos), sem
  fade-in e sem fade-out.
- **Volume constante do começo ao fim** (0–20 s ≈ sob a voz ≈ cauda), sem ducking e sem subir na cauda.
- "Iniciando no 00:00:22" = a faixa começa no ponto 0:22 da música (`musica_offset: 22`, padrão).
  - Se o dono disser outro ponto, mude só o `musica_offset`.
  - Ela nunca entra só no segundo 22 do vídeo: os 30 têm música desde o início.

### Perfil de mixagem por produto (medido nos 30)
| Produto | Música abaixo da voz (`musica_lu`) | Cauda só música (`cauda`) |
|---|---|---|
| Salsas (MX) | **17,5** (16,9–21,1) | **6,3 s** (3,4–6,4) |
| Gelato (BR) | **14,8** (13,9–15,4) | **10,8 s** (6,4–11,1) |
| Produto novo | 16 (meio-termo) | 9 s. Depois de definir, use o mesmo em todos os criativos do produto. |

A voz sai sempre em −16 LUFS na montagem. A música fica em −16 − `musica_lu`.

### Texto na tela
- **Zero legenda durante a narração.** O único texto é o CTA.
- **Quando entra**: **junto da frase do CTA** ("Clique no botão" / "dale clic al botón"), de 0 a 0,6 s
  antes dela. Nos 30: salsas −0,15…+0,38 s; gelato ~0,1–0,7 s. O script acha a frase na transcrição e
  põe o CTA 0,2 s antes. Fica até o fim.
- **Texto**: pt "Clique no / botão abaixo"; es "Haz clic en / el botón de abajo".
  - **Fonte: a "Sistema" do CapCut** (pedido do dono, a do texto padrão "Texto padrão" do CapCut).
    - Comparada lado a lado, a mais parecida é a **Montserrat SemiBold** (mesmo "a" de dois andares, "o"
      redondo, "t" com corte inclinado), por isso é ela que o montador usa (`assets/fonts`).
    - Poppins NÃO serve (o "a" é diferente).
    - Se o dono mandar o arquivo da fonte do CapCut, troque o `@font-face`.
  - ~108 px, branco com contorno preto grosso, cada linha sobre faixa verde `#009b01` com bordas de pincel.
  - Bloco em y ≈ 580–915 (as duas referências variam nessa faixa).
- **Ícone**: balão verde sólido do WhatsApp com contorno branco de sticker, telefone branco e badge
  vermelho "1" com borda branca. ~380 px, centro em (540, ~1240). Arquivo `assets/whatsapp_badge.svg`.
- **Entrada**:
  - `pop` (gelato): grupo cresce de 0 → 100% em 0,33 s.
  - `digitar` (salsas): texto aparece letra a letra e o ícone em fade, ~0,5 s.

### Cauda
- Só música + CTA + b-roll depois que a voz acaba. A duração é **fixa por produto** (tabela acima): salsas
  6,3 s, gelato 10,8 s.

## Fluxo de trabalho

1. **Setup** (toda sessão nova): `bash scripts/setup.sh` na raiz do repo. Instala o Chrome do render, o
   transcritor (Whisper local) e o separador voz/música. Tudo que o HTML usa fica local: CDNs são
   bloqueados neste ambiente.
2. **Material do dono**: voz (mp3/wav), música, copy (texto) e b-rolls (ou pedido para buscar no TikTok).
   Falta voz ou música → peça. Nunca invente.
3. **Leia a copy e planeje a congruência**:
   - Qual é o objeto do hook? Separe 1–2 b-rolls que mostram exatamente ele.
   - Liste os substantivos concretos da copy e o b-roll de cada um (`sincronia`).
   - Marque a virada "e não só isso / y no solo eso / bônus" se quiser o flash (`flash_em`, opcional).
4. **Classifique os b-rolls**: folha de contato de cada um
   (`ffmpeg -i x.mp4 -vf "fps=1,scale=180:-1,tile=6x2" x.png`) e prefixos de categoria. Descarte talking
   head, barra preta e texto grande queimado.
5. **Spec** (`spec.json` ao lado do material):
   ```json
   {
     "nome": "salsas_ad13",
     "idioma": "es",
     "voz": "voz.mp3",
     "musica": "musica.mp3",
     "musica_offset": 22,
     "musica_lu": 17.5,
     "broll_dir": "broll",
     "gancho": ["gancho_frascos.mp4"],
     "sincronia": [
       {"fala": "mermeladas de chile", "broll": "textura_mermelada.mp4"},
       {"fala": "habanero", "broll": "textura_habanero.mp4"}
     ],
     "cta_entrada": "digitar",
     "cauda": 6.3
   }
   ```
   Opcionais:
   - `musica_inicio` (padrão 0).
   - `cta_linhas`.
   - `cta_tempo`: força o momento do CTA.
   - `flash_em`: lista de frases.
   - `apertar_pausas`: só se a voz vier arrastada.
   - `clips`: EDL manual `[{"src","in","dur"}]`.
   - `seed`.
6. **Monte**: `python3 .claude/skills/criativo-broll/scripts/montar_criativo.py spec.json`. O relatório
   precisa mostrar:
   - máx ≤ 2,00 s;
   - 0 b-roll repetido em sequência;
   - âncoras de sincronia N/N;
   - CTA visual logo antes da frase do CTA;
   - a primeira frase transcrita batendo com o clipe do gancho.
7. **Revise o `edl.json`** (cena a cena: início, duração, arquivo, trecho, motivo). Ajuste âncoras ou
   `seed` se precisar.
8. **Renderize** em segundo plano: `npx hyperframes render -o saida.mp4` na pasta do projeto (~4–5x a
   duração do vídeo).
9. **Confira o MP4 antes de entregar** (obrigatório, o dono cobra qualidade nas versões oficiais).
   Para conferir sem renderizar tudo de novo, use
   `npx hyperframes snapshot --at 74.6,75,76 --no-end` na pasta do projeto (gera PNG dos instantes pedidos).
   - `scripts/analisar_referencia.sh saida.mp4`: cenas ≤ 2 s, voz inteira até o fim (sem corte no meio
     de palavra), cauda só música.
   - Folha de contato e quadro do CTA: ícone reto e inteiro, texto legível, nada fora da tela.
   - Ouça o fim: a última palavra da voz precisa estar completa.
10. **Entregue** com `SendUserFile` (comprima com `-crf 23` se passar de 30 MB) + resumo de 3–5 linhas.


### Recursos do spec usados no 1º criativo real (ad16 finger foods)
- `gancho_ate`: frase da aterrissagem. O gancho é reescalado para terminar exatamente nela, e a aterrissagem
  mostra o produto pronto. Pedido do dono no ad16: hook = receita no meio do preparo, aterrissagem = petiscos
  prontos.
- `gancho_ins`: entradas fixas do clipe do gancho, em ordem, para a receita avançar.
- `"in"` em cada âncora de `sincronia`: escolhe o trecho exato que mostra a palavra.
- `evitar`: `{"clipe.mp4": [[ini, fim], ...]}`, trechos proibidos (rosto falando, embalagem com marca,
  trecho fraco).
- Gancho e aterrissagem da mesma receita: corte um b-roll em dois (processo → `gancho_*`, produto pronto →
  `final_*`) e tire o original do banco para não repetir trecho.
- Música mais curta que o vídeo a partir do 0:22: monte a trilha antes (0:22→fim + 0:22→… com acrossfade
  de 0,12 s no beat) e passe `musica_offset: 0`.
- Antes de renderizar, gere uma grade com o quadro do meio de cada corte do `edl.json` e procure rosto,
  texto ou embalagem.
- Se o render falhar com "Chrome cannot start" (timeout), é transitório: rode de novo.
- Entrega: o render `-q delivery` sai com ~170 MB. Para enviar no chat, faça 2 passadas a 2500k (~28 MB).

## Analisando novas referências
- Um vídeo: `scripts/analisar_referencia.sh video.mp4 pasta/` (cortes, folhas de contato, espectrograma,
  níveis, BPM, fim da voz) + `python3 scripts/transcrever.py video.mp4 pt|es` (fala com tempo, para a
  tabela fala × tela).
- **Lote**: `python3 scripts/analisar_lote.py lista.tsv saida/` (ou uma pasta de mp4).
  - Mede por vídeo: cortes e % acima de 2 s, gancho falado + folha dos 6 primeiros s, CTA visual × frase
    do CTA, cauda, voz × música (LU) e se a batida toca desde o início.
  - Fecha com a mediana do lote. Rode com `bash scripts/setup.sh --tudo` antes (spleeter para os níveis).
  - Os 30 criativos do Drive (15 salsas MX + 15 gelato BR) estão listados em
    `references/drive_criativos.tsv` e **já foram analisados** (`references/lote-drive-30.md`). O
    download direto usa `drive.usercontent.google.com` (arquivos públicos). O conector do Drive só serve
    para listar, porque baixa no máximo 10 MB.
- Separar voz e música à mão:
  `MODEL_PATH=/opt/ml/pretrained_models /opt/ml/sp/bin/spleeter separate -p spleeter:2stems -o saida/ video.wav`.
- Padrão novo e consistente em 2+ criativos → **adicione aqui e em `references/`** com o número medido e
  o porquê. Esta skill é a memória do método.

## Pendências
- Busca de b-roll no TikTok: skill futura.
- Se o dono mandar o arquivo da fonte "Sistema" do CapCut, troque a Montserrat no `@font-face`.

### Ajustes do dono no ad16 (v2) — valem para os próximos
- Bebida (cerveja) só nos momentos estratégicos em que a voz fala dela; nunca como enchimento. No spec: `evitar`
  cobrindo o resto do clipe de bebida (ex.: `[[0, in-0.1], [in+dur, 999]]`).
- Na aterrissagem do gancho ("…por causa desses petiscos aqui"), usar a mesa/porção mais farta e apetitosa
  (ex.: `gancho_porcao_boteco`), não um close de um petisco só.
- B-roll vetado pelo dono → `evitar: {clip: [[0, 999]]}` no spec do produto.
- **Música começando "no segundo 00:01" = 1 s depois do início do criativo** (o 1º segundo é só voz, sem música),
  NÃO o ponto da faixa. No spec: `"musica_inicio": 1.0`; a faixa continua a partir do 0:22 (`musica_offset`).
  Padrão do produto finger foods a partir do ad17. Faixa curta → emendar no ponto de loop casado na batida
  (`atrim` + `acrossfade=d=0.12`; finger foods: `musica_bed.wav` = 22.15→80.81 + 22.15→).
- Quando o dono falar um tempo ("no segundo X"), é tempo do criativo/narração, salvo se ele disser "da música".

### ad17/ad18 (finger foods) — recursos e padrões novos
- `"depois": <s>` numa âncora de `sincronia`: procura a frase só depois desse tempo (frase repetida na copy,
  ex.: "mini hamburguer" no meio e na lista de receitas).
- Use a grafia que o Whisper escreveu (ex.: "pateis", "quichis", "mini hambulguer"). Se o relatório avisar
  "âncora ignorada", confira `transcricao.tsv` e troque a frase.
- Hook "petisco de bar" (ad17): alternar 2–3 b-rolls de porção/mesa de boteco no gancho (`gancho` com vários
  clipes + `gancho_ins`). Hook "fazendo a receita" (ad18): uma receita de boteco do início ao fim no gancho
  (bolinha de queijo: mistura → farinha → massa → recheio → corte → bolear → empanar), aterrissando na porção pronta.
- Trechos proibidos de todo o banco finger foods ficam acumulados em `projetos/finger-foods/ad1x_spec.json`
  (`evitar`): copie o `evitar` do último spec ao começar o próximo criativo.

### Variedade entre ads (pedido do dono: "tá repetindo muito b-roll nos ads")
- Spec `"outros_ads": ["edl_adX.json", ...]`: o montador prefere, na mesma categoria, o clipe que menos apareceu
  nos ads anteriores do produto, e prefere clipe ainda não usado no próprio ad antes de voltar a um já usado.
- Ao começar um ad novo: copie os `edl.json` dos ads anteriores para a pasta e liste em `outros_ads`; copie
  `projetos/<produto>/evitar_banco.json` para o `evitar`; varie também as âncoras (não use sempre o mesmo clipe
  para a mesma palavra em todos os ads).
- Clipe de contexto específico (ex.: café/latte só em copy de empresa/coffee break) → `evitar` inteiro nos outros ads.
- Banco finger foods: pasta única `banco_ff/` (136 clipes) montada a partir de `banco.tsv`.
- Antes de renderizar, cruze o `edl.json` com o `rostos.json` do banco (nenhuma cena pode cair num trecho com
  rosto) e olhe a grade: quadro branco/vazio, máquina industrial, close desfocado → `evitar` e monte de novo.
- CTA falado sem "botão" (ex.: "Me chama no WhatsApp agora"): a lista de frases inclui "me chama no whatsapp";
  se o Whisper errar a frase, use `cta_tempo` (início da frase − 0,2 s).
- Disco da sessão: cada projeto copia o b-roll para `assets/broll` (~1 GB) e o HyperFrames guarda histórico de
  render em `~/.cache/hyperframes/history` (~2 GB por render). Depois de entregar, apague `assets/broll` dos
  projetos prontos, o render bruto (`full.mp4`) e as pastas antigas do histórico.
- O montador recopia um clipe para `assets/broll` quando o arquivo do banco mudou (recorte, regravação).

### Rostos no b-roll (ad24, finger foods)
- O detector usado para montar `rostos_banco.json` perdeu rosto pequeno/de lado no topo do quadro
  (`processo_canape_confeitado` 0–7 s, `processo_minihamburguer_montagem` 0,4–2,9 s). O YuNet do OpenCV pega esses,
  mas dá muito falso positivo em comida (score até 0,85). Fluxo: rode o YuNet só nos trechos usados pelos `edl.json`,
  faça uma folha com a caixa desenhada e confirme no olho; rosto confirmado → `rostos_banco.json` + `evitar_banco.json`.
- `projetos/finger-foods/rostos_banco.json` é a lista curada (só trechos com rosto confirmado).
- Olhe o gancho (primeiros 6 s) em tamanho grande, não só na grade: rosto pequeno some na miniatura.

### Regras do dono a partir do ad27 (finger foods)
- **CTA na tela só no CTA FINAL.** Copy com mais de uma chamada ("Eu te mando no WhatsApp…" / "Clique aqui abaixo…"
  no meio e "Clica no botão…" no fim): o "Clique no botão abaixo" + ícone entra só na última frase de CTA. O montador
  já faz isso (última ocorrência de qualquer frase de `FRASES_CTA`). Ads antigos não foram corrigidos (pedido do dono).
- **Varie os b-rolls entre ads.** Ao montar um ad novo, bloqueie no `evitar` todos os trechos (±0,3 s) já usados nos
  `edl.json` dos ads anteriores do produto; só gancho e âncoras escolhidas de propósito podem repetir trecho.
  Resultado nos ads 27–30: de ~35 % para ~5–15 % de trechos repetidos. Escolha ganchos e âncoras entre os clipes
  menos usados (conte os usos nos `edl.json` antes).
- Trechos com pote/garrafa de marca, taça de vinho ao fundo, quadro branco/borrado → `evitar_banco.json`.
