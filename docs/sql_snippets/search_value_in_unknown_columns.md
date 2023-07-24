## Search for a value in unknown column(s)

This can be useful if you are looking for a certain value but don't know the column it's in.

```bigquery
SELECT *
FROM your_table_here t
WHERE REGEXP_CONTAINS(LOWER(TO_JSON_STRING(t)), r'"your_string_value_here"')
```

Note the double-quotes around the search term; the records are converted into JSON 
and since we are looking for a particular string, it will be wrapped in double quotes.
