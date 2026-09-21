# Advertising Product Analytics

## 🚀 Dashboard interativo

Explore o dashboard publicado no Streamlit:

👉 **[Acessar o dashboard](https://advertising-appuct-analytics-de3qrpwpyzwgfjyyjqvjft.streamlit.app/)**

> Projeto de portfólio com dados educacionais e fictícios, desenvolvido para analisar desempenho de campanhas, eficiência de produtos publicitários, ocupação de inventário e geração de receita.

**Projeto autoral | Dados educacionais e fictícios**

---

## Sobre o projeto

Este projeto simula uma análise de dados aplicada a produtos de publicidade digital, com foco em entender como dados de campanhas, anunciantes e inventário publicitário podem apoiar a avaliação de **desempenho, eficiência, ocupação e geração de receita** dos diferentes formatos de produto.

A análise combina conhecimentos de **Publicidade e Propaganda, Marketing, Customer Experience e Data Analytics**, utilizando SQL para exploração e agregação dos dados, Python e Pandas para análise e cálculo de indicadores, e Streamlit para construção do dashboard interativo.

O projeto foi desenvolvido como case de portfólio e utiliza dados **educacionais e fictícios**, sem representar dados reais ou confidenciais de empresas.

---

## Problema de negócio

Produtos de publicidade digital possuem diferentes formatos, modelos de precificação e características de entrega. Para avaliar seu desempenho, é necessário combinar indicadores de campanhas com informações de inventário e monetização.

A principal pergunta deste projeto é:

> **Como os dados de campanhas, anunciantes e inventário publicitário podem apoiar decisões sobre desempenho e eficiência dos produtos?**

A partir dessa pergunta, a análise busca identificar diferenças de desempenho entre os produtos, avaliar indicadores de interação e conversão, analisar a ocupação do inventário e relacionar investimento, receita e eficiência de monetização.

## Objetivo

Construir uma análise exploratória de produtos publicitários a partir de dados de campanhas, anunciantes e inventário, transformando os dados em indicadores que permitam avaliar:

- desempenho de campanhas;
- eficiência de interação e conversão;
- ocupação do inventário publicitário;
- geração e participação da receita;
- relação entre investimento e monetização;
- diferenças de desempenho entre produtos e períodos.

O objetivo é demonstrar como uma abordagem orientada a dados pode transformar informações operacionais em **indicadores e insights de apoio à tomada de decisão**.

---

## Modelagem dos dados

O banco de dados foi estruturado em quatro tabelas principais:

### Products

Cadastro dos produtos publicitários.

Principais campos:

* `product_id`
* `product_name`
* `format`
* `pricing_model`

### Advertisers

Cadastro dos anunciantes.

Principais campos:

* `advertisers_id`
* `advertisers_name`
* `industry`

### Campaigns

Dados de desempenho das campanhas.

Principais campos:

* `campaign_id`
* `advertisers_id`
* `product_id`
* `date`
* `investment`
* `impressions`
* `clicks`
* `conversions`

### Inventory

Dados simplificados de disponibilidade, venda e receita do inventário.

Principais campos:

* `inventory_id`
* `date`
* `product_id`
* `available_impressions`
* `sold_impressions`
* `revenue`

As tabelas são relacionadas por identificadores de anunciantes e produtos, permitindo cruzar informações de campanhas e inventário.

---

## Produtos analisados

A base educacional contém quatro produtos publicitários:

| Produto                  | Formato | Modelo de precificação |
| ------------------------ | ------- | ---------------------- |
| Vídeo Pre-roll           | Vídeo   | CPM                    |
| Vídeo Mid-roll           | Vídeo   | CPM                    |
| Display Banner           | Display | CPM                    |
| Native Sponsored Content | Native  | CPC                    |

---

## Indicadores analisados

### Campanhas

**CTR — Click-Through Rate**

Mede a proporção de impressões que resultaram em cliques.

`CTR = cliques / impressões × 100`

**CPC — Custo por Clique**

Mede o investimento médio necessário para gerar um clique.

`CPC = investimento / cliques`

**Taxa de conversão**

Mede a proporção de cliques que resultaram em conversões.

`Taxa de conversão = conversões / cliques × 100`

**Custo por conversão**

Mede o investimento médio associado a cada conversão.

`Custo por conversão = investimento / conversões`

### Inventário

**Ocupação do inventário**

Mede a proporção do inventário disponível que foi vendido.

`Ocupação = impressões vendidas / impressões disponíveis × 100`

**CPM de receita**

Mede a receita gerada a cada mil impressões vendidas.

`CPM de receita = receita / impressões vendidas × 1000`

### Monetização

Também foi calculada a relação:

`Receita / Investimento`

Esse indicador compara a receita registrada no inventário com o investimento das campanhas.

Ele **não é tratado como ROAS**, pois a base educacional não estabelece atribuição direta entre o investimento de uma campanha e a receita específica do inventário.

---

## Análises realizadas

As análises foram desenvolvidas em SQL e posteriormente utilizadas como base para a exploração em Python e para o dashboard.

Entre as análises realizadas estão:

* desempenho por produto;
* CTR por produto;
* CPC por produto;
* taxa de conversão;
* custo por conversão;
* desempenho por anunciante;
* combinação anunciante × produto;
* evolução mensal dos indicadores;
* participação do investimento;
* participação das conversões;
* participação da receita;
* ocupação do inventário;
* receita por produto;
* CPM de receita;
* relação entre receita e investimento;
* verificações de qualidade dos dados.

Também foram realizados testes de consistência para identificar possíveis problemas, como:

* cliques superiores às impressões;
* conversões superiores aos cliques;
* valores negativos;
* produtos inexistentes;
* anunciantes inexistentes.

---

## Principais insights

A análise da base demonstrou diferenças de desempenho e monetização entre os produtos avaliados.

- **Native** apresentou o maior CTR (2,50%) e a maior taxa de conversão (4,22%), além do menor CPC (R$ 2,00) e menor custo por conversão (R$ 47,37) entre os produtos analisados.
- **Vídeo** apresentou a maior receita total (R$ 162 mil) e o maior CPM de receita (R$ 60,00).
- **Display** apresentou menor eficiência nos indicadores de interação e conversão quando comparado aos demais produtos da base.
- O **Native** apresentou participação nas conversões superior à sua participação no investimento, enquanto o **Display** apresentou comportamento inverso.
- A ocupação total do inventário analisado foi de **81,82%**, considerando 7,2 milhões de impressões vendidas de um total de 8,8 milhões disponíveis.

Os resultados representam o comportamento observado na base educacional utilizada e não devem ser interpretados como recomendações universais de alocação ou desempenho de produtos.

---

## Dashboard

O projeto possui um dashboard desenvolvido em **Streamlit**, permitindo visualizar os principais indicadores de campanhas e inventário em uma única interface.

O painel apresenta:

* visão geral dos investimentos e resultados;
* desempenho dos produtos;
* eficiência de conversão;
* indicadores de inventário;
* receita e monetização;
* comparação entre investimento e receita;
* eficiência de monetização;
* indicadores detalhados de campanha;
* indicadores detalhados de inventário;
* participação na receita e no investimento;
* principais insights analíticos.

---

## Tecnologias utilizadas

* **SQL**

  * consultas;
  * agregações;
  * `JOIN`;
  * `GROUP BY`;
  * `HAVING`;
  * `ORDER BY`;
  * CTEs;
  * criação de views;
  * validação de dados.

* **Python**

  * pandas;
  * exploração e tratamento dos dados;
  * cálculo de indicadores;
  * análise exploratória;
  * visualização.

* **Streamlit**

  * construção do dashboard interativo.

* **Plotly**

  * visualizações interativas.

* **SQLite**

  * armazenamento e consulta da base de dados.

---

## Estrutura do projeto

```text
advertising-product-analytics/

│
├── data/
│   └── advertising_product_analytics.db
│
├── sql/
│   └── analysis.sql
│
├── python/
│   └── 01_eda.py
│
├── dashboard/
│   └── dashboard.py
│
└── README.md
```

---

## Limitações

Este projeto utiliza uma base pequena, fictícia e construída exclusivamente para fins educacionais e de portfólio.

Por esse motivo:

* os resultados não representam o mercado publicitário real;
* não devem ser utilizados para decisões reais de investimento;
* não é possível estabelecer causalidade entre investimento e performance;
* não foram aplicados modelos estatísticos avançados;
* não foram consideradas variáveis externas que poderiam influenciar o desempenho das campanhas;
* a relação entre campanhas e receita do inventário foi simplificada para fins didáticos.

Além disso, a base foi construída para demonstrar o processo analítico e, portanto, algumas relações entre os dados não representam necessariamente a complexidade de uma operação publicitária real.

---

## Uso de IA no desenvolvimento

O ChatGPT foi utilizado como ferramenta de apoio durante o desenvolvimento deste projeto, principalmente para esclarecimento de conceitos, aprendizado de SQL, Python e Streamlit, revisão de código, debugging e discussão da estrutura das análises.

A definição do problema de negócio, a modelagem da análise, a seleção dos indicadores, a interpretação dos resultados e as decisões de apresentação foram realizadas e validadas pela autora.

O uso de IA fez parte do processo de aprendizagem e desenvolvimento, sem substituir a análise crítica e as decisões tomadas ao longo do projeto.

---

## Autoria

Projeto desenvolvido por **Bárbara Letícia Marques Archanjo Dutra** como projeto de portfólio em Data Analytics.

O projeto busca demonstrar a aplicação prática de conhecimentos de **Publicidade e Propaganda, Marketing, Customer Experience, SQL, Python e análise de dados** em um contexto de produtos publicitários.
