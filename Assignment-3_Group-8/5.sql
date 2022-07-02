select p.k as author1, p.l as author2
from (select distinct c.author_name as k, d.author_name as l, count(*)
	from contribution as c, contribution as d
	where c.id = d.id and c.author_name!=d.author_name and c.author_name < d.author_name
	group by c.author_name,d.author_name) as p

where p.count > 1