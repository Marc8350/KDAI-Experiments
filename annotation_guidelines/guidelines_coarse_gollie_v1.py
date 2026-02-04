from typing import List
from src.tasks.utils_typing import Entity, dataclass

@dataclass
class Art(Entity):
    """Includes artistic productions like periodicals, movies, theatrical productions, operas, broadcast programs, and musical pieces or bands."""
    span: str  # For example: "Time", "The Seven Year Itch", "Imelda de ' Lambertazzi", "The Gale Storm Show : Oh , Susanna", "Hollywood Studio Symphony"

@dataclass
class Building(Entity):
    """Denotes artificial constructions, for instance, galleries, flight terminals, arenas, and designated architectural sites."""
    span: str  # For instance: "Henry Ford Museum", "Sheremetyevo International Airport", "Boston Garden", "Communiplex"

@dataclass
class Event(Entity):
    """Relates to historical happenings, uprisings, societal movements, or particular arranged phases and occasions."""
    span: str  # Representative cases: "French Revolution", "Eastwood Scoring Stage", "Bicentennial Boycott movement", "Masaryk Democratic Movement"

@dataclass
class Location(Entity):
    """Consists of geographic units like nations, areas, urban centers, provinces, and distinct territories."""
    span: str  # Including: "Republic of Croatia", "Mediterranean Basin", "Near East", "Cornwall", "Dearborn", "Michigan"

@dataclass
class Organization(Entity):
    """Pertains to corporations, groups, global organizations, athletic clubs, and corporate departments."""
    span: str  # Illustrations: "IAEA", "Church 's Chicken", "Arsenal", "First Division", "Luc Alphand Aventures"

@dataclass
class Other(Entity):
    """Covers varied categories including technical terminology, dialects, chemical substances, and legal statutes."""
    span: str  # Like: "Amphiphysin", "N-terminal", "English", "uranium", "United States Freedom Support Act"

@dataclass
class Person(Entity):
    """Identifies individual humans, encompassing actual, historical figures or imaginary personas."""
    span: str  # Such as: "George Axelrod", "Richard Quine", "Gaetano Donizetti", "Deborah Lurie", "William Morshead"

@dataclass
class Product(Entity):
    """Concerns market commodities, automobile types, equipment, armaments, and additional fabricated products."""
    span: str  # Cases like: "Rolls-Royce Phantom", "Corvettes - GT1 C6R", "Fairbottom Bobs", "ZU-23-2M Wróbel"

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