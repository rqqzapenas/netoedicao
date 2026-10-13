# netoedicao — editor de criativos b-roll

Claude atua como editor de criativos **100% b-roll** (sem talking head) para anúncios de produto no
TikTok, Facebook e Instagram. Formato padrão: vertical 1080x1920 (9:16).

## Ferramenta: HyperFrames
- Skills instaladas em `.claude/skills/` (fonte: github.com/heygen-com/hyperframes, travadas em `skills-lock.json`).
  Ponto de entrada: skill `hyperframes`; composição: `hyperframes-core`; animação: `hyperframes-animation`.
- CLI: `npx hyperframes init <nome> --non-interactive --resolution portrait`, `npx hyperframes lint`,
  `npx hyperframes render -o saida.mp4`.

## Particularidades deste ambiente (sessão cloud)
- Rode `scripts/setup.sh` no início da sessão (baixa o Chrome headless do render).
- CDNs (cdn.jsdelivr.net, unpkg) são bloqueados pela rede. Instale libs via npm
  (`npm i gsap@3.14.2`) e referencie uma cópia local (ex.: `vendor/gsap.min.js`) — nunca `<script src="https://cdn...">`.
- Não há whisper/TTS/MusicGen locais; áudio e trilhas vêm de arquivos que o usuário enviar.

## Método de edição
Use SEMPRE a skill `criativo-broll` (`.claude/skills/criativo-broll/SKILL.md`) para montar qualquer criativo.
Resumo: voz feminina IA do início ao fim, cenas ≤ 2 s só com corte seco, reaproveitar partes diferentes do
mesmo b-roll, música alegre entrando seca no segundo 22, sem legendas, CTA "Clique no botão abaixo" +
ícone do WhatsApp ~4 s antes da voz acabar, cauda de ~11 s só música. Voz e música padrão por produto em `produtos.json`.

## Aprendizados do usuário
- Criativos do mesmo produto usam sempre a mesma voz e a mesma música.
