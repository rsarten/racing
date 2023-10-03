with
meets as (
	select 
		meet_id,
		venue_id,
		"date",
		"link"
	from racing.meets
),

races as (
	select
		distinct race_id, meet_id
	from racing.races
)

select
	m_.meet_id,
	venue_id,
	"date",
	"link"
from meets as m_
left join races as r_
 using(meet_id)
where race_id is null
order by m_.meet_id
