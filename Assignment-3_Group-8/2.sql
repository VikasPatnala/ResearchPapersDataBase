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

SELECT paper.id as id_1,p.citesid_2, p.authors,p.Title, p.Venue_name, p.abstract
FROM paper left JOIN (SELECT distinct cites.id_1,cites.citesid_2,stringify(cites.citesid_2) as authors,paper.Title, paper.Venue_name, paper.abstract
From (cites left join paper on cites.citesid_2=paper.id)) as p ON paper.id = p.id_1;


