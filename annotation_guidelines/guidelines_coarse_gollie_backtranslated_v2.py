from typing import List
from src.tasks.utils_typing import Entity, dataclass

@dataclass
class Art(Entity):
    """Includes artistic productions like movies, literature, periodicals, musical records, compositions, theatrical operas, and TV broadcasts."""
    span: str  # Such as: "Time", "The Seven Year Itch", "The Shawshank Redemption", "Imelda de' Lambertazzi", "Bosch", "L'Atlantide"

@dataclass
class Building(Entity):
    """Represents artificial constructions and installations, for instance, medical centers, arenas, sound stages, galleries, and air terminals."""
    span: str  # Such as: "Henry Ford Museum", "Sheremetyevo International Airport", "Boston Garden", "Memorial Sloan-Kettering Cancer Center", "Alpha Recording Studios"

@dataclass
class Event(Entity):
    """Denotes past incidents, athletic competitions, sociopolitical shifts, uprisings, voting processes, and structured proceedings."""
    span: str  # Such as: "French Revolution", "Stanley Cup", "World Cup", "March 1898 elections", "Eastwood Scoring Stage", "Union for a Popular Movement"

@dataclass
class Location(Entity):
    """Pertains to physical terrains and areas, such as nations, provinces, urban centers, municipalities, transportation routes, or watersheds."""
    span: str  # Such as: "Croatia", "Mediterranean Basin", "Cornwall", "Michigan", "London", "Northern Europe", "Victoria line"

@dataclass
class Organization(Entity):
    """Identifies structured collectives like corporations, athletic clubs, state departments, armed forces, and global bodies."""
    span: str  # Such as: "IAEA", "Church's Chicken", "Arsenal", "Warner Brothers", "Supreme Court", "4th Army", "French National Assembly"

@dataclass
class Other(Entity):
    """Covers particular entities excluded from other classifications, such as molecular proteins, atomic elements, statutory laws, awards, tongues, and conceptual notions like astrology signs."""
    span: str  # Such as: "Amphiphysin", "uranium", "United States Freedom Support Act", "English", "Order of the Republic of Guinea", "Zodiac", "p53 protein"

@dataclass
class Person(Entity):
    """Signifies human individuals, whether existing or imaginary, encompassing both personal names and formal designations."""
    span: str  # Such as: "George Axelrod", "Richard Quine", "Gaetano Donizetti", "Mrs. Strong", "Bette Davis", "Jacqueline Bouvier Kennedy", "Binion"

@dataclass
class Product(Entity):
    """Designates manufactured items, particular automobile versions, armaments, mechanical equipment, programs, and computer components."""
    span: str  # Such as: "Rolls-Royce Phantom", "Corvettes", "Fairbottom Bobs", "ZU-23-2M Wróbel", "Wikipedia", "AR-15", "PDP-1"

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