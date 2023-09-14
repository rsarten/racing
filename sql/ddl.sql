drop table if exists racing.states;
create table racing.states(
	state_id serial primary key,
	state_code varchar(3),
	state_name varchar(50)
);

insert into racing.states(state_code, state_name)
values 
	('NSW', 'New South Wales'),
	('VIC', 'Victoria'),
	('QLD', 'Queensland'),
	('WA', 'Western Australia'),
	('SA', 'South Australia'),
	('TAS', 'Tasmania'),
	('ACT', 'Australian Capital Territory'),
	('NT', 'Northern Territory');

drop table if exists racing.venues;
create table racing.venues(
	venue_id serial primary key,
	"name" varchar(50),
	"state" varchar(3)
);

drop table if exists racing.tracks;
create table racing.tracks(
	track_id serial primary key,
	venue_id int,
	distance int,
	track_type varchar(20)
);

drop table if exists racing.meets;
create table racing.meets(
	meet_id serial primary key,
	venue_id int,
	"date" date,
	condition varchar(255),
	dual_track varchar(1),
	information text,
	penetrometer varchar(20),
	rail varchar(100),
	weather varchar(50),
	"type" varchar(20),
	link varchar(255)
);

drop table if exists racing.races;
create table racing.races(
	race_id serial primary key,
	meet_id int,
	track_id int,
	race_number int,
	prize_pool int,
	"time" timestamp
);

drop table if exists racing.results;
create table racing.results(
	result_id serial primary key,
	race_id int,
	horse_id int,
	finished int,
	margin numeric(8, 2),
	barrier int,
	scratched boolean,
	starting_price numeric(6, 2),
	"weight" varchar(50),
	horse_code varchar(50),
	jokey_name varchar(100),
	jockey_code varchar(50)
);

drop table if exists racing.horses;
create table racing.horses(
	horse_id serial primary key,
	horse_code varchar(50),
	"name" varchar(50)
);