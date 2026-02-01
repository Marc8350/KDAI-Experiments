from typing import List
from src.tasks.utils_typing import Entity, dataclass

@dataclass
class Art(Entity):
    """Includes titles of artistic productions and publications, such as cinema, periodicals, theatrical performances, and musical compositions."""
    span: str  # Such as: "The New Yorker", "Inception", "Waiting for Godot", "The Marriage of Figaro"

@dataclass
class Building(Entity):
    """Represents physical infrastructures and human-built establishments, like galleries, transit hubs, and athletic stadiums."""
    span: str  # Such as: "The Guggenheim", "Heathrow Airport", "Madison Square Garden"

@dataclass
class Event(Entity):
    """Pertains to noteworthy historical incidents, political uprisings, cultural shifts, or designated operational phases and organized occasions."""
    span: str  # Such as: "The French Revolution", "The Great Depression", "Woodstock", "Apollo 11 Mission"

@dataclass
class Location(Entity):
    """Denotes spatial and political territories, encompassing nations, provinces, urban centers, maritime features, and regional zones."""
    span: str  # Such as: "Japan", "The Alps", "Lake Victoria", "Scandinavia", "New South Wales"

@dataclass
class Organization(Entity):
    """Identifies formal assemblies of individuals, such as global institutions, private enterprises, athletic clubs, and competitive associations."""
    span: str  # Such as: "The United Nations", "Tesla", "Manchester City", "NBA", "Red Cross"

@dataclass
class Other(Entity):
    """Captures miscellaneous entities falling outside standard classifications, such as linguistic systems, chemical substances, or molecular biology components like proteins and domains."""
    span: str  # Such as: "p53 protein", "Zinc finger", "Mandarin", "Plutonium", "Carbon dioxide"

@dataclass
class Person(Entity):
    """Designates human individuals, including writers, historical actors, filmmakers, or personas from literature and lore."""
    span: str  # Such as: "Marie Curie", "William Shakespeare", "Steven Spielberg", "Sherlock Holmes", "Albert Einstein"

@dataclass
class Product(Entity):
    """Relates to fabricated goods, particularly automotive types, prototype vehicles, or specific pieces of machinery."""
    span: str  # Such as: "Tesla Model 3", "Boeing 747", "Enigma Machine", "Ford Mustang"

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