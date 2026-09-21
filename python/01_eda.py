import os
import sqlite3

import pandas as pd
import matplotlib.pyplot as plt


# ============================================================
# 1. CONFIGURAÇÃO
# ============================================================

pasta_graficos = "dashboard"

os.makedirs(
    pasta_graficos,
    exist_ok=True
)


# ============================================================
# 2. CONEXÃO COM O BANCO
# ============================================================

conexao = sqlite3.connect(
    "data/advertising_product_analytics.db"
)

print("Banco conectado!")


# ============================================================
# 3. CONSULTA PRINCIPAL — CAMPANHAS
# ============================================================

consulta = """

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
    consulta,
    conexao
)


# ============================================================
# 4. CONSULTA — INVENTÁRIO E RECEITA
# ============================================================

consulta_inventario = """

SELECT

    products.product_name AS produto,

    SUM(inventory.available_impressions)
        AS impressoes_disponiveis,

    SUM(inventory.sold_impressions)
        AS impressoes_vendidas,

    SUM(inventory.revenue)
        AS receita

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
# 5. CRUZAMENTO DE CAMPANHAS E INVENTÁRIO
# ============================================================

dados = dados.merge(
    inventario,
    on="produto",
    how="left"
)


# ============================================================
# 6. KPIs DE PERFORMANCE
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
# 7. KPIs DE INVENTÁRIO E MONETIZAÇÃO
# ============================================================

dados["ocupacao"] = (
    dados["impressoes_vendidas"]
    / dados["impressoes_disponiveis"]
    * 100
)


dados["receita_cpm"] = (
    dados["receita"]
    / dados["impressoes_vendidas"]
    * 1000
)


dados["receita_investimento_ratio"] = (
    dados["receita"]
    / dados["investimento"]
)


# ============================================================
# 8. TOTAIS DA BASE
# ============================================================

investimento_total = (
    dados["investimento"]
    .sum()
)


conversoes_total = (
    dados["conversoes"]
    .sum()
)


receita_total = (
    dados["receita"]
    .sum()
)


impressoes_disponiveis_total = (
    dados["impressoes_disponiveis"]
    .sum()
)


impressoes_vendidas_total = (
    dados["impressoes_vendidas"]
    .sum()
)


# ============================================================
# 9. PARTICIPAÇÃO NO INVESTIMENTO E CONVERSÕES
# ============================================================

dados["participacao_investimento"] = (
    dados["investimento"]
    / investimento_total
    * 100
)


dados["participacao_conversoes"] = (
    dados["conversoes"]
    / conversoes_total
    * 100
)


dados["gap_conversao_investimento"] = (
    dados["participacao_conversoes"]
    - dados["participacao_investimento"]
)


# ============================================================
# 10. PARTICIPAÇÃO NA RECEITA
# ============================================================

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
# 11. ORGANIZAÇÃO DOS DADOS
# ============================================================

dados = dados.round(2)


dados = dados.sort_values(
    "gap_conversao_investimento",
    ascending=False
)


dados = dados.reset_index(
    drop=True
)


produtos_acima = dados[
    dados["gap_conversao_investimento"] > 0
]


# ============================================================
# 12. PRINCIPAIS INSIGHTS
# ============================================================

produto_maior_gap = dados.loc[
    dados["gap_conversao_investimento"].idxmax(),
    "produto"
]


maior_gap = dados[
    "gap_conversao_investimento"
].max()


produto_menor_gap = dados.loc[
    dados["gap_conversao_investimento"].idxmin(),
    "produto"
]


menor_gap = dados[
    "gap_conversao_investimento"
].min()


produto_maior_receita = dados.loc[
    dados["receita"].idxmax(),
    "produto"
]


maior_receita = dados[
    "receita"
].max()


produto_maior_ctr = dados.loc[
    dados["ctr"].idxmax(),
    "produto"
]


maior_ctr = dados[
    "ctr"
].max()


produto_menor_cpc = dados.loc[
    dados["cpc"].idxmin(),
    "produto"
]


menor_cpc = dados[
    "cpc"
].min()


# ============================================================
# 13. INSIGHTS TEXTUAIS
# ============================================================

insight_gap = (
    f"Na base analisada, o produto {produto_maior_gap} "
    f"apresentou a maior diferença positiva entre sua "
    f"participação nas conversões e sua participação no "
    f"investimento: {maior_gap:.2f} pontos percentuais."
)


insight_receita = (
    f"Na base analisada, o produto {produto_maior_receita} "
    f"apresentou a maior receita, de "
    f"R$ {maior_receita:,.2f}."
)


insight_ctr = (
    f"Na base analisada, o produto {produto_maior_ctr} "
    f"apresentou o maior CTR, de {maior_ctr:.2f}%."
)


insight_cpc = (
    f"Na base analisada, o produto {produto_menor_cpc} "
    f"apresentou o menor CPC, de R$ {menor_cpc:.2f}."
)


# ============================================================
# 14. RESULTADOS NO TERMINAL
# ============================================================

print()

print("=" * 70)

print("KPIs DE PERFORMANCE POR PRODUTO")

print("=" * 70)


print(
    dados[
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
    ]
)


print()

print("=" * 70)

print("KPIs DE INVENTÁRIO E MONETIZAÇÃO")

print("=" * 70)


print(
    dados[
        [
            "produto",
            "impressoes_disponiveis",
            "impressoes_vendidas",
            "ocupacao",
            "receita",
            "receita_cpm",
            "receita_investimento_ratio"
        ]
    ]
)


print()

print("=" * 70)

print("PARTICIPAÇÃO NO INVESTIMENTO X CONVERSÕES")

print("=" * 70)


print(
    dados[
        [
            "produto",
            "participacao_investimento",
            "participacao_conversoes",
            "gap_conversao_investimento"
        ]
    ]
)


print()

print("Produtos com diferença positiva:")

print(
    produtos_acima[
        [
            "produto",
            "gap_conversao_investimento"
        ]
    ]
)


print()

print("PRINCIPAIS INSIGHTS")

print(insight_gap)

print(insight_receita)

print(insight_ctr)

print(insight_cpc)


print()

print("TOTAIS DA BASE")

print(
    f"Investimento total: R$ {investimento_total:,.2f}"
)


print(
    f"Conversões totais: {conversoes_total:,.0f}"
)


print(
    f"Receita total: R$ {receita_total:,.2f}"
)


print(
    f"Impressões disponíveis: "
    f"{impressoes_disponiveis_total:,.0f}"
)


print(
    f"Impressões vendidas: "
    f"{impressoes_vendidas_total:,.0f}"
)


print(
    f"Ocupação geral do inventário: "
    f"{impressoes_vendidas_total / impressoes_disponiveis_total * 100:.2f}%"
)


# ============================================================
# 15. GRÁFICO 1 — CTR
# ============================================================

plt.figure(
    figsize=(8, 5)
)

plt.bar(
    dados["produto"],
    dados["ctr"]
)

plt.title(
    "CTR por produto"
)

plt.xlabel(
    "Produto"
)

plt.ylabel(
    "CTR (%)"
)

plt.tight_layout()

plt.savefig(
    f"{pasta_graficos}/ctr_por_produto.png",
    dpi=300,
    bbox_inches="tight"
)

plt.close()


# ============================================================
# 16. GRÁFICO 2 — CPC
# ============================================================

plt.figure(
    figsize=(8, 5)
)

plt.bar(
    dados["produto"],
    dados["cpc"]
)

plt.title(
    "CPC por produto"
)

plt.xlabel(
    "Produto"
)

plt.ylabel(
    "CPC (R$)"
)

plt.tight_layout()

plt.savefig(
    f"{pasta_graficos}/cpc_por_produto.png",
    dpi=300,
    bbox_inches="tight"
)

plt.close()


# ============================================================
# 17. GRÁFICO 3 — TAXA DE CONVERSÃO
# ============================================================

plt.figure(
    figsize=(8, 5)
)

plt.bar(
    dados["produto"],
    dados["taxa_conversao"]
)

plt.title(
    "Taxa de conversão por produto"
)

plt.xlabel(
    "Produto"
)

plt.ylabel(
    "Taxa de conversão (%)"
)

plt.tight_layout()

plt.savefig(
    f"{pasta_graficos}/taxa_conversao_por_produto.png",
    dpi=300,
    bbox_inches="tight"
)

plt.close()


# ============================================================
# 18. GRÁFICO 4 — INVESTIMENTO X CONVERSÕES
# ============================================================

plt.figure(
    figsize=(8, 5)
)

plt.bar(
    dados["produto"],
    dados["participacao_investimento"],
    label="Investimento (%)"
)

plt.bar(
    dados["produto"],
    dados["participacao_conversoes"],
    alpha=0.7,
    label="Conversões (%)"
)

plt.title(
    "Participação no investimento x conversões"
)

plt.xlabel(
    "Produto"
)

plt.ylabel(
    "Participação (%)"
)

plt.legend()

plt.tight_layout()

plt.savefig(
    f"{pasta_graficos}/investimento_vs_conversoes.png",
    dpi=300,
    bbox_inches="tight"
)

plt.close()


# ============================================================
# 19. GRÁFICO 5 — RECEITA POR PRODUTO
# ============================================================

plt.figure(
    figsize=(8, 5)
)

plt.bar(
    dados["produto"],
    dados["receita"]
)

plt.title(
    "Receita por produto"
)

plt.xlabel(
    "Produto"
)

plt.ylabel(
    "Receita (R$)"
)

plt.tight_layout()

plt.savefig(
    f"{pasta_graficos}/receita_por_produto.png",
    dpi=300,
    bbox_inches="tight"
)

plt.close()


# ============================================================
# 20. GRÁFICO 6 — OCUPAÇÃO DO INVENTÁRIO
# ============================================================

plt.figure(
    figsize=(8, 5)
)

plt.bar(
    dados["produto"],
    dados["ocupacao"]
)

plt.title(
    "Ocupação do inventário por produto"
)

plt.xlabel(
    "Produto"
)

plt.ylabel(
    "Ocupação (%)"
)

plt.tight_layout()

plt.savefig(
    f"{pasta_graficos}/ocupacao_por_produto.png",
    dpi=300,
    bbox_inches="tight"
)

plt.close()


# ============================================================
# 21. FINALIZAÇÃO
# ============================================================

conexao.close()


print()

print("=" * 70)

print(
    "Análise exploratória concluída."
)

print(
    "Gráficos salvos na pasta:",
    pasta_graficos
)

print("=" * 70)