from typing import List
from src.tasks.utils_typing import Entity, dataclass

@dataclass
class Art(Entity):
    """Represents artistic titles and creative productions, such as cinematic films, periodicals, theatrical plays, operas, and broadcast series."""
    span: str  # Examples: "Time", "The Seven Year Itch", "Imelda de ' Lambertazzi", "The Gale Storm Show: Oh, Susanna"

@dataclass
class Building(Entity):
    """Covers constructed facilities and human-made edifices, including stadiums, transport hubs like airports, and galleries or museums."""
    span: str  # Examples: "Henry Ford Museum", "Sheremetyevo International Airport", "Boston Garden"

@dataclass
class Event(Entity):
    """Designates notable historical incidents, uprisings, organized social campaigns, or specific phases and structured activities."""
    span: str  # Examples: "Iranian Constitutional Revolution", "Eastwood Scoring Stage", "Bicentennial Boycott movement"

@dataclass
class Location(Entity):
    """Identifies geographic places and territories, such as sovereign nations, urban centers, provinces, aquatic bodies, and geopolitical zones."""
    span: str  # Examples: "Michigan", "Republic of Croatia", "Mediterranean Basin", "Near East", "Cornwall"

@dataclass
class Organization(Entity):
    """Denotes formal associations and collective bodies, including global organizations, businesses, athletic clubs, and professional sports leagues."""
    span: str  # Examples: "IAEA", "Church's Chicken", "Texas Chicken", "Arsenal", "Tottenham"

@dataclass
class Other(Entity):
    """Categorizes miscellaneous entities falling outside primary classifications, such as linguistic systems, chemical substances, and biological components like proteins or domains."""
    span: str  # Examples: "Amphiphysin", "N-terminal", "BAR", "English", "uranium"

@dataclass
class Person(Entity):
    """Pertains to human individuals, encompassing writers, filmmakers, historical personalities, and personas from fiction."""
    span: str  # Examples: "George Axelrod", "Richard Quine", "Gaetano Donizetti", "Ellaline Terriss", "Edmund Payne"

@dataclass
class Product(Entity):
    """Includes industrial goods and fabricated items, particularly specific mechanical devices, automotive models, and prototype vehicles."""
    span: str  # Examples: "Rolls-Royce Phantom", "Rolls-Royce 100EX", "Corvettes-GT1 C6R", "Fairbottom Bobs"

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