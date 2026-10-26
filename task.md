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

Concluído: commit de conteúdo `a07517f6097e3d05ffc3fb25f50a16fd9a617ea9` enviado para `main`. Workflow [40274283622](https://github.com/talesgomes27/quarto-blog/actions/runs/40274283622) terminou com sucesso.

Smoke público: 16 páginas e recursos responderam HTTP 200 com conteúdo byte a byte idêntico ao `_site/` validado, incluindo as dez páginas PT/EN principais, foto corrigida, CSS, fonte, imagem de projeto e gráficos dos dois estudos. Evidência em `docs/pages-smoke-2026-10-26.json`. Página Sobre também conferida visualmente no endereço público.

LinkedIn permanece sem confirmação automatizada (HTTP 999). Não foi testado envio de comentários Giscus. Esta atualização documental não altera o artefato publicado.

## Continuação — Textos e comentários

Pedido: conferir comentários nos dois idiomas e adaptar Textos ao tema publicado.

- Arquivo PT/EN atualizado com listagem nativa, layout responsivo, botões de categoria acessíveis pelo teclado, filtro nomeado e miniaturas com texto alternativo.
- Giscus: repositório público, Discussions habilitado e IDs conferidos ao vivo. Os quatro artigos usam mapeamento por título, com conversas separadas por tradução; não havia discussões existentes. Idioma das duas páginas PT corrigido para `pt`; EN permanece `en`. Nenhum comentário/reação enviado.
- Corrigido filtro de categoria vazio: o runtime antigo de `_freeze/site_libs/` era incompatível com a codificação base64 do Quarto atual. Hook instala a cópia inalterada do runtime Quarto 1.10.19 versionada em `scripts/vendor`, sem alterar os arquivos congelados históricos. URL versionada evita cache antigo.
- Browser local: filtro Bellabeat, estado vazio, ordenação por data, categoria R e reset Todos conferidos; desktop PT e mobile EN sem overflow. Testes cobrem idempotência, rótulos/botões, cópia de runtime e configuração Giscus nos quatro artigos.
- Estado: preparando publicação da continuação e validação dos quatro widgets no destino público.
