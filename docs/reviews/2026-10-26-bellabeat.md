# Revisão do estudo Bellabeat — 26/10/2026

> Registro do diagnóstico anterior à correção. Para o estado atualizado dos artigos e a rastreabilidade das mudanças, consulte o [registro de correções](../revisions/2026-10-26/changes.md).

O estudo pode ser mantido como análise exploratória histórica, mas precisa de correções metodológicas e de redação antes de sustentar conclusões sobre saúde ou clientes Bellabeat. As médias publicadas são reproduzíveis a partir da tabela arquivada de 943 linhas; o problema central está na duplicação de observações, nos denominadores e na força das interpretações.

Esta revisão preserva os artigos e o `_freeze`. Não é uma reescrita, uma validação clínica ou uma reexecução do pipeline R.

## Evidência e método

- Artigo original: `posts/bellabeat/index.qmd`, 526 linhas; tradução: `posts/bellabeat/en.qmd`.
- Resultado publicado: `_freeze/posts/bellabeat/index/execute-results/html.json`. Seu Markdown contém a tabela `daily_data` completa em um JSON de pagedtable, que permite conferir as 943 linhas sem executar R.
- Fonte indicada pelo usuário: [FitBit Fitness Tracker Data, Kaggle](https://www.kaggle.com/datasets/arashnic/fitbit). A ficha aponta para o registro original [Furberg, Brinton, Keating e Ortiz, Zenodo, DOI 10.5281/zenodo.53894](https://zenodo.org/records/53894). A descrição do registro declara 30 participantes recrutados por Amazon Mechanical Turk; isso não deve ser silenciosamente substituído pela contagem de IDs nos CSVs.
- Arquivo original conferido: [segunda parcela, 12/04 a 12/05/2016](https://zenodo.org/records/53894/files/mturkfitbit_export_4.12.16-5.12.16.zip), 25.291.915 bytes. MD5 `7afbecdce29814e1be2e9a7c94f8f165`, igual ao publicado pelo Zenodo; SHA-256 `4741dfabd18453de19b6dd0a7204e8fea6e45e70bc9ddbe396956c8e4fde02f8`.
- Definições de campos: [Fitabase Data Dictionary, atualização indicada no documento de 02/05/2018](https://www.fitabase.com/media/1748/fitabasedatadictionary.pdf). O documento define `TotalDistance` em quilômetros e `Calories` como gasto energético total estimado em quilocalorias. Não define esse campo como calorias exclusivamente de exercício.
- Conferência independente em Python padrão, sem pacotes adicionais: `scripts/audit_bellabeat.py`. Saída agregada: `docs/reviews/evidence/bellabeat-audit.json`. Nenhuma linha individual ou ID original é gravado nesse resultado.

O ZIP do Zenodo é uma fonte upstream verificável, não uma prova de identidade binária com o antigo download local do Kaggle, que não está no checkout. Contudo, a reconstrução dos três `left_join` produziu 943 linhas e encontrou correspondência para todas elas no snapshot em sete campos numéricos, com tolerância absoluta de `1e-5`. Essa correspondência sustenta as verificações descritas, sem certificar o ambiente R inteiro ou todos os gráficos.

## Dados observados

| Tabela upstream | Linhas | IDs distintos | Pares ID/data | Observação |
| --- | ---: | ---: | ---: | --- |
| Atividade diária | 940 | 33 | 940 | Sem duplicatas exatas |
| Sono | 413 | 24 | 410 | Três linhas duplicadas exatas |
| Frequência cardíaca | 2.483.658 | 14 | 334 | Agregada em média por ID/data |
| Peso/IMC | 67 | 8 | 67 | Cobertura muito menor que a atividade |

O período observado nessas quatro tabelas e no snapshot é 12/04/2016 a 12/05/2016. A referência a 18 arquivos deve ser contextualizada como o recorte usado; o registro upstream contém duas parcelas mensais. O número de tabelas da ficha atual do Kaggle não prova qual pacote foi baixado em 2021.

| Variável no snapshot | Observações não ausentes | IDs distintos | Média arquivada recalculada |
| --- | ---: | ---: | ---: |
| Passos/dia | 943 | 33 | 7.652,1888 |
| Distância total, km/dia | 943 | 33 | 5,5029 |
| Gasto energético estimado, kcal/dia | 943 | 33 | 2.307,5080 |
| Média diária dos registros de FC, bpm | 335 | 14 | 78,5616 |
| IMC | 67 | 8 | 25,1852 |
| Sono, horas/dia | 413 | 24 | 6,9911 |
| Minutos sedentários convertidos para horas/dia | 943 | 33 | 16,5059 |

Essas médias usam registros disponíveis, não a média com peso igual de 33 pessoas. Duas pessoas contribuem com 54 dos 67 registros de IMC. A FC é média aritmética de medições coletadas em horários variáveis durante o dia; não é uma medida de frequência cardíaca de repouso.

## Achados e correções propostas

| ID | Gravidade e status | Localização | Evidência e efeito | Correção proposta |
| --- | --- | --- | --- | --- |
| BE-01 | Alta — conclusão não sustentada | PT linha 484; EN linha 800 | A frase sobre prevenir doenças cardíacas excede os dados. Não há diagnóstico, incidência de doença, intervenção ou controle de confundidores nas quatro tabelas usadas. O boxplot compara FC média diária observada, não risco clínico ou FC de repouso. | Retirar a alegação preventiva e restringir a conclusão à associação descritiva nesta amostra. |
| BE-02 | Alta — duplicação confirmada | PT linhas 64–73 e 134–155; propagação nas linhas 289–293 | O sono upstream tem três duplicatas exatas. Sem deduplicação, os `left_join` geram 943 linhas para 940 pares ID/data. O `right_join` entre duas versões longas, ambas derivadas dessa tabela, multiplica as chaves repetidas: o código implica 3.796 linhas longas, contra 3.760 com uma linha por ID/data e quatro intensidades. A multiplicação muda os pesos de dias e pontos nos gráficos. | Definir a chave de cada tabela, remover duplicatas exatas de sono antes da junção, verificar unicidade de ID/data e construir a tabela longa sem uma junção muitos-para-muitos. Recalcular tabelas/gráficos em uma versão corrigida separada antes de substituir resultados publicados. |
| BE-03 | Alta — comparação de dias inadequada | PT linhas 301 e 303–331 | `geom_col` soma todas as observações por dia da semana. Terça, quarta e quinta aparecem cinco vezes no intervalo; os demais dias aparecem quatro vezes, com números distintos de registros. Totais mais altos não demonstram maior atividade típica nesses dias. | Mostrar média ou distribuição por participante-dia e informar denominadores; usar média por pessoa ou modelo de medidas repetidas conforme a pergunta. |
| BE-04 | Alta — extrapolação da população | PT linhas 3 e 15; EN linha 27 | Fitbit não é um produto Bellabeat. A descrição upstream fala em 30 participantes, enquanto atividade tem 33 IDs. Sono, FC e IMC têm coberturas diferentes. Não há sexo/idade ou identificação de clientes Bellabeat nas quatro tabelas usadas. | Corrigir a atribuição da marca e distinguir contexto comercial Bellabeat de dados Fitbit. Informar IDs observados por tabela e a divergência documental 30/33, sem afirmar sua causa. Limitar a generalização. |
| BE-05 | Alta — associação tratada como mecanismo causal | PT linhas 453, 484, 520–526; EN linhas 759, 800, 838–844 | As relações sono/calorias e sono/FC são observacionais, com vários dias por pessoa e sem ajuste por composição dos grupos, atividade, ausência de dados ou outras características. Os intervalos padrão de `geom_smooth(method='lm')` não incorporam a dependência entre dias de uma mesma pessoa. | Usar linguagem associativa. Separar variação dentro da pessoa e entre pessoas antes de sugerir mecanismo. Não interpretar sono como causa de redução de gasto energético. |
| BE-06 | Média — denominadores omitidos | PT linhas 200–216 | IMC usa 67 registros de oito IDs, FC 335 de 14 e sono 413 de 24. A expressão genérica “usuários” faz parecer que todas as médias abrangem 33 pessoas com peso igual. | Acrescentar n de registros e IDs em cada resumo, proporção ausente e regra de ponderação; considerar resumo por pessoa como análise de sensibilidade. |
| BE-07 | Média — variável e título não correspondem | PT linhas 340–353 | O gráfico usa `x=activities_time` e `y=activities_dist`, mas o título diz relação da distância com “total de calorias gastas”. | Corrigir o título para distância versus tempo por intensidade. Isso é uma correção de rotulagem; não autoriza inventar um resultado calórico. |
| BE-08 | Média — semântica de medidas precisa ser explícita | PT linhas 202, 206, 364–389 | O resumo trata `total_distance` como distância “ativa”; `Calories` é gasto total estimado, não energia de exercício isolada. Distância e tempo de intensidade, passos e calorias vêm do mesmo sistema de estimação, o que limita leituras como validação independente. | Nomear “distância total registrada” e “gasto energético total estimado (kcal)”; descrever associações sem atribuir toda variação à atividade ou ao sono. |
| BE-09 | Média — grupos pequenos e medidas repetidas | PT linhas 419–449, 458–505 | O grupo sono >10h tem 18 registros de 12 IDs; a comparação sono/FC nesse grupo tem apenas nove registros de cinco IDs. Nos outros grupos, participantes podem aparecer em mais de uma faixa em dias diferentes. | Informar registros e IDs por faixa e por variável. Não tratar as faixas como três grupos independentes de pessoas; marcar o resultado como exploratório. |
| BE-10 | Baixa — rótulo perde significado no processamento | PT linha 436 | `total_time_in_bed` passa a armazenar horas na cama menos horas dormidas, embora mantenha o nome de tempo total. No código atual essa coluna participa de `drop_na`, mas não é o eixo do gráfico de sono/calorias. | Criar `awake_time_in_bed` em vez de sobrescrever a coluna. Não atribuir a esse problema um efeito numérico sobre os gráficos que não usam essa variável. |

### Sensibilidade à deduplicação, sem substituir o arquivo histórico

Remover apenas as três linhas exatamente repetidas da tabela arquivada muda a média de passos de 7.652,19 para 7.637,91 e o gasto estimado de 2.307,51 para 2.303,61 kcal/dia. A média de sono passa de 6,9911 para 6,9862 horas. Portanto os valores publicados não devem ser chamados de inventados: são compatíveis com a tabela publicada, mas carregam o peso extra das duplicatas.

A distância média por participante-dia, após essa deduplicação exata, é aproximadamente 5,855 km no sábado e 5,832 km na terça; os números não sustentam “terça, quarta e quinta são os dias mais ativos” como uma comparação de médias. Essa é uma sensibilidade descritiva; não constitui teste estatístico nem resolve diferenças entre participantes.

### Sono e frequência cardíaca: o que os registros permitem dizer

| Faixa de sono | Registros com sono | IDs com sono | Registros com sono e FC | IDs com sono e FC | FC média diária, bpm |
| --- | ---: | ---: | ---: | ---: | ---: |
| <6h | 100 | 22 | 31 | 10 | 76,9598 |
| 6–10h, inclusive | 295 | 20 | 142 | 10 | 73,2467 |
| >10h | 18 | 12 | 9 | 5 | 67,9099 |

Contagens reproduzidas do snapshot com duplicatas preservadas, para refletir a análise histórica. O sentido da diferença descritiva entre <6h e 6–10h está presente; a conclusão preventiva não decorre dessa diferença. Não foram calculados intervalos ou p-valores que fingissem independência entre registros.

## Redações PT/EN propostas

**Origem e população — PT:** “Este estudo de caso usa registros Fitbit no contexto de um exercício de análise para Bellabeat. O arquivo de atividade diária contém 33 identificadores distintos, enquanto a descrição original do dataset declara 30 participantes; a diferença não foi esclarecida. O recorte observado vai de 12 de abril a 12 de maio de 2016, e a cobertura varia entre atividade, sono, frequência cardíaca e peso.”

**Origin and population — EN:** “This case study uses Fitbit records in the context of a Bellabeat analytics exercise. The daily activity file contains 33 distinct identifiers, whereas the original dataset description reports 30 participants; this difference remains unresolved. The observed period is April 12 to May 12, 2016, and coverage differs across activity, sleep, heart rate and weight.”

**Sono e FC — PT:** “Nos registros com sono e frequência cardíaca disponíveis, a FC média diária observada foi maior na faixa de sono inferior a seis horas do que na faixa de seis a dez horas. A comparação é exploratória, reúne medidas repetidas das mesmas pessoas e não demonstra que aumentar o sono previna doenças cardíacas.”

**Sleep and heart rate — EN:** “Among records with both sleep and heart-rate data, observed mean daily heart rate was higher for sleep durations below six hours than for durations from six to ten hours. This exploratory comparison includes repeated measurements of the same people and does not establish that increasing sleep prevents heart disease.”

**Dias da semana — PT:** “Os totais acumulados diferem por dia da semana, mas o intervalo contém cinco terças, quartas e quintas e quatro ocorrências dos demais dias. É necessário normalizar pela cobertura de participantes-dias antes de comparar atividade típica.”

**Weekdays — EN:** “Accumulated totals differ by weekday, but the period includes five Tuesdays, Wednesdays and Thursdays and four occurrences of each other weekday. Participant-day coverage must be accounted for before comparing typical activity.”

## Reproduzir esta revisão

```bash
# Recalcula as verificações do snapshot já versionado.
python3 scripts/audit_bellabeat.py

# Com a cópia local do ZIP original previamente baixado, verifica MD5,
# reconstrói os left joins e confere sete campos contra o snapshot.
python3 scripts/audit_bellabeat.py --source-zip /tmp/bellabeat-source-2016.zip
```

O primeiro comando gera somente a parte arquivada; para conservar também a validação upstream no JSON, execute o segundo por último. O script não faz download, não executa R nem grava dados individuais. O ZIP ficou em `/tmp`, fora dos arquivos versionados. A descarga levou cerca de um minuto; foram percorridas 2.483.658 medições de FC em streaming para agregação por dia, sem carregar a tabela de FC inteira na memória.

A correção editorial da marca, dos rótulos e do alcance das conclusões já tem fundamento. Corrigir a série publicada de resultados e gráficos exige uma versão analítica corrigida, com política de deduplicação, chaves de junção verificadas e reconciliação explícita entre os artigos PT/EN e o `_freeze`.
