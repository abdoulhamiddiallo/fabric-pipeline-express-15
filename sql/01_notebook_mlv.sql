-- NB_Hawker, langage Spark SQL : une cellule par bloc, puis Exécuter tout

-- Cellule 1 : les trois couches et la table brute
CREATE SCHEMA IF NOT EXISTS bronze;
CREATE SCHEMA IF NOT EXISTS silver;
CREATE SCHEMA IF NOT EXISTS gold;
CREATE TABLE IF NOT EXISTS bronze.orders (order_id STRING, centre STRING, dish STRING, qty STRING, unit_price_sgd STRING, ordered_at STRING);

-- Cellule 2 : argent, typé et filtré par deux contraintes
CREATE OR REPLACE MATERIALIZED LAKE VIEW silver.orders_clean
(
  CONSTRAINT qty_ok CHECK (qty > 0) ON MISMATCH DROP,
  CONSTRAINT price_ok CHECK (unit_price IS NOT NULL) ON MISMATCH DROP
)
COMMENT "Commandes valides des hawker centres"
AS SELECT
  CAST(order_id AS INT) AS order_id,
  centre,
  dish,
  CAST(qty AS INT) AS qty,
  CAST(unit_price_sgd AS DECIMAL(6,2)) AS unit_price,
  CAST(ordered_at AS TIMESTAMP) AS ordered_at,
  CAST(qty AS INT) * CAST(unit_price_sgd AS DECIMAL(6,2)) AS amount
FROM bronze.orders;

-- Cellule 3 : or, le tableau par centre
CREATE OR REPLACE MATERIALIZED LAKE VIEW gold.centre_board
AS SELECT centre, COUNT(*) AS orders, SUM(qty) AS portions, CAST(SUM(amount) AS DECIMAL(10,2)) AS revenue_sgd
FROM silver.orders_clean
GROUP BY centre;

-- Cellule 4 : or, le tableau par plat
CREATE OR REPLACE MATERIALIZED LAKE VIEW gold.dish_board
AS SELECT dish, SUM(qty) AS portions, CAST(SUM(amount) AS DECIMAL(10,2)) AS revenue_sgd
FROM silver.orders_clean
GROUP BY dish;
