from typing import List
from src.tasks.utils_typing import Entity, dataclass

@dataclass
class Art(Entity):
    """Refers to creative works including books, films, magazines, albums, songs, operas, and television shows."""
    span: str  # Such as: "Time", "The Seven Year Itch", "The Shawshank Redemption", "Imelda de' Lambertazzi", "Bosch", "L'Atlantide"

@dataclass
class Building(Entity):
    """Refers to man-made structures and facilities such as museums, airports, hospitals, stadiums, and recording studios."""
    span: str  # Such as: "Henry Ford Museum", "Sheremetyevo International Airport", "Boston Garden", "Memorial Sloan-Kettering Cancer Center", "Alpha Recording Studios"

@dataclass
class Event(Entity):
    """Refers to historical occurrences, sports tournaments, political movements, revolutions, elections, and organized activities."""
    span: str  # Such as: "French Revolution", "Stanley Cup", "World Cup", "March 1898 elections", "Eastwood Scoring Stage", "Union for a Popular Movement"

@dataclass
class Location(Entity):
    """Refers to geographical places including countries, regions, cities, towns, and specific transit lines or basins."""
    span: str  # Such as: "Croatia", "Mediterranean Basin", "Cornwall", "Michigan", "London", "Northern Europe", "Victoria line"

@dataclass
class Organization(Entity):
    """Refers to organized groups such as companies, sports teams, government agencies, military units, and international institutions."""
    span: str  # Such as: "IAEA", "Church's Chicken", "Arsenal", "Warner Brothers", "Supreme Court", "4th Army", "French National Assembly"

@dataclass
class Other(Entity):
    """Refers to specific entities that do not fit into other categories, including proteins, chemical elements, legislative acts, honors, languages, and abstract concepts like zodiac signs."""
    span: str  # Such as: "Amphiphysin", "uranium", "United States Freedom Support Act", "English", "Order of the Republic of Guinea", "Zodiac", "p53 protein"

@dataclass
class Person(Entity):
    """Refers to real or fictional individual human beings, including their names and titles."""
    span: str  # Such as: "George Axelrod", "Richard Quine", "Gaetano Donizetti", "Mrs. Strong", "Bette Davis", "Jacqueline Bouvier Kennedy", "Binion"

@dataclass
class Product(Entity):
    """Refers to consumer goods, specific models of vehicles, weapons, machinery, software, and hardware."""
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