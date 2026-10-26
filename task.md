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
- Concluído: commit `00d8c34cf314312809950ac4b2482f6f761dbfbf` publicado; workflow [40275442018](https://github.com/talesgomes27/quarto-blog/actions/runs/40275442018) terminou com sucesso. Oito arquivos públicos retornaram HTTP 200 e correspondem byte a byte ao artefato validado.
- Browser público: quatro widgets Giscus carregaram sem erro visível de repositório/app, com editor, prévia e login no idioma correto; nenhum comentário ou reação enviado. Autenticação e envio efetivo não testados.
- Textos público: categoria R mostra os dois estudos e Todos restaura a lista; página conferida visualmente. Registro: `docs/archive-comments-smoke-2026-10-26.json`.

## Continuação — envio real de comentários e tema dark

- Autor autorizou quatro comentários temporários e sua remoção, além do tema dark com alternância na navbar. A nova autorização Giscus no GitHub foi confirmada explicitamente antes do clique em Authorize.
- Envios reais: Bike-share PT/EN e Bellabeat PT/EN confirmados pelo editor Giscus e pelo GitHub. Removidos somente os IDs dos testes, com comparação exata de corpo e autor. Zero comentários restantes confirmado na API e nos quatro formulários. Conversas vazias criadas pelo Giscus foram preservadas. Evidência sem tokens: `docs/comment-submission-tests-2026-10-26.json`.
- Tema: alternância nativa Quarto light/dark, light existente preservado, dark com fundo azul profundo e acento verde. Preferência persiste entre páginas; fotos e gráficos não recebem inversão. Giscus acompanha light/dark_dimmed. Toggle nomeado em PT/EN e com área de toque de 44px.
- Validação concluída: dark na home e Sobre desktop, Textos EN no celular, ausência de overflow, retorno ao light, persistência ao navegar/recarregar e stylesheet do Giscus alternando entre `/themes/light.css` e `/themes/dark_dimmed.css`. Revisão independente sem bloqueadores; contrastes dark de texto e links acima de AA. Testes de idioma/temas, preservação e aritmética dos estudos passaram. Concluído: tema publicado no commit `61c2f84b638ee7e2c4f67811e2f47cd517624095`, seguido da correção de cache `2be95cd681f7f26f03799a34a65d04438ae3a075`. Workflow final [40277301223](https://github.com/talesgomes27/quarto-blog/actions/runs/40277301223) terminou com sucesso.
- O CSS personalizado recebe query de versão pelo SHA-256 para impedir mistura de nova paleta e CSS antigo em cache. Teste cobre a transformação idempotente e presença da versão nas páginas.
- Smoke final público: 17 páginas/recursos retornaram HTTP 200 e correspondem ao artefato local. Toggle, tons computados, área móvel de 44×44px, ausência de overflow e sincronização Giscus conferidos no navegador integrado; preferência restaurada ao light. Registro: `docs/dark-theme-smoke-2026-10-26.json`.
- Não foram testados outros navegadores. Nenhum comentário de teste permaneceu; quatro conversas vazias criadas pelo Giscus foram mantidas.

## Continuação — extensões e distribuição dos estudos

- Modo contínuo: aplicação das recomendações autorizada; commit e push cobertos pelo pedido anterior nesta conversa. Destino preservado: `main` de `talesgomes27/quarto-blog`, com deploy pelo workflow Pages existente. Base: `a523e7c`.
- Artefato preparado: `_site/` renderizado com Quarto 1.10.19. Prévias de links internos no portal; retomada de leitura e citação ABNT/APA nos quatro estudos; feeds RSS separados PT/EN; links de compartilhamento LinkedIn/e-mail. Resultados, código e execução estática das análises preservados.
- Inventário local: 263 extensões distintas nas quatro listagens oficiais, guia de decisão, script de atualização e orientação permanente em `AGENTS.md`. Três dependências fixadas por commit, licenças e hashes em `docs/quarto-extensions/installed.json`.
- Prontidão local: render completo, cinco verificações Python aprovadas e navegação dirigida no navegador. Prévias nos dois idiomas/temas, retomada de leitura, citação/BibTeX e layout de 375px conferidos; detalhes e limites no guia. Sem envio de compartilhamentos ou comentários.
- Publicação concluída: commit `3c769511dceef66221d06511b0dda7b578c3d90f` enviado para `main`; workflow [40336453500](https://github.com/talesgomes27/quarto-blog/actions/runs/40336453500) terminou com sucesso. Smoke público: 24 páginas/recursos HTTP 200 e idênticos byte a byte ao artefato validado, incluindo os dois feeds e os assets das extensões. Registro em `docs/extensions-smoke-2026-10-26.json`.
- Navegador público: prévia da home PT carregou título e descrição corretos; painel de citação do Bike Share PT abriu recolhível, com somente ABNT/APA e URL completa da tradução. Nenhum compartilhamento ou comentário enviado. Os demais testes interativos permanecem os locais documentados no guia.
- Recuperação segue o mecanismo existente: novo commit de reversão da alteração identificada, com render e publicação, sem reescrever histórico; executar recuperação somente se autorizada.

## Continuação — ícones de compartilhamento

- Esclarecido que `social-share` não foi instalada: a funcionalidade usa links HTML locais. Adicionados os ícones Bootstrap de LinkedIn e envelope aos botões dos quatro estudos, mantendo rótulos PT/EN e URLs. Ícones decorativos usam `aria-hidden`; botões mantêm 44px.
- Atualização executada pelo pós-render existente e cópia do CSS, sem reexecutar análises. Cinco verificações Python passaram. Navegador local: PT desktop claro e EN em viewport de 375px escuro, ícones renderizados e sem transbordamento. Envios reais não testados.
- Commit e push seguem a autorização anterior, com o workflow Pages e a recuperação já documentados.
- Publicado no commit `e1e75540334b7649bffdb43828d0e771d9e49184`; workflow [40338132076](https://github.com/talesgomes27/quarto-blog/actions/runs/40338132076) concluído com sucesso. Os quatro artigos, CSS e fonte de ícones responderam HTTP 200 e corresponderam ao artefato local. Ícones e rótulos também conferidos no Bellabeat PT público. Evidência em `docs/share-icons-smoke-2026-10-26.json`.
