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

O banco de b-roll decide a qualidade do criativo. A skill `criativo-broll` precisa de material variado,
que **mostre o que a copy fala** e com **≥ 1,3× a duração do vídeo**, porque nunca se repete trecho.

## Como funciona
| Etapa | Ferramenta | Precisa de login? |
|---|---|---|
| Busca por palavra-chave | `scripts/tiktok_busca.mjs` (Chromium headless, lê a API de busca da página) | **Sim**: o TikTok só mostra resultados de busca logado |
| Vídeos de um perfil | `scripts/baixar_broll.py @perfil` (yt-dlp) | Não |
| Download de links | `scripts/baixar_broll.py URL …` (yt-dlp `--impersonate chrome`) | Não |
| Triagem | folhas de contato (12 quadros por vídeo) + olho do Claude | — |

**Login da conta de busca** (conta secundária do dono, nunca a principal):
- Variável de ambiente `TIKTOK_COOKIES`, com o cookies.txt (formato Netscape) do tiktok.com inteiro, puro
  ou em base64. É o preferido: o TikTok às vezes recusa só o `sessionid`.
- Ou a variável `TIKTOK_SESSIONID`, só com o cookie `sessionid`.
- As duas ficam nas configurações do ambiente e valem a partir de uma sessão nova.
- **Nunca** salve cookie ou senha no repositório, nem peça para colar no chat.
- O script avisa "✓ logado como @…" ou "✗ sem login válido (session_expired)". Se expirou, peça ao dono
  para exportar de novo, sem sair da conta depois de exportar.

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
3. **Busque** (no projeto do criativo):
   `node .claude/skills/buscar-broll/scripts/tiktok_busca.mjs "termo 1" "termo 2" --rolagens=6 --saida=busca.jsonl`
4. **Baixe os melhores** (vertical, 6–180 s, mais plays primeiro):
   `python3 .claude/skills/buscar-broll/scripts/baixar_broll.py busca.jsonl brutos/ --max=40 --min-plays=20000`
   Perfis bons de b-roll: `baixar_broll.py @perfil brutos/ --max=30`.
5. **Triagem visual**: abra `brutos/folhas/*.png`.
   - **Aprova**: mão/utensílio em ação, close apetitoso, luz boa, vertical cheio, cozinha bonita,
     variedade.
   - **Reprova**: pessoa falando para a câmera o tempo todo, texto/legenda grande queimado, marca d'água
     de outro app, horizontal com barras, escuro, tremido, produto feio.
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
- Muitos vídeos de receita têm legenda queimada. Prefira os sem legenda. Se o trecho bom não tem texto,
  aproveite só esse trecho.
