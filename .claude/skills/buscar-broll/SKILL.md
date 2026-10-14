---
name: buscar-broll
description: >
  Encontrar e baixar b-rolls do TikTok para os criativos do método do Neto — busca por palavra-chave com a
  conta de busca logada, listagem de perfis, download sem marca d'água em 1080p, folha de contato de cada
  vídeo e triagem do que serve como b-roll (mão e produto em ação, sem talking head, sem texto queimado,
  batendo com a copy). Use quando o dono pedir "pega b-roll", "acha b-roll de X no TikTok", "busca vídeos
  de finger food", "baixa esses vídeos", "puxa os vídeos desse perfil", ou quando o montador avisar
  "b-roll insuficiente". Entrega a pasta pronta para a skill criativo-broll.
---

# Buscar b-roll no TikTok

> **REGRA ABSOLUTA DO DONO: NUNCA baixar b-roll que tenha legenda/texto na imagem.**
> Todo vídeo passa pela checagem anti-texto ANTES do download (`baixar_broll.py` faz sozinho). Uma cópia de
> baixa resolução vai para um diretório temporário, o OCR lê 12 quadros do vídeo inteiro, e a cópia é
> apagada. Achou texto → rejeitado, não é salvo e vai para `rejeitados.tsv`. O filtro é propositalmente rígido:
> texto de rótulo ou marca grande em cena também reprova. Nunca contorne isso baixando direto com yt-dlp.

O banco de b-roll decide a qualidade do criativo. A skill `criativo-broll` precisa de material variado,
que **mostre o que a copy fala** e com **≥ 1,3× a duração do vídeo**, porque nunca se repete trecho.

## Como funciona
| Fonte | Como | Login? | Rende |
|---|---|---|---|
| **Página de hashtag** `/tag/<termo>` | `tiktok_busca.mjs` (Chromium headless, lê a API da página) | **Não** (logado dá captcha) | ~110–150 vídeos por hashtag |
| Página discover `/discover/<termo-com-hifen>` | idem | Não | 0–45 (nem todo termo tem página) |
| Busca por palavra-chave | idem, com a sessão logada | Sim | ~0–20: o TikTok pede captcha a servidor |
| Perfil | `baixar_broll.py @perfil` (yt-dlp) | Não | os últimos vídeos |
| Links soltos | `baixar_broll.py URL …` | Não | — |

- O script abre hashtag e discover num contexto **sem login**, porque logado o TikTok mostra captcha também
  nessas páginas. A busca logada é só complemento.
- Só entram resultados das APIs de busca, hashtag e discover. O feed "para você" que a página carrega por
  trás é ignorado.

**Rendimento real** (teste de finger food, 12 mais vistos): 10 rejeitados por texto, 1 irrelevante, 1
aprovado. Por isso:
- peça **muitos candidatos** (`--max=150` rende ~20–30 limpos);
- use **várias hashtags** em pt, es e en.

**Login da conta de busca** (conta secundária, nunca a principal), em ordem de preferência:
1. variável `TIKTOK_COOKIES` com o cookies.txt inteiro, puro ou em base64;
2. `--cookies=arquivo` apontando para um arquivo **fora do repo**;
3. `TIKTOK_SESSIONID`, só o sessionid. É o mais fraco: o TikTok às vezes recusa.

Nunca grave cookie ou senha no repositório. O script mostra "✓ logado como @…" ou "✗ sem login válido".

## Fluxo
1. **Setup**: `bash scripts/setup.sh` na raiz do repo. Instala yt-dlp + curl_cffi + playwright-core.
2. **Monte a lista de buscas a partir da copy**, não do nome do produto. Para cada bloco da copy:
   - o **objeto do gancho**;
   - **cada coisa concreta nomeada** (ingredientes, variedades, embalagem, "potinhos", "mercado");
   - **produto pronto** (money shot);
   - **processo**;
   - **pessoas provando**.
   Busque em pt, es e en: os melhores b-rolls costumam ser gringos. Exemplo (finger food): "finger food",
   "mini coxinha", "salgadinho de festa", "canapés", "bocaditos", "party appetizers", "mini quiche",
   "appetizer recipe", "festa salgados caseiros".
3. **Busque** (no projeto do criativo). Cada termo vira hashtag + discover + busca logada; use também
   `"#hashtag"` e `"discover:slug"` explícitos:
   `node .claude/skills/buscar-broll/scripts/tiktok_busca.mjs "finger food" "#appetizers" "mini salgados" --rolagens=6 --saida=busca.jsonl`
4. **Baixe os melhores**. O script filtra vertical, 6–180 s, legenda do post com algo de comida e mais
   plays primeiro, e **só baixa o que passa na checagem anti-texto**:
   `python3 .claude/skills/buscar-broll/scripts/baixar_broll.py busca.jsonl brutos/ --max=150 --min-plays=20000`
   (~10 s por vídeo checado; rode em segundo plano)
   Perfis bons de b-roll: `baixar_broll.py @perfil brutos/ --max=30`.
5. **Triagem visual**: abra `brutos/folhas/*.png`.
   - **Aprova**: mão/utensílio em ação, close apetitoso, luz boa, vertical cheio, cozinha bonita,
     variedade.
   - **Reprova**: qualquer texto ou legenda (se escapou do OCR, apague o arquivo), pessoa falando para a
     câmera o tempo todo, marca d'água de outro app, horizontal com barras, escuro, tremido, produto feio,
     assunto fora da copy (dança, meme).
   - **Aproveita parcial**: se só um trecho presta, anote o intervalo (o montador usa trechos).
6. **Organize para o montador**: copie os aprovados para `broll/` com o prefixo de categoria:
   - `gancho_*` = o objeto da 1ª frase;
   - `final_*`, `processo_*`, `textura_*`, `reacao_*`;
   - nomes que digam o que é (`processo_mini_coxinha_modelando.mp4`), porque as âncoras de `sincronia`
     apontam para eles.
7. **Confira o banco**: soma das durações aprovadas ≥ 1,3× a duração prevista do vídeo, e pelo menos 1
   clipe para cada coisa concreta da copy. Faltou? Volte ao passo 3 com termos mais específicos.
8. Entregue ao dono a lista do que achou (folhas mais fortes) antes de montar, se ele quiser aprovar.

## Observações
- O download pega o maior formato (normalmente 1080x1920 em H.265, que o render aceita) e sem marca d'água.
- O áudio original do b-roll não é usado: o montador deixa todo b-roll mudo.
- A maioria dos vídeos de receita tem legenda queimada, e todos esses são descartados (regra do dono). Não
  existe "aproveitar só o trecho sem legenda".

## Rostos no b-roll
- A folha de contato (12 quadros) não pega rosto que aparece 1–2 s no meio da receita ("provando", corte para a
  câmera). Depois de aprovar clipes novos, rode `python3 scripts/detectar_rostos.py banco/ --saida=rostos.json`
  (YuNet, 4 quadros/s, ~0,1 s por segundo de vídeo) e junte o resultado ao `evitar_banco.json` do produto.
- Rodada 3 do finger foods: 46 dos 136 clipes tinham algum trecho com rosto.

## Barras pretas embutidas
- Alguns vídeos vêm com faixa preta queimada na imagem (pillarbox/letterbox dentro do 1080x1920). O `object-fit:
  cover` não tira isso. Ao aprovar clipes, rode `cropdetect` em cada um e, se a área útil for < 97% da largura ou
  da altura, recorte e regrave antes de pôr no banco:
  `ffmpeg -ss <meio> -i x.mp4 -t 3 -vf cropdetect=24:2:0 -f null - 2>&1 | grep -o "crop=[0-9:]*" | sort | uniq -c | sort -rn | head -1`
  `ffmpeg -i x.mp4 -vf "crop=W:H:X:Y" -c:v libx264 -crf 18 -an x_ok.mp4`
- Finger foods: `gancho_caixinha_canapes` (laterais) e `gancho_coxinha_producao_massa` (topo/base) foram recortados.
  Ao restaurar o banco do `banco.tsv`, recorte esses dois de novo.
