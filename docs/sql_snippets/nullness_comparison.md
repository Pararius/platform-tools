## Nullness comparison

The following example shows how you can compare nullnes between two tables in BigQuery.


```bigquery
SELECT 
    'v1',
    -- Repeat the following for every column you want to compare with,
    -- TIP: use column-selection mode in your editor to write these lines much quicker
    100 * countif(your_column is null) / count(1) AS your_column,
    -- ...
FROM your_table_v1

UNION ALL

SELECT
    'v2',
    -- Repeat the following for every column you want to compare with,
    -- TIP: use column-selection mode in your editor to write these lines much quicker
    100 * countif(your_column is null) / count(1) AS your_column,
    -- ...
FROM your_table_v2

ORDER BY 1
```