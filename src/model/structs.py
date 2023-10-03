from attr import define, field, Factory

from src.export.table_work import (get_venue_id, get_horse_id, 
                                   get_meet_id, get_race_id, 
                                   get_result_id, get_track_id,
                                   get_jockey_id, get_trainer_id,
                                   get_venue_from_meet)
from src.export.table_work import add_entry

@define
class Venue:
    venue: str
    state: str
    venue_id: int = field(kw_only=True, default=None)

    def retrieve_id(self, conn):
        if self.venue_id is None:
            self.venue_id = get_venue_id(self.state, self.venue, conn)

    def add_to_db(self, conn, cascade = True):
        if self.venue_id is None: 
            self.retrieve_id(conn)
        if self.venue_id is None:
            statement = """
            insert into racing.venues(state, venue)
            values (%s, %s) returning venue_id
            """
            values = (self.state, self.venue)
            self.venue_id = add_entry(statement, values, conn)

@define
class Track:
    distance: str = field(converter=int)
    track_type: str
    track_id: int = field(kw_only=True, default=None)
    venue_id: int = field(kw_only=True, default=None)

    def retrieve_id(self, conn):
        if self.track_id is None:
            if self.venue_id is not None:
                self.track_id = get_track_id(self.venue_id, self.distance, conn)

    def add_to_db(self, conn, cascade = True):
        if self.venue_id is None:
            raise AttributeError("Track must have venue_id to write")
        if self.track_id is None: 
            self.retrieve_id(conn)
        if self.track_id is None:
            statement = """
            insert into racing.tracks(venue_id, distance, track_type)
            values (%s, %s, %s) returning track_id
            """
            values = (self.venue_id, self.distance, self.track_type)
            self.venue_id = add_entry(statement, values, conn)

@define
class MeetDetails:
    meet_id: int = field(kw_only=True, default=None)
    distance: str = field(converter=int)
    track_type: str

@define
class Horse:
    horse_name: str
    horse_code: str
    horse_id: int = field(kw_only=True, default=None)
    date_of_birth: str = field(kw_only=True, default=None)

    def retrieve_id(self, conn):
        if self.horse_id is None:
            self.horse_id = get_horse_id(self.horse_code, conn)

    def add_to_db(self, conn, cascade = True):
        if self.horse_id is None:
            self.retrieve_id(conn)
        if self.horse_id is None:
            statement = """
            insert into racing.horses(horse_code, horse_name, date_of_birth)
            values (%s, %s, %s) returning horse_id
            """
            values = (self.horse_code, self.horse_name, self.date_of_birth)
            self.horse_id = add_entry(statement, values, conn)
    
@define
class Jockey:
    jockey_name: str
    jockey_code: str
    jockey_id: int = field(kw_only=True, default=None)

    def retrieve_id(self, conn):
        if self.jockey_id is None:
            self.jockey_id = get_jockey_id(self.jockey_code, conn)

    def add_to_db(self, conn, cascade = True):
        if self.jockey_id is None:
            self.retrieve_id(conn)
        if self.jockey_id is None:
            statement = """
            insert into racing.jockeys(jockey_code, jockey_name)
            values (%s, %s) returning jockey_id
            """
            values = (self.jockey_code, self.jockey_name)
            self.jockey_id = add_entry(statement, values, conn)

@define
class Trainer:
    trainer_name: str
    trainer_code: str
    trainer_id: int = field(kw_only=True, default=None)

    def retrieve_id(self, conn):
        if self.trainer_id is None:
            self.trainer_id = get_trainer_id(self.trainer_code, conn)

    def add_to_db(self, conn, cascade = True):
        if self.trainer_id is None:
            self.retrieve_id(conn)
        if self.trainer_id is None:
            statement = """
            insert into racing.trainers(trainer_code, trainer_name)
            values (%s, %s) returning trainer_id
            """
            values = (self.trainer_code, self.trainer_name)
            self.trainer_id = add_entry(statement, values, conn)

@define
class Result:
    finished: int = field(converter=int)
    margin: float = field(converter=float)
    barrier: int = field(converter=int)
    scratched: bool = field(converter=bool)
    starting_price: float = field(converter=float)
    weight: float = field(converter=float)
    horse: Horse
    jockey: Jockey
    trainer: Trainer
    result_id: int = field(kw_only=True, default=None)
    race_id: int = field(kw_only=True, default=None)

    def retrieve_id(self, conn):
        if self.result_id is None:
            if self.race_id is not None and self.horse is not None:
                self.result_id = get_result_id(self.race_id, self.horse.horse_id, conn)

    def add_to_db(self, conn, cascade = True):
        self.id_to_children(conn)

        if self.race_id is None:
            raise AttributeError("Result must have race_id to write")
        if self.horse is None or self.horse.horse_id is None:
            raise AttributeError("Result must have horse_id to write")
        if self.jockey is None or self.jockey.jockey_id is None:
            raise AttributeError("Result must have jockey_id to write")
        if self.trainer is None or self.trainer.trainer_id is None:
            raise AttributeError("Result must have trainer_id to write")
        
        if self.result_id is None:
            self.retrieve_id(conn)
        if self.result_id is None:
            statement = """
            insert into racing.results(race_id, horse_id, jockey_id,
            trainer_id, finished, margin, barrier, scratched, 
            starting_price, weight)
            values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s) returning result_id
            """
            values = (self.race_id,
                      self.horse.horse_id, 
                      self.jockey.jockey_id,
                      self.trainer.trainer_id,
                      self.finished, 
                      self.margin,
                      self.barrier, 
                      self.scratched, 
                      self.starting_price, 
                      self.weight)
            self.result_id = add_entry(statement, values, conn)

    def id_to_children(self, conn):
        if self.horse is not None:
            if self.horse.horse_id is None:
                self.horse.add_to_db(conn)
        if self.trainer is not None:
            if self.trainer.trainer_id is None:
                self.trainer.add_to_db(conn)
        if self.jockey is not None:
            if self.jockey.jockey_id is None:
                self.jockey.add_to_db(conn)

@define
class Race:
    race_number: int = field(converter=int)
    prize_pool: int = field(converter=int)
    time: str
    results: [Result] = field(kw_only=True, default=None)
    race_id: int = field(kw_only=True, default=None)
    meet_id: int = field(kw_only=True, default=None)
    track: Track = field(kw_only=True, default=None)

    def retrieve_id(self, conn):
        if self.race_id is None:
            if self.meet_id is not None:
                self.race_id = get_race_id(self.meet_id, self.race_number, conn)

    def add_to_db(self, conn, cascade = True):
        if self.track is not None:
            if self.track.venue_id is None:
                self.track.venue_id = get_venue_from_meet(self.meet_id, conn)
            self.track.add_to_db(conn)

        if self.meet_id is None:
            raise AttributeError("Race must have meet_id to write")
        if self.track is None:
            raise AttributeError("Race must have Track to write")
        if self.track.track_id is None:
            raise AttributeError("Race must have Track with track_id to write")
        
        if self.race_id is None:
            self.retrieve_id(conn)
        if self.race_id is None:
            statement = """
            insert into racing.races(meet_id, track_id, race_number, prize_pool, time)
            values (%s, %s, %s, %s, %s) returning race_id
            """
            values = (self.meet_id, 
                      self.track.track_id, 
                      self.race_number, 
                      self.prize_pool, 
                      self.time)
            self.race_id = add_entry(statement, values, conn)
        
        if cascade:
            self.id_to_children()
            for result in self.results:
                result.add_to_db(conn)

    def id_to_children(self):
        if self.race_id is not None:
            if self.results is not None and self.results != []:
                for result in self.results:
                    if result.race_id is None:
                        result.race_id = self.race_id

@define
class Meet:
    date: str
    link: str
    meet_type: str
    meet_id: int = field(kw_only=True, default=None)
    venue_id: int = field(kw_only=True, default=None)
    races: [Race] = field(kw_only=True, default = Factory(list))
    details: MeetDetails = field(kw_only=True, default=None)

    def retrieve_id(self, conn):
        if self.meet_id is None:
            if self.venue_id is not None:
                self.meet_id = get_meet_id(self.venue_id, self.date, self.meet_type, conn)

    def add_to_db(self, conn, cascade = True):
        if self.venue_id is None:
            raise AttributeError("Meet must have venue_id to write")
        if self.meet_id is None:
            self.retrieve_id(conn)
        if self.meet_id is None:
            statement = """
            insert into racing.meets(venue_id, date, meet_type, link)
            values (%s, %s, %s, %s) returning meet_id
            """
            values = (self.venue_id, self.date, self.meet_type, self.link)
            self.meet_id = add_entry(statement, values, conn)
        
        if cascade:
            self.id_to_children()
            for race in self.races:
                race.add_to_db(conn)


    def id_to_children(self):
        """
        Pass down meet_id to races.
        Pass down venue_id to tracks in races.
        """
        if self.meet_id is None:
            raise AttributeError("Meet must have meet_id to be able to pass to children")
        if self.races is not None and self.races != []:
            for race in self.races:
                if race.meet_id is None:
                    race.meet_id = self.meet_id
                if race.track.venue_id is None:
                    race.track.venue_id = self.venue_id

