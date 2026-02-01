from typing import List
from src.tasks.utils_typing import Entity, dataclass

@dataclass
class Art(Entity):
    """Includes titles of creative productions such as movies, theatrical plays, periodicals, television programs, and operas."""
    span: str  # Such as: "Time", "The Seven Year Itch", "Imelda de ' Lambertazzi", "The Gale Storm Show: Oh, Susanna"

@dataclass
class Building(Entity):
    """Covers human-constructed facilities and edifices, including athletic stadiums, air terminals, and museums."""
    span: str  # Such as: "Henry Ford Museum", "Sheremetyevo International Airport", "Boston Garden"

@dataclass
class Event(Entity):
    """Pertains to organized happenings, historical incidents, societal movements, revolutions, or particular activity phases."""
    span: str  # Such as: "Iranian Constitutional Revolution", "Eastwood Scoring Stage", "Bicentennial Boycott movement"

@dataclass
class Location(Entity):
    """Represents geographic sites and geopolitical zones, such as urban centers, nations, territories, and aquatic bodies."""
    span: str  # Such as: "Michigan", "Republic of Croatia", "Mediterranean Basin", "Near East", "Cornwall"

@dataclass
class Organization(Entity):
    """Designates formal associations and collective entities, including corporate firms, global agencies, professional leagues, and athletic clubs."""
    span: str  # Such as: "IAEA", "Church's Chicken", "Texas Chicken", "Arsenal", "Tottenham"

@dataclass
class Other(Entity):
    """Encompasses items outside conventional classifications, such as chemical components, biological units (like domains or proteins), and languages."""
    span: str  # Such as: "Amphiphysin", "N-terminal", "BAR", "English", "uranium"

@dataclass
class Person(Entity):
    """Describes individual persons, ranging from authors and filmmakers to historical personas and imaginary figures."""
    span: str  # Such as: "George Axelrod", "Richard Quine", "Gaetano Donizetti", "Ellaline Terriss", "Edmund Payne"

@dataclass
class Product(Entity):
    """Consists of fabricated goods, focusing on automotive models, prototype vehicles, and distinct mechanical items."""
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