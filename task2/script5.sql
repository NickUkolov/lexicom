UPDATE full_names fn
SET status = (
    SELECT sn.status
    FROM short_names sn
    WHERE sn.name = regexp_replace(fn.name, '\..*$', '')
)
WHERE regexp_replace(fn.name, '\..*$', '') IN (
    SELECT name
    FROM short_names
);