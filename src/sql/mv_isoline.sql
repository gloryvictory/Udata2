-- View: public.mv_isoline

-- DROP MATERIALIZED VIEW public.mv_isoline;

CREATE MATERIALIZED VIEW public.mv_isoline
AS
 SELECT udata2.compname,
    udata2.ext,
    count(udata2.ext) AS count,
    sum(udata2.size) AS summary,
    pg_size_pretty(sum(udata2.size)) AS pg_size_pretty
   FROM udata2
  GROUP BY udata2.compname, udata2.ext
 HAVING (udata2.ext::bpchar IN ( SELECT ext.ext
           FROM ext
          WHERE ext.product ~~ 'Isoline%'::text OR ext.product ~~ 'Izoline%'::text))
  ORDER BY (sum(udata2.size)) DESC
WITH DATA;

ALTER TABLE public.mv_isoline
    OWNER TO udatauser2;