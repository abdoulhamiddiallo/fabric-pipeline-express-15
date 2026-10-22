-- [Read board] Script sur WH_Hawker, type Requête : une ligne de chiffres et la phrase msg pour Teams
WITH b AS (
  SELECT
    (SELECT COUNT(*) FROM LH_Hawker.bronze.orders) AS raw_rows,
    (SELECT COUNT(*) FROM LH_Hawker.silver.orders_clean) AS clean_rows,
    (SELECT TOP 1 centre FROM LH_Hawker.gold.centre_board
       ORDER BY revenue_sgd DESC) AS top_centre,
    (SELECT CAST(MAX(revenue_sgd) AS varchar(12))
       FROM LH_Hawker.gold.centre_board) AS top_centre_sgd,
    (SELECT TOP 1 dish FROM LH_Hawker.gold.dish_board
       ORDER BY revenue_sgd DESC) AS top_dish,
    (SELECT CAST(MAX(revenue_sgd) AS varchar(12))
       FROM LH_Hawker.gold.dish_board) AS top_dish_sgd,
    (SELECT CAST(SUM(revenue_sgd) AS varchar(12))
       FROM LH_Hawker.gold.centre_board) AS total_sgd
)
SELECT *,
  CONCAT('Hawker board, 9 novembre 2026 : ',
    clean_rows, ' commandes valides sur ', raw_rows,
    ' (', raw_rows - clean_rows, ' écartées par les contraintes). ',
    'Meilleur centre : ', top_centre, ', ', top_centre_sgd, ' SGD. ',
    'Plat roi : ', top_dish, ', ', top_dish_sgd, ' SGD. ',
    'Total : ', total_sgd, ' SGD.') AS msg
FROM b;
