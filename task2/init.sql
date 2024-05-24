CREATE TABLE short_names (
    name VARCHAR(255) PRIMARY KEY,
    status INT
);

CREATE TABLE full_names (
    name VARCHAR(255) PRIMARY KEY,
    status INT
);

-- Генерация тестовых данных
DO $$
DECLARE
    i INT;
    random_status INT;
    random_extension VARCHAR(4);
BEGIN
    FOR i IN 1..700000 LOOP
        random_status := (RANDOM() * 2)::INT;
        random_extension := CASE WHEN RANDOM() < 0.5 THEN '.mp3' ELSE '.wav' END;

        INSERT INTO short_names (name, status) VALUES
        ('name' || i, random_status);

        IF i <= 500000 THEN
            INSERT INTO full_names (name, status) VALUES
            ('name' || i || random_extension, null);
        END IF;
    END LOOP;
END $$;