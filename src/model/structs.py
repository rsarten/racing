from attr import define, field

from src.export.table_work import (get_venue_id, get_horse_id, 
                                   get_meet_id, get_race_id, 
                                   get_result_id, get_track_id)
from src.export.table_work import add_entry

@define
class Venue:
    venue: str
    state: str
    venue_id: int = field(kw_only=True, default=None)

    def retrieve_id(self, conn):
        if self.venue_id is None:
            self.venue_id = get_venue_id(self.state, self.venue, conn)

    def add_to_db(self, conn):
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
                self.track_id = get_track_id(self.state, self.venue, conn)

    def add_to_db(self, conn):
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

    def add_to_db(self, conn):
        if self.horse_id is None:
            self.retrieve_id(conn)
        if self.horse_id is None:
            statement = """
            insert into racing.horses(horse_code, horse_name, date_of_birth)
            values (%s, %s, %s) returning race_id
            """
            values = (self.horse_code, self.horse_name, self.date_of_birth)
            self.meet_id = add_entry(statement, values, conn)
    
@define
class Jockey:
    jockey_id: int = field(kw_only=True, default=None)
    name: str
    code: str

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
    result_id: int = field(kw_only=True, default=None)
    race_id: int = field(kw_only=True, default=None)
    horse_id: int = field(kw_only=True, default=None)

@define
class Race:
    race_number: int = field(converter=int)
    prize_pool: int = field(converter=int)
    time: str
    results: [Result] = field(kw_only=True, default=None)
    race_id: int = field(kw_only=True, default=None)
    meet_id: int = field(kw_only=True, default=None)
    track_id: int = field(kw_only=True, default=None)

    def retrieve_id(self, conn):
        if self.race_id is None:
            if self.meet_id is not None:
                self.race_id = get_race_id(self.meet_id, self.race_number, conn)

    def add_to_db(self, conn):
        if self.meet_id is None:
            raise AttributeError("Race must have meet_id to write")
        if self.track_id is None:
            raise AttributeError("Race must have track_id to write")
        
        if self.race_id is None:
            self.retrieve_id(conn)
        if self.race_id is None:
            statement = """
            insert into racing.race(meet_id, track_id, race_number, prize_pool, time)
            values (%s, %s, %s, %s, %s) returning race_id
            """
            values = (self.meet_id, self.track_id, self.race_number, self.prize_pool, self.time)
            self.meet_id = add_entry(statement, values, conn)

@define
class Meet:
    date: str
    link: str
    meet_type: str
    meet_id: int = field(kw_only=True, default=None)
    venue_id: int = field(kw_only=True, default=None)
    races: [Race] = field(kw_only=True, default=None)
    details: MeetDetails = field(kw_only=True, default=None)

    def retrieve_id(self, conn):
        if self.meet_id is None:
            if self.venue_id is not None:
                self.meet_id = get_meet_id(self.venue_id, self.date, self.meet_type, conn)

    def add_to_db(self, conn):
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