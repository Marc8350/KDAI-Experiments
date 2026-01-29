from typing import List
from src.tasks.utils_typing import Entity, dataclass

@dataclass
class Art(Entity):
    """Refers to creative works and titles, including magazines, films, plays, operas, and television shows."""
    span: str  # Such as: "Time", "The Seven Year Itch", "Imelda de ' Lambertazzi", "The Gale Storm Show: Oh, Susanna"

@dataclass
class Building(Entity):
    """Refers to man-made structures and facilities, such as museums, airports, and sports arenas."""
    span: str  # Such as: "Henry Ford Museum", "Sheremetyevo International Airport", "Boston Garden"

@dataclass
class Event(Entity):
    """Refers to historical occurrences, revolutions, social movements, or specific organized activities and stages."""
    span: str  # Such as: "Iranian Constitutional Revolution", "Eastwood Scoring Stage", "Bicentennial Boycott movement"

@dataclass
class Location(Entity):
    """Refers to geographical entities, including countries, regions, cities, bodies of water, and geopolitical areas."""
    span: str  # Such as: "Michigan", "Republic of Croatia", "Mediterranean Basin", "Near East", "Cornwall"

@dataclass
class Organization(Entity):
    """Refers to collective groups of people, including international agencies, commercial companies, sports teams, and leagues."""
    span: str  # Such as: "IAEA", "Church's Chicken", "Texas Chicken", "Arsenal", "Tottenham"

@dataclass
class Other(Entity):
    """Refers to entities that do not fit into standard categories, including biological terms (proteins, domains), languages, and chemical elements."""
    span: str  # Such as: "Amphiphysin", "N-terminal", "BAR", "English", "uranium"

@dataclass
class Person(Entity):
    """Refers to individual human beings, including historical figures, authors, directors, and fictional characters."""
    span: str  # Such as: "George Axelrod", "Richard Quine", "Gaetano Donizetti", "Ellaline Terriss", "Edmund Payne"

@dataclass
class Product(Entity):
    """Refers to manufactured items, specifically vehicle models, concept cars, or specific mechanical objects."""
    span: str  # Such as: "Rolls-Royce Phantom", "Rolls-Royce 100EX", "Corvettes-GT1 C6R", "Fairbottom Bobs"

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