-- View: public.mv_all_games

-- DROP MATERIALIZED VIEW public.mv_all_games;

CREATE MATERIALIZED VIEW mv_games
TABLESPACE pg_default
AS
 SELECT udata2.compname,
    udata2.folder,
    udata2.ext
   FROM udata2
  WHERE (udata2.folder ~~ '%game%'::text OR udata2.folder ~~ '%игры%'::text  OR udata2.folder ~~ '%игра%'::text) AND udata2.ext::text ~~ 'exe'::text AND udata2.folder !~~ '%C:\Windows\%'::TEXT
  ORDER BY udata2.compname
WITH DATA;

ALTER TABLE mv_games
    OWNER TO udatauser2;


CREATE OR REPLACE VIEW v_games AS
select
    mv_games.compname,
	mv_games.folder,
	mv_games.ext
from mv_games
