-- Table: public.ext

-- DROP TABLE public.ext;

CREATE TABLE public.ext
(
    ext character(10) COLLATE pg_catalog."default",
    category character(255) COLLATE pg_catalog."default",
    description text COLLATE pg_catalog."default",
    product character(255) COLLATE pg_catalog."default",
    is_project character(255) COLLATE pg_catalog."default"
)
WITH (
    OIDS = FALSE
)
TABLESPACE pg_default;

ALTER TABLE public.ext
    OWNER to udatauser2;