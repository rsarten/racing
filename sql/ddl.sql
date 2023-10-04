
drop table if exists racing.venues;
create table racing.venues(
	venue_id serial primary key,
	"name" varchar(50) not null,
	"state" varchar(3) not null
);

drop table if exists racing.meets;
create table racing.meets(
	meet_id serial primary key,
	venue_id int not null,
	"date" date not null,
	meet_type varchar(20) not null,
	link varchar(255) not null
);

drop table if exists racing.tracks;
create table racing.tracks(
	track_id serial primary key,
	venue_id int not null,
	distance int not null,
	track_type varchar(20) not null
);

drop table if exists racing.meet_details;
create table racing.meets(
	meet_id int primary key,
	condition varchar(255),
	dual_track varchar(1),
	information text,
	penetrometer varchar(20),
	rail varchar(100),
	weather varchar(50)
);

drop table if exists racing.races;
create table racing.races(
	race_id serial primary key,
	meet_id int not null,
	track_id int not null,
	race_number int not null,
	prize_pool int,
	race_time varchar(50),
	winning_time varchar(50)
);

drop table if exists racing.results;
create table racing.results(
	result_id serial primary key,
	race_id int,
	horse_id int,
	jockey_id int,
	trainer_id int,
	finished int,
	margin numeric(8, 2),
	barrier int,
	scratched boolean,
	starting_price numeric(6, 2),
	"weight" varchar(50)
);

drop table if exists racing.horses;
create table racing.horses(
	horse_id serial primary key,
	horse_code varchar(50),
	horse_name varchar(255),
	date_of_birth date
);

drop table if exists racing.jockeys;
create table racing.jockeys(
	jockey_id serial primary key,
	jockey_code varchar(50),
	jockey_name varchar(255)
);

drop table if exists racing.trainers;
create table racing.trainers(
	trainer_id serial primary key,
	trainer_code varchar(50),
	trainer_name varchar(255)
);