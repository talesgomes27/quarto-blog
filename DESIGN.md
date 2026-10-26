---
name: Portal de Tales Gomes
description: Portal editorial de projetos, textos e tecnologia, com temas claro e escuro e acento verde petróleo.
colors:
  ink: "#172f3f"
  muted: "#4c6170"
  accent: "#136c65"
  paper: "#eef5f1"
  rule: "#dce5e3"
  white: "#ffffff"
  accent-hover: "#094b46"
  code-background: "#f2f6f4"
  code-text: "#28574f"
dark-colors:
  canvas: "#12232e"
  ink: "#e4eeef"
  muted: "#adc1c9"
  accent: "#84d3bf"
  accent-hover: "#b1eadb"
  paper: "#1c3540"
  rule: "#405b66"
  code-text: "#a7ddcd"
  input-border: "#66828d"
typography:
  display:
    fontFamily: "Mukta Malar, sans-serif"
    fontSize: "clamp(2.5rem, 4.15vw, 4.1rem)"
    fontWeight: 700
    lineHeight: 1.12
    letterSpacing: "-.025em"
  body:
    fontFamily: "Mukta Malar, sans-serif"
    fontSize: "1.1rem"
    fontWeight: 400
  project-title:
    fontFamily: "Mukta Malar, sans-serif"
    fontSize: "2.05rem"
    fontWeight: 700
    lineHeight: 1.15
    letterSpacing: "-.025em"
  intro:
    fontFamily: "Mukta Malar, sans-serif"
    fontSize: "1.42rem"
    lineHeight: 1.4
rounded:
  image: "5px"
  button: "4px"
  focus: "2px"
spacing:
  section: "2rem"
  project-gap: "2.5rem"
  mobile-inline: "1.5rem"
components:
  button-primary:
    backgroundColor: "{colors.accent}"
    textColor: "{colors.white}"
    rounded: "{rounded.button}"
    padding: ".45rem 1.8rem"
  button-primary-hover:
    backgroundColor: "{colors.accent-hover}"
    textColor: "{colors.white}"
  text-link:
    textColor: "{colors.accent}"
  editorial-aside:
    backgroundColor: "{colors.paper}"
    padding: "2.85rem 2.85rem 1.8rem"
---

# Design System: Portal de Tales Gomes

## Overview

**Creative North Star: "Caderno de tecnologia"**

Portal claro de leitura e trabalho autoral, com tinta azul escura, verde petróleo e áreas verde pálido. A direção C aprovada combina uma apresentação curta, estudos com imagens e uma lateral editorial; a interface usa a mesma fonte humanista em títulos e texto.

O branco e os separadores finos dão estrutura. Fotografias sintéticas ilustram os temas da página inicial; gráficos e resultados dentro dos estudos continuam sendo conteúdo dos artigos. Português é o idioma principal e a navegação expõe PT e EN.

**Key Characteristics:**
- Tipografia humanista local, em pesos 400 e 700.
- Hierarquia por tamanho, espaço e separadores finos.
- Verde petróleo para ação e verde pálido para a lateral.

## Colors

O acento primário verde petróleo marca links, botão de contato, página ativa e foco. A tinta azul escura sustenta títulos e texto; a tinta suavizada atende descrições e metadados. Branco é o fundo principal, papel verde pálido distingue a lateral e a cor de linha separa navegação, estudos e rodapé. O código tem fundo claro e texto verde próprios, definidos no tema SCSS.

Os tokens acima são definidos em `styles.css`, `custom.scss` e `custom-dark.scss`. Seleção, barra de rolagem, divisória interna, separador de idiomas, fundo principal e texto de botão usam papéis semânticos no CSS.

### Tema escuro

O tema claro mantém a paleta aprovada. A variante escura usa um fundo azul profundo, superfícies editoriais azul-esverdeadas, tinta clara e acento verde mais luminoso. Mantém tipografia, composição, conteúdo e imagens originais. O texto dos botões muda para azul profundo sobre o acento claro; links, hover, foco, seleção e barras de rolagem seguem a variante ativa.

O Quarto compila duas variantes do tema `default`: `custom.scss` para claro e `custom-dark.scss` para escuro. O controle nativo da navbar alterna os temas e preserva a preferência de leitura entre páginas; a primeira opção configurada é a clara. A classe nativa `body.quarto-dark` ativa os tokens escuros. As variáveis SCSS adaptam componentes Bootstrap, tabelas, formulários, navegação, popovers e busca; o Giscus usa `light` e `dark_dimmed`, sincronizados pelo Quarto. Nenhum filtro de inversão é aplicado a imagens ou gráficos; figuras incorporadas podem preservar seus fundos claros.

## Typography

Mukta Malar é servida por dois arquivos TTF locais, com `font-display: swap`, para peso regular (400) e negrito (700); a alternativa é `sans-serif`. O corpo parte de (1.1rem), definido no tema Quarto. Títulos usam negrito e espaçamento ligeiramente fechado; os três primeiros níveis têm quebra equilibrada.

Na abertura, o título é fluido; a introdução tem largura máxima de (66ch). Títulos dos estudos usam (2.05rem), subtítulos (1.32rem), descrições (1.08rem) e metadados (1rem) no desktop amplo. A lateral usa títulos de (2.4rem) e texto de (1.14rem). A marca na navegação usa (2rem). As adaptações menores estão em Layout.

Metadados, código e tabelas usam números tabulares. Nos documentos fora da abertura, o conteúdo recebe entrelinha de (1.65); descrições do arquivo usam (1.5).

## Layout

A navbar nativa do Quarto é fixa, acompanha o tema ativo, tem seletor claro/escuro e busca em overlay e colapso abaixo de `lg`. Tem borda inferior fina, espaçamento vertical de (.6rem) e lateral de (3.9%). Os links PT e EN são explícitos; no desktop uma barra separa os idiomas. A página ativa recebe cor de acento e sublinhado.

A abertura tem largura máxima de (1600px), centrada, com colunas (2.2fr / 1fr); a lateral tem mínimo de (300px). A coluna principal usa padding (1.45rem 2.8rem 1.5rem 4.15vw); acima de (1600px), o padding esquerdo passa a (4rem). Cada estudo distribui imagem e texto em (.8fr / 1.04fr), separados por (2.5rem), com linha entre estudos. O contato centralizado fecha a abertura e limita o texto a (67ch).

- Até (1200px): padding principal de (2rem), lateral de (2.5rem 1.8rem), espaço entre imagem e texto de (1.5rem), colunas (.8fr / 1fr), título de estudo de (1.7rem) e imagem com altura de (16rem).
- Até (991px): a abertura passa a uma coluna; a lateral passa a duas colunas, com imagem ocupando ambas. O padding lateral da página é (1.5rem), a introdução passa a (1.25rem), o título principal usa `clamp(2.4rem, 6vw, 3.8rem)` e as imagens de estudo têm altura de (15rem). O menu recolhido remove a barra entre idiomas.
- Até (575px): cada estudo passa a imagem sobre texto, com espaço de (1rem); a imagem usa proporção (1.65) e altura automática. A lateral passa a uma coluna. O título principal fica em (2.65rem), títulos de estudo em (1.85rem), descrições em (1.13rem) e marca em (1.75rem).

O arquivo de textos mantém a listagem nativa Quarto com miniatura, título, descrição, data, categorias, filtro e ordenação. Os estudos usam a estrutura de leitura Quarto, com código, tabelas e figuras existentes; não recebem a composição de duas colunas da abertura.

## Elevation & Depth

A composição customizada é plana: fundos distintos e bordas de (1px) delimitam as regiões, sem sombras adicionadas. A profundidade vem das fotografias e do contraste de superfícies. Overlays de busca e lightbox continuam sob os estilos e comportamentos nativos do Quarto.

## Shapes

Imagens e miniaturas têm cantos suavizados; o botão é discretamente arredondado. A lista de estudos não recebe caixa própria: seus limites são espaço e separadores. As imagens da abertura usam recorte `object-fit: cover`; a imagem de leitura tem altura de (15rem) no desktop e margens que a ampliam dentro da lateral. Os pontos responsivos retiram essa ampliação.

## Components

### Navegação

Marca em negrito, links de (1.08rem), fundo do tema ativo e uma linha inferior. O estado ativo é verde e sublinhado; busca, botão de menu e ícones profissionais são fornecidos pelo Quarto. A navegação de idioma leva à versão equivalente por meio da localização implementada no projeto.

### Links de leitura

O link de ação é verde, negrito e não quebra internamente. Links adjacentes têm espaço de (1.7rem), reduzido a (.8rem) até (1200px). O título de estudo é um link na cor da tinta; no hover fica verde e sublinhado. Links gerais têm deslocamento de sublinhado de (.22em).

### Botão de contato

Um link com aparência de botão Quarto abre o endereço de contato. Usa fundo e borda de acento, texto branco no tema claro e azul profundo no escuro, com padding do token de componente. No hover, fundo e borda usam o acento de hover da variante ativa. Não há variante adicional customizada.

### Linha de estudo e lateral editorial

A linha de estudo agrupa imagem clicável, título, subtítulo, metadados, descrição e links. As três imagens WebP da abertura têm (1000px) de largura, são sintéticas e trazem texto alternativo que as identifica como ilustrativas; os arquivos JSON adjacentes registram sua proveniência. Elas não substituem as figuras de análise dos artigos. A imagem do estudo escurece levemente no hover, com transição de filtro de (.22s ease-out).

A lateral reúne seções editoriais, separador interno e imagem de leitura sobre papel verde. No mobile, preserva a sequência de leitura abaixo dos estudos. O rodapé recebe borda superior e texto suavizado.

### Foco e movimento

O foco visível global tem contorno de (3px), afastamento de (5px) e a cor de acento. A preferência `prefers-reduced-motion: reduce` remove transições e força rolagem automática. Não há animação de entrada customizada.

## Do's and Don'ts

### Do:
- Do manter a navegação Quarto e o acesso explícito a PT e EN.
- Do usar a paleta e a fonte locais já implementadas.
- Do preservar o foco visível e a preferência por movimento reduzido.
- Do identificar as imagens sintéticas como ilustrativas e preservar os gráficos dos estudos.

### Don't:
- Don't tratar fotografias ilustrativas como resultados das análises.
- Don't adicionar sombras ou cartões elevados ao padrão atual.
- Don't substituir o conteúdo e os resultados dos artigos ao aplicar o sistema visual.

### Página Sobre

Usa o modelo nativo `trestles` do Quarto, com retrato e links profissionais à esquerda e biografia à direita. No celular, os blocos ficam em sequência; os quatro links mantêm duas colunas e alvos de pelo menos 44px. O contato usa o papel verde do portal. As versões PT e EN compartilham estrutura e estilos, limitados à classe `profile-about`.

O retrato `assets/profile/tales-gomes.jpg` é a primeira fotografia fornecida pelo autor nesta revisão, preservada sem edição ou recorte do arquivo (SHA-256: `0d7eba1fe7ae5b38778fc55e8ddc09820d2b1c2a41da675707f534891aa7dc92`). O rosto sem óculos e o sorriso orientaram a escolha. A imagem original permanece na proporção 374 × 512.

Na preparação da publicação, o autor solicitou remover a marca Gemini. `tales-gomes-clean.png` é a edição usada nas duas páginas, feita com `image_gen` para remover somente a marca; a proveniência está no JSON adjacente e o arquivo original foi preservado.

### Arquivo de textos

`writing-archive` preserva a listagem, filtro textual, ordenação e categorias nativas do Quarto. O título usa a escala da abertura; linhas com fotografia à esquerda, texto e data à direita ficam separadas por linhas finas. Categorias ocupam uma lateral de papel verde no desktop e seguem os estudos no celular, onde a leitura começa pelo título e pelo filtro textual. O pós-processamento converte os controles de categoria em botões nativos e dá nome acessível ao filtro nos dois idiomas, preservando os handlers do Quarto.
