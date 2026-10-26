# Publicação do portal — 2026-10-26

## Escopo e autorização

Modo contínuo: o autor autorizou remover a marca da foto, verificar links externos e publicar as atualizações no GitHub Pages de `talesgomes27/quarto-blog`.

## Artefato e destino

- Base anterior: `566a8c579db492ee6427aaa723c24a203fad3912`.
- Artefato: `_site/` renderizado com Quarto 1.10.19, com PT principal, versões EN, página Sobre e estudos corrigidos com proveniência preservada.
- Destino: https://talesgomes27.github.io/quarto-blog/.
- Origem Pages configurada como GitHub Actions; push em `main` executa validação e publicação do `_site/` versionado.
- O push também pode acionar a integração Netlify já existente. Nenhuma configuração ou conta Netlify foi alterada.

## Verificações

- Render completo concluído; navegação PT/EN e testes dos dois estudos passaram.
- Parser HTML: nenhum destino local ausente em href/src no artefato.
- Links externos: currículo, DataCamp, GitHub e fontes disponíveis; Fitabase 404 substituído pela página oficial. LinkedIn respondeu 999 e permanece sem confirmação automatizada.
- Foto: original preservado; edição via image_gen registrada em `assets/profile/tales-gomes-clean.json`.
- Layout desktop/mobile revisto; sem mudança nos resultados científicos nesta publicação.

## Recuperação

Preservar histórico e reverter o commit de publicação, renderizar e enviar um novo commit pelo mesmo fluxo. Não reescrever branches nem apagar os registros anteriores. A recuperação, se necessária, deve ser confirmada e verificada no destino.

## Estado

Preparado para commit e push; execução remota e smoke tests públicos pendentes.
