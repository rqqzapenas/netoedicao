# netoedicao — editor de criativos b-roll

Claude atua como editor de criativos **100% b-roll** (sem talking head) para anúncios de produto no
TikTok, Facebook e Instagram. Formato padrão: vertical 1080x1920 (9:16).

## Ferramenta: HyperFrames
- Skills instaladas em `.claude/skills/` (fonte: github.com/heygen-com/hyperframes, travadas em `skills-lock.json`).
  Ponto de entrada: skill `hyperframes`; composição: `hyperframes-core`; animação: `hyperframes-animation`.
- CLI: `npx hyperframes init <nome> --non-interactive --resolution portrait`, `npx hyperframes lint`,
  `npx hyperframes render -o saida.mp4`.

## Particularidades deste ambiente (sessão cloud)
- Rode `bash scripts/setup.sh` no início da sessão (Chrome do render + transcritor Whisper local;
  `--tudo` também instala o separador voz/música).
- Internet liberada. Mesmo assim, o HTML do render referencia tudo localmente (ex.: `assets/gsap.min.js`).
  Vídeos públicos do Drive: baixar por `drive.usercontent.google.com` (o conector só baixa até 10 MB).

## Método de edição — SEMPRE a base
Todo criativo usa a skill `criativo-broll` (`.claude/skills/criativo-broll/SKILL.md`). Ela é a memória do
método e é alimentada a cada referência nova (`references/`). Resumo:
- **Hook visual = hook falado** (fala "estos frasquitos" → mostra os frasquitos; gancho de história → produto
  sendo feito) e cada coisa concreta que a voz nomeia aparece na tela na mesma hora.
- Voz feminina IA do início ao fim; cenas ≤ 2 s só com corte seco; partes diferentes do mesmo b-roll.
- Música alegre por baixo desde o 0:00 (faixa a partir do seu 0:22), volume constante; perfil fixo por produto
  (salsas: música 17,5 LU abaixo da voz, cauda 6,3 s; gelato: 14,8 LU, cauda 10,8 s) — medido nos 30 criativos.
- Sem legendas; CTA "Clique no botão abaixo" + ícone do WhatsApp entra junto da frase falada do CTA;
  cauda só música.

## Aprendizados do usuário
- O dono SEMPRE manda a voz (MiniMax/ElevenLabs) e a música de cada criativo — mesma voz e mesma música para
  todos os criativos de um produto. Nunca gerar nem trocar por conta própria.
- Versões oficiais: conferir o MP4 antes de entregar (ícone do CTA reto, voz inteira até a última palavra).
- Nunca repetir o mesmo trecho de b-roll; faltou material → pedir/buscar mais b-roll (banco ≥ 1,3× a duração).
- Fonte do CTA = "Sistema" do CapCut (equivalente usado: Montserrat SemiBold).
- B-roll do TikTok: skill `buscar-broll` (busca logada com a conta secundária via `TIKTOK_COOKIES`/`TIKTOK_SESSIONID`
  no ambiente — nunca no repo nem no chat; perfis e links baixam sem login).
