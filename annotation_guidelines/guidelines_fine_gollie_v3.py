from typing import List
from src.tasks.utils_typing import Entity, dataclass

@dataclass
class ArtBroadcastprogram(Entity):
    """Includes any content produced for radio or television, such as talk segments, game shows, sitcoms, and serials."""
    span: str  # e.g., "The Tonight Show", "Jeopardy!", "Friends", "Saturday Night Live", "The Wire"

@dataclass
class ArtFilm(Entity):
    """Pertains to cinematic productions or motion pictures across all genres."""
    span: str  # e.g., "Inception", "Pulp Fiction", "The Godfather", "Seven Samurai"

@dataclass
class ArtMusic(Entity):
    """Denotes musical compositions, including individual songs, full albums, scores, and bands or orchestras."""
    span: str  # e.g., "The Beatles", "Bohemian Rhapsody", "London Philharmonic Orchestra", "Dark Side of the Moon"

@dataclass
class ArtOther(Entity):
    """Covers miscellaneous creative works not fitting into standard categories, like music videos or sculptures."""
    span: str  # e.g., "David by Michelangelo", "Thriller music video", "The Gates installation"

@dataclass
class ArtPainting(Entity):
    """Refers to works of art like paintings, murals, graffiti, or specific artistic photographic series."""
    span: str  # e.g., "The Starry Night", "Guernica", "Mona Lisa", "Girl with a Pearl Earring"

@dataclass
class ArtWrittenart(Entity):
    """Identifies literary works such as novels, periodicals, theatrical plays, and operatic scripts."""
    span: str  # e.g., "The Great Gatsby", "The New Yorker", "Hamlet", "Les Misérables", "The Hobbit"

@dataclass
class BuildingAirport(Entity):
    """Relates to aviation hubs and flight terminals."""
    span: str  # e.g., "Heathrow Airport", "Charles de Gaulle Airport", "John F. Kennedy International"

@dataclass
class BuildingHospital(Entity):
    """Describes medical institutions, infirmaries, and healthcare clinics."""
    span: str  # e.g., "Mayo Clinic", "St. Jude Children's Research Hospital", "Johns Hopkins Hospital"

@dataclass
class BuildingHotel(Entity):
    """Pertains to inns, hotels, and other lodging facilities."""
    span: str  # e.g., "The Ritz-Carlton", "Hilton London", "Burj Al Arab"

@dataclass
class BuildingLibrary(Entity):
    """Refers to archives of books, research libraries, and national collections."""
    span: str  # e.g., "Library of Congress", "Bodleian Library", "New York Public Library"

@dataclass
class BuildingOther(Entity):
    """Covers diverse physical structures not otherwise categorized, such as shrines, galleries, or recording spaces."""
    span: str  # e.g., "The Louvre", "Abbey Road Studios", "St. Patrick's Cathedral", "Guggenheim Museum"

@dataclass
class BuildingRestaurant(Entity):
    """Denotes places to eat, including bistros, cafes, and diners."""
    span: str  # e.g., "McDonald's", "Le Bernardin", "The Cheesecake Factory"

@dataclass
class BuildingSportsfacility(Entity):
    """Refers to athletic arenas, stadiums, and gymnasiums."""
    span: str  # e.g., "Wembley Stadium", "Madison Square Garden", "Allianz Arena"

@dataclass
class BuildingTheater(Entity):
    """Identifies venues for performing arts, such as opera houses and playhouses."""
    span: str  # e.g., "The Old Vic", "Sydney Opera House", "Bolshoi Theatre", "Broadway"

@dataclass
class EventAttackBattleWarMilitaryconflict(Entity):
    """Includes military engagements, wars, specific battles, and armed hostilities."""
    span: str  # e.g., "World War II", "Battle of Gettysburg", "The Gulf War", "Operation Desert Storm"

@dataclass
class EventDisaster(Entity):
    """Pertains to catastrophic occurrences, whether natural or industrial, like quakes or famines."""
    span: str  # e.g., "The Great Fire of London", "Indian Ocean Tsunami", "Chernobyl Disaster"

@dataclass
class EventElection(Entity):
    """Describes political voting events, such as general elections or parliamentary polls."""
    span: str  # e.g., "2020 Presidential Election", "Brexit Referendum", "Canadian Federal Election"

@dataclass
class EventOther(Entity):
    """Covers miscellaneous organized events, social movements, or series not otherwise specified."""
    span: str  # e.g., "Civil Rights Movement", "The Renaissance", "World Economic Forum"

@dataclass
class EventProtest(Entity):
    """Relates to social uprisings, strikes, boycotts, and political revolutions."""
    span: str  # e.g., "Arab Spring", "French Revolution", "Montgomery Bus Boycott"

@dataclass
class EventSportsevent(Entity):
    """Refers to major athletic competitions, tournaments, and match series."""
    span: str  # e.g., "The Olympics", "Super Bowl", "Wimbledon", "Tour de France"

@dataclass
class LocationGpe(Entity):
    """Denotes geopolitical regions such as nations, municipalities, states, and territories."""
    span: str  # e.g., "France", "Tokyo", "New South Wales", "Scandinavian Peninsula", "Chicago"

@dataclass
class LocationBodiesofwater(Entity):
    """Refers to aquatic features like lakes, reservoirs, straits, and rivers."""
    span: str  # e.g., "Lake Superior", "Hoover Dam", "English Channel", "Amazon River"

@dataclass
class LocationIsland(Entity):
    """Describes islands, archipelagos, or landmasses surrounded by water."""
    span: str  # e.g., "Madagascar", "The Galápagos Islands", "Manhattan", "Tasmania"

@dataclass
class LocationMountain(Entity):
    """Identifies mountain peaks, ranges, ridges, and glacial formations."""
    span: str  # e.g., "Mount Everest", "The Andes", "Rocky Mountains", "Franz Josef Glacier"

@dataclass
class LocationOther(Entity):
    """Covers general geographic points, bridges, or boundaries not captured elsewhere."""
    span: str  # e.g., "Golden Gate Bridge", "The Equator", "Tropic of Capricorn"

@dataclass
class LocationPark(Entity):
    """Relates to public parks, protected wildlife areas, and historic sites."""
    span: str  # e.g., "Yellowstone National Park", "Central Park", "Kruger National Park"

@dataclass
class LocationRoadRailwayHighwayTransit(Entity):
    """Refers to infrastructure for transportation, including streets, train lines, and highways."""
    span: str  # e.g., "Route 66", "Trans-Siberian Railway", "M1 Motorway", "London Underground"

@dataclass
class OrganizationCompany(Entity):
    """Describes commercial entities, firms, and corporate brands."""
    span: str  # e.g., "Apple Inc.", "Toyota", "Google", "Coca-Cola"

@dataclass
class OrganizationEducation(Entity):
    """Pertains to academic institutions, including schools, colleges, and research universities."""
    span: str  # e.g., "Harvard University", "Oxford", "Eton College", "Stanford"

@dataclass
class OrganizationGovernmentGovernmentagency(Entity):
    """Refers to legislative bodies, courts, and administrative state departments."""
    span: str  # e.g., "The Pentagon", "European Parliament", "FBI", "The White House"

@dataclass
class OrganizationMediaNewspaper(Entity):
    """Denotes news outlets, broadcasting networks, and magazine publishers."""
    span: str  # e.g., "The New York Times", "BBC", "CNN", "Reuters", "The Economist"

@dataclass
class OrganizationOther(Entity):
    """Covers various groups like military units, non-profits, or international unions not listed elsewhere."""
    span: str  # e.g., "NATO", "Red Cross", "UNICEF", "101st Airborne Division"

@dataclass
class OrganizationPoliticalparty(Entity):
    """Describes groups organized for political purposes and elections."""
    span: str  # e.g., "Democratic Party", "Labour Party", "ANC", "BJP"

@dataclass
class OrganizationReligion(Entity):
    """Relates to religious institutions, denominations, and faith groups."""
    span: str  # e.g., "Catholicism", "Sunni Islam", "The Church of England", "Buddhism"

@dataclass
class OrganizationShoworganization(Entity):
    """Refers to musical groups, dance companies, and performance ensembles."""
    span: str  # e.g., "The Rolling Stones", "Radiohead", "Berlin Philharmonic", "Cirque du Soleil"

@dataclass
class OrganizationSportsleague(Entity):
    """Identifies professional sports associations and league hierarchies."""
    span: str  # e.g., "NBA", "Premier League", "NFL", "La Liga"

@dataclass
class OrganizationSportsteam(Entity):
    """Refers to specific sports clubs and national athletic squads."""
    span: str  # e.g., "Manchester United", "Los Angeles Lakers", "All Blacks", "Ferrari F1 Team"

@dataclass
class OtherAstronomything(Entity):
    """Describes celestial objects like planets, stars, galaxies, and zodiacal symbols."""
    span: str  # e.g., "Mars", "Polaris", "Andromeda Galaxy", "Leo", "Jupiter"

@dataclass
class OtherAward(Entity):
    """Refers to formal honors, prizes, and decorative titles."""
    span: str  # e.g., "Nobel Prize", "Academy Award", "Pulitzer Prize", "Knighthood"

@dataclass
class OtherBiologything(Entity):
    """Identifies biological components like DNA, proteins, cellular structures, and taxons."""
    span: str  # e.g., "Hemoglobin", "Mitochondria", "Enzyme", "Genome", "Drosophila"

@dataclass
class OtherChemicalthing(Entity):
    """Describes chemical elements, molecules, and compounds."""
    span: str  # e.g., "Nitrogen", "Sodium Chloride", "Methane", "H2O"

@dataclass
class OtherCurrency(Entity):
    """Relates to monetary units and specific financial denominations."""
    span: str  # e.g., "Euro", "Yen", "US Dollar", "£50 note"

@dataclass
class OtherDisease(Entity):
    """Refers to health conditions, pathogens, and medical disorders."""
    span: str  # e.g., "Diabetes", "Malaria", "COVID-19", "Alzheimer's disease"

@dataclass
class OtherEducationaldegree(Entity):
    """Describes academic qualifications and certifications."""
    span: str  # e.g., "Master of Arts", "PhD", "MBA", "Bachelor of Science"

@dataclass
class OtherGod(Entity):
    """Refers to divine figures, deities, and mythological creators."""
    span: str  # e.g., "Zeus", "Vishnu", "Allah", "Odin"

@dataclass
class OtherLanguage(Entity):
    """Identifies specific human tongues and dialects."""
    span: str  # e.g., "Mandarin", "Spanish", "Swahili", "Cantonese"

@dataclass
class OtherLaw(Entity):
    """Pertains to legal statutes, international treaties, and constitutional acts."""
    span: str  # e.g., "Geneva Convention", "Magna Carta", "Affordable Care Act"

@dataclass
class OtherLivingthing(Entity):
    """Describes organisms such as fauna, flora, and other biological life forms."""
    span: str  # e.g., "African Elephant", "Oak tree", "Bacteria", "Great White Shark"

@dataclass
class OtherMedical(Entity):
    """Refers to medical branches, diagnostic procedures, and pharmaceutical drugs."""
    span: str  # e.g., "Cardiology", "MRI scan", "Penicillin", "Chemotherapy"

@dataclass
class PersonActor(Entity):
    """Relates to individuals performing in stage, film, or television works."""
    span: str  # e.g., "Meryl Streep", "Tom Hanks", "Viola Davis", "Leonardo DiCaprio"

@dataclass
class PersonArtistAuthor(Entity):
    """Identifies creators such as novelists, composers, and visual artists."""
    span: str  # e.g., "Ernest Hemingway", "Pablo Picasso", "Ludwig van Beethoven", "J.K. Rowling"

@dataclass
class PersonAthlete(Entity):
    """Describes professional competitors in sports and athletics."""
    span: str  # e.g., "Serena Williams", "Lionel Messi", "Usain Bolt", "Tom Brady"

@dataclass
class PersonDirector(Entity):
    """Refers to individuals who oversee the production of movies or theater."""
    span: str  # e.g., "Steven Spielberg", "Alfred Hitchcock", "Greta Gerwig", "Martin Scorsese"

@dataclass
class PersonOther(Entity):
    """Covers individuals who do not fit into specific vocational categories, including historical figures."""
    span: str  # e.g., "Rosa Parks", "Albert Einstein", "Princess Diana", "Neil Armstrong"

@dataclass
class PersonPolitician(Entity):
    """Pertains to government officials, state leaders, and monarchs."""
    span: str  # e.g., "Winston Churchill", "Barack Obama", "Angela Merkel", "Queen Elizabeth II"

@dataclass
class PersonScholar(Entity):
    """Identifies academics, researchers, and scientific experts."""
    span: str  # e.g., "Noam Chomsky", "Stephen Hawking", "Marie Curie", "Jane Goodall"

@dataclass
class PersonSoldier(Entity):
    """Refers to military personnel, commanders, and combatants."""
    span: str  # e.g., "General Patton", "Napoleon Bonaparte", "Dwight D. Eisenhower"

@dataclass
class ProductAirplane(Entity):
    """Describes specific aircraft types and helicopter models."""
    span: str  # e.g., "Boeing 747", "Airbus A380", "Concorde", "Black Hawk"

@dataclass
class ProductCar(Entity):
    """Relates to automobile models and vehicle lines."""
    span: str  # e.g., "Tesla Model S", "Ford Mustang", "Volkswagen Beetle", "Toyota Corolla"

@dataclass
class ProductFood(Entity):
    """Refers to prepared dishes, ingredients, and specific biological crops used as food."""
    span: str  # e.g., "Sushi", "Quinoa", "Parmesan cheese", "Tofu"

@dataclass
class ProductGame(Entity):
    """Identifies video games, board games, and gaming titles."""
    span: str  # e.g., "Minecraft", "The Legend of Zelda", "Monopoly", "Fortnite"

@dataclass
class ProductOther(Entity):
    """Covers miscellaneous manufactured goods and technical components."""
    span: str  # e.g., "iPhone", "Kindle", "PlayStation 5", "Swiss Army Knife"

@dataclass
class ProductShip(Entity):
    """Refers to maritime vessels, boats, and naval ships."""
    span: str  # e.g., "Titanic", "USS Enterprise", "HMS Victory", "Mayflower"

@dataclass
class ProductSoftware(Entity):
    """Describes computer applications, operating systems, and digital tools."""
    span: str  # e.g., "Linux", "Microsoft Excel", "Adobe Photoshop", "Python"

@dataclass
class ProductTrain(Entity):
    """Identifies railway locomotives and specific train models."""
    span: str  # e.g., "Bullet Train", "The Flying Scotsman", "Eurostar", "Orient Express"

@dataclass
class ProductWeapon(Entity):
    """Refers to weaponry, artillery, and defense systems."""
    span: str  # e.g., "AK-47", "Excalibur missile", "Patriot Defense System", "M1 Abrams"

ENTITY_DEFINITIONS: List[Entity] = [
    ArtBroadcastprogram,
    ArtFilm,
    ArtMusic,
    ArtOther,
    ArtPainting,
    ArtWrittenart,
    BuildingAirport,
    BuildingHospital,
    BuildingHotel,
    BuildingLibrary,
    BuildingOther,
    BuildingRestaurant,
    BuildingSportsfacility,
    BuildingTheater,
    EventAttackBattleWarMilitaryconflict,
    EventDisaster,
    EventElection,
    EventOther,
    EventProtest,
    EventSportsevent,
    LocationGpe,
    LocationBodiesofwater,
    LocationIsland,
    LocationMountain,
    LocationOther,
    LocationPark,
    LocationRoadRailwayHighwayTransit,
    OrganizationCompany,
    OrganizationEducation,
    OrganizationGovernmentGovernmentagency,
    OrganizationMediaNewspaper,
    OrganizationOther,
    OrganizationPoliticalparty,
    OrganizationReligion,
    OrganizationShoworganization,
    OrganizationSportsleague,
    OrganizationSportsteam,
    OtherAstronomything,
    OtherAward,
    OtherBiologything,
    OtherChemicalthing,
    OtherCurrency,
    OtherDisease,
    OtherEducationaldegree,
    OtherGod,
    OtherLanguage,
    OtherLaw,
    OtherLivingthing,
    OtherMedical,
    PersonActor,
    PersonArtistAuthor,
    PersonAthlete,
    PersonDirector,
    PersonOther,
    PersonPolitician,
    PersonScholar,
    PersonSoldier,
    ProductAirplane,
    ProductCar,
    ProductFood,
    ProductGame,
    ProductOther,
    ProductShip,
    ProductSoftware,
    ProductTrain,
    ProductWeapon,
]