# Extensões Quarto para o blog

Consulta em **26/10/2026**, com Quarto **1.10.19**. O [catálogo oficial](https://quarto.org/docs/extensions/) foi consultado nas quatro categorias: shortcodes/filtros, artigos de periódicos, formatos e Reveal.js. O índice reúne **263 extensões distintas em 278 entradas**, pois algumas aparecem em mais de uma categoria. Não é um inventário de todo o ecossistema.

## Buscar sem acessar o site

- [catalog.md](catalog.md): nomes, funcionalidades declaradas, autores e repositórios, agrupados por categoria.
- [catalog.json](catalog.json): o mesmo inventário estruturado, com data, URLs de origem, contagens e hashes das páginas consultadas.
- [installed.json](installed.json): origens fixadas e hashes das três extensões adotadas, incluindo adaptações locais.

As descrições do inventário mantêm o idioma do catálogo de origem. Para buscar por necessidade, comece pela tabela em português abaixo; depois consulte os detalhes da candidata no inventário.

```bash
rg -ni 'code|table|sql|python|diagram|citation|reading|navigation' docs/quarto-extensions/catalog.md
rg -ni 'código|tabela|interativo|leitura|referência' docs/quarto-extensions/README.md
```

## Escolhas para este blog

As prioridades são avaliações locais, baseadas nos posts existentes. A funcionalidade declarada no catálogo não prova compatibilidade ou qualidade. `remember`, `link-previews` e `cite-this` foram instaladas, renderizadas e verificadas neste portal.

| Necessidade | Candidata / fonte | Decisão e aplicação |
| --- | --- | --- |
| Retomar a leitura de um estudo longo | [remember](https://github.com/mcanouil/quarto-remember) | **Adotada** no Bike Share e Bellabeat, PT/EN. Versão 1.4.1, commit `200497b4fb8f3a4aff1150d48b359995bf4afae5`, Quarto >=1.9.37. Oferece continuar a última leitura com posição salva; usa armazenamento local no navegador. |
| Ampliar código largo | [code-fullscreen](https://github.com/shafayetShafee/code-fullscreen) | **Não adotada**, após leitura do JS/CSS no commit `10cf352cb69661723de1b84d1e10941aca77eae3`: controles dependem de hover, ausência de tratamento de Escape/foco no código consultado, fundo claro fixo e fonte de 1.5vw abaixo de 992px. Não compensa substituir os blocos atuais por esse comportamento. |
| Incluir código de arquivo sem duplicar | [include-code-files](https://github.com/quarto-ext/include-code-files) | **Recomendada para posts futuros** com arquivos locais de código que sejam a fonte vigente. Aceita arquivo e faixas de linhas. Não substituir os snapshots de código associados a resultados já importados por scripts de outra revisão. |
| Incluir arquivo com código recolhível | [add-code-files](https://github.com/shafayetShafee/add-code-files) | **Condicional**: alternativa à anterior quando a inclusão precisar trabalhar com `code-fold`. O README diferencia explicitamente as duas opções. |
| Conferir links externos | [linkrot](https://github.com/coatless-quarto/linkrot) | **Condicional** para uma revisão de links com rede disponível. O projeto declara estar em desenvolvimento e consulta destinos durante o render; não ativar globalmente no fluxo estático atual. Timeout/bloqueio de robô exige interpretação, não remoção automática da fonte. |
| Modo de leitura sem navegação | [focus-mode](https://github.com/lsbjordao/quarto-focus-mode) | **Não adotada no layout atual**: o README exige navegação por sidebar para websites e desativa o recurso em dispositivos de toque. O blog usa navbar; o sumário do artigo não é a sidebar de navegação exigida. |
| Código R/Python executável pelo leitor | [quarto-live](https://github.com/r-wasm/quarto-live), [webr](https://github.com/coatless/quarto-webr), [pyodide](https://github.com/coatless-quarto/pyodide), [shinylive](https://github.com/quarto-ext/shinylive) | **Condicionais a novos tutoriais/demonstrações**: verificar no repositório a opção exata encontrada no catálogo. Avaliar dependências de navegador, downloads e tempo de carregamento. Não transformar o render dos estudos arquivados em uma reexecução da análise. |
| Exercícios e aprendizado interativo | `quizdown`, `shortiquiz`, `stepbystep` | **Condicionais** a posts didáticos que tenham perguntas ou etapas reais. Localizar instruções e controles em PT/EN antes do uso. Repositórios no catálogo local. |
| SQL interativo | `interactive-sql` | **Condicional** a um tutorial com banco demonstrativo publicável. Conferir o que será incluído no HTML antes de disponibilizar dados. |
| Diagramas e algoritmos | `diagram-zoom`, `pseudocode`, `d2`, `livefigures`, `study-flow` | **Condicionais** ao assunto do post. Mermaid/Graphviz nativos vêm primeiro quando atenderem. Verificar ferramentas de render e eventuais serviços externos na candidata. |
| Tabelas com células mescladas ou estrutura especial | `quartable`, `table-cell-merge` | **Condicionais** a tabelas que exijam esses recursos. As tabelas atuais já usam região rolável com foco de teclado. |
| Como citar e bibliografia por seção | `cite-this`, `section-biblios`, `bibentry` | **cite-this adotada** nos quatro estudos para copiar citação ABNT/APA ou baixar BibTeX. As outras continuam condicionais ao documento. Não inserir DOI ou metadados bibliográficos não fornecidos. |
| Ícones e identificação de linguagem | `bsicons`, `fontawesome`, `language-name`, `language-cell-decorator` | **Condicionais** quando ajudarem a reconhecer ações ou distinguir linguagens. Preservar nomes acessíveis; evitar ícones apenas decorativos. |
| Inserir PDF, mídia ou galeria | `embedpdf`, `social-embeds`, `static-photo-gallery` | **Condicionais** a conteúdo que precise ser consultado dentro do post; conferir formatos e serviços exigidos. |
| Formatos de periódicos e apresentações | Categorias `journal-articles`, `custom-formats` e `revealjs` | **Consulta futura** para exportações ou slides. Não mudar o formato HTML do portal apenas porque existe um template de outro destino. |

Nas linhas com nomes sem link, procure o nome em `catalog.md`: cada entrada aponta para o repositório declarado na listagem oficial. A instalação não é automática.

## Melhorias para o blog como um todo

Aplicação concluída em 26/10/2026, após consulta aos READMEs e aos arquivos executados pelas candidatas.

| Prioridade | Recurso | Ganho para o portal e limite |
| --- | --- | --- |
| Navegação | [link-previews](https://github.com/ravila4/quarto-link-previews) | **Adotada no portal**, versão 0.3.1, commit `e646ac114bcdce4535d807dc1a7920d8d9a26cfe`. Prévias de páginas internas reutilizam o Tippy do Quarto e os temas existentes. Conteúdo restrito ao título e introdução; estados de carregamento/indisponibilidade localizados. Exige Quarto >=1.8.27. É desativada sem ponteiro preciso/hover; o leitor continua usando links normais. Links simples recebem prévia por foco; grupos de cards do pacote usam apenas hover. |
| Divulgação dos textos | [social-share](https://github.com/schochastics/quarto-social-share) | **Funcionalidade implementada com links HTML**, sem instalar o pacote. LinkedIn e e-mail, com título e endereço exato de cada tradução, são suficientes. A fonte consultada do pacote acrescenta uma coleção Font Awesome e botões apenas com ícones; a implementação local usa rótulos de texto, ícones Bootstrap já incluídos no site e o CSS existente. Ícones são decorativos para leitores de tela. Os destinos abrem somente por ação do leitor. |
| Reuso acadêmico/profissional | [cite-this](https://github.com/lsbjordao/quarto-cite-this) | **Adotada nos quatro estudos**, versão 1.0.4, commit `0525fbfaff1a27c293cc5f7b80755e6c2f478ec4`. Controle recolhível ao final do artigo: citação ABNT/APA, cópia e download `.bib`, interface PT/EN. Mantém autor, datas e endereços dos estudos; sem DOI inventado. |
| Manutenção editorial | [linkrot](https://github.com/coatless-quarto/linkrot) | Verificação de links externos em uma rodada de manutenção de todo o conteúdo. Continuar como tarefa separada do render estático normal: consulta rede, o projeto se declara em desenvolvimento e bloqueios/timeout exigem interpretação. |

O [RSS nativo das listagens](https://quarto.org/docs/websites/website-listings.html#feeds) também foi ativado: `textos.xml` em PT e `en/textos.xml` em EN, com resumos e apenas os estudos publicados de cada idioma. Há links visíveis no arquivo e rodapé e descoberta automática no HTML. Não depende de extensão.

[Respeitar a preferência de tema do sistema](https://quarto.org/docs/output-formats/html-themes.html#dark-mode), com `respect-user-color-scheme: true`, permanece uma opção não ativada. A alternância e a preferência já salvas foram preservadas. A extensão `auto-dark` não é indicada para este portal: seu README recomenda um único tema claro e desaconselha a alternância light/dark que já utilizamos.

## Integração e validação do portal

`link-previews` é configurada em `_quarto.yml`. `cite-this` é ativada explicitamente no YAML dos quatro artigos, com escopo `page`, posição `inline`, estilos ABNT/APA e URL publicada completa da tradução. Cada artigo termina com o shortcode `cite-this page collapsed=true`. Ao criar outro post, preencher a configuração completa: o bloco aninhado da página pode substituir opções herdadas. `scripts/localize.py` gera compartilhamento e descoberta RSS para os pares de páginas registrados, preservando a transformação idempotente.

Adaptação necessária em `cite-this.lua`: restaurar `_G.PANDOC_SCRIPT_FILE` depois de coletar os metadados, inclusive em caso de erro. A fonte original deixava a variável alterada e impedia o lightbox nativo de resolver seus arquivos. Licenças MIT dos pacotes e licença original dos estilos CSL foram preservadas; hashes e diferenças estão em `installed.json`.

Validação local: render completo das 13 páginas e cinco verificações Python aprovadas (idiomas/idempotência, estudos, inventário/hashes e recursos do blog). No navegador, prévias PT/EN acompanharam os temas claro/escuro; citação exibiu somente o artigo e os dois estilos, com cópia confirmada pela interface e download BibTeX conferido. Em viewport de 375px, citação e compartilhamento não transbordaram, os botões mantiveram 44px e as abas responderam ao teclado. Os dois feeds foram conferidos por idioma e destino. Código e resultados das análises foram preservados, sem reexecução.

Limites: a confirmação de cópia veio da interface, sem leitura independente do clipboard do sistema. Não houve envio de e-mail/LinkedIn nem teste em aparelho físico. A revisão das dependências foi dirigida à integração; não é uma auditoria de segurança completa. A extensão de citação ainda emite um aviso sobre a ausência de autor de `work`, escopo que não é exibido nem usado no portal.

Publicação conferida no commit `3c769511dceef66221d06511b0dda7b578c3d90f`, workflow [40336453500](https://github.com/talesgomes27/quarto-blog/actions/runs/40336453500) concluído com sucesso. Os 24 destinos públicos consultados corresponderam byte a byte ao artefato local; hashes em [extensions-smoke-2026-10-26.json](../extensions-smoke-2026-10-26.json). Prévia da home e painel de citação do Bike Share em português também foram conferidos no navegador público.

## Recursos que o blog já tem

- **Lightbox**: `lightbox: true` já é um recurso nativo do Quarto instalado. A pasta legada `_extensions/quarto-ext/lightbox` 0.1.1 continua presente; ela não precisa ser reativada ou duplicada. A renderização anterior já advertia sobre a incorporação ao Quarto.
- **Tema claro/escuro**: a alternância nativa já está configurada. `auto-dark` não é necessária para reproduzir esse recurso.
- **Código recolhível**: há `code-fold` e/ou blocos `<details>` nos artigos. Uma extensão só se justifica se resolver um requisito além disso.
- **Sumário, busca, categorias, referências cruzadas e navegação PT/EN**: preservar os mecanismos existentes, em vez de instalar uma segunda implementação para a mesma função.

## Orientação permanente

Ao criar ou revisar um post, consultar este guia e o índice local. **Quando uma extensão for útil ao post, utilizá-la**, escolhendo pelo benefício concreto para o leitor ou para a autoria. Quando o recurso nativo já atender, usá-lo.

Para aplicar uma candidata:

1. Conferir README, licença, arquivos que serão executados, requisitos do Quarto e dependências da versão escolhida. A listagem é descoberta, não homologação.
2. Fixar versão ou commit; guardar a extensão no repositório com sua licença e registrar origem/adaptações. Ativar no YAML do post, mantendo o escopo necessário.
3. Renderizar sem alterar a política de execução da análise. Conferir PT/EN, temas, celular, teclado, links/recursos e testes existentes; verificar que resultados e código preservado não foram modificados.

## Remember: implantação local

Ativada pelo filtro `remember` nos quatro artigos, sem adicionar o filtro à home, ao arquivo, à 404 ou ao rascunho Netflix/Amazon. As dependências Lua já vêm no pacote; nada é instalado globalmente. Licenças MIT preservadas.

O JavaScript recebeu apenas textos em português para o aviso e seus botões, selecionados pelo `lang` da página. A interface inglesa original foi mantida. `styles.css` aplica as cores existentes do blog ao aviso. Os hashes originais e instalados estão em `installed.json`.

Limites observados no código de origem: uma única posição é armazenada por origem e comparada com o pathname; a leitura de outro artigo pode substituir a posição anterior. PT e EN têm caminhos distintos e não compartilham progresso de tradução. O recurso depende de armazenamento do navegador e fica indisponível quando ele não puder ser usado. Não é sincronização entre dispositivos.

Validação local concluída em 26/10/2026: render completo das 13 páginas; filtro presente nos quatro estudos e ausente da home/arquivo/404; testes dos estudos e navegação preservados; hashes dos arquivos instalados conferidos. No navegador, aceitar retomou a seção salva do Bike Share; Tab percorreu os dois botões em ciclo; Escape fechou o aviso; começar do início no Bellabeat EN fechou o aviso e manteve a página no topo. O aviso em português foi conferido em desktop claro e celular de 375px em tema escuro, sem transbordamento. As análises não foram reexecutadas. Esta é uma validação funcional dirigida, não uma auditoria de segurança completa da dependência.

## Atualizar o índice

```bash
python3 tests/test_quarto_extensions.py
python3 scripts/update_quarto_extensions.py
```

O segundo comando requer rede, baixa apenas as quatro listagens oficiais e regenera `catalog.json`/`catalog.md`. Não instala nem executa extensões. Erro de rede ou listagem vazia/incompatível interrompe a coleta antes de substituir o índice existente. Conferir o diff de data, contagens e entradas após atualizar. A curadoria deste README é manual: atualizar o inventário não homologa novas extensões nem muda decisões registradas.

Consultar o índice primeiro. Voltar à fonte da candidata para instalar/atualizar ou quando o recurso procurado não estiver coberto; reconsultar as quatro páginas somente quando for necessário renovar o catálogo.
