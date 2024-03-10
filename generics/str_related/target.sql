create table test as
select
    a,
    b,
    c
from table a
left join table2 b
    on table.id = table2.id
where a = 1
    and b = 2
    and c = 3;

select
    a,
    b,
    c
from table c
left join table2 dft
    on table.id = table2.id
where a = 1
    and b = 2
    and c = 3;


