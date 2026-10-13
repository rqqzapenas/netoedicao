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
- CDNs (cdn.jsdelivr.net, unpkg), HuggingFace e Google Drive são bloqueados pela rede. Libs via npm/pip e
  referenciadas localmente (ex.: `assets/gsap.min.js`); modelos vêm de releases do GitHub.

## Método de edição — SEMPRE a base
Todo criativo usa a skill `criativo-broll` (`.claude/skills/criativo-broll/SKILL.md`). Ela é a memória do
método e é alimentada a cada referência nova (`references/`). Resumo:
- **Hook visual = hook falado** (fala "estos frasquitos" → mostra os frasquitos) e cada coisa concreta que a
  voz nomeia aparece na tela na mesma hora.
- Voz feminina IA do início ao fim; cenas ≤ 2 s só com corte seco; partes diferentes do mesmo b-roll.
- Música alegre por baixo desde o início (faixa a partir do 0:22), 12–18 LU abaixo da voz, volume constante.
- Sem legendas; CTA "Clique no botão abaixo" + ícone do WhatsApp entra ~0,4 s antes da voz falar o CTA;
  cauda de 6–11 s só música.

## Aprendizados do usuário
- O dono SEMPRE manda a voz (MiniMax/ElevenLabs) e a música de cada criativo — mesma voz e mesma música para
  todos os criativos de um produto. Nunca gerar nem trocar por conta própria.
- Versões oficiais: conferir o MP4 antes de entregar (ícone do CTA reto, voz inteira até a última palavra).
- Nunca repetir o mesmo trecho de b-roll; faltou material → pedir/buscar mais b-roll (banco ≥ 1,3× a duração).
- Fonte do CTA = "Sistema" do CapCut (equivalente usado: Montserrat SemiBold).
