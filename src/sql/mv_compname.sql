-- View: public.mv_compname

-- DROP MATERIALIZED VIEW public.mv_compname;

CREATE MATERIALIZED VIEW public.mv_compname
AS
 SELECT udata2.compname,
    sum(udata2.size) AS size_sum,
    pg_size_pretty(sum(udata2.size)) AS size_pretty
   FROM udata2
  GROUP BY udata2.compname
  ORDER BY (sum(udata2.size)) DESC
WITH DATA;

ALTER TABLE public.mv_compname
    OWNER TO udatauser2;