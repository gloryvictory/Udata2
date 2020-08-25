-- View: public.mv_geology

-- DROP MATERIALIZED VIEW public.mv_geology;

CREATE MATERIALIZED VIEW public.mv_geology
AS
 SELECT udata2.compname,
    udata2.ext,
    count(udata2.ext) AS count,
    sum(udata2.size) AS size_sum,
    pg_size_pretty(sum(udata2.size)) AS size_pretty
   FROM udata2
  GROUP BY udata2.compname, udata2.ext
 HAVING (udata2.ext::bpchar IN ( SELECT ext.ext
           FROM ext
          WHERE ext.category ~~ 'geol%'::text))
  ORDER BY (sum(udata2.size)) DESC
WITH DATA;

ALTER TABLE public.mv_geology
    OWNER TO udatauser2;