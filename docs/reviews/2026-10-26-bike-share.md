# Revisão do estudo Bike-share / Cyclistic

> Registro do diagnóstico anterior à correção. Para o estado atualizado dos artigos e a rastreabilidade das mudanças, consulte o [registro de correções](../revisions/2026-10-26/changes.md).

Data: 26/10/2026. Escopo: reconciliação científica e técnica das versões EN e PT do blog com código, tabelas e gráficos arquivados e com o repositório informado pelo autor. Revisão não destrutiva: artigos, `_freeze/` e site renderizado permanecem intactos.

## Parecer

O artigo precisa de correções antes de servir como referência profissional principal. Há divergências numéricas demonstráveis entre a narrativa e suas próprias saídas: distribuição por tipo de bicicleta, participação dos grupos, médias de duração e rankings de meses/dias. Também há um erro de classificação de estações e interpretações que precisam distinguir viagens de pessoas.

As saídas arquivadas permitem propor uma reconciliação editorial, mas não demonstram que os cálculos sobre os CSVs originais foram reproduzidos. Não foi identificada a causa histórica das divergências, nem se infere fabricação ou alteração intencional.

O repositório atual é uma evolução da análise, não uma fonte intercambiável de resultados para o blog antigo. Usa o mesmo período nominal, porém outros filtros e um pipeline diferente, com alternativa sintética para execução local. Seus números não devem substituir automaticamente os de 2021.

## Evidências e identidade das versões

- Blog EN: `posts/bike-share-navigate/index.qmd`, linhas verificadas nesta revisão; período declarado de julho/2020 a junho/2021 (linha 78).
- Tradução PT: `posts/bike-share-navigate/pt.qmd`. É uma tradução estática das saídas arquivadas, com nota explícita de não reexecução; reproduz as divergências da narrativa inglesa.
- Registro computacional: `_freeze/posts/bike-share-navigate/index/execute-results/html.json`, campo `result.markdown`. Contém 4.460.151 registros na carga e 4.335.006 após a filtragem. Hash SHA-256 e números extraídos: [evidência JSON](evidence/bike-share-audit.json).
- Gráficos inspecionados: `posts/bike-share-navigate/index_files/figure-html/unnamed-chunk-15-1.png` (contagem mensal) e `unnamed-chunk-16-1.png` (duração média mensal).
- Repositório remoto fixado no commit [`5c21b988e46548d7592245d1937cee0c8af6993c`](https://github.com/talesgomes27/DAC8-Case-Study-1/commit/5c21b988e46548d7592245d1937cee0c8af6993c), de 13/10/2026, mensagem `docs: alinha metricas textuais e interpretacoes com a base censitaria real`. Foram consultados README, `docs/index.Rmd`, `report/index.qmd`, scripts de ingestão/limpeza/estatística/Parquet e gerador da amostra. Nada desse código remoto foi executado.

### Diferenças que impedem tratar os pipelines como equivalentes

| Critério | Blog antigo | Repositório atual fixado |
| --- | --- | --- |
| Fonte de execução | CSVs em `database/`, ausentes neste checkout | Parquet prioritário, depois CSVs; sem dados completos, fallback para `sample_tripdata.csv` |
| Duração | `trip_duration > 2`; nenhum teto | `>= 2` e `<= 1440` minutos |
| Coordenadas ausentes | Mantidas | Excluídas, com limites geográficos adicionais |
| Estações | Trimestres jan–mar, abr–jun, jul–set, out–dez, rotulados como estações | Grupos meteorológicos dez–fev, mar–mai, jun–ago, set–nov |
| Saída | Tabelas e gráficos congelados do estudo original | Novas variáveis, testes, regressão e segmentação |

Fontes fixadas: [ingestão](https://github.com/talesgomes27/DAC8-Case-Study-1/blob/5c21b988e46548d7592245d1937cee0c8af6993c/R/01_ingest.R#L17-L66), [limpeza](https://github.com/talesgomes27/DAC8-Case-Study-1/blob/5c21b988e46548d7592245d1937cee0c8af6993c/R/02_clean_and_transform.R), [gerador sintético](https://github.com/talesgomes27/DAC8-Case-Study-1/blob/5c21b988e46548d7592245d1937cee0c8af6993c/data/generate_sample.R#L1-L6). O arquivo [`docs/index.Rmd`](https://github.com/talesgomes27/DAC8-Case-Study-1/blob/5c21b988e46548d7592245d1937cee0c8af6993c/docs/index.Rmd) conserva a versão antiga e os mesmos trechos divergentes. O recorte temporal do gerador também é jul/2020–jun/2021: isso não transforma a simulação em uma amostra dos CSVs reais.

## Achados localizados

Alta = altera resultado/conclusão ou compromete interpretação metodológica. Média = descrição de método, alcance ou comunicação relevante. Os números sugeridos abaixo descrevem o registro arquivado, não uma nova reprodução dos dados brutos.

| ID | Localização EN / PT | Severidade e status | Evidência e diagnóstico | Correção proposta |
| --- | --- | --- | --- | --- |
| B01 | EN 283; PT 883 | Alta; divergência confirmada | A narrativa atribui `classic_bike` >41%, `electric_bike` 31% e `docked_bike` 28%. A tabela registra 1.998.627 docked, 1.089.217 electric e 1.247.162 classic, sobre 4.335.006 viagens: 46,10%, 25,13% e 28,77%, respectivamente. | Se a decisão for preservar o registro antigo, alinhar a narrativa à tabela e à ordem docked > classic > electric. Tratar a origem das divergências como desconhecida. |
| B02 | EN 285; PT 885 | Alta; divergência confirmada | A narrativa informa 55% membros/45% casuais; as contagens arquivadas são 2.447.344/1.887.662, ou 56,46%/43,54%. Arredondar para inteiros produziria 56%/44%, não 55%/45%. | Usar as participações calculadas sobre a mesma base, com denominador explícito de viagens. |
| B03 | EN 293, 336, 697; PT 893, 1144, 1665 | Alta; divergência confirmada | O texto informa média geral 24,26 min, membros 14,71, casuais 36,15 e razão 2,45. A saída geral mostra 26,97 min; a tabela por grupo mostra 15,59300 e 41,72614. A média ponderada calculada dessas médias arredondadas e contagens é aproximadamente 26,97258; a razão é aproximadamente 2,67595. | Reconciliar para 26,97 min geral; 15,59/41,73 por grupo e aproximadamente 2,68 vezes, se mantida a base arquivada. Informar também medianas 11,13/19,70 e a sensibilidade a valores extremos. Não apresentar a aritmética com médias arredondadas como reconstrução de precisão integral. |
| B04 | EN 291, 342, 699; PT 891, 1150, 1667 | Alta; divergência confirmada | O ranking narrativo omite junho. Frequências gerais: junho 709.441; agosto 604.137; julho 540.120; maio 516.940; setembro 516.748. Por grupo, junho também lidera: membros 347.389 e casuais 362.052. O gráfico mensal inspecionado confirma visualmente junho como pico. | No total, usar junho > agosto > julho > maio > setembro; nos grupos, membros junho > agosto > setembro > julho e casuais junho > agosto > julho > maio. Especificar os anos ao discutir evolução: jan–jun são 2021; jul–dez são 2020. |
| B05 | EN 344; PT 1152 | Alta; divergência confirmada | Para membros, o texto declara quarta, quinta e sexta. A tabela `top_counts` registra quarta 376.862, sábado 364.031 e sexta 362.687 como os três maiores. Para casuais, sábado/domingo/sexta está coerente com a saída. | Corrigir somente o ranking de membros; evitar deduzir motivação pendular individual desse ranking. |
| B06 | EN 338, 701; PT 1146, 1669 | Alta; divergência confirmada | A ordem de tipos por grupo também diverge. Membros: docked 1.043.233 > classic 801.776 > electric 602.335. Casuais: docked 955.394 > electric 486.882 > classic 445.386. A frase de que casuais usam mais docked que membros é falsa em contagem absoluta, embora a participação de docked dentro de casuais possa ser maior. | Distinguir quantidade de viagens e composição percentual dentro de cada grupo. Corrigir as ordens e declarar o denominador da comparação. |
| B07 | EN 200–204, 291, 340; PT código correspondente e 891, 1148 | Alta; erro de classificação + divergência confirmados | O código chama jan–mar de inverno, abr–jun de primavera, jul–set de verão e out–dez de outono. São trimestres civis, não estações meteorológicas de Chicago. Sob esses rótulos antigos, as contagens são summer 1.661.005 > spring 1.554.959 > fall 754.436 > winter 364.606, contrariando a ordem summer > fall > spring > winter escrita no texto. | Ou renomear como trimestres civis, preservando os resultados; ou aplicar dez–fev / mar–mai / jun–ago / set–nov e regenerar tabelas e gráficos afetados. A escolha modifica a análise e não deve ocorrer silenciosamente. A narrativa coincide parcialmente com outra classificação possível; isso não identifica a causa histórica. |
| B08 | EN 187, 189, 231; PT 347, 349 e código correspondente | Média; inconsistência de método confirmada | A descrição diz duração >0; outra frase fala em excluir <2. O filtro real é >2, que exclui também exatamente dois minutos. | Documentar “viagens com duração estritamente superior a dois minutos”. Justificar o limiar como decisão analítica; a inspeção de código não comprova que registros curtos sejam erros. |
| B09 | EN 231, 336, 422, 497, 698, 700; PT trechos correspondentes | Alta; risco demonstrado, nova estimativa não validada | Não há teto de duração. Saídas registram máximos de 33.421,37 min para membros e 55.944,15 para casuais, cerca de 23,21 e 38,85 dias. As médias por hora e mês podem ser sensíveis a essas observações. O gráfico mensal mostra julho, não fevereiro, como maior duração média casual. | Não atribuir os extremos a falha, manutenção, furto ou lazer sem evidência. Fazer análise de sensibilidade com mediana/IQR/percentis, contagens por célula e critérios documentados antes de recomendar campanhas com base em médias noturnas. Corrigir a afirmação sobre fevereiro para o que o gráfico efetivamente mostra, ou retirar até conferir valores exatos. |
| B10 | EN 696; PT 1664; recomendações EN 704–708 / PT 1672–1676 | Alta; ambiguidade conclusiva e inferência não sustentada | Casuais têm 789.897 viagens no fim de semana e 1.097.765 nos dias úteis: 41,85%/58,15%. Membros têm 27,64% no fim de semana. É maior concentração relativa dos casuais nos fins de semana que a dos membros, não maioria de suas viagens nesse período. Além disso, as linhas representam viagens, sem ID persistente de pessoa; frequência/retorno individual e conversão não são medidos. | Especificar o comparador: “fins de semana representam uma parcela maior das viagens casuais do que das viagens de membros”. Classificar descontos, fidelidade e conversão como hipóteses a testar com dados transacionais/experimento, sem promessa de eficácia ou identificação de usuários recorrentes. |
| B11 | EN 86, 96, 104, 148, 351–372; PT 72, 82, 90, 308 e código correspondente | Média; evidência insuficiente | “Nenhuma informação vital está faltando”, “não interferiu” e usar R/RStudio não demonstram integridade ou ausência de viés. Há valores ausentes nas estações e coordenadas; rankings usam `drop_na`, logo descrevem apenas registros com localização observada. | Registrar contagens e cobertura por grupo/tipo de bicicleta, limitar rankings ao subconjunto observado e declarar verificações efetivamente realizadas: duplicatas/IDs, datas, durações, tipos, arquivos e perdas. Não afirmar que a ausência é neutra sem teste. |
| B12 | EN 431 e 509; gráficos `unnamed-chunk-13-1.png` / `unnamed-chunk-16-1.png` | Média; rótulos incorretos confirmados no código, segundo gráfico inspecionado | A figura por hora usa média de duração, mas o título diz número de viagens. A figura mensal mostra meses, mas o eixo x diz “hour of the day”. | Corrigir título para duração média por hora e eixo mensal para mês. Regenerar as figuras por um procedimento rastreável; não editar apenas o código mantendo PNG antigo divergente. |

### Resultados que permanecem coerentes no registro

- Pico geral por hora às 17h, 18h e 16h, nessa ordem.
- Volumes por faixa do dia: tarde > noite > manhã > madrugada.
- Pico semanal geral no sábado e mínimo na segunda-feira; participação de fins de semana de 33,82% (o “33%” do texto perde precisão, mas a ordem está coerente).
- Casuais apresentam duração média e mediana maiores que membros no registro arquivado. O tamanho exato da diferença depende da métrica e do tratamento de extremos.

Essas concordâncias são verificações internas, sem confirmação dos CSVs originais ou de generalização para a operação atual.

## Redações propostas, ainda não aplicadas

### PT: resumo reconciliado com as saídas arquivadas

> O registro arquivado reúne 4.335.006 viagens após o filtro de duração estritamente superior a dois minutos, no período de julho de 2020 a junho de 2021. Dessas viagens, 56,46% pertencem à categoria de membros e 43,54% à de usuários casuais. As médias registradas são de 15,59 e 41,73 minutos, respectivamente; as medianas são de 11,13 e 19,70 minutos. Junho de 2021 apresenta o maior volume mensal nos dois grupos. Fins de semana concentram uma parcela maior das viagens casuais que das viagens de membros. Esses resultados descrevem viagens, não frequência de pessoas identificadas, e as médias precisam ser interpretadas diante das durações extremas registradas.

### EN: equivalent wording

> The archived record contains 4,335,006 trips after a strict duration filter of more than two minutes, covering July 2020 through June 2021. Member trips account for 56.46% and casual trips for 43.54%. The recorded mean durations are 15.59 and 41.73 minutes, respectively; the medians are 11.13 and 19.70 minutes. June 2021 has the highest monthly trip count in both groups. Weekends account for a larger share of casual trips than of member trips. These results describe trips rather than identified individuals' riding frequency, and the recorded extreme durations limit interpretation of the means.

### Limite para recomendações

PT: “Os padrões observados sugerem hipóteses de campanhas a serem avaliadas. A análise não mede a probabilidade de conversão, a frequência individual ou o efeito de descontos; essas decisões exigem dados adicionais e um desenho de avaliação.”

EN: “The observed patterns suggest campaign hypotheses for evaluation. This analysis does not measure conversion probability, individual riding frequency or the effect of discounts; those decisions require additional data and an evaluation design.”

## Ordem de correção recomendada

1. Decidir se o blog apresenta a análise histórica reconciliada ou uma nova versão do estudo. Não mesclar narrativas e métricas dos dois pipelines.
2. Na versão histórica, corrigir os trechos B01–B06 e B08/B10 em EN e PT de forma equivalente, indicando que os números vêm do registro arquivado.
3. Resolver a classificação de estações e o tratamento de durações extremas antes de renovar conclusões sazonais ou noturnas. A opção de recalcular exige nova trilha de evidência e atualização de tabelas/figuras.
4. Revisar limitações, fonte Divvy e rótulos gráficos; manter datas históricas e registrar a data da revisão separadamente.
5. Para usar o relatório atual como trabalho atualizado no portal, verificar sua execução com os dados completos, identificar a fonte efetivamente carregada e conferir métricas/tamanho de efeito/modelos. O simples funcionamento do fallback sintético não valida os resultados censitários do README.

## Verificações realizadas e limites

- Extração das frequências e da tabela de duração diretamente do Markdown congelado; todas as contagens marginais extraídas somam 4.335.006.
- Aritmética independente em Python padrão: percentuais, média ponderada a partir de médias de grupo já arredondadas e razão entre médias. Asserts confirmaram média ponderada arredondada em 26,97 e razão arredondada em 2,68.
- Inspeção visual de dois gráficos mensais e leitura dos trechos computacionais pertinentes. Não foi feita leitura pixel a pixel de todos os gráficos.
- Leitura do código remoto no commit fixado, sem executá-lo; não foi auditado todo o novo modelo inferencial do repositório.
- Não foram baixados os 12 CSVs de 2020/2021, não foi reexecutado R e não houve reprodução completa da análise. Nenhuma conclusão foi corrigida nos artigos nesta etapa.

## Fontes primárias externas

- [Repositório fornecido, versão fixada](https://github.com/talesgomes27/DAC8-Case-Study-1/tree/5c21b988e46548d7592245d1937cee0c8af6993c).
- [Divvy — System Data](https://divvybikes.com/system-data): documentação de campos de viagem e preparação dos dados disponibilizados. A página atual não substitui o manifesto dos arquivos históricos usados no blog.
- [NOAA/NCEI — Meteorological Versus Astronomical Seasons](https://www.ncei.noaa.gov/news/meteorological-versus-astronomical-seasons): meses das estações meteorológicas do hemisfério norte, usados para avaliar B07. Fonte consultada em 26/10/2026; não se transcrevem suas explicações integralmente.
