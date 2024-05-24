WITH rows_to_update AS (
    SELECT fn.name, sn.status
    FROM full_names fn
    JOIN short_names sn ON sn.name = regexp_replace(fn.name, '\..*$', '')
)

UPDATE full_names fn
SET status = ru.status
FROM rows_to_update ru
WHERE fn.name = ru.name;
