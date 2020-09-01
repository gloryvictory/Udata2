-- View: public.mv_all_projects

-- DROP MATERIALIZED VIEW public.mv_all_projects;

CREATE MATERIALIZED VIEW mv_all_projects
AS
SELECT udata2.ext,
    count(udata2.ext) AS count,
    sum(udata2.size) AS size_sum,
    pg_size_pretty(sum(udata2.size)) AS size_pretty
   FROM udata2
  GROUP BY udata2.ext
 HAVING (udata2.ext::bpchar IN ( SELECT ext.ext
           FROM ext
          WHERE ext.is_project IS NOT NULL))
  ORDER BY (sum(udata2.size)) DESC
WITH DATA;

ALTER TABLE mv_all_projects
    OWNER TO udatauser2;


CREATE OR REPLACE VIEW v_all_projects AS
select
    ext.description,
    mv_all_projects.ext,
    mv_all_projects.count,
    mv_all_projects.size_sum,
    mv_all_projects.size_pretty
from mv_all_projects, ext
where mv_all_projects.ext=ext.ext

