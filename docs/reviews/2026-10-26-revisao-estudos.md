# Revisão dos estudos antigos do blog

> Registro do diagnóstico anterior à correção. Para o estado atualizado dos artigos e a rastreabilidade das mudanças, consulte o [registro de correções](../revisions/2026-10-26/changes.md).

Revisão de 26/10/2026. Foram examinados os dois artigos e suas traduções, os resultados computacionais arquivados, o repositório Bike-share informado pelo autor e os dados/documentação de origem do Bellabeat. Os artigos, gráficos publicados e arquivos `_freeze/` não foram alterados nesta etapa.

## Resultado

O Bike-share apresenta divergências entre conclusões e resultados arquivados. O Bellabeat tem médias compatíveis com o processamento arquivado, mas precisa corrigir duplicações nas junções e limitar as interpretações de associações observadas. A conclusão sobre prevenção de doenças cardíacas não é sustentada por esse estudo.

| Prioridade | Estudo | Evidência | Encaminhamento |
| --- | --- | --- | --- |
| Alta | Bellabeat | Não há desfecho clínico nem desenho que identifique prevenção de doença cardíaca. | Retirar essa conclusão e explicitar o caráter exploratório e observacional. |
| Alta | Bike-share | A tabela arquivada apresenta médias de 15,593 e 41,72614 minutos para membros e casuais; a narrativa apresenta 14,71 e 36,15. A razão entre as médias da tabela é aproximadamente 2,68, não 2,45. | Reconciliar a prosa PT/EN com uma versão analítica identificada; não misturar números de versões diferentes. |
| Alta | Bike-share | Tipos de bicicleta, participação dos grupos e alguns rankings de meses/dias também divergem da narrativa. | Corrigir os trechos localizados no parecer específico, com denominadores explícitos de viagens. |
| Alta | Bellabeat | A atividade tem 940 registros de usuário-dia; três duplicatas exatas de sono se propagam pelas junções, produzindo 943 linhas. A junção posterior dos dados em formato longo amplia essa multiplicidade. | Definir e verificar a chave usuário-dia, resolver duplicatas e regenerar resultados afetados antes de substituir médias ou figuras. |
| Alta | Ambos | Viagens não equivalem a pessoas identificadas; dias repetidos da mesma pessoa não equivalem a participantes independentes. | Explicitar unidade de análise, cobertura e limites das recomendações. |
| Alta | Bike-share | Durações extremas chegam a aproximadamente 38,85 dias; a classificação de estações usa trimestres civis. | Documentar as decisões e fazer análise de sensibilidade antes de renovar conclusões sazonais e baseadas em médias. |
| Média | Bellabeat | Cobertura de sono, frequência cardíaca e peso é diferente; os dados são de usuários Fitbit, usados em um caso de estudo Bellabeat. | Corrigir a identificação da fonte e informar amostras efetivas por variável/gráfico, sem generalizar para clientes Bellabeat. |

Não foi determinada a causa histórica das divergências. A revisão não atribui intenção, fabricação ou validade geral dos dados a partir desses achados.

## Pareceres e correções propostas

- [Bike-share: achados localizados, evidências e redações PT/EN](2026-10-26-bike-share.md).
- [Bellabeat: achados localizados, verificações e redações PT/EN](2026-10-26-bellabeat.md).

Esses pareceres distinguem inconsistência demonstrada, limitação metodológica e questão que exige nova análise. As redações propostas ainda não substituem os artigos.

## O que foi efetivamente verificado

| Verificação | Bike-share | Bellabeat |
| --- | --- | --- |
| Código e narrativa publicados | Lidos e confrontados com tabelas arquivadas | Lidos e confrontados com tabelas/dados arquivados |
| Origem adicional fornecida | Repositório GitHub fixado em commit | Kaggle e arquivo original indicado no Zenodo |
| Conferência numérica | Frequências, rankings e aritmética das saídas arquivadas | Contagens e junções reproduzidas em Python com dados de origem; comparação com o registro arquivado |
| Reexecução integral em R | Não realizada | Não realizada |
| Traduções | 53 blocos de código/saída preservados em PT | 16 blocos de código/saída preservados em EN |
| Alterações nos artigos nesta revisão | Nenhuma | Nenhuma |

Os valores do Bike-share reconciliam o registro arquivado; não constituem reprodução dos CSVs originais. A versão recente do repositório mantém o mesmo período nominal, mas usa filtros e processamento diferentes e oferece uma alternativa sintética de execução. Não deve substituir automaticamente o estudo histórico.

No Bellabeat, a reprodução das junções e a concordância dos campos numéricos verificados sustentam a coerência entre os dados consultados e o processamento arquivado. Isso não demonstra causalidade, representatividade ou equivalência entre todos os arquivos do pacote Kaggle e os arquivos usados originalmente pelo autor.

## Ordem de atualização recomendada

1. Aplicar as correções editoriais demonstráveis em português e inglês: origem dos dados, unidade de análise, alcance das conclusões e números reconciliados com uma versão identificada.
2. Para o Bike-share, decidir explicitamente entre preservar o estudo histórico reconciliado ou apresentar uma versão atualizada baseada no repositório. Se atualizar, verificar a execução com dados completos e registrar filtros, perdas, tratamento dos extremos e origem efetiva dos dados.
3. Para o Bellabeat, corrigir as cardinalidades das junções, conferir cobertura por participante e variável e refazer tabelas e gráficos afetados. Usar frequências normalizadas ao comparar dias da semana e distinguir dias observados de pessoas.
4. Atualizar os resultados arquivados e suas traduções de forma coordenada. Revisar as figuras renderizadas, preservar a data original e registrar a revisão separadamente.

Não basta mudar a prosa sobre médias afetadas pela limpeza sem definir qual processamento passa a ser a referência. Também não basta alterar o código de um gráfico e manter a imagem antiga.

## Rastreabilidade

- [Manifesto de entradas e hashes SHA-256](evidence/input-manifest.json).
- [Verificação de preservação das entradas e blocos traduzidos](evidence/preservation-checks.json).
- [Evidência numérica Bike-share](evidence/bike-share-audit.json).
- [Evidência numérica Bellabeat](evidence/bellabeat-audit.json).
- [Repositório Bike-share no commit consultado](https://github.com/talesgomes27/DAC8-Case-Study-1/tree/5c21b988e46548d7592245d1937cee0c8af6993c).
- [Dataset Kaggle informado](https://www.kaggle.com/datasets/arashnic/fitbit).
- [Registro original Fitbit no Zenodo](https://zenodo.org/records/53894).

Não houve publicação, alteração no repositório externo ou substituição silenciosa de números. Dados brutos baixados para conferência ficaram fora do projeto; as evidências versionáveis registram apenas agregados e proveniência.
