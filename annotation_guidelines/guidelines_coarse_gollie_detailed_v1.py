from typing import List
from src.tasks.utils_typing import Entity, dataclass

@dataclass
class Art(Entity):
    """Denotes artistic productions such as literature, movies, periodicals, musical records, tracks, stage plays, and broadcasts."""
    span: str  # Examples include: "Time", "The Seven Year Itch", "The Shawshank Redemption", "Imelda de' Lambertazzi", "Bosch", "L'Atlantide"

@dataclass
class Building(Entity):
    """Includes physical infrastructures and constructed sites like galleries, flight hubs, medical centers, athletic arenas, and sound studios."""
    span: str  # Examples include: "Henry Ford Museum", "Sheremetyevo International Airport", "Boston Garden", "Memorial Sloan-Kettering Cancer Center", "Alpha Recording Studios"

@dataclass
class Event(Entity):
    """Encompasses significant happenings, athletic competitions, ideological groups, civic uprisings, ballot cycles, and structured proceedings."""
    span: str  # Examples include: "French Revolution", "Stanley Cup", "World Cup", "March 1898 elections", "Eastwood Scoring Stage", "Union for a Popular Movement"

@dataclass
class Location(Entity):
    """Relates to terrestrial sites and areas, covering nations, provinces, municipalities, villages, as well as distinct transport routes or drainage areas."""
    span: str  # Examples include: "Croatia", "Mediterranean Basin", "Cornwall", "Michigan", "London", "Northern Europe", "Victoria line"

@dataclass
class Organization(Entity):
    """Signifies collective bodies like businesses, athletic clubs, state departments, armed divisions, and global organizations."""
    span: str  # Examples include: "IAEA", "Church's Chicken", "Arsenal", "Warner Brothers", "Supreme Court", "4th Army", "French National Assembly"

@dataclass
class Other(Entity):
    """Captures miscellaneous items outside standard classes, such as biological molecules, chemical substances, statutes, awards, tongues, and conceptual ideas like astrological signs."""
    span: str  # Examples include: "Amphiphysin", "uranium", "United States Freedom Support Act", "English", "Order of the Republic of Guinea", "Zodiac", "p53 protein"

@dataclass
class Person(Entity):
    """Identifies human figures, whether actual or made-up, including their formal designations and monikers."""
    span: str  # Examples include: "George Axelrod", "Richard Quine", "Gaetano Donizetti", "Mrs. Strong", "Bette Davis", "Jacqueline Bouvier Kennedy", "Binion"

@dataclass
class Product(Entity):
    """Pertains to commercial merchandise, particular automobile series, armaments, mechanical equipment, programs, and computer components."""
    span: str  # Examples include: "Rolls-Royce Phantom", "Corvettes", "Fairbottom Bobs", "ZU-23-2M Wróbel", "Wikipedia", "AR-15", "PDP-1"

ENTITY_DEFINITIONS: List[Entity] = [
    Art,
    Building,
    Event,
    Location,
    Organization,
    Other,
    Person,
    Product,
]