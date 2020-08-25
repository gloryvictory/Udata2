-- View: public.mv_all

-- DROP MATERIALIZED VIEW public.mv_all;

CREATE MATERIALIZED VIEW mv_all
AS
SELECT udata2.compname,
    udata2.ext,
    count(udata2.ext) AS count,
    sum(udata2.size) AS size_sum,
    pg_size_pretty(sum(udata2.size)) AS size_pretty
   FROM udata2
  GROUP BY udata2.compname, udata2.ext
 HAVING (udata2.ext::bpchar IN ( SELECT DISTINCT ext.ext
           FROM ext))
  ORDER BY (sum(udata2.size)) DESC;

ALTER TABLE mv_all
    OWNER TO udatauser2;