from typing import List
from src.tasks.utils_typing import Entity, dataclass

@dataclass
class Art(Entity):
    """Encompasses artistic productions like periodicals, movies, theatrical performances, operas, TV programs, as well as musical acts or pieces."""
    span: str  # Examples: "Time", "The Seven Year Itch", "Imelda de ' Lambertazzi", "The Gale Storm Show : Oh , Susanna", "Hollywood Studio Symphony"

@dataclass
class Building(Entity):
    """Identifies human-constructed edifices including museum facilities, aviation hubs, sports arenas, and designated architectural sites."""
    span: str  # Examples: "Henry Ford Museum", "Sheremetyevo International Airport", "Boston Garden", "Communiplex"

@dataclass
class Event(Entity):
    """Designates past happenings, uprisings, social campaigns, or particular arranged phases and occasions."""
    span: str  # Examples: "French Revolution", "Eastwood Scoring Stage", "Bicentennial Boycott movement", "Masaryk Democratic Movement"

@dataclass
class Location(Entity):
    """Consists of geographic units such as nations, provinces, municipalities, regional areas, and distinct lands."""
    span: str  # Examples: "Republic of Croatia", "Mediterranean Basin", "Near East", "Cornwall", "Dearborn", "Michigan"

@dataclass
class Organization(Entity):
    """Pertains to corporate entities, global organizations, athletic squads, commercial groups, and administrative branches."""
    span: str  # Examples: "IAEA", "Church 's Chicken", "Arsenal", "First Division", "Luc Alphand Aventures"

@dataclass
class Other(Entity):
    """Involves various categories like nomenclature in science, linguistic forms, substances on the periodic table, and statutory laws."""
    span: str  # Examples: "Amphiphysin", "N-terminal", "English", "uranium", "United States Freedom Support Act"

@dataclass
class Person(Entity):
    """Represents human individuals, ranging from contemporary or historic figures to imagined personas."""
    span: str  # Examples: "George Axelrod", "Richard Quine", "Gaetano Donizetti", "Deborah Lurie", "William Morshead"

@dataclass
class Product(Entity):
    """Covers tradeable commodities, types of transport, industrial equipment, armaments, and diverse fabricated objects."""
    span: str  # Examples: "Rolls-Royce Phantom", "Corvettes - GT1 C6R", "Fairbottom Bobs", "ZU-23-2M Wróbel"

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