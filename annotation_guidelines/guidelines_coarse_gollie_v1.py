from typing import List
from src.tasks.utils_typing import Entity, dataclass

@dataclass
class Art(Entity):
    """Relates to imaginative productions and their titles, covering periodicals, cinema, stage plays, and serial programs."""
    span: str  # For example: "National Geographic", "Pulp Fiction", "The Marriage of Figaro", "Breaking Bad"

@dataclass
class Building(Entity):
    """Identifies architectural structures and public facilities, including exhibition halls, transit terminals, and sports complexes."""
    span: str  # For example: "The Louvre", "Heathrow Airport", "Madison Square Garden"

@dataclass
class Event(Entity):
    """Designates historical milestones, social transformations, organized gatherings, or specific performance spaces."""
    span: str  # For example: "The French Revolution", "Woodstock", "Civil Rights Movement", "Abbey Road Studios"

@dataclass
class Location(Entity):
    """Describes geographic regions and political zones, encompassing sovereign states, cities, territories, and bodies of water."""
    span: str  # For example: "Bavaria", "Kingdom of Thailand", "Pacific Ocean", "Scandinavia", "Kyoto"

@dataclass
class Organization(Entity):
    """Categorizes collective entities, such as multinational bodies, commercial enterprises, and professional sports franchises."""
    span: str  # For example: "UNESCO", "Microsoft", "Real Madrid", "National Basketball Association"

@dataclass
class Other(Entity):
    """Captures entities not fitting primary labels, like molecular biology terms (proteins, sequences), spoken languages, and chemical substances."""
    span: str  # For example: "Hemoglobin", "C-terminal", "SH3 domain", "Mandarin Chinese", "Plutonium"

@dataclass
class Person(Entity):
    """Refers to individual humans, whether they are historical figures, creators, or fictional personas."""
    span: str  # For example: "Albert Einstein", "Virginia Woolf", "Steven Spielberg", "Sherlock Holmes", "Marie Curie"

@dataclass
class Product(Entity):
    """Pertains to manufactured commodities, especially vehicle types, automotive prototypes, or specific mechanical apparatuses."""
    span: str  # For example: "Tesla Model S", "Boeing 747", "Leica M6", "Ford Mustang"

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