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
- Duração = fim da voz + cauda (as referências têm 82,5 s e 87 s).

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
- Alegre, coerente com o produto, ~100–115 BPM (gelato 110, salsas 105). **O dono manda a música** (a
  mesma por produto).
- **Toca por baixo desde o início do vídeo** até o último frame, sem fade-in e sem fade-out.
- **"Iniciando no 00:00:22" = começar a faixa no ponto 0:22 da música** (`musica_offset: 22`).
  - Medido: nas duas referências a batida já existe no segundo 1, no mesmo andamento e no mesmo nível da
    cauda.
  - Pendente de confirmação do dono. Se ele disser que a música só deve entrar no segundo 22 do vídeo,
    use `musica_inicio: 22, musica_offset: 0`.
- Nível constante **12–18 LU abaixo da voz** (montagem: −30 LUFS), sem ducking, sem subir na cauda.

### Texto na tela
- **Zero legenda durante a narração.** O único texto é o CTA.
- **Quando entra**: 0,4–0,6 s **antes** da voz falar a frase do CTA ("Clique no botão" / "dale clic al
  botón"). O script acha a frase na transcrição. Fica até o fim (13–15 s na tela).
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
- Só música + CTA + b-roll por **6–11 s** depois que a voz acaba (salsas 6,4 s; gelato 11 s). Padrão: 9 s.

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
     "broll_dir": "broll",
     "gancho": ["gancho_frascos.mp4"],
     "sincronia": [
       {"fala": "mermeladas de chile", "broll": "textura_mermelada.mp4"},
       {"fala": "habanero", "broll": "textura_habanero.mp4"}
     ],
     "cta_entrada": "digitar",
     "cauda": 9
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

## Analisando novas referências
- Um vídeo: `scripts/analisar_referencia.sh video.mp4 pasta/` (cortes, folhas de contato, espectrograma,
  níveis, BPM, fim da voz) + `python3 scripts/transcrever.py video.mp4 pt|es` (fala com tempo, para a
  tabela fala × tela).
- **Lote**: `python3 scripts/analisar_lote.py lista.tsv saida/` (ou uma pasta de mp4).
  - Mede por vídeo: cortes e % acima de 2 s, gancho falado + folha dos 6 primeiros s, CTA visual × frase
    do CTA, cauda, voz × música (LU) e se a batida toca desde o início.
  - Fecha com a mediana do lote. Rode com `bash scripts/setup.sh --tudo` antes (spleeter para os níveis).
  - Os 30 criativos do Drive (15 salsas MX + 15 gelato BR) estão listados em
    `references/drive_criativos.tsv`. Baixar exige o domínio `drive.usercontent.google.com` liberado na
    rede do ambiente (os arquivos são públicos). O conector do Drive só baixa até 10 MB.
- Separar voz e música à mão:
  `MODEL_PATH=/opt/ml/pretrained_models /opt/ml/sp/bin/spleeter separate -p spleeter:2stems -o saida/ video.wav`.
- Padrão novo e consistente em 2+ criativos → **adicione aqui e em `references/`** com o número medido e
  o porquê. Esta skill é a memória do método.

## Pendências
- **Lote do Drive** (30 criativos): pronto para rodar assim que `drive.usercontent.google.com` estiver
  liberado. Depois, consolide a mediana do lote nesta skill, principalmente % de cenas > 2 s, cauda e
  antecedência do CTA. Até agora (2 referências): cauda 6,4–11 s, CTA 0,38–0,41 s antes da fala, música
  14–17,5 LU abaixo da voz e batida presente desde o início.
- **Projeto do CapCut** `ad2_gelatos`: precisa do controle do computador (Claude desktop com "Uso do
  computador" ligado e o computador escolhido em Dispositivos) ou do zip da pasta.
  - Ler `draft_info.json`: `tracks` → segmentos com `target_timerange`/`source_timerange` em µs,
    `materials.videos/audios`, volumes, velocidade, fontes de texto.
  - Confirma o ponto de início da música, os volumes exatos e a fonte "Sistema".
- Confirmar com o dono o significado de "música iniciando no 00:00:22" (ver Música).
- Busca de b-roll no TikTok: skill futura.
