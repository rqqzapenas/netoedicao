# Anatomia do criativo de referência — "gelato"

Arquivo analisado: `gelato.mp4`. 1080x1920, 30 fps, H.264 + AAC 44,1 kHz estéreo, **82,5 s**, 54 cenas.
Medições feitas com `scripts/analisar_referencia.sh` (corte por `scene>0.22`, loudness EBU R128, espectrograma).

## Linha do tempo macro

| Tempo | O que acontece | Áudio |
|---|---|---|
| 0,00 | Primeiro frame já é o produto final sendo servido (bola de gelato saindo na boleadora) | voz entra em **~0,25 s** |
| 0 → 5,5 | **Gancho visual**: 6 cenas, só produto pronto/apetitoso, média 0,9 s, com um flash de 0,27 s | só voz |
| 5,5 → 12,6 | **Processo**: açúcar caindo, ovo quebrando, gema caindo (flash 0,17 s), creme na máquina, espátula, pistache por cima | só voz |
| 12,6 → 21,3 | **Variedade de sabores** (caramelo, oreo): textura, calda escorrendo, bola caindo na taça, cenas mais longas (1,7–1,9 s) | só voz |
| **~22,0** | **Música entra, corte seco**, sem fade, logo depois de uma pausa da voz (21,3–21,9) | voz + música |
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

## Áudio

- **Voz**: feminina, IA (MiniMax/ElevenLabs), contínua de 0,25 s a 71,4 s. Pausas entre frases bem apertadas (0,15–0,25 s), sem ar morto.
- **Música**: alegre, ~110 BPM, entra **seca em ~22,0 s** e vai até o último frame, também sem fade-out.
- Níveis: voz sozinha −27,8 LUFS; voz+música −27,4 LUFS; **música sozinha −38,9 LUFS** → a música fica **~11 LU abaixo da voz** e mantém o mesmo nível na cauda (não sobe quando a voz acaba e não tem ducking).
- O master inteiro está em −27,7 LUFS (baixo). Na montagem normalizamos a voz em −16 LUFS e a música em −27 LUFS, mantendo a diferença de 11 LU.

## Texto na tela

- **Nenhuma legenda durante a narração.** O único texto do vídeo é o CTA final.
- Entra em 67,4 s (~4 s antes da voz acabar) e fica até o fim (~15 s).
- Animação: o grupo texto+ícone cresce de 0 a 100% em ~10 frames (0,33 s), a partir do centro, sem bounce.
- Texto: "Clique no / botão abaixo", 2 linhas centralizadas, sans geométrica (Montserrat SemiBold), ~104 px, branco com contorno preto grosso, cada linha sobre uma **faixa verde (#009407) com bordas irregulares de pincel**. Bloco ocupa y ≈ 585–830 (30–43% da altura).
- Ícone: balão verde de WhatsApp com telefone branco, contorno branco de sticker e badge vermelho "1"; ~370 px, centro em x = 540, y ≈ 1240 (65%).
- Tudo acima da zona da UI do TikTok/Reels (rodapé e lateral direita livres).
