from typing import List
from src.tasks.utils_typing import Entity, dataclass

@dataclass
class ArtBroadcastprogram(Entity):
    """Refers to television or radio broadcast programs, including game shows, talk shows, and series."""
    span: str  # Such as: "The Gale Storm Show", "12 Corazones", "Jonovision", "Trailer Park Boys"

@dataclass
class ArtFilm(Entity):
    """Refers to movies or films of any genre."""
    span: str  # Such as: "L'Atlantide", "The Shawshank Redemption", "Bosch", "Men in Her Diary"

@dataclass
class ArtMusic(Entity):
    """Refers to musical compositions, songs, albums, or scores."""
    span: str  # Such as: "Hollywood Studio Symphony", "Champion Lover", "Mass in C minor", "Altenberg Lieder"

@dataclass
class ArtOther(Entity):
    """Refers to other forms of art not covered by specific categories, such as sculptures or broadcast segments."""
    span: str  # Such as: "Venus de Milo", "The Today Show", "Bleed Like Me", "Cloud Gate"

@dataclass
class ArtPainting(Entity):
    """Refers to paintings, drawings, graffiti, or specific lens series named as art products."""
    span: str  # Such as: "Production/Reproduction", "Cofiwch Dryweryn", "Touit", "Kamichama Karin"

@dataclass
class ArtWrittenart(Entity):
    """Refers to written works like magazines, novels, plays, operas, or academic theses."""
    span: str  # Such as: "Time", "The Seven Year Itch", "Imelda de ' Lambertazzi", "Writing, Teachers and Students in Graeco-Roman Egypt"

@dataclass
class BuildingAirport(Entity):
    """Refers to airports and aviation hubs."""
    span: str  # Such as: "Sheremetyevo International Airport", "London Luton Airport", "Newark Liberty International Airport"

@dataclass
class BuildingHospital(Entity):
    """Refers to hospitals, medical centers, and clinical facilities."""
    span: str  # Such as: "Memorial Sloan-Kettering Cancer Center", "Yeungnam University Hospital", "Huntington Hospital"

@dataclass
class BuildingHotel(Entity):
    """Refers to hotels, resorts, and lodging establishments."""
    span: str  # Such as: "The Standard Hotel", "Radisson Blu Sea Plaza Hotel", "Flamingo Hotel", "Hotel Sacher Salzburg"

@dataclass
class BuildingLibrary(Entity):
    """Refers to libraries and national or state archives."""
    span: str  # Such as: "Bayerische Staatsbibliothek", "British Library", "Edmon Low Library", "National Library of Laos"

@dataclass
class BuildingOther(Entity):
    """Refers to various buildings and structures such as museums, recording studios, churches, or manors."""
    span: str  # Such as: "Henry Ford Museum", "Alpha Recording Studios", "Church of England parish church", "Villa Las Colinas"

@dataclass
class BuildingRestaurant(Entity):
    """Refers to dining establishments, halls, or delis."""
    span: str  # Such as: "Trumbull", "Carnegie Deli", "Fatburger", "Morrison's"

@dataclass
class BuildingSportsfacility(Entity):
    """Refers to stadiums, gardens, or arenas designed for sports and events."""
    span: str  # Such as: "Boston Garden", "Glenn Warner Soccer Facility", "Scotiabank Place"

@dataclass
class BuildingTheater(Entity):
    """Refers to theaters, opera houses, or performance spaces."""
    span: str  # Such as: "Sanders Theatre", "Pittsburgh Civic Light Opera", "National Paris Opera", "Whitehall Theatre"

@dataclass
class EventAttackBattleWarMilitaryconflict(Entity):
    """Refers to wars, military operations, battles, and general military conflicts."""
    span: str  # Such as: "Vietnam War", "Operation Zipper", "Battle of Romani", "World War I"

@dataclass
class EventDisaster(Entity):
    """Refers to natural disasters, famines, or significant accidents."""
    span: str  # Such as: "1693 Sicily earthquake", "North Korean famine", "1912 North Mount Lyell Disaster", "Trigana Air Service Flight 267"

@dataclass
class EventElection(Entity):
    """Refers to political elections, by-elections, or parliamentary votes."""
    span: str  # Such as: "March 1898 elections", "Elections to the European Parliament", "1982 Mitcham and Morden by-election"

@dataclass
class EventOther(Entity):
    """Refers to movements, campaigns, or institutional milestones categorized as events."""
    span: str  # Such as: "Eastwood Scoring Stage", "Masaryk Democratic Movement", "Union for a Popular Movement", "Haq Movement"

@dataclass
class EventProtest(Entity):
    """Refers to revolutions, rebellions, boycotts, or organized protests."""
    span: str  # Such as: "Iranian Constitutional Revolution", "Bicentennial Boycott", "Irish Rebellion of 1798"

@dataclass
class EventSportsevent(Entity):
    """Refers to sports tournaments, championships, or specific matches."""
    span: str  # Such as: "Stanley Cup", "World Cup", "2008 National Champions", "Olympic event"

@dataclass
class LocationGPE(Entity):
    """Refers to Geopolitical Entities such as countries, cities, states, or districts."""
    span: str  # Such as: "Croatia", "Paris", "Dearborn", "Michigan"

@dataclass
class LocationBodiesofwater(Entity):
    """Refers to bodies of water like lakes, rivers, kills, or seas."""
    span: str  # Such as: "Atatürk Dam Lake", "Arthur Kill", "Norfolk coast", "East China Sea"

@dataclass
class LocationIsland(Entity):
    """Refers to islands, archipelagos, or peninsulas."""
    span: str  # Such as: "Samsat district", "Staten Island", "Maldives", "Mainland"

@dataclass
class LocationMountain(Entity):
    """Refers to mountains, ridges, glaciers, or mountain ranges."""
    span: str  # Such as: "Ruweisat Ridge", "Salamander Glacier", "Mount Diablo", "K2"

@dataclass
class LocationOther(Entity):
    """Refers to specific locations, transit lines, or estates not falling under common categories."""
    span: str  # Such as: "Cartuther", "Victoria line", "Camino Palmero"

@dataclass
class LocationPark(Entity):
    """Refers to parks, national parks, or community complexes."""
    span: str  # Such as: "Gramercy Park", "Shenandoah National Park", "Millennium Park"

@dataclass
class LocationRoadRailwayHighwayTransit(Entity):
    """Refers to roads, bridges, rail lines, or transit systems."""
    span: str  # Such as: "NJT", "Friern Barnet Road", "North Jersey Coast Line", "Outerbridge Crossing"

@dataclass
class OrganizationCompany(Entity):
    """Refers to commercial companies and corporate entities."""
    span: str  # Such as: "Church's Chicken", "WHL", "Warner Brothers", "Taco Cabana"

@dataclass
class OrganizationEducation(Entity):
    """Refers to educational institutions like universities, colleges, or academies."""
    span: str  # Such as: "Belfast Royal Academy", "MIT", "Barnard College", "Latvia University of Life Sciences and Technologies"

@dataclass
class OrganizationGovernmentGovernmentagency(Entity):
    """Refers to government bodies, courts, police departments, or legislative assemblies."""
    span: str  # Such as: "Supreme Court", "Congregazione dei Nobili", "Diet", "US Park Police"

@dataclass
class OrganizationMediaNewspaper(Entity):
    """Refers to media outlets, news organizations, or magazines."""
    span: str  # Such as: "Al Jazeera", "Clash", "TimeOut Melbourne", "Nickelodeon"

@dataclass
class OrganizationOther(Entity):
    """Refers to various organizations like military units, international agencies, or specific groups."""
    span: str  # Such as: "IAEA", "4th Army", "SS Division Nordland", "Quixtar"

@dataclass
class OrganizationPoliticalparty(Entity):
    """Refers to political parties or associations."""
    span: str  # Such as: "Shimpotō", "Al Wafa' Islamic party", "National Liberal Party", "Republican"

@dataclass
class OrganizationReligion(Entity):
    """Refers to religious denominations, churches, or faith-based groups."""
    span: str  # Such as: "Jewish", "Christian", "Catholic Church", "Episcopalians"

@dataclass
class OrganizationShoworganization(Entity):
    """Refers to musical groups, bands, or orchestras."""
    span: str  # Such as: "Mr. Mister", "Bochumer Symphoniker", "Yeah Yeah Yeahs"

@dataclass
class OrganizationSportsleague(Entity):
    """Refers to sports leagues or divisions."""
    span: str  # Such as: "First Division", "NHL", "China League One", "Bundesliga"

@dataclass
class OrganizationSportsteam(Entity):
    """Refers to professional or national sports teams."""
    span: str  # Such as: "Arsenal", "Luc Alphand Aventures", "Tre Kronor", "Audi"

@dataclass
class OtherAstronomything(Entity):
    """Refers to celestial bodies, constellations, or astronomical concepts."""
    span: str  # Such as: "Zodiac", "Algol", "Camelopardalis", "Sun", "Tandun III"

@dataclass
class OtherAward(Entity):
    """Refers to awards, honors, or prizes."""
    span: str  # Such as: "Order of the Republic of Guinea", "Grammy", "European Car of the Year", "Kodansha Manga Award"

@dataclass
class OtherBiologything(Entity):
    """Refers to biological entities such as proteins, domains, or species classifications."""
    span: str  # Such as: "Amphiphysin", "p53 protein", "Ismaridae", "Retinoblastoma protein"

@dataclass
class OtherChemicalthing(Entity):
    """Refers to chemical elements, compounds, or atmospheres."""
    span: str  # Such as: "uranium", "carbon dioxide", "sulfur", "Carbon monoxide"

@dataclass
class OtherCurrency(Entity):
    """Refers to monetary units or specific currency amounts."""
    span: str  # Such as: "Travancore Rupee", "$", "Rs 25 lac crore", "Aruban florin"

@dataclass
class OtherDisease(Entity):
    """Refers to medical conditions, diseases, or physiological states."""
    span: str  # Such as: "Dysentery", "hypothyroidism", "bladder cancer", "Septic shock"

@dataclass
class OtherEducationaldegree(Entity):
    """Refers to academic degrees or titles."""
    span: str  # Such as: "BSc ( Hons ) in physics", "Master of Visual Studies", "Ph.D", "Medical Degree"

@dataclass
class OtherGod(Entity):
    """Refers to deities, religious figures, or gods."""
    span: str  # Such as: "El", "Raijin", "Baglamukhi", "Jesus"

@dataclass
class OtherLanguage(Entity):
    """Refers to languages or language-based names."""
    span: str  # Such as: "English", "Breton-speaking", "Latin", "Arabic"

@dataclass
class OtherLaw(Entity):
    """Refers to acts, treaties, statutes, or legal agreements."""
    span: str  # Such as: "Freedom Support Act", "Thirty Years ' Peace", "AIA", "Rush–Bagot Treaty"

@dataclass
class OtherLivingthing(Entity):
    """Refers to animals, plants, or biological families."""
    span: str  # Such as: "monkeys", "patchouli", "Rafflesiaceae", "zebras"

@dataclass
class OtherMedical(Entity):
    """Refers to medical fields, treatments, or pharmaceuticals."""
    span: str  # Such as: "amitriptyline", "Pediatrics", "cryoprecipitate", "heart transplants"

@dataclass
class PersonActor(Entity):
    """Refers to actors or performers in film and theater."""
    span: str  # Such as: "Ellaline Terriss", "Tchéky Karyo", "Bajpayee", "Reynolds"

@dataclass
class PersonArtistAuthor(Entity):
    """Refers to writers, composers, lyricists, or artists."""
    span: str  # Such as: "Hicks", "George Axelrod", "Gaetano Donizetti", "Deborah Lurie"

@dataclass
class PersonAthlete(Entity):
    """Refers to sports professionals, cyclists, or players."""
    span: str  # Such as: "Neville", "Jaguar", "Bruno Zanoni", "Ernie Johnson"

@dataclass
class PersonDirector(Entity):
    """Refers to film or theater directors."""
    span: str  # Such as: "Richard Quine", "Bob Swaim", "Frank Darabont", "Costner"

@dataclass
class PersonOther(Entity):
    """Refers to notable individuals not classified into other specialized categories."""
    span: str  # Such as: "Holden", "Olympia Elizabeth", "Mrs. Strong", "Binion"

@dataclass
class PersonPolitician(Entity):
    """Refers to political leaders, monarchs, or congressmen."""
    span: str  # Such as: "Emeric", "Rivière", "William III", "Gillis Long"

@dataclass
class PersonScholar(Entity):
    """Refers to academics, researchers, or scientists."""
    span: str  # Such as: "Stedman", "Wurdack", "Davis", "Ted Robert Gurr"

@dataclass
class PersonSoldier(Entity):
    """Refers to military personnel, commanders, or generals."""
    span: str  # Such as: "Krukenberg", "Bruno Loerzer", "Wolfe", "Sir James Outram"

@dataclass
class ProductAirplane(Entity):
    """Refers to aircraft, helicopters, or fighter jets."""
    span: str  # Such as: "EC135T2", "FGR.2s", "Mil Mi-58", "Su-30"

@dataclass
class ProductCar(Entity):
    """Refers to automobiles and concept cars."""
    span: str  # Such as: "Rolls-Royce Phantom", "Corvettes", "Renault 12", "Lancia Thema 8.32"

@dataclass
class ProductFood(Entity):
    """Refers to food items, agricultural products, or specific grape varieties used for wine."""
    span: str  # Such as: "V. labrusca", "yakiniku", "red grape", "Merlot"

@dataclass
class ProductGame(Entity):
    """Refers to video games, gaming consoles, or specific handheld models."""
    span: str  # Such as: "Splinter Cell", "Airforce Delta", "RPG", "Game Boy Micro"

@dataclass
class ProductOther(Entity):
    """Refers to various physical products like computers, cryptographic devices, or engines."""
    span: str  # Such as: "Fairbottom Bobs", "PDP-1", "X11", "SecurID 800"

@dataclass
class ProductShip(Entity):
    """Refers to ships, vessels, frigates, or submersibles."""
    span: str  # Such as: "HMS Chinkara", "Essex", "Embuscade", "Alvin"

@dataclass
class ProductSoftware(Entity):
    """Refers to software, websites, or development tools."""
    span: str  # Such as: "Wikipedia", "AmiPDF", "SQL Server", "micro-PROLOG"

@dataclass
class ProductTrain(Entity):
    """Refers to trains, locomotives, or hybrid vehicle engines."""
    span: str  # Such as: "High Speed Trains", "Royal Scots Grey", "Lexus CT 200h", "Keystone Service"

@dataclass
class ProductWeapon(Entity):
    """Refers to weapons, rifles, or artillery."""
    span: str  # Such as: "ZU-23-2M", "AR-15", "ZSU-57-2", "40mm Bofors gun"

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
    LocationGPE,
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