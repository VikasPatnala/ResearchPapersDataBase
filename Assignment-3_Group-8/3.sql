CREATE OR REPLACE FUNCTION stringify(paperid integer)
returns TEXT
language plpgsql
AS $$
declare 
au text default '';
r record;
BEGIN
	for r in
	select author_name from contribution where paperid = id order by contrib asc
	loop
	au = concat_ws(', ',au,r.author_name);
	end loop;
	au = substr(au,3);
	RETURN au;
END $$;

SELECT paper.id as X,u.Z as Z, u.authors,u.Title, u.Venue_name, u.abstract
FROM paper left JOIN (
select distinct p.X, p.Z, stringify(p.Z) as authors,paper.Title, paper.Venue_name, paper.abstract
From
(SELECT DISTINCT b.citesid_2 as X, a.id_1 as Z
FROM cites as a inner join cites as b on a.citesid_2 = b.id_1
where b.citesid_2 != a.id_1) as p left join paper on p.Z = paper.id) as u ON paper.id = u.X;