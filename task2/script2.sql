CREATE TEMP TABLE temp_update AS
SELECT fn.name, sn.status
FROM full_names fn
JOIN short_names sn ON sn.name = regexp_replace(fn.name, '\..*$', '');

UPDATE full_names fn
SET status = tu.status
FROM temp_update tu
WHERE fn.name = tu.name;