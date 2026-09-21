import sqlite3

import pandas as pd
import plotly.express as px
import streamlit as st


# ============================================================
# 1. CONFIGURAÇÃO
# ============================================================

st.set_page_config(
    page_title="Análise de Produtos de Publicidade",
    page_icon="📊",
    layout="wide"
)


# ============================================================
# 2. CONEXÃO COM O BANCO
# ============================================================

conexao = sqlite3.connect(
    "data/advertising_product_analytics.db"
)


# ============================================================
# 3. DADOS DE CAMPANHAS
# ============================================================

consulta_campanhas = """
SELECT
    products.product_name AS produto,
    SUM(campaigns.investment) AS investimento,
    SUM(campaigns.impressions) AS impressoes,
    SUM(campaigns.clicks) AS cliques,
    SUM(campaigns.conversions) AS conversoes
FROM campaigns
JOIN products
    ON campaigns.product_id = products.product_id
GROUP BY products.product_name
"""

dados = pd.read_sql_query(
    consulta_campanhas,
    conexao
)


# ============================================================
# 4. INDICADORES DE CAMPANHA
# ============================================================

dados["ctr"] = (
    dados["cliques"]
    / dados["impressoes"]
    * 100
)

dados["cpc"] = (
    dados["investimento"]
    / dados["cliques"]
)

dados["taxa_conversao"] = (
    dados["conversoes"]
    / dados["cliques"]
    * 100
)

dados["custo_por_conversao"] = (
    dados["investimento"]
    / dados["conversoes"]
)


# ============================================================
# 5. DADOS DE INVENTÁRIO
# ============================================================

consulta_inventario = """
SELECT
    products.product_name AS produto,
    SUM(inventory.available_impressions) AS impressoes_disponiveis,
    SUM(inventory.sold_impressions) AS impressoes_vendidas,
    SUM(inventory.revenue) AS receita
FROM inventory
JOIN products
    ON inventory.product_id = products.product_id
GROUP BY products.product_name
"""

inventario = pd.read_sql_query(
    consulta_inventario,
    conexao
)


# ============================================================
# 6. INDICADORES DE INVENTÁRIO
# ============================================================

inventario["ocupacao"] = (
    inventario["impressoes_vendidas"]
    / inventario["impressoes_disponiveis"]
    * 100
)

inventario["cpm_receita"] = (
    inventario["receita"]
    / inventario["impressoes_vendidas"]
    * 1000
)


# ============================================================
# 7. CRUZAMENTO ENTRE CAMPANHAS E INVENTÁRIO
# ============================================================

dados = dados.merge(
    inventario,
    on="produto",
    how="left"
)


# ============================================================
# 8. INDICADORES DE MONETIZAÇÃO
# ============================================================

investimento_total = dados["investimento"].sum()
receita_total = dados["receita"].sum()

dados["razao_receita_investimento"] = (
    dados["receita"]
    / dados["investimento"]
)

dados["participacao_investimento"] = (
    dados["investimento"]
    / investimento_total
    * 100
)

dados["participacao_receita"] = (
    dados["receita"]
    / receita_total
    * 100
)

dados["gap_receita_investimento"] = (
    dados["participacao_receita"]
    - dados["participacao_investimento"]
)


# ============================================================
# 9. TOTAIS DE CAMPANHA
# ============================================================

impressoes_total = dados["impressoes"].sum()
cliques_total = dados["cliques"].sum()
conversoes_total = dados["conversoes"].sum()


# ============================================================
# 10. TOTAIS DE INVENTÁRIO
# ============================================================

impressoes_disponiveis_total = (
    dados["impressoes_disponiveis"].sum()
)

impressoes_vendidas_total = (
    dados["impressoes_vendidas"].sum()
)

ocupacao_total = (
    impressoes_vendidas_total
    / impressoes_disponiveis_total
    * 100
)

cpm_receita_total = (
    receita_total
    / impressoes_vendidas_total
    * 1000
)


# ============================================================
# 11. PRINCIPAIS INDICADORES
# ============================================================

produto_maior_ctr = dados.loc[
    dados["ctr"].idxmax(),
    "produto"
]

maior_ctr = dados["ctr"].max()


produto_menor_cpc = dados.loc[
    dados["cpc"].idxmin(),
    "produto"
]

menor_cpc = dados["cpc"].min()


produto_maior_conversao = dados.loc[
    dados["taxa_conversao"].idxmax(),
    "produto"
]

maior_taxa_conversao = dados["taxa_conversao"].max()


produto_maior_receita = dados.loc[
    dados["receita"].idxmax(),
    "produto"
]

maior_receita = dados["receita"].max()


produto_maior_cpm = dados.loc[
    dados["cpm_receita"].idxmax(),
    "produto"
]

maior_cpm = dados["cpm_receita"].max()


produto_maior_gap = dados.loc[
    dados["gap_receita_investimento"].idxmax(),
    "produto"
]

maior_gap = dados["gap_receita_investimento"].max()


# ============================================================
# 12. CABEÇALHO
# ============================================================

st.title(
    "Análise de Produtos de Publicidade"
)

st.subheader(
    "Análise de desempenho e eficiência de produtos publicitários"
)

st.markdown(
    """
Este painel analisa indicadores de campanhas e inventário
publicitário para apoiar a leitura de desempenho, eficiência,
ocupação e geração de receita dos diferentes formatos de produto.
"""
)

st.caption(
    "Projeto de portfólio | Dados educacionais e fictícios"
)


# ============================================================
# 13. VISÃO GERAL
# ============================================================

st.markdown("## Visão geral")

coluna1, coluna2, coluna3, coluna4 = st.columns(4)

coluna1.metric(
    "Investimento",
    f"R$ {investimento_total:,.0f}".replace(
        ",",
        "."
    )
)

coluna2.metric(
    "Impressões",
    f"{impressoes_total:,.0f}".replace(
        ",",
        "."
    )
)

coluna3.metric(
    "Cliques",
    f"{cliques_total:,.0f}".replace(
        ",",
        "."
    )
)

coluna4.metric(
    "Conversões",
    f"{conversoes_total:,.0f}".replace(
        ",",
        "."
    )
)


# ============================================================
# 14. DESEMPENHO DOS PRODUTOS
# ============================================================

st.markdown("## Desempenho dos produtos")

coluna_grafico1, coluna_grafico2 = st.columns(2)


grafico_ctr = px.bar(
    dados,
    x="produto",
    y="ctr",
    title="CTR por produto",
    labels={
        "produto": "Produto",
        "ctr": "CTR (%)"
    },
    text_auto=".2f"
)

grafico_ctr.update_layout(
    showlegend=False
)

coluna_grafico1.plotly_chart(
    grafico_ctr,
    use_container_width=True
)


grafico_cpc = px.bar(
    dados,
    x="produto",
    y="cpc",
    title="CPC por produto",
    labels={
        "produto": "Produto",
        "cpc": "CPC (R$)"
    },
    text_auto=".2f"
)

grafico_cpc.update_layout(
    showlegend=False
)

coluna_grafico2.plotly_chart(
    grafico_cpc,
    use_container_width=True
)


# ============================================================
# 15. EFICIÊNCIA DE CONVERSÃO
# ============================================================

st.markdown("## Eficiência de conversão")

grafico_conversao = px.bar(
    dados,
    x="produto",
    y="taxa_conversao",
    title="Taxa de conversão por produto",
    labels={
        "produto": "Produto",
        "taxa_conversao": "Taxa de conversão (%)"
    },
    text_auto=".2f"
)

grafico_conversao.update_layout(
    showlegend=False
)

st.plotly_chart(
    grafico_conversao,
    use_container_width=True
)


# ============================================================
# 16. INVENTÁRIO PUBLICITÁRIO
# ============================================================

st.markdown("## Inventário publicitário")

coluna_inv1, coluna_inv2, coluna_inv3 = st.columns(3)

coluna_inv1.metric(
    "Impressões disponíveis",
    f"{impressoes_disponiveis_total:,.0f}".replace(
        ",",
        "."
    )
)

coluna_inv2.metric(
    "Impressões vendidas",
    f"{impressoes_vendidas_total:,.0f}".replace(
        ",",
        "."
    )
)

coluna_inv3.metric(
    "Ocupação do inventário",
    f"{ocupacao_total:.2f}%"
)


# ============================================================
# 17. RECEITA E MONETIZAÇÃO
# ============================================================

st.markdown("## Receita e monetização")

coluna_receita1, coluna_receita2 = st.columns(2)


grafico_receita = px.bar(
    dados,
    x="produto",
    y="receita",
    title="Receita por produto",
    labels={
        "produto": "Produto",
        "receita": "Receita (R$)"
    },
    text_auto=".2s"
)

grafico_receita.update_layout(
    showlegend=False
)

coluna_receita1.plotly_chart(
    grafico_receita,
    use_container_width=True
)


grafico_cpm = px.bar(
    dados,
    x="produto",
    y="cpm_receita",
    title="CPM de receita por produto",
    labels={
        "produto": "Produto",
        "cpm_receita": "CPM de receita (R$)"
    },
    text_auto=".2f"
)

grafico_cpm.update_layout(
    showlegend=False
)

coluna_receita2.plotly_chart(
    grafico_cpm,
    use_container_width=True
)


# ============================================================
# 18. INVESTIMENTO X RECEITA
# ============================================================

st.markdown("## Investimento x receita")

grafico_investimento_receita = px.bar(
    dados,
    x="produto",
    y=[
        "investimento",
        "receita"
    ],
    barmode="group",
    title="Comparação entre investimento e receita",
    labels={
        "produto": "Produto",
        "value": "Valor (R$)",
        "variable": "Indicador"
    },
    text_auto=".2s"
)

grafico_investimento_receita.update_layout(
    legend_title_text="Indicador"
)

st.plotly_chart(
    grafico_investimento_receita,
    use_container_width=True
)


# ============================================================
# 19. EFICIÊNCIA DE MONETIZAÇÃO
# ============================================================

st.markdown("## Eficiência de monetização")

grafico_razao = px.bar(
    dados,
    x="produto",
    y="razao_receita_investimento",
    title="Razão Receita / Investimento",
    labels={
        "produto": "Produto",
        "razao_receita_investimento": "Receita / Investimento"
    },
    text_auto=".2f"
)

grafico_razao.update_layout(
    showlegend=False
)

st.plotly_chart(
    grafico_razao,
    use_container_width=True
)

st.caption(
    """
A razão Receita / Investimento compara a receita do inventário
com o investimento registrado nas campanhas. Ela não representa
ROAS, pois a base não estabelece atribuição direta entre o
investimento de campanha e a receita.
"""
)


# ============================================================
# 20. INDICADORES DE INVENTÁRIO POR PRODUTO
# ============================================================

st.markdown("## Indicadores de inventário por produto")

tabela_inventario = dados[
    [
        "produto",
        "impressoes_disponiveis",
        "impressoes_vendidas",
        "ocupacao",
        "receita",
        "cpm_receita"
    ]
].copy()

tabela_inventario.columns = [
    "Produto",
    "Impressões disponíveis",
    "Impressões vendidas",
    "Ocupação (%)",
    "Receita (R$)",
    "CPM de receita (R$)"
]

st.dataframe(
    tabela_inventario.style.format(
        {
            "Impressões disponíveis": "{:,.0f}",
            "Impressões vendidas": "{:,.0f}",
            "Ocupação (%)": "{:.2f}",
            "Receita (R$)": "R$ {:,.0f}",
            "CPM de receita (R$)": "R$ {:.2f}"
        }
    ),
    use_container_width=True,
    hide_index=True
)


# ============================================================
# 21. INDICADORES DE CAMPANHA POR PRODUTO
# ============================================================

st.markdown("## Indicadores de campanha por produto")

tabela = dados[
    [
        "produto",
        "investimento",
        "impressoes",
        "cliques",
        "conversoes",
        "ctr",
        "cpc",
        "taxa_conversao",
        "custo_por_conversao"
    ]
].copy()

tabela.columns = [
    "Produto",
    "Investimento",
    "Impressões",
    "Cliques",
    "Conversões",
    "CTR (%)",
    "CPC (R$)",
    "Conversão (%)",
    "Custo por conversão (R$)"
]

st.dataframe(
    tabela.style.format(
        {
            "Investimento": "R$ {:,.0f}",
            "Impressões": "{:,.0f}",
            "Cliques": "{:,.0f}",
            "Conversões": "{:,.0f}",
            "CTR (%)": "{:.2f}",
            "CPC (R$)": "R$ {:.2f}",
            "Conversão (%)": "{:.2f}",
            "Custo por conversão (R$)": "R$ {:.2f}"
        }
    ),
    use_container_width=True,
    hide_index=True
)


# ============================================================
# 22. PARTICIPAÇÃO NA RECEITA E NO INVESTIMENTO
# ============================================================

st.markdown(
    "## Participação na receita e no investimento"
)

grafico_participacao = px.bar(
    dados,
    x="produto",
    y=[
        "participacao_investimento",
        "participacao_receita"
    ],
    barmode="group",
    title="Participação por produto",
    labels={
        "produto": "Produto",
        "value": "Participação (%)",
        "variable": "Indicador"
    },
    text_auto=".2f"
)

grafico_participacao.update_layout(
    legend_title_text="Indicador"
)

st.plotly_chart(
    grafico_participacao,
    use_container_width=True
)


# ============================================================
# 23. INSIGHTS
# ============================================================

st.markdown("## Insights")

coluna_insight1, coluna_insight2, coluna_insight3 = st.columns(3)


coluna_insight1.metric(
    "Maior CTR",
    produto_maior_ctr,
    f"{maior_ctr:.2f}%"
)


coluna_insight2.metric(
    "Menor CPC",
    produto_menor_cpc,
    f"R$ {menor_cpc:.2f}"
)


coluna_insight3.metric(
    "Maior receita",
    produto_maior_receita,
    f"R$ {maior_receita:,.0f}".replace(
        ",",
        "."
    )
)


st.info(
    f"""
Na base analisada, o produto **{produto_maior_ctr}** apresentou
o maior CTR e também o menor CPC.

Na dimensão de monetização, o produto **{produto_maior_receita}**
apresentou a maior receita, enquanto o produto **{produto_maior_cpm}**
apresentou o maior CPM de receita.

O produto **{produto_maior_gap}** também apresentou a maior
diferença positiva entre sua participação na receita e sua
participação no investimento, de **{maior_gap:.2f} pontos
percentuais**.

Esses resultados são descritivos e refletem exclusivamente a base
educacional utilizada neste projeto. A amostra não permite inferir
causalidade ou recomendar alocação de investimento sem análises
adicionais.
"""
)


# ============================================================
# 24. NOTA METODOLÓGICA
# ============================================================

st.markdown("### Nota metodológica")

st.caption(
    """
Os dados utilizados neste projeto são fictícios e foram construídos
exclusivamente para fins educacionais e de portfólio. Os indicadores
de inventário representam uma visão simplificada de disponibilidade,
venda e geração de receita de espaços publicitários.
"""
)


# ============================================================
# 25. RODAPÉ
# ============================================================

st.divider()

st.caption(
    "Análise de produtos publicitários | Projeto de portfólio em Data Analytics"
)


# ============================================================
# 26. FINALIZAÇÃO
# ============================================================

conexao.close()
