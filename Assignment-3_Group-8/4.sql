select distinct a.citesid_2, a.num, stringify(a.citesid_2) as authors,paper.Title, paper.Venue_name, paper.abstract
from
(select cites.citesid_2, count(cites.citesid_2) as num
from cites
GROUP BY cites.citesid_2
order by num desc
LIMIT 20) as a inner join paper on a.citesid_2 = paper.id 
order by num desc