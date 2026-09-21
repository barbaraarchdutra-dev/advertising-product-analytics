-- ============================================================
-- ANÁLISE DE PRODUTOS DE PUBLICIDADE
-- Projeto de portfólio | Dados educacionais e fictícios
-- ============================================================


-- ============================================================
-- 1. DESEMPENHO POR PRODUTO
-- ============================================================

SELECT
    products.product_name AS product,
    SUM(campaigns.investment) AS total_investment,
    SUM(campaigns.impressions) AS total_impressions,
    SUM(campaigns.clicks) AS total_clicks,
    SUM(campaigns.conversions) AS total_conversions,

    ROUND(
        SUM(campaigns.clicks) * 100.0
        / NULLIF(SUM(campaigns.impressions), 0),
        2
    ) AS ctr_percent,

    ROUND(
        SUM(campaigns.investment)
        / NULLIF(SUM(campaigns.clicks), 0),
        2
    ) AS cpc,

    ROUND(
        SUM(campaigns.conversions) * 100.0
        / NULLIF(SUM(campaigns.clicks), 0),
        2
    ) AS conversion_rate_percent,

    ROUND(
        SUM(campaigns.investment)
        / NULLIF(SUM(campaigns.conversions), 0),
        2
    ) AS cost_per_conversion

FROM campaigns

JOIN products
    ON campaigns.product_id = products.product_id

GROUP BY products.product_name

ORDER BY ctr_percent DESC;


-- ============================================================
-- 2. DESEMPENHO POR ANUNCIANTE
-- ============================================================

SELECT
    advertisers.advertisers_name AS advertiser,
    advertisers.industry AS industry,

    SUM(campaigns.investment) AS total_investment,
    SUM(campaigns.impressions) AS total_impressions,
    SUM(campaigns.clicks) AS total_clicks,
    SUM(campaigns.conversions) AS total_conversions,

    ROUND(
        SUM(campaigns.clicks) * 100.0
        / NULLIF(SUM(campaigns.impressions), 0),
        2
    ) AS ctr_percent,

    ROUND(
        SUM(campaigns.investment)
        / NULLIF(SUM(campaigns.clicks), 0),
        2
    ) AS cpc,

    ROUND(
        SUM(campaigns.conversions) * 100.0
        / NULLIF(SUM(campaigns.clicks), 0),
        2
    ) AS conversion_rate_percent,

    ROUND(
        SUM(campaigns.investment)
        / NULLIF(SUM(campaigns.conversions), 0),
        2
    ) AS cost_per_conversion

FROM campaigns

JOIN advertisers
    ON campaigns.advertisers_id = advertisers.advertisers_id

GROUP BY
    advertisers.advertisers_name,
    advertisers.industry

ORDER BY total_investment DESC;


-- ============================================================
-- 3. ANUNCIANTE X PRODUTO
-- ============================================================

SELECT
    advertisers.advertisers_name AS advertiser,
    products.product_name AS product,

    SUM(campaigns.investment) AS total_investment,
    SUM(campaigns.impressions) AS total_impressions,
    SUM(campaigns.clicks) AS total_clicks,
    SUM(campaigns.conversions) AS total_conversions,

    ROUND(
        SUM(campaigns.clicks) * 100.0
        / NULLIF(SUM(campaigns.impressions), 0),
        2
    ) AS ctr_percent,

    ROUND(
        SUM(campaigns.investment)
        / NULLIF(SUM(campaigns.clicks), 0),
        2
    ) AS cpc,

    ROUND(
        SUM(campaigns.conversions) * 100.0
        / NULLIF(SUM(campaigns.clicks), 0),
        2
    ) AS conversion_rate_percent,

    ROUND(
        SUM(campaigns.investment)
        / NULLIF(SUM(campaigns.conversions), 0),
        2
    ) AS cost_per_conversion

FROM campaigns

JOIN advertisers
    ON campaigns.advertisers_id = advertisers.advertisers_id

JOIN products
    ON campaigns.product_id = products.product_id

GROUP BY
    advertisers.advertisers_name,
    products.product_name

ORDER BY
    ctr_percent DESC;


-- ============================================================
-- 4. DESEMPENHO MENSAL
-- ============================================================

SELECT
    substr(campaigns.date, 1, 7) AS month,

    COUNT(campaigns.campaign_id) AS campaigns,

    SUM(campaigns.investment) AS total_investment,
    SUM(campaigns.impressions) AS total_impressions,
    SUM(campaigns.clicks) AS total_clicks,
    SUM(campaigns.conversions) AS total_conversions,

    ROUND(
        SUM(campaigns.clicks) * 100.0
        / NULLIF(SUM(campaigns.impressions), 0),
        2
    ) AS ctr_percent,

    ROUND(
        SUM(campaigns.investment)
        / NULLIF(SUM(campaigns.clicks), 0),
        2
    ) AS cpc,

    ROUND(
        SUM(campaigns.conversions) * 100.0
        / NULLIF(SUM(campaigns.clicks), 0),
        2
    ) AS conversion_rate_percent

FROM campaigns

GROUP BY substr(campaigns.date, 1, 7)

ORDER BY month;


-- ============================================================
-- 5. DESEMPENHO MENSAL POR PRODUTO
-- ============================================================

SELECT
    substr(campaigns.date, 1, 7) AS month,
    products.product_name AS product,

    SUM(campaigns.investment) AS total_investment,
    SUM(campaigns.impressions) AS total_impressions,
    SUM(campaigns.clicks) AS total_clicks,
    SUM(campaigns.conversions) AS total_conversions,

    ROUND(
        SUM(campaigns.clicks) * 100.0
        / NULLIF(SUM(campaigns.impressions), 0),
        2
    ) AS ctr_percent,

    ROUND(
        SUM(campaigns.investment)
        / NULLIF(SUM(campaigns.clicks), 0),
        2
    ) AS cpc,

    ROUND(
        SUM(campaigns.conversions) * 100.0
        / NULLIF(SUM(campaigns.clicks), 0),
        2
    ) AS conversion_rate_percent

FROM campaigns

JOIN products
    ON campaigns.product_id = products.product_id

GROUP BY
    substr(campaigns.date, 1, 7),
    products.product_name

ORDER BY
    month,
    product;


-- ============================================================
-- 6. PARTICIPAÇÃO DO INVESTIMENTO X CONVERSÕES
-- ============================================================

WITH product_totals AS (

    SELECT
        products.product_name AS product,
        SUM(campaigns.investment) AS investment,
        SUM(campaigns.conversions) AS conversions

    FROM campaigns

    JOIN products
        ON campaigns.product_id = products.product_id

    GROUP BY products.product_name
)

SELECT
    product,
    investment,
    conversions,

    ROUND(
        investment * 100.0
        / SUM(investment) OVER (),
        2
    ) AS investment_share_percent,

    ROUND(
        conversions * 100.0
        / SUM(conversions) OVER (),
        2
    ) AS conversion_share_percent,

    ROUND(
        (
            conversions * 100.0
            / SUM(conversions) OVER ()
        )
        -
        (
            investment * 100.0
            / SUM(investment) OVER ()
        ),
        2
    ) AS conversion_investment_gap_pp

FROM product_totals

ORDER BY conversion_investment_gap_pp DESC;


-- ============================================================
-- 7. INVENTÁRIO POR PRODUTO
-- ============================================================

SELECT
    products.product_name AS product,

    SUM(inventory.available_impressions)
        AS available_impressions,

    SUM(inventory.sold_impressions)
        AS sold_impressions,

    ROUND(
        SUM(inventory.sold_impressions) * 100.0
        / NULLIF(
            SUM(inventory.available_impressions),
            0
        ),
        2
    ) AS occupancy_percent,

    SUM(inventory.revenue) AS total_revenue,

    ROUND(
        SUM(inventory.revenue) * 1000.0
        / NULLIF(
            SUM(inventory.sold_impressions),
            0
        ),
        2
    ) AS revenue_cpm

FROM inventory

JOIN products
    ON inventory.product_id = products.product_id

GROUP BY products.product_name

ORDER BY total_revenue DESC;


-- ============================================================
-- 8. RECEITA MENSAL POR PRODUTO
-- ============================================================

SELECT
    substr(inventory.date, 1, 7) AS month,
    products.product_name AS product,

    SUM(inventory.available_impressions)
        AS available_impressions,

    SUM(inventory.sold_impressions)
        AS sold_impressions,

    SUM(inventory.revenue) AS total_revenue,

    ROUND(
        SUM(inventory.sold_impressions) * 100.0
        / NULLIF(
            SUM(inventory.available_impressions),
            0
        ),
        2
    ) AS occupancy_percent,

    ROUND(
        SUM(inventory.revenue) * 1000.0
        / NULLIF(
            SUM(inventory.sold_impressions),
            0
        ),
        2
    ) AS revenue_cpm

FROM inventory

JOIN products
    ON inventory.product_id = products.product_id

GROUP BY
    substr(inventory.date, 1, 7),
    products.product_name

ORDER BY
    month,
    product;


-- ============================================================
-- 9. RECEITA X INVESTIMENTO
-- ============================================================

SELECT
    products.product_name,

    SUM(campaigns.investment) AS total_investment,

    SUM(inventory.revenue) AS total_revenue,

    ROUND(
        SUM(inventory.revenue)
        / NULLIF(SUM(campaigns.investment), 0),
        2
    ) AS revenue_investment_ratio

FROM campaigns

JOIN products
    ON campaigns.product_id = products.product_id

JOIN inventory
    ON campaigns.product_id = inventory.product_id
    AND campaigns.date = inventory.date

GROUP BY products.product_name

ORDER BY revenue_investment_ratio DESC;


-- ============================================================
-- 10. PARTICIPAÇÃO DA RECEITA X INVESTIMENTO
-- ============================================================

WITH product_totals AS (

    SELECT
        products.product_name AS product,

        SUM(campaigns.investment) AS investment,

        SUM(inventory.revenue) AS revenue

    FROM campaigns

    JOIN products
        ON campaigns.product_id = products.product_id

    JOIN inventory
        ON campaigns.product_id = inventory.product_id
        AND campaigns.date = inventory.date

    GROUP BY products.product_name
)

SELECT
    product,
    investment,
    revenue,

    ROUND(
        investment * 100.0
        / SUM(investment) OVER (),
        2
    ) AS investment_share_percent,

    ROUND(
        revenue * 100.0
        / SUM(revenue) OVER (),
        2
    ) AS revenue_share_percent,

    ROUND(
        (
            revenue * 100.0
            / SUM(revenue) OVER ()
        )
        -
        (
            investment * 100.0
            / SUM(investment) OVER ()
        ),
        2
    ) AS revenue_investment_gap_pp

FROM product_totals

ORDER BY revenue_investment_gap_pp DESC;


-- ============================================================
-- 11. VALIDAÇÃO: CLIQUES NÃO DEVEM SUPERAR IMPRESSÕES
-- ============================================================

SELECT
    campaign_id,
    date,
    impressions,
    clicks

FROM campaigns

WHERE clicks > impressions;


-- ============================================================
-- 12. VALIDAÇÃO: CONVERSÕES NÃO DEVEM SUPERAR CLIQUES
-- ============================================================

SELECT
    campaign_id,
    date,
    clicks,
    conversions

FROM campaigns

WHERE conversions > clicks;


-- ============================================================
-- 13. VALIDAÇÃO: VALORES NEGATIVOS
-- ============================================================

SELECT
    campaign_id,
    investment,
    impressions,
    clicks,
    conversions

FROM campaigns

WHERE investment < 0
   OR impressions < 0
   OR clicks < 0
   OR conversions < 0;


-- ============================================================
-- 14. VALIDAÇÃO: PRODUTOS SEM CADASTRO
-- ============================================================

SELECT
    campaigns.campaign_id,
    campaigns.product_id

FROM campaigns

LEFT JOIN products
    ON campaigns.product_id = products.product_id

WHERE products.product_id IS NULL;


-- ============================================================
-- 15. VALIDAÇÃO: ANUNCIANTES SEM CADASTRO
-- ============================================================

SELECT
    campaigns.campaign_id,
    campaigns.advertisers_id

FROM campaigns

LEFT JOIN advertisers
    ON campaigns.advertisers_id = advertisers.advertisers_id

WHERE advertisers.advertisers_id IS NULL;