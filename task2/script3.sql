UPDATE full_names fn
SET status = (
    SELECT sn.status
    FROM short_names sn
    WHERE sn.name = regexp_replace(fn.name, '\..*$', '')
)
WHERE EXISTS (
    SELECT 1
    FROM short_names sn
    WHERE sn.name = regexp_replace(fn.name, '\..*$', '')
);