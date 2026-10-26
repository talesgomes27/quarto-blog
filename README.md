# quarto-blog

Portal de Tales Gomes em Quarto: projetos, estudos e textos sobre ciência de dados e tecnologia. Português é o idioma principal; cada estudo publicado tem uma versão em inglês.

## Prévia e renderização

Requisitos: Quarto (validado com 1.10.19) e Python 3, usado pelo hook de navegação. A atualização visual não acrescenta dependências de R ou Python às páginas do portal.

```bash
quarto preview
quarto render
python3 tests/test_localize.py _site
```

O diretório `_site/` já era versionado neste projeto e contém o site renderizado. Renderizar não publica. O workflow `.github/workflows/pages.yml` valida e publica o artefato `_site/` versionado no GitHub Pages após push em `main`. No repositório, Settings → Pages → Source deve estar como **GitHub Actions**. O site é servido em https://talesgomes27.github.io/quarto-blog/.

## Estrutura e idiomas

| Conteúdo | Português | Inglês |
| --- | --- | --- |
| Início | `index.qmd` | `en/index.qmd` |
| Arquivo | `textos.qmd` | `en/textos.qmd` |
| Sobre | `about.qmd` | `en/about.qmd` |
| Bike-share | `posts/bike-share-navigate/pt.qmd` | `posts/bike-share-navigate/index.qmd` |
| Bellabeat | `posts/bellabeat/index.qmd` | `posts/bellabeat/en.qmd` |

Os endereços antigos dos estudos foram preservados. `scripts/localize.py` roda após o render e adapta a navbar nativa do Quarto: rótulos, links de navegação, idioma do HTML e alternates `hreflang`. O seletor PT/EN aponta para a página equivalente por links HTML estáticos. A busca, o menu responsivo e as listagens continuam nativos do Quarto.

Para adicionar um projeto ou texto:

1. Crie o conteúdo em `.qmd`, com título, descrição, data, idioma e imagem.
2. Prepare e revise sua tradução em outro arquivo. `lang` localiza a interface do Quarto; não traduz o conteúdo.
3. Adicione o par de caminhos HTML em `PAIRS`, em `scripts/localize.py`, e inclua cada versão na listagem do seu idioma. Para destacar um trabalho, atualize as duas homes.
4. Renderize e execute a verificação acima. Confira o seletor em ambos os sentidos.

Se o domínio mudar, atualize `website.site-url` em `_quarto.yml` e `SITE_URL` em `scripts/localize.py`.

## Preservação das análises

Os quatro artigos publicados usam `engine: markdown` e `freeze: false`: renderizar o site não recalcula as análises nem baixa dados. As duas versões de cada estudo compartilham resultados identificados e gráficos localizados. Os `_freeze/` históricos permanecem intactos, e os seis arquivos de entrada anteriores à correção foram preservados em `docs/revisions/2026-10-26/before/`, com manifesto SHA-256.

O **Bike-share** é uma reconciliação dos agregados históricos. O script confere hashes, calcula os resultados apresentados e gera os gráficos; não reprocessa os CSVs completos nem usa o fallback sintético do repositório externo.

```bash
Rscript --vanilla scripts/reconcile_bikeshare.R
python3 tests/test_bikeshare_revision.py
```

O **Bellabeat** foi recalculado em R a partir do ZIP original do Zenodo, com remoção das três duplicatas exatas de sono, chaves únicas, junções verificadas e normalização das comparações semanais. O script verifica MD5 e SHA-256 do ZIP antes da leitura. A cópia dos dados brutos fica fora do repositório.

```bash
Rscript --vanilla scripts/rebuild_bellabeat.R /caminho/mturkfitbit_export_4.12.16-5.12.16.zip
python3 tests/test_study_corrections.py
quarto render
python3 tests/test_localize.py _site
```

Os scripts requerem R e os pacotes instalados registrados na proveniência: ggplot2, jsonlite e digest; Bellabeat também usa data.table e dplyr. Não instalam dependências nem fazem download. Resultados agregados, tabelas, gráficos, versões e hashes ficam em `revision-2026-10-26/`, dentro de cada estudo. O detalhamento das correções está em [changes.md](docs/revisions/2026-10-26/changes.md).

O comparativo Netflix/Amazon permanece rascunho e fora da busca e das listagens. Para qualquer artigo computacional futuro, renderizar um arquivo isoladamente pode executar seu código; não apague `_freeze/` para uma mudança de apresentação.

## Identidade visual

`custom.scss` configura o tema light e `custom-dark.scss` o dark; a alternância nativa do Quarto fica na navbar, com nome acessível em PT/EN e preferência persistente. O Giscus acompanha a troca com light/dark_dimmed; `styles.css` define a composição responsiva aprovada. A fonte Mukta Malar é servida localmente, com licença em `assets/fonts/OFL.txt`. As fotografias de `assets/plates/` foram geradas por IA como ilustrações dos assuntos; os arquivos `.webp.json` registram seus prompts. Não representam os dados ou resultados dos estudos.

O sistema visual está descrito em `DESIGN.md`. O JSON de tokens, a preferência de construção e o registro da direção em `.impeccable/` são versionáveis; propostas, capturas e arquivos temporários de revisão são ignorados pelo Git. Esses arquivos de desenvolvimento não são incluídos no site renderizado.

## Validação desta atualização

Render completo, navegação estática PT/EN, links e assets locais, listagens por idioma e exclusão do rascunho verificados. Menu móvel, busca e troca de idioma exercitados no navegador. Layout inspecionado em desktop e celular, com revisão independente.

As correções dos estudos foram verificadas por testes de preservação, contagens, aritmética e hashes e por revisão independente. Bellabeat foi recalculado em R e confrontado com uma implementação Python; Bike-share permanece limitado aos agregados arquivados, sem reprodução dos CSVs completos. A publicação no GitHub Pages foi concluída e conferida em produção; execução e hashes públicos estão em `task.md` e `docs/pages-smoke-2026-10-26.json`. Envio e remoção reais de um comentário por estudo/idioma foram conferidos no Giscus e no GitHub; nenhum comentário de teste permaneceu. Registro em `docs/comment-submission-tests-2026-10-26.json`. Os IDs públicos do Giscus foram preservados do HTML anterior para evitar uma consulta de rede durante o build.
