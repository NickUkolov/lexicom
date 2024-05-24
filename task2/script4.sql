UPDATE full_names fn
SET status = sn.status
FROM short_names sn
WHERE sn.name = regexp_replace(fn.name, '\..*$', '');