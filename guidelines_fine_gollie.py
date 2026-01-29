from typing import List
from src.tasks.utils_typing import Entity, dataclass

@dataclass
class ArtBroadcastprogram(Entity):
    """Refers to television or radio programs, including talk shows, game shows, sitcoms, and series."""
    span: str  # Such as: "The Gale Storm Show", "12 Corazones", "Street Cents", "Jonovision", "Trailer Park Boys"

@dataclass
class ArtFilm(Entity):
    """Refers to movies or films of various genres."""
    span: str  # Such as: "L'Atlantide", "The Shawshank Redemption", "Bosch"

@dataclass
class ArtMusic(Entity):
    """Refers to musical works, including songs, albums, scores, and musical groups or symphonies."""
    span: str  # Such as: "Hollywood Studio Symphony", "Atkinson, Danko and Ford", "Champion Lover", "Sex"

@dataclass
class ArtOther(Entity):
    """Refers to miscellaneous artistic works or programs not covered by specific categories, such as statues or music videos."""
    span: str  # Such as: "Venus de Milo", "The Today Show", "Bleed Like Me"

@dataclass
class ArtPainting(Entity):
    """Refers to paintings, graffiti, or specific lens series in photography often treated as art."""
    span: str  # Such as: "Production/Reproduction", "Cofiwch Dryweryn", "Touit", "Loxia", "Batis"

@dataclass
class ArtWrittenart(Entity):
    """Refers to written creative works such as novels, magazines, plays, operas, and novellas."""
    span: str  # Such as: "Time", "The Seven Year Itch", "Imelda de ' Lambertazzi", "Rita Hayworth and Shawshank Redemption"

@dataclass
class BuildingAirport(Entity):
    """Refers to airports and aviation terminals."""
    span: str  # Such as: "Sheremetyevo International Airport", "London Luton Airport", "Newark Liberty International Airport"

@dataclass
class BuildingHospital(Entity):
    """Refers to hospitals, medical centers, and clinics."""
    span: str  # Such as: "Memorial Sloan-Kettering Cancer Center", "Yeungnam University Hospital", "Hokkaido University Hospital"

@dataclass
class BuildingHotel(Entity):
    """Refers to hotels and lodging establishments."""
    span: str  # Such as: "The Standard Hotel", "Radisson Blu Sea Plaza Hotel", "Flamingo Hotel"

@dataclass
class BuildingLibrary(Entity):
    """Refers to libraries and journal archives."""
    span: str  # Such as: "Bayerische Staatsbibliothek", "British Library", "Berlin State Library", "Edmon Low Library"

@dataclass
class BuildingOther(Entity):
    """Refers to various physical structures and buildings not covered by specific categories, like museums, studios, or religious buildings."""
    span: str  # Such as: "Henry Ford Museum", "Communiplex", "Alpha Recording Studios", "Saint Matthew Church"

@dataclass
class BuildingRestaurant(Entity):
    """Refers to dining establishments, delis, and cafes."""
    span: str  # Such as: "Trumbull", "Carnegie Deli", "Fatburger"

@dataclass
class BuildingSportsfacility(Entity):
    """Refers to stadiums, gardens, sports centers, and athletic complexes."""
    span: str  # Such as: "Boston Garden", "Sports Center", "Glenn Warner Soccer Facility"

@dataclass
class BuildingTheater(Entity):
    """Refers to theaters, opera houses, and performing arts venues."""
    span: str  # Such as: "Sanders Theatre", "Pittsburgh Civic Light Opera", "National Paris Opera"

@dataclass
class EventAttackBattleWarMilitaryconflict(Entity):
    """Refers to wars, battles, military operations, and armed conflicts."""
    span: str  # Such as: "Vietnam War", "Easter Offensive", "Operation Zipper", "Battle of Romani"

@dataclass
class EventDisaster(Entity):
    """Refers to natural or man-made disasters, including earthquakes, famines, and industrial accidents."""
    span: str  # Such as: "1693 Sicily earthquake", "North Korean famine", "1912 North Mount Lyell Disaster"

@dataclass
class EventElection(Entity):
    """Refers to political elections, by-elections, and votes for parliament."""
    span: str  # Such as: "March 1898 elections", "Elections to the European Parliament", "Mitcham and Morden by-election"

@dataclass
class EventOther(Entity):
    """Refers to miscellaneous events, movements, or series not covered by specific categories."""
    span: str  # Such as: "Eastwood Scoring Stage", "Masaryk Democratic Movement", "Union for a Popular Movement"

@dataclass
class EventProtest(Entity):
    """Refers to revolutions, boycotts, protests, and social uprisings."""
    span: str  # Such as: "Iranian Constitutional Revolution", "Bicentennial Boycott", "Iranian revolution"

@dataclass
class EventSportsevent(Entity):
    """Refers to sports championships, tournaments, and specific game series."""
    span: str  # Such as: "Stanley Cup", "World Cup", "National Champions"

@dataclass
class LocationGpe(Entity):
    """Refers to geopolitical entities such as countries, cities, states, and regions."""
    span: str  # Such as: "Croatian", "Republic of Croatia", "Mediterranean Basin", "Cornwall", "Los Angeles"

@dataclass
class LocationBodiesofwater(Entity):
    """Refers to lakes, dams, kills, and coastlines."""
    span: str  # Such as: "Atatürk Dam Lake", "Arthur Kill", "Norfolk coast"

@dataclass
class LocationIsland(Entity):
    """Refers to islands, archipelagos, or districts located on islands."""
    span: str  # Such as: "Samsat", "Staten Island", "Laccadives", "Maldives"

@dataclass
class LocationMountain(Entity):
    """Refers to mountains, ridges, and glaciers."""
    span: str  # Such as: "Ruweisat Ridge", "Miteirya Ridge", "Salamander Glacier", "Mount Diablo"

@dataclass
class LocationOther(Entity):
    """Refers to general locations, lines, or areas not covered by other categories."""
    span: str  # Such as: "Cartuther", "Victoria line", "Northern City Line", "West Gate Bridge"

@dataclass
class LocationPark(Entity):
    """Refers to parks, national parks, and specific historic districts or community complexes."""
    span: str  # Such as: "Gramercy Park", "Painted Desert Community Complex", "Shenandoah National Park"

@dataclass
class LocationRoadRailwayHighwayTransit(Entity):
    """Refers to roads, rail lines, subway lines, and transit links."""
    span: str  # Such as: "NJT", "Newark-Elizabeth Rail Link", "Friern Barnet Road", "North Jersey Coast Line"

@dataclass
class OrganizationCompany(Entity):
    """Refers to commercial businesses, corporations, and franchises."""
    span: str  # Such as: "Church's Chicken", "Two Pesos, Inc.", "Taco Cabana, Inc.", "WHL"

@dataclass
class OrganizationEducation(Entity):
    """Refers to schools, universities, colleges, and academic academies."""
    span: str  # Such as: "Belfast Royal Academy", "Ulster College of Physical Education", "MIT", "Barnard College"

@dataclass
class OrganizationGovernmentGovernmentagency(Entity):
    """Refers to courts, councils, legislative bodies, and government organizations."""
    span: str  # Such as: "Supreme Court", "Congregazione dei Nobili", "Diet", "New York City Council"

@dataclass
class OrganizationMediaNewspaper(Entity):
    """Refers to news organizations, newspapers, magazines, and TV networks."""
    span: str  # Such as: "Al Jazeera", "Clash", "TimeOut Melbourne", "Fuse"

@dataclass
class OrganizationOther(Entity):
    """Refers to organizations not covered by other categories, such as armies, divisions, or consortia."""
    span: str  # Such as: "IAEA", "4th Army", "SS Division Nordland"

@dataclass
class OrganizationPoliticalparty(Entity):
    """Refers to political parties and groups."""
    span: str  # Such as: "Shimpotō", "Al Wafa' Islamic party", "National Liberal Party"

@dataclass
class OrganizationReligion(Entity):
    """Refers to religious denominations, churches, and faith-based schools."""
    span: str  # Such as: "Jewish", "Christian", "Catholic Church", "non-denominational Christian"

@dataclass
class OrganizationShoworganization(Entity):
    """Refers to musical bands, orchestras, and entertainment troupes."""
    span: str  # Such as: "Mr. Mister", "Lizzy", "Bochumer Symphoniker", "Yeah Yeah Yeahs"

@dataclass
class OrganizationSportsleague(Entity):
    """Refers to sports divisions, leagues, and athletic associations."""
    span: str  # Such as: "First Division", "NHL", "China League One"

@dataclass
class OrganizationSportsteam(Entity):
    """Refers to professional and national sports teams."""
    span: str  # Such as: "Arsenal", "Tottenham", "Luc Alphand Aventures", "Swedish national men's ice hockey team"

@dataclass
class OtherAstronomything(Entity):
    """Refers to celestial bodies like stars, planets, constellations, and signs of the zodiac."""
    span: str  # Such as: "Zodiac", "Algol", "Caput Larvae", "42 Camelopardalis", "Sun"

@dataclass
class OtherAward(Entity):
    """Refers to honors, medals, awards, and formal titles of recognition."""
    span: str  # Such as: "Order of the Republic", "Grand Commander of the Order of the Niger", "Grammy", "European Car of the Year"

@dataclass
class OtherBiologything(Entity):
    """Refers to biological entities such as proteins, domains, genes, families, and orders of insects."""
    span: str  # Such as: "Amphiphysin", "N-terminal", "lipid", "BAR domain", "p53 protein", "Hymenoptera"

@dataclass
class OtherChemicalthing(Entity):
    """Refers to chemical elements and compounds."""
    span: str  # Such as: "uranium", "carbon dioxide", "sulfur", "Carbon monoxide"

@dataclass
class OtherCurrency(Entity):
    """Refers to units of money and currency denominations."""
    span: str  # Such as: "Travancore Rupee", "$", "Rs 25 lac crore"

@dataclass
class OtherDisease(Entity):
    """Refers to medical conditions, illnesses, and epidemics."""
    span: str  # Such as: "Dysentery Epidemic", "hypothyroidism", "bladder cancer"

@dataclass
class OtherEducationaldegree(Entity):
    """Refers to academic degrees and certifications."""
    span: str  # Such as: "BSc ( Hons ) in physics", "Master of Visual Studies", "Bachelor of Education", "Ph.D."

@dataclass
class OtherGod(Entity):
    """Refers to deities, creators, and gods from various religions or mythologies."""
    span: str  # Such as: "El", "Raijin", "Fujin", "Baglamukhi"

@dataclass
class OtherLanguage(Entity):
    """Refers to specific languages or dialects."""
    span: str  # Such as: "English", "Breton-speaking", "Latin", "Hebrew", "Arabic"

@dataclass
class OtherLaw(Entity):
    """Refers to statutes, acts, treaties, and federal laws."""
    span: str  # Such as: "United States Freedom Support Act", "Thirty Years' Peace", "America Invents Act"

@dataclass
class OtherLivingthing(Entity):
    """Refers to animals, plants, and other biological organisms."""
    span: str  # Such as: "monkeys", "insects", "patchouli", "Rafflesiaceae", "Euphorbiaceae"

@dataclass
class OtherMedical(Entity):
    """Refers to medical fields, procedures, and pharmacological treatments."""
    span: str  # Such as: "amitriptyline", "Pediatrics", "pediatrician", "cryoprecipitate"

@dataclass
class PersonActor(Entity):
    """Refers to performers in film, theater, and television."""
    span: str  # Such as: "Ellaline Terriss", "Edmund Payne", "Tchéky Karyo", "Fernando Rey", "Bajpayee"

@dataclass
class PersonArtistAuthor(Entity):
    """Refers to writers, authors, poets, and musicians."""
    span: str  # Such as: "George Axelrod", "Gaetano Donizetti", "Stephen King", "Deborah Lurie"

@dataclass
class PersonAthlete(Entity):
    """Refers to professional sports players, cyclists, and quarterbacks."""
    span: str  # Such as: "Neville", "Tozawa", "Jaguar", "Bruno Zanoni", "Sam"

@dataclass
class PersonDirector(Entity):
    """Refers to directors of films, plays, and other artistic productions."""
    span: str  # Such as: "Richard Quine", "Bob Swaim", "Frank Darabont", "Jonze"

@dataclass
class PersonOther(Entity):
    """Refers to individuals not covered by specific professional categories, including historical figures and famous family members."""
    span: str  # Such as: "Holden", "Campbell", "Wallis", "Rockefeller", "Bette Davis"

@dataclass
class PersonPolitician(Entity):
    """Refers to government leaders, monarchs, and political representatives."""
    span: str  # Such as: "Emeric", "Rivière", "William III", "Mary II", "Barack Obama"

@dataclass
class PersonScholar(Entity):
    """Refers to academics, scientists, and researchers."""
    span: str  # Such as: "Stalmine", "Stedman", "Wurdack", "Davis"

@dataclass
class PersonSoldier(Entity):
    """Refers to military personnel and commanders."""
    span: str  # Such as: "Krukenberg", "Helmuth Weidling", "Bruno Loerzer", "Wolfe"

@dataclass
class ProductAirplane(Entity):
    """Refers to specific aircraft models and helicopters."""
    span: str  # Such as: "EC135T2 CPDS", "FGR.2s", "Mil Mi-58", "Mil Mi-28"

@dataclass
class ProductCar(Entity):
    """Refers to car models and automotive platforms."""
    span: str  # Such as: "Rolls-Royce Phantom", "Corvettes", "Renault 12", "Fiat 128"

@dataclass
class ProductFood(Entity):
    """Refers to food items, ingredients, and specific crop varieties."""
    span: str  # Such as: "V. labrusca", "yakiniku", "red grape"

@dataclass
class ProductGame(Entity):
    """Refers to video games and gaming sequels."""
    span: str  # Such as: "Splinter Cell", "Airforce Delta", "Hardcore RPG"

@dataclass
class ProductOther(Entity):
    """Refers to miscellaneous products, technical components, or items like museum pieces."""
    span: str  # Such as: "Fairbottom Bobs", "PDP-1", "X11", "E-mount"

@dataclass
class ProductShip(Entity):
    """Refers to naval vessels, ships, and landing craft."""
    span: str  # Such as: "HMS Chinkara", "Congress", "Essex", "Embuscade"

@dataclass
class ProductSoftware(Entity):
    """Refers to computer software, platforms, and programming tools."""
    span: str  # Such as: "Wikipedia", "Apdf", "AmiPDF", "BIDS", "SQL Server"

@dataclass
class ProductTrain(Entity):
    """Refers to specific train models and locomotive types."""
    span: str  # Such as: "High Speed Trains", "55022 Royal Scots Grey", "Lexus CT 200h"

@dataclass
class ProductWeapon(Entity):
    """Refers to firearms, artillery, and military weapons systems."""
    span: str  # Such as: "ZU-23-2M Wróbel", "AR-15", "M-14", "ZSU-57-2"

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