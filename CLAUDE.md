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

## Aprendizados do usuário
(preencher conforme o treinamento — estilo, ritmo de corte, hooks, legendas, CTA)
