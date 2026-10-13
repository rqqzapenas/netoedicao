# Lote completo — 30 criativos do Drive (15 salsas MX + 15 gelato BR)

Medido com `scripts/analisar_lote.py`: cortes, transcrição, CTA visual × falado, voz × música separadas com
spleeter. Tabela por vídeo: `lote_drive_30_medidas.tsv`. Todos os 30 foram baixados e analisados, sem erro.

## Padrão medido (mediana e faixa)

| Medida | Salsas (MX, es) | Gelato (BR, pt) | O que vira regra |
|---|---|---|---|
| Duração | 99 s (70–130) | 74 s (44–110) | Duração = tamanho da copy. Não existe alvo fixo. |
| Nº de cenas | 56 (33–82) | 54 (28–85) | — |
| Mediana da cena | 1,28 s (0,68–2,70) | 1,13 s (0,87–1,37) | Alvo ~1,1–1,3 s |
| Cenas > 2 s | 30% (21–73%) | 16% (8–31%) | Regra do dono: ≤ 2 s (as referências passam disso às vezes) |
| Maior cena | 6,3 s (3,5–12,8) | 4,3 s (2,8–12,5) | Planos longos quase sempre no CTA/final |
| Voz começa | 0,12 s (0,06–0,41) | 0,15 s (0,12–0,25) | Voz no primeiro frame |
| Cauda só música | **6,3 s** (3,4–6,4) | **10,8 s** (6,4–11,1) | **Fixa por produto** |
| CTA visual × frase do CTA | −0,03 s (−0,15…+0,38) | +0,69 s (−0,11…+5,0)* | CTA entra junto da frase (0–0,6 s antes) |
| Voz | −16,2 LUFS | −27,1 LUFS | Export diferente por produto. Montagem: −16 |
| Música abaixo da voz | **17,6 LU** (16,9–21,1) | **14,8 LU** (13,9–15,4) | **Fixa por produto** |
| Música 0–20 s × cauda | −32,7 × −33,2 LUFS | −42,9 × −40,4 LUFS | Volume constante do começo ao fim |
| Batida presente desde o início | 15/15 (periodicidade 0,42–0,58) | 15/15 (0,73–0,83) | **Música toca desde o 0:00 em 30/30** |
| BPM | 105 em 15/15 | 110 em 15/15 | **Mesma música em todos os criativos do produto** |

\* Gelato: 5 vídeos sem CTA verde detectado no automático, e alguns entram 1–5 s antes (o CTA aparece e a
voz ainda fecha a frase anterior). A maioria fica entre 0,1 e 1 s.

**Leitura:** cada produto tem um **perfil de mixagem fixo** (mesma música, mesmo volume da música, mesma
cauda), e esse perfil se repete nos 15 criativos. Ao montar um criativo novo de um produto, use o perfil
dele (`musica_lu` e `cauda` no spec).

## Gancho falado × imagem dos primeiros 3 s (os 30)

| Família de gancho | Exemplos (fala) | O que a imagem mostra |
|---|---|---|
| **Demonstrativo + objeto + dinheiro** | "¿Tú crees que *estos frasquitos* me hacen vender 20 mil…" (salsas ad12) · "Você acredita que *esses potinhos* me fazem vender R$10 mil…" (gelato ad7) | **o objeto citado**: frasquitos / mulher com dezenas de potinhos |
| **Ingredientes baratos/poucos** | "*Un puñito de chiles secos y una cebolla*…" (ad8) · "Agarré *1 kilo de jalapeño* por 22 pesos" (ad9) · "esse sorvete de doce de leite com *dois ingredientes*" (gelato ad6) | **os ingredientes, na ordem falada**: chiles secos na panela → cebola / jalapeños / doce de leite |
| **"Vem comigo / Vente conmigo"** | "Vente conmigo a ver las recetas de salsa de chile que me hacen facturar 20 mil" (ad3) · "Vem comigo aprender a receita de gelatos que me faz faturar" (gelato ad3) | pessoa fazendo/mostrando o produto, ou produção em volume (copos sendo enchidos) |
| **História de dor → virada** | "me corrieron de mi trabajo porque salí embarazada" (ad1 / gelato ad1) · "Mi exmarido me dijo…" (ad2) · "trabajaba 12 horas en un hospital" (ad5) · "Eu não sabia fazer nada de doce" (gelato ad4) | **o produto sendo feito/servido** (o "hoje": a virada). Não se ilustra a dor. |
| **Inimigo / comparação com o mercado** | "Ya viste la cantidad de conservadores… que tiene" (ad13) · "Quem vai pagar 40 reais num pote de sorvete?" (gelato ad2) · "Sabe aquele pote de sorvete que a gente compra no mercado?" (gelato ad8) · "Sabe aquele gelato… que custa uma fortuna?" (gelato ad11) | **o inimigo citado**: prateleira de molhos industriais com sticker ⚠ / potes / pote branco de mercado com etiqueta "sorvete caseiro" / gelato de casquinha |
| **Promessa direta / entrega** | "Te voy a mandar más de 100 recetas de salsas a tu WhatsApp" (ad6) · "7 dias e 7 ideias de gelatos" (gelato ad10) · "a verdadeira base italiana de gelato" (gelato ad5) | **variedade** (vários potinhos de salsas diferentes) ou o produto pronto |
| **Segredo / autoridade** | "la receta secreta de mi abuela de 100 años" (ad14) · "Nadie prepara salsa de chile como yo" (ad11) · "os gelatos que a gente prepara aqui na Itália" (gelato ad14) · "Você acha que conhece esse sorvete? Então olha como ele é feito aqui na Itália" (gelato ad15) | produto premium em close (salsa caindo, bandeja de gelateria) ou pessoa provando ("yo") |
| **Lista** | "3 de las mejores salsas taqueras, voy a empezar por la de guacamole" (ad15) | **o 1º item citado** (salsa verde de guacamole) |

Regra que sai daqui: **o que a frase nomeia aparece; se ela não nomeia nada visível (história, emoção),
aparece o produto sendo feito ou servido, no plano mais apetitoso.**

Os ângulos se repetem **entre produtos**: o mesmo modelo de copy vira um criativo de salsas e outro de
gelato (ad1 "demitida grávida", ad3 "vem comigo", ad12/ad7 "esses frasquitos/potinhos"). O modelo de
edição também é o mesmo.

## O que mais o lote confirmou
- **Zero legenda** no meio dos 30 (90 quadros checados em 20/40/60% de cada vídeo). O único texto do editor é
  o CTA. Aparecem stickers queimados nos próprios b-rolls (comentário do TikTok, ⚠ de outro criador) e
  nada mais.
- Pessoa na tela (cozinheira, mulher provando, gelateira com potes) aparece em vários. Nunca há
  lip-sync com a narração: é b-roll de pessoa.
- B-roll de vários criadores diferentes no mesmo vídeo (cozinhas e mãos diferentes). Coerência de cozinha não
  importa; o que importa é o assunto bater com a fala.
