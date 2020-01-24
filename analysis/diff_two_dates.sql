select a.location, a.date, a.temperature - b.temperature as diff
from (
    select location, temperature, date, lag(date) over (partition by location order by date) as previous_day
    from (
	select *, row_number() over (partition by location order by date desc) as row_number
    	from temperatures
    ) b
    where row_number in (1, 2)
) a
inner join temperatures b
on a.previous_day = b.date and a.location = b.location;
