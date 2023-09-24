from attr import define, field

@define
class Venue:
    venue: str
    state: str
    venue_id: int = field(kw_only=True, default=None)

@define
class Track:
    distance: str = field(converter=int)
    track_type: str
    track_id: int = field(kw_only=True, default=None)
    venue_id: int = field(kw_only=True, default=None)

@define
class MeetDetails:
    meet_id: int = field(kw_only=True, default=None)
    distance: str = field(converter=int)
    track_type: str

@define
class Horse:
    horse_id: int = field(kw_only=True, default=None)
    name: str
    code: str

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

@define
class Meet:
    date: str
    link: str
    meet_type: str
    meet_id: int = field(kw_only=True, default=None)
    venue_id: int = field(kw_only=True, default=None)
    races: [Race] = field(kw_only=True, default=None)
    details: MeetDetails = field(kw_only=True, default=None)

