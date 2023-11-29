with
results as (
	select * 
	from racing.results
),
races as (
	select * 
	from racing.races
),
meets as (
	select *
	from racing.meets
),
tracks as (
	select *
	from racing.tracks
),
venues as (
	select *
	from racing.venues
),
horses as (
	select *
	from racing.horses
),
jockeys as (
	select *
	from racing.jockeys
),
trainers as (
	select *
	from racing.trainers
)

select *
from meets as me
left join venues as ve
using(venue_id)
left join races as ra
using(meet_id)
left join tracks as tr
using(track_id)
left join results as re
using(race_id)
left join horses as ho
using(horse_id)
left join jockeys as jo
using(jockey_id)
left join trainers as tra
using(trainer_id)
order by meet_id, race_id, result_id;