
-- Database: udatadb2

-- DROP DATABASE udatadb2;

CREATE DATABASE udatadb2
    WITH
    OWNER = postgres
    ENCODING = 'UTF8'
    LC_COLLATE = 'ru_RU.UTF-8'
    LC_CTYPE = 'ru_RU.UTF-8'
    TABLESPACE = pg_default
    CONNECTION LIMIT = -1;

GRANT ALL ON DATABASE udatadb2 TO postgres;

GRANT TEMPORARY, CONNECT ON DATABASE udatadb2 TO PUBLIC;

GRANT ALL ON DATABASE udatadb2 TO udatauser2;