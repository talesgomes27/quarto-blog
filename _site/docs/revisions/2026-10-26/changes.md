# Correções aplicadas aos estudos — 26/10/2026

Autorização: corrigir os problemas identificados nos dois estudos, atualizar português e inglês e manter a rastreabilidade. As datas originais dos artigos foram mantidas; `date-modified` identifica esta revisão.

## Versões e entradas preservadas

O [manifesto anterior](before-manifest.json) registra hashes SHA-256 e cópias comprimidas das quatro fontes Quarto e dos dois resultados computacionais históricos. Os dois arquivos `_freeze/` permanecem byte a byte iguais às cópias preservadas. Os pareceres de diagnóstico em `docs/reviews/` descrevem a situação anterior e não foram reescritos como se fossem a versão corrigida.

O [manifesto da correção](applied-manifest.json) identifica as fontes atuais e os recursos gerados. Os artigos apontam para os próprios resultados, scripts e fontes históricas, permitindo comparar as duas versões.

## Bike-share: reconciliação histórica

Foi adotada a reconciliação dos agregados do blog, referentes a julho de 2020–junho de 2021. Não foram incorporadas métricas do pipeline mais recente do repositório externo, que usa filtros diferentes e oferece dados sintéticos como alternativa de execução. Os CSVs completos não foram reprocessados.

| Achados | Correção aplicada | Evidência e limite |
| --- | --- | --- |
| B01–B03 | Percentuais, médias e razões reconciliados; medianas e quartis apresentados | Tabelas arquivadas, contagens conservadas e cálculo verificável no script R |
| B04–B06 | Rankings de meses, dias e bicicletas corrigidos; denominadores explícitos | Junho de 2021 lidera o volume; participação relativa separada de contagem absoluta |
| B07 | Agregados renomeados como trimestres civis, com ano | Composição histórica preservada; nenhuma reclassificação meteorológica alegada |
| B08 | Filtro descrito como duração estritamente superior a dois minutos | Limite histórico mantido e identificado como decisão analítica |
| B09 | Extremos, mediana e IQR explicitados; conclusões noturnas e pico de duração não sustentados retirados | Não foi simulada remoção de extremos; nova estimação com tetos exige os registros individuais |
| B10–B11 | Viagens separadas de pessoas; recomendações tratadas como hipóteses; limitações de localização e integridade declaradas | Não se presume ausência de viés nem se estima conversão individual |
| B12 | Gráficos com rótulos incorretos substituídos por gráficos auditáveis dos agregados | Seis PNGs PT/EN gerados pelo script; figuras históricas não são apresentadas como atualizadas |

Fonte de cálculo: `_freeze/posts/bike-share-navigate/index/execute-results/html.json` e `docs/reviews/evidence/bike-share-audit.json`. Código: `scripts/reconcile_bikeshare.R`. Resultados e hashes: `posts/bike-share-navigate/revision-2026-10-26/results.json`.

O tratamento do risco de durações extremas consiste em limitar a conclusão publicada e mostrar medidas menos sensíveis, mantendo os dados históricos identificados. Isso não equivale a validar novos filtros ou a reproduzir a base bruta.

## Bellabeat: recálculo corrigido em R

Fonte: parcela original de 12/04/2016–12/05/2016 do [Zenodo](https://zenodo.org/records/53894), indicada como origem na ficha Kaggle fornecida. O ZIP de 25.291.915 bytes foi validado por MD5 e SHA-256; os quatro CSVs usados têm hashes registrados. A identidade binária com o download local usado pelo autor em 2021 não foi estabelecida.

| Achados | Correção aplicada | Evidência e limite |
| --- | --- | --- |
| BE01 / BE05 | Alegação preventiva e inferências causais retiradas; medidas repetidas e ausência de desfecho clínico explicitadas | Comparações publicadas são descritivas, sem p-valores ou IC de observações supostamente independentes |
| BE02 | Três duplicatas exatas de sono removidas antes das junções; chaves únicas verificadas; formato longo construído diretamente | 940 participantes-dias, 410 registros de sono e 3.760 linhas longas; falha explícita para chaves conflitantes |
| BE03 | Totais semanais substituídos por médias por participante-dia observado e contagens de cobertura | A exposição desigual de cinco versus quatro datas é informada; composição de participantes continua uma limitação |
| BE04 / BE06 | Fonte Fitbit e contexto Bellabeat separados; cobertura e denominadores informados por variável | 33 IDs na atividade, 24 no sono, 14 em FC e oito em IMC; divergência documental 30/33 declarada |
| BE07 / BE08 | Títulos, eixos e unidades refeitos; distância total e gasto energético total estimado corretamente nomeados | Doze PNGs localizados; variáveis do mesmo dispositivo não são tratadas como validação independente |
| BE09 | Registros e IDs por faixa/variável apresentados, sem assumir grupos independentes | Grupos pequenos continuam marcados como exploratórios |
| BE10 | Tempo total na cama preservado; tempo acordado na cama calculado em coluna separada | Transformação explícita no script e no resumo de variáveis |

Código: `scripts/rebuild_bellabeat.R`. Resultados e comparação histórica/corrigida: `posts/bellabeat/revision-2026-10-26/results.json`. Proveniência: `provenance.json` no mesmo diretório. Não foram publicados registros individuais ou IDs nos novos resultados.

## Validação

- `tests/test_bikeshare_revision.py`: contagens, razões, hashes, figuras PT/EN e snapshots.
- `tests/test_study_corrections.py`: snapshots das seis entradas, `_freeze/` inalterado, resultados Bellabeat contra cálculo independente em Python, normalização semanal, hashes e recursos PT/EN.
- O recálculo Bellabeat foi executado sobre o ZIP validado; testes internos verificaram contagens, unicidade das chaves e ausência da junção muitos-para-muitos. ZIP incorreto é rejeitado antes da extração.
- Revisão independente dos quatro artigos e resultados: os 22 achados foram tratados por correção ou retirada da inferência acompanhada de limitação explícita.
- Renderização e checagens da saída são registradas no manifesto da correção após a integração.
- As tabelas usam regiões roláveis com foco de teclado; comandos inline longos quebram linha no celular, preservando seu conteúdo.

Não houve publicação, envio ao GitHub ou alteração dos repositórios externos. O recálculo do Bellabeat e a reconciliação do Bike-share são operações diferentes e continuam identificados separadamente.
