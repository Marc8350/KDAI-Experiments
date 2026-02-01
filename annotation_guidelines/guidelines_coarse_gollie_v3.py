from typing import List
from src.tasks.utils_typing import Entity, dataclass

@dataclass
class Art(Entity):
    """Encompasses artistic productions and named titles, such as periodicals, motion pictures, theatrical scripts, and broadcast series."""
    span: str  # Examples: "National Geographic", "Citizen Kane", "The Phantom of the Opera", "Stranger Things"

@dataclass
class Building(Entity):
    """Identifies human-constructed edifices and public installations, including galleries, transit hubs, and athletic stadiums."""
    span: str  # Examples: "The Louvre", "Heathrow Airport", "Madison Square Garden", "Burj Khalifa"

@dataclass
class Event(Entity):
    """Includes significant historical incidents, political uprisings, cultural shifts, or designated organizational phases."""
    span: str  # Examples: "The French Revolution", "Woodstock Music Festival", "The Great Depression", "Apollo 11 Mission"

@dataclass
class Location(Entity):
    """Classifies geographic features and political territories, such as nations, provinces, urban centers, and natural water bodies."""
    span: str  # Examples: "Japan", "Bavaria", "Paris", "Atlantic Ocean", "The Sahara"

@dataclass
class Organization(Entity):
    """Pertains to organized assemblies, spanning global institutions, corporate firms, and professional athletic clubs."""
    span: str  # Examples: "UNESCO", "Microsoft", "FC Barcelona", "The Red Cross", "NASA"

@dataclass
class Other(Entity):
    """Covers miscellaneous entities like linguistic families, chemical substances, or scientific nomenclature such as molecular structures."""
    span: str  # Examples: "Hemoglobin", "Zinc", "Mandarin Chinese", "Kinase domain", "Carbon-14"

@dataclass
class Person(Entity):
    """Represents specific humans, whether they are real historical personalities, writers, or invented literary figures."""
    span: str  # Examples: "Albert Einstein", "Virginia Woolf", "Sherlock Holmes", "Christopher Nolan", "Marie Curie"

@dataclass
class Product(Entity):
    """Relates to commercial goods, particularly automotive types, experimental vehicle designs, or distinct machinery."""
    span: str  # Examples: "Tesla Model S", "Boeing 747", "PlayStation 5", "Ford Mustang", "Hubble Space Telescope"

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