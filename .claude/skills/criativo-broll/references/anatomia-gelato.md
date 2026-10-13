# Anatomia do criativo de referência — "gelato"

Arquivo analisado: `gelato.mp4`. 1080x1920, 30 fps, H.264 + AAC 44,1 kHz estéreo, **82,5 s**, 54 cenas.
Medições feitas com `scripts/analisar_referencia.sh` (corte por `scene>0.22`, loudness EBU R128, espectrograma).

## Linha do tempo macro

| Tempo | O que acontece | Áudio |
|---|---|---|
| 0,00 | Primeiro frame já é o produto final sendo servido (bola de gelato saindo na boleadora) — exatamente o que a 1ª frase fala ("aquele gelato… que custa uma fortuna") | voz entra em **~0,25 s**, música baixa por baixo |
| 0 → 5,5 | **Gancho visual**: 6 cenas, só produto pronto/apetitoso, média 0,9 s, com um flash de 0,27 s | voz + música baixa |
| 5,5 → 12,6 | **Processo**: açúcar caindo, ovo quebrando, gema caindo (flash 0,17 s), creme na máquina, espátula, pistache por cima | voz + música baixa |
| 12,6 → 21,3 | **Variedade de sabores** (caramelo, oreo): textura, calda escorrendo, bola caindo na taça, cenas mais longas (1,7–1,9 s) | voz + música baixa |
| **~22,0** | A música fica mais cheia (mudança de seção da própria faixa) logo depois de uma pausa da voz (21,3–21,9) | voz + música |
| 21,3 → 25,3 | Volta o b-roll da abertura (mesmo arquivo, **outro trecho**) | |
| 25,3 → 27,5 | **Reação humana** (mulher animada com casquinha, sem falar para a câmera) | |
| 27,5 → 45,9 | Blocos de sabor: chocolate (raspas, fouet), frutas vermelhas (calda), stracciatella (macro de colher) — rajadas de 0,6–0,7 s alternando com 1,5–2,0 s | |
| 45,9 → 50,8 | **Segunda reação humana** (outra mulher, casquinha, colher) | |
| 50,8 → 56,8 | Volta o b-roll do oreo (outro trecho) | |
| 56,8 → 60,8 | **Rajada**: 5 cortes de 0,7–0,9 s no mesmo sabor | |
| 60,8 → 67,4 | Casquinha na sorveteria, doce de leite em espiral, bandeja | |
| **67,4** | **CTA visual pop**: "Clique no botão abaixo" + ícone do WhatsApp com badge "1" | voz falando o fechamento |
| **71,4** | **Voz termina** | |
| 71,4 → 82,5 | **Cauda de ~11 s só com música**, b-roll seguindo (cenas 1,6–3 s), CTA fixo na tela | música sozinha, mesmo volume |
| 82,5 | Fim seco (música corta, sem fade-out) | |

## Cortes

- Média 1,53 s, **mediana 1,35 s**. 49 de 54 cenas ≤ 2,2 s.
- Gancho (0–5 s): 1,43 · 1,13 · 0,83 · 0,67 · **0,27** · 1,13 — acelera e "pisca" antes de entrar no processo.
- Flashes (≤ 0,33 s) em 4,07 · 7,60 · 41,00 · 43,47: dão um "soco" de energia; sempre um ângulo/trecho diferente de algo já visto.
- Ondas de energia: rápido (0–5) → médio (5–12) → calmo (12–28) → rajada (31–37) → calmo → rajada (56–61) → cauda calma.
- **Só corte seco.** Nenhuma transição, zoom, fade ou efeito; o b-roll já tem movimento próprio (mão, colher, calda).
- Na referência há 4 planos acima de 2 s (3,0 · 4,27 · 6,8 no CTA). **A regra do dono é no máximo 2 s** — a skill divide esses planos em dois trechos.

## Tipos de b-roll (todos verticais, nativos de TikTok, com mão/utensílio em ação)

1. **Final/"money shot"** — bola sendo servida, casquinha cheia erguida para a câmera, bola caindo na taça.
2. **Processo** — ingredientes simples (açúcar, ovo, leite), máquina, espátula, finalização com topping. Mostra que é fácil e caseiro.
3. **Textura/ASMR** — calda escorrendo da colher, boleadora raspando, macro do creme, espiral de doce de leite. Prende o olho.
4. **Reação humana** — pessoa feliz segurando/provando o produto, sem falar para a câmera. Uma a cada ~20 s.
5. **Variedade** — cada bloco de 5–15 s é um sabor diferente → transmite "você vai aprender MUITAS receitas".

Ambiente: cozinhas claras, luz quente, bancada de mármore/madeira/granito, flores e limões de enfeite → aspiracional, mas caseiro.
Qualidade mista é aceitável (os últimos 15 s são visivelmente comprimidos/repostados) — o que importa é o conteúdo apetitoso.

## Reaproveitamento do mesmo b-roll

| B-roll | 1º uso | 2º uso |
|---|---|---|
| Boleadora na tigela + casquinha (cozinha dourada) | 0,0–2,6 | 21,3–25,3 |
| Pote de pistache | 2,6–3,4 | 3,4–4,3 (outro ângulo/trecho) e 10,5–12,6 |
| Forma de oreo | 17,6–21,3 | 50,8–56,8 |
| Frutas vermelhas | 36,7–41,0 | 66,4–73,2 |

Regra observada: o 2º uso usa **outra parte** do arquivo e fica a **15–30 s de distância** do 1º; nunca em sequência.

## Áudio (remedido com voz e música separadas — spleeter)

- **Voz**: feminina, IA (MiniMax/ElevenLabs), contínua de 0,25 s a 71,5 s. Pausas entre frases 0,25–0,45 s.
- **Música**: alegre, **110 BPM**, **presente desde o segundo 1** (a batida de 110 BPM já aparece em 1–21 s com
  periodicidade 0,78, mesmo andamento da cauda). O nível da música separada é praticamente o mesmo antes e
  depois de 22 s (−42,8 × −41,9 LUFS). O "salto" em ~22 s é a própria faixa ficando mais cheia.
  → Interpretação provável de "música iniciando no 00:00:22": a faixa entra no início do vídeo **a partir do
  ponto 0:22 da música** (pulando a introdução). Confirmar com o dono.
- Níveis: voz −28 LUFS; música por baixo −42 LUFS (**~14 LU abaixo da voz**); cauda só música −39 LUFS
  (praticamente o mesmo nível — não sobe quando a voz acaba, sem ducking). Fim seco, sem fade-out.
- O master inteiro está em −27,7 LUFS (baixo). Na montagem: voz −16 LUFS, música −30 LUFS.

## Fala × tela (transcrição com tempo)

| Fala | Texto | Tela |
|---|---|---|
| 0,25–7,14 | Sabe aquele **gelato** de casquinha que custa uma fortuna? Eu faço igualzinho em casa com **3 ingredientes** e sem precisar de máquina. | 0–5,5 gelato sendo servido/casquinha (gancho) → 5,5–7,8 **açúcar, ovos, leite** (os ingredientes) |
| 7,45–11,53 | E o melhor, gastando menos de 15 reais em cada **pote de 1 litro**. | 7,8–12,6 creme na máquina → passando para o **pote** |
| 11,99–21,41 | Meu nome é Luciana. Morei 10 anos na Itália, trabalhei numa gelateria em Florença e aprendi o verdadeiro gelato com uma senhora de 80 anos em Bologna. | pote, caramelo, oreo (variedade, ritmo calmo para a história) |
| 22,17–24,61 | Sempre ia anotando tudinho que ela me ensinava. | volta o b-roll da abertura |
| 25,30–35,65 | Quando voltei para o Brasil vi que já tinha mais de **130 receitas**: pistache, **chocolate**, flocos, morango, amendoim e até zero açúcar. | 25,3 mulher feliz com casquinha → 27,5–36,7 **chocolate** (raspas, fouet, bola) |
| 36,15–40,61 | Gelato feito com a técnica dos italianos tem outra textura, outro sabor. | frutas vermelhas, macro de **textura** |
| 40,95–44,55 | Sai do freezer e a casa toda já está esperando com a colher na mão. | macro de **colher** no stracciatella |
| 44,79–46,98 | Marido não compra mais pote no mercado. | 45,9 mulher com casquinha (reação) |
| 47,45–51,27 | Filhos brigam pra ver quem **raspa o pote**… | colher raspando a casquinha, oreo sendo raspado |
| 51,64–55,69 | Não precisa ser chef, não precisa de ingrediente caro, precisa só aprender o jeito certo. | oreo na taça |
| 56,34–63,33 | Se você quer aprender… eu mando o conteúdo completo no seu WhatsApp, antes de você pagar qualquer coisa. | **rajada** 56,8–60,8 (5 cortes de 0,7–0,9) |
| 63,64–67,59 | Você recebe, abre, faz uma receita no fim de semana e depois me conta como foi. | casquinha na sorveteria, doce de leite |
| **67,43** | — | **CTA visual entra** (0,56 s antes da frase do CTA) |
| 67,99–71,53 | Clica no botão aqui embaixo e vem comigo que eu te explico direitinho. | frutas vermelhas, CTA |
| 71,5–82,5 | — (11 s só música) | b-roll segue, CTA fixo |

## Texto na tela

- **Nenhuma legenda durante a narração.** O único texto do vídeo é o CTA final.
- Entra em 67,4 s, **0,56 s antes** da voz falar "Clica no botão aqui embaixo" (67,99 s), e fica até o fim (~15 s).
- Animação: o grupo texto+ícone cresce de 0 a 100% em ~10 frames (0,33 s), a partir do centro, sem bounce.
- Texto: "Clique no / botão abaixo", 2 linhas centralizadas, sans geométrica (Montserrat SemiBold), ~104 px, branco com contorno preto grosso, cada linha sobre uma **faixa verde (#009407) com bordas irregulares de pincel**. Bloco ocupa y ≈ 585–830 (30–43% da altura).
- Ícone: balão verde de WhatsApp com telefone branco, contorno branco de sticker e badge vermelho "1"; ~370 px, centro em x = 540, y ≈ 1240 (65%).
- Tudo acima da zona da UI do TikTok/Reels (rodapé e lateral direita livres).
