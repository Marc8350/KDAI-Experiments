from typing import List
from src.tasks.utils_typing import Entity, dataclass

@dataclass
class ArtBroadcastprogram(Entity):
    """Includes content broadcast via radio or television, such as sitcoms, series, and talk or game shows."""
    span: str  # For example: "12 Corazones", "Jonovision", "The Gale Storm Show", "Trailer Park Boys", "Street Cents"

@dataclass
class ArtFilm(Entity):
    """Covers cinematic works and motion pictures of any genre."""
    span: str  # Examples: "Bosch", "The Shawshank Redemption", "L'Atlantide"

@dataclass
class ArtMusic(Entity):
    """Pertains to musical creations, including albums, songs, symphonies, orchestral scores, and bands."""
    span: str  # e.g., "Sex", "Champion Lover", "Atkinson, Danko and Ford", "Hollywood Studio Symphony"

@dataclass
class ArtOther(Entity):
    """Encompasses various artistic programs or works not categorized elsewhere, such as music videos or sculptures."""
    span: str  # Such as: "Bleed Like Me", "The Today Show", "Venus de Milo"

@dataclass
class ArtPainting(Entity):
    """Refers to visual art like graffiti and paintings, as well as specific photography lens series."""
    span: str  # For instance: "Batis", "Loxia", "Touit", "Cofiwch Dryweryn", "Production/Reproduction"

@dataclass
class ArtWrittenart(Entity):
    """Relates to creative literary works, including plays, novels, magazines, novellas, and operas."""
    span: str  # Examples include: "Rita Hayworth and Shawshank Redemption", "Imelda de ' Lambertazzi", "The Seven Year Itch", "Time"

@dataclass
class BuildingAirport(Entity):
    """Refers to aviation hubs and airport terminals."""
    span: str  # e.g., "Newark Liberty International Airport", "London Luton Airport", "Sheremetyevo International Airport"

@dataclass
class BuildingHospital(Entity):
    """Covers medical centers, clinics, and hospital facilities."""
    span: str  # For example: "Hokkaido University Hospital", "Yeungnam University Hospital", "Memorial Sloan-Kettering Cancer Center"

@dataclass
class BuildingHotel(Entity):
    """Includes lodging facilities and hotels."""
    span: str  # Such as: "Flamingo Hotel", "Radisson Blu Sea Plaza Hotel", "The Standard Hotel"

@dataclass
class BuildingLibrary(Entity):
    """Pertains to archive collections and libraries."""
    span: str  # e.g., "Edmon Low Library", "Berlin State Library", "British Library", "Bayerische Staatsbibliothek"

@dataclass
class BuildingOther(Entity):
    """Encompasses diverse physical edifices not fitting specific types, such as religious sites, museums, or recording studios."""
    span: str  # For instance: "Saint Matthew Church", "Alpha Recording Studios", "Communiplex", "Henry Ford Museum"

@dataclass
class BuildingRestaurant(Entity):
    """Refers to eateries, cafes, and delicatessens."""
    span: str  # Examples: "Fatburger", "Carnegie Deli", "Trumbull"

@dataclass
class BuildingSportsfacility(Entity):
    """Relates to athletic complexes, stadiums, sports centers, and indoor arenas."""
    span: str  # Such as: "Glenn Warner Soccer Facility", "Sports Center", "Boston Garden"

@dataclass
class BuildingTheater(Entity):
    """Covers performing arts locations, opera houses, and theaters."""
    span: str  # e.g., "National Paris Opera", "Pittsburgh Civic Light Opera", "Sanders Theatre"

@dataclass
class EventAttackBattleWarMilitaryconflict(Entity):
    """Pertains to armed conflicts, military operations, battles, and wars."""
    span: str  # For example: "Battle of Romani", "Operation Zipper", "Easter Offensive", "Vietnam War"

@dataclass
class EventDisaster(Entity):
    """Includes both industrial accidents and natural catastrophes, such as famines or earthquakes."""
    span: str  # Such as: "1912 North Mount Lyell Disaster", "North Korean famine", "1693 Sicily earthquake"

@dataclass
class EventElection(Entity):
    """Refers to political voting events, including by-elections and parliamentary polls."""
    span: str  # Examples: "Mitcham and Morden by-election", "Elections to the European Parliament", "March 1898 elections"

@dataclass
class EventOther(Entity):
    """Covers miscellaneous social movements, series, or events not otherwise specified."""
    span: str  # e.g., "Union for a Popular Movement", "Masaryk Democratic Movement", "Eastwood Scoring Stage"

@dataclass
class EventProtest(Entity):
    """Relates to social uprisings, boycotts, revolutions, and public protests."""
    span: str  # For instance: "Iranian revolution", "Bicentennial Boycott", "Iranian Constitutional Revolution"

@dataclass
class EventSportsevent(Entity):
    """Refers to athletic tournaments, specific match series, and championships."""
    span: str  # Such as: "National Champions", "World Cup", "Stanley Cup"

@dataclass
class LocationGpe(Entity):
    """Includes geopolitical territories like states, cities, regions, and nations."""
    span: str  # e.g., "Los Angeles", "Cornwall", "Mediterranean Basin", "Republic of Croatia", "Croatian"

@dataclass
class LocationBodiesofwater(Entity):
    """Pertains to dams, coastlines, lakes, and kills."""
    span: str  # Examples: "Norfolk coast", "Arthur Kill", "Atatürk Dam Lake"

@dataclass
class LocationIsland(Entity):
    """Covers archipelagos, islands, or specific districts situated on islands."""
    span: str  # For instance: "Maldives", "Laccadives", "Staten Island", "Samsat"

@dataclass
class LocationMountain(Entity):
    """Refers to glaciers, mountain ridges, and peaks."""
    span: str  # Such as: "Mount Diablo", "Salamander Glacier", "Miteirya Ridge", "Ruweisat Ridge"

@dataclass
class LocationOther(Entity):
    """Encompasses general geographic areas, bridges, or transit lines not categorized elsewhere."""
    span: str  # e.g., "West Gate Bridge", "Northern City Line", "Victoria line", "Cartuther"

@dataclass
class LocationPark(Entity):
    """Relates to national parks, community complexes, and designated historic districts."""
    span: str  # For example: "Shenandoah National Park", "Painted Desert Community Complex", "Gramercy Park"

@dataclass
class LocationRoadRailwayHighwayTransit(Entity):
    """Includes rail lines, roads, transit connections, and subway routes."""
    span: str  # Such as: "North Jersey Coast Line", "Friern Barnet Road", "Newark-Elizabeth Rail Link", "NJT"

@dataclass
class OrganizationCompany(Entity):
    """Refers to corporate entities, franchises, and commercial businesses."""
    span: str  # e.g., "WHL", "Taco Cabana, Inc.", "Two Pesos, Inc.", "Church's Chicken"

@dataclass
class OrganizationEducation(Entity):
    """Covers academic institutions such as universities, colleges, schools, and academies."""
    span: str  # Examples: "Barnard College", "MIT", "Ulster College of Physical Education", "Belfast Royal Academy"

@dataclass
class OrganizationGovernmentGovernmentagency(Entity):
    """Pertains to legislative bodies, courts, councils, and official government agencies."""
    span: str  # For instance: "New York City Council", "Diet", "Congregazione dei Nobili", "Supreme Court"

@dataclass
class OrganizationMediaNewspaper(Entity):
    """Includes television networks, magazines, newspapers, and news outlets."""
    span: str  # Such as: "Fuse", "TimeOut Melbourne", "Clash", "Al Jazeera"

@dataclass
class OrganizationOther(Entity):
    """Refers to organizational groups not defined elsewhere, like consortia, military divisions, or armies."""
    span: str  # e.g., "SS Division Nordland", "4th Army", "IAEA"

@dataclass
class OrganizationPoliticalparty(Entity):
    """Relates to political groups and parties."""
    span: str  # For example: "National Liberal Party", "Al Wafa' Islamic party", "Shimpotō"

@dataclass
class OrganizationReligion(Entity):
    """Covers faith-based institutions, religious denominations, and parochial schools."""
    span: str  # Such as: "non-denominational Christian", "Catholic Church", "Christian", "Jewish"

@dataclass
class OrganizationShoworganization(Entity):
    """Includes entertainment groups, orchestras, and musical bands."""
    span: str  # e.g., "Yeah Yeah Yeahs", "Bochumer Symphoniker", "Lizzy", "Mr. Mister"

@dataclass
class OrganizationSportsleague(Entity):
    """Refers to athletic associations, sports divisions, and leagues."""
    span: str  # Examples: "China League One", "NHL", "First Division"

@dataclass
class OrganizationSportsteam(Entity):
    """Covers national and professional teams in various sports."""
    span: str  # For instance: "Swedish national men's ice hockey team", "Luc Alphand Aventures", "Tottenham", "Arsenal"

@dataclass
class OtherAstronomything(Entity):
    """Pertains to celestial entities, including constellations, planets, stars, and zodiac signs."""
    span: str  # Such as: "Sun", "42 Camelopardalis", "Caput Larvae", "Algol", "Zodiac"

@dataclass
class OtherAward(Entity):
    """Includes formal recognitions, titles of honor, medals, and awards."""
    span: str  # e.g., "European Car of the Year", "Grammy", "Grand Commander of the Order of the Niger", "Order of the Republic"

@dataclass
class OtherBiologything(Entity):
    """Refers to biological components such as genes, proteins, molecular domains, and insect orders."""
    span: str  # For example: "Hymenoptera", "p53 protein", "BAR domain", "lipid", "N-terminal", "Amphiphysin"

@dataclass
class OtherChemicalthing(Entity):
    """Relates to chemical compounds and elements."""
    span: str  # Such as: "Carbon monoxide", "sulfur", "carbon dioxide", "uranium"

@dataclass
class OtherCurrency(Entity):
    """Covers monetary denominations and units of currency."""
    span: str  # Examples: "Rs 25 lac crore", "$", "Travancore Rupee"

@dataclass
class OtherDisease(Entity):
    """Includes illnesses, medical conditions, and epidemics."""
    span: str  # e.g., "bladder cancer", "hypothyroidism", "Dysentery Epidemic"

@dataclass
class OtherEducationaldegree(Entity):
    """Refers to academic certifications and degrees."""
    span: str  # For instance: "Ph.D.", "Bachelor of Education", "Master of Visual Studies", "BSc ( Hons ) in physics"

@dataclass
class OtherGod(Entity):
    """Pertains to deities, creators, and gods from mythological or religious traditions."""
    span: str  # Such as: "Baglamukhi", "Fujin", "Raijin", "El"

@dataclass
class OtherLanguage(Entity):
    """Relates to specific dialects or languages."""
    span: str  # e.g., "Arabic", "Hebrew", "Latin", "Breton-speaking", "English"

@dataclass
class OtherLaw(Entity):
    """Covers treaties, federal acts, statutes, and laws."""
    span: str  # For example: "America Invents Act", "Thirty Years' Peace", "United States Freedom Support Act"

@dataclass
class OtherLivingthing(Entity):
    """Includes biological organisms such as plants and animals."""
    span: str  # Such as: "Euphorbiaceae", "Rafflesiaceae", "patchouli", "insects", "monkeys"

@dataclass
class OtherMedical(Entity):
    """Refers to pharmaceutical treatments, medical procedures, and specialized fields of medicine."""
    span: str  # e.g., "cryoprecipitate", "pediatrician", "Pediatrics", "amitriptyline"

@dataclass
class PersonActor(Entity):
    """Covers performers in television, theater, and film."""
    span: str  # Examples: "Bajpayee", "Fernando Rey", "Tchéky Karyo", "Edmund Payne", "Ellaline Terriss"

@dataclass
class PersonArtistAuthor(Entity):
    """Relates to authors, musicians, poets, and writers."""
    span: str  # For instance: "Deborah Lurie", "Stephen King", "Gaetano Donizetti", "George Axelrod"

@dataclass
class PersonAthlete(Entity):
    """Refers to professional sports competitors, including quarterbacks, cyclists, and players."""
    span: str  # Such as: "Sam", "Bruno Zanoni", "Jaguar", "Tozawa", "Neville"

@dataclass
class PersonDirector(Entity):
    """Covers directors of theatrical, film, or other artistic works."""
    span: str  # e.g., "Jonze", "Frank Darabont", "Bob Swaim", "Richard Quine"

@dataclass
class PersonOther(Entity):
    """Includes individuals not falling under specific professions, such as famous family members or historical figures."""
    span: str  # For example: "Bette Davis", "Rockefeller", "Wallis", "Campbell", "Holden"

@dataclass
class PersonPolitician(Entity):
    """Refers to political representatives, monarchs, and government leaders."""
    span: str  # Such as: "Barack Obama", "Mary II", "William III", "Rivière", "Emeric"

@dataclass
class PersonScholar(Entity):
    """Relates to researchers, scientists, and academics."""
    span: str  # Examples: "Davis", "Wurdack", "Stedman", "Stalmine"

@dataclass
class PersonSoldier(Entity):
    """Covers military commanders and personnel."""
    span: str  # e.g., "Wolfe", "Bruno Loerzer", "Helmuth Weidling", "Krukenberg"

@dataclass
class ProductAirplane(Entity):
    """Refers to specific helicopter and aircraft models."""
    span: str  # For instance: "Mil Mi-28", "Mil Mi-58", "FGR.2s", "EC135T2 CPDS"

@dataclass
class ProductCar(Entity):
    """Includes automotive platforms and car models."""
    span: str  # Such as: "Fiat 128", "Renault 12", "Corvettes", "Rolls-Royce Phantom"

@dataclass
class ProductFood(Entity):
    """Pertains to food products, ingredients, and specific crop types."""
    span: str  # e.g., "red grape", "yakiniku", "V. labrusca"

@dataclass
class ProductGame(Entity):
    """Covers gaming sequels and video games."""
    span: str  # Examples: "Hardcore RPG", "Airforce Delta", "Splinter Cell"

@dataclass
class ProductOther(Entity):
    """Relates to miscellaneous products, technological components, or museum artifacts."""
    span: str  # For instance: "E-mount", "X11", "PDP-1", "Fairbottom Bobs"

@dataclass
class ProductShip(Entity):
    """Refers to ships, naval vessels, and landing craft."""
    span: str  # Such as: "Embuscade", "Essex", "Congress", "HMS Chinkara"

@dataclass
class ProductSoftware(Entity):
    """Includes programming tools, platforms, and computer software."""
    span: str  # e.g., "SQL Server", "BIDS", "AmiPDF", "Apdf", "Wikipedia"

@dataclass
class ProductTrain(Entity):
    """Covers specific locomotive types and train models."""
    span: str  # For example: "Lexus CT 200h", "55022 Royal Scots Grey", "High Speed Trains"

@dataclass
class ProductWeapon(Entity):
    """Refers to military weapon systems, artillery, and firearms."""
    span: str  # Such as: "ZSU-57-2", "M-14", "AR-15", "ZU-23-2M Wróbel"

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