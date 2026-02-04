from typing import List
from src.tasks.utils_typing import Entity, dataclass

@dataclass
class Art(Entity):
    """Denotes artistic productions like periodicals, movies, theatrical performances, operas, TV programs, and music ensembles or pieces."""
    span: str  # Examples: "Time", "The Seven Year Itch", "Imelda de ' Lambertazzi", "The Gale Storm Show : Oh , Susanna", "Hollywood Studio Symphony"

@dataclass
class Building(Entity):
    """Describes human-constructed edifices including airfields, galleries, athletic arenas, and designated building clusters."""
    span: str  # Representative cases: "Henry Ford Museum", "Sheremetyevo International Airport", "Boston Garden", "Communiplex"

@dataclass
class Event(Entity):
    """Represents significant history, revolts, societal shifts, or particular arranged phases and happenings."""
    span: str  # For instance: "French Revolution", "Eastwood Scoring Stage", "Bicentennial Boycott movement", "Masaryk Democratic Movement"

@dataclass
class Location(Entity):
    """Includes geographic units like nations, provinces, urban areas, districts, and defined land masses."""
    span: str  # Demonstrations: "Republic of Croatia", "Mediterranean Basin", "Near East", "Cornwall", "Dearborn", "Michigan"

@dataclass
class Organization(Entity):
    """Pertains to corporations, societies, global bodies, athletic clubs, and organizational segments."""
    span: str  # Sample entries: "IAEA", "Church 's Chicken", "Arsenal", "First Division", "Luc Alphand Aventures"

@dataclass
class Other(Entity):
    """Covers varied categories like linguistics, scientific terminology, atomic elements, and legal statutes."""
    span: str  # Illustrative items: "Amphiphysin", "N-terminal", "English", "uranium", "United States Freedom Support Act"

@dataclass
class Person(Entity):
    """Identifies human individuals, encompassing historical figures, real people, or characters from fiction."""
    span: str  # Personages such as: "George Axelrod", "Richard Quine", "Gaetano Donizetti", "Deborah Lurie", "William Morshead"

@dataclass
class Product(Entity):
    """Signifies tradeable items, transport models, mechanical equipment, armaments, and different fabricated objects."""
    span: str  # Such items as: "Rolls-Royce Phantom", "Corvettes - GT1 C6R", "Fairbottom Bobs", "ZU-23-2M Wróbel"

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