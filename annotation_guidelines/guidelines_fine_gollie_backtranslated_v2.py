from typing import List
from src.tasks.utils_typing import Entity, dataclass

@dataclass
class ArtBroadcastProgram(Entity):
    """Covers radio and television broadcasts, such as series, documentaries, talk shows, and game shows."""
    span: str  # Such as: "The Gale Storm Show", "12 Corazones", "Jonovision", "Trailer Park Boys", "Mozart in Prague", "Soweto TV"

@dataclass
class ArtFilm(Entity):
    """Identifies cinema productions and movies across all genres."""
    span: str  # Such as: "L'Atlantide", "The Shawshank Redemption", "Bosch", "Men in Her Diary", "Dances with Wolves", "Dune"

@dataclass
class ArtMusic(Entity):
    """Encompasses musical compositions, albums, songs, concert events, and ballads."""
    span: str  # Such as: "Atkinson, Danko and Ford", "Champion Lover", "Mass in C minor", "On the Loose", "The Boys of Wexford", "Free Fallin"

@dataclass
class ArtOther(Entity):
    """Represents various artistic creations like historical artifacts, theater plays, music videos, or sculptures."""
    span: str  # Such as: "Venus de Milo", "The Today Show", "Cloud Gate", "Without the Prince", "Guys and Dolls", "Sphinx", "Lula and the Sailor"

@dataclass
class ArtPainting(Entity):
    """Denotes visual designs, sketches, paintings, lenses, or graffiti."""
    span: str  # Such as: "Production/Reproduction", "Cofiwch Dryweryn", "Touit", "Kamichama Karin", "The Sacrament of the Last Supper", "Athenaeum Portrait"

@dataclass
class ArtWrittenart(Entity):
    """Pertains to literary works, including theses, scripts, poems, magazines, and books."""
    span: str  # Such as: "Time", "The Seven Year Itch", "Imelda de' Lambertazzi", "Histories", "Adventure World Magazine", "Standard of Perfection"

@dataclass
class BuildingAirport(Entity):
    """Includes airfields, aviation terminals, and airports."""
    span: str  # Such as: "Sheremetyevo International Airport", "Newark Liberty International Airport", "Zhuhai Airport", "Vienna International Airport"

@dataclass
class BuildingHospital(Entity):
    """Refers to clinics, hospitals, and other medical facilities."""
    span: str  # Such as: "Memorial Sloan-Kettering Cancer Center", "Yeungnam University Hospital", "Huntington Hospital", "Brigham and Women’s Hospital"

@dataclass
class BuildingHotel(Entity):
    """Covers lodging establishments, resorts, and hotels."""
    span: str  # Such as: "The Standard Hotel", "Radisson Blu Sea Plaza Hotel", "Flamingo Hotel", "Hotel Sacher Salzburg", "Pierre Hotel"

@dataclass
class BuildingLibrary(Entity):
    """Identifies institutional archives and libraries."""
    span: str  # Such as: "Bayerische Staatsbibliothek", "British Library", "Berlin State Library", "Edmon Low Library", "Jefferson Market Library"

@dataclass
class BuildingOther(Entity):
    """Encompasses various structures such as drill halls, palaces, recording studios, churches, and museums."""
    span: str  # Such as: "Henry Ford Museum", "Alpha Recording Studios", "St John The Evangelist", "Palazzo Monte dei Poveri Vergognosi", "The Echo"

@dataclass
class BuildingRestaurant(Entity):
    """Includes fast-food outlets, delis, cafes, and restaurants."""
    span: str  # Such as: "Trumbull dining hall", "Carnegie Deli", "Fatburger", "Morrison's", "Skyline", "McDonald's", "El Pollo Loco"

@dataclass
class BuildingSportsfacility(Entity):
    """Represents athletic fields, sports centers, stadiums, and arenas."""
    span: str  # Such as: "Boston Garden", "Scotiabank Place", "ARCO Arena", "Appleton Arena", "Hughes Stadium", "Capital One Field"

@dataclass
class BuildingTheater(Entity):
    """Refers to performing arts stages, opera houses, and theaters."""
    span: str  # Such as: "Sanders Theatre", "Pittsburgh Civic Light Opera", "Whitehall Theatre", "Hicks Theatre", "Piccadilly Theatre", "The Warehouse Theatre"

@dataclass
class EventAttackBattleWarMilitaryConflict(Entity):
    """Denotes bombings, military operations, specific battles, and wars."""
    span: str  # Such as: "Vietnam War", "Operation Zipper", "Battle of Romani", "World War I", "Corinthian War", "Bali bombing", "Battle of Taku Forts"

@dataclass
class EventDisaster(Entity):
    """Pertains to environmental catastrophes, accidents, famines, and natural disasters."""
    span: str  # Such as: "1693 Sicily earthquake", "North Korean famine", "1912 North Mount Lyell Disaster", "Chernobyl accident", "Hurricane Opal"

@dataclass
class EventElection(Entity):
    """Covers campaign cycles, by-elections, and political elections."""
    span: str  # Such as: "March 1898 elections", "Elections to the European Parliament", "1982 Mitcham and Morden by-election", "1940 presidential election"

@dataclass
class EventOther(Entity):
    """Represents diverse organized events like art salons, air shows, movements, and revolutions."""
    span: str  # Such as: "Masaryk Democratic Movement", "The Proms", "Romanian Revolution", "1995 Paris Air Show", "Salon des Indépendants"

@dataclass
class EventProtest(Entity):
    """Includes organized protests, rebellions, boycotts, and revolutions."""
    span: str  # Such as: "Iranian Constitutional Revolution", "Bicentennial Boycott", "Irish Rebellion of 1798", "Defiance Campaign", "Pro-Test Petition"

@dataclass
class EventSportsevent(Entity):
    """Identifies cups, matches, championships, and sporting tournaments."""
    span: str  # Such as: "Stanley Cup", "World Cup", "Giro d'Italia", "Basketball ID", "United States Figure Skating Championships"

@dataclass
class LocationGpe(Entity):
    """Refers to geopolitical entities, such as provinces, states, cities, and countries."""
    span: str  # Such as: "Croatia", "Europe", "Cornwall", "Michigan", "Germany", "Sweden", "United States", "Azerbaijani"

@dataclass
class LocationBodiesofwater(Entity):
    """Covers bays, oceans, seas, lakes, and rivers."""
    span: str  # Such as: "Atatürk Dam Lake", "Arthur Kill", "East China Sea", "Jordan River", "Newark Bay", "Upper New York Bay", "Onkaparinga River"

@dataclass
class LocationIsland(Entity):
    """Denotes peninsulas, archipelagos, and islands."""
    span: str  # Such as: "Laccadives", "Maldives", "Mainland", "Shetland", "Long Island", "Khark Islalnd", "Annobón", "Staten Island"

@dataclass
class LocationMountain(Entity):
    """Pertains to ridges, peaks, mountain ranges, and mountains."""
    span: str  # Such as: "Ruweisat Ridge", "Salamander Glacier", "Mount Diablo", "K2", "Himalayan", "Karakoram", "Innuitian Mountains"

@dataclass
class LocationOther(Entity):
    """Includes specific estates, valleys, forests, and bridges."""
    span: str  # Such as: "Cartuther", "Victoria line", "Camino Palmero", "West Gate Bridge", "Bintan Resorts", "Jawai Bandh forests", "Helike"

@dataclass
class LocationPark(Entity):
    """Represents historical districts, conservation areas, and parks."""
    span: str  # Such as: "Gramercy Park", "Shenandoah National Park", "Millennium Park", "Yellowstone Park", "Wind Cave", "Dalymount Park"

@dataclass
class LocationRoadRailwayHighwayTransit(Entity):
    """Refers to transit routes, railway lines, highways, streets, and roads."""
    span: str  # Such as: "Friern Barnet Road", "North Jersey Coast Line", "Outerbridge Crossing", "State Route 151", "Claremont Avenue", "Salisbury Highway"

@dataclass
class OrganizationCompany(Entity):
    """Denotes businesses, corporations, and private companies."""
    span: str  # Such as: "Church's Chicken", "Taco Cabana", "WHL", "Warner Brothers", "Chiltern Air Support", "Braathens SAFE", "Hooper & Co."

@dataclass
class OrganizationEducation(Entity):
    """Pertains to educational academies, colleges, universities, and schools."""
    span: str  # Such as: "Belfast Royal Academy", "MIT", "Barnard College", "Latvia University of Life Sciences", "University of Canterbury", "Harvard"

@dataclass
class OrganizationGovernmentGovernmentagency(Entity):
    """Identifies legislative assemblies, departments, courts, and government bodies."""
    span: str  # Such as: "Supreme Court", "Diet", "US Park Police", "Rajasthan government", "United States District Court"

@dataclass
class OrganizationMediaNewspaper(Entity):
    """Covers magazines, television networks, newspapers, and news agencies."""
    span: str  # Such as: "Al Jazeera", "Clash", "TimeOut Melbourne", "Nickelodeon", "Sky Sports", "Pro Football Focus TV", "VH1"

@dataclass
class OrganizationOther(Entity):
    """Represents councils, clubs, foundations, and military forces like armies."""
    span: str  # Such as: "IAEA", "4th Army", "SS Division Nordland", "Quixtar", "Leicester City Council", "John McAslan + Partners"

@dataclass
class OrganizationPoliticalparty(Entity):
    """Refers to political organizations and parties."""
    span: str  # Such as: "Shimpotō", "Haq Movement", "National Liberal Party", "Republican", "BNG", "Democratic Party", "Socialist Party"

@dataclass
class OrganizationReligion(Entity):
    """Denotes organized religious groups, sects, and denominations."""
    span: str  # Such as: "Jewish", "Christian", "Episcopalians", "United Methodists", "United Protestant Church of France", "Buddhism"

@dataclass
class OrganizationShoworganization(Entity):
    """Pertains to artistic ensembles, performing groups, orchestras, and bands."""
    span: str  # Such as: "Mr. Mister", "Yeah Yeah Yeahs", "New York Youth Symphony", "Yakshagana Himmela", "Collegium 1704"

@dataclass
class OrganizationSportsleague(Entity):
    """Identifies athletic conferences and professional or collegiate sports leagues."""
    span: str  # Such as: "First Division", "NHL", "China League One", "Bundesliga", "F1", "Atlantic Coast Conference"

@dataclass
class OrganizationSportsteam(Entity):
    """Covers national athletic teams and specific sports teams."""
    span: str  # Such as: "Arsenal", "Tottenham", "Luc Alphand Aventures", "Tre Kronor", "Utah Jazz", "Dallas Mavericks", "Wuhan Zall"

@dataclass
class OtherAstronomything(Entity):
    """Represents celestial regions, asteroids, constellations, planets, and stars."""
    span: str  # Such as: "Algol", "42 Camelopardalis", "Sun", "Tandun III", "Ceres", "Birgitta", "Mars", "Asteroid Belt", "DC-7"

@dataclass
class OtherAward(Entity):
    """Pertains to prestigious recognitions, medals, honors, and prizes."""
    span: str  # Such as: "Order of the Republic", "European Car of the Year", "Kodansha Manga Award", "Spotlight Award", "CMAA"

@dataclass
class OtherBiologything(Entity):
    """Denotes biological domains, cells, families of organisms, genes, and proteins."""
    span: str  # Such as: "Amphiphysin", "p53 protein", "Ismaridae", "Hymenoptera", "Retinoblastoma protein", "collagen", "hydroxyproline"

@dataclass
class OtherChemicalthing(Entity):
    """Includes chemical additives, gases, compounds, and elements."""
    span: str  # Such as: "uranium", "carbon monoxide", "sulfur", "Molybdenum sulfide", "acetone", "atropine", "amphetamines"

@dataclass
class OtherCurrency(Entity):
    """Refers to financial sums and specific monetary units."""
    span: str  # Such as: "Travancore Rupee", "Aruban florin", "Netherlands Antillean guilder", "Euro", "Deutsche mark"

@dataclass
class OtherDisease(Entity):
    """Pertains to syndromes, medical conditions, and illnesses."""
    span: str  # Such as: "Dysentery", "hypothyroidism", "cancer", "Septic shock", "polyp", "Glial scarring", "diabetes", "infertility"

@dataclass
class OtherEducationaldegree(Entity):
    """Identifies certifications, diplomas, and academic degrees."""
    span: str  # Such as: "BSc", "Master of Visual Studies", "Ph.D.", "Medical Degree", "Doctor of Military Science", "MB ChB"

@dataclass
class OtherGod(Entity):
    """Represents figures of mythology or worship, gods, and deities."""
    span: str  # Such as: "El", "Raijin", "Baglamukhi", "Jesus", "Zeus", "Prometheus", "Aeolians", "Achilles"

@dataclass
class OtherLanguage(Entity):
    """Covers linguistic versions and specific languages."""
    span: str  # Such as: "English", "Breton-speaking", "Latin", "Italian", "Tibetan", "Tajik", "Aramaic", "Arabic"

@dataclass
class OtherLaw(Entity):
    """Denotes formal legal resolutions, acts, statutes, and treaties."""
    span: str  # Such as: "Freedom Support Act", "Thirty Years' Peace", "America Invents Act", "Rush–Bagot Treaty", "War Powers Resolution"

@dataclass
class OtherLivingthing(Entity):
    """Pertains to biological families, insects, animals, and plants."""
    span: str  # Such as: "monkeys", "patchouli", "Rafflesiaceae", "zebras", "beetle", "Lagerstroemia", "Carp", "rainbow trout"

@dataclass
class OtherMedical(Entity):
    """Includes medical terminology, procedures, drugs, and treatments."""
    span: str  # Such as: "amitriptyline", "Pediatrics", "cryoprecipitate", "transplants", "oxycodone", "Folic acid", "Melatonin", "MRI"

@dataclass
class PersonActor(Entity):
    """Represents professional performers in television, theater, and film."""
    span: str  # Such as: "Ellaline Terriss", "Edmund Payne", "Tchéky Karyo", "Jean Rochefort", "Bajpayee", "Sharon Duncan-Brewster"

@dataclass
class PersonArtistAuthor(Entity):
    """Identifies humorists and creators of literature, music, and art."""
    span: str  # Such as: "George Axelrod", "Gaetano Donizetti", "Deborah Lurie", "Stephen King", "Ace Frehley", "Sam Levenson"

@dataclass
class PersonAthlete(Entity):
    """Pertains to athletes and professional sports players."""
    span: str  # Such as: "Neville", "Tozawa", "Bruno Zanoni", "Ernie Johnson", "Guto", "Fausto Coppi"

@dataclass
class PersonDirector(Entity):
    """Denotes individuals managing the production of music videos, plays, or films."""
    span: str  # Such as: "Richard Quine", "Bob Swaim", "Frank Darabont", "Denis Villeneuve", "McG", "Peter Johnson"

@dataclass
class PersonOther(Entity):
    """Refers to family figures and notable individuals not categorized by other professional roles."""
    span: str  # Such as: "Mrs. Strong", "Wallis", "Barbara Hutton", "Binion", "Reitman", "Chief Irvin Irving"

@dataclass
class PersonPolitician(Entity):
    """Includes candidates, presidents, monarchs, and government officials."""
    span: str  # Such as: "Emeric", "Louis XIV", "Nikolai Ryzhkov", "Barack Obama", "Bill Haslam", "Mitt Romney"

@dataclass
class PersonScholar(Entity):
    """Represents historians, academics, scientists, and researchers."""
    span: str  # Such as: "Stedman", "Wurdack", "Ted Robert Gurr", "Döndrup", "R. Brent Tully", "William Stimpson"

@dataclass
class PersonSoldier(Entity):
    """Pertains to soldiers, commanders, and military personnel."""
    span: str  # Such as: "Krukenberg", "Helmuth Weidling", "Bruno Loerzer", "James Outram", "Joachim Murat", "Dong Laifu"

@dataclass
class ProductAirplane(Entity):
    """Identifies spacecraft and specific aircraft models."""
    span: str  # Such as: "EC135T2 CPDS", "FGR.2s", "Mil Mi-58", "Su-30", "WC-135", "Gull III", "Soyuz spacecraft"

@dataclass
class ProductCar(Entity):
    """Covers locomotives, trucks, and specific car models."""
    span: str  # Such as: "Rolls-Royce Phantom", "Corvettes", "Renault 12", "Lancia Thema", "Rolls Royce Sweptail", "Ferrari F12 TRS"

@dataclass
class ProductFood(Entity):
    """Denotes recipes, beverages, ingredients, and specific food items."""
    span: str  # Such as: "icewine", "yakiniku", "Merlot", "Wahaha branded products", "focaccia", "Yellow coq au vin", "Hop Monster"

@dataclass
class ProductGame(Entity):
    """Represents tabletop game systems, gaming consoles, and video games."""
    span: str  # Such as: "Splinter Cell", "Airforce Delta", "Game Boy Micro", "Ms. Pac-Man", "RuneQuest II", "Samurai Warriors"

@dataclass
class ProductOther(Entity):
    """Pertains to miscellaneous commercial goods like cryptographic devices, missiles, or hardware."""
    span: str  # Such as: "PDP-1", "SecurID 800", "Sinclair Spectrum", "Apple II", "Durandal", "A330", "Airbus A320neos"

@dataclass
class ProductShip(Entity):
    """Identifies submarines, ships, and marine vessels."""
    span: str  # Such as: "HMS Chinkara", "Congress", "Essex", "Embuscade", "Alvin", "HMS Milford", "Niels Juel"

@dataclass
class ProductSoftware(Entity):
    """Covers protocols, operating systems, applications, and computer programs."""
    span: str  # Such as: "Wikipedia", "Apdf", "BIDS Helper", "Visual Studio", "SQL Server", "Apache Wave", "Android 4.1.2 Jelly Bean"

@dataclass
class ProductTrain(Entity):
    """Represents locomotives, railway services, and specific train models."""
    span: str  # Such as: "High Speed Trains", "Royal Scots Grey", "Lexus CT 200h", "Keystone Service", "ICE 3M", "Class 90"

@dataclass
class ProductWeapon(Entity):
    """Denotes artillery, missiles, firearms, and types of weapons."""
    span: str  # Such as: "ZU-23-2M Wrúbel", "AR-15", "M-14", "ZSU-57-2", "40mm Bofors gun", "Lee-Enfield", "Gongchen"


ENTITY_DEFINITIONS: List[Entity] = [
    ArtBroadcastProgram,
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
    EventAttackBattleWarMilitaryConflict,
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