DROP FUNCTION abc();
CREATE OR REPLACE FUNCTION abc()
returns table (
	f1 text,
	second text,
	third text
)
language plpgsql
AS $$
declare 
r record;
h record;
BEGIN
	for r in
		select distinct d.fir as fir,d.sec as sec,d.thi as thi 
		from
		(
		(select c.x as fir,c.y as sec,c.z as thi	
		from(
				select a.id_1 as x, b.id_1 as y, b.citesid_2 as z
				from (cites as a inner join cites as b on a.citesid_2 = b.id_1) 
				where b.id_1 is not NULL
			) as c inner join cites as d on c.z = d.id_1
			where c.x = d.citesid_2)
		UNION
		(select c.x as fir,c.y as sec,c.z as thi
		from(
			select a.id_1 as x, b.id_1 as y, b.citesid_2 as z
			from (cites as a inner join cites as b on a.citesid_2 = b.id_1) 
			where b.id_1 is not NULL and b.citesId_2 in (
				SELECT citesId_2
				From cites
				where id_1 = a.id_1
			)
		) as c	
		)
		) as d
		where d.fir!=d.sec and d.sec!=d.thi and d.thi!=d.fir
	loop
	for h in 
		select f1.id as id1,second.id as id2,third.id as id3,f1.author_name as f1author, second.author_name as SecondAuthor,third.author_name as thirdAuthor
		from 
			(Select author_name,id from contribution where id = r.fir) as f1,
			(Select author_name,id from contribution where id = r.sec) as second,
			(Select author_name,id from contribution where id = r.thi) as third

		loop
		
		f1 = h.f1author;
		second = h.secondAuthor;
		third = h.thirdAuthor; 
		if(h.f1author<h.thirdAuthor and h.secondAuthor<h.thirdAuthor)
		then
			if(h.f1author < h.secondAuthor)
			then
				f1 = h.f1author;
				second = h.secondAuthor;
				third = h.thirdAuthor;
			else
				f1 = h.secondAuthor;
				second = h.f1author;
				third = h.thirdAuthor;
			end if;
		elsif(h.f1author<h.secondAuthor and h.thirdAuthor<h.secondAuthor)
		then
			if(h.f1author < h.thirdAuthor)
			then
				f1 = h.f1author;
				second = h.thirdAuthor;
				third = h.secondAuthor;
			else
				f1 = h.thirdauthor;
				second = h.f1author;
				third = h.secondAuthor;
			end if;
		elsif(h.secondAuthor<h.f1author and h.thirdAuthor<h.f1author)
		then
			if(h.secondAuthor < h.thirdAuthor)
			then
				f1 = h.secondAuthor;
				second = h.thirdAuthor;
				third = h.f1author; 
			else
				f1 = h.thirdauthor;
				second = h.secondAuthor;
				third = h.f1author;
			end if;
		end if;

		return next;
		end loop;
	end loop;
	
END $$;

select a.f1,a.second,a.third,count(*) 
from abc() as a
where a.f1!=a.second and a.second!=a.third and a.third !=a.f1
GROUP BY(a.f1,a.second,a.third)
ORDER BY count(*) Desc