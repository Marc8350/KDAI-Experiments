from typing import List
from src.tasks.utils_typing import Entity, dataclass

@dataclass
class Art(Entity):
    """Refers to titles of creative works including films, magazines, plays, operas, and musical ensembles such as symphonies."""
    span: str  # Such as: "Time", "The Seven Year Itch", "Imelda de ' Lambertazzi", "Hollywood Studio Symphony"

@dataclass
class Building(Entity):
    """Refers to man-made structures and facilities such as museums, airports, stadiums, arenas, and commercial complexes."""
    span: str  # Such as: "Henry Ford Museum", "Sheremetyevo International Airport", "Boston Garden", "Communiplex"

@dataclass
class Event(Entity):
    """Refers to historical occurrences, revolutions, social movements, boycotts, or specific production stages/phases."""
    span: str  # Such as: "Iranian Constitutional Revolution", "Eastwood Scoring Stage", "Bicentennial Boycott movement", "Masaryk Democratic Movement"

@dataclass
class Location(Entity):
    """Refers to geographical and political entities such as countries, regions, cities, territories, and bodies of water."""
    span: str  # Such as: "Republic of Croatia", "Near East", "Northern Europe", "Cornwall", "Dearborn"

@dataclass
class Organization(Entity):
    """Refers to organized groups of people including companies, sports teams, international agencies, commercial franchises, and governing bodies."""
    span: str  # Such as: "IAEA", "Church 's Chicken", "Arsenal", "First Division", "Luc Alphand Aventures"

@dataclass
class Other(Entity):
    """A broad category for entities that do not fit standard labels, including biological/chemical terms, languages, chemical elements, and names of legal acts."""
    span: str  # Such as: "Amphiphysin", "English", "uranium", "United States Freedom Support Act", "SH3 domain"

@dataclass
class Person(Entity):
    """Refers to individual human beings, including real historical figures, contemporary people, and fictional characters."""
    span: str  # Such as: "George Axelrod", "Richard Quine", "Gaetano Donizetti", "Deborah Lurie", "William Morshead"

@dataclass
class Product(Entity):
    """Refers to man-made objects, commercial goods, vehicles, specific models of machinery, and weapon systems."""
    span: str  # Such as: "Rolls-Royce Phantom", "Corvettes - GT1 C6R", "Fairbottom Bobs", "ZU-23-2M Wróbel"

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