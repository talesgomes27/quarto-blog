# Substituição do Bike Share — 26/10/2026

O autor solicitou substituir a versão histórica do blog pelo projeto atualizado de `DAC8-Case-Study-1` e confirmou a tradução completa do relatório para inglês.

## Origem e alcance

- Fonte: `DAC8-Case-Study-1/docs/index.html`, do checkout local limpo no commit `c4295b70c2fd8c850d11bf5382a52b9f04978288`.
- O relatório foi importado como Markdown estático nas URLs existentes: `posts/bike-share-navigate/pt.html` e `posts/bike-share-navigate/index.html`.
- Preservados: cinco tabelas, nove gráficos PNG extraídos sem alteração de bytes e 14 blocos de código R. Listas que o HTML de origem havia achatado foram restauradas a partir de `report/index.qmd`.
- Traduzidos: as seis fases completas, tabelas, legendas e descrições acessíveis. Código R, nomes das variáveis do modelo e textos internos das imagens permanecem originais; a versão EN explica os rótulos dos gráficos.
- Home e arquivo passam a apresentar a edição de 13/10/2026. As duas fontes históricas substituídas estão compactadas neste diretório; os resultados e recursos da reconciliação histórica continuam preservados.
- Nenhum pipeline R ou alternativa sintética foi executado. Resultados e interpretações do relatório fornecido foram preservados, sem nova auditoria científica. O repositório de origem não foi alterado.

Os hashes do relatório, da fonte Quarto, das figuras e dos artigos históricos estão em `posts/bike-share-navigate/updated-2026-10-13/provenance.json`. Os snapshots compactados da edição importada também estão nesse diretório.

## Validação local

- Quarto 1.10.19: renderização completa das 13 páginas concluída; novas páginas usam `engine: markdown` e matemática MathML.
- `python3 tests/test_localize.py _site`: navegação PT/EN aprovada.
- `python3 tests/test_study_corrections.py`: evidências anteriores e Bellabeat preservados.
- `python3 tests/test_bikeshare_revision.py`: reconciliação histórica arquivada, hashes dos snapshots, igualdade de todos os valores numéricos das tabelas, nove figuras idênticas e 14 blocos de código idênticos ao HTML de origem.
- Parser HTML: destinos locais de links e recursos presentes nas seis páginas afetadas (home, arquivo e estudo, PT/EN).
- Navegador: relatório PT no desktop; relatório EN no celular em tema claro/escuro; nove imagens carregadas; tabelas e fórmula com rolagem local e foco de teclado; código expansível sem transbordamento da página a 375px.

A publicação segue o workflow existente após push para `main`; este registro descreve a validação local anterior ao envio.
