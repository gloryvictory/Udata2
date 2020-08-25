-- View: public.mv_geography

-- DROP MATERIALIZED VIEW public.mv_geography;

CREATE MATERIALIZED VIEW public.mv_geography
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
          WHERE ext.category ~~ 'geog%'::text))
  ORDER BY (sum(udata2.size)) DESC
WITH DATA;

ALTER TABLE public.mv_geography
    OWNER TO udatauser2;